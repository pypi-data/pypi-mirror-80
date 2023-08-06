""" Defines the Basis object and supporting functions """
#***************************************************************************************************
# Copyright 2015, 2019 National Technology & Engineering Solutions of Sandia, LLC (NTESS).
# Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains certain rights
# in this software.
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
# in compliance with the License.  You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0 or in the LICENSE file in the root pyGSTi directory.
#***************************************************************************************************

from functools import partial, wraps, lru_cache
from itertools import product, chain

import copy as _copy
import numbers as _numbers
import collections as _collections
import warnings as _warnings
import itertools as _itertools

from numpy.linalg import inv as _inv
import numpy as _np
import scipy.sparse as _sps
import scipy.sparse.linalg as _spsl

import math

from ..tools.basisconstructors import _basisConstructorDict


#Helper functions
def _sparse_equal(A, B, atol=1e-8):
    """ NOTE: same as matrixtools.sparse_equal - but can't import that here """
    if _np.array_equal(A.shape, B.shape) == 0:
        return False

    r1, c1 = A.nonzero()
    r2, c2 = B.nonzero()

    lidx1 = _np.ravel_multi_index((r1, c1), A.shape)
    lidx2 = _np.ravel_multi_index((r2, c2), B.shape)
    sidx1 = lidx1.argsort()
    sidx2 = lidx2.argsort()

    index_match = _np.array_equal(lidx1[sidx1], lidx2[sidx2])
    if index_match == 0:
        return False
    else:
        v1 = A.data
        v2 = B.data
        V1 = v1[sidx1]
        V2 = v2[sidx2]
    return _np.allclose(V1, V2, atol=atol)


