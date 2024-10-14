""" Python API for CST methods under Simulation -> Settings

author: Aaron Gobeyn
"""

from ..utils import wrap_nonstr_in_double_quotes
from ..writer import VbaWriter


class Settings(object):
    # NOTE: We used everything listed on the documentation website, but there are a lot more options in CST itself, maybe they can also be accessed
    # using VBA but we're not sure.
    @staticmethod
    def Background(
        writer: VbaWriter,
        material_type: str,
        apply_in_all_directions: bool,
        epsilon: float | None = None,
        mu: float | None = None,
        electric_conductivity: float | None = None,
        x_bounds: tuple[float, float] | None = None,
        y_bounds: tuple[float, float] | None = None,
        z_bounds: tuple[float, float] | None = None,
        thermal_type: str | None = None,
        thermal_conductivity: float | None = None,
    ) -> None:
        """Set the material of the background that surrounds the structure. By default the volume is defined by the maximum distance of the structure. The
        bounds can be set manually with the `x_bounds`, `y_bounds` and `z_bounds`, though this requires `apply_in_all_directions` to be `False`. There are two options for the material type set with the `material_type`
        parameter. If `normal`, one can set the `epsilon`, `mu` and `electric_conductivity` parameters, and also configure thermal properties with
        `thermal_type` and `thermal_conductivity`.

        See: https://space.mit.edu/RADIO/CST_online/mergedProjects/VBA_3D/special_vbasolver/special_vbasolver_background_object.htm

        :param writer: VBA IO handler
        :type writer: VbaWriter
        :param material_type: Set background material, either 'normal' or 'pec'.
        :type material_type: str
        :param apply_in_all_directions: Apply value set by x-direction lower bound for all directions.
        :type apply_in_all_directions: bool
        :param epsilon: Relative electric permittivity, defaults to "1.0" if no value is provided.
        :type epsilon: float | None (default=None)
        :param mu: Relative magnetic permeability, defaults to "1.0" if no value is provided.
        :type mu: float | None (default=None)
        :param electric_conductivity: Electric conductivity, set in S/m and defaults to "0.0" if no value is provided.
        :type electric_conductivity: float | None (default=None)
        :param x_bounds: X-range of the background bounding box, by default uses the minimal and maximal values of the structure.
        :type x_bounds: tuple[float, float] | None (default=None)
        :param y_bounds: Y-range of the background bounding box, by default uses the minimal and maximal values of the structure.
        :type y_bounds: tuple[float, float] | None (default=None)
        :param z_bounds: Z-range of the background bounding box, by default uses the minimal and maximal values of the structure.
        :type z_bounds: tuple[float, float] | None (default=None)
        :param thermal_type: Set thermal type of background material, either 'normal' or 'ptc', set to 'normal' by default.
        :type thermal_type: str | None (default=None)
        :param thermal_conductivity: Set thermal conductivity in W/K/m, set to "0.0" by default.
        :type thermal_conductivity: float | None (default=None)
        """
        assert material_type in [
            "normal",
            "pec",
        ], "Material type is not of the valid options: 'normal' or 'pec'."
        if thermal_type is not None:
            assert thermal_type in [
                "normal",
                "type",
            ], "Thermal type is not of the valid options: 'normal' or 'ptc'"

        writer.start_with(structure="Background")
        writer.write(".Reset\n")
        writer.write(f".Type {VbaWriter.string_repr(text=material_type)}\n")
        if epsilon is not None:
            writer.write(f".Epsilon {wrap_nonstr_in_double_quotes(value=epsilon)}\n")
        if mu is not None:
            writer.write(f".Mu {wrap_nonstr_in_double_quotes(value=mu)}\n")
        if electric_conductivity is not None:
            writer.write(
                f".ElConductivity {wrap_nonstr_in_double_quotes(value=electric_conductivity)}\n"
            )
        if x_bounds is not None:
            writer.write(
                f".XminSpace {wrap_nonstr_in_double_quotes(value=x_bounds[0])}\n"
            )
            writer.write(
                f".XmaxSpace {wrap_nonstr_in_double_quotes(value=x_bounds[1])}\n"
            )
        if y_bounds is not None:
            writer.write(
                f".YminSpace {wrap_nonstr_in_double_quotes(value=y_bounds[0])}\n"
            )
            writer.write(
                f".YmaxSpace {wrap_nonstr_in_double_quotes(value=y_bounds[1])}\n"
            )
        if z_bounds is not None:
            writer.write(
                f".ZminSpace {wrap_nonstr_in_double_quotes(value=z_bounds[0])}\n"
            )
            writer.write(
                f".ZmaxSpace {wrap_nonstr_in_double_quotes(value=z_bounds[1])}\n"
            )
        if thermal_type is not None:
            writer.write(f".ThermalType {VbaWriter.string_repr(text=thermal_type)}\n")
        if thermal_conductivity is not None:
            writer.write(
                f".ThermalConductivity {wrap_nonstr_in_double_quotes(value=thermal_conductivity)}\n"
            )
        writer.write(
            f".ApplyInAllDirections {wrap_nonstr_in_double_quotes(value=apply_in_all_directions)}\n"
        )
        writer.end_with()

    # NOTE: There is a lot listed on the documentation, we've only implemented what we needed so far.
    @staticmethod
    def Boundaries(
        writer: VbaWriter,
        apply_in_all_directions: bool,
        x_boundaries: tuple[str, str] | None = None,
        y_boundaries: tuple[str, str] | None = None,
        z_boundaries: tuple[str, str] | None = None,
        boundary_type: str | None = None,
    ) -> None:
        """Set boundary conditions for the bounding box. If `apply_in_all_directions` is set to `True` all directions use the
        conditions set by `boundary_type`. We can set different conditions for the minimum and maximum in each Cartesian direction.
        The possible boundary type options are listed in the Table below:

        | Boundary Type | Description |
        |---------------|-------------|
        | electric | Tangential component of the electric field is zero. |
        | magnetic | Tangential component of the magnetic field is zero. |
        | tangential | All tangential components of all fields are zero. |
        | normal | All normal field components are zero. |
        | open | There is no boundary, only open space. |
        | expanded open | Equivalent to open, but adds a bit of space to the computational domain. |
        | periodic | Periodic boundary condition. |
        | conducting wall | Boundary behaves like a wall of lossy metal material. |
        | unit cell | For unit cell structures. |

        See: https://space.mit.edu/RADIO/CST_online/mergedProjects/VBA_3D/special_vbasolver/special_vbasolver_boundary_object.htm

        :param writer: VBA IO handler
        :type writer: VbaWriter
        :param apply_in_all_directions: Apply boundary condition of `x_boundaries[0]` in all directions.
        :type apply_in_all_directions: bool
        :param x_boundaries: Boundary type of the lower and upper bound in the x-direction, see the Table for the options. Argument
            does not need to be provided if `apply_in_all_directions` is `True`.
        :type x_boundaries: tuple[str,str] | None (default=None)
        :param y_boundaries: Boundary type of the lower and upper bound in the y-direction, see the Table for the options. Argument
            does not need to be provided if `apply_in_all_directions` is `True`.
        :type y_boundaries: tuple[str,str] | None (default=None)
        :param z_boundaries: Boundary type of the lower and upper bound in the z-direction, see the Table for the options. Argument
            does not need to be provided if `apply_in_all_directions` is `True`.
        :type z_boundaries: tuple[str,str] | None (default=None)
        :param boundary_type: Boundary type listed in the Table to use in all directions if `apply_in_all_directions` is set to `True`. Argument only needs to be
            provided in that case.
        :type boundary_type: str | None (default=None)
        """
        writer.start_with(structure="Boundary")
        writer.write(
            f".ApplyInAllDirections {wrap_nonstr_in_double_quotes(value=apply_in_all_directions)}\n"
        )
        if apply_in_all_directions is False:
            if x_boundaries is not None:
                writer.write(f".Xmin {VbaWriter.string_repr(text=x_boundaries[0])}\n")
                writer.write(f".Xmax {VbaWriter.string_repr(text=x_boundaries[1])}\n")
            if y_boundaries is not None:
                writer.write(f".Ymin {VbaWriter.string_repr(text=y_boundaries[0])}\n")
                writer.write(f".Ymax {VbaWriter.string_repr(text=y_boundaries[1])}\n")
            if z_boundaries is not None:
                writer.write(f".Zmin {VbaWriter.string_repr(text=z_boundaries[0])}\n")
                writer.write(f".Zmin {VbaWriter.string_repr(text=z_boundaries[1])}\n")
        else:
            if boundary_type is not None:
                writer.write(f".Xmin {VbaWriter.string_repr(text=boundary_type)}\n")
        writer.end_with()
