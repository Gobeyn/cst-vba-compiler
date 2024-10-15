""" Python interface for CST methods involved in file handling.

author: Aaron Gobeyn
"""

from ..utils import wrap_nonstr_in_double_quotes
from ..writer import VbaWriter


class FileHandling(object):
    """See http://www.mweda.com/cst/cst2013/mergedProjects/VBA_Help_DS/special_vbacommands/projectobject.htm"""

    @staticmethod
    def FileNew(writer: VbaWriter) -> None:
        """Open a new, unnamed project.

        :param writer: VBA IO handler
        :type writer: VbaWriter
        """
        writer.write("FileNew\n")

    @staticmethod
    def OpenFile(writer: VbaWriter, filepath: str) -> None:
        """Open an existing project stored at `filepath`.

        :param writer: VBA IO handler
        :type writer: VbaWriter
        :param filepath: File path to the existing CST project.
        :type filepath: str
        """
        writer.write(f"OpenFile {VbaWriter.string_repr(text=filepath)}\n")

    @staticmethod
    def Quit(writer: VbaWriter) -> None:
        """Close the CST project without saving.

        :param writer: VBA IO handler
        :type writer: VbaWriter
        """
        writer.write("Quit\n")

    @staticmethod
    def Save(writer: VbaWriter) -> None:
        """Save the CST project.

        :param writer: VBA IO handler
        :type writer: VbaWriter
        """
        writer.write("Save\n")

    @staticmethod
    def SaveAs(writer: VbaWriter, filepath: str, include_results: bool) -> None:
        """Save current state of the project under `filepath`. Results are included if
        `include_results` is set to `True`.

        :param writer: VBA IO handler
        :type writer: VbaWriter
        :param filepath: File path to save CST project to
        :type filepath: str
        :param include_results: Include results in saved project if `True`, or not if `False`
        :type include_results: bool
        """
        writer.write(
            f"SaveAs {VbaWriter.string_repr(text=filepath)}, {wrap_nonstr_in_double_quotes(value=include_results)}\n"
        )
