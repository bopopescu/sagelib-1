"""
Fraction Field of Integral Domains

AUTHORS:

- William Stein (with input from David Joyner, David Kohel, and Joe
  Wetherell)

- Burcin Erocal

EXAMPLES:

Quotienting is a constructor for an element of the
fraction field::

    sage: R.<x> = QQ[]
    sage: (x^2-1)/(x+1)
    x - 1
    sage: parent((x^2-1)/(x+1))
    Fraction Field of Univariate Polynomial Ring in x over Rational Field

The GCD is not taken (since it doesn't converge sometimes) in the
inexact case.

::

    sage: Z.<z> = CC[]
    sage: I = CC.gen()
    sage: (1+I+z)/(z+0.1*I)
    (z + 1.00000000000000 + I)/(z + 0.100000000000000*I)
    sage: (1+I*z)/(z+1.1)
    (I*z + 1.00000000000000)/(z + 1.10000000000000)

TESTS::

    sage: F = FractionField(IntegerRing())
    sage: F == loads(dumps(F))
    True

::

    sage: F = FractionField(PolynomialRing(RationalField(),'x'))
    sage: F == loads(dumps(F))
    True

::

    sage: F = FractionField(PolynomialRing(IntegerRing(),'x'))
    sage: F == loads(dumps(F))
    True

::

    sage: F = FractionField(PolynomialRing(RationalField(),2,'x'))
    sage: F == loads(dumps(F))
    True
"""

#*****************************************************************************
#
#   Sage: System for Algebra and Geometry Experimentation    
#
#       Copyright (C) 2005 William Stein <wstein@gmail.com>
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

import ring
import field
import fraction_field_element
import sage.misc.latex as latex

from sage.structure.parent import Parent
from sage.structure.coerce_maps import CallableConvertMap
from sage.categories.basic import QuotientFields

def FractionField(R, names=None):
    """
    Create the fraction field of the integral domain R.
    
    INPUT:
    
    
    -  ``R`` - an integral domain
    
    -  ``names`` - ignored
    
    
    EXAMPLES: We create some example fraction fields.
    
    ::
    
        sage: FractionField(IntegerRing())
        Rational Field
        sage: FractionField(PolynomialRing(RationalField(),'x'))
        Fraction Field of Univariate Polynomial Ring in x over Rational Field
        sage: FractionField(PolynomialRing(IntegerRing(),'x'))
        Fraction Field of Univariate Polynomial Ring in x over Integer Ring
        sage: FractionField(PolynomialRing(RationalField(),2,'x'))
        Fraction Field of Multivariate Polynomial Ring in x0, x1 over Rational Field
    
    Dividing elements often implicitly creates elements of the fraction
    field.
    
    ::
    
        sage: x = PolynomialRing(RationalField(), 'x').gen()
        sage: f = x/(x+1)
        sage: g = x**3/(x+1)
        sage: f/g
        1/x^2
        sage: g/f
        x^2
    
    The input must be an integral domain.
    
    ::
    
        sage: Frac(Integers(4))
        Traceback (most recent call last):
        ...
        TypeError: R must be an integral domain.
    """
    if not ring.is_Ring(R):
        raise TypeError, "R must be a ring"
    if not R.is_integral_domain():
        raise TypeError, "R must be an integral domain."
    return R.fraction_field()

def is_FractionField(x):
    """
    Tests whether or not x inherits from FractionField_generic.
    
    EXAMPLES::
    
        sage: from sage.rings.fraction_field import is_FractionField
        sage: is_FractionField(Frac(ZZ['x']))
        True
        sage: is_FractionField(QQ)
        False
    """
    return isinstance(x, FractionField_generic)
    
