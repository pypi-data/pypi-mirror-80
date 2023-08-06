from PropBank.ArgumentTypeEnum cimport ArgumentTypeEnum


cdef class Role(object):

    cdef str __description, __f, __n

    cpdef str getDescription(self)
    cpdef str getF(self)
    cpdef str getN(self)
    cpdef ArgumentTypeEnum getArgumentType(self)