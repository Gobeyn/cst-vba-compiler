""" Python interface for the CST methods under Modeling -> Shapes

author: Aaron Gobeyn
"""

from ..utils import wrap_nonstr_in_double_quotes
from ..writer import VbaWriter


class Faces(object):
    @staticmethod
    def Face(
        writer: VbaWriter,
        name: str,
        mode: str,
        curve: str | None = None,
        twistangle: float | None = None,
        thickness: float | None = None,
        taperangle: float | None = None,
        offset: float | None = None,
    ) -> None:
        """Create a `Face` object called `name` under the `Faces` folder by one of three methods:
        1. mode="PickFace": Face is defined via the picked face of a solid (see `picks.py`). The
            face can be place an amount `offset` from the picked face.
        2. mode="ExtrudeCurve": Define face by extruding a curve profile, e.g. a curve object
            called `curve` under the `Curves` folder. The taper angle of the extrusion is
            determined by `taperangle` and the twist angle by `twistangle`.
        3. mode="CoverCurve": Define face by covering a curve profile, e.g. a curve object
            called `curve` under the `Curves` folder.

        See: https://space.mit.edu/RADIO/CST_online/mergedProjects/VBA_3D/common_vbafaces/common_vbafaces_face_object.htm

        :param writer: VBA IO handler
        :type writer: VbaWriter
        :param name: Name of the created Face stored under the `Faces` folder.
        :type name: str
        :param mode: One of three possible ways to select a face, "PickFace", "ExtrudeCurve" or "CoverCurve".
            See the function of each mode in the description of this method.
        :type mode: str
        :param curve: Curve object called `curve` under the `Curves` folder. This is an optional argument
            only required when the face is determined using a curve based mode.
        :type curve: str | None (default=None)
        :param twistangle: Twist angle to use when the face is defined via curve extrusion. The angle is
            assumed to be in degrees (0 to 360). This argument is always optional.
        :type twistangle: float | None (default=None)
        :param thickness: Thickness of the created face. If unspecified the thickness is 0.0. The argument is
            always optional.
        :type thickness: float | None (default=None)
        :param taperangle: Taper angle to use when the face is defined via curve extrusion. The angle is assumed
            to be in degrees (0 to 360). This argument is always optional.
        :type taperangle: float | None (default=None)
        :param offset: Amount to offset face when the face is picked from a Solid. When unspecified the offset is
            0.0. This argument is always optional.
        :type offset: float | None (default=None)
        """
        # Check if the mode is a valid one.
        assert (
            mode == "PickFace" or mode == "ExtrudeCurve" or mode == "CoverCurve"
        ), "The provided mode for Face selection is not a valid mode."
        # Check that if the mode is curve based, a curve is actually provided.
        assert (mode == "ExtrudeCurve" and curve is not None) or (
            mode == "CoverCurve" and curve is not None
        ), "Mode for face creation is a curved based mode, but no curve was provided."

        writer.start_with(structure="Face")
        writer.write(".Reset\n")
        writer.write(f".Name {VbaWriter.string_repr(text=name)}\n")
        writer.write(f".Type {VbaWriter.string_repr(text=mode)}\n")
        if curve is not None:
            writer.write(f".Curve {VbaWriter.string_repr(text=curve)}\n")
        if (offset is not None) and (mode == "PickFace"):
            writer.write(f".Offset {wrap_nonstr_in_double_quotes(value=offset)}\n")
        if taperangle is not None and mode == "ExtrudeCurve":
            writer.write(
                f".Taperangle {wrap_nonstr_in_double_quotes(value=taperangle)}\n"
            )
        if thickness is not None:
            writer.write(
                f".Thickness {wrap_nonstr_in_double_quotes(value=thickness)}\n"
            )
        if twistangle is not None and mode == "ExtrudeCurve":
            writer.write(
                f".Twistangle {wrap_nonstr_in_double_quotes(value=twistangle)}\n"
            )
        writer.write(".Create\n")
        writer.end_with()

    @staticmethod
    def DeleteFace(writer: VbaWriter, name: str) -> None:
        """Delete the Face called `name` stored under the `Faces` folder.

        See: https://space.mit.edu/RADIO/CST_online/mergedProjects/VBA_3D/common_vbafaces/common_vbafaces_face_object.htm

        :param writer: VBA IO handler
        :type writer: VbaWriter
        :param name: Name of the face to delete.
        :type name: str
        """
        writer.write(f"Face.Delete {VbaWriter.string_repr(text=name)}\n")