class FractionField_generic(field.Field):
    """
    The fraction field of an integral domain.
    """
    def __init__(self, R,
            element_class=fraction_field_element.FractionFieldElement,
            category=QuotientFields()):
        """
        Create the fraction field of the integral domain R.
        
        INPUT:
        
        
        -  ``R`` - an integral domain
        
        
        EXAMPLES::
        
            sage: Frac(QQ['x'])
            Fraction Field of Univariate Polynomial Ring in x over Rational Field
            sage: Frac(QQ['x,y']).variable_names()
            ('x', 'y')
            sage: category(Frac(QQ['x']))
            Category of quotient fields
        """
        self._R = R
        self._element_class = element_class
        self._element_init_pass_parent = False
        Parent.__init__(self, base=R, names=R._names, category=category)

    def __reduce__(self):
        """
        TESTS::
        
            sage: K = Frac(QQ['x'])
            sage: loads(dumps(K)) is K
            True
        """
        return FractionField, (self._R,)

    def _coerce_map_from_(self, S):
        """
        Returns ``True`` if elements of ``S`` can be coerced into this 
        fraction field.
        
        This fraction field has coercions from:
        
        - itself
        - any fraction field where the base ring coerces to the base
          ring of this fraction field
        - any ring that coerces to the base ring of this fraction field
        
        EXAMPLES::
        
            sage: F = QQ['x,y'].fraction_field()
            sage: F.has_coerce_map_from(F)
            True
        
        ::
        
            sage: F.has_coerce_map_from(ZZ['x,y'].fraction_field())
            True
        
        ::
        
            sage: F.has_coerce_map_from(ZZ['x,y,z'].fraction_field())
            False
        
        ::
        
            sage: F.has_coerce_map_from(ZZ)
            True
        
        Test coercions:
        
        ::
        
            sage: F.coerce(1)
            1
            sage: F.coerce(int(1))
            1
            sage: F.coerce(1/2)
            1/2
        
        ::
        
            sage: K = ZZ['x,y'].fraction_field()
            sage: x,y = K.gens()
            sage: F.coerce(F.gen())
            x
            sage: F.coerce(x)
            x
            sage: F.coerce(x/y)
            x/y
            sage: L = ZZ['x'].fraction_field()
            sage: K.coerce(L.gen())
            x
        
        We demonstrate that trac ticket #7958 is resolved in the case of 
        number fields::
        
            sage: _.<x> = ZZ[]
            sage: K.<a> = NumberField(x^5-3*x^4+2424*x^3+2*x-232)
            sage: R.<b> = K.ring_of_integers()
            sage: S.<y> = R[]
            sage: F = FractionField(S)
            sage: F(1/a)
            (a^4 - 3*a^3 + 2424*a^2 + 2)/232
        """
        from sage.rings.integer_ring import ZZ
        from sage.rings.rational_field import QQ
        from sage.rings.number_field.number_field_base import NumberField
        
        # The case ``S`` being `\QQ` requires special handling since `\QQ` is 
        # not implemented as a ``FractionField_generic``.
        if S is QQ and self._R.has_coerce_map_from(ZZ):
            return CallableConvertMap(S, self, \
                lambda x: self._element_class(self, x.numerator(),
                x.denominator()), parent_as_first_arg=False)
        
        # Number fields also need to be handled separately.
        if isinstance(S, NumberField):
            return CallableConvertMap(S, self, \
                self._number_field_to_frac_of_ring_of_integers, \
                parent_as_first_arg=False)
        
        if isinstance(S, FractionField_generic) and \
            self._R.has_coerce_map_from(S.ring()):
            return CallableConvertMap(S, self, \
                lambda x: self._element_class(self, x.numerator(),
                x.denominator()), parent_as_first_arg=False)
        
        if self._R.has_coerce_map_from(S):
            return CallableConvertMap(S, self, self._element_class,
                parent_as_first_arg=True)
        
        return None
    
    def _number_field_to_frac_of_ring_of_integers(self, x):
        r"""
        Returns the number field element ``x`` as an element of ``self``, 
        explicitly treating the numerator of ``x``  as an element of the ring 
        of integers and the denominator as an integer.
        
        INPUT:
        
        -  ``x`` - Number field element
        
        OUTPUT:
        
        -  Element of ``self``
        
        TEST:
        
        We demonstrate that trac ticket #7958 is resolved in the case of 
        number fields::
        
            sage: _.<x> = ZZ[]
            sage: K.<a> = NumberField(x^5-3*x^4+2424*x^3+2*x-232)
            sage: R.<b> = K.ring_of_integers()
            sage: S.<y> = R[]
            sage: F = FractionField(S)
            sage: F(1/a)
            (a^4 - 3*a^3 + 2424*a^2 + 2)/232
        """
        f = x.polynomial()   # Polynomial over QQ
        d = f.denominator()  # Integer
        return self._element_class(self, numerator=d*x, denominator=d)
    
    def is_field(self, proof = True):
        """
        Returns True, since the fraction field is a field.
        
        EXAMPLES::
        
            sage: Frac(ZZ).is_field()
            True
        """
        return True

    def is_finite(self):
        """
        Tells whether this fraction field is finite.

        .. NOTE::

           A fraction field is finite if and only if the associated
           integral domain is finite.

        EXAMPLE::

            sage: Frac(QQ['a','b','c']).is_finite()
            False

        """
        return self._R.is_finite()

    def base_ring(self):
        """
        Return the base ring of self; this is the base ring of the ring
        which this fraction field is the fraction field of.
        
        EXAMPLES::
        
            sage: R = Frac(ZZ['t']) 
            sage: R.base_ring()
            Integer Ring
        """
        return self._R.base_ring()

    def characteristic(self):
        """
        Return the characteristic of this fraction field.
        
        EXAMPLES::
        
            sage: R = Frac(ZZ['t']) 
            sage: R.base_ring()
            Integer Ring
            sage: R = Frac(ZZ['t']); R.characteristic()
            0
            sage: R = Frac(GF(5)['w']); R.characteristic()
            5
        """
        return self._R.characteristic()
    
    def _repr_(self):
        """
        EXAMPLES::
        
            sage: str(Frac(ZZ['x']))
            'Fraction Field of Univariate Polynomial Ring in x over Integer Ring'
        """
        return "Fraction Field of %s"%self._R

    def _latex_(self):
        """
        EXAMPLES::
        
            sage: latex(Frac(GF(7)['x,y,z']))
            \mathrm{Frac}(\Bold{F}_{7}[x, y, z])
        """
        return "\\mathrm{Frac}(%s)"%latex.latex(self._R)

    def _magma_init_(self, magma):
        """
        Return a string representation of self in the given magma
        instance.
        
        EXAMPLES::
        
            sage: QQ['x'].fraction_field()._magma_init_(magma)            # optional - magma
            'SageCreateWithNames(FieldOfFractions(SageCreateWithNames(PolynomialRing(_sage_ref...),["x"])),["x"])'
            sage: GF(9,'a')['x,y,z'].fraction_field()._magma_init_(magma) # optional - magma
            'SageCreateWithNames(FieldOfFractions(SageCreateWithNames(PolynomialRing(_sage_ref...,3,"grevlex"),["x","y","z"])),["x","y","z"])'
        
        _magma_init_ gets called implicitly below.
        
        ::
        
            sage: magma(QQ['x,y'].fraction_field())                  # optional - magma
            Multivariate rational function field of rank 2 over Rational Field
            Variables: x, y
            sage: magma(ZZ['x'].fraction_field())                    # optional - magma
            Univariate rational function field over Integer Ring
            Variables: x
        
        Verify that conversion is being properly cached::
        
            sage: k = Frac(QQ['x,z'])                                # optional - magma
            sage: magma(k) is magma(k)                               # optional - magma
            True
        """
        s = 'FieldOfFractions(%s)'%self.ring()._magma_init_(magma)
        return magma._with_names(s, self.variable_names())

    def ring(self):
        """
        Return the ring that this is the fraction field of.
        
        EXAMPLES::
        
            sage: R = Frac(QQ['x,y'])
            sage: R
            Fraction Field of Multivariate Polynomial Ring in x, y over Rational Field
            sage: R.ring()
            Multivariate Polynomial Ring in x, y over Rational Field
        """
        return self._R
    
    def is_exact(self):
        """
        EXAMPLES::
        
            sage: Frac(ZZ['x']).is_exact()
            True
            sage: Frac(CDF['x']).is_exact()
            False
        """
        try:
            return self.__is_exact
        except AttributeError:
            r = self.ring().is_exact()
            self.__is_exact = r
        return r

    def _element_constructor_(self, x, y=1, coerce=True):
        """
        Construct an element of this fraction field.
        
        EXAMPLES::
        
            sage: F = QQ['x,y'].fraction_field()
            sage: F._element_constructor_(1)
            1
            sage: F._element_constructor_(F.gen(0)/F.gen(1))
            x/y
        
        ::
        
            sage: K = ZZ['x,y'].fraction_field()
            sage: x,y = K.gens()
        
        ::
        
            sage: F._element_constructor_(x/y)
            x/y
        """
        if isinstance(x, self._element_class):
            if x.parent() is self:
                return x
            else:
                return self._element_class(self, x.numerator(), x.denominator())
        return self._element_class(self, x, y,
                coerce=coerce, reduce = self.is_exact())

    def construction(self):
        """
        EXAMPLES::
        
            sage: Frac(ZZ['x']).construction()
            (FractionField, Univariate Polynomial Ring in x over Integer Ring)
            sage: K = Frac(GF(3)['t'])
            sage: f, R = K.construction()
            sage: f(R)
            Fraction Field of Univariate Polynomial Ring in t over Finite Field of size 3
            sage: f(R) == K
            True
        """
        from sage.categories.pushout import FractionField
        return FractionField(), self.ring()

    def __cmp__(self, other):
        """
        EXAMPLES::
        
            sage: Frac(ZZ['x']) == Frac(ZZ['x'])
            True
            sage: Frac(ZZ['x']) == Frac(QQ['x'])
            False
            sage: Frac(ZZ['x']) == Frac(ZZ['y'])
            False
            sage: Frac(ZZ['x']) == QQ['x']
            False
        """
        if not isinstance(other, FractionField_generic):
            return cmp(type(self), type(other))
        return cmp(self._R, other._R)

    def ngens(self):
        """
        This is the same as for the parent object.
        
        EXAMPLES::
        
            sage: R = Frac(PolynomialRing(QQ,'z',10)); R
            Fraction Field of Multivariate Polynomial Ring in z0, z1, z2, z3, z4, z5, z6, z7, z8, z9 over Rational Field
            sage: R.ngens()
            10
        """
        return self._R.ngens()

    def gen(self, i=0):
        """
        Return the ith generator of self.
        
        EXAMPLES::
        
            sage: R = Frac(PolynomialRing(QQ,'z',10)); R
            Fraction Field of Multivariate Polynomial Ring in z0, z1, z2, z3, z4, z5, z6, z7, z8, z9 over Rational Field
            sage: R.0
            z0
            sage: R.gen(3)
            z3
            sage: R.3
            z3
        """
        x = self._R.gen(i)
        one = self._R.one_element()
        r = self._element_class(self, x, one, coerce=False, reduce=False)
        return r

    def _is_valid_homomorphism_(self, codomain, im_gens):
        """
        Check if the homomorphism defined by sending generators of this
        fraction field to im_gens in codomain is valid.
        
        EXAMPLES::
        
            sage: F = QQ['x,y'].fraction_field()
            sage: x,y = F.gens()
            sage: F._is_valid_homomorphism_(F, [y,x])
            True
            sage: R = ZZ['x']; x = R.gen()
            sage: F._is_valid_homomorphism_(R, [x, x])
            False
        
        TESTS::
        
            sage: F._is_valid_homomorphism_(ZZ, [])
            False
        
        Test homomorphisms:
        
        ::
        
            sage: phi = F.hom([2*y, x])
            sage: phi(x+y)
            x + 2*y
            sage: phi(x/y)
            2*y/x
        """
        if len(im_gens) != self.ngens():
            return False
        # it is enough to check if elements of the base ring coerce to
        # the codomain
        if codomain.has_coerce_map_from(self.base_ring()):
            return True
        return False

    def random_element(self, *args, **kwds):
        """
        Returns a random element in this fraction field.
        
        EXAMPLES::
        
            sage: F = ZZ['x'].fraction_field()
            sage: F.random_element()
            (2*x - 8)/(-x^2 + x)
        
        ::
        
            sage: F.random_element(degree=5)
            (-12*x^5 - 2*x^4 - x^3 - 95*x^2 + x + 2)/(-x^5 + x^4 - x^3 + x^2)
        """
        return self._element_class(self, self._R.random_element(*args, **kwds),
            self._R._random_nonzero_element(*args, **kwds), 
            coerce = False, reduce=True)

