

# G-coordinator

日本語バージョンはQiitaで[ここ](https://qiita.com/tomohiron907/items/e14137fd15cb52a415dc)に載せています．
# What is G-coordinator?
To use a 3D printer, it is basically necessary to prepare a 3D model, run it through slicing software to create a G-code, and load it into the printer. G-coordinator is an open source software for creating G-codes directly in python.
![gif_img1](img/modeling.gif)
By creating G-codes directly, you can easily create shapes and forms that would be difficult to achieve using conventional methods of creating 3D models. For example, the following weave shape can be realized.

<img src="img/printted_thing.jpg" width=70%>

While Grasshopper in Rhinoceros can do the same thing with visual programming, G-coordinator uses python to achieve the same thing. This allows a high degree of freedom in modeling.

By drawing a python script in the editor on the left and executing it, the nozzle path of the 3D printer is displayed and a preview of the model can be checked. The left side of the screen allows you to adjust various print settings and output G-code.



# Requirements
G-coordinator is currently available for macOS and Windows.
G-coordinator can also be started by executing the python code main.py in the src directory. The following libraries are required to run main.py.
```
pyqt5
pyqtgraph
numpy
pyopengl
matplotlib
```
If you run G-coordinator from an .app or .exe executable file, you do not need to install these libraries.


For the final check of the output G-cocde, software such as prusa-slicer or repetier would be useful.

# G-coordinator installation procedure
Please download the software from [here](https://github.com/tomohiron907/G-coordinator/releases) according to your operating system.

If you have a Python environment set up, please clone this GitHub repository and **make the current directory "src"**. Then, execute "main.py" in the command prompt. The necessary INI configuration file for execution is also included in the "src" directory.
# How G-code works

Before modeling, it is useful to understand the structure of a G-code briefly, so that you can model it in G-coordinator. The photo below shows a G-code opened in REPETIER.
![img5](img/reptier.png)


```G1 F800 X114.97987 Y105.63424 Z2.00000 E0.00589```

These lines are repeated in large numbers.
This is an instruction to push the filament out 0.00589 mm from its current position to position X114.97987 Y105.63424 Z2.00000, moving at a speed of 800 mm per minute.

In other words, when it comes right down to it, there are a total of five elements to be controlled by G-code: three elements of coordinates (x, y, z), speed, and the amount of extrusion. In addition, since speed and extrusion can be determined automatically by the G-coordinator (of course, they can also be specified individually), all that needs to be considered are the coordinates at which the nozzle moves.

# Test modeling (cylinder)
Now, let's start modeling with G-coordinator. First, let's create a cylinder wall as the simplest model.
In the folder downloaded from github, there is a folder named "Example". Open 'default_cylinder.py' in the "example" folder by clicking the "open file" button in the upper left corner.

The code will be displayed in the editor on the left, and when you press the reload button, it will look like the picture below.

![img6](img/test_modeling.png)

In G-coordinator, modeling is done in a function called object_modeling(). As mentioned earlier, what we want is a list of coordinates.



```ruby
def object_modeling():
    full_object=[]
    for height in range(LAYER):
        arg = np.linspace(0, np.pi*2,100)
        rad = 10
        x = rad*np.cos(arg)
        y = rad*np.sin(arg)
        z = np.full_like(arg, height*0.2+0.2)
        layer = Path(x,y,z)
        full_object.append(layer)
            

    return full_object
```


In G-coordinator, we use the Path class object for modeling. This refers to the continuous trajectory along which the nozzle extrudes resin. In other words, in the case of the cylindrical example mentioned earlier, the nozzle follows a circular path while continuously extruding resin in a particular layer. Therefore, the trajectory of a single circle is represented as a Path object.

![img7](img/nozzle_path.png)


The following is a description of what is being done in the function.
First, each layer is iterated using a for statement. The current number of layers is 10, so the function iterates from layer 0 to layer 9.

<br>
Next, to draw a circle, the angle (argument) is set in a numpy array in the range of 0 to 2π. The number of elements is set to 100, so exactly 99 regular angles are created.

<br>
If we fix the radius at 10, then

The x-coordinate is ```radius * cos(arg)```

The y-coordinate is ```radius * sin(arg)```.

For the z-coordinate in the height direction, an array with the same number of elements as arg is initialized according to the height. 0.2 is added because we want the first layer to print at a height of 0.2, even if the height starts at 0.

<br>

```layer = Path(x,y,z)```


The end point of the nth layer and the start point of the n+1st layer are automatically traveled.
For each layer, a layer is added to the list of full_objects and a full_object is set as the return value.

# Printing settings

Once modeling is complete, prepare the G-code.

<img src = "img/print_settings.png" width  = 50%>

At this stage, it is not possible to make such complicated print settings. Only the minimum settings are available.
As you can see, nozzle_diameter is the nozzle diameter and layer_height is the layer height.

When you click on the "Machine Settings" button, a window for 3D printer hardware settings will appear.

<img src = "img/machine_settings.png" width  = 50%>

 Here, you have the option to select the kinematics. Generally, for a Cartesian system with three axes (X, Y, Z), please choose the Cartesian option. Additionally, there are other options available to support specific types of 3D printers and G-code, such as:

- Nozzle Tilt: For robotic arm-type 3D printers or printers that support Hexa G-code.
- Bed Tilt: For 3D printers where the bed tilts, similar to a machining center.
- Bed Rotate: For 3D printers where the bed rotates.

These options are provided to accommodate different types of 3D printers with specific functionalities.

The Origin item requires a bit of attention. In general 3D printers, the origin is set to the front left of the bed, but in G-coordinator, the origin is set to the center of the bed to make it easier to write the formula for modeling.
The bed of the 3D printer I am currently using is 210mm x 210mm, so I set the origin at 105mm from the center of the bed.

Coordinates of (10,-20) on the G-coordinator are converted to (115, 85) on the G-code and recorded.

In addition, a speed setting is also provided. The print speed here is the default value when nothing is set, and if the speed is specified in detail in the editor, it takes precedence. The same is true for the bottom item Extrusion_multiplier.

In travel_option, you can set whether or not retraction is used and the z-hop.

In extrusion_multiplier, you can determine the factor by which the extrusion amount (E value) is multiplied.

Please specify the absolute path of the .txt files containing the Start G-code and End G-code in the printing settings field. Once you have specified the paths, it is necessary to restart G-coordinator for the changes to take effect.

For other printing settings, you don't need to restart G-coordinator every time you make changes. Once you modify the settings, they will take effect immediately without requiring a restart.

# Export G-code
When ready, press the Gcode Export button.

<img src = "img/gcode_export_window.png" width  = 50%>

In this window, only the first 1000 lines of the generated G-code are displayed. However, when you click the save button, the entire G-code will be saved. When saving the G-code, please make sure to enter the name as "{name}.gcode" including the file extension.