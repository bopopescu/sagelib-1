r"""
Affine Weyl Groups
"""
#*****************************************************************************
#  Copyright (C) 2009    Nicolas M. Thiery <nthiery at users.sf.net>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#******************************************************************************

from sage.misc.cachefunc import cached_method
from sage.categories.category import Category
from sage.categories.category_singleton import Category_singleton
from sage.categories.weyl_groups import WeylGroups

class AffineWeylGroups(Category_singleton):

    @cached_method
    def super_categories(self):
        r"""
        EXAMPLES::

            sage: AffineWeylGroups().super_categories()
            [Category of weyl groups]
        """
        return [WeylGroups()]

    class ParentMethods:

        @cached_method
        def special_node(self):
            """
            Returns the distinguished special node of the underlying
            Dynkin diagram
            
            EXAMPLES::

                sage: W=WeylGroup(['A',3,1])
                sage: W.special_node()
                0
                
            """
            return self.cartan_type().special_node()

        def affine_grassmannian_elements_of_given_length(self, k):
            """
            Returns the affine Grassmannian elements of length `k`, as a list.

            EXAMPLES::

                sage: W=WeylGroup(['A',3,1])
                sage: [x.reduced_word() for x in W.affine_grassmannian_elements_of_given_length(3)]
                [[2, 1, 0], [3, 1, 0], [2, 3, 0]]

            SEE ALSO: :meth:`AffineWeylGroups.ElementMethods.is_affine_grassmannian`.

            TODO: should return an enumerated set, with iterator, ...
            """
            if k == 0:
                return [self.unit()]
            w = []
            s = self.simple_reflections()
            for x in self.affine_grassmannian_elements_of_given_length(k-1):
                for i in x.descents(side="left", positive = True):
                    y = s[i]*x
                    if y not in w and y.is_affine_grassmannian():
                        w.append(y)
            return w

    class ElementMethods:
        def is_affine_grassmannian(self):
            """
            INPUT:
             - self: an element of an affine Weyl group
            
            Tests whether self is Grassmannian, i.e. any of the following
            equivalent properties hold:
             - all reduced words for self end with 0.
             - self is the identity, or 0 is its single right descent.
             - self is a mimimal coset representative for W / cl W.

            EXAMPLES::

                sage: W=WeylGroup(['A',3,1])
                sage: w=W.from_reduced_word([2,1,0])
                sage: w.is_affine_grassmannian()
                True
                sage: w=W.from_reduced_word([2,0])
                sage: w.is_affine_grassmannian()
                False
                sage: W.unit().is_affine_grassmannian()
                True
            """
            return self.descents() in [[], [self.parent().special_node()]]

        def affine_grassmannian_to_core(self):
            r"""
            Bijection between affine Grassmannian elements of type `A_k^{(1)}` and `(k+1)`-cores.

            INPUT:

            - ``self`` -- an affine Grassmannian element of some affine Weyl group of type `A_k^{(1)}`

            Recall that an element `w` of an affine Weyl group is
            affine Grassmannian if all its all reduced words end in 0, see :meth:`is_affine_grassmannian`.

            OUTPUT:

            - a `(k+1)`-core

            See also :meth:`affine_grassmannian_to_partition`.

            EXAMPLES::

                sage: W = WeylGroup(['A',2,1])
                sage: w = W.from_reduced_word([0,2,1,0])
                sage: la = w.affine_grassmannian_to_core(); la
                [4, 2]
                sage: type(la)
                <class 'sage.combinat.core.Cores_length_with_category.element_class'>
                sage: la.to_grassmannian() == w
                True

                sage: w = W.from_reduced_word([0,2,1])
                sage: w.affine_grassmannian_to_core()
                Traceback (most recent call last):
                ...
                ValueError: Error! this only works on type 'A' affine Grassmannian elements
            """
            from sage.combinat.partition import Partition
            from sage.combinat.core import Core
            if not self.is_affine_grassmannian() or not self.parent().cartan_type().letter == 'A':
                raise ValueError, "Error! this only works on type 'A' affine Grassmannian elements"
            out = Partition([])
            rword = self.reduced_word()
            kp1 = self.parent().n
            for i in range(len(rword)):
                for c in filter( lambda x: (x[1]-x[0])%kp1==rword[-i-1], out.outside_corners()):
                    out = out.add_cell(c[0],c[1])
            return Core(out._list,kp1)

        def affine_grassmannian_to_partition(self):
            r"""
            Bijection between affine Grassmannian elements of type `A_k^{(1)}` and `k`-bounded partitions.

            INPUT:

            - ``self`` is affine Grassmannian element of the affine Weyl group of type `A_k^{(1)}` (i.e. all reduced words end in 0)

            OUTPUT:

            - `k`-bounded partition

            See also :meth:`affine_grassmannian_to_core`.

            EXAMPLES::

                sage: k = 2
                sage: W = WeylGroup(['A',k,1])
                sage: w = W.from_reduced_word([0,2,1,0])
                sage: la = w.affine_grassmannian_to_partition(); la
                [2, 2]
                sage: la.from_kbounded_to_grassmannian(k) == w
                True
            """
            return self.affine_grassmannian_to_core().to_bounded_partition()

