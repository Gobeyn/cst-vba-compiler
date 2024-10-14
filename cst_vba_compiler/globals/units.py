""" Python API for setting units in CST.

author: Aaron Gobeyn
"""

from ..writer import VbaWriter


def Units(
    writer: VbaWriter,
    length: str = "mm",
    time: str = "ns",
    frequency: str = "GHz",
    temperature: str = "celsius",
) -> None:
    """Set the units which should be used to measure quantities in. Four need to be specified, namely the unit of length,
    time, frequency and temperature.

    :param writer: VBA IO handler
    :type writer: VbaWriter
    :param length: Unit of length, the options are:
        | Setting | Meaning |
        |---------|---------|
        | m | Meter |
        | cm | Centimeter |
        | mm | Millimeter |
        | um | Micrometer |
        | nm | Nanometer |
        | ft | Feet |
        | in | Inch |
        | mil | A thousandth of an Inch |
    :type length: str (default="mm")
    :param time: Unit of time, the options are:
        | Setting | Meaning |
        |---------|---------|
        | fs | Femptosecond (1e-15 s) |
        | ps | Picosecond (1e-12 s) |
        | ns | Nanosecond (1e-9 s) |
        | us | Microsecond (1e-6 s) |
        | ms | Millisecond (1e-3 s) |
        | s | Second (1 s) |
    :type time: str (default="ns")
    :param frequency: Unit of frequency, the options are:
        | Setting | Meaning |
        |---------|---------|
        | Hz | Hertz (1 Hz) |
        | kHz | Kilohertz (1e3 Hz) |
        | MHz | Megahertz (1e6 Hz) |
        | GHz | Gigahertz (1e9 Hz) |
        | THz | Terrahertz (1e12 Hz) |
        | PHz | Petahertz (1e15 Hz) |
    :type frequency: str (default="GHz")
    :param temperature: Unit of temperature, the options are "celsius", "kelvin" and "fahrenheit".
    :type temperature: str (default="celsius")
    """
    assert length in [
        "m",
        "cm",
        "mm",
        "um",
        "nm",
        "ft",
        "in",
        "mil",
    ], "Provided unit of length is not supported."
    assert time in [
        "fs",
        "ps",
        "ns",
        "us",
        "ms",
        "s",
    ], "Provided unit of time is not supported."
    assert frequency in [
        "Hz",
        "kHz",
        "MHz",
        "GHz",
        "THz",
        "PHz",
    ], "Provided unit of frequency is not supported."
    assert temperature in [
        "celsius",
        "kelvin",
        "fahrenheit",
    ], "Provided unit of temperature is not supported."

    writer.start_with(structure="Units")
    writer.write(f".Geometry {VbaWriter.string_repr(text=length)}\n")
    writer.write(f".Time {VbaWriter.string_repr(text=time)}\n")
    writer.write(f".Frequency {VbaWriter.string_repr(text=frequency)}\n")
    writer.write(f".TemperatureUnit {VbaWriter.string_repr(text=temperature)}\n")
    writer.end_with()
