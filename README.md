# MiniDXF

Minimal Python librery to create DXF files with basic features.
This library is written to create basic 2D drawings, initially designed to create 2D contours for use in CNC cutting machines. 


## Installation

pip install minidxf

## Usage

Import the library:
from minidxf import DXFDocument

Methods for drawing:
- line (x1,y1,x2,y2)
- arc(center_x,center_y,radius,start_angle,end_angle)
- arc_3points(x1,y1,x2,y2,x3,y3)

Methods for retrieving information:
- bbox() - bounding box of the drawing
- height() - vertical dimension of the drawing
- width() - horizontal dimension of the drawing

Methods for basic transformations:
- translate(dx,dy)
- rotate(angle)
- move_to_origin()

Methods for file management:
- save(filename)

## Example code

```python
from miniDXF import DXFDocument

# Create a new DXF document
doc = DXFDocument()

# Add a line
doc.line(0, 0, 100, 0)

# Add an arc (center, radius, angles)
doc.arc(50, 50, 25, 0, 180)

# Add an arc defined by three points
doc.arc_3p(0, 0, 100, 0, 50, 50)

# Rotate all geometry 90 degrees counter-clockwise
doc.rotate(90)

# Move geometry so the bounding box starts at (0, 0)
doc.move_to_origin()

# Save DXF file
doc.save("example.dxf")

## Notes

The DXF file is created with the minimal possible features. It conotains layer 0 only, and the default units are milimiters.

## License


This project is licensed under the **GNU General Public License v3.0** (GPLv3).