class Basis(object):
    '''
    An ordered set of labeled matrices/vectors.

    The base class for basis objects.  A basis in pyGSTi is an abstract notion
    of a set of labeled elements, or "vectors".  Each basis has a certain size,
    and has .elements, .labels, and .ellookup members, the latter being a
    dictionary mapping of labels to elements.

    An important point to note that isn't immediately
    intuitive is that while Basis object holds *elements* (in its
    `.elements` property) these are not the same as its *vectors*
    (given by the object's `vector_elements` property).  Often times,
    in what we term a "simple" basis, the you just flatten an element
    to get the corresponding vector-element.  This works for bases
    where the elements are either vectors (where flattening does
    nothing) and matrices.  By storing `elements` as distinct from
    `vector_elements`, the Basis can capture additional structure
    of the elements (such as viewing them as matrices) that can
    be helpful for their display and interpretation.  The elements
    are also sometimes referred to as the "natural elements" because
    they represent how to display the element in a natrual way.  A
    non-simple basis occurs when vector_elements need to be stored as
    elements in a larger "embedded" way so that these elements can be
    displayed and interpeted naturally.

    A second important note is that there is assumed to be some underlying
    "standard" basis underneath all the bases in pyGSTi.  The elements in
    a Basis are *always* written in this standard basis.  In the case of the
    "std"-named basis in pyGSTi, these elements are just the trivial vector
    or matrix units, so one can rightly view the "std" pyGSTi basis as the
    "standard" basis for a that particular dimension.
    '''

    @classmethod
    def cast(cls, nameOrBasisOrMatrices, dim=None, sparse=None, classicalName='cl'):
        """
        Convert various things that can describe a basis into a `Basis` object.

        Parameters
        ----------
        nameOrBasisOrMatrices : various
            Can take on a variety of values to produce different types of bases:

            - `None`: an empty `ExpicitBasis`
            - `Basis`: checked with `dim` and `sparse` and passed through.
            - `str`: `BuiltinBasis` or `DirectSumBasis` with the given name.
            - `list`: an `ExplicitBasis` if given matrices/vectors or a
                     `DirectSumBasis` if given a `(name, dim)` pairs.

        dim : int or StateSpaceLabels, optional
            The dimension of the basis to create.  Sometimes this can be
            inferred based on `nameOrBasisOrMatrices`, other times it must
            be supplied.  This is the dimension of the space that this basis
            fully or partially spans.  This is equal to the number of basis
            elements in a "full" (ordinary) basis.  When a `StateSpaceLabels`
            object is given, a more detailed direct-sum-of-tensor-product-blocks
            structure for the state space (rather than a single dimension) is
            described, and a basis is produced for this space.  For instance,
            a `DirectSumBasis` basis of `TensorProdBasis` components can result
            when there are multiple tensor-product blocks and these blocks
            consist of multiple factors.

        sparse : bool, optional
            Whether the resulting basis should be "sparse", meaning that its
            elements will be sparse rather than dense matrices.

        classicalName : str, optional
            An alternate builtin basis name that should be used when
            constructing the bases for the classical sectors of `dim`,
            when `dim` is a `StateSpaceLabels` object.

        Returns
        -------
        Basis
        """
        #print("DB: CAST = ",nameOrBasisOrMatrices,dim)
        from .labeldicts import StateSpaceLabels as _SSLs
        if nameOrBasisOrMatrices is None:  # special case of empty basis
            return ExplicitBasis([], [], "*Empty*", "Empty (0-element) basis", False, sparse)  # empty basis
        elif isinstance(nameOrBasisOrMatrices, Basis):
            #then just check to make sure consistent with `dim` & `sparse`
            basis = nameOrBasisOrMatrices
            if dim is not None:
                assert(dim == basis.dim or dim == basis.elsize), \
                    "Basis object has unexpected dimension: %d != %d or %d" % (dim, basis.dim, basis.elsize)
            if sparse is not None:
                assert(sparse == basis.sparse), "Basis object has unexpected sparsity: %s" % (basis.sparse)
            return basis
        elif isinstance(nameOrBasisOrMatrices, str):
            name = nameOrBasisOrMatrices
            if isinstance(dim, _SSLs):
                sslbls = dim
                tpbBases = []
                for tpbLabels in sslbls.labels:
                    if len(tpbLabels) == 1:
                        nm = name if (sslbls.labeltypes[tpbLabels[0]] == 'Q') else classicalName
                        tpbBases.append(BuiltinBasis(nm, sslbls.labeldims[tpbLabels[0]], sparse))
                    else:
                        tpbBases.append(TensorProdBasis([
                            BuiltinBasis(name if (sslbls.labeltypes[l] == 'Q') else classicalName,
                                         sslbls.labeldims[l], sparse) for l in tpbLabels]))
                if len(tpbBases) == 1:
                    return tpbBases[0]
                else:
                    return DirectSumBasis(tpbBases)
            elif isinstance(dim, (list, tuple)):  # list/tuple of block dimensions
                tpbBases = []
                for tpbDim in dim:
                    if isinstance(tpbDim, (list, tuple)):  # list/tuple of tensor-product dimensions
                        tpbBases.append(
                            TensorProdBasis([BuiltinBasis(name, factorDim, sparse) for factorDim in tpbDim]))
                    else:
                        tpbBases.append(BuiltinBasis(name, tpbDim, sparse))
                return DirectSumBasis(tpbBases)
            else:
                return BuiltinBasis(name, dim, sparse)
        elif isinstance(nameOrBasisOrMatrices, (list, tuple, _np.ndarray)):
            # assume a list/array of matrices or (name, dim) pairs
            if len(nameOrBasisOrMatrices) == 0:  # special case of empty basis
                return ExplicitBasis([], [], "*Empty*", "Empty (0-element) basis", False, sparse)  # empty basis
            elif isinstance(nameOrBasisOrMatrices[0], _np.ndarray):
                b = ExplicitBasis(nameOrBasisOrMatrices, sparse=sparse)
                if dim is not None:
                    assert(dim == b.dim), "Created explicit basis has unexpected dimension: %d vs %d" % (dim, b.dim)
                if sparse is not None:
                    assert(sparse == b.sparse), "Basis object has unexpected sparsity: %s" % (b.sparse)
                return b
            else:  # assume els are (name, dim) pairs
                compBases = [BuiltinBasis(subname, subdim, sparse)
                             for (subname, subdim) in nameOrBasisOrMatrices]
                return DirectSumBasis(compBases)

        else:
            raise ValueError("Can't cast %s to be a basis!" % str(type(nameOrBasisOrMatrices)))

    def __init__(self, name, longname, dim, size, elshape, real, sparse):
        """
        Create a new Basis (base class) object.

        The arguments below describe the basic properties of all basis
        objects in pyGSTi.  It is important to remember that the
        `vector_elements` of a basis are different from its `elements`
        (see the :class:`Basis` docstring), and that `dim` refers
        to the vector elements whereas elshape refers to the elements.

        For example, consider a 2-element Basis containing the I and X Pauli
        matrices.  The `size` of this basis is `2`, as there are two elements
        (and two vector elements).  Since vector elements are the length-4
        flattened Pauli matrices, the dimension (`dim`) is `4`.  Since the
        elements are 2x2 Pauli matrices, the `elshape` is `(2,2)`.

        As another example consider a basis which spans all the diagonal
        2x2 matrices.  The elements of this basis are the two matrix units
        with a 1 in the (0,0) or (1,1) location.  The vector elements,
        however, are the length-2 [1,0] and [0,1] vectors obtained by extracting
        just the diagonal entries from each basis element.  Thus, for this
        basis, `size=2`, `dim=2`, and `elshape=(2,2)` - so the dimension is
        not just the product of `elshape` entries (equivalently, `elsize`).


        Parameters
        ----------
        name : string
            The name of the basis.  This can be anything, but is
            usually short and abbreviated.  There are several
            types of bases built into pyGSTi that can be constructed by
            this name.

        longname : string
            A more descriptive name for the basis.

        dim : int
            The dimension of the vector space this basis fully or partially
            spans.  Equivalently, the length of the `vector_elements` of the
            basis.

        size : int
            The number of elements (or vector-elements) in the basis.

        elshape : tuple
            The shape of each element.  Typically either a length-1 or length-2
            tuple, corresponding to vector or matrix elements, respectively.
            Note that *vector elements* always have shape `(dim,)` (or `(dim,1)`
            in the sparse case).

        real : bool
            Elements and vector elements are always allowed to have complex
            entries.  This argument indicates whether the coefficients in the
            expression of an arbitrary vector in this basis must be real.  For
            example, if `real=True`, then when pyGSTi transforms a vector in
            some other basis to a vector in *this* basis, it will demand that
            the values of that vector (i.e. the coefficients which multiply
            this basis's elements to obtain a vector in the "standard" basis)
            are real.

        sparse : bool
            Whether the elements of `.elements` for this Basis are stored (when
            they are stored at all) as sparse matrices or vectors.
        """
        self.name = name
        self.longname = longname
        self.dim = dim  # dimension of vector space this basis fully or partially spans
        self.size = size  # number of elements (== dim if a *full* basis)
        self.elshape = tuple(elshape)  # shape of "natural" elements - size may be > self.dim (to display naturally)
        # whether coefficients must be real (*not* whether elements are real - they're always complex)
        self.real = real
        self.sparse = sparse  # whether elements are stored as sparse vectors/matrices

    @property
    def elndim(self):
        """The number of element dimensions, i.e. `len(self.elshape)`"""
        if self.elshape is None: return 0
        return len(self.elshape)

    @property
    def elsize(self):
        """The total element size, i.e. `product(self.elshape)`"""
        if self.elshape is None: return 0
        return int(_np.product(self.elshape))

    def is_simple(self):
        """
        Whether the flattened-element vector space is the *same*
        space as the space this basis's vectors belong to.

        Returns
        -------
        bool
        """
        return self.elsize == self.dim

    def is_complete(self):
        """
        Whether this is a complete basis, i.e. this basis's
        vectors span the entire space that they live in.

        Returns
        -------
        bool
        """
        return self.dim == self.size

    def is_partial(self):
        """
        The negative of :method:`is_complete`, effectively "is_incomplete".

        Returns
        -------
        bool
        """
        return not self.is_complete()

    @property
    def vector_elements(self):
        """ The "vectors" of this basis, always 1D (sparse or dense) arrays. """
        if self.sparse:
            return [_sps.lil_matrix(el).reshape((self.elsize, 1)) for el in self.elements]
        else:
            return [el.flatten() for el in self.elements]

    def copy(self):
        """
        Make a copy of this Basis object.

        Returns
        -------
        Basis
        """
        return _copy.deepcopy(self)

    def __str__(self):
        return '{} (dim={}), {} elements of shape {} :\n{}'.format(
            self.longname, self.dim, self.size, self.elshape, ', '.join(self.labels))

    def __getitem__(self, index):
        if isinstance(index, str) and self.ellookup is not None:
            return self.ellookup[index]
        return self.elements[index]

    def __len__(self):
        return self.size

    def __eq__(self, other):
        otherIsBasis = isinstance(other, Basis)

        if otherIsBasis and (self.sparse != other.sparse):  # sparseness mismatch => not equal
            return False

        if self.sparse:
            if self.dim > 256:
                _warnings.warn("Attempted comparison between bases with large sparse matrices!  Assuming not equal.")
                return False  # to expensive to compare sparse matrices

            if otherIsBasis:
                return all([_sparse_equal(A, B) for A, B in zip(self.elements, other.elements)])
            else:
                return all([_sparse_equal(A, B) for A, B in zip(self.elements, other)])
        else:
            if otherIsBasis:
                return _np.array_equal(self.elements, other.elements)
            else:
                return _np.array_equal(self.elements, other)

    def transform_matrix(self, to_basis):
        '''
        Get the matrix that transforms a vector from this basis to `to_basis`.

        Parameters
        ----------
        to_basis : Basis or string
            The basis to transform to or a built-in basis name.  In the latter
            case, a basis to transform to is built with the same structure as
            this basis but with all components constructed from the given name.

        Returns
        -------
        numpy.ndarray (even if basis is sparse)
        '''
        #Note: construct to_basis as sparse this basis is sparse and
        # if to_basis is not already a Basis object
        if not isinstance(to_basis, Basis):
            to_basis = self.equivalent(to_basis)

        #Note same logic as matrixtools.safedot(...)
        if to_basis.sparse:
            return to_basis.get_from_std().dot(self.get_to_std())
        elif self.sparse:
            #return _sps.csr_matrix(to_basis.get_from_std()).dot(self.get_to_std())
            return _np.dot(to_basis.get_from_std(), self.get_to_std().toarray())
        else:
            return _np.dot(to_basis.get_from_std(), self.get_to_std())

    def reverse_transform_matrix(self, from_basis):
        '''
        Get the matrix that transforms a vector from `from_basis` to this basis.

        The reverse of :method:`transform_matrix`.

        Parameters
        ----------
        from_basis : Basis or string
            The basis to transform from or a built-in basis name.  In the latter
            case, a basis to transform from is built with the same structure as
            this basis but with all components constructed from the given name.

        Returns
        -------
        numpy.ndarray (even if basis is sparse)
        '''
        if not isinstance(from_basis, Basis):
            from_basis = self.equivalent(from_basis)

        #Note same logic as matrixtools.safedot(...)
        if self.sparse:
            return self.get_from_std().dot(from_basis.get_to_std())
        elif from_basis.sparse:
            #return _sps.csr_matrix(to_basis.get_from_std()).dot(self.get_to_std())
            return _np.dot(self.get_from_std(), from_basis.get_to_std().toarray())
        else:
            return _np.dot(self.get_from_std(), from_basis.get_to_std())

    @lru_cache(maxsize=128)
    def is_normalized(self):
        '''
        Check if a basis is normalized, meaning that Tr(Bi Bi) = 1.0.

        Available only to bases whose elements are *matrices* for now.

        Returns
        -------
        bool
        '''
        if self.elndim == 2:
            for i, mx in enumerate(self.elements):
                t = _np.trace(_np.dot(mx, mx))
                t = _np.real(t)
                if not _np.isclose(t, 1.0): return False
            return True
        elif self.elndim == 1:
            raise NotImplementedError("TODO: add code so this works for *vector*-valued bases too!")
        else:
            raise ValueError("I don't know what normalized means for elndim == %d!" % self.elndim)

    @lru_cache(maxsize=128)
    def get_to_std(self):
        '''
        Retrieve the matrix that transforms a vector from this basis to the
        standard basis of this basis's dimension.

        Returns
        -------
        numpy array or scipy.sparse.lil_matrix
            An array of shape `(dim, size)` where `dim` is the dimension
            of this basis (the length of its vectors) and `size` is the
            size of this basis (its number of vectors).
        '''
        if self.sparse:
            toStd = _sps.lil_matrix((self.dim, self.size), dtype='complex')
        else:
            toStd = _np.zeros((self.dim, self.size), 'complex')

        for i, vel in enumerate(self.vector_elements):
            toStd[:, i] = vel
        return toStd

    @lru_cache(maxsize=128)
    def get_from_std(self):
        '''
        Retrieve the matrix that transforms vectors from the standard basis
        to this basis.

        Returns
        -------
        numpy array or scipy sparse matrix
            An array of shape `(size, dim)` where `dim` is the dimension
            of this basis (the length of its vectors) and `size` is the
            size of this basis (its number of vectors).
        '''
        if self.sparse:
            if self.is_complete():
                return _spsl.inv(self.get_to_std().tocsc()).tocsr()
            else:
                assert(self.size < self.dim), "Basis seems to be overcomplete: size > dimension!"
                # we'd need to construct a different pseudo-inverse if the above assert fails

                A = self.get_to_std()  # shape (dim,size) - should have indep *cols*
                Adag = A.getH()        # shape (size, dim)
                invAdagA = _spsl.inv(Adag.tocsr().dot(A.tocsc())).tocsr()
                return invAdagA.dot(Adag.tocsc())
        else:
            if self.is_complete():
                return _inv(self.get_to_std())
            else:
                assert(self.size < self.dim), "Basis seems to be overcomplete: size > dimension!"
                # we'd need to construct a different pseudo-inverse if the above assert fails

                A = self.get_to_std()  # shape (dim,size) - should have indep *cols*
                Adag = A.transpose().conjugate()  # shape (size, dim)
                return _np.dot(_inv(_np.dot(Adag, A)), Adag)

    @lru_cache(maxsize=128)
    def get_to_element_std(self):
        '''
        Get the matrix that transforms vectors in this basis (with length equal
        to the `dim` of this basis) to vectors in the "element space" - that
        is, vectors in the same standard basis that the *elements* of this basis
        are expressed in.

        Returns
        -------
        numpy array
            An array of shape `(element_dim, size)` where `element_dim` is the
            dimension, i.e. size, of the elements of this basis (e.g. 16 if the
            elements are 4x4 matrices) and `size` is the size of this basis (its
            number of vectors).
        '''
        # This default implementation assumes that the (flattened) element space
        # *is* a standard representation of the vector space this basis or partial-basis
        # acts upon (this is *not* true for direct-sum bases, where the flattened
        # elements represent vectors in a larger "embedding" space (w/larger dim than actual space).
        assert(self.is_simple()), "Incorrectly using a simple-assuming implementation of get_to_element_std"
        return self.get_to_std()

    @lru_cache(maxsize=128)
    def get_from_element_std(self):  # OLD: get_expand_mx(self):
        '''
        Get the matrix that transforms vectors in the "element space" - that
        is, vectors in the same standard basis that the *elements* of this basis
        are expressed in - to vectors in this basis (with length equal to the
        `dim` of this basis).

        Returns
        -------
        numpy array
            An array of shape `(size, element_dim)` where `element_dim` is the
            dimension, i.e. size, of the elements of this basis (e.g. 16 if the
            elements are 4x4 matrices) and `size` is the size of this basis (its
            number of vectors).
        '''
        if self.sparse:
            raise NotImplementedError("get_from_element_std not implemented for sparse mode")  # (b/c pinv used)
        return _np.linalg.pinv(self.get_to_element_std())

    def equivalent(self, builtinBasisName):
        """
        Create a Basis that is equivalent in structure & dimension to this
        basis but whose simple components (perhaps just this basis itself) is
        of the builtin basis type given by `builtinBasisName`.

        Parameters
        ----------
        builtinBasisName : str
            The name of a builtin basis, e.g. `"pp"`, `"gm"`, or `"std"`. Used to
            construct the simple components of the returned basis.

        Returns
        -------
        Basis
        """
        #This default implementation assumes that this basis is simple.
        assert(self.is_simple()), "Incorrectly using a simple-assuming implementation of equivalent()"
        return BuiltinBasis(builtinBasisName, self.dim, sparse=self.sparse)

    #TODO: figure out if we actually need the return value from this function to
    # not have any components...  Maybe jamiolkowski.py needs this?  If it's
    # unnecessary, we can update these doc strings and perhaps TensorProdBasis's
    # implementation:
    def simple_equivalent(self, builtinBasisName=None):
        """
        Create a simple basis *and* one without components (e.g. a
        :class:`TensorProdBasis`, is a simple basis w/components) of the
        builtin type specified whose dimension is compatible with the
        *elements* of this basis.  This function might also be named
        "element_equivalent", as it returns the `builtinBasisName`-analogue
        of the standard basis that this basis's elements are expressed in.

        Parameters
        ----------
        builtinBasisName : str, optional
            The name of the built-in basis to use.  If `None`, then a
            copy of this basis is returned (if it's simple) or this
            basis's name is used to try to construct a simple and
            component-free version of the same builtin-basis type.

        Returns
        -------
        Basis
        """
        #This default implementation assumes that this basis is simple.
        assert(self.is_simple()), "Incorrectly using a simple-assuming implementation of simple_equivalent()"
        if builtinBasisName is None: return self.copy()
        else: return self.equivalent(builtinBasisName)


