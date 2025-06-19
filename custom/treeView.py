import cv2
import numpy as np

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class FileSystemTreeView(QTreeView):
    """
    文件系统树视图类，用于浏览和选择图像文件
    继承自QTreeView，提供文件系统导航功能
    """
    
    def __init__(self, parent=None):
        """初始化文件系统树视图"""
        super().__init__(parent=parent)
        self.mainwindow = parent  # 引用主窗口
        
        # 创建文件系统模型并设置根路径为当前目录
        self.fileSystemModel = QFileSystemModel()
        self.fileSystemModel.setRootPath('.')
        self.setModel(self.fileSystemModel)
        
        # 设置视图外观
        self.setColumnWidth(0, 200)  # 设置第一列(文件名)宽度
        self.setColumnHidden(1, True)  # 隐藏文件大小列
        self.setColumnHidden(2, True)  # 隐藏文件类型列
        self.setColumnHidden(3, True)  # 隐藏修改日期列
        self.header().hide()  # 隐藏标题栏
        
        # 设置交互特性
        self.setAnimated(True)  # 启用展开/折叠动画
        self.setFocusPolicy(Qt.NoFocus)  # 选中项不显示虚线边框
        
        # 连接双击事件到图像选择处理函数
        self.doubleClicked.connect(self.select_image)
        self.setMinimumWidth(200)  # 设置最小宽度
    
    def select_image(self, file_index):
        """
        处理文件双击事件，选择图像文件
        :param file_index: 被双击的文件索引
        """
        # 获取文件完整路径
        file_name = self.fileSystemModel.filePath(file_index)
        
        # 检查是否为图像文件
        if file_name.endswith(('.jpg', '.png', '.bmp')):
            # 使用OpenCV读取图像，支持中文路径
            src_img = cv2.imdecode(np.fromfile(file_name, dtype=np.uint8), -1)
            
            # 通知主窗口更新图像
            self.mainwindow.change_image(src_img)
