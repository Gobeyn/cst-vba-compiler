""" Python interface for general project managing methods in CST
"""

from ..utils import wrap_nonstr_in_double_quotes
from ..writer import VbaWriter


class General(object):
    @staticmethod
    def DisableInteraction(writer: VbaWriter, disable: bool = False) -> None:
        """Disable user interaction for the duration of the macro runtime if
        `disable` is `True`. After macro execution, `disable` is automatically
        set to `False`.

        See: https://space.mit.edu/RADIO/CST_online/mergedProjects/VBA_3D/common_vbaapp/common_vbaappapplication_object.htm

        :param writer: VBA IO handler
        :type writer: VbaWriter
        :param disable: Disable user interaction of `True`.
        :type disable: bool (default=False)
        """
        writer.write(f"SetLock {wrap_nonstr_in_double_quotes(value=disable)}\n")
