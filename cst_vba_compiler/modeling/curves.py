""" Python interface for the CST methods under Modeling -> Curves

author: Aaron Gobeyn
date: 01-10-2024
"""

from ..utils import num_or_list_of_nums_to_str, wrap_nonstr_in_double_quotes
from ..writer import VbaWriter


class Curves:
    @staticmethod
    def Ellipse(
        writer: VbaWriter,
        name: str,
        center: tuple[float | str, float | str],
        x_radius: float | str,
        y_radius: float | str,
        segments: int = 0,
        curve: str = "curve",
    ):
        """Create 2D ellipse in the xy-plane centered on `center` with radius `x_radius` in the $x$-direction and
        radius `y_radius` in the $y$-direction. If the value of `segments` is $0$, the ellipse is a perfect, unsegmented ellipse.
        Otherwise, the values should be greater than $2$ and the ellipse is represented by a segmented polygonal curve.

        See: https://space.mit.edu/RADIO/CST_online/mergedProjects/3D/common_struct/common_struct_curveellipse.htm

        :param writer: VBA IO handler
        :type writer: VbaWriter
        :param name: Name of the Ellipse
        :type name: str
        :param center: $(x,y)$ coordinates of the Ellipse center. The values can either be literal (`float`) or
            the name of a parameter (`str`).
        :type center: tuple[float | str, float | str]
        :param x_radius: Ellipse radius in the $x$-direction. The value can either be literal (`float`) or the name
            of a parameter (`str`).
        :type x_radius: float | str
        :param y_radius: Ellipse radius in the $y$-direction. The value van either be literal (`float`) or the name of
            a parameter (`str`).
        :type y_radius: float | str
        :param segments: Amount of segments the Ellipse should be split into. If $0$, the ellipse is unsegmented (perfect),
            otherwise the value should be larger than $2$ and the Ellipse is represented by a segmented polygonal curve.
        :type segments: int (default=0)
        :param curve: Name of the folder under Curves where the Ellipse is stored.
        :type curve: str (default="curve")
        """

        # Start the `With` block
        writer.start_with(structure="Ellipse")
        # Default line that always appears for some reason
        writer.write(text=".Reset\n")
        # Set the name of the ellipse
        writer.write(text=f".Name {VbaWriter.string_repr(text=name)}\n")
        # Set the name of the curve
        writer.write(text=f".Curve {VbaWriter.string_repr(text=curve)}\n")
        # Set the x-radius
        writer.write(text=f".XRadius {wrap_nonstr_in_double_quotes(value=x_radius)}\n")
        # Set the y-radius
        writer.write(text=f".YRadius {wrap_nonstr_in_double_quotes(value=y_radius)}\n")
        # Set the x-coordinate of the center
        writer.write(text=f".Xcenter {wrap_nonstr_in_double_quotes(center[0])}\n")
        # Set the y-coordinate of the center
        writer.write(text=f".Ycenter {wrap_nonstr_in_double_quotes(center[1])}\n")
        # Set the segments
        writer.write(text=f".Segments {wrap_nonstr_in_double_quotes(segments)}\n")
        # Create the curve
        writer.write(text=".Create\n")
        # End the `With` block
        writer.end_with()

    @staticmethod
    def Line(
        writer: VbaWriter,
        name: str,
        start_point: tuple[float | str, float | str],
        end_point: tuple[float | str, float | str],
        curve: str = "curve",
    ) -> None:
        """Create a 2D line in the xy-plane called `name` in the Curves folder under the name `curve`
        starting from `start_point` and ending at `end_point`.

        See: https://space.mit.edu/RADIO/CST_online/mergedProjects/3D/common_struct/common_struct_curveline.htm

        :param writer: VBA IO handler
        :type writer: VbaWriter
        :param name: Name of the created Line
        :type name: str
        :param start_point: Tuple of numeric values (`float`) and/or parameter names (`str`) containing the $(x,y)$ values at which the Line
            starts.
        :type start_point: tuple[float | str, float | str]
        :param end_point: Tuple of numeric values (`float`) and/or parameter names (`str`) containing the $(x,y)$ values at which the Line ends.
        :type end_point: tuple[float | str, float | str]
        :param curve: Name of the folder under Curves where the Line is stored.
        :type curve: str (default="curve")
        """
        # Start the `With` block
        writer.start_with(structure="Line")
        # Default line that always appears for some reason
        writer.write(text=".Reset\n")
        # Set the name of the line
        writer.write(text=f".Name {VbaWriter.string_repr(text=name)}\n")
        # Set the name of the curve
        writer.write(text=f".Curve {VbaWriter.string_repr(text=curve)}\n")
        # Set x-coordinate of first point
        writer.write(text=f".X1 {wrap_nonstr_in_double_quotes(value=start_point[0])}\n")
        # Set y-coordinate of first point
        writer.write(text=f".Y1 {wrap_nonstr_in_double_quotes(value=start_point[1])}\n")
        # Set x-coordinate of second point
        writer.write(text=f".X2 {wrap_nonstr_in_double_quotes(value=end_point[0])}\n")
        # Set y-coordinate of second point
        writer.write(text=f".Y2 {wrap_nonstr_in_double_quotes(value=end_point[1])}\n")
        # Create the line
        writer.write(text=f".Create\n")
        # End the `With` block
        writer.end_with()

    @staticmethod
    def Polygon(
        writer: VbaWriter,
        name: str,
        start_point: tuple[float | str, float | str],
        next_points: list[tuple[float | str, float | str]],
        which_relative: list[bool] | None = None,
        curve: str = "curve",
    ) -> None:
        """
        Create a 2D polygon curve, the curve starts at `start_point` and connects the `next_points` in lines, e.g.
        `start_point` is connected to `next_points[0]`, which is connection to `next_points[1]` etc. By default, each
        point in the `next_points` list is assumed to be an absolute point. It is also possible to interpret a point in
        `next_points` as relative to the previous point. A point will be interpreted as relative, if the index for said point
        in the `which_relative` list is set to `True`, e.g. if point `next_points[i]` needs to be interpreted as relative,
        `which_relative[i]` should be `True`, otherwise it should be `False`.

        See: https://space.mit.edu/RADIO/CST_online/mergedProjects/VBA_3D/common_vbacurves/common_vbacurves_polygon_object.htm

        :param writer: VBA IO handler
        :type writer: VbaWriter
        :param name: Name of the created line
        :type name: str
        :param start_point: Starting $(x,y)$ point of the polygonal curve, specified as a tuple of numeric values (`float`) and/or
            parameter names (`str`).
        :type start_point: tuple[float | str, float | str]
        :param next_points: List of points in the same format as `start_point` that connect, in sequence, to form the polygonal curve.
        :type next_points: list[tuple[float | str, float | str]]
        :param which_relative: List of boolean values specifying which points should be interpreted as relative to the previous point (`True`) and
            which as absolute points (`False`). If set the `None` (the default value), it is equivalent to having a list of `False` values. Note that
            the length of the list should be of equal length as the `next_points` list.
        :type which_relative: list[bool] | None (default=None)
        :param curve: Name of the folder under Curves where the Polygon is stored.
        :type curve: str (default="curve")
        """
        # Check that at least one connecting point is given
        assert (
            len(next_points) >= 1
        ), "At least one connecting point is needed to define a Polygon Curve."
        # If `which_relative` is `None`, interpret as array of `False` values
        if which_relative is None:
            which_relative: list[bool] = [False for _ in range(len(next_points))]
        else:
            # Check that every connecting point has an interpretation
            assert len(next_points) == len(
                which_relative
            ), "Length of `next_points` array is not equal to the length of `which_relative` array."

        # Start `With` block
        writer.start_with(structure="Polygon")
        # Write reset line
        writer.write(".Reset\n")
        # Set name of curve
        writer.write(f".Name {VbaWriter.string_repr(text=name)}\n")
        # Set the name of the curve
        writer.write(text=f".Curve {VbaWriter.string_repr(text=curve)}\n")
        # Set starting point
        writer.write(
            f".Point {wrap_nonstr_in_double_quotes(value=start_point[0])}, {wrap_nonstr_in_double_quotes(value=start_point[1])}\n"
        )
        # Write connecting point lines
        for point, is_relative in zip(next_points, which_relative):
            if is_relative:
                writer.write(
                    f".RLine {wrap_nonstr_in_double_quotes(value=point[0])}, {wrap_nonstr_in_double_quotes(value=point[1])}\n"
                )
            else:
                writer.write(
                    f".LineTo {wrap_nonstr_in_double_quotes(value=point[0])}, {wrap_nonstr_in_double_quotes(value=point[1])}\n"
                )
        # Create Polygon
        writer.write(".Create\n")
        # End `With` block
        writer.end_with()

    @staticmethod
    def TrimCurves(
        writer: VbaWriter,
        curve_item_1: str,
        curve_item_2: str,
        delete_edges_1: int | list[int],
        delete_edges_2: int | list[int],
        curve: str = "curve",
    ) -> None:
        """
        Trim two intersecting items under the Curves folder. Points of intersection created new segments/edges which can be deleted (trimmed).
        Note that the items must be stored in Curves under the same curve object.

        See: https://space.mit.edu/RADIO/CST_online/mergedProjects/VBA_3D/common_vbacurves/common_vbacurves_trimcurves_object.htm

        :param writer: VBA IO handler
        :type writer: VbaWriter
        :param curve_item_1: Name of curve item under Curves/`curve` to intersect with `curve_item_2`.
        :type curve_item_1: str
        :param curve_item_2: Name of curve item under Curves/`curve` to intersect with `curve_item_1`.
        :type curve_item_2: str
        :param delete_edges_1: Edge, or list of edges, of `curve_item_1` defined due to the curve intersection that
            will be deleted by the Trim operation.
        :type delete_edges_1: int | list[int]
        :param delete_edges_2: Edge, or list of edges, of `curve_item_1` defined due to the curve intersection that
            will be deleted by the Trim operation.
        :type delete_edges_2: int | list[int]
        :param curve: Name of the folder under Curves where the Ellipse is stored.
        :type curve: str (default="curve")
        """
        # Start the `With` block
        writer.start_with(structure="TrimCurves")
        # Default line that always appears for some reason
        writer.write(text=".Reset\n")
        # Set the curve object
        writer.write(text=f".Curve {VbaWriter.string_repr(text=curve)}\n")
        # Set the first curve item
        writer.write(text=f".CurveItem1 {VbaWriter.string_repr(text=curve_item_1)}\n")
        # Set the second curve item
        writer.write(text=f".CurveItem2 {VbaWriter.string_repr(text=curve_item_2)}\n")
        # Set the edges to trim for the first curve
        writer.write(
            text=f".DeleteEdges1 {num_or_list_of_nums_to_str(nums=delete_edges_1)}\n"
        )
        # Set the edges to trim for the second curve
        writer.write(
            text=f".DeleteEdges2 {num_or_list_of_nums_to_str(nums=delete_edges_2)}\n"
        )
        # Execute the Trim
        writer.write(text=".Trim\n")
        # End the `With` block
        writer.end_with()
