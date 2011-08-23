"""
Finite Prime Fields

AUTHORS:
     -- William Stein: initial version
     -- Martin Albrecht (2008-01): refactoring

TESTS:
    sage: k = GF(3)
    sage: TestSuite(k).run()
"""

#*****************************************************************************
#       Copyright (C) 2006 William Stein <wstein@gmail.com>
#       Copyright (C) 2008 Martin Albrecht <malb@informatik.uni-bremen.de> 
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
#*****************************************************************************

import sys

from sage.rings.finite_rings.finite_field_base import FiniteField as FiniteField_generic
from sage.structure.parent_gens import normalize_names, ParentWithGens

import sage.rings.finite_rings.integer_mod_ring as integer_mod_ring
import sage.rings.integer as integer
import sage.rings.rational as rational
import sage.rings.finite_rings.integer_mod as integer_mod
import sage.rings.arith as arith


class FiniteField_prime_modn(FiniteField_generic, integer_mod_ring.IntegerModRing_generic):
    def __init__(self, p, name=None):
        """
        Return a new finite field of order $p$ where $p$ is prime.

        INPUT:
            p -- an integer >= 2
            name -- ignored

        EXAMPLES:
            sage: FiniteField(3)
            Finite Field of size 3
            
            sage: FiniteField(next_prime(1000))
            Finite Field of size 1009
        """
        p = integer.Integer(p)
        if not arith.is_prime(p):
            raise ArithmeticError, "p must be prime"
        from sage.categories.finite_fields import FiniteFields
        self.__char = p
        import sage.structure.factorization as factorization
        self._IntegerModRing_generic__factored_order = factorization.Factorization([(p,1)], integer.Integer(1))
        self._kwargs = {}
        integer_mod_ring.IntegerModRing_generic.__init__(self, p, category = FiniteFields())
        FiniteField_generic.__init__(self, self, ('x',), normalize=False)

    def __reduce__(self):
        """
        EXAMPLES::
        
            sage: k = FiniteField(5); type(k)
            <class 'sage.rings.finite_rings.finite_field_prime_modn.FiniteField_prime_modn_with_category'>
            sage: k is loads(dumps(k))
            True
        """
        return self._factory_data[0].reduce_data(self)

    def __cmp__(self, other):
        r"""
        Compare \code{self} with \code{other}. Two finite prime fields
        are considered equal if their characteristic is equal.

        EXAMPLE:
            sage: K = FiniteField(3)
            sage: copy(K) == K
            True
        """
        if not isinstance(other, FiniteField_prime_modn):
            return cmp(type(self), type(other))
#        elif other.__class__ != FiniteField_prime_modn:
#            return -cmp(other, self)
        return cmp(self.__char, other.__char)

    def __richcmp__(left, right, op):
        r"""
        Compare \code{self} with \code{right}.
        
        EXAMPLE::

            sage: k = GF(2)
            sage: j = GF(3)
            sage: k == j
            False
            
            sage: GF(2) == copy(GF(2))
            True
        """
        return left._richcmp_helper(right, op)

    def _is_valid_homomorphism_(self, codomain, im_gens):
        """
        This is called implicitly by the hom constructor.
        
        EXAMPLES:
            sage: k = GF(73^2,'a')
            sage: f = k.modulus()
            sage: r = f.change_ring(k).roots()
            sage: k.hom([r[0][0]]) # indirect doctest
            Ring endomorphism of Finite Field in a of size 73^2
              Defn: a |--> 72*a + 3
        """
        try:
            return im_gens[0] == codomain._coerce_(self.gen(0))
        except TypeError:
            return False

    def _coerce_map_from_(self, S):
        """
        This is called implicitly by arithmetic methods.

        EXAMPLES:
            sage: k = GF(7)
            sage: e = k(6)
            sage: e * 2 # indirect doctest
            5
            sage: 12 % 7
            5
        """
        from sage.rings.integer_ring import ZZ
        from sage.rings.finite_rings.integer_mod_ring import IntegerModRing_generic
        if S is int:
            return integer_mod.Int_to_IntegerMod(self)
        elif S is ZZ:
            return integer_mod.Integer_to_IntegerMod(self)
        elif isinstance(S, IntegerModRing_generic):
            from sage.rings.residue_field import ResidueField_generic
            if S.characteristic() == self.characteristic() and not isinstance(S, ResidueField_generic):
                try:
                    return integer_mod.IntegerMod_to_IntegerMod(S, self)
                except TypeError:
                    pass
        to_ZZ = ZZ.coerce_map_from(S)
        if to_ZZ is not None:
            return integer_mod.Integer_to_IntegerMod(self) * to_ZZ

    def characteristic(self):
        r"""
        Return the characteristic of \code{self}.

        EXAMPLE:
            sage: k = GF(7)
            sage: k.characteristic()
            7
        """
        return self.__char

    def modulus(self):
        """
        Return the minimal polynomial of self, which is always $x - 1$.

        EXAMPLE:
            sage: k = GF(199)
            sage: k.modulus()
            x + 198
        """
        try:
            return self.__modulus
        except AttributeError:
            x = self['x'].gen()
            self.__modulus = x - 1
        return self.__modulus

    def is_prime_field(self):
        """
        Return True

        EXAMPLE:
            sage: k.<a> = GF(3)
            sage: k.is_prime_field()
            True

            sage: k.<a> = GF(3^2)
            sage: k.is_prime_field()
            False
        """
        return True
        
    def polynomial(self, name=None):
        """
        Returns the polynomial \var{name}.

        EXAMPLE:
            sage: k.<a> = GF(3)
            sage: k.polynomial()
            x
        """
        if name is None:
            name = self.variable_name()
        try:
            return self.__polynomial[name]
        except  AttributeError:
            from sage.rings.finite_rings.constructor import FiniteField
            R = FiniteField(self.characteristic())[name]
            f = self[name]([0,1])
            try:
                self.__polynomial[name] = f
            except (KeyError, AttributeError):
                self.__polynomial = {}
                self.__polynomial[name] = f
            return f

    def order(self):
        """
        Return the order of this finite field.

        EXAMPLE:
            sage: k = GF(5)
            sage: k.order()
            5
        """
        return self.__char

    def gen(self, n=0):
        """
        Return generator of this finite field as an extension of its
        prime field. 

        NOTE: If you want a primitive element for this finite field
        instead, use \code{self.multiplicative_generator()}.
        
        EXAMPLES:
            sage: k = GF(13)
            sage: k.gen()
            1
            sage: k.gen(1)
            Traceback (most recent call last):
            ...
            IndexError: only one generator
        """
        if n != 0:
            raise IndexError, "only one generator"
        return self(1)

    def __iter__(self):
        """
        EXAMPLES: 
            sage: list(GF(7))
            [0, 1, 2, 3, 4, 5, 6]
            
        We can even start iterating over something that would be too big
        to actually enumerate:
            sage: K = GF(next_prime(2^256))
            sage: all = iter(K)
            sage: all.next()
            0
            sage: all.next()
            1
            sage: all.next()
            2
        """
        yield self(0)
        i = one = self(1)
        while i:
            yield i
            i += one
        
    def degree(self):
        """
        Returns the degree of the finite field, which is a positive
        integer.

        EXAMPLES:
            sage: FiniteField(3).degree()
            1
        """
        return integer.Integer(1)