class LazyBasis(Basis):
    """
    A :class:`Basis` whose labels and elements that are constructed only when at least
    one of them is needed.  This class is also used as a base class for higher-level,
    more specific basis classes.
    """

    def __init__(self, name, longname, dim, size, elshape, real, sparse):
        """
        Creates a new LazyBasis.  Parameters are the same as those to
        :method:`Basis.__init__`.
        """
        self._elements = None        # "natural-shape" elements - can be vecs or matrices
        self._labels = None          # element labels
        self._ellookup = None        # fast element lookup
        super(LazyBasis, self).__init__(name, longname, dim, size, elshape, real, sparse)

    def _lazy_build_elements(self):
        raise NotImplementedError("Derived classes must implement this function!")

    def _lazy_build_labels(self):
        raise NotImplementedError("Derived classes must implement this function!")

    @property
    def ellookup(self):
        """A dictionary mapping basis element labels to the elements themselves"""
        if self._ellookup is None:
            if self._elements is None:
                self._lazy_build_elements()
            if self._labels is None:
                self._lazy_build_labels()
            self._ellookup = {lbl: el for lbl, el in zip(self._labels, self._elements)}
        return self._ellookup

    @property
    def elements(self):
        """The basis elements (sometimes different from the *vectors*)"""
        if self._elements is None:
            self._lazy_build_elements()
        return self._elements

    @property
    def labels(self):
        """The basis labels"""
        if self._labels is None:
            self._lazy_build_labels()
        return self._labels

    def __str__(self):
        if self._labels is None and self.dim > 64:
            return '{} (dim={}), {} elements of shape {} (not computed yet)'.format(
                self.longname, self.dim, self.size, self.elshape)
        else:
            return super(LazyBasis, self).__str__()


