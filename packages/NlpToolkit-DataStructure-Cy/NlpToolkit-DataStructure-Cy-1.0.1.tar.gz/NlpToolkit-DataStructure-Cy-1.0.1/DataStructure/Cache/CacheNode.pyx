cdef class CacheNode(object):

    def __init__(self, key: object, data: object):
        """
        A constructor of CacheNode class which takes a key and a data as inputs and initializes private fields with
        these inputs.

        PARAMETERS
        ----------
        key : object
            K type input for representing keys.
        data : object
            T type input values represented by keys.
        """
        self.__key = key
        self.__data = data
        self.__previous = None
        self.__next = None

    cpdef object getData(self):
        """
        Getter for data value.

        RETURNS
        -------
        object
            data value.
        """
        return self.__data

    cpdef object getKey(self):
        """
        Getter for key value.

        RETURNS
        -------
        object
            key value.
        """
        return self.__key

    cpdef CacheNode getPrevious(self):
        """
        Getter for the previous CacheNode.

        RETURNS
        -------
        CacheNode
            previous CacheNode.
        """
        return self.__previous

    cpdef CacheNode getNext(self):
        """
        Getter for the next CacheNode.

        RETURNS
        -------
        CacheNode
            next CacheNode.
        """
        return self.__next

    cpdef setPrevious(self, CacheNode previous):
        """
        Setter for the previous CacheNode.

        PARAMETERS
        ----------
        previous : CacheNode
            previous CacheNode.
        """
        self.__previous = previous

    cpdef setNext(self, CacheNode next):
        """
        Setter for the next CacheNode.

        PARAMETERS
        ----------
        next : CacheNode
            next CacheNode.
        """
        self.__next = next
