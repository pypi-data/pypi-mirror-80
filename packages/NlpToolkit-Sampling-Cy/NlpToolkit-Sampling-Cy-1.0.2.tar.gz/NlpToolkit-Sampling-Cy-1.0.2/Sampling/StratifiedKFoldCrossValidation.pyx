from Sampling.KFoldCrossValidation cimport KFoldCrossValidation
import random


cdef class StratifiedKFoldCrossValidation(KFoldCrossValidation):

    cdef list __instanceLists
    cdef list _N

    def __init__(self, instanceLists: list, K: int, seed: int):
        """
        A constructor of StratifiedKFoldCrossValidation class which takes as set of class samples as an array of array of
        instances, a K (K in K-fold cross-validation) and a seed number, then shuffles each class sample using the
        seed number.

        PARAMETERS
        ----------
        instanceLists : list
            Original class samples. Each element of the this array is a sample only from one class.
        K : int
            K in K-fold cross-validation
        seed : int
            Random number to create K-fold sample(s)
        """
        cdef int i
        self.__instanceLists = instanceLists
        self._N = []
        for i in range(len(instanceLists)):
            random.seed(seed)
            random.shuffle(instanceLists[i])
            self._N.append(len(instanceLists[i]))
        self.K = K

    cpdef list getTrainFold(self, int k):
        """
        getTrainFold returns the k'th train fold in K-fold stratified cross-validation.

        PARAMETERS
        ----------
        k : int
            index for the k'th train fold of the K-fold stratified cross-validation

        RETURNS
        -------
        list
            Produced training sample
        """
        cdef int i, j
        cdef list trainFold = []
        for i in range(len(self._N)):
            for j in range((k * self._N[i]) // self.K):
                trainFold.append(self.__instanceLists[i][j])
            for j in range(((k + 1) * self._N[i]) // self.K, self._N[i]):
                trainFold.append(self.__instanceLists[i][j])
        return trainFold

    cpdef list getTestFold(self, int k):
        """
        getTestFold returns the k'th test fold in K-fold stratified cross-validation.

        PARAMETERS
        ----------
        k : int
            index for the k'th test fold of the K-fold stratified cross-validation

        RETURNS
        -------
        list
            Produced testing sample
        """
        cdef int i, j
        cdef list testFold = []
        for i in range(len(self._N)):
            for j in range((k * self._N[i]) // self.K, ((k + 1) * self._N[i]) // self.K):
                testFold.append(self.__instanceLists[i][j])
        return testFold
