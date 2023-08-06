cdef class Subset(object):
        cdef list set
        cdef int __rangeEnd, elementCount

        cpdef list get(self)
        cpdef bint next(self)
