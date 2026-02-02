# MiniDXF - Minimal DXF writer
# Copyright (C) 2026 Gumer Freire
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

import math

## HELPER FUNCTIONS
def _rotate_point(x, y, angle_deg):
    rad = math.radians(angle_deg)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)

    return (
        x * cos_a - y * sin_a,
        x * sin_a + y * cos_a,
    )

def _arc_from_3_points(x1, y1, x2, y2, x3, y3):
    det = 2 * (x1*(y2 - y3) + x2*(y3 - y1) + x3*(y1 - y2))
    if abs(det) < 1e-9:
        raise ValueError("Points are colinear")

    a = x1**2 + y1**2
    b = x2**2 + y2**2
    c = x3**2 + y3**2

    cx = (a*(y2 - y3) + b*(y3 - y1) + c*(y1 - y2)) / det
    cy = (a*(x3 - x2) + b*(x1 - x3) + c*(x2 - x1)) / det

    r = math.hypot(cx - x1, cy - y1)

    start_ang = math.degrees(math.atan2(y1 - cy, x1 - cx))
    mid_ang   = math.degrees(math.atan2(y3 - cy, x3 - cx))
    end_ang   = math.degrees(math.atan2(y2 - cy, x2 - cx))

    def is_between(a, b, c):
        a, b, c = a % 360, b % 360, c % 360
        if a < c:
            return a < b < c
        return b > a or b < c

    if not is_between(start_ang, mid_ang, end_ang):
        start_ang, end_ang = end_ang, start_ang

    return cx, cy, r, start_ang, end_ang

## CLASS DEFINITION
class _DXFEntity:
    def to_dxf(self) -> str:
        raise NotImplementedError

    def bbox(self):
        raise NotImplementedError

    def translate(self, dx, dy):
        raise NotImplementedError
    
    def rotate(self, angle_deg):
        raise NotImplementedError

## ENTITIES CLASSES
class _Line(_DXFEntity):
    def __init__(self, x1, y1, x2, y2, layer="0"):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.layer = layer

    def to_dxf(self) -> str:
        return f"""0
LINE
8
{self.layer}
10
{self.x1}
20
{self.y1}
30
0.0
11
{self.x2}
21
{self.y2}
31
0.0
"""
    def bbox(self):
        return (
            min(self.x1, self.x2),
            min(self.y1, self.y2),
            max(self.x1, self.x2),
            max(self.y1, self.y2),
        )

    def translate(self, dx, dy):
        self.x1 += dx
        self.y1 += dy
        self.x2 += dx
        self.y2 += dy

    def rotate(self, angle_deg):
        self.x1, self.y1 = _rotate_point(self.x1, self.y1, angle_deg)
        self.x2, self.y2 = _rotate_point(self.x2, self.y2, angle_deg)

class _Arc(_DXFEntity):
    def __init__(self, cx, cy, radius, start_angle, end_angle, layer="0"):
        self.cx = cx
        self.cy = cy
        self.radius = radius
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.layer = layer

    def to_dxf(self) -> str:
        return f"""0
ARC
8
{self.layer}
10
{self.cx}
20
{self.cy}
30
0.0
40
{self.radius}
50
{self.start_angle}
51
{self.end_angle}
"""
    def bbox(self):
        angles = [self.start_angle, self.end_angle]

        for a in (0, 90, 180, 270):
            if self._angle_in_arc(a):
                angles.append(a)

        xs = []
        ys = []

        for a in angles:
            rad = math.radians(a)
            xs.append(self.cx + self.radius * math.cos(rad))
            ys.append(self.cy + self.radius * math.sin(rad))

        return min(xs), min(ys), max(xs), max(ys)

    def _angle_in_arc(self, angle):
        a1 = self.start_angle % 360
        a2 = self.end_angle % 360
        angle = angle % 360

        if a1 <= a2:
            return a1 <= angle <= a2
        else:
            # wrapped arc (e.g. 300° → 45°)
            return angle >= a1 or angle <= a2

    def translate(self, dx, dy):
        self.cx += dx
        self.cy += dy

    def rotate(self, angle_deg):
        self.cx, self.cy = _rotate_point(self.cx, self.cy, angle_deg)
        self.start_angle += angle_deg
        self.end_angle += angle_deg