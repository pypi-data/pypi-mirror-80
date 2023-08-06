cdef class CrossValidation(object):

    cpdef list getTrainFold(self, int k):
        pass

    cpdef list getTestFold(self, int k):
        pass