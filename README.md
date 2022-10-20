# MarginExpand

 MarginExpand用于解决阅读pdf、电子书和论文时做笔记地方不够的问题，MarginExpand可以实现Pdf margin expand功能，可根据文件的大小批量为pdf文件添加白边，并且可以挑选纸张的样式，非常适合电子笔记爱image好者。本项目用python，pyqt，pyside2开发，可以独立运行在windows系统。



## 问题的起源：

+ 每次看论文看电子书的时候都苦于没有地方可以做笔记， 并且没有地方做批注，这不得不让我将笔记写在其他文件上， 但是这就会使得笔记和pdf文件分离，复习起来需要同时打开两个文件， 是一个非常麻烦的事情。如果在论文、电子书、课件上可以添加额外的区域用来记笔记，那将会大大提高做笔记的效率
+ 市面上能实现pdf裁切和页面编辑的软件有很多，例如wps，abobe，photoshop等，但是有三个缺点
  + 不能批量处理多个pdf文件，每次只能手动编辑一个文件
  + 不能给白边添加方格，横线，点格等样式
  + 手动编辑pdf文件，修改页面大小和边距，每次都需要花费很多时间，
+ ipad上实现该功能的笔记软件只有marginnote3，但是该软件不能给白边添加格式，也不能批量处理。由于我平时非常对pdf白边扩展的需求非常高，并且每次使用pc端专业软件都非常耗时， 并且每次越用越气（为什么goodnotes等一众笔记软件不给集成这个功能）最后干脆自己做了MarginExpand解决这个问题



## 使用指南

+ 点击文件夹中的exe软件，无需安装直接运行
  + ![image](https://github.com/fate-ubw/MarginExpand/blob/main/image/2.jpg)
+ 运行界面如下：
  + ![image](https://github.com/fate-ubw/MarginExpand/blob/main/image/%E7%95%8C%E9%9D%A2%E8%AF%B4%E6%98%8E.jpg)
+ 使用方式：
  1. 点击Input File 选择需要编辑的pdf
  2. 点击Output Path 指定输出路径（默认D盘）
  3. 选择margin的纸张样式（blank paper白纸、squared paper方格、ruled paper横线点格）
  4. 选择扩展尺寸（推荐扩展Wide(50%)和(SuperWide100%))
  5. Start！

## 使用案例

+ 教材
+ ![image](https://github.com/fate-ubw/MarginExpand/blob/main/image/3.jpg)
+ 论文
+ ![image](https://github.com/fate-ubw/MarginExpand/blob/main/image/4.jpg)



## 软件bug

+ 软件速度时快时慢，具体原因未知，由于使用了多线程，可能是多线程或者运行内存的问题
+ 由于软件本质上是采用PyPDF2的函数库来对pdf的媒体框(MediaBox) 、裁剪框(CropBox)进行裁切，如果pdf文件使用了其他软件进行过裁切（有的软件仅仅在视图上修改了pdf的尺寸，并没有在参数上做调整），那么可能无法得到理想的效果 
+ 目前软件使用Thread直接开辟线程进行页面的融合，如果pdf页数非常多会占用很多内存，可以少开一些软件



## 源代码和代码打包

+ 代码全部开源，使用python语言编写，使用函数库如下

1. Pyside2
2. PyPDF2
3. decimal
4. threading

+ 打包使用pyinstaller，如果打包时遇到了问题，可以在issue里面提问



## 未来的功能

+ 在左边也可以添加白边
+ 开辟多个线程对多个pdf文件同时进行操作，提高软件的运行速度
+ 添加pdf文件的预览功能，使得用户可以对pdf添加白边的宽度有一个大概的把握
+ 添加直接打开输出的文件操作，无需用户自己再找生成的pdf功能
+ 实现对word、ppt、pptx、caj、md等文件转换为pdf，并且添加白边的功能
+ 合并Start按钮和进度条信息


# English Version

# MarginExpand

 MarginExpand is used to solve the problem of insufficient space for taking notes when reading pdfs, e-books and papers. MarginExpand can realize the Pdf margin expand function, which can add white margins to pdf files in batches according to the size of the files, and can choose the style of the paper, which is very suitable for electronic Notebook lover. This project is developed with python, pyqt, pyside2, and can run independently on windows system.



## What is the problem I want to solve :

- Every time I read the paper and read the e-book, I have no place to take notes and no place to make annotations. This has to make me write the notes on other files, but this will separate the notes from the pdf file and review it. It is a very troublesome thing to need to open two files at the same time. If you can add additional areas to take notes on papers, e-books, and courseware, it will greatly improve the efficiency of note-taking
- There are many softwares on the market that can realize pdf cutting and page editing, such as wps, abobe, photoshop, etc., but there are three disadvantages
  - Cannot batch process multiple pdf files, you can only manually edit one file at a time
  - You cannot add squares, horizontal lines, dots and other styles to the white border
  - Editing pdf files manually, modifying page size and margins, it takes a lot of time each time,
- The note-taking software that implements this function on the ipad is only marginnote3, but this software cannot add formatting to white borders, nor can it be processed in batches. Because I usually have a very high demand for pdf white border expansion, and every time I use the professional software on the PC side, it is very time-consuming, and the more I use it, the more angry I am (why are goodnotes and other note-taking software not integrated with this function) Finally, I simply I made MarginExpand myself to solve this problem



## User's guidance

- Click the exe software in the folder to run directly without installation
  + ![image](https://github.com/fate-ubw/MarginExpand/blob/main/image/2.jpg)
- The running interface is as follows:
  + ![image](https://github.com/fate-ubw/MarginExpand/blob/main/image/1.jpg)
- How to use:
  1. Click Input File to select the pdf to be edited
  2. Click Output Path to specify the output path (default D drive)
  3. Select the paper style of the margin (blank paper, squared paper, ruled paper)
  4. Select the extension size (recommended extension Wide(50%) and (SuperWide100%))
  5. Start!

## Use Cases

- Textbooks
 + ![image](https://github.com/fate-ubw/MarginExpand/blob/main/image/3.jpg)
- paper
 + ![image](https://github.com/fate-ubw/MarginExpand/blob/main/image/4.jpg)



## bugs

- The speed of the software is sometimes fast and sometimes slow. The specific reason is unknown. Due to the use of multi-threading, it may be a problem of multi-threading or running memory
- Since the software essentially uses the function library of PyPDF2 to cut the media box (MediaBox) and crop box (CropBox) of the pdf, if the pdf file has been cut by other software (some software only modify the view) The size of the pdf is not adjusted, and the parameters are not adjusted), then the ideal effect may not be obtained.



## Source code and code packaging

- The code is all open source, written in python language, using the function library as follows

1. Pyside2
2. PyPDF2
3. decimal
4. threading

- Use pyinstaller for packaging. If you encounter problems during packaging, you can ask questions in the issue



## Future features

- You can also add a white border on the left
- Open up multiple threads to operate multiple pdf files at the same time to improve the running speed of the software
- Add the preview function of pdf files, so that users can have a rough grasp of the width of white borders added to pdf
- Add the file operation of directly opening the output, without the need for the user to find the generated pdf function
- Realize the function of converting word, ppt, pptx, caj, md and other files to pdf, and adding white borders
- Merged Start button and progress bar information


