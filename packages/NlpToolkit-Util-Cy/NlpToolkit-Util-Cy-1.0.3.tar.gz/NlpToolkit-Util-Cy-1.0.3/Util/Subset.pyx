cdef class Subset(object):

    def __init__(self, rangeStart: int, rangeEnd: int, elementCount: int):
        """
        The constructor of Subset class which takes 3 integer inputs; rangeStart, rangeEnd, and elementCount.
        It initializes variables rangeEnd and elementCount with given inputs, creates 2 arrays; set and multiset with
        the size of given elementCount and multisetCount, which is derived from elementCount, respectively. Then, it
        assigns rangeStart+i to each ith element of set.

        Parameters
        ----------
        rangeStart : int
            input defining start range.
        rangeEnd : int
            input defining ending range.
        elementCount : int
            input element count.
        """
        cdef int i
        self.__rangeEnd = rangeEnd
        self.elementCount = elementCount
        self.set = []
        for i in range(elementCount):
            self.set.append(rangeStart + i)

    cpdef list get(self):
        """
        Getter for the set list

        Returns
        ----------
        list
            the set list
        """
        return self.set

    cpdef bint next(self):
        """
        The next method generates the next subset.

        Returns
        ----------
        boolean
            true if next subset generation is possible, false otherwise.
        """
        cdef int i, j
        for i in range(self.elementCount - 1, -1, -1):
            self.set[i] = self.set[i] + 1
            if self.set[i] <= self.__rangeEnd - self.elementCount + i + 1:
                break
        else:
            return False
        for j in range(i + 1, self.elementCount):
            self.set[j] = self.set[j - 1] + 1
        return True
