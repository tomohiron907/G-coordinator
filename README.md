# G-coordinator


# What is G-coordinator?
To use a 3D printer, it is basically necessary to prepare a 3D model, run it through slicing software to create a G-code, and load it into the printer. G-coordinator is an open source software for creating G-codes directly in python.
![img1](img/操作画面.png)
By creating G-codes directly, you can easily create shapes and forms that would be difficult to achieve using conventional methods of creating 3D models. For example, the following weave shape can be realized.

<img src="img/造形事例1.jpg" width=70%>

While Grasshopper in Rhinoceros can do the same thing with visual programming, G-coordinator uses python to achieve the same thing. This allows a high degree of freedom in modeling.

By drawing a python script in the editor on the left and executing it, the nozzle path of the 3D printer is displayed and a preview of the model can be checked. The left side of the screen allows you to adjust various print settings and output G-code.



# Requirements
To use G-coordinator, you need to have a good python environment. Some knowledge of python is also required for modeling.
In the following article, VS-CODE is used, but of course, pycharm and the like are also acceptable.
For the final check of the output G-cocde, software such as prusa-slicer or repetier would be useful.

# G-coordinator installation procedure
This section is intended for those who are not familiar with python, so those who are familiar with python can skip this section.
The source code of G-coordinator is available on github [here](https://github.com/tomohiron907/G-coordinator). (You can download the zip file from the bottom of the green <>code button.) The main code is placed in the src directory, so after downloading and extracting, open the src file with an editor. In this directory, 'main_app.py' is the main pytnon script to be executed.

Then, install the necessary libraries by pip. The necessary items are listed in requiremets.txt.
![img3](img/インストール後.png)


Download the libraries needed to run the program by typing the following in a terminal.

```pip install numpy```
```pip install pyqt5```
```pip install pyqtgraph```
```pip install pyopengl```
```pip install shaply```

In some cases, you may need to install something that comes standard on a mac, but is not required on a win machine.
If the error disappears and main_app.py is executed, the installation is complete.

![img4](img/ソフト起動画面.png)
