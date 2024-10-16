""" Python API for data exports from CST

author: Aaron Gobeyn
"""

from ..utils import wrap_nonstr_in_double_quotes
from ..writer import VbaWriter


# NOTE: We have not implemented all the available options yet!
def ASCIIExport(
    writer: VbaWriter,
    export_path: str,
    data_mode: str | None = None,
    file_type: str = "ascii",
    step: int | float | None = None,
    step_directional: list[int] | list[float] | None = None,
    subvolume: list[tuple[float, float]] | None = None,
    use_subvolume: bool = False,
    use_meter: bool = False,
    csv_separator: str | None = None,
) -> None:
    """
    Export a selected tree item as ASCII, CSV or HDF5 data.
    See https://space.mit.edu/RADIO/CST_online/mergedProjects/VBA_3D/common_vbaimpexp/asciiexport_object.htm

    :param writer: VBA IO handler
    :type writer: VbaWriter
    :param export_path: Path to export the data to, take care with the file extension.
    :type export_path: str
    :param data_mode: Mode to use when sampling the data, this can be either 'FixedNumber' which will export
        a fixed number of samples, or "FixedWidth" which fixes the step with of the sample. To set either
        the number or width, see the `step` and `step_directional` parameters. Note that this setting is
        only available when exporting 2D/3D field results.
    :type data_mode: str | None (default=None)
    :param file_type: Format of the exported data, options are "ascii", "csv" and "hdf5".
    :type file_type: str (default="ascii")
    :param step: Depending on the `data_mode` setting, it is either interpreted as the number of samples
        in each direction, or the width in each direction. Note that this setting is only available when
        exporting 2D/3D field results.
    :type step: int | float | None (default=None)
    :param step_directional: Same as step, but each Cartesian direction is specified separately in a list ordered
        as [x,y,z].
    :type step_directional: list[int] | list[float] | None (default=None)
    :param subvolume: Defines volume to evaluate results as bounds in the Cartesian directions, e.g.
        $[(x_{min}, x_{max}), (y_{min}, y_{max}), (z_{min}, z_{max})]$. Note that this is only available for
        2D/3D field results.
    :type subvolume: list[tuple[float, float]] | None (default=None)
    :param use_subvolume: If set to `True` the sub-volume defined in `subvolume` is used instead of the entire structure
        volume.
    :type use_subvolume: bool (default=False)
    :param use_meter: If `True`, coordinates are exported in meter, otherwise the project units are used. Note that this is
        only available for 2D/3D exports.
    :type use_meter: bool (default=False)
    :param csv_separator: Separator for csv file formats, this is only available for 2D/3D exports.
    :type csv_separator: str (default=",")
    """
    if data_mode is not None:
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
    if data_mode is not None:
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
    writer.write(
        f".ExportCoordinatesInMeter {wrap_nonstr_in_double_quotes(value=use_meter)}\n"
    )
    if csv_separator is not None:
        writer.write(f".SetCsvSeparator {VbaWriter.string_repr(text=csv_separator)}\n")
    writer.write(".Execute\n")
    writer.end_with()
