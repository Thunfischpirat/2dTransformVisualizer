# Visualize Application of 2D Transformations to Rectangles

## Description
This application provides a GUI interface based on the Qt library to draw and manage rectangles on a Cartesian grid. You can choose from standard 2D transformations
applied via matrix multiplication in a homogeneous coordinate system. The application was realized based on the specifications in exercise 2.2 of the book
*Computer Vision: Algorithms and Application*. 

Rectangles can be created by pressing and holding the left mouse button and sliding the mouse over the screen 
to adjust the size of the new rectangle. 

By right-clicking on an existing rectangle, you can choose to move or delete it. 

If you want to apply a geometric transformation to the rectangle, you can check the corresponding box on the sidebar and press the button corresponding to the transformation
you would like to apply on the bottom of the screen. After entering the parameters of the transformation matrix and pressing the "Ok" button, the transformation-matrix
will be applied to all the rectangles with checked boxes.

<img src="https://github.com/Thunfischpirat/2dTransformVisualizer/assets/28505637/1d0e2c87-c4e8-4611-8a6b-c7276e02b61e" width="800" height="600">



## File Overview
- Rectangle:
  - `DrawRectangle.py`: Contains functionalities related to drawing rectangles.
  - `Rectangle.py`: Defines the structure and properties of a rectangle.
  - `RectangleList.py`: Manages a list of rectangles.
  - `RectangleSignalEmitter.py`: Handles signals related to rectangles.
- Utils:  
  - `CartesianGrid.py`: Implements a Cartesian grid for the application.
  - `TransformationHandler.py`: Handles transformations related to rectangles.


## Setup and Running

The Python version used in this project is 3.11.4. To install all dependencies, run the following command if you have poetry installed on your system:
```
poetry install 
```
Afterwards, to start up the GUI, you can run 
```
python main.py
```
or alternatively 
```
poetry run python main.py
```

Enjoy playing around with geometric transformations.

## Contribute
If you would like to expand the project by adding new primitives or improving the existing functionality, feel free to open issues or create pull
requests :-)

---
