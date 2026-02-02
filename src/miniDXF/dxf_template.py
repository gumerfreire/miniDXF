# MiniDXF - Minimal DXF writer
# Copyright (C) 2026 Gumer Freire
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

DXF_TEMPLATE = """0
SECTION
2
HEADER
9
$ACADVER
1
AC1009
9
$INSUNITS
70
{insunits}
0
ENDSEC
0
SECTION
2
TABLES
0
TABLE
2
LAYER
70
1
0
LAYER
2
0
70
0
62
7
6
CONTINUOUS
0
ENDTAB
0
ENDSEC
0
SECTION
2
BLOCKS
0
ENDSEC
0
SECTION
2
ENTITIES
{entities}
0
ENDSEC
0
SECTION
2
OBJECTS
0
ENDSEC
0
EOF
"""