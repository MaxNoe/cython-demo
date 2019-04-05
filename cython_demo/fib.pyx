



def fibonacci(int n) -> int:
    cdef unsigned long n0 = 0
    cdef unsigned long n1 = 1
    cdef unsigned long temp
    cdef unsigned long i
    for i in range(n):
        temp = n1
        n1 = n0 + n1
        n0 = temp

    return n1
