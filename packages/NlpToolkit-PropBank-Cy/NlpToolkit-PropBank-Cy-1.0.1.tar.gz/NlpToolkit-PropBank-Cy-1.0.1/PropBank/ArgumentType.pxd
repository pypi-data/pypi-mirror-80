from PropBank.ArgumentTypeEnum cimport ArgumentTypeEnum

cdef class ArgumentType():

    @staticmethod
    cdef ArgumentTypeEnum getArguments(str argumentsType)
    @staticmethod
    cdef str getPropbankType(ArgumentTypeEnum argumentType)