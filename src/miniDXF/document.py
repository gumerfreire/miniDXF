# MiniDXF - Minimal DXF writer
# Copyright (C) 2026 Gumer Freire
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

from .entities import _Line, _Arc, _arc_from_3_points
from .dxf_template import DXF_TEMPLATE

_UNITS = {
    "mm": 4,
    "inch": 1,
}

class DXFDocument:
    def __init__(self, units="mm"):
        if units not in _UNITS:
            raise ValueError(f"Unsupported units: {units}")

        self._units = units
        self._entities = []

    # PUBLIC API
    def line(self, x1, y1, x2, y2, layer="0"):
        """
        Draws a line in the DXF given two points

        Parameters:
        x1,y1:  Coordinates x,y of initial point
        x2,y2:  Coordinates x,y of final point
        layer:  Layer name (optional, default 0)
        """
        self._entities.append(_Line(x1, y1, x2, y2, layer))
        return self

    def arc(self, cx, cy, radius, start_angle, end_angle, layer="0"):
        """
        Draws an arc in the DXF given the center, radius, and start / end angles.
        Angles are given in degrees. 0 is X axis (right) and positive angle is counterclockwise.

        Parameters:
        cx,cy:  Coordinates x,y for the center of the arc
        radius: Radius of the arc
        start_angle:    Initial angle (degrees)
        end_angle:      End angle (degrees)
        layer:         Layer name (optional, default 0)
        """
        self._entities.append(
            _Arc(cx, cy, radius, start_angle, end_angle, layer="0")
        )
        return self

    def arc_3points(self, x1, y1, x2, y2, x3, y3, layer="0"):
        """
        Add an arc defined by three points.
        The arc starts at (x1, y1), ends at (x2, y2), and passes through (x3, y3).

        Parameters:
            x1, y1: start point
            x2, y2: end point
            x3, y3: point the arc passes through
            layer:  Layer name (optional, default 0)
        """
        cx, cy, r, start_ang, end_ang = _arc_from_3_points(
            x1, y1, x2, y2, x3, y3
        )
        self._entities.append(
            _Arc(cx, cy, r, start_ang, end_ang, layer)
        )
        return self

    def to_dxf(self) -> str:
        """
        Generate the DXF representation of the document.

        Returns:
        A string containing the complete DXF file content, including header, tables, entities, and EOF sections.
        """
        entities_dxf = "".join(e.to_dxf() for e in self._entities)

        return DXF_TEMPLATE.format(
            insunits=_UNITS[self._units],
            entities=entities_dxf.rstrip(),
        )

    def save(self, path):
        """
        Saves the created content in a DXF file.

        Parameters:
        path:   file name
        """
        with open(path, "w", encoding="ascii") as f:
            f.write(self.to_dxf())

    def bbox(self):
        """
        Returns the bounding box, limits of the drawing: (min_x, min_y, max_x, max_y)
        Returns None if the document is empty.
        """
        if not self._entities:
            return None

        boxes = [e.bbox() for e in self._entities]

        min_x = min(b[0] for b in boxes)
        min_y = min(b[1] for b in boxes)
        max_x = max(b[2] for b in boxes)
        max_y = max(b[3] for b in boxes)

        return min_x, min_y, max_x, max_y

    def width(self):
        """
        Returns the total width of the drawing (horizontal dimension)
        """
        b = self.bbox()
        return None if b is None else b[2] - b[0]

    def height(self):
        """
        Returns the total height of the drawing (vertical dimension)
        """
        b = self.bbox()
        return None if b is None else b[3] - b[1]

    def translate(self, dx, dy):
        """
        Moves thee entire drawing by the amount specified in axis x and y.

        Parameters:
        dx:     Horizontal displacement amount
        dy:     Vertical displacement amount
        """
        for e in self._entities:
            e.translate(dx, dy)
        return self

    def rotate(self, angle_deg):
        """
        Rotates the entire drawing with center (0,0) by the angle specified. The angle is
        defined in degrees. Positive angles are counterclockwise.

        Parameters:
        angle_deg:  Angle of rotation
        """
        for e in self._entities:
            e.rotate(angle_deg)
        return self

    def move_to_origin(self):
        """
        Translates all geometry so that the bounding box lower-left corner is (0, 0).
        """
        bbox = self.bbox()
        if bbox is None:
            return self

        min_x, min_y, _, _ = bbox
        self.translate(-min_x, -min_y)
        return self