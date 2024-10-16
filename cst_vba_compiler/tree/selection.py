""" Python API for selecting tree items in CST.

author: Aaron Gobeyn
"""

from ..writer import VbaWriter


def SelectTreeItem(writer: VbaWriter, tree_path: str) -> None:
    """Select item from the CST data tree, the `tree_path` corresponds to the
    path within CST, for example '2D/3D Results\\E-field\\e'.

    :param writer: VBA IO handler
    :type writer: VbaWriter
    :param tree_path: Path within the CST tree to the desired item to select.
    :type tree_path: str
    """
    writer.write(f"SelectTreeItem {VbaWriter.string_repr(text=tree_path)}\n")