class ExplicitBasis(Basis):
    """
    A `Basis` whose elements are specified directly.  All explicit bases are
    simple: their vector space is always taken to be that of the the flattened
    elements.
    """
    Count = 0  # The number of custom bases, used for serialized naming

    def __init__(self, elements, labels=None, name=None, longname=None, real=False, sparse=None):
        '''
        Create a new ExplicitBasis.

        Parameters
        ----------
        elements : iterable
            A list of the elements of this basis.

        labels : iterable, optional
            A list of the labels corresponding to the elements of `elements`.
            If given, `len(labels)` must equal `len(elements)`.

        name : str, optional
            The name of this basis.  If `None`, then a name will be
            automatically generated.

        longname : str, optional
            A more descriptive name for this basis.  If `None`, then the
            short `name` will be used.

        real : bool, optional
            Whether the coefficients in the expression of an arbitrary vector
            as a linear combination of this basis's elements must be real.

        sparse : bool, optional
            Whether the elements of this Basis are stored as sparse matrices or
            vectors.  If `None`, then this is automatically determined by the
            type of the initial object: `elements[0]` (`sparse=False` is used
            when `len(elements) == 0`).
        '''
        if name is None:
            name = 'ExplicitBasis_{}'.format(ExplicitBasis.Count)
            if longname is None: longname = "Auto-named " + name
            ExplicitBasis.Count += 1
        elif longname is None: longname = name

        if labels is None: labels = ["E%d" % k for k in range(len(elements))]
        if (len(labels) != len(elements)):
            raise ValueError("Expected a list of %d labels but got: %s" % (len(elements), str(labels)))

        self.labels = labels
        self.elements = []
        size = len(elements)
        if size == 0:
            elshape = (); dim = 0; sparse = False
        else:
            if sparse is None:
                sparse = _sps.issparse(elements[0]) if len(elements) > 0 else False
            elshape = None
            for el in elements:
                if sparse:
                    if not _sps.issparse(el):
                        el = _sps.csr_matrix(el)  # try to convert to a sparse matrix
                else:
                    if not isinstance(el, _np.ndarray):
                        el = _np.array(el)  # try to convert to a numpy array

                if elshape is None: elshape = el.shape
                else: assert(elshape == el.shape), "Inconsistent element shapes!"
                self.elements.append(el)
            dim = int(_np.product(elshape))
        self.ellookup = {lbl: el for lbl, el in zip(self.labels, self.elements)}  # fast by-label element lookup

        super(ExplicitBasis, self).__init__(name, longname, dim, size, elshape, real, sparse)

    def __hash__(self):
        return hash((self.name, self.dim, self.elshape, self.sparse))  # better?


