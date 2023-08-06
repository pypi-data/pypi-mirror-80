cdef class CrossValidation(object):

    cdef int K

    cpdef list getTrainFold(self, int k)
    cpdef list getTestFold(self, int k)