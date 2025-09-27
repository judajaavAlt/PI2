class Description:
    def __validate_description(self, description):
        if not isinstance(description, str):
            error_msg = "Description must be a string"
            error_msg += f", got {type(description).__name__}"
            raise TypeError(error_msg)

        max_char = 255
        if len(description) > max_char:
            error_msg = f"Description must be {max_char}"
            error_msg += " characters long at most"
            error_msg += f", got {len(description)} "
            error_msg += "characters long description"
            raise TypeError(error_msg)

    def __init__(self, description: str):
        self.__validate_description(description)
        self.__description = description

    @property
    def value(self):
        return self.__description

    def __str__(self):
        return self.__description

    def __repr__(self):
        return f"Description({repr(self.__description)})"

    def __eq__(self, other):
        if isinstance(other, Description):
            return self.__description == other.__description
        if isinstance(other, str):
            return self.__description == other
        return False

    def __hash__(self):
        return hash(self.__description)
