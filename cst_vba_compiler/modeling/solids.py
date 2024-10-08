""" Python interface for CST methods from Modeling related to the manipulation of solids

author: Aaron Gobeyn
"""

from ..writer import VbaWriter


class Solids(object):
    @staticmethod
    def Add(writer: VbaWriter, solid_1: str, solid_2: str):
        """Boolean addition of two solids called `solid_1` and `solid_2`. The resulting
        solid is stored under `solid_1` and `solid_2` is deleted in the process.
        """
        writer.write(
            f"Solid.Add {VbaWriter.string_repr(text=solid_1)}, {VbaWriter.string_repr(text=solid_2)}\n"
        )
