cdef class CacheNode(object):

    cdef object __key, __data
    cdef CacheNode __previous, __next

    cpdef object getData(self)
    cpdef object getKey(self)
    cpdef CacheNode getPrevious(self)
    cpdef CacheNode getNext(self)
    cpdef setPrevious(self, CacheNode previous)
    cpdef setNext(self, CacheNode next)