class BuiltinBasis(LazyBasis):
    """
    A basis that is included within and integrated into pyGSTi, such that it may
    be represented, in many cases, merely by its name.  (In actuality, a
    dimension is also required, but this is often able to be inferred from
    context.)
    """

    def __init__(self, name, dim, sparse=False):
        '''
        Create a new BuiltinBasis object.

        Parameters
        ----------
        name : {"pp", "gm", "std", "qt", "id", "cl", "sv"}
            Name of the basis to be created.

        dim : int
            The dimension of the basis to be created.  Note that this is the
            dimension of the *vectors*, which correspond to flattened elements
            in simple cases.  Thus, a 1-qubit basis would have dimension 2 in
            the state-vector (`name="sv"`) case and dimension 4 when
            constructing a density-matrix basis (e.g. `name="pp"`).

        sparse : bool, optional
            Whether basis elements should be stored as SciPy CSR sparse matrices
            or dense numpy arrays (the default).
        '''
        assert(name in _basisConstructorDict), "Unknown builtin basis name '%s'!" % name
        if sparse is None: sparse = False  # choose dense matrices by default (when sparsity is "unspecified")
        self.cargs = {'dim': dim, 'sparse': sparse}

        longname = _basisConstructorDict[name].longname
        real = _basisConstructorDict[name].real
        size, dim, elshape = _basisConstructorDict[name].sizes(**self.cargs)
        super(BuiltinBasis, self).__init__(name, longname, dim, size, elshape, real, sparse)

        #Check that sparse is True only when elements are *matrices*
        assert(not self.sparse or self.elndim == 2), "`sparse == True` is only allowed for *matrix*-valued bases!"

    def __hash__(self):
        return hash((self.name, self.dim, self.sparse))

    def _lazy_build_elements(self):
        f = _basisConstructorDict[self.name].constructor
        self._elements = _np.array(f(**self.cargs))  # a list of (dense) mxs -> ndarray (possibly sparse in future?)
        assert(len(self._elements) == self.size), "Logic error: wrong number of elements were created!"

    def _lazy_build_labels(self):
        f = _basisConstructorDict[self.name].labeler
        self._labels = f(**self.cargs)

    def __eq__(self, other):
        if isinstance(other, BuiltinBasis):  # then can compare quickly
            return (self.name == other.name) and (self.cargs == other.cargs) and (self.sparse == other.sparse)
        elif isinstance(other, str):
            return self.name == other  # see if other is a string equal to our name
        else:
            return LazyBasis.__eq__(self, other)


