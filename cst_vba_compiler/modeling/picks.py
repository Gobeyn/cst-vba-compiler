""" Python interface for the CST methods under Modeling -> Picks

author: Aaron Gobeyn
"""

from ..utils import wrap_nonstr_in_double_quotes
from ..writer import VbaWriter


class Picks(object):
    @staticmethod
    def PickFaceFromId(writer: VbaWriter, name: str, id: int) -> None:
        """Pick a face of a solid called `name` under the identity number `id`.

        See: https://space.mit.edu/RADIO/CST_online/mergedProjects/VBA_3D/common_vbapicko/common_vbapicko_pick_object.htm

        :param writer: VBA IO handler
        :type writer: VbaWriter
        :param name: Name of the solid to pick the face from
        :type name: str
        :param id: Identity number of the face in that solid
        :type id: int
        """
        writer.write(
            f"Pick.PickFaceFromId {VbaWriter.string_repr(text=name)}, {wrap_nonstr_in_double_quotes(value=id)}\n"
        )

    @staticmethod
    def PickEdgeFromId(
        writer: VbaWriter, name: str, edge_id: int, vertex_id: int
    ) -> None:
        """Pick an edge of a solid called `name`. The edge is specified with the edge identity number
        `edge_id`. The starting point of the edge is also required and is specified with the
        vertex identity number `vertex_id`.

        See: https://space.mit.edu/RADIO/CST_online/mergedProjects/VBA_3D/common_vbapicko/common_vbapicko_pick_object.htm

        :param writer: VBA IO handler
        :type writer: VbaWriter
        :param name: Name of the solid to pick the edge from.
        :type name: str
        :param edge_id: Identity number of the edge within the solid.
        :type edge_id: int
        :param vertex_id: Identity number of the starting point of the edge within the solid.
        :type vertex_id: int
        """
        writer.write(
            f"Pick.PickEdgeFromId {VbaWriter.string_repr(text=name)}, {wrap_nonstr_in_double_quotes(value=edge_id)}, {wrap_nonstr_in_double_quotes(value=vertex_id)}\n"
        )
