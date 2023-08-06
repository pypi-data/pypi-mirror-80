from Math.Matrix cimport Matrix


cdef class Hmm(object):

    cdef Matrix transitionProbabilities
    cdef dict stateIndexes
    cdef list states
    cdef int stateCount

    cpdef dict calculateEmissionProbabilities(self, object state, list observations, list emittedSymbols)
    cpdef double safeLog(self, double x)
