import numpy as np
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import QListWidgetItem, QPushButton
from flags import *  # 导入图像处理相关常量定义


class MyItem(QListWidgetItem):
    """
    所有图像处理项的基类，继承自QListWidgetItem
    提供统一的图标设置、尺寸设置和参数管理功能
    """
    def __init__(self, name=None, parent=None):
        super(MyItem, self).__init__(name, parent=parent)
        self.setIcon(QIcon('icons/color.png'))  # 设置统一图标
        self.setSizeHint(QSize(60, 60))  # 设置列表项大小

    def get_params(self):
        """获取所有以单下划线开头的保护属性，转换为字典格式"""
        protected = [v for v in dir(self) if v.startswith('_') and not v.startswith('__')]
        param = {}
        for v in protected:
            param[v.replace('_', '', 1)] = self.__getattribute__(v)
        return param

    def update_params(self, param):
        """根据参数字典更新对应保护属性的值"""
        for k, v in param.items():
            if '_' + k in dir(self):
                self.__setattr__('_' + k, v)


class GrayingItem(MyItem):
    """图像灰度化处理项"""
    def __init__(self, parent=None):
        super(GrayingItem, self).__init__(' 灰度化 ', parent=parent)
        self._mode = BGR2GRAY_COLOR  # 灰度化模式

    def __call__(self, img):
        """
        执行灰度化处理
        先将RGB转为灰度图，再转回BGR以保持通道数一致
        """
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        return img


class FilterItem(MyItem):
    """图像滤波处理项，支持多种滤波方式"""

    def __init__(self, parent=None):
        super().__init__('平滑处理', parent=parent)
        self._ksize = 3        # 核大小
        self._kind = MEAN_FILTER  # 滤波类型
        self._sigmax = 0       # 高斯滤波标准差

    def __call__(self, img):
        """根据不同的滤波类型执行相应的平滑处理"""
        if self._kind == MEAN_FILTER:
            img = cv2.blur(img, (self._ksize, self._ksize))  # 均值滤波
        elif self._kind == GAUSSIAN_FILTER:
            img = cv2.GaussianBlur(img, (self._ksize, self._ksize), self._sigmax)  # 高斯滤波
        elif self._kind == MEDIAN_FILTER:
            img = cv2.medianBlur(img, self._ksize)  # 中值滤波
        return img


class MorphItem(MyItem):
    """图像形态学操作项"""
    def __init__(self, parent=None):
        super().__init__(' 形态学 ', parent=parent)
        self._ksize = 3           # 结构元素大小
        self._op = ERODE_MORPH_OP  # 形态学操作类型
        self._kshape = RECT_MORPH_SHAPE  # 结构元素形状

    def __call__(self, img):
        """执行形态学操作，如腐蚀、膨胀等"""
        op = MORPH_OP[self._op]
        kshape = MORPH_SHAPE[self._kshape]
        kernal = cv2.getStructuringElement(kshape, (self._ksize, self._ksize))
        img = cv2.morphologyEx(img, self._op, kernal)
        return img


class GradItem(MyItem):
    """图像梯度计算项"""

    def __init__(self, parent=None):
        super().__init__('图像梯度', parent=parent)
        self._kind = SOBEL_GRAD  # 梯度计算方法
        self._ksize = 3          # 核大小
        self._dx = 1             # x方向导数阶数
        self._dy = 0             # y方向导数阶数

    def __call__(self, img):
        """
        计算图像梯度
        当dx和dy同时为0且非拉普拉斯算子时显示错误提示
        """
        if self._dx == 0 and self._dy == 0 and self._kind != LAPLACIAN_GRAD:
            self.setBackground(QColor(255, 0, 0))  # 错误状态：红色背景
            self.setText('图像梯度 （无效: dx与dy不同时为0）')
        else:
            self.setBackground(QColor(200, 200, 200))  # 正常状态：灰色背景
            self.setText('图像梯度')
            if self._kind == SOBEL_GRAD:
                img = cv2.Sobel(img, -1, self._dx, self._dy, self._ksize)  # Sobel算子
            elif self._kind == SCHARR_GRAD:
                img = cv2.Scharr(img, -1, self._dx, self._dy)  # Scharr算子
            elif self._kind == LAPLACIAN_GRAD:
                img = cv2.Laplacian(img, -1)  # 拉普拉斯算子
        return img


class ThresholdItem(MyItem):
    """图像阈值处理项"""
    def __init__(self, parent=None):
        super().__init__('阈值处理', parent=parent)
        self._thresh = 127         # 阈值
        self._maxval = 255         # 最大值
        self._method = BINARY_THRESH_METHOD  # 阈值方法

    def __call__(self, img):
        """
        执行阈值处理
        先转为灰度图，处理后再转回BGR格式
        """
        method = THRESH_METHOD[self._method]
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        img = cv2.threshold(img, self._thresh, self._thresh, method)[1]
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        return img