class DirectSumBasis(LazyBasis):
    '''
    A basis that is the direct sum of one or more "component" bases.  Elements
    of this basis are the union of the basis elements on each component, each
    embedded into a common block-diagonal structure where each component
    occupies its own block.  Thus, when there is more than one component, a
    `DirectSumBasis` is not a simple basis because the size of its elements
    is larger than the size of its vector space (which corresponds to just
    the diagonal blocks of its elements).
    '''

    def __init__(self, component_bases, name=None, longname=None):
        '''
        Create a new DirectSumBasis - a basis for a space that is the direct-sum
        of the spaces spanned by other "component" bases.

        Parameters
        ----------
        component_bases : iterable
            A list of the component bases.  Each list elements may be either
            a Basis object or a tuple of arguments to :function:`Basis.cast`,
            e.g. `('pp',4)`.

        name : str, optional
            The name of this basis.  If `None`, the names of the component bases
            joined with "+" is used.

        longname : str, optional
            A longer description of this basis.  If `None`, then a long name is
            automatically generated.
        '''
        assert(len(component_bases) > 0), "Must supply at least one component basis"

        self.component_bases = []
        self._vector_elements = None  # vectorized elements: 1D arrays

        for compbasis in component_bases:
            if isinstance(compbasis, Basis):
                self.component_bases.append(compbasis)
            else:
                #compbasis can be a list/tuple of args to Basis.cast, e.g. ('pp',2)
                self.component_bases.append(Basis.cast(*compbasis))

        if name is None:
            name = "+".join([c.name for c in self.component_bases])
        if longname is None:
            longname = "Direct-sum basis with components " + ", ".join(
                [c.name for c in self.component_bases])

        real = all([c.real for c in self.component_bases])
        sparse = all([c.sparse for c in self.component_bases])
        assert(all([c.real == real for c in self.component_bases])), "Inconsistent `real` value among component bases!"
        assert(all([c.sparse == sparse for c in self.component_bases])), "Inconsistent sparsity among component bases!"

        #Init everything but elements and labels & their number/size
        dim = sum([c.dim for c in self.component_bases])
        elndim = len(self.component_bases[0].elshape)
        assert(all([len(c.elshape) == elndim for c in self.component_bases])
               ), "Inconsistent element ndims among component bases!"
        elshape = [sum([c.elshape[k] for c in self.component_bases]) for k in range(elndim)]
        size = sum([c.size for c in self.component_bases])
        super(DirectSumBasis, self).__init__(name, longname, dim, size, elshape, real, sparse)

    def __hash__(self):
        return hash(tuple((hash(comp) for comp in self.component_bases)))

    def _lazy_build_vector_elements(self):
        if self.sparse:
            compMxs = []
        else:
            compMxs = _np.zeros((self.size, self.dim), 'complex')

        i, start = 0, 0
        for compbasis in self.component_bases:
            for lbl, vel in zip(compbasis.labels, compbasis.vector_elements):
                assert(_sps.issparse(vel) == self.sparse), "Inconsistent sparsity!"
                if self.sparse:
                    mx = _sps.lil_matrix((self.dim, 1))
                    mx[start:start + compbasis.dim, 0] = vel
                    compMxs.append(mx)
                else:
                    compMxs[i, start:start + compbasis.dim] = vel
                i += 1
            start += compbasis.dim

        assert(i == self.size)
        self._vector_elements = compMxs

    def _lazy_build_elements(self):
        self._elements = []

        for vel in self.vector_elements:
            vstart = 0
            if self.sparse:  # build block-diagonal sparse mx
                diagBlks = []
                for compbasis in self.component_bases:
                    cs = compbasis.elshape
                    comp_vel = vel[vstart:vstart + compbasis.dim]
                    diagBlks.append(comp_vel.reshape(cs))
                    vstart += compbasis.dim
                el = _sps.block_diag(diagBlks, "csr", 'complex')

            else:
                start = [0] * self.elndim
                el = _np.zeros(self.elshape, 'complex')
                for compbasis in self.component_bases:
                    cs = compbasis.elshape
                    comp_vel = vel[vstart:vstart + compbasis.dim]
                    slc = tuple([slice(start[k], start[k] + cs[k]) for k in range(self.elndim)])
                    el[slc] = comp_vel.reshape(cs)
                    vstart += compbasis.dim
                    for k in range(self.elndim): start[k] += cs[k]

            self._elements.append(el)
        if not self.sparse:  # _elements should be an array rather than a list
            self._elements = _np.array(self._elements)

    def _lazy_build_labels(self):
        self._labels = []
        for i, compbasis in enumerate(self.component_bases):
            for lbl in compbasis.labels:
                self._labels.append(lbl + "/%d" % i)

    def __eq__(self, other):
        otherIsBasis = isinstance(other, DirectSumBasis)
        if not otherIsBasis: return False  # can't be equal to a non-DirectSumBasis
        if len(self.component_bases) != len(other.component_bases): return False
        return all([c1 == c2 for (c1, c2) in zip(self.component_bases, other.component_bases)])

    @property
    def vector_elements(self):
        """ The "vectors" of this basis, always 1D (sparse or dense) arrays. """
        if self._vector_elements is None:
            self._lazy_build_vector_elements()
        return self._vector_elements

    @lru_cache(maxsize=128)
    def get_to_std(self):
        '''
        Retrieve the matrix that transforms a vector from this basis to the
        standard basis of this basis's dimension.

        Returns
        -------
        numpy array or scipy.sparse.lil_matrix
            An array of shape `(dim, size)` where `dim` is the dimension
            of this basis (the length of its vectors) and `size` is the
            size of this basis (its number of vectors).
        '''
        if self.sparse:
            toStd = _sps.lil_matrix((self.dim, self.size), dtype='complex')
        else:
            toStd = _np.zeros((self.dim, self.size), 'complex')

        #use vector elements, which are not just flattened elements
        # (and are computed separately)
        for i, vel in enumerate(self.vector_elements):
            toStd[:, i] = vel
        return toStd

    @lru_cache(maxsize=128)
    def get_to_element_std(self):
        '''
        Get the matrix that transforms vectors in this basis (with length equal
        to the `dim` of this basis) to vectors in the "element space" - that
        is, vectors in the same standard basis that the *elements* of this basis
        are expressed in.

        Returns
        -------
        numpy array
            An array of shape `(element_dim, size)` where `element_dim` is the
            dimension, i.e. size, of the elements of this basis (e.g. 16 if the
            elements are 4x4 matrices) and `size` is the size of this basis (its
            number of vectors).
        '''
        assert(not self.sparse), "get_to_element_std not implemented for sparse mode"
        expanddim = self.elsize  # == _np.product(self.elshape)
        if self.sparse:
            toSimpleStd = _sps.lil_matrix((expanddim, self.size), dtype='complex')
        else:
            toSimpleStd = _np.zeros((expanddim, self.size), 'complex')

        for i, el in enumerate(self.elements):
            if self.sparse:
                vel = _sps.lil_matrix(el.reshape(-1, 1))  # sparse vector == sparse n x 1 matrix
            else:
                vel = el.flatten()
            toSimpleStd[:, i] = vel
        return toSimpleStd

    def equivalent(self, builtinBasisName):
        """
        Create a Basis that is equivalent in structure & dimension to this
        basis but whose simple components (perhaps just this basis itself) is
        of the builtin basis type given by `builtinBasisName`.

        Parameters
        ----------
        builtinBasisName : str
            The name of a builtin basis, e.g. `"pp"`, `"gm"`, or `"std"`. Used to
            construct the simple components of the returned basis.

        Returns
        -------
        DirectSumBasis
        """
        equiv_components = [c.equivalent(builtinBasisName) for c in self.component_bases]
        return DirectSumBasis(equiv_components)

    def simple_equivalent(self, builtinBasisName=None):
        """
        Create a simple basis *and* one without components (e.g. a
        :class:`TensorProdBasis`, is a simple basis w/components) of the
        builtin type specified whose dimension is compatible with the
        *elements* of this basis.  This function might also be named
        "element_equivalent", as it returns the `builtinBasisName`-analogue
        of the standard basis that this basis's elements are expressed in.

        Parameters
        ----------
        builtinBasisName : str, optional
            The name of the built-in basis to use.  If `None`, then a
            copy of this basis is returned (if it's simple) or this
            basis's name is used to try to construct a simple and
            component-free version of the same builtin-basis type.

        Returns
        -------
        Basis
        """
        if builtinBasisName is None:
            builtinBasisName = self.name  # default
            if len(self.component_bases) > 0:
                first_comp_name = self.component_bases[0].name
                if all([c.name == first_comp_name for c in self.component_bases]):
                    builtinBasisName = first_comp_name  # if all components have the same name
        return BuiltinBasis(builtinBasisName, self.elsize, sparse=self.sparse)  # Note: changes dimension


