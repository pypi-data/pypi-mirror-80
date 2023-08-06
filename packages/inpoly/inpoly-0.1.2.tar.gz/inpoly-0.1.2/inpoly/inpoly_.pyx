
import numpy as np
cimport numpy as np
cimport cython

@cython.boundscheck(False)  # deactivate bnds checking
@cython.wraparound(False)   # deactivate -.ve indexing
def _inpoly(np.ndarray[double, ndim=+2] vert,
            np.ndarray[double, ndim=+2] node,
        np.ndarray[np.int32_t, ndim=+2] edge,
        const double ftol, const double lbar):
    """
    _INPOLY: the local cython version of the crossing-number
    test. Loop over edges; do a binary-search for the first
    vertex that intersects with the edge y-range; crossing-
    number comparisons; break when the local y-range is met.

    Updated: 26 September, 2020

    Authors: Darren Engwirda, Keith Roberts

    """
    cdef size_t epos, jpos, inod, jnod, jvrt
    cdef double feps, veps
    cdef double xone, xtwo, xmin, xmax, xdel
    cdef double yone, ytwo, ymax, ydel
    cdef double xpos, ypos, mul1, mul2

    feps = ftol * (lbar ** +2)          # local bnds reltol
    veps = ftol * (lbar ** +1)

    cdef size_t vnum = vert.shape[0]
    cdef size_t enum = edge.shape[0]

    cdef np.ndarray[np.int8_t] stat = np.full(
        vnum, +0, dtype=np.int8)

    cdef np.ndarray[np.int8_t] bnds = np.full(
        vnum, +0, dtype=np.int8)

    cdef np.int8_t *sptr = &stat[+0]    # ptr to contiguous
    cdef np.int8_t *bptr = &bnds[+0]

#----------------------------------- compute y-range overlap
    cdef np.ndarray[Py_ssize_t] ivec = \
        np.argsort(vert[:, 1], kind = "quicksort")

    YMIN = node[edge[:, 0], 1] - veps

    cdef np.ndarray[Py_ssize_t] head = \
        np.searchsorted(
            vert[:, 1], YMIN, "left", sorter=ivec)

    cdef const Py_ssize_t *iptr = &ivec[+0]
    cdef const Py_ssize_t *hptr = &head[+0]

#----------------------------------- loop over polygon edges
    for epos in range(enum):

        inod = edge[epos, 0]            # unpack *this edge
        jnod = edge[epos, 1]

        xone = node[inod, 0]
        xtwo = node[jnod, 0]
        yone = node[inod, 1]
        ytwo = node[jnod, 1]

        xmin = min(xone, xtwo)          # compute edge bbox
        xmax = max(xone, xtwo)

        xmax = xmax + veps
        ymax = ytwo + veps

        xdel = xtwo - xone
        ydel = ytwo - yone

    #------------------------------- calc. edge-intersection
        for jpos in range(hptr[epos], vnum):

            jvrt = iptr[jpos]

            if bptr[jvrt]: continue

            xpos = vert[jvrt, 0]
            ypos = vert[jvrt, 1]

            if ypos >= ymax: break      # due to the y-sort

            if xpos >= xmin:
                if xpos <= xmax:
                #------------------- compute crossing number
                    mul1 = ydel * (xpos - xone)
                    mul2 = xdel * (ypos - yone)

                    if feps >= abs(mul2 - mul1):
                #------------------- BNDS -- approx. on edge
                        bptr[jvrt] = 1
                        sptr[jvrt] = 1

                    elif (ypos == yone) and (xpos == xone):
                #------------------- BNDS -- match about ONE
                        bptr[jvrt] = 1
                        sptr[jvrt] = 1

                    elif (ypos == ytwo) and (xpos == xtwo):
                #------------------- BNDS -- match about TWO
                        bptr[jvrt] = 1
                        sptr[jvrt] = 1

                    elif (mul1 <= mul2) and (ypos >= yone) \
                            and (ypos < ytwo):
                #------------------- advance crossing number
                        sptr[jvrt] = 1 - sptr[jvrt]

            elif (ypos >= yone) and (ypos < ytwo):
            #----------------------- advance crossing number
                sptr[jvrt] = 1 - sptr[jvrt]

    return stat, bnds
