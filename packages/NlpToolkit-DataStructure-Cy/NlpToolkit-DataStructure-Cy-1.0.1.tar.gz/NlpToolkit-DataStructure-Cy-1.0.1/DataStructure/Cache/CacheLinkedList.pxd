from DataStructure.Cache.CacheNode cimport CacheNode

cdef class CacheLinkedList(object):

    cdef CacheNode _head, _tail

    cpdef CacheNode remove(self)
    cpdef removeGiven(self, CacheNode cacheNode)
    cpdef add(self, CacheNode cacheNode)
