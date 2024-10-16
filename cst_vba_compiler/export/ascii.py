""" Python API for data exports from CST

author: Aaron Gobeyn
"""

from ..utils import wrap_nonstr_in_double_quotes
from ..writer import VbaWriter


# NOTE: We have not implemented all the available options yet!
def ASCIIExport(
    writer: VbaWriter,
    export_path: str,
    data_mode: str,
    file_type: str = "ascii",
    step: int | float | None = None,
    step_directional: list[int] | list[float] | None = None,
    subvolume: list[tuple[int | float, int | float]] | None = None,
    use_subvolume: bool = False,
) -> None:
    """

    See https://space.mit.edu/RADIO/CST_online/mergedProjects/VBA_3D/common_vbaimpexp/asciiexport_object.htm
    """
    assert data_mode in [
        "FixedNumber",
        "FixedWidth",
    ], "Provided data mode is not of the supported options."
    assert file_type in [
        "ascii",
        "csv",
        "hdf5",
    ], "Provided file type is not of the supported options."

    writer.start_with(structure="ASCIIExport")
    writer.write(".Reset\n")
    writer.write(f".FileName {VbaWriter.string_repr(text=export_path)}\n")
    writer.write(f".SetfileType {VbaWriter.string_repr(text=file_type)}\n")
    writer.write(f".Mode {VbaWriter.string_repr(text=data_mode)}\n")
    if step is not None:
        writer.write(f".Step {wrap_nonstr_in_double_quotes(value=step)}\n")
    if step_directional is not None:
        writer.write(
            f".StepX {wrap_nonstr_in_double_quotes(value=step_directional[0])}\n"
        )
        writer.write(
            f".StepY {wrap_nonstr_in_double_quotes(value=step_directional[1])}\n"
        )
        writer.write(
            f".StepZ {wrap_nonstr_in_double_quotes(value=step_directional[2])}\n"
        )
    if subvolume is not None:
        writer.write(
            f".SetSubvolume {wrap_nonstr_in_double_quotes(value=subvolume[0][0])}, {wrap_nonstr_in_double_quotes(value=subvolume[0][1])}, {wrap_nonstr_in_double_quotes(value=subvolume[1][0])}, {wrap_nonstr_in_double_quotes(value=subvolume[1][1])}, {wrap_nonstr_in_double_quotes(value=subvolume[2][0])}, {wrap_nonstr_in_double_quotes(value=subvolume[2][1])}\n"
        )
    writer.write(f".UseSubvolume {wrap_nonstr_in_double_quotes(value=use_subvolume)}\n")

    writer.write(".Execute\n")
    writer.end_with()
