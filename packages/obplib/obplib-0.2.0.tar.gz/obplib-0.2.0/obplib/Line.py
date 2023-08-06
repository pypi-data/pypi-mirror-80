# SPDX-FileCopyrightText: 2019,2020 Freemelt AB
#
# SPDX-License-Identifier: Apache-2.0

"""
Copyright 2019,2020 Freemelt AB

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""


"""@Line docstring
A class which describes a line drawn between point P1 and P2 using a specified scan speed and specified beam paramters
"""

# PyPI
from google.protobuf.json_format import MessageToDict

# Project
import obplib.OBP_pb2 as OBP
from obplib.Point import Point
from obplib.Beamparameters import Beamparameters


class Line:
    def __init__(self, P1, P2, Speed, bp):
        """
        Constructor for the Line class

        Args:
            P1 (Point): The start point
            P2 (Point): The end point
            Speed (Int): Speed in µm/s
            bp (Beamparameters): Beam parameters
        """
        self.P1 = P1
        self.P2 = P2
        self.Speed = Speed
        self.bp = bp

    @classmethod
    def from_dict(cls, kw):
        """
        Returns an instance of the Line class created using parameters specified in a dictionary

        Args:
            kw (dictionary): A dictionary representation of a Line object
        """
        P1 = Point(kw["x0"], kw["y0"])
        P2 = Point(kw["x1"], kw["y1"])
        speed = int(kw["speed"])
        bp = Beamparameters(kw["params"]["spotSize"], kw["params"]["beamPower"])
        return cls(P1, P2, speed, bp)

    def get_pb(self):
        """
        Returns a protobuf packet containing Line information

        Returns:
            pkt (binary): A packet protobuf containing line info
        """
        pkt = OBP.Packet()
        line1 = OBP.Line()
        line1.params.CopyFrom(self.bp.get_pb())
        line1.x0 = self.P1.x
        line1.x1 = self.P2.x
        line1.y0 = self.P1.y
        line1.y1 = self.P2.y
        line1.speed = self.Speed
        pkt.line.CopyFrom(line1)

        return pkt

    def get_packet(self, packet):
        """
        Returns a serialized packet

        Args:
            packet (binary): A packet

        Returns:
            A serialized packet (String): A serialized packet
        """
        pkt = packet.SerializeToString()
        return pkt

    def write_obp(self):
        """
        Overloaded writer method - is called by the FileHandler when writing to obp

        Returns:
            serialized (binary): A serialized protobuf packet
        """
        return self.get_packet(self.get_pb())

    def get_obpj(self):
        """
        Overloaded writer method - is called by the FileHandler when writing to obpj

        Returns:
            d (dictionary): A dictionary representation of a protobuf packet
        """
        d = MessageToDict(self.get_pb())
        return d

    def translate(self, V):
        """
        Returns a new Line object which has been translated according to the given vector V

        Args:
            V (Vector): A translation vector

        Returns:
            Line: A Line which has been traslated according to the given vector
        """
        return Line(self.P1.translate(V), self.P2.translate(V), self.Speed, self.bp)

    def rotate(self, theta):
        """
        Returns a new Line which has been rotated theta radians around the origin

        Args:
            theta (radians): The amount of radians which the Line is to be rotated

        Returns:
            Line: A Line rotated theta radians relative to the origin
        """
        return Line(self.P1.rotate(theta), self.P2.rotate(theta), self.Speed, self.bp)

    def scale(self, factor):
        """
        Returns a new Line scaled by the specified factor.

        Args:
            factor (float): The factor with which to scale the Line

        Returns:
            Line: A Line scaled using the specified factor
        """
        return Line(self.P1.scale(factor), self.P2.scale(factor), self.Speed, self.bp)

    def null_attr(self, attr):
        if (attr) == None:
            return 0
