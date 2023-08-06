cdef class FramesetArgument(object):

    cdef str __argumentType,__definition, __function

    cpdef str getArgumentType(self)
    cpdef str getDefinition(self)
    cpdef str getFunction(self)
    cpdef setDefinition(self, str definition)
    cpdef setFunction(self, str function)