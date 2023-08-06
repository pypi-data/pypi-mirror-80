<!--
SPDX-FileCopyrightText: 2019,2020 Freemelt AB

SPDX-License-Identifier: Apache-2.0
-->

# OBPlib-Python
Python library to generate OBP data for metal 3d printers.

## Minimum example
Create two points and a set of beam parameters. Create a line with these params and a speed. Write as binary and textual OBP data to files. 

```
import obplib as obp

a = obp.Point(1,1)
b = obp.Point(2,2)

bp = obp.Beamparameters(1,1)

line = obp.Line(a,b,1,bp)

obp.write_obpj([line], "test.obpj")
obp.write_obp([line], "test.obp")
```

## obpc
This package contains the obpc tool that can convert back and forth between binary and textual OBP. 
