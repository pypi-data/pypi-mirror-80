from PropBank.ArgumentTypeEnum cimport ArgumentTypeEnum


cdef class Frameset(object):

    cdef list __framesetArguments
    cdef str __id

    cpdef bint containsArgument(self, ArgumentTypeEnum argumentType)
    cpdef addArgument(self, str argumentType, str definition, str function=*)
    cpdef deleteArgument(self, str argumentType, str definition)
    cpdef list getFramesetArguments(self)
    cpdef str getId(self)
    cpdef setId(self, str _id)
    cpdef save(self, str fileName)