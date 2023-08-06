cdef class HmmState(object):

    cdef dict emissionProbabilities
    cdef object state

    cpdef object getState(self)
    cpdef double getEmitProb(self, object symbol)