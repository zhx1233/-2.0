from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class TableWidget(QTableWidget):
    """表格部件基类，定义图像处理参数表格的通用功能"""
    
    def __init__(self, parent=None):
        """初始化表格部件，设置基本外观和行为"""
        super(TableWidget, self).__init__(parent=parent)
        self.mainwindow = parent  # 引用主窗口
        self.setShowGrid(True)  # 显示网格线
        self.setAlternatingRowColors(True)  # 隔行显示不同颜色，提高可读性
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 禁止直接编辑表格项
        self.horizontalHeader().setVisible(False)  # 隐藏水平表头
        self.verticalHeader().setVisible(False)  # 隐藏垂直表头
        self.horizontalHeader().sectionResizeMode(QHeaderView.Stretch)  # 水平方向拉伸填充
        self.verticalHeader().sectionResizeMode(QHeaderView.Stretch)  # 垂直方向拉伸填充
        self.horizontalHeader().setStretchLastSection(True)  # 最后一列拉伸填充
        self.setFocusPolicy(Qt.NoFocus)  # 表格不获取焦点
    
    def signal_connect(self):
        """连接所有控件的信号到更新处理函数"""
        for spinbox in self.findChildren(QSpinBox):
            spinbox.valueChanged.connect(self.update_item)  # 整数输入框值变化信号
        for doublespinbox in self.findChildren(QDoubleSpinBox):
            doublespinbox.valueChanged.connect(self.update_item)  # 浮点数输入框值变化信号
        for combox in self.findChildren(QComboBox):
            combox.currentIndexChanged.connect(self.update_item)  # 下拉框选择变化信号
        for checkbox in self.findChildren(QCheckBox):
            checkbox.stateChanged.connect(self.update_item)  # 复选框状态变化信号
    
    def update_item(self):
        """更新表格项数据，并通知主窗口更新图像"""
        param = self.get_params()  # 获取当前参数
        self.mainwindow.useListWidget.currentItem().update_params(param)  # 更新当前列表项参数
        self.mainwindow.update_image()  # 通知主窗口更新图像显示
    
    def update_params(self, param=None):
        """根据参数更新表格控件的值"""
        if param is None:
            param = {}
        for key in param.keys():
            box = self.findChild(QWidget, name=key)  # 根据对象名查找控件
            if isinstance(box, QSpinBox) or isinstance(box, QDoubleSpinBox):
                box.setValue(param[key])  # 设置数值控件值
            elif isinstance(box, QComboBox):
                box.setCurrentIndex(param[key])  # 设置下拉框选中索引
            elif isinstance(box, QCheckBox):
                box.setChecked(param[key])  # 设置复选框状态
    
    def get_params(self):
        """获取当前表格中所有控件的参数值"""
        param = {}
        for spinbox in self.findChildren(QSpinBox):
            param[spinbox.objectName()] = spinbox.value()  # 收集整数输入框值
        for doublespinbox in self.findChildren(QDoubleSpinBox):
            param[doublespinbox.objectName()] = doublespinbox.value()  # 收集浮点数输入框值
        for combox in self.findChildren(QComboBox):
            param[combox.objectName()] = combox.currentIndex()  # 收集下拉框选中索引
        for combox in self.findChildren(QCheckBox):
            param[combox.objectName()] = combox.isChecked()  # 收集复选框状态
        return param


class GrayingTableWidget(TableWidget):
    """灰度转换表格部件，目前与基类功能相同"""
    
    def __init__(self, parent=None):
        super(GrayingTableWidget, self).__init__(parent=parent)


class FilterTabledWidget(TableWidget):
    """滤波操作表格部件，用于设置滤波参数"""
    
    def __init__(self, parent=None):
        super(FilterTabledWidget, self).__init__(parent=parent)
        
        # 滤波类型下拉框
        self.kind_comBox = QComboBox()
        self.kind_comBox.addItems(['均值滤波', '高斯滤波', '中值滤波'])
        self.kind_comBox.setObjectName('kind')
        
        # 核大小输入框
        self.ksize_spinBox = QSpinBox()
        self.ksize_spinBox.setObjectName('ksize')
        self.ksize_spinBox.setMinimum(1)  # 最小核大小
        self.ksize_spinBox.setSingleStep(2)  # 步长为2，保证奇数核大小
        
        # 设置表格结构
        self.setColumnCount(2)
        self.setRowCount(2)
        self.setItem(0, 0, QTableWidgetItem('类型'))
        self.setCellWidget(0, 1, self.kind_comBox)
        self.setItem(1, 0, QTableWidgetItem('核大小'))
        self.setCellWidget(1, 1, self.ksize_spinBox)
        
        self.signal_connect()  # 连接信号


class MorphTabledWidget(TableWidget):
    """形态学操作表格部件，用于设置形态学处理参数"""
    
    def __init__(self, parent=None):
        super(MorphTabledWidget, self).__init__(parent=parent)
        
        # 操作类型下拉框
        self.op_comBox = QComboBox()
        self.op_comBox.addItems(['腐蚀操作', '膨胀操作', '开操作', '闭操作', '梯度操作', '顶帽操作', '黑帽操作'])
        self.op_comBox.setObjectName('op')
        
        # 核大小输入框
        self.ksize_spinBox = QSpinBox()
        self.ksize_spinBox.setMinimum(1)
        self.ksize_spinBox.setSingleStep(2)
        self.ksize_spinBox.setObjectName('ksize')
        
        # 核形状下拉框
        self.kshape_comBox = QComboBox()
        self.kshape_comBox.addItems(['方形', '十字形', '椭圆形'])
        self.kshape_comBox.setObjectName('kshape')
        
        # 设置表格结构
        self.setColumnCount(2)
        self.setRowCount(3)
        self.setItem(0, 0, QTableWidgetItem('类型'))
        self.setCellWidget(0, 1, self.op_comBox)
        self.setItem(1, 0, QTableWidgetItem('核大小'))
        self.setCellWidget(1, 1, self.ksize_spinBox)
        self.setItem(2, 0, QTableWidgetItem('核形状'))
        self.setCellWidget(2, 1, self.kshape_comBox)
        self.signal_connect()


class GradTabledWidget(TableWidget):
    """梯度检测表格部件，用于设置梯度检测参数"""
    
    def __init__(self, parent=None):
        super(GradTabledWidget, self).__init__(parent=parent)
        
        # 算子类型下拉框
        self.kind_comBox = QComboBox()
        self.kind_comBox.addItems(['Sobel算子', 'Scharr算子', 'Laplacian算子'])
        self.kind_comBox.setObjectName('kind')
        
        # 核大小输入框
        self.ksize_spinBox = QSpinBox()
        self.ksize_spinBox.setMinimum(1)
        self.ksize_spinBox.setSingleStep(2)
        self.ksize_spinBox.setObjectName('ksize')
        
        # x方向导数阶数输入框
        self.dx_spinBox = QSpinBox()
        self.dx_spinBox.setMaximum(1)
        self.dx_spinBox.setMinimum(0)
        self.dx_spinBox.setSingleStep(1)
        self.dx_spinBox.setObjectName('dx')
        
        # y方向导数阶数输入框
        self.dy_spinBox = QSpinBox()
        self.dy_spinBox.setMaximum(1)
        self.dy_spinBox.setMinimum(0)
        self.dy_spinBox.setSingleStep(1)
        self.dy_spinBox.setObjectName('dy')
        
        # 设置表格结构
        self.setColumnCount(2)
        self.setRowCount(4)
        self.setItem(0, 0, QTableWidgetItem('类型'))
        self.setCellWidget(0, 1, self.kind_comBox)
        self.setItem(1, 0, QTableWidgetItem('核大小'))
        self.setCellWidget(1, 1, self.ksize_spinBox)
        self.setItem(2, 0, QTableWidgetItem('x方向'))
        self.setCellWidget(2, 1, self.dx_spinBox)
        self.setItem(3, 0, QTableWidgetItem('y方向'))
        self.setCellWidget(3, 1, self.dy_spinBox)
        
        self.signal_connect()


class ThresholdTableWidget(TableWidget):
    """阈值处理表格部件，用于设置阈值处理参数"""
    
    def __init__(self, parent=None):
        super(ThresholdTableWidget, self).__init__(parent=parent)
        
        # 阈值输入框
        self.thresh_spinBox = QSpinBox()
        self.thresh_spinBox.setObjectName('thresh')
        self.thresh_spinBox.setMaximum(255)  # 最大阈值为255
        self.thresh_spinBox.setMinimum(0)    # 最小阈值为0
        self.thresh_spinBox.setSingleStep(1)  # 步长为1
        
        # 最大值输入框
        self.maxval_spinBox = QSpinBox()
        self.maxval_spinBox.setObjectName('maxval')
        self.maxval_spinBox.setMaximum(255)
        self.maxval_spinBox.setMinimum(0)
        self.maxval_spinBox.setSingleStep(1)
        
        # 阈值方法下拉框
        self.method_comBox = QComboBox()
        self.method_comBox.addItems(['二进制阈值化', '反二进制阈值化', '截断阈值化', '阈值化为0', '反阈值化为0', '大津算法'])
        self.method_comBox.setObjectName('method')
        
        # 设置表格结构
        self.setColumnCount(2)
        self.setRowCount(3)
        self.setItem(0, 0, QTableWidgetItem('类型'))
        self.setCellWidget(0, 1, self.method_comBox)
        self.setItem(1, 0, QTableWidgetItem('阈值'))
        self.setCellWidget(1, 1, self.thresh_spinBox)
        self.setItem(2, 0, QTableWidgetItem('最大值'))
        self.setCellWidget(2, 1, self.maxval_spinBox)
        
        self.signal_connect()


class EdgeTableWidget(TableWidget):
    """边缘检测表格部件，用于设置Canny边缘检测参数"""
    
    def __init__(self, parent=None):
        super(EdgeTableWidget, self).__init__(parent=parent)
        
        # 低阈值输入框
        self.thresh1_spinBox = QSpinBox()
        self.thresh1_spinBox.setMinimum(0)
        self.thresh1_spinBox.setMaximum(255)
        self.thresh1_spinBox.setSingleStep(1)
        self.thresh1_spinBox.setObjectName('thresh1')
        
        # 高阈值输入框
        self.thresh2_spinBox = QSpinBox()
        self.thresh2_spinBox.setMinimum(0)
        self.thresh2_spinBox.setMaximum(255)
        self.thresh2_spinBox.setSingleStep(1)
        self.thresh2_spinBox.setObjectName('thresh2')
        
        # 设置表格结构
        self.setColumnCount(2)
        self.setRowCount(2)
        self.setItem(0, 0, QTableWidgetItem('阈值1'))
        self.setCellWidget(0, 1, self.thresh1_spinBox)
        self.setItem(1, 0, QTableWidgetItem('阈值2'))
        self.setCellWidget(1, 1, self.thresh2_spinBox)
        self.signal_connect()


class EqualizeTableWidget(TableWidget):
    """直方图均衡化表格部件，用于设置各颜色通道的均衡化选项"""
    
    def __init__(self, parent=None):
        super(EqualizeTableWidget, self).__init__(parent=parent)
        # 红色通道复选框
        self.red_checkBox = QCheckBox()
        self.red_checkBox.setObjectName('red')
        self.red_checkBox.setTristate(False)  # 禁止三态，只允许选中/未选中
        
        # 绿色通道复选框
        self.blue_checkBox = QCheckBox()
        self.blue_checkBox.setObjectName('blue')
        self.blue_checkBox.setTristate(False)
        
        # 蓝色通道复选框
        self.green_checkBox = QCheckBox()
        self.green_checkBox.setObjectName('green')
        self.green_checkBox.setTristate(False)
        
        # 设置表格结构
        self.setColumnCount(2)
        self.setRowCount(3)
        self.setItem(0, 0, QTableWidgetItem('R通道'))
        self.setCellWidget(0, 1, self.red_checkBox)
        self.setItem(1, 0, QTableWidgetItem('G通道'))
        self.setCellWidget(1, 1, self.green_checkBox)
        self.setItem(2, 0, QTableWidgetItem('B通道'))
        self.setCellWidget(2, 1, self.blue_checkBox)
        self.signal_connect()


class HoughLineTableWidget(TableWidget):
    """霍夫线检测表格部件，用于设置霍夫变换参数"""
    
    def __init__(self, parent=None):
        super(HoughLineTableWidget, self).__init__(parent=parent)
        
        # 交点阈值输入框
        self.thresh_spinBox = QSpinBox()
        self.thresh_spinBox.setMinimum(0)
        self.thresh_spinBox.setMaximum(1000)  # 最大阈值为1000
        self.thresh_spinBox.setSingleStep(1)
        self.thresh_spinBox.setObjectName('thresh')
        
        # 最小线段长度输入框
        self.min_length_spinBox = QSpinBox()
        self.min_length_spinBox.setMinimum(0)
        self.min_length_spinBox.setMaximum(1000)
        self.min_length_spinBox.setSingleStep(1)
        self.min_length_spinBox.setObjectName('min_length')
        
        # 最大线段间距输入框
        self.max_gap_spinbox = QSpinBox()
        self.max_gap_spinbox.setMinimum(0)
        self.max_gap_spinbox.setMaximum(1000)
        self.max_gap_spinbox.setSingleStep(1)
        self.max_gap_spinbox.setObjectName('max_gap')
        
        # 设置表格结构
        self.setColumnCount(2)
        self.setRowCount(3)
        self.setItem(0, 0, QTableWidgetItem('交点阈值'))
        self.setCellWidget(0, 1, self.thresh_spinBox)
        self.setItem(1, 0, QTableWidgetItem('最小长度'))
        self.setCellWidget(1, 1, self.min_length_spinBox)
        self.setItem(2, 0, QTableWidgetItem('最大间距'))
        self.setCellWidget(2, 1, self.max_gap_spinbox)
        self.signal_connect()


