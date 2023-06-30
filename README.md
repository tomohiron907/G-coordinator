

# G-coordinator

日本語バージョンは，このページの下に載せています．
# What is G-coordinator?
To use a 3D printer, it is basically necessary to prepare a 3D model, run it through slicing software to create a G-code, and load it into the printer. G-coordinator is an open source software for creating G-codes directly in python.
![gif_img1](img/modeling.gif)
By creating G-codes directly, you can easily create shapes and forms that would be difficult to achieve using conventional methods of creating 3D models. For example, the following weave shape can be realized.



<img src="img/wave_tray.JPG" width=80%>
<img src="img/printted_thing.jpg" width=70%>
<br>
 - [OTHER WORKS](#works-anchor)


<br>
While Grasshopper in Rhinoceros can do the same thing with visual programming, G-coordinator uses python to achieve the same thing. This allows a high degree of freedom in modeling.

By drawing a python script in the editor on the left and executing it, the nozzle path of the 3D printer is displayed and a preview of the model can be checked. The left side of the screen allows you to adjust various print settings and output G-code.



# Requirements
G-coordinator is currently available for macOS and Windows.
G-coordinator can also be started by executing the python code main.py in the src directory.

To install the required libraries, enter the following command．

```
pip install -r requirements.txt
```
If you run G-coordinator from an .app or .exe executable file, you do not need to install these libraries.


For the final check of the output G-cocde, software such as prusa-slicer or repetier would be useful.

# G-coordinator installation procedure
Please download the software from [here](https://github.com/tomohiron907/G-coordinator/releases) according to your operating system.

If you have a Python environment set up, please clone this GitHub repository and <span style="color: Crimson; ">make the current directory "src"</span>. Then, execute "main.py" in the command prompt. The necessary INI configuration file for execution is also included in the "src" directory.
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

In G-coordinator, modeling is done in a function  object_modeling(). As mentioned earlier, what we want is a list of coordinates.



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


<br>

# Lastly

There are few people who have an interest in both coding/mathematics for fabrication and 3D printing. Therefore, when using G-coordinator, it can be challenging for individuals to start the fabrication process from scratch, resulting in a limited user base. To address this, I encourage users to actively tweet about their creations or modifications made using G-coordinator, and include the hashtag #Gcoordinator (without hyphen). This will contribute to the activation of the community and foster greater engagement.

### Works
<a id="works-anchor"></a>


<img src = "img/works/sin_wall.jpg" width  = 50%>
<img src = "img/works/light_fixture.jpg" width  = 50%>
<img src = "img/works/clock.jpg" width  = 50%>
<img src = "img/works/light_cup.jpg" width  = 50%>
<img src = "img/works/gyroid_coaster.jpg" width  = 50%>
<img src = "img/works/wave_cup_2.jpg" width  = 50%>
<img src = "img/works/wave_cup.jpg" width  = 50%>
<img src = "img/works/wave_tray_1.jpg" width  = 50%>
<img src = "img/works/wave_bottle_2.jpg" width  = 50%>
<img src = "img/works/wave_wall_1.jpg" width  = 50%>
<img src = "img/works/envelope_2.jpg" width  = 50%>
<img src = "img/works/lissajous_1.jpg" width  = 50%>
<img src = "img/works/lissajous_2.jpg" width  = 50%>
<img src = "img/works/audrey.jpg" width  = 50%>
<img src = "img/works/audrey_2.jpg" width  = 50%>
<img src = "img/works/envelope_1.jpg" width  = 50%>
<img src = "img/works/others.jpg" width  = 50%>

<br>
<br>

---
<br>
<br>

# G-coordinatorとは？
3Dプリンタを使用するためには，基本的には3Dモデルを用意し，それをスライスソフトにかけてG-codeを作成してプリンタに読み込ませる必要があります．今回開発したG-coordinatorはpythonで直接G-codeを作成するためのオープンソースフトウェアです．(URL:https://github.com/tomohiron907/G-coordinator)

![gif_img1](img/modeling.gif)

<br>

直接G-codeを作成することにより，従来の3Dモデルを作成する方法では実現が困難であった形状や造形を，容易に作り出すことができます．例えば，下のような編み形状を実現できます．

<img src="img/wave_tray.JPG" width=80%>
<img src="img/printted_thing.jpg" width=70%>


<br>
RhinocerosのGrasshopperではビジュアルプログラミングにて同様のことは可能ですが，G-coordinatorではそれをpythonで実現します．

<br>
左側のエディタにpythonスクリプトを描き，それを実行することにより，3Dプリンタのノズルパスが表示され造形のプレビューが確認できます．また，画面の左側で各種印刷設定を調整し，G-codeを出力することができます．

<br>


# 必要事項
G-coordinatorは現在，macOSとWindowsに対応しています．
また，pythonファイルを直接実行することでも起動できます．
その場合には，以下のコマンドでライブラリを一括インストールできます．
```
pip install -r requirements.txt
```
.appや.exeなどの実行ファイルとしてG-coordinatorを起動した場合にはライブラリのインストールは必要ありません．
出力されたG-codeを確認するために，Prusa slicerやReptierなどのソフトがあれば便利です．


# G-coordinatorのインストール
[ここ](https://github.com/tomohiron907/G-coordinator/releases)から，お使いのOSにあったものをダウンロードしてください．


python環境が整っている場合には，このgithubリポジトリのクローンを作成し，<span style="color: Crimson; ">カレントディレクトリをsrcにして，</span>main.pyを実行してください．実行に必要なini設定ファイルもsrcの中に入っているからです．

また，インストール手順をまとめた動画もyoutube にアップしています．
https://www.youtube.com/watch?v=LqZGno-BWG0


# G-codeの仕組み

造形の前に，G-codeの構造を簡単にでも把握しておくことは，今後，造形を行う上でも有用です．下の写真は，repetierでG-codeを開いたものです

![img5](img/reptier.png)


<br>

基本的には，
```G1 F800 X114.97987 Y105.63424 Z2.00000 E0.00589```
こういった行が大量に繰り返されています．
これは，現在の位置からX114.97987 Y105.63424 Z2.00000の位置まで，分速800ｍｍで移動しながら，フィラメントを0.00589mm押し出すという命令です．

つまり，突き詰めれば，G-codeで制御すべき要素は，座標(x, y, z)の三要素とスピード，押し出し量の計５つです．さらに，スピードと，押し出しはG-coordinator から自動で決定できる（もちろん細かく個別に指定することも可能）なので，考えるべきは，どの位置にノズルが動くかという座標のみで良いです．

# テスト造形（円柱）
では，いよいよ，G-coordinatorで造形をしていきましょう．まずは，最も簡単なモデルとして，円柱の壁を作ります．
githubからダウンロードしたフォルダの中に，Exampleというフォルダがあります．左上のopen fileを押してexampleの中の’default_cylinder.py'を開いてください．

左のエディタにコードが表示され，reloadボタンを押すと，以下の写真のようになります．

![img6](img/test_modeling.png)

<br>

G-coordinator では，object_modeling()という関数の中でモデリングを行います．先ほど述べた通り，最終的に欲しいものは，座標のリストです．なので，通るべき点の座標を含んだlistを作成しています．



<br>

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
<br>

G-coordinatorの中では，Pathクラスのオブジェクトをモデリングに使用します。
これは，ノズルが樹脂を絶え間なく出し続ける経路のことを指しています。つまり，上の円柱の例では，ノズルは，ある層において，樹脂を出し続けながら，円を描くので一つの円の経路がpathというオブジェクトです．

<br>

![img7](img/nozzle_path.png)

<br>
関数内で何をしているかについてです．
まず，for文で各レイヤーについて繰り返しをしています．現在のレイヤー数は10なので，0層目から9層目まで繰り返されるイメージです．

<br>
次に，円を描くために，角度（argument)をnumpy arrayで0から2πの範囲で設定しています．要素数は100としているため，正確には，正99角形が造形されます．
半径は10で固定すると，
x座標は，

```半径×cos(arg)```
y座標は，
```半径×sin(arg)```
より計算できます．
高さ方向のz座標に関しては，argと同じ要素数のarrayをheightに応じて値を初期化しています．0.2を足しているのは，heightが0から始まっても，第一層目は高さ0.2の場所に印刷して欲しいからです．

```layer = Path(x,y,z)```

<br>
なお，n段目のPathの終点とn+1段目のPathの始点とは，自動でトラベルするようになっています．
そして，各レイヤーごとに，full_objectのlist にPathを追加し，full_objectを返り値として設定しています．

<br>

# 印刷設定

造形が完了すれば，G-codeの準備をします．

<img src = "img/print_settings.png" width  = 50%>

現段階では，そこまで，複雑な印刷設定ができないです．最低限の設定項目のみです．
読んで字のごとくですが，nozzle_daimeterはノズル径，layer_heightはレイヤーの高さです．

一番上のmachine settingsのボタンを押すと，3Dプリンタのハードウェア設定のウィンドウが出てきます．

<br>
<img src = "img/machine_settings.png" width  = 50%>

ここでは，kinematicsを選択することが可能です．一般的には3軸x, y, zのCartesianの項目を選択してください．ここでは，他に，
- ロボットアーム型やHexaといった3Dプリンタ用のGcodeをサポートするために，Nozzle Tilt
- マシニングセンタのようなベッドが傾く3Dプリンタ用にBed Tilt
- ベッドが回転する3Dプリンタに用にBed Rotate

がサポートされています。

<br>
少し注意の必要なのは，Origin の項目です．一般の3Dプリンタでは，原点をベッドの左手前に設定していますが，G-coordinatorでは，造形の数式を簡単に書くために，原点をベッドの中央に設定しています．
自分の今使用している3Dプリンタのベッドが210mm×210mmなので，その中心の105mm を原点と設定しています．

<br>
G-coordinator上で(10,-20)の座標が，G-code上では(115, 85)に変換されて記録されるイメージです．

<br>
他には，スピードの項目も設けています．ここでのプリントスピードは，何も設定しなかった場合のデフォルト値であり，エディタで細かくスピードを指定した場合には，そちらが優先されます．これは，一番下の項目のExtrusion_multiplierでも同様です．

<br>
travel_optionでは，リトラクションの有無とｚホップの設定が可能です．

<br>
extrusion_multiplier では，押し出し量（E値）に掛ける係数を決定できます．


# G-codeの出力

準備が整ったら，Export Gcodeボタンを押してください

<img src = "img/gcode_export_window.png" width  = 50%>

このウィンドウでは，G-code作成したG-codeの最初の１０００行だけが表示されています。もちろん，保存ボタンを押して保存されるのはG-code全体です．また，Gーcodeを保存するときに，名前は，{名前}.gcodeと、拡張子まで入力する必要があります。

<br>

# 最後に

G-coodinatorを使うにあたり，造形のためのコードや数学と3Dプリンタの両方に興味のある人が少ないこともあり，なかなか自分で1から造形をおこなうのは難しく，ユーザも限られてしまいます．そこで，G-coordinatorで造形をおこなったり，改造して印刷をおこなったりしたものを積極的に　#Gcoordinator（ハイフンなしに注意）でツイートしてもらえると，よりコミュニティの活性化につながると思っています．

# 作品
<img src = "img/works/sin_wall.jpg" width  = 50%>
<img src = "img/works/light_fixture.jpg" width  = 50%>
<img src = "img/works/clock.jpg" width  = 50%>
<img src = "img/works/light_cup.jpg" width  = 50%>
<img src = "img/works/gyroid_coaster.jpg" width  = 50%>
<img src = "img/works/wave_cup_2.jpg" width  = 50%>
<img src = "img/works/wave_cup.jpg" width  = 50%>
<img src = "img/works/wave_tray_1.jpg" width  = 50%>
<img src = "img/works/wave_bottle_2.jpg" width  = 50%>
<img src = "img/works/wave_wall_1.jpg" width  = 50%>
<img src = "img/works/envelope_2.jpg" width  = 50%>
<img src = "img/works/lissajous_1.jpg" width  = 50%>
<img src = "img/works/lissajous_2.jpg" width  = 50%>
<img src = "img/works/audrey.jpg" width  = 50%>
<img src = "img/works/audrey_2.jpg" width  = 50%>
<img src = "img/works/envelope_1.jpg" width  = 50%>
<img src = "img/works/others.jpg" width  = 50%>