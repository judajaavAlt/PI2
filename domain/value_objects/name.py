class Name:
    def __validate_name(self, name):
        if not isinstance(name, str):
            error_msg = f"Name must be a string, got {type(name).__name__}"
            raise TypeError(error_msg)

        max_char = 50
        if len(name) > max_char:
            error_msg = f"Name must be {max_char} characters long at most"
            error_msg += f", got {len(name)} characters long name"
            raise TypeError(error_msg)

    def __init__(self, name: str):
        self.__validate_name(name)
        self.__name = name

    @property
    def value(self):
        return self.__name

    def __str__(self):
        return self.__name

    def __repr__(self):
        return f"Name({repr(self.__name)})"

    def __eq__(self, other):
        if isinstance(other, Name):
            return self.__name == other.__name
        if isinstance(other, str):
            return self.__name == other
        return False

    def __hash__(self):
        return hash(self.__name)