class TensorProdBasis(LazyBasis):
    '''
    A Basis that is the tensor product of one or more "component" bases.

    The elements of a TensorProdBasis consist of all tensor products of
    component basis elements (respecting the order given).  The components
    of a TensorProdBasis must be simple bases so that kronecker products
    can be used to produce the parent basis's elements.

    A TensorProdBasis is a "simple" basis in that its flattened elements
    do correspond to its vectors.
    '''

    def __init__(self, component_bases, name=None, longname=None):
        '''
        Create a new TensorProdBasis whose elements are the tensor products
        of the elements of a set of "component" bases.

        Parameters
        ----------
        component_bases : iterable
            A list of the component bases.  Each list elements may be either
            a Basis object or a tuple of arguments to :function:`Basis.cast`,
            e.g. `('pp',4)`.

        name : str, optional
            The name of this basis.  If `None`, the names of the component bases
            joined with "*" is used.

        longname : str, optional
            A longer description of this basis.  If `None`, then a long name is
            automatically generated.
        '''
        assert(len(component_bases) > 0), "Must supply at least one component basis"

        self.component_bases = []
        for compbasis in component_bases:
            if isinstance(compbasis, Basis):
                self.component_bases.append(compbasis)
            else:
                #compbasis can be a list/tuple of args to Basis.cast, e.g. ('pp',2)
                self.component_bases.append(Basis.cast(*compbasis))

        if name is None:
            name = "*".join([c.name for c in self.component_bases])
        if longname is None:
            longname = "Tensor-product basis with components " + ", ".join(
                [c.name for c in self.component_bases])

        real = all([c.real for c in self.component_bases])
        sparse = all([c.sparse for c in self.component_bases])
        assert(all([c.real == real for c in self.component_bases])), "Inconsistent `real` value among component bases!"
        assert(all([c.sparse == sparse for c in self.component_bases])), "Inconsistent sparsity among component bases!"
        assert(sparse is False), "Sparse matrices are not supported within TensorProductBasis objects yet"

        dim = int(_np.product([c.dim for c in self.component_bases]))
        assert(all([c.is_simple() for c in self.component_bases])), \
            "Components of a tensor product basis must be *simple* (have vector-dimension == size of elements)"
        # because we use the natural representation to take tensor (kronecker) products.
        # Note: this assertion also means dim == product(component_elsizes) == elsize, so basis is *simple*

        size = int(_np.product([c.size for c in self.component_bases]))
        elndim = max([c.elndim for c in self.component_bases])
        elshape = [1] * elndim
        for c in self.component_bases:
            off = elndim - c.elndim
            for k, d in enumerate(c.elshape):
                elshape[k + off] *= d

        super(TensorProdBasis, self).__init__(name, longname, dim, size, elshape, real, sparse)

    def __hash__(self):
        return hash(tuple((hash(comp) for comp in self.component_bases)))

    def _lazy_build_elements(self):
        #LAZY building of elements (in case we never need them)
        compMxs = _np.zeros((self.size,) + self.elshape, 'complex')

        #Take kronecker product of *natural* reps of component-basis elements
        # then reshape to vectors at the end.  This requires that the vector-
        # dimension of the component spaces equals the "natural space" dimension.
        comp_els = [c.elements for c in self.component_bases]
        for i, factors in enumerate(_itertools.product(*comp_els)):
            M = _np.identity(1, 'complex')
            for f in factors:
                M = _np.kron(M, f)
            compMxs[i] = M
        self._elements = compMxs

    def _lazy_build_labels(self):
        self._labels = []
        comp_lbls = [c.labels for c in self.component_bases]
        for i, factor_lbls in enumerate(_itertools.product(*comp_lbls)):
            self._labels.append(''.join(factor_lbls))

    def __eq__(self, other):
        otherIsBasis = isinstance(other, TensorProdBasis)
        if not otherIsBasis: return False  # can't be equal to a non-DirectSumBasis
        if len(self.component_bases) != len(other.component_bases): return False
        return all([c1 == c2 for (c1, c2) in zip(self.component_bases, other.component_bases)])

    def equivalent(self, builtinBasisName):
        """
        Create a Basis that is equivalent in structure & dimension to this
        basis but whose simple components (perhaps just this basis itself) is
        of the builtin basis type given by `builtinBasisName`.

        Parameters
        ----------
        builtinBasisName : str
            The name of a builtin basis, e.g. `"pp"`, `"gm"`, or `"std"`. Used to
            construct the simple components of the returned basis.

        Returns
        -------
        TensorProdBasis
        """
        equiv_components = [c.equivalent(builtinBasisName) for c in self.component_bases]
        return TensorProdBasis(equiv_components)

    def simple_equivalent(self, builtinBasisName=None):
        """
        Create a simple basis *and* one without components (e.g. a
        :class:`TensorProdBasis`, is a simple basis w/components) of the
        builtin type specified whose dimension is compatible with the
        *elements* of this basis.  This function might also be named
        "element_equivalent", as it returns the `builtinBasisName`-analogue
        of the standard basis that this basis's elements are expressed in.

        Parameters
        ----------
        builtinBasisName : str, optional
            The name of the built-in basis to use.  If `None`, then a
            copy of this basis is returned (if it's simple) or this
            basis's name is used to try to construct a simple and
            component-free version of the same builtin-basis type.

        Returns
        -------
        Basis
        """
        if builtinBasisName is None:
            builtinBasisName = self.name  # default
            if len(self.component_bases) > 0:
                first_comp_name = self.component_bases[0].name
                if all([c.name == first_comp_name for c in self.component_bases]):
                    builtinBasisName = first_comp_name  # if all components have the same name
        return BuiltinBasis(builtinBasisName, self.elsize, sparse=self.sparse)


