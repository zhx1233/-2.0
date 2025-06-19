import sys
import cv2
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import matplotlib.pyplot as plt

from custom.stackedWidget import StackedWidget
from custom.treeView import FileSystemTreeView
from custom.listWidgets import FuncListWidget, UsedListWidget
from custom.graphicsView import GraphicsView


class MyApp(QMainWindow):
    """
    主应用窗口类，集成了图像处理的主要功能
    """
    
    def __init__(self):
        """初始化主窗口，设置UI组件和信号连接"""
        super(MyApp, self).__init__()
        
        # 创建工具栏和操作按钮
        self.tool_bar = self.addToolBar('工具栏')
        self.action_right_rotate = QAction(QIcon("icons/右旋转.png"), "向右旋转90", self)
        self.action_left_rotate = QAction(QIcon("icons/左旋转.png"), "向左旋转90°", self)
        self.action_histogram = QAction(QIcon("icons/直方图.png"), "直方图", self)
        self.action_right_rotate.triggered.connect(self.right_rotate)
        self.action_left_rotate.triggered.connect(self.left_rotate)
        self.action_histogram.triggered.connect(self.histogram)
        self.tool_bar.addActions((self.action_left_rotate, self.action_right_rotate, self.action_histogram))
        
        # 初始化自定义组件
        self.useListWidget = UsedListWidget(self)  # 已选操作列表
        self.funcListWidget = FuncListWidget(self)  # 可用操作列表
        self.stackedWidget = StackedWidget(self)    # 参数设置堆栈窗口
        self.fileSystemTreeView = FileSystemTreeView(self)  # 文件系统树视图
        self.graphicsView = GraphicsView(self)      # 图像显示视图
        
        # 创建并配置文件目录停靠窗口
        self.dock_file = QDockWidget(self)
        self.dock_file.setWidget(self.fileSystemTreeView)
        self.dock_file.setTitleBarWidget(QLabel('目录'))
        self.dock_file.setFeatures(QDockWidget.NoDockWidgetFeatures)
        
        # 创建并配置图像处理功能停靠窗口
        self.dock_func = QDockWidget(self)
        self.dock_func.setWidget(self.funcListWidget)
        self.dock_func.setTitleBarWidget(QLabel('图像操作'))
        self.dock_func.setFeatures(QDockWidget.NoDockWidgetFeatures)
        
        # 创建并配置已选操作停靠窗口
        self.dock_used = QDockWidget(self)
        self.dock_used.setWidget(self.useListWidget)
        self.dock_used.setTitleBarWidget(QLabel('已选操作，右键删除'))
        self.dock_used.setFeatures(QDockWidget.NoDockWidgetFeatures)
        
        # 创建并配置属性设置停靠窗口
        self.dock_attr = QDockWidget(self)
        self.dock_attr.setWidget(self.stackedWidget)
        self.dock_attr.setTitleBarWidget(QLabel('属性'))
        self.dock_attr.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.dock_attr.close()  # 默认关闭属性窗口
        
        # 设置中央窗口和停靠窗口布局
        self.setCentralWidget(self.graphicsView)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock_file)
        self.addDockWidget(Qt.TopDockWidgetArea, self.dock_func)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock_used)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock_attr)
        
        # 设置窗口基本属性
        self.setWindowTitle('Opencv图像处理')
        self.setWindowIcon(QIcon('icons/main.png'))
        self.src_img = None  # 原始图像
        self.cur_img = None  # 当前处理后的图像
    
    def update_image(self):
        """更新图像显示，基于当前选择的处理操作链"""
        if self.src_img is None:
            return
        img = self.process_image()  # 处理图像
        self.cur_img = img
        self.graphicsView.update_image(img)  # 更新视图显示
    
    def change_image(self, img):
        """更改当前显示的图像，并重新应用所有处理操作"""
        self.src_img = img
        img = self.process_image()
        self.cur_img = img
        self.graphicsView.change_image(img)  # 更新视图并适应窗口大小
    
    def process_image(self):
        """根据已选操作列表处理图像"""
        img = self.src_img.copy()  # 复制原始图像，避免修改原图
        # 遍历所有已选操作并依次应用
        for i in range(self.useListWidget.count()):
            img = self.useListWidget.item(i)(img)
        return img
    
    def right_rotate(self):
        """将图像向右旋转90度"""
        self.graphicsView.rotate(90)
    
    def left_rotate(self):
        """将图像向左旋转90度"""
        self.graphicsView.rotate(-90)
    
    def histogram(self):
        """显示当前图像的直方图"""
        color = ('b', 'g', 'r')
        # 分别计算并绘制BGR三个通道的直方图
        for i, col in enumerate(color):
            histr = cv2.calcHist([self.cur_img], [i], None, [256], [0, 256])
            histr = histr.flatten()  # 将直方图数据展平
            plt.plot(range(256), histr, color=col)  # 绘制直方图曲线
            plt.xlim([0, 256])  # 设置x轴范围
        plt.show()  # 显示图表


if __name__ == "__main__":
    """应用程序入口点"""
    app = QApplication(sys.argv)
    # 加载样式表
    app.setStyleSheet(open('custom/styleSheet.qss', encoding='utf-8').read())
    window = MyApp()  # 创建主窗口
    window.show()  # 显示窗口
    sys.exit(app.exec_())  # 进入应用程序主循环