class LightTableWidget(TableWidget):
    """亮度调整表格部件，用于设置亮度调整参数"""
    
    def __init__(self, parent=None):
        super(LightTableWidget, self).__init__(parent=parent)
        
        # 亮度系数输入框（浮点数）
        self.alpha_spinBox = QDoubleSpinBox()
        self.alpha_spinBox.setMinimum(0)       # 最小系数为0
        self.alpha_spinBox.setMaximum(3)       # 最大系数为3
        self.alpha_spinBox.setSingleStep(0.1)  # 步长为0.1
        self.alpha_spinBox.setObjectName('alpha')
        
        # 亮度偏移量输入框
        self.beta_spinbox = QSpinBox()
        self.beta_spinbox.setMinimum(0)
        self.beta_spinbox.setSingleStep(1)
        self.beta_spinbox.setObjectName('beta')
        
        # 设置表格结构
        self.setColumnCount(2)
        self.setRowCount(2)
        self.setItem(0, 0, QTableWidgetItem('alpha'))
        self.setCellWidget(0, 1, self.alpha_spinBox)
        self.setItem(1, 0, QTableWidgetItem('beta'))
        self.setCellWidget(1, 1, self.beta_spinbox)
        self.signal_connect()


class GammaITabelWidget(TableWidget):
    """伽马变换表格部件，用于设置伽马变换参数"""
    
    def __init__(self, parent=None):
        super(GammaITabelWidget, self).__init__(parent=parent)
        # 伽马值输入框（浮点数）
        self.gamma_spinbox = QDoubleSpinBox()
        self.gamma_spinbox.setMinimum(0)      # 最小伽马值为0
        self.gamma_spinbox.setSingleStep(0.1) # 步长为0.1
        self.gamma_spinbox.setObjectName('gamma')
        
        # 设置表格结构
        self.setColumnCount(2)
        self.setRowCount(1)
        self.setItem(0, 0, QTableWidgetItem('gamma'))
        self.setCellWidget(0, 1, self.gamma_spinbox)
        self.signal_connect()


class SaltAndPepperTableWidget(TableWidget):
    """椒盐噪声表格部件，用于设置椒盐噪声添加参数"""
    
    def __init__(self, parent=None):
        super(SaltAndPepperTableWidget, self).__init__(parent=parent)
        
        # 食盐噪声阈值输入框（白色噪声）
        self.salt_threshold_spin = QSpinBox()
        self.salt_threshold_spin.setObjectName('salt_threshold')
        self.salt_threshold_spin.setRange(0, 255)  # 阈值范围0-255
        self.salt_threshold_spin.setValue(100)      # 默认值100
        self.salt_threshold_spin.setSuffix(' (越低添加越多白色噪声)')  # 后缀说明
        
        # 胡椒噪声阈值输入框（黑色噪声）
        self.pepper_threshold_spin = QSpinBox()
        self.pepper_threshold_spin.setObjectName('pepper_threshold')
        self.pepper_threshold_spin.setRange(0, 255)
        self.pepper_threshold_spin.setValue(200)
        self.pepper_threshold_spin.setSuffix(' (越高添加越多黑色噪声)')
        
        # 噪声比例输入框
        self.noise_ratio_spin = QDoubleSpinBox()
        self.noise_ratio_spin.setObjectName('noise_ratio')
        self.noise_ratio_spin.setRange(0.0, 1.0)  # 比例范围0.0-1.0
        self.noise_ratio_spin.setValue(0.1)        # 默认比例0.1
        self.noise_ratio_spin.setSingleStep(0.01)  # 步长0.01
        self.noise_ratio_spin.setSuffix(' (噪声比例)')
        
        # 设置表格结构
        self.setColumnCount(2)
        self.setRowCount(3)
        self.setItem(0, 0, QTableWidgetItem('食盐噪声阈值'))
        self.setCellWidget(0, 1, self.salt_threshold_spin)
        self.setItem(1, 0, QTableWidgetItem('胡椒噪声阈值'))
        self.setCellWidget(1, 1, self.pepper_threshold_spin)
        self.setItem(2, 0, QTableWidgetItem('噪声比例'))
        self.setCellWidget(2, 1, self.noise_ratio_spin)
        self.signal_connect()
