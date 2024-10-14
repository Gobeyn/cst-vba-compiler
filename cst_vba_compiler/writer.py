"""
Class that handles the IO with the generated VBA script.

author: Aaron Gobeyn
date: 01-10-2024
"""

import os
from io import TextIOWrapper


class VbaWriter(object):
    """This is a class which handles all the IO for the generate VBA script.

    :param filehandle: Handle of the file we want to write to. This assumed to be
        the return value of the `open` method.
    :type filehandle: TextIOWrapper
    """

    def __init__(self, filehandle: TextIOWrapper):
        """Constructor method"""
        # Handle to the VBA file to which we can write.
        self.__filehandle = filehandle
        # Extract file path from handle
        self.__filepath = self.__filehandle.name
        # Store the current indent depth, e.g. the amount of tabs to prepend.
        self.__indent_depth: int = 0
        # Write boilerplate lines in the VBA script that always need to be there.
        self.__write_essentials()
        # Initialise an empty dictionary of parameters, the dictionary grows when we add parameters
        self.__parameters: dict = dict()
        # Store what the current scope is, i.e. are we currently in a Function? If so which one? Are
        # we in the Main entry point? etc.
        self.__current_scope: str | None = None

    def write(self, text: str) -> None:
        """API for writing with `text` to the private
        file handle of the class. This can also be used to
        write VBA script manually and insert it into the file
        in case certain aspects are not supported.

        :param text: Text to write
        :type text: str
        """
        try:
            self.__filehandle.write("\t" * self.__indent_depth + text)
        except:
            raise IOError(f"Unable to write contents to {self.__filepath}.")

    def __write_essentials(self) -> None:
        """Write contents to the VBA script that will always need to be there,
        namely:
        - Option Explicit
        """
        self.write(text="Option Explicit\n")

    @staticmethod
    def create(filepath: str) -> None:
        """Given a file path, create the file and
        all the directories in between if they do not exist.

        :param filepath: Path to the VBA file we want to create.
        :type filepath: str
        """
        # Get the directory path from the file path
        directory = os.path.dirname(filepath)

        # Create the directories if they do not exist
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        # Create the file only if it does not exist
        if not os.path.exists(filepath):
            with open(filepath, "a"):
                pass  # No need to write anything

    @staticmethod
    def string_repr(text: str) -> str:
        """Given a string, return the representation of that
        string where the single quotes are replaced with double quotes
        as required by VBA.

        :param text: Text to convert into a VBA String.
        :type text: str
        """
        text_repr: str = repr(text)
        text_repr = '"' + text_repr.strip("'") + '"'
        return text_repr

    @staticmethod
    def wrap_double_quotes(value) -> str:
        """Wrap the `repr` of `value` in double quotes.

        :param value: Something that has the `__repr__` dunder method
            which we want to convert into a string, wrapped with double quotes.
        :type value: Any that implements `__repr__`
        """
        return '"' + repr(value) + '"'

    def start_main(self) -> None:
        """Write the line 'Sub Main ()' which functions as the entry point for a VBA script. Update the
        current scope."""
        self.write(text="Sub Main ()\n")
        self.__current_scope = "Main"
        self.__indent_depth += 1

    def end_main(self) -> None:
        """Write the line 'End Sub' to close the VBA script entry point. Everything written between
        the call of `start_main` method and this method is contained within the main loop of the VBA script.
        The scope is set back to `None`
        """
        self.write(text="Save\n")
        self.__indent_depth -= 1
        self.write(text="End Sub\n")
        self.__current_scope = None

    def start_with(self, structure: str) -> None:
        """Start a `With` block for `structure`.

        :param structure: Name of the structure
        :type structure: str
        """
        self.write(text=f"With {structure}\n")
        self.__indent_depth += 1

    def end_with(self) -> None:
        """End a `With` block"""
        self.__indent_depth -= 1
        self.write(text="End With\n")

    def list_parameters(self):
        """Method for printing the defined parameters."""
        print(self.__parameters)

    def initialise_parameter(self, name: str, declare_type: str | type) -> None:
        """Initialise a parameter, e.g. declare in VBA that there is a parameter
        called `name` that is of type `declare_type` without assigning it a value. This
        parameter is added to the parameter dictionary with value `None`. A value can be
        assigned later, however, a value can only be assigned if the `name` is present in the
        dictionary. The scope of the variable is also stored.
        See: https://learn.microsoft.com/en-us/office/vba/language/reference/user-interface-help/data-type-summary
        for a list of accepted VBA types.

        For convenience, we also allow the possibility of inferring from Python types. If `declare_type` is not a string,
        but a Python type, then the inferences as listed in the `add_parameter` method are performed.

        :param name: Name of the parameter
        :type name: str
        :param declare_type: String that encodes the literal VBA type, or Python type that is inferred into a VBA type.
        :type declare_type: str | type
        """

        if isinstance(declare_type, str):
            vba_type: str = declare_type
        else:
            match declare_type.__name__:
                case "bool":
                    vba_type: str = "Boolean"
                case "float":
                    vba_type: str = "Double"
                case "int":
                    vba_type: str = "Integer"
                case "str":
                    vba_type: str = "String"
                case _:
                    raise ValueError(
                        f"The type {declare_type.__name__} does not have supported VBA type conversion."
                    )

        self.__parameters[(name, self.__current_scope)] = {
            "value": None,
            "type": vba_type,
        }
        self.write(f"Dim {name} As {vba_type}\n")

    def assign_parameter(self, name: str, value) -> None:
        """Assign a value to a parameter whose type has already been defined.
        We will assume that if the user specified the type beforehand, they assign
        a value of the correct type so there will be no type checking in this function.
        The assumed variable scope is the current scope. Note that this method uses
        the `repr` method on the value, so custom data classes that implement the
        `__repr__` dunder method can also be used.

        :param name: Name of the parameter
        :type name: str
        :param value: Value of the parameter, make sure this corresponds with
            the type you've set for this parameter beforehand.
        :type value: Any
        """
        # Check if the parameter has been initialised
        if (key := (name, self.__current_scope)) in self.__parameters:
            self.__parameters[key]["value"] = value
            val_vba_content: str = repr(value)
            if isinstance(value, str):
                val_vba_content = VbaWriter.string_repr(text=value)
            self.write(f"{name} = {val_vba_content}\n")
        else:
            raise ValueError(
                f"Parameter {name} in scope {self.__current_scope} did not receive type initialisation."
            )

    def add_parameter(
        self,
        name: str,
        value,
        declare_type: str | None = None,
    ) -> None:
        """Add a parameter called `name` with contents `value` to the parameter dictionary, and
        write the corresponding line in the VBA file.
        The type that needs to be specified in VBA is automatically inferred from the
        type in Python, however one can set it manually with `declare_type` as well, though this is
        not recommended due to some subtleties when writing the correct line in the VBA file. The scope
        in which the parameter is defined is also stored.

        Here is a list of the supported inferred VBA types from the Python types
            | Python type | VBA type |
            |_____________|__________
            | bool | Boolean |
            | int | Integer |
            | float | Double |
            | str | String |

        Note that the VBA Integer type is 16-bit, if the value of the Python integer
        does not fit into 16-bits an exception will be thrown.

        Internally, the method uses the `repr` function on the values, one can create their own data class
        with a `__repr__` dunder method that corresponds to the VBA expectations in case the required type
        is not implemented.

        :param name: Name of the parameter
        :type name: str
        :param value: Value of the parameter
        :type value: Any
        :param declare_type: Manually set the VBA type of the value instead of inferring it.
        :type declare_type: str | None (default=None)
        """
        # Check if we need to infer the type
        if declare_type is None:
            match value:
                case bool():
                    val_type: str = "Boolean"
                case float():
                    val_type: str = "Double"
                case int():
                    # Check if the value does not exceed 16-bit range
                    if value >= -(2**15) and value <= 2**15 - 1:
                        val_type: str = "Integer"
                    else:
                        raise ValueError(
                            f"Size of value: {value} cannot be represented by a 16-bit integer, as required by VBA."
                        )
                case str():
                    val_type: str = "String"
                case _:
                    raise ValueError(
                        f"Type of the `value` parameter: {type(value)}, is not supported for VBA type conversion."
                    )
        else:
            val_type: str = declare_type
            # Note that this does not work for all types, see Boolean and String for example.

        # Add entry to the parameter list.
        self.__parameters[(name, self.__current_scope)] = {
            "value": value,
            "type": val_type,
        }

        val_vba_content: str = repr(value)
        if isinstance(value, str):
            val_vba_content = VbaWriter.string_repr(text=value)

        # Write line to the VBA scripts
        self.write(text=f"Dim {name} As {val_type}\n")
        self.write(text=f"{name} = {val_vba_content}\n")