class EmbeddedBasis(LazyBasis):
    '''
    A basis that embeds a basis for a smaller state space within a larger
    state space.

    The elements of an EmbeddedBasis are therefore just embedded versions
    of the elements of the basis that is embedded.
    '''

    @classmethod
    def embed_label(cls, lbl, target_labels):
        """
        Convenience method that gives the EmbeddedBasis label for `lbl`
        without needing to construct the `EmbeddedBasis`.  E.g. "

        Parameters
        ----------
        lbl : str
            Un-embedded basis element label, e.g. `"XX"`.

        target_labels : tuple
            The target state space labels upon which this basis element
            will be embedded, e.g. `(1,2)`

        Returns
        -------
        str
            The embedded-basis-element label as an EmbeddedBasis would
            assign it.  E.g. `"XX:1,2"`.
        """
        return "%s:%s" % (lbl, ",".join(map(str, target_labels)))

    @classmethod
    def unembed_label(cls, lbl, target_labels):
        """Convenience method that performs the reverse of :method:`embed_label` """
        suffix = ":" + ",".join(map(str, target_labels))
        if lbl.endswith(suffix):
            return lbl[:-len(suffix)]
        else:
            raise ValueError("Cannot unembed '%s' - doesn't end in '%s'!" % (lbl, suffix))

    def __init__(self, basis_to_embed, state_space_labels, target_labels, name=None, longname=None):
        '''
        Create a new EmbeddedBasis.

        Parameters
        ----------
        basis_to_embed : Basis
            The basis being embedded.

        state_space_labels : StateSpaceLabels
            An object describing the struture of the entire state space.

        target_labels : list or tuple
            The labels contained in `stateSpaceLabels` which demarcate the
            portions of the state space acted on by `basis_to_embed`.

        name : str, optional
            The name of this basis.  If `None`, the names of `basis_to_embed`
            is joined with ':' characters to the elements of `target_labels`.

        longname : str, optional
            A longer description of this basis.  If `None`, then a long name is
            automatically generated.
        '''
        self.embedded_basis = basis_to_embed
        self.target_labels = target_labels
        self.state_space_labels = state_space_labels

        if name is None:
            name = ':'.join((basis_to_embed.name,) + tuple(map(str, target_labels)))
        if longname is None:
            longname = "Embedded %s basis as %s within %s" % \
                (basis_to_embed.name, ':'.join(map(str, target_labels)), str(state_space_labels))

        real = basis_to_embed.real
        sparse = basis_to_embed.sparse
        dim = state_space_labels.dim
        size = basis_to_embed.size
        elndim = basis_to_embed.elndim

        if elndim == 2:  # a "matrix" basis
            d = int(_np.sqrt(dim))
            assert(d**2 == dim), \
                "Dimension of `state_space_labels` must be a perfect square when embedding a matrix basis"
            elshape = (d, d)
        elif elndim == 1:
            elshape = (dim,)
        else:
            raise ValueError("Can only embed bases with .elndim == 1 or 2 (received %d)!" % elndim)

        super(EmbeddedBasis, self).__init__(name, longname, dim, size, elshape, real, sparse)

    def __hash__(self):
        return hash(tuple(hash(self.embedded_basis), self.target_labels, self.state_space_labels.labels))

    def _lazy_build_elements(self):
        """ Take a dense or sparse basis matrix and embed it. """
        #LAZY building of elements (in case we never need them)
        if self.elndim == 2:  # then use EmbeddedOp to do matrix
            from .operation import StaticDenseOp
            from .operation import EmbeddedOp
            sslbls = self.state_space_labels.copy()
            sslbls.reduce_dims_densitymx_to_state()  # because we're working with basis matrices not gates

            if self.sparse:
                self._elements = []
                for spmx in self.embedded_basis.elements:
                    mxAsOp = StaticDenseOp(spmx.todense(), evotype='statevec')
                    self._elements.append(EmbeddedOp(sslbls, self.target_labels,
                                                     mxAsOp).tosparse())
            else:
                self._elements = _np.zeros((self.size,) + self.elshape, 'complex')
                for i, mx in enumerate(self.embedded_basis.elements):
                    self._elements[i] = EmbeddedOp(sslbls, self.target_labels,
                                                   StaticDenseOp(mx, evotype='statevec')).todense()
        else:
            # we need to perform embedding using vectors rather than matrices - doable, but
            # not needed yet, so defer implementation to later.
            raise NotImplementedError("Embedding *vector*-type bases not implemented yet")

    def _lazy_build_labels(self):
        self._labels = [EmbeddedBasis.embed_label(lbl, self.target_labels)
                        for lbl in self.embedded_basis.labels]

    def __eq__(self, other):
        otherIsBasis = isinstance(other, EmbeddedBasis)
        if not otherIsBasis: return False  # can't be equal to a non-EmbeddedBasis
        if self.target_labels != other.target_labels or self.state_space_labels != other.state_space_labels:
            return False
        return self.embedded_basis == other.embedded_basis

    def equivalent(self, builtinBasisName):
        """
        Create a Basis that is equivalent in structure & dimension to this
        basis but whose simple components (perhaps just this basis itself) is
        of the builtin basis type given by `builtinBasisName`.

        Parameters
        ----------
        builtinBasisName : str
            The name of a builtin basis, e.g. `"pp"`, `"gm"`, or `"std"`. Used to
            construct the simple components of the returned basis.

        Returns
        -------
        EmbeddedBasis
        """
        equiv_embedded = self.embedded_basis.equivalent(builtinBasisName)
        return EmbeddedBasis(equiv_embedded, self.state_space_labels, self.target_labels)

    def simple_equivalent(self, builtinBasisName=None):
        """
        Create a simple basis *and* one without components (e.g. a
        :class:`TensorProdBasis`, is a simple basis w/components) of the
        builtin type specified whose dimension is compatible with the
        *elements* of this basis.  This function might also be named
        "element_equivalent", as it returns the `builtinBasisName`-analogue
        of the standard basis that this basis's elements are expressed in.

        Parameters
        ----------
        builtinBasisName : str, optional
            The name of the built-in basis to use.  If `None`, then a
            copy of this basis is returned (if it's simple) or this
            basis's name is used to try to construct a simple and
            component-free version of the same builtin-basis type.

        Returns
        -------
        Basis
        """
        if builtinBasisName is None:
            builtinBasisName = self.embedded_basis.name  # default
        return BuiltinBasis(builtinBasisName, self.elsize, sparse=self.sparse)
