import cv2

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class GraphicsView(QGraphicsView):
    """图像显示视图类，用于展示和交互处理后的图像"""
    
    def __init__(self, parent=None):
        """初始化图像显示视图，设置基本属性和场景"""
        super(GraphicsView, self).__init__(parent=parent)
        self._zoom = 0  # 缩放级别
        self._empty = True  # 标记是否有图像
        self._photo = QGraphicsPixmapItem()  # 图像显示项
        self._scene = QGraphicsScene(self)  # 图形场景
        self._scene.addItem(self._photo)  # 将图像项添加到场景
        self.setScene(self._scene)  # 设置场景
        self.setAlignment(Qt.AlignCenter)  # 图像居中显示
        self.setDragMode(QGraphicsView.ScrollHandDrag)  # 设置拖动模式为手型滚动
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 隐藏垂直滚动条
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 隐藏水平滚动条
        self.setMinimumSize(640, 480)  # 设置最小显示尺寸
    
    def contextMenuEvent(self, event):
        """右键菜单事件处理，当有图像时显示保存菜单"""
        if not self.has_photo():
            return
        menu = QMenu()  # 创建右键菜单
        save_action = QAction('另存为', self)  # 创建保存动作
        save_action.triggered.connect(self.save_current)  # 连接保存事件
        menu.addAction(save_action)  # 添加动作到菜单
        menu.exec(QCursor.pos())  # 在鼠标位置显示菜单
    
    def save_current(self):
        """保存当前显示的图像到文件"""
        # 打开文件保存对话框，获取文件名
        file_name = QFileDialog.getSaveFileName(self, '另存为', './', 'Image files(*.jpg *.gif *.png)')[0]
        print(file_name)
        if file_name:
            # 保存图像到指定文件
            self._photo.pixmap().save(file_name)
    
    def get_image(self):
        """获取当前显示的图像"""
        if self.has_photo():
            # 将QGraphicsPixmapItem转换为QImage返回
            return self._photo.pixmap().toImage()
    
    def has_photo(self):
        """检查是否有图像显示"""
        return not self._empty
    
    def change_image(self, img):
        """更新显示图像并适应视图"""
        self.update_image(img)  # 更新图像显示
        self.fitInView()  # 适应视图大小
    
    def img_to_pixmap(self, img):
        """将OpenCV格式的图像转换为QPixmap"""
        # BGR转RGB色彩空间
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, c = img.shape  # 获取图像高度、宽度和通道数
        # 创建QImage对象，注意行字节数为3*w（RGB三通道）
        image = QImage(img, w, h, 3 * w, QImage.Format_RGB888)
        return QPixmap.fromImage(image)  # 转换为QPixmap返回
    
    def update_image(self, img):
        """更新图像显示内容"""
        self._empty = False  # 标记为有图像
        # 设置图像项的像素图
        self._photo.setPixmap(self.img_to_pixmap(img))
    
    def fitInView(self, scale=True):
        """使图像适应视图大小"""
        rect = QRectF(self._photo.pixmap().rect())  # 获取图像矩形
        if not rect.isNull():
            self.setSceneRect(rect)  # 设置场景矩形
            if self.has_photo():
                # 计算当前变换的单位矩形
                unity = self.transform().mapRect(QRectF(0, 0, 1, 1))
                # 重置缩放为1/unity.width()和1/unity.height()
                self.scale(1 / unity.width(), 1 / unity.height())
                viewrect = self.viewport().rect()  # 获取视口矩形
                # 获取变换后的图像矩形
                scenerect = self.transform().mapRect(rect)
                # 计算适应视口的缩放因子
                factor = min(viewrect.width() / scenerect.width(),
                             viewrect.height() / scenerect.height())
                self.scale(factor, factor)  # 应用缩放因子
            self._zoom = 0  # 重置缩放级别
    
    def wheelEvent(self, event):
        """鼠标滚轮事件处理，实现图像缩放"""
        if self.has_photo():
            # 处理滚轮滚动方向
            if event.angleDelta().y() > 0:
                factor = 1.25  # 放大因子
                self._zoom += 1  # 增加缩放级别
            else:
                factor = 0.8  # 缩小因子
                self._zoom -= 1  # 减少缩放级别
            # 根据缩放级别执行相应操作
            if self._zoom > 0:
                self.scale(factor, factor)  # 放大图像
            elif self._zoom == 0:
                self.fitInView()  # 适应视图
            else:
                self._zoom = 0  # 防止缩放级别为负
