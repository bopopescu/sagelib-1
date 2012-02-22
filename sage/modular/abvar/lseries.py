"""
`L`-series of modular abelian varieties

At the moment very little functionality is implemented -- this is mostly a
placeholder for future planned work. 

AUTHOR:

- William Stein (2007-03)

TESTS::

    sage: L = J0(37)[0].padic_lseries(5)
    sage: loads(dumps(L)) == L
    True
    sage: L = J0(37)[0].lseries()
    sage: loads(dumps(L)) == L
    True
"""

###########################################################################
#       Copyright (C) 2007 William Stein <wstein@gmail.com>               #
#  Distributed under the terms of the GNU General Public License (GPL)    #
#                  http://www.gnu.org/licenses/                           #
###########################################################################

from sage.structure.sage_object import SageObject
from sage.rings.all import Integer

class Lseries(SageObject):
    """
    Base class for `L`-series attached to modular abelian varieties.
    """
    def __init__(self, abvar):
        """
        Called when creating an L-series.

        INPUT:

        - ``abvar`` -- a modular abelian variety

        EXAMPLES::

            sage: J0(11).lseries()
            Complex L-series attached to Abelian variety J0(11) of dimension 1
        """
        self.__abvar = abvar
        
    def abelian_variety(self):
        """
        Return the abelian variety that this `L`-series is attached to.

        OUTPUT:
            a modular abelian variety

        EXAMPLES::

            sage: J0(11).padic_lseries(7).abelian_variety()
            Abelian variety J0(11) of dimension 1
        """
        return self.__abvar

class Lseries_complex(Lseries):
    """
    A complex `L`-series attached to a modular abelian variety.

    EXAMPLES::

        sage: A = J0(37)
        sage: A.lseries()
        Complex L-series attached to Abelian variety J0(37) of dimension 2
    """
    def __call__(self, s):
        """
        Evaluate this complex `L`-series at `s`.

        INPUT:
        
        - ``s`` -- complex number

        OUTPUT:
            a complex number L(A, s).

        EXAMPLES:
        This is not yet implemented::

            sage: L = J0(37).lseries()
            sage: L(2)
            Traceback (most recent call last):
            ...
            NotImplementedError
        """
        raise NotImplementedError
    
    def __cmp__(self, other):
        """
        Compare this complex `L`-series to another one.

        INPUT:
        
        - ``other`` -- object

        OUTPUT:
           -1, 0, or 1

        EXAMPLES::

            sage: L = J0(37)[0].lseries(); M = J0(37)[1].lseries()
            sage: cmp(L,M)
            -1
            sage: cmp(L,L)
            0
            sage: cmp(M,L)
            1
        """
        if not isinstance(other, Lseries_complex):
            return cmp(type(self), type(other))
        return cmp(self.abelian_variety(), other.abelian_variety())


    def _repr_(self):
        """
        String representation of `L`-series.

        OUTPUT:
            a string

        EXAMPLES::

            sage: L = J0(37).lseries()
            sage: L._repr_()
            'Complex L-series attached to Abelian variety J0(37) of dimension 2'
        """
        return "Complex L-series attached to %s"%self.abelian_variety()

    def rational_part(self):
        """
        Return the rational part of this `L`-function at the central critical
        value 1.

        NOTE: This is not yet implemented.

        EXAMPLES::

            sage: J0(37).lseries().rational_part()
            Traceback (most recent call last):
            ...
            NotImplementedError
        """
        raise NotImplementedError        