class FractionField_1poly_field(FractionField_generic):
    """
    The fraction field of a univariate polynomial ring over a field.

    Many of the functions here are included for coherence with number fields.
    """
    def __init__(self, R,
            element_class=fraction_field_element.FractionFieldElement_1poly_field):
        """
        Just changes the default for element_class

        EXAMPLES::

            sage: R.<t> = QQ[]; K = R.fraction_field()
            sage: K._element_class
            <class 'sage.rings.fraction_field_element.FractionFieldElement_1poly_field'>
        """
        FractionField_generic.__init__(self, R, element_class)

    def ring_of_integers(self):
        """
        Returns the ring of integers in this fraction field.

        EXAMPLES::

            sage: K = FractionField(GF(5)['t'])
            sage: K.ring_of_integers()
            Univariate Polynomial Ring in t over Finite Field of size 5
        """
        return self._R

    def maximal_order(self):
        """
        Returns the maximal order in this fraction field.

        EXAMPLES::

            sage: K = FractionField(GF(5)['t'])
            sage: K.maximal_order()
            Univariate Polynomial Ring in t over Finite Field of size 5
        """
        return self._R

    def class_number(self):
        """
        Here for compatibility with number fields and function fields.

        EXAMPLES::

            sage: R.<t> = GF(5)[]; K = R.fraction_field()
            sage: K.class_number()
            1
        """
        return 1
