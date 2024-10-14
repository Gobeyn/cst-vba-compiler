""" Python interface for CST methods to run eigenmode solver simulations.

author: Aaron Gobeyn
"""

from ..utils import wrap_nonstr_in_double_quotes
from ..writer import VbaWriter


# NOTE: We have not implemented all of the possible options.
def EigenmodeSolver(
    writer: VbaWriter,
    number_of_modes: int,
    mesh_type: str,
    auto_hex_mesh: bool = False,
    auto_tetra_mesh: bool = False,
) -> None:
    """Start the Eigenmode Solver with the given settings. Some settings, such as the frequency range, need to be set with `SolverSettings`,
    see solver.general.SolverSettings.

    :param writer: VBA IO handler
    :type writer: VbaWriter
    :param number_of_modes: Amount of modes to compute within the defined frequency range.
    :type number_of_modes: int
    :param mesh_type: Supports hexahedral and tetrahedral meshes, specify which one. The possible values are "Hexahedral Mesh" or "Tetrahedral Mesh".
    :type mesh_type: str
    :param auto_hex_mesh: Enable automatic hexahedral mesh adaptation.
    :type auto_hex_mesh: bool (default=False)
    :param auto_tetra_mesh: Enable automatic tetrahedral mesh adaptation.
    :type auto_tetra_mesh: bool (default=False)
    """
    assert mesh_type in [
        "Hexahedral Mesh",
        "Tetrahedral Mesh",
    ], "Provided mesh type is not supported."
    writer.start_with(structure="EigenmodeSolver")
    writer.write(".Reset\n")
    writer.write(f".SetMeshType {VbaWriter.string_repr(text=mesh_type)}\n")
    if mesh_type == "Hexahedral Mesh":
        writer.write(
            f".SetMeshAdaptationHex {wrap_nonstr_in_double_quotes(value=auto_hex_mesh)}\n"
        )
    else:
        writer.write(
            f".SetMeshAdaptationTet {wrap_nonstr_in_double_quotes(value=auto_tetra_mesh)}\n"
        )
    writer.write(
        f".SetNumberOfModes {wrap_nonstr_in_double_quotes(value=number_of_modes)}\n"
    )
    writer.write(".Start\n")
    writer.end_with()
