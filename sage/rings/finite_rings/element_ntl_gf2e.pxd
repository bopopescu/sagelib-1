include "../../libs/ntl/decl.pxi"

from sage.rings.finite_rings.finite_field_base cimport FiniteField
from sage.structure.element cimport Element, RingElement, ModuleElement
from sage.rings.finite_rings.element_base cimport FinitePolyExtElement

cdef class FiniteField_ntl_gf2eElement(FinitePolyExtElement)

cdef class FiniteField_ntl_gf2e(FiniteField):
    cdef GF2EContext_c F
    cdef object _polynomial 
    cdef object _polynomial_ring 
    cdef object _is_conway
    cdef object _hash
    cdef _coerce_c_impl(self, x)
    cdef FiniteField_ntl_gf2eElement _new(FiniteField_ntl_gf2e self)

cdef class FiniteField_ntl_gf2e_iterator:
    cdef int iterator
    cdef FiniteField_ntl_gf2e _parent

cdef class FiniteField_ntl_gf2eElement(FinitePolyExtElement):
    cdef GF2E_c x
    cdef FiniteField_ntl_gf2eElement _new(FiniteField_ntl_gf2eElement self)
