""" Python interface to set general settings for solvers in CST.

author: Aaron Gobeyn
"""

from ..utils import wrap_nonstr_in_double_quotes
from ..writer import VbaWriter


class SolverSettings(object):
    @staticmethod
    def FrequencyRange(writer: VbaWriter, frequency_range: tuple[float, float]) -> None:
        """Set the frequency range used for all solvers.

        See: https://space.mit.edu/RADIO/CST_online/mergedProjects/VBA_3D/special_vbasolver/special_vbasolver_solver_object.htm
        :param writer: VBA IO handler
        :type: VbaWritee
        :param frequency_range: Minimal and maximal value of the frequency range to search in. The units of frequency
            can be set in global.units
        :type frequency_range: tuple[float, float]
        """
        writer.write(
            f"Solver.FrequencyRange {wrap_nonstr_in_double_quotes(value=frequency_range[0])}, {wrap_nonstr_in_double_quotes(value=frequency_range[1])}\n"
        )