class EdgeItem(MyItem):
    """Canny边缘检测项"""
    def __init__(self, parent=None):
        super(EdgeItem, self).__init__('边缘检测', parent=parent)
        self._thresh1 = 20  # 第一个阈值
        self._thresh2 = 100  # 第二个阈值

    def __call__(self, img):
        """执行Canny边缘检测，然后转回BGR格式"""
        img = cv2.Canny(img, threshold1=self._thresh1, threshold2=self._thresh2)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        return img


class EqualizeItem(MyItem):
    """图像直方图均衡化项"""
    def __init__(self, parent=None):
        super().__init__(' 均衡化 ', parent=parent)
        self._blue = True   # 是否均衡化蓝色通道
        self._green = True  # 是否均衡化绿色通道
        self._red = True    # 是否均衡化红色通道

    def __call__(self, img):
        """
        对选定的通道执行直方图均衡化
        分别处理RGB三个通道，然后合并
        """
        b, g, r = cv2.split(img)
        if self._blue:
            b = cv2.equalizeHist(b)
        if self._green:
            g = cv2.equalizeHist(g)
        if self._red:
            r = cv2.equalizeHist(r)
        return cv2.merge((b, g, r))


class HoughLineItem(MyItem):
    """霍夫直线检测项"""
    def __init__(self, parent=None):
        super(HoughLineItem, self).__init__('直线检测', parent=parent)
        self._rho = 1             # 距离分辨率
        self._theta = np.pi / 180  # 角度分辨率
        self._thresh = 80         # 阈值
        self._min_length = 200    # 最小线段长度
        self._max_gap = 15        # 最大线段间隙

    def __call__(self, img):
        """
        执行霍夫直线检测
        先转为灰度图，检测后在原图上绘制绿色直线
        """
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        lines = cv2.HoughLinesP(img_gray, self._rho, self._theta, self._thresh, 
                               minLineLength=self._min_length, maxLineGap=self._max_gap)
        img_result = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR)
        if lines is None: return img_result  # 没有检测到直线时直接返回
        for line in lines:
            for x1, y1, x2, y2 in line:
                img_result = cv2.line(img_result, (x1, y1), (x2, y2), (0, 255, 0), thickness=2)
        return img_result


class LightItem(MyItem):
    """图像亮度调节项"""
    def __init__(self, parent=None):
        super(LightItem, self).__init__('亮度调节(增加和减少亮度)', parent=parent)
        self._alpha = 1  # 对比度控制
        self._beta = 0   # 亮度控制

    def __call__(self, img):
        """
        调整图像亮度和对比度
        使用addWeighted函数实现: dst = src1*alpha + src2*(1-alpha) + beta
        """
        blank = np.zeros(img.shape, img.dtype)
        img = cv2.addWeighted(img, self._alpha, blank, 1 - self._alpha, self._beta)
        return img


class GammaItem(MyItem):
    """图像伽马校正项，用于调整亮度和对比度"""
    def __init__(self, parent=None):
        super(GammaItem, self).__init__('伽马校正(调整图像的亮度和对比度)', parent=parent)
        self._gamma = 1  # 伽马值

    def __call__(self, img):
        """
        执行伽马校正
        通过查找表(LUT)快速应用非线性变换: I_out = 255 * (I_in/255)^γ
        """
        gamma_table = [np.power(x / 255.0, self._gamma) * 255.0 for x in range(256)]
        gamma_table = np.round(np.array(gamma_table)).astype(np.uint8)
        return cv2.LUT(img, gamma_table)


class SaltAndPepperItem(MyItem):
    """椒盐噪声添加项"""
    def __init__(self, parent=None):
        super(SaltAndPepperItem, self).__init__('椒盐噪声', parent=parent)
        self._noise_ratio = 0.05  # 噪声比例
        self._salt_vs_pepper = 0.5  # 盐噪声与椒噪声的比例

    def __call__(self, img):
        """
        添加椒盐噪声
        随机选择像素点设置为白色(盐)或黑色(椒)
        """
        output = img.copy()
        total_pixels = img.shape[0] * img.shape[1]
        num_salt = int(total_pixels * self._noise_ratio * self._salt_vs_pepper)  # 盐噪声数量
        num_pepper = int(total_pixels * self._noise_ratio * (1.0 - self._salt_vs_pepper))  # 椒噪声数量
        
        # 添加盐噪声（白点）
        for _ in range(num_salt):
            i = np.random.randint(0, img.shape[0])
            j = np.random.randint(0, img.shape[1])
            if img.ndim == 2:  # 单通道图像
                output[i, j] = 255
            else:  # 多通道图像
                output[i, j] = [255, 255, 255]
                
        # 添加椒噪声（黑点）
        for _ in range(num_pepper):
            i = np.random.randint(0, img.shape[0])
            j = np.random.randint(0, img.shape[1])
            if img.ndim == 2:
                output[i, j] = 0
            else:
                output[i, j] = [0, 0, 0]

        return output
