################################################################################
#       Copyright (C) 2010-2012 William Stein <wstein@gmail.com>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#
#    This code is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    General Public License for more details.
#
#  The full text of the GPL is available at:
#
#                  http://www.gnu.org/licenses/
################################################################################

cdef enum:
    MAX_CONTFRAC = 100
    MAX_DEG = 10000

from sage.modular.modsym.p1list cimport P1List

cdef class ModularSymbolMap:
    cdef long d, N
    cdef public long denom
    cdef long* X  # coefficients of linear map from P^1 to Q^d.
    cdef public object C
    cdef P1List P1
    cdef int evaluate(self, long v[MAX_DEG], long a, long b) except -1