class FromProfile2D(object):
    # NOTE: Not all possible arguments have been implemented.
    @staticmethod
    def Rotate(
        writer: VbaWriter,
        name: str,
        component: str,
        material: str,
        mode: str,
        angle: float = 360.0,
        height: float = 0.0,
        radius_ratio: float = 1.0,
        Nsteps: int = 0,
        number_of_picked_faces: int = 1,
        start_angle: float | None = None,
        split_closed_edges: bool = True,
        segmented_profile: bool = False,
        delete_base_face_solid: bool = False,
        clear_picked_face: bool = True,
        simplify_solid: bool = True,
        use_advanced_segmented_rotation: bool = True,
        cut_end_off: bool = False,
    ) -> None:
        """
        Create a solid by rotating a face. The name of the resulting object is specified by `name` and the component
        under which it is stored (which must already exist!) is `component`. The material of the solid is set by `material`,
        note that the material must already exist. By default there is "Vacuum" and "PEC". The rotation can occur in two modes,
        "Pointlist", where the profile is defined by a list of points that are rotated, and "Picks" where a picked face is rotated. Other
        parameters and flags can be set, see the documentation of the arguments below.

        See: https://space.mit.edu/RADIO/CST_online/mergedProjects/VBA_3D/common_vbarotateo/common_vbarotateo_rotate_object.htm

        :param writer: VBA IO handler
        :type writer: VbaWriter
        :param name: Name of the generated solid.
        :type name: str
        :param component: Name of the component under which the solid should be stored. Note that this component must exist.
        :type component: str
        :param material: Name of material of the solid. The material must already exist.
        :type material: str
        :param mode: Mode of the rotation, this can either be "Pointlist" or "Picks".
        :type mode: str
        :param angle: Set the angle of rotation, in degrees. If the mode is "Pointlist", the angle will start from `start_angle`.
        :type angle: float (default=360.0)
        :param height: Bend the rotated solid along the axis of rotation such that a helix is formed. This parameter specifies the distance
            between the start and end profile along the rotation axis.
        :type height: float (default=0.0)
        :param radius_ratio: Defines the ratio between the radius after a 360 degree rotation with respect to the starting radius. The radius changes
            linearly depending on the angle of rotation. The radius is defined as the distance from axis of rotation and center of gravity of the
            to be rotated profile.
        :type radius_ratio: float (default=1.0)
        :param Nsteps: Defines the number of segments the rotated solid will be made out of. If set to zero, the created shape is analytical.
        :type Nsteps: int (default=0)
        :param number_of_picked_faces: We could not find documentation for this, but it is used in the macro for a TESLA half cell from TU Darmstadt.
        :type number_of_picked_faces: int (default=1)
        :param start_angle: Starting angle for the rotation, in degrees. This is only for the case where the mode is "Pointlist".
        :type start_angle: float | None (default=None)
        :param split_closed_edges: Needs to be `True` for backwards compatibility
        :type split_closed_edges: bool (default=True)
        :param segmented_profile: The rotation will be done by the defined number of segments
        :type segmented_profile: bool (default=False)
        :param delete_base_face_solid: Delete the face used for rotation after the solid is created.
        :type delete_base_face_solid: bool (default=False)
        :param clear_picked_face: Clear the Pick of the Face after the rotation.
        :type clear_picked_face: bool (default=True)
        :param simplify_solid: Needs to be `True` for backwards compatibility
        :type simplify_solid: bool (default=True)
        :param use_advanced_segmented_rotation: Needs to be `True` for backwards compatibility
        :type use_advanced_segmented_rotation: bool (default=True)
        :param cut_end_off: We could not find documentation for this, but it is used in the macro for a TESLA half cell from TU Darmstadt.
        :type cut_end_off: bool (default=False)
        """
        assert (
            mode == "Pointlist" or mode == "Picks"
        ), "Provided mode is not supported, must be Pointlist or Picks."

        writer.start_with(structure="Rotate")
        writer.write(f".Name {VbaWriter.string_repr(text=name)}\n")
        writer.write(f".Component {VbaWriter.string_repr(text=component)}\n")
        writer.write(
            f".NumberOfPickedFaces {wrap_nonstr_in_double_quotes(value=number_of_picked_faces)}\n"
        )
        writer.write(f".Material {VbaWriter.string_repr(text=material)}\n")
        writer.write(f".Mode {VbaWriter.string_repr(text=mode)}\n")
        if start_angle is not None and mode == "Pointlist":
            writer.write(f".StartAngle {wrap_nonstr_in_double_quotes(start_angle)}\n")
        writer.write(f".Angle {wrap_nonstr_in_double_quotes(value=angle)}\n")
        writer.write(f".Height {wrap_nonstr_in_double_quotes(value=height)}\n")
        writer.write(
            f".RadiusRatio {wrap_nonstr_in_double_quotes(value=radius_ratio)}\n"
        )
        writer.write(f".NSteps {wrap_nonstr_in_double_quotes(value=Nsteps)}\n")
        writer.write(
            f".SplitClosedEdges {wrap_nonstr_in_double_quotes(value=split_closed_edges)}\n"
        )
        writer.write(
            f".SegmentedProfile {wrap_nonstr_in_double_quotes(value=segmented_profile)}\n"
        )
        writer.write(
            f".DeleteBaseFaceSolid {wrap_nonstr_in_double_quotes(value=delete_base_face_solid)}\n"
        )
        writer.write(
            f".ClearPickedFace {wrap_nonstr_in_double_quotes(value=clear_picked_face)}\n"
        )
        writer.write(
            f".SimplifySolid {wrap_nonstr_in_double_quotes(value=simplify_solid)}\n"
        )
        writer.write(
            f".UseAdvancedSegmentedRotation {wrap_nonstr_in_double_quotes(value=use_advanced_segmented_rotation)}\n"
        )
        writer.write(f".CutEndOff {wrap_nonstr_in_double_quotes(value=cut_end_off)}\n")

        writer.write(".Create\n")
        writer.end_with()


# class Shapes(object):
#     pass
