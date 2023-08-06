cdef class Argument(object):

    cdef str __argumentType
    cdef str __id

    def __init__(self, argument: str):
        """
        A constructor of Argument class which takes argument string which is in the form of argumentType$id
        and parses this string into argumentType and id. If the argument string does not contain '$' then the
        constructor return a NONE type argument.

        PARAMETERS
        ----------
        argument : str
            Argument string containing the argumentType and id
        """
        if "$" in argument:
            self.__argumentType = argument[0:argument.index("$")]
            self.__id = argument[argument.index("$") + 1:]
        else:
            self.__argumentType = "NONE"

    cpdef initWithId(self, str argumentType, str _id):
        """
        Another constructor of Argument class which takes argumentType and id as inputs and initializes corresponding 
        attributes

        PARAMETERS
        ----------
        argumentType : str 
            Type of the argument
        _id : str 
            Id of the argument
        """
        self.__argumentType = argumentType
        self.__id = _id

    cpdef str getArgumentType(self):
        """
        Accessor for argumentType.

        RETURNS
        -------
        str
            argumentType.
        """
        return self.__argumentType

    cpdef str getId(self):
        """
        Accessor for id.

        RETURNS
        -------
        str
            id.
        """
        return self.__id

    def __str__(self) -> str:
        """
        __str__ converts an Argument to a string. If the argumentType is "NONE" returns only "NONE", otherwise
        it returns argument string which is in the form of argumentType$id

        RETURNS
        -------
        str
            string form of argument
        """
        if self.__argumentType == "NONE":
            return self.__argumentType
        else:
            return self.__argumentType + "$" + self.__id
