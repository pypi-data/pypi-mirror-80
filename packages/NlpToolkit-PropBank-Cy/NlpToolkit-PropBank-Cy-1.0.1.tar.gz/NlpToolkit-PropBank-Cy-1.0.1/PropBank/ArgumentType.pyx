cdef class ArgumentType():

    @staticmethod
    cdef ArgumentTypeEnum getArguments(str argumentsType):
        """
        The getArguments method takes an argumentsType string and returns the ArgumentType form of it.

        PARAMETERS
        ----------
        argumentsType : str
            Type of the argument in string form

        RETURNS
        -------
        ArgumentType
            Type of the argument in ArgumentType form
        """
        for argumentType in ArgumentTypeEnum:
            if argumentsType == argumentType.name:
                return argumentType
        return ArgumentType.NONE

    @staticmethod
    cdef str getPropbankType(ArgumentTypeEnum argumentType):
        """
        The getPropbankType method takes an argumentType in ArgumentType form and returns the string form of it.

        PARAMETERS
        ----------
        argumentType : ArgumentType
            Type of the argument in {@link ArgumentType} form

        RETURNS
        -------
        str
            Type of the argument in string form
        """
        if argumentType is None:
            return "NONE"
        return argumentType
