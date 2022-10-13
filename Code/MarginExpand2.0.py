# time:2022-10-4
# author:jim
# bug:none
from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import Signal, QObject  # 创建自定义信号与槽所用的库
from PySide2.QtGui import QIcon
from PyPDF2.generic import RectangleObject
from PyPDF2 import PdfReader, PdfWriter, Transformation

from decimal import Decimal
from threading import Thread

margin_width = {"1": 0.2, "2": 0.33, "3": 0.5, "4": 1}
MarginType = {"1": "1", "2": "2", "3": "3", "4": "4"}


class MySignals(QObject):
    # 定义一种信号，两个参数 类型分别是： QTextBrowser 和 字符串
    # 调用 emit方法 发信号时，传入参数 必须是这里指定的 参数类型
    text_print = Signal(str)
    text_clear = Signal()


class MarginExpand:

    def __init__(self):  # 这里原本是自己来创建这个用户的界面，但是可以通过qt的界面来实现

        self.ui = QUiLoader().load('MarginExpand_3.ui')  # 这其实拿过来的就是qt的页面中最大的Qwidget

        # ButtonGroup：

        self.ui.buttonGroup_size.addButton(self.ui.SuperNarrow, 1)
        self.ui.buttonGroup_size.addButton(self.ui.Narrow, 2)
        self.ui.buttonGroup_size.addButton(self.ui.Wide, 3)
        self.ui.buttonGroup_size.addButton(self.ui.SuperWide, 4)

        self.ui.buttonGroup_style.addButton(self.ui.blankpaper, 1)
        self.ui.buttonGroup_style.addButton(self.ui.squredpaper, 2)
        self.ui.buttonGroup_style.addButton(self.ui.ruled_paper, 3)
        self.ui.buttonGroup_style.addButton(self.ui.dotted_paper, 4)
        self.ui.Wide.setChecked(True)
        self.ui.squredpaper.setChecked(True)
        self.ui.buttonGroup_size.buttonClicked.connect(self.handleButtonClicked)
        # 这要传递的参数是button本身，是选中被触发的那个button，但是之前直接把group传进去了，这是个大问题
        # 生活中的算法：最近两次解决大的bug都是通过找到近似的例子，以后不能蛮干，需要找到近似的例子再实现，不可以随随便便拍脑瓜
        self.ui.buttonGroup_style.buttonClicked.connect(self.handleButtonClicked)

        # file input and output
        self.ui.inputFile.clicked.connect(self.loadfile)
        self.ui.outputPath.clicked.connect(self.output)
        self.ui.Start.clicked.connect(self.handleCalc)  # 通过取得button的类，同样这个名字也和design里面的东西相关

        # 自定义信号
        self.ms = MySignals()
        self.ms.text_print.connect(self.printToGui)
        self.ms.text_clear.connect(self.clearToGui)
        # progressbar
        self.progress_value = 0
        self.ui.progressBar.setMinimum(0)
        self.ui.progressBar.setMaximum(100)
        self.ui.progressBar.setValue(self.progress_value)
        # load and output files variables
        self.files_name = []  # 获取
        self.output_path = 'D:'

    def loadfile(self):
        self.files_name, _ = QFileDialog.getOpenFileNames(self.ui, '打开文件', 'C:', 'pdf文件(*.pdf)')
        if self.files_name == []:
            return
        self.ui.textBoard.append("Input files:")
        print(self.files_name)  # 拿到的文件名是一个list
        for name in self.files_name:
            self.ui.textBoard.append(name)

    def output(self):
        self.output_path = QFileDialog.getExistingDirectory(self.ui,
                                                            "选取输出文件夹",
                                                            'D:')  # 起始路径
        if self.output_path == '':
            return
        else:
            # self.ms.text_print(f"Out put path:{self.output_path}")
            self.ui.textBoard.append(f"Out put path:{self.output_path}")

    def printToGui(self, text):
        self.ui.textBoard.append(str(text))

    def clearToGui(self):
        self.ui.textBoard.clear()

    def handleButtonClicked(self, button):
        pass
        # print("")
        # self.ui.textBoard.append(f'{button.group().checkedId()}')
        # self.ui.textBoard.append(f'{button.text()}')
        # self.ui.textBoard.clear()
        # self.ui.textBoard.append(f'{margin_width[button.text()]}')

    def handleCalc(self):
        self.ui.Start.setEnabled(False)

        def marginExpand():
            Margin_type = str(self.ui.buttonGroup_style.checkedId())  # 输入参数：纸张的类型
            Margin_width = str(self.ui.buttonGroup_size.checkedId())  # marginExpand的宽度
            # -----测试打印代码----
            # self.ui.textBoard.append(f'size id:{self.ui.buttonGroup_size.checkedId()}')
            # self.ui.textBoard.append(f'size id:{margin_width[str(self.ui.buttonGroup_size.checkedId())]}')
            # self.ui.textBoard.append(f'style id:{self.ui.buttonGroup_style.checkedId()}')
            # self.ui.textBoard.append(f'style id:{MarginType[str(self.ui.buttonGroup_style.checkedId())]}')

            margin_file_path = f"./Margintype/Margintype_{MarginType[Margin_type]}.pdf"  # margin文件路径

            print(self.files_name)

            # 上一个函数内部的变量是没法调用的，需要传递出来

            for file_name in self.files_name:  # bug:通过file—name之后的list好像没有拿到文件的路径
                print(file_name)
                index = -1
                output_name = ''
                while file_name[index] != '/':
                    output_name = file_name[index] + output_name
                    index = index - 1

                self.ms.text_print.emit(f"Current file：{output_name}")

                reader = PdfReader(file_name)
                number_of_page = len(reader.pages)
                number_of_currentpage = 1
                # 输出页面
                writer = PdfWriter()
                print("页面总数:", len(reader.pages))
                self.progress_value = 0
                for page in reader.pages:
                    # 进度条比例的运算：
                    self.progress_value = (number_of_currentpage / number_of_page) * 100
                    self.ui.progressBar.setValue(self.progress_value)
                    # 文本信息的输出
                    self.ms.text_print.emit(f"Progress:{number_of_currentpage}/{number_of_page}")
                    # 其实可以通过每页的时间，来估计整个文档的时间，（也就是其实可以通过pdf的大小，也matgin的宽度来进行估计的）

                    page1 = page
                    # page1_media = page1.cropbox
                    page1_height = page1.cropbox.getHeight()
                    page1_width = page1.cropbox.getWidth()

                    if number_of_currentpage > 1:
                        page_last = reader.pages[number_of_currentpage - 2]  # 上一个页面的

                        if int(page_last.cropbox.left) == int(page1.cropbox.left) and int(
                                page_last.cropbox.right / (1 + Decimal(margin_width[Margin_width]))) == int(
                                page1.cropbox.right) and int(page_last.cropbox.bottom) == int(
                                page1.cropbox.bottom) and int(page_last.cropbox.top) == int(page1.cropbox.top):

                            print("same")
                        else:
                            print("not same")
                            # ------------page2:margin页面的初始化-------------
                            # margin页面
                            reader2 = PdfReader(margin_file_path)
                            page2 = reader2.pages[0]
                            # 获取page2的尺寸
                            page2_crop = page2.cropbox
                            page2_height = page2.cropbox.getHeight()
                            page2_width = page2.cropbox.getWidth()
                            # print("page_margin:", page2_crop)
                            # -----------margin页面尺寸放缩-----------------------
                            height_ratio = round(float(page1_height / page2_height), 1)
                            width_ratio = round(float(page1_width / page2_width), 1)
                            page2.scale_by(max(width_ratio, height_ratio))
                            # print(f"宽度比：{width_ratio},长度比： {height_ratio}")
                            # 1:对margin进行裁剪
                            # print("放缩之后的剪裁")

                            page2.mediabox = RectangleObject((page1.mediabox.left, page1.mediabox.bottom,
                                                              page1.mediabox.right * Decimal(
                                                                  margin_width[Margin_width]),
                                                              page1.mediabox.top))
                            page2.cropbox = RectangleObject((page1.cropbox.left, page1.cropbox.bottom,
                                                             page1.cropbox.right * Decimal(margin_width[Margin_width]),
                                                             page1.cropbox.top))
                            page2.trimbox = RectangleObject((page1.trimbox.left, page1.trimbox.bottom,
                                                             page1.trimbox.right * Decimal(margin_width[Margin_width]),
                                                             page1.trimbox.top))
                            page2.bleedbox = RectangleObject((page1.bleedbox.left, page1.bleedbox.bottom,
                                                              page1.bleedbox.right * Decimal(
                                                                  margin_width[Margin_width]),
                                                              page1.bleedbox.top))
                            page2.artbox = RectangleObject((page1.artbox.left, page1.artbox.bottom,
                                                            page1.artbox.right * Decimal(margin_width[Margin_width]),
                                                            page1.artbox.top))

                            # margin的位置移动
                            # print("page1的平移")
                            Expand_width = page1.cropbox.right  # page1的宽度
                            op = Transformation().translate(tx=Expand_width, ty=0)
                            page2.add_transformation(op)
                            # margin页面固定
                            page2_crop = page2.cropbox
                            page2.mediabox = RectangleObject(
                                (
                                    page2_crop.left + Expand_width, page2_crop.bottom, page2_crop.right + Expand_width,
                                    page2_crop.top))
                            page2.cropbox = RectangleObject(
                                (
                                    page2_crop.left + Expand_width, page2_crop.bottom, page2_crop.right + Expand_width,
                                    page2_crop.top))
                            page2.trimbox = RectangleObject(
                                (
                                    page2_crop.left + Expand_width, page2_crop.bottom, page2_crop.right + Expand_width,
                                    page2_crop.top))
                            page2.bleedbox = RectangleObject(
                                (
                                    page2_crop.left + Expand_width, page2_crop.bottom, page2_crop.right + Expand_width,
                                    page2_crop.top))
                            page2.artbox = RectangleObject(
                                (
                                    page2_crop.left + Expand_width, page2_crop.bottom, page2_crop.right + Expand_width,
                                    page2_crop.top))
                    else:
                        # ------------page2:margin页面的初始化-------------
                        # margin页面
                        reader2 = PdfReader(margin_file_path)
                        page2 = reader2.pages[0]
                        # 获取page2的尺寸
                        page2_crop = page2.cropbox
                        page2_height = page2.cropbox.getHeight()
                        page2_width = page2.cropbox.getWidth()  # 这里好像没有必要3位数好像1位数字就可以了
                        # print("page_margin:", page2_crop)
                        # -----------margin页面尺寸放缩-----------------------
                        height_ratio = round(float(page1_height / page2_height), 1)  # 是否一位就可以，没必要那么精准吧
                        width_ratio = round(float(page1_width / page2_width), 1)
                        page2.scale_by(max(width_ratio, height_ratio))
                        # print(f"宽度比：{width_ratio},长度比： {height_ratio}")
                        # 1:对margin进行裁剪
                        # print("放缩之后的剪裁")

                        page2.mediabox = RectangleObject((page1.mediabox.left, page1.mediabox.bottom,
                                                          page1.mediabox.right * Decimal(margin_width[Margin_width]),
                                                          page1.mediabox.top))
                        page2.cropbox = RectangleObject((page1.cropbox.left, page1.cropbox.bottom,
                                                         page1.cropbox.right * Decimal(margin_width[Margin_width]),
                                                         page1.cropbox.top))
                        page2.trimbox = RectangleObject((page1.trimbox.left, page1.trimbox.bottom,
                                                         page1.trimbox.right * Decimal(margin_width[Margin_width]),
                                                         page1.trimbox.top))
                        page2.bleedbox = RectangleObject((page1.bleedbox.left, page1.bleedbox.bottom,
                                                          page1.bleedbox.right * Decimal(margin_width[Margin_width]),
                                                          page1.bleedbox.top))
                        page2.artbox = RectangleObject((page1.artbox.left, page1.artbox.bottom,
                                                        page1.artbox.right * Decimal(margin_width[Margin_width]),
                                                        page1.artbox.top))

                        # margin的位置移动
                        # print("page1的平移")
                        Expand_width = page1.cropbox.right  # page1的宽度
                        op = Transformation().translate(tx=Expand_width, ty=0)
                        page2.add_transformation(op)
                        # margin页面固定
                        page2_crop = page2.cropbox
                        page2.mediabox = RectangleObject(
                            (
                                page2_crop.left + Expand_width, page2_crop.bottom, page2_crop.right + Expand_width,
                                page2_crop.top))
                        page2.cropbox = RectangleObject(
                            (
                                page2_crop.left + Expand_width, page2_crop.bottom, page2_crop.right + Expand_width,
                                page2_crop.top))
                        page2.trimbox = RectangleObject(
                            (
                                page2_crop.left + Expand_width, page2_crop.bottom, page2_crop.right + Expand_width,
                                page2_crop.top))
                        page2.bleedbox = RectangleObject(
                            (
                                page2_crop.left + Expand_width, page2_crop.bottom, page2_crop.right + Expand_width,
                                page2_crop.top))
                        page2.artbox = RectangleObject(
                            (
                                page2_crop.left + Expand_width, page2_crop.bottom, page2_crop.right + Expand_width,
                                page2_crop.top))

                    number_of_currentpage += 1
                    # page1和page2d页面的融合

                    page1.merge_page(page2, expand=True)
                    # output页面固定
                    page1_media = page1.mediabox  # 还真是融合完成之后，只有mediabox改变了
                    page1.mediabox = RectangleObject(
                        (page1_media.left, page1_media.bottom, page1_media.right, page1_media.top))
                    page1.cropbox = RectangleObject(
                        (page1_media.left, page1_media.bottom, page1_media.right, page1_media.top))
                    page1.trimbox = RectangleObject(
                        (page1_media.left, page1_media.bottom, page1_media.right, page1_media.top))
                    page1.bleedbox = RectangleObject(
                        (page1_media.left, page1_media.bottom, page1_media.right, page1_media.top))
                    page1.artbox = RectangleObject(
                        (page1_media.left, page1_media.bottom, page1_media.right, page1_media.top))
                    # 页面输出
                    # print("page页面的输出")
                    writer.add_page(page1)
                    # self.ui.textBoard.clear()#可能的bug，在子函数的线程中修改主线程中的控件信息，可能导致程序崩溃
                    # self.ms.text_clear.emit()
                # 从文件路径中提取文件的名字
                index = -1
                output_name = ''
                while file_name[index] != '/':
                    output_name = file_name[index] + output_name
                    index = index - 1
                file_name = output_name

                with open(f"{self.output_path}/MarginExpand_{file_name}", "wb") as fp:
                    writer.write(fp)
                self.ms.text_print.emit("MarginExpand Done！")
            self.ui.Start.setEnabled(True)

        # show = Thread(target=marginExpand,args=(files_name,))
        show = Thread(target=marginExpand)
        show.start()


if __name__ == '__main__':
    app = QApplication([])
    app.setWindowIcon(QIcon('./image/MarginExpand.jpg'))
    marginexpand = MarginExpand()
    marginexpand.ui.show()
    app.exec_()