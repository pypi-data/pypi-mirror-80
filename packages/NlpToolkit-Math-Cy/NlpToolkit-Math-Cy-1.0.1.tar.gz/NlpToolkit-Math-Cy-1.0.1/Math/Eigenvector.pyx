from Math.Vector cimport Vector


cdef class Eigenvector(Vector):

    cdef double eigenvalue

    def __init__(self, eigenvalue: double, values: list):
        """
        A constructor of Eigenvector which takes a double eigenValue and an list values as inputs.
        It calls its super class Vector with values list and initializes eigenValue variable with its
        eigenValue input.

        PARAMETERS
        ----------
        eigenvalue : double
            eigenValue double input.
        values : list
            list input.
        """
        super().__init__(values)
        self.eigenvalue = eigenvalue

    cpdef float getEigenvalue(self):
        """
        The eigenValue method which returns the eigenValue variable.

        RETURNS
        -------
        double
            eigenValue variable.
        """
        return self.eigenvalue
