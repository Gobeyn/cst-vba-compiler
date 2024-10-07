""" Python interface for the CST methods in Modeling -> Tools

author: Aaron Gobeyn
"""

from ..utils import wrap_nonstr_in_double_quotes
from ..writer import VbaWriter


class Transform(object):
    # NOTE: Only mirroring of shapes has been implemented.
    @staticmethod
    def Transform(
        writer: VbaWriter,
        name: str,
        transform_object_type: str,
        transform_method: str,
        plane_normal: tuple[float, float, float] = (1.0, 0.0, 0.0),
        origin: str = "ShapeCenter",
        center: tuple[float, float, float] | None = None,
        copy: bool = False,
        unite: bool = False,
        repetitions: int = 1,
    ) -> None:
        """Transform the object with name `name` of of type `transform_object_type` with the `transform_method`. The available options
        for `transform_object_type` are {"Shape", ...}. The possible `transform_method` options, what they do and the required arguments for
        them are shown in the table below.

        | Method | Description | Required Arguments |
        |________|_____________|____________________|
        | Mirror | Mirror the selected object with respect to a plane defined by its center and normal direction | `origin`, `center` and `plane_normal` |
        | ... | ... | ... |

        See https://space.mit.edu/RADIO/CST_online/mergedProjects/VBA_3D/special_vbatransformo/special_vbatransformo_transform_object.htm

        :param writer: VBA IO handler
        :type writer: VbaWriter
        :param name: Name of the object to transform.
        :type name: str
        :param transform_object_type: Type of the object to transform, available options are {"Shape", ...}
        :type transform_object_type: str
        :param transform_method: Transformation method, the available options are {"Mirror", ...}, see the method description for
            more details on each method.
        :type transform_method: str
        :param origin: Define origin for the transformation. The possible options are {"ShapeCenter", "CommonCenter", "Free"}.
        :type origin: str (default="ShapeCenter")
        :param center: Set the origin of the transformation manually, this is only possible of `origin` is set the "Free".
        :type center: tuple[float, float, float] | None (default=None)
        :param plane_normal: Define the normal of the mirroring plane. This will only do something if `transform_method` is "Mirror".
        :type plane_normal: tuple[float, float, float] (default=(1.0, 0.0, 0.0))
        :param copy: If `True`, the new solid is copied and the original untouched, if `False` the original object is deleted.
        :type copy: bool (default=False)
        :param unite: If `True`, the new object created during transformation (requires `copy` to be `True`) is united with the original object,
            otherwise the objects will remain separate.
        :type unite: bool (default=False)
        :param repetitions: Amount of times the transformation should be applied to the selected object.
        :type repetitions: int (default=1)
        """
        object_options = ["Shape"]
        method_options = ["Mirror"]

        assert (
            transform_object_type in object_options
        ), "Object type for the transformation is not of the supported options."
        assert (
            transform_method in method_options
        ), "Transformation method is not of the supported options"

        writer.start_with(structure="Transform")
        writer.write(".Reset\n")
        writer.write(f".Name {VbaWriter.string_repr(text=name)}\n")
        writer.write(f".Origin {VbaWriter.string_repr(text=origin)}\n")
        if center is not None:
            writer.write(
                f".Center {wrap_nonstr_in_double_quotes(value=center[0])}, {wrap_nonstr_in_double_quotes(value=center[1])}, {wrap_nonstr_in_double_quotes(value=center[2])}\n"
            )
        writer.write(
            f".PlaneNormal {wrap_nonstr_in_double_quotes(value=plane_normal[0])}, {wrap_nonstr_in_double_quotes(value=plane_normal[1])}, {wrap_nonstr_in_double_quotes(value=plane_normal[2])}\n"
        )
        writer.write(f".MultipleObjects {wrap_nonstr_in_double_quotes(value=copy)}\n")
        writer.write(f".GroupObjects {wrap_nonstr_in_double_quotes(value=unite)}\n")
        writer.write(
            f".Transform {VbaWriter.string_repr(text=transform_object_type)}, {VbaWriter.string_repr(text=transform_method)}\n"
        )
        writer.write(
            f".Repetitions {wrap_nonstr_in_double_quotes(value=repetitions)}\n"
        )
        writer.end_with()
