"""Functions for the construction of new models."""
#***************************************************************************************************
# Copyright 2015, 2019 National Technology & Engineering Solutions of Sandia, LLC (NTESS).
# Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains certain rights
# in this software.
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
# in compliance with the License.  You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0 or in the LICENSE file in the root pyGSTi directory.
#***************************************************************************************************

import numpy as _np
import itertools as _itertools
import collections as _collections
import scipy.linalg as _spl
import scipy.sparse as _sps
import warnings as _warnings


from ..tools import optools as _gt
from ..tools import basistools as _bt
from ..tools import internalgates as _itgs
from ..tools.basisconstructors import sigmax, sigmay, sigmaz
from ..objects import operation as _op
from ..objects import spamvec as _spamvec
from ..objects import povm as _povm
from ..objects import opfactory as _opfactory
from ..objects import explicitmodel as _emdl
from ..objects import gaugegroup as _gg
from ..objects import labeldicts as _ld
from ..objects import qubitgraph as _qubitgraph
from ..objects.localnoisemodel import LocalNoiseModel as _LocalNoiseModel
from ..objects import label as _label
from ..objects.basis import Basis as _Basis
from ..objects.basis import DirectSumBasis as _DirectSumBasis
from ..objects.basis import BuiltinBasis as _BuiltinBasis


#############################################
# Build gates based on "standard" gate names
############################################

def basis_build_vector(vecExpr, basis):
    """
    Build a rho or E vector from an expression.

    Parameters
    ----------
    vecExpr : string
        the expression which determines which vector to build.  Currenlty, only
        integers are allowed, which specify a the vector for the pure state of
        that index.  For example, "1" means return vectorize(``|1><1|``).  The
        index labels the absolute index of the state within the entire state
        space, and is independent of the direct-sum decomposition of density
        matrix space.

    basis : Basis object
        The basis of the returned vector.  Allowed
        values are Matrix-unit (std), Gell-Mann (gm), Pauli-product (pp),
        and Qutrit (qt) (or a custom basis object).

    Returns
    -------
    numpy array
        The vector specified by vecExpr in the desired basis.
    """
    #TODO REMOVE
    #opDim = basis.dim
    #vecInReducedStdBasis = _np.zeros( (opDim,1), 'd' ) # assume index given as vecExpr refers to a
    #                                                     #Hilbert-space state index, so "reduced-std" basis
    #blockDims = [int(_np.sqrt(opDim))] # FIX - get block dims from basis?

    #So far just allow integer prepExpressions that give the index of state (within the state space) that we
    #prep/measure
    try:
        index = int(vecExpr)
    except:
        raise ValueError("Expression must be the index of a state (as a string)")

    #standard basis that has the same direct-sum structure as `basis`:
    std_basis = basis.equivalent('std')
    vecInSimpleStdBasis = _np.zeros(std_basis.elshape, 'd')  # a matrix, but flattened it is our spamvec
    vecInSimpleStdBasis[index, index] = 1.0  # now a matrix with just a single 1 on the diag
    vecInReducedStdBasis = _np.dot(std_basis.get_from_element_std(), vecInSimpleStdBasis.flatten())
    # translates the density matrx / SPAMVec to the std basis with our desired block structure

    #TODO REMOVE
    #start = 0; vecIndex = 0
    #for blockDim in blockDims:
    #    for i in range(start,start+blockDim):
    #        for j in range(start,start+blockDim):
    #            if (i,j) == (index,index):
    #                vecInReducedStdBasis[ vecIndex, 0 ] = 1.0  #set diagonal element of density matrix
    #                break
    #            vecIndex += 1
    #    start += blockDim
    #from ..objects.basis import BuiltinBasis
    #hackstd = BuiltinBasis('std',opDim)
    #return _bt.change_basis(vecInReducedStdBasis, hackstd, basis)

    vec = _bt.change_basis(vecInReducedStdBasis, std_basis, basis)
    return vec.reshape(-1, 1)


def build_vector(stateSpaceDims, stateSpaceLabels, vecExpr, basis="gm"):
    """
    DEPRECATED: use :func:`basis_build_vector` instead.
    """
    _warnings.warn(("This function is deprecated and will be removed in the"
                    " future.  Please use `basis_build_vector` instead."))
    return basis_build_vector(vecExpr, _Basis.cast(basis, stateSpaceDims))


def basis_build_identity_vec(basis):
    """
    Build a the identity vector for a given space and basis.

    Parameters
    ----------
    basis : Basis object
        The basis of the returned vector.  Allowed
        values are Matrix-unit (std), Gell-Mann (gm), Pauli-product (pp),
        and Qutrit (qt) (or a custom basis object).

    Returns
    -------
    numpy array
        The identity vector in the desired basis.
    """
    opDim = basis.dim
    if isinstance(basis, _DirectSumBasis):
        blockDims = [c.dim for c in basis.component_bases]
    else: blockDims = [opDim]

    # assume index given as vecExpr refers to a Hilbert-space state index, so "reduced-std" basis
    vecInReducedStdBasis = _np.zeros((opDim, 1), 'd')

    #set all diagonal elements of density matrix to 1.0 (end result = identity density mx)
    start = 0; vecIndex = 0
    for blockVecDim in blockDims:
        blockDim = int(_np.sqrt(blockVecDim))  # vec -> matrix dim
        for i in range(start, start + blockDim):
            for j in range(start, start + blockDim):
                if i == j: vecInReducedStdBasis[vecIndex, 0] = 1.0  # set diagonal element of density matrix
                vecIndex += 1
        start += blockDim
    return _bt.change_basis(vecInReducedStdBasis, "std", basis)


def build_identity_vec(stateSpaceDims, basis="gm"):
    """
    Build the identity vector given a certain density matrix struture.

    Parameters
    ----------
    stateSpaceDims : list
        A list of integers specifying the dimension of each block
        of a block-diagonal the density matrix.

    basis : str, optional
        The string abbreviation of the basis of the returned vector.  Allowed
        values are Matrix-unit (std), Gell-Mann (gm), Pauli-product (pp),
        and Qutrit (qt).

    Returns
    -------
    numpy array
    """
    return basis_build_identity_vec(_Basis.cast(basis, stateSpaceDims))


def basis_build_operation(stateSpaceLabels, opExpr, basis="gm", parameterization="full"):
    """
    Build an operation object from an expression.

    Parameters
    ----------
    stateSpaceLabels : list of tuples or StateSpaceLabels
        Each tuple corresponds to a block of a density matrix in the standard
        basis (and therefore a component of the direct-sum density matrix
        space). Elements of a tuple are user-defined labels beginning with "L"
        (single level) or "Q" (two-level; qubit) which interpret the
        d-dimensional state space corresponding to a d x d block as a tensor
        product between qubit and single level systems.

    opExpr : string
        expression for the gate to build.  String is first split into parts
        delimited by the colon (:) character, which are composed together to
        create the final gate.  Each part takes on of the allowed forms:

        - I(ssl_0, ...) = identity operation on one or more state space labels
          (ssl_i)
        - X(theta, ssl) = x-rotation by theta radians of qubit labeled by ssl
        - Y(theta, ssl) = y-rotation by theta radians of qubit labeled by ssl
        - Z(theta, ssl) = z-rotation by theta radians of qubit labeled by ssl
        - CX(theta, ssl0, ssl1) = controlled x-rotation by theta radians.  Acts
          on qubit labeled by ssl1 with ssl0 being the control.
        - CY(theta, ssl0, ssl1) = controlled y-rotation by theta radians.  Acts
          on qubit labeled by ssl1 with ssl0 being the control.
        - CZ(theta, ssl0, ssl1) = controlled z-rotation by theta radians.  Acts
          on qubit labeled by ssl1 with ssl0 being the control.
        - CNOT(ssl0, ssl1) = standard controlled-not gate.  Acts on qubit
          labeled by ssl1 with ssl0 being the control.
        - CPHASE(ssl0, ssl1) = standard controlled-phase gate.  Acts on qubit
          labeled by ssl1 with ssl0 being the control.
        - LX(theta, i0, i1) = leakage between states i0 and i1.  Implemented as
          an x-rotation between states with integer indices i0 and i1 followed
          by complete decoherence between the states.

    basis : Basis object
        The basis the returned operation should be represented in.

    parameterization : {"full","TP","static"}, optional
        How to parameterize the resulting gate.

        - "full" = return a FullDenseOp.
        - "TP" = return a TPDenseOp.
        - "static" = return a StaticDenseOp.

    Returns
    -------
    LinearOperator
        A gate object representing the gate given by opExpr in the desired
        basis.
    """
    # opExpr can contain single qubit ops: X(theta) ,Y(theta) ,Z(theta)
    #                      two qubit ops: CNOT
    #                      clevel qubit ops: Leak
    #                      two clevel opts: Flip
    #  each of which is given additional parameters specifying which indices it acts upon
    #dmDim, opDim, blockDims = basis.dim REMOVE
    #fullOpDim = dmDim**2

    #Working with a StateSpaceLabels object gives us access to all the info we'll need later
    sslbls = _ld.StateSpaceLabels(stateSpaceLabels)
    assert(sslbls.dim == basis.dim), \
        "State space labels dim (%s) != basis dim (%s)" % (sslbls.dim, basis.dim)

    # ------------------------------------------------------------------------------------------------------------------
    # -- Helper Functions ----------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    def to_label(lbl):
        """ Convert integer-strings to integers in state space label """
        try: return int(lbl)
        except: return lbl.strip()

    def to_labels(lbls):
        """ Convert integer-strings to integers in state space labels """
        return [to_label(lbl) for lbl in lbls]

    # ------------------------------------------------------------------------------------------------------------------
    # -- End Helper Functions ------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    #print "DB: dim = ",dim, " dmDim = ",dmDim
    opInFinalBasis = None  # what will become the final operation matrix
    # defaultI2P = "all" if parameterization != "linearTP" else "TP"
    #default indices to parameterize (I2P) - used only when
    # creating parameterized gates

    opTermsInFinalBasis = []
    exprTerms = opExpr.split(':')
    for exprTerm in exprTerms:

        l = exprTerm.index('('); r = exprTerm.rindex(')')
        opName = exprTerm[0:l]
        argsStr = exprTerm[l + 1:r]
        args = argsStr.split(',')

        if opName == "I":
            # qubit labels (TODO: what about 'L' labels? -- not sure if they work with this...)
            labels = to_labels(args)
            stateSpaceDim = sslbls.product_dim(labels)
            # *real* 4x4 mx in Pauli-product basis -- still just the identity!
            pp_opMx = _op.StaticDenseOp(_np.identity(stateSpaceDim, 'd'), evotype='densitymx')
            opTermInFinalBasis = _op.EmbeddedDenseOp(sslbls, labels, pp_opMx)

        elif opName == "D":
            # like 'I', but only parameterize the diagonal elements - so can be a depolarization-type map
            raise NotImplementedError("Removed temporarily - need to update using embedded gates")
            # # qubit labels (TODO: what about 'L' labels? -- not sure if they work with this...)
            # labels = to_labels(args)
            # stateSpaceDim = sslbls.product_dim(labels)

            # if parameterization not in ("linear","linearTP"):
            #     raise ValueError("'D' gate only makes sense to use when and parameterization == 'linear'")

            # if defaultI2P == "TP":
            #     # parameterize only the diagonals els after the first
            #     indicesToParameterize = [ (i,i) for i in range(1,stateSpaceDim**2) ]
            # else:
            #     # parameterize only the diagonals els
            #     indicesToParameterize = [ (i,i) for i in range(0,stateSpaceDim**2) ]
            # # *real* 4x4 mx in Pauli-product basis -- still just the identity!
            # pp_opMx = _np.identity(stateSpaceDim**2, 'd')
            # # pp_opMx assumed to be in the Pauli-product basis
            # opTermInFinalBasis = embed_operation(pp_opMx, tuple(labels), indicesToParameterize)

        elif opName in ('X', 'Y', 'Z'):  # single-qubit gate names
            assert(len(args) == 2)  # theta, qubit-index
            theta = eval(args[0], {"__builtins__": None}, {'pi': _np.pi})
            label = to_label(args[1])
            assert(sslbls.labeldims[label] == 4), "%s gate must act on qubits!" % opName

            if opName == 'X': ex = -1j * theta * sigmax / 2
            elif opName == 'Y': ex = -1j * theta * sigmay / 2
            elif opName == 'Z': ex = -1j * theta * sigmaz / 2

            Uop = _spl.expm(ex)  # 2x2 unitary matrix operating on single qubit in [0,1] basis
            # complex 4x4 mx operating on vectorized 1Q densty matrix in std basis
            operationMx = _gt.unitary_to_process_mx(Uop)
            # *real* 4x4 mx in Pauli-product basis -- better for parameterization
            pp_opMx = _op.StaticDenseOp(_bt.change_basis(operationMx, 'std', 'pp'), evotype='densitymx')
            opTermInFinalBasis = _op.EmbeddedDenseOp(sslbls, [label], pp_opMx)

        elif opName == 'N':  # more general single-qubit gate
            assert(len(args) == 5)  # theta, sigmaX-coeff, sigmaY-coeff, sigmaZ-coeff, qubit-index
            theta = eval(args[0], {"__builtins__": None}, {'pi': _np.pi, 'sqrt': _np.sqrt})
            sxCoeff = eval(args[1], {"__builtins__": None}, {'pi': _np.pi, 'sqrt': _np.sqrt})
            syCoeff = eval(args[2], {"__builtins__": None}, {'pi': _np.pi, 'sqrt': _np.sqrt})
            szCoeff = eval(args[3], {"__builtins__": None}, {'pi': _np.pi, 'sqrt': _np.sqrt})
            label = to_label(args[4])
            assert(sslbls.labeldims[label] == 4), "%s gate must act on qubits!" % opName

            ex = -1j * theta * (sxCoeff * sigmax / 2. + syCoeff * sigmay / 2. + szCoeff * sigmaz / 2.)
            Uop = _spl.expm(ex)  # 2x2 unitary matrix operating on single qubit in [0,1] basis
            # complex 4x4 mx operating on vectorized 1Q densty matrix in std basis
            operationMx = _gt.unitary_to_process_mx(Uop)
            # *real* 4x4 mx in Pauli-product basis -- better for parameterization
            pp_opMx = _op.StaticDenseOp(_bt.change_basis(operationMx, 'std', 'pp'), evotype='densitymx')
            opTermInFinalBasis = _op.EmbeddedDenseOp(sslbls, [label], pp_opMx)

        elif opName in ('CX', 'CY', 'CZ', 'CNOT', 'CPHASE'):  # two-qubit gate names

            if opName in ('CX', 'CY', 'CZ'):
                assert(len(args) == 3)  # theta, qubit-label1, qubit-label2
                theta = eval(args[0], {"__builtins__": None}, {'pi': _np.pi})
                label1 = to_label(args[1]); label2 = to_label(args[2])

                if opName == 'CX': ex = -1j * theta * sigmax / 2
                elif opName == 'CY': ex = -1j * theta * sigmay / 2
                elif opName == 'CZ': ex = -1j * theta * sigmaz / 2
                Utarget = _spl.expm(ex)  # 2x2 unitary matrix operating on target qubit

            else:  # opName in ('CNOT','CPHASE')
                assert(len(args) == 2)  # qubit-label1, qubit-label2
                label1 = to_label(args[0]); label2 = to_label(args[1])

                if opName == 'CNOT':
                    Utarget = _np.array([[0, 1],
                                         [1, 0]], 'd')
                elif opName == 'CPHASE':
                    Utarget = _np.array([[1, 0],
                                         [0, -1]], 'd')

            # 4x4 unitary matrix operating on isolated two-qubit space
            Uop = _np.identity(4, 'complex'); Uop[2:, 2:] = Utarget
            assert(sslbls.labeldims[label1] == 4 and sslbls.labeldims[label2] == 4), \
                "%s gate must act on qubits!" % opName

            # complex 16x16 mx operating on vectorized 2Q densty matrix in std basis
            operationMx = _gt.unitary_to_process_mx(Uop)
            # *real* 16x16 mx in Pauli-product basis -- better for parameterization
            pp_opMx = _op.StaticDenseOp(_bt.change_basis(operationMx, 'std', 'pp'), evotype='densitymx')
            opTermInFinalBasis = _op.EmbeddedDenseOp(sslbls, [label1, label2], pp_opMx)

        elif opName == "LX":  # TODO - better way to describe leakage?
            assert(len(args) == 3)  # theta, dmIndex1, dmIndex2 - X rotation between any two density matrix basis states
            theta = eval(args[0], {"__builtins__": None}, {'pi': _np.pi})
            i1 = int(args[1])  # row/column index of a single *state* within the density matrix
            i2 = int(args[2])  # row/column index of a single *state* within the density matrix
            ex = -1j * theta * sigmax / 2
            Uop = _spl.expm(ex)  # 2x2 unitary matrix operating on the i1-th and i2-th states of the state space basis

            opDim = basis.dim
            dmDim = int(_np.sqrt(basis.elsize))  # matrix dim of the "embedding space"
            if isinstance(basis, _DirectSumBasis):
                blockDims = [c.dim for c in basis.component_bases]
            else: blockDims = [opDim]

            Utot = _np.identity(dmDim, 'complex')
            Utot[i1, i1] = Uop[0, 0]
            Utot[i1, i2] = Uop[0, 1]
            Utot[i2, i1] = Uop[1, 0]
            Utot[i2, i2] = Uop[1, 1]
            # dmDim^2 x dmDim^2 mx operating on vectorized total densty matrix
            opTermInStdBasis = _gt.unitary_to_process_mx(Utot)

            # contract [3] to [2, 1]
            embedded_std_basis = _Basis.cast('std', 9)  # [2]
            std_basis = _Basis.cast('std', blockDims)  # std basis w/blockdim structure, i.e. [4,1]
            opTermInReducedStdBasis = _bt.resize_std_mx(opTermInStdBasis, 'contract',
                                                        embedded_std_basis, std_basis)

            opMxInFinalBasis = _bt.change_basis(opTermInReducedStdBasis, std_basis, basis)
            opTermInFinalBasis = _op.FullDenseOp(opMxInFinalBasis, evotype='densitymx')

        else: raise ValueError("Invalid gate name: %s" % opName)

        opTermsInFinalBasis.append(opTermInFinalBasis)

    opInFinalBasis = opTermsInFinalBasis[0] if len(opTermsInFinalBasis) == 1 \
        else _op.ComposedDenseOp(list(reversed(opTermsInFinalBasis)))
    #Note: expressions are listed in "matrix composition order" (reverse for ComposedDenseOp)

    finalOpMx = opInFinalBasis.todense()
    if basis.real:
        assert(_np.linalg.norm(finalOpMx.imag) < 1e-6), "Operation matrix should be real but isn't!"
        finalOpMx = _np.real(finalOpMx)

    if parameterization == "full":
        return _op.FullDenseOp(finalOpMx)
    if parameterization == "static":
        return _op.StaticDenseOp(finalOpMx)
    if parameterization == "TP":
        return _op.TPDenseOp(finalOpMx)

    raise ValueError("Invalid 'parameterization' parameter: "
                     "%s (must by 'full', 'TP', 'static')"
                     % parameterization)


def build_operation(stateSpaceDims, stateSpaceLabels, opExpr, basis="gm", parameterization="full"):
    """
    DEPRECATED: use :func:`basis_build_operation` instead.
    """
    _warnings.warn(("This function is deprecated and will be removed in the"
                    " future.  Please use `basis_build_operation` instead."))
    sslbls = _ld.StateSpaceLabels(stateSpaceLabels, stateSpaceDims)
    return basis_build_operation(sslbls, opExpr, _Basis.cast(basis, stateSpaceDims),
                                 parameterization)


def basis_build_explicit_model(stateSpaceLabels, basis,
                               opLabels, opExpressions,
                               prepLabels=('rho0',), prepExpressions=('0',),
                               effectLabels='standard', effectExpressions='standard',
                               povmLabels='Mdefault', parameterization="full"):
    """
    Build a new Model given lists of operation labels and expressions.

    Parameters
    ----------
    stateSpaceLabels : a list of tuples
        Each tuple corresponds to a block of a density matrix in the standard
        basis (and therefore a component of the direct-sum density matrix
        space). Elements of a tuple are user-defined labels beginning with "L"
        (single level) or "Q" (two-level; qubit) which interpret the
        d-dimensional state space corresponding to a d x d block as a tensor
        product between qubit and single level systems.

    basis : Basis object
        The source and destination basis, respectively.  Allowed
        values are Matrix-unit (std), Gell-Mann (gm), Pauli-product (pp),
        and Qutrit (qt) (or a custom basis object).

    opLabels : list of strings
       A list of labels for each created gate in the final model.  To
        conform with text file parsing conventions these names should begin
        with a capital G and can be followed by any number of lowercase
        characters, numbers, or the underscore character.

    opExpressions : list of strings
        A list of gate expressions, each corresponding to a operation label in
        opLabels, which determine what operation each gate performs (see
        documentation for :meth:`build_operation`).

    prepLabels : list of string, optional
        A list of labels for each created state preparation in the final
        model.  To conform with conventions these labels should begin with
        "rho".

    prepExpressions : list of strings, optional
        A list of vector expressions for each state preparation vector (see
        documentation for :meth:`build_vector`).

    effectLabels : list, optional
        If `povmLabels` is a string, then this is just a list of the effect
        (outcome) labels for the single POVM.  If `povmLabels` is a tuple,
        then `effectLabels` must be a list of lists of effect labels, each
        list corresponding to a POVM.  If set to the special string `"standard"`
        then the length-n binary strings are used when the state space consists
        of n qubits (e.g. `"000"`, `"001"`, ... `"111"` for 3 qubits) and
        the labels `"0"`, `"1"`, ... `"<dim>"` are used, where `<dim>`
        is the dimension of the state space, in all non-qubit cases.

    effectExpressions : list, optional
        A list or list-of-lists of (string) vector expressions for each POVM
        effect vector (see documentation for :meth:`build_vector`).  Expressions
        correspond to labels in `effectLabels`.  If set to the special string
        `"standard"`, then the expressions `"0"`, `"1"`, ... `"<dim>"` are used,
        where `<dim>` is the dimension of the state space.

    povmLabels : list or string, optional
        A list of POVM labels, or a single (string) label.  In the latter case,
        only a single POVM is created and the format of `effectLabels` and
        `effectExpressions` is simplified (see above).

    parameterization : {"full","TP","static"}, optional
        How to parameterize the gates of the resulting Model (see
        documentation for :meth:`build_operation`).

    Returns
    -------
    Model
        The created model.
    """
    #defP = "TP" if (parameterization in ("TP","linearTP")) else "full"
    stateSpaceLabels = _ld.StateSpaceLabels(stateSpaceLabels)

    ret = _emdl.ExplicitOpModel(stateSpaceLabels, basis.copy(), default_param=parameterization)
    #prep_prefix="rho", effect_prefix="E", gate_prefix="G")

    for label, rhoExpr in zip(prepLabels, prepExpressions):
        vec = basis_build_vector(rhoExpr, basis)
        if parameterization == "full":
            ret.preps[label] = _spamvec.FullSPAMVec(vec, 'densitymx', 'prep')
        elif parameterization == "TP":
            ret.preps[label] = _spamvec.TPSPAMVec(vec)  # only a "prep"
        elif parameterization == "static":
            ret.preps[label] = _spamvec.StaticSPAMVec(vec, 'densitymx', 'prep')
        else:
            raise ValueError("Invalid parameterization: %s" % parameterization)

    if isinstance(povmLabels, str):
        povmLabels = [povmLabels]
        effectLabels = [effectLabels]
        effectExpressions = [effectExpressions]

    dmDim = int(_np.sqrt(basis.dim))  # "densitymx" evotype assumed... FIX?
    for povmLbl, ELbls, EExprs in zip(povmLabels,
                                      effectLabels, effectExpressions):
        effects = []

        if ELbls == "standard":
            qubit_dim = 4  # 2 if evotype in ('statevec', 'stabilizer') else 4
            if stateSpaceLabels.num_tensor_prod_blocks() == 1 and \
               all([ldim == qubit_dim for ldim in stateSpaceLabels.tensor_product_block_dims(0)]):
                # a single tensor product block comprised of qubits: '000', '001', etc.
                nQubits = len(stateSpaceLabels.tensor_product_block_dims(0))
                ELbls = [''.join(t) for t in _itertools.product(('0', '1'), repeat=nQubits)]
            else:
                ELbls = list(map(str, range(dmDim)))  # standard = 0,1,...,dmDim
        if EExprs == "standard":
            EExprs = list(map(str, range(dmDim)))  # standard = 0,1,...,dmDim

        for label, EExpr in zip(ELbls, EExprs):
            evec = basis_build_vector(EExpr, basis)
            if parameterization == "static":
                effects.append((label, _spamvec.StaticSPAMVec(evec, 'densitymx', 'effect')))
            else:
                effects.append((label, _spamvec.FullSPAMVec(evec, 'densitymx', 'effect')))

        if len(effects) > 0:  # don't add POVMs with 0 effects
            if parameterization == "TP":
                ret.povms[povmLbl] = _povm.TPPOVM(effects)
            else:
                ret.povms[povmLbl] = _povm.UnconstrainedPOVM(effects)

    for (opLabel, opExpr) in zip(opLabels, opExpressions):
        ret.operations[opLabel] = basis_build_operation(stateSpaceLabels,
                                                        opExpr, basis, parameterization)

    if parameterization == "full":
        ret.default_gauge_group = _gg.FullGaugeGroup(ret.dim)
    elif parameterization == "TP":
        ret.default_gauge_group = _gg.TPGaugeGroup(ret.dim)
    else:
        ret.default_gauge_group = None  # assume no gauge freedom

    return ret


def build_explicit_model(stateSpaceLabels,
                         opLabels, opExpressions,
                         prepLabels=('rho0',), prepExpressions=('0',),
                         effectLabels='standard', effectExpressions='standard',
                         povmLabels='Mdefault', basis="auto", parameterization="full"):
    """
    Build a new Model given lists of labels and expressions.

    Parameters
    ----------
    stateSpaceLabels : a list of tuples
        Each tuple corresponds to a block of a density matrix in the standard
        basis (and therefore a component of the direct-sum density matrix
        space). Elements of a tuple are user-defined labels beginning with "L"
        (single level) or "Q" (two-level; qubit) which interpret the
        d-dimensional state space corresponding to a d x d block as a tensor
        product between qubit and single level systems.

    opLabels : list of strings
       A list of labels for each created gate in the final model.  To
        conform with text file parsing conventions these names should begin
        with a capital G and can be followed by any number of lowercase
        characters, numbers, or the underscore character.

    opExpressions : list of strings
        A list of gate expressions, each corresponding to a operation label in
        opLabels, which determine what operation each gate performs (see
        documentation for :meth:`build_operation`).

    prepLabels : list of string
        A list of labels for each created state preparation in the final
        model.  To conform with conventions these labels should begin with
        "rho".

    prepExpressions : list of strings
        A list of vector expressions for each state preparation vector (see
        documentation for :meth:`build_vector`).

    effectLabels : list, optional
        If `povmLabels` is a string, then this is just a list of the effect
        (outcome) labels for the single POVM.  If `povmLabels` is a tuple,
        then `effectLabels` must be a list of lists of effect labels, each
        list corresponding to a POVM.  If set to the special string `"standard"`
        then the length-n binary strings are used when the state space consists
        of n qubits (e.g. `"000"`, `"001"`, ... `"111"` for 3 qubits) and
        the labels `"0"`, `"1"`, ... `"<dim>"` are used, where `<dim>`
        is the dimension of the state space, in all non-qubit cases.

    effectExpressions : list, optional
        A list or list-of-lists of (string) vector expressions for each POVM
        effect vector (see documentation for :meth:`build_vector`).  Expressions
        correspond to labels in `effectLabels`.  If set to the special string
        `"standard"`, then the expressions `"0"`, `"1"`, ... `"<dim>"` are used,
        where `<dim>` is the dimension of the state space.

    povmLabels : list or string, optional
        A list of POVM labels, or a single (string) label.  In the latter case,
        only a single POVM is created and the format of `effectLabels` and
        `effectExpressions` is simplified (see above).

    basis : {'gm','pp','std','qt','auto'}, optional
        the basis of the matrices in the returned Model

        - "std" = operation matrix operates on density mx expressed as sum of matrix
          units
        - "gm"  = operation matrix operates on dentity mx expressed as sum of
          normalized Gell-Mann matrices
        - "pp"  = operation matrix operates on density mx expresses as sum of
          tensor-product of Pauli matrices
        - "qt"  = operation matrix operates on density mx expressed as sum of
          Qutrit basis matrices
        - "auto" = "pp" if possible (integer num of qubits), "qt" if density
          matrix dim == 3, and "gm" otherwise.

    parameterization : {"full","TP"}, optional
        How to parameterize the gates of the resulting Model (see
        documentation for :meth:`build_operation`).

    Returns
    -------
    Model
        The created model.
    """

    #Note: so far, all allowed `parameterization` values => densitymx evotype
    stateSpaceLabels = _ld.StateSpaceLabels(stateSpaceLabels, evotype="densitymx")
    stateSpaceDim = stateSpaceLabels.dim
    # Note: what about stateSpaceLabels.tpb_dims?

    if basis == "auto":
        if _np.isclose(_np.log2(stateSpaceDim) / 2,
                       round(_np.log2(stateSpaceDim) / 2)):
            basis = "pp"
        elif stateSpaceDim == 9:
            basis = "qt"
        else: basis = "gm"

    return basis_build_explicit_model(stateSpaceLabels,
                                      _Basis.cast(basis, stateSpaceLabels),
                                      opLabels, opExpressions,
                                      prepLabels, prepExpressions,
                                      effectLabels, effectExpressions,
                                      povmLabels, parameterization=parameterization)


def build_explicit_alias_model(mdl_primitives, alias_dict):
    """
    Creates a new model by composing the gates of an existing `Model`,
    `mdl_primitives`, according to a dictionary of `Circuit`s, `alias_dict`.
    The keys of `alias_dict` are the operation labels of the returned `Model`.
    SPAM vectors are unaltered, and simply copied from `mdl_primitives`.

    Parameters
    ----------
    mdl_primitives : Model
        A Model containing the "primitive" gates (those used to compose
        the gates of the returned model).

    alias_dict : dictionary
        A dictionary whose keys are strings and values are Circuit objects
        specifying sequences of primitive gates.  Each key,value pair specifies
        the composition rule for a creating a gate in the returned model.

    Returns
    -------
    Model
        A model whose gates are compositions of primitive gates and whose
        spam operations are the same as those of `mdl_primitives`.
    """
    mdl_new = mdl_primitives.copy()
    for gl in mdl_primitives.operations.keys():
        del mdl_new.operations[gl]  # remove all gates from mdl_new

    for gl, opstr in alias_dict.items():
        mdl_new.operations[gl] = mdl_primitives.product(opstr)
        #Creates fully parameterized gates by default...
    return mdl_new


def build_localnoise_model(nQubits, gate_names, nonstd_gate_unitaries=None, custom_gates=None,
                           availability=None, qubit_labels=None, geometry="line", parameterization='static',
                           evotype="auto", sim_type="auto", on_construction_error='raise',
                           independent_gates=False, ensure_composed_gates=False, globalIdle=None):
    """
    Creates a "standard" n-qubit local-noise model, usually of ideal gates.

    The returned model is "standard", in that the following standard gate
    names may be specified as elements to `gate_names` without the need to
    supply their corresponding unitaries (as one must when calling
    the constructor directly):

    - 'Gi' : the 1Q idle operation
    - 'Gx','Gy','Gz' : 1Q pi/2 rotations
    - 'Gxpi','Gypi','Gzpi' : 1Q pi rotations
    - 'Gh' : Hadamard
    - 'Gp' : phase
    - 'Gcphase','Gcnot','Gswap' : standard 2Q gates

    Furthermore, if additional "non-standard" gates are needed,
    they are specified by their *unitary* gate action, even if
    the final model propagates density matrices (as opposed
    to state vectors).

    Parameters
    ----------
    nQubits : int
        The total number of qubits.

    gate_names : list
        A list of string-type gate names (e.g. `"Gx"`) either taken from
        the list of builtin "standard" gate names given above or from the
        keys of `nonstd_gate_unitaries`.  These are the typically 1- and 2-qubit
        gates that are repeatedly embedded (based on `availability`) to form
        the resulting model.

    nonstd_gate_unitaries : dict, optional
        A dictionary of numpy arrays which specifies the unitary gate action
        of the gate names given by the dictionary's keys.  As an advanced
        behavior, a unitary-matrix-returning function which takes a single
        argument - a tuple of label arguments - may be given instead of a
        single matrix to create an operation *factory* which allows
        continuously-parameterized gates.  This function must also return
        an empty/dummy unitary when `None` is given as it's argument.

    custom_gates : dict, optional
        A dictionary that associates with gate labels
        :class:`LinearOperator`, :class:`OpFactory`, or `numpy.ndarray`
        objects.  These objects describe the full action of the gate or
        primitive-layer they're labeled by (so if the model represents
        states by density matrices these objects are superoperators, not
        unitaries), and override any standard construction based on builtin
        gate names or `nonstd_gate_unitaries`.  Keys of this dictionary may
        be string-type gate *names*, which will be embedded according to
        `availability`, or labels that include target qubits,
        e.g. `("Gx",0)`, which override this default embedding behavior.
        Furthermore, :class:`OpFactory` objects may be used in place of
        `LinearOperator` objects to allow the evaluation of labels with
        arguments.

    availability : dict, optional
        A dictionary whose keys are the same gate names as in
        `gatedict` and whose values are lists of qubit-label-tuples.  Each
        qubit-label-tuple must have length equal to the number of qubits
        the corresponding gate acts upon, and causes that gate to be
        embedded to act on the specified qubits.  For example,
        `{ 'Gx': [(0,),(1,),(2,)], 'Gcnot': [(0,1),(1,2)] }` would cause
        the `1-qubit `'Gx'`-gate to be embedded three times, acting on qubits
        0, 1, and 2, and the 2-qubit `'Gcnot'`-gate to be embedded twice,
        acting on qubits 0 & 1 and 1 & 2.  Instead of a list of tuples,
        values of `availability` may take the special values:

        - `"all-permutations"` and `"all-combinations"` equate to all possible
        permutations and combinations of the appropriate number of qubit labels
        (deterined by the gate's dimension).
        - `"all-edges"` equates to all the vertices, for 1Q gates, and all the
        edges, for 2Q gates of the graphy given by `geometry`.
        - `"arbitrary"` or `"*"` means that the corresponding gate can be placed
        on any target qubits via an :class:`EmbeddingOpFactory` (uses less
        memory but slower than `"all-permutations"`.

        If a gate name (a key of `gatedict`) is not present in `availability`,
        the default is `"all-edges"`.

    qubit_labels : tuple, optional
        The circuit-line labels for each of the qubits, which can be integers
        and/or strings.  Must be of length `nQubits`.  If None, then the
        integers from 0 to `nQubits-1` are used.

    geometry : {"line","ring","grid","torus"} or QubitGraph, optional
        The type of connectivity among the qubits, specifying a graph used to
        define neighbor relationships.  Alternatively, a :class:`QubitGraph`
        object with `qubit_labels` as the node labels may be passed directly.
        This argument is only used as a convenient way of specifying gate
        availability (edge connections are used for gates whose availability
        is unspecified by `availability` or whose value there is `"all-edges"`).

    parameterization : {"full", "TP", "CPTP", "H+S", "S", "static", "H+S terms",
                        "H+S clifford terms", "clifford"}
        The type of parameterizaton to use for each gate value before it is
        embedded. See :method:`Model.set_all_parameterizations` for more
        details.

    evotype : {"auto","densitymx","statevec","stabilizer","svterm","cterm"}
        The evolution type.  Often this is determined by the choice of
        `parameterization` and can be left as `"auto"`, which prefers
        `"densitymx"` (full density matrix evolution) when possible. In some
        cases, however, you may want to specify this manually.  For instance,
        if you give unitary maps instead of superoperators in `gatedict`
        you'll want to set this to `"statevec"`.

    sim_type : {"auto", "matrix", "map", "termorder:<N>"}
        The simulation method used to compute predicted probabilities for the
        resulting :class:`Model`.  Usually `"auto"` is fine, the default for
        each `evotype` is usually what you want.  Setting this to something
        else is expert-level tuning.

    on_construction_error : {'raise','warn',ignore'}
        What to do when the creation of a gate with the given
        `parameterization` fails.  Usually you'll want to `"raise"` the error.
        In some cases, for example when converting as many gates as you can
        into `parameterization="clifford"` gates, `"warn"` or even `"ignore"`
        may be useful.

    independent_gates : bool, optional
        Whether gates are allowed independent local noise or not.  If False,
        then all gates with the same name (e.g. "Gx") will have the *same*
        (local) noise (e.g. an overrotation by 1 degree), and the
        `operation_bks['gates']` dictionary contains a single key per gate
        name.  If True, then gates with the same name acting on different
        qubits may have different local noise, and so the
        `operation_bks['gates']` dictionary contains a key for each gate
         available gate placement.

    ensure_composed_gates : bool, optional
        If True then the elements of the `operation_bks['gates']` will always
        be either :class:`ComposedDenseOp` (if `sim_type == "matrix"`) or
        :class:`ComposedOp` (othewise) objects.  The purpose of this is to
        facilitate modifying the gate operations after the model is created.
        If False, then the appropriately parameterized gate objects (often
        dense gates) are used directly.

    globalIdle : LinearOperator, optional
        A global idle operation, which is performed once at the beginning
        of every circuit layer.  If `None`, no such operation is performed.
        If a 1-qubit operator is given and `nQubits > 1` the global idle
        is the parallel application of this operator on each qubit line.
        Otherwise the given operator must act on all `nQubits` qubits.


    Returns
    -------
    Model
        A model with `"rho0"` prep, `"Mdefault"` POVM, and gates labeled by
        gate name (keys of `gatedict`) and qubit labels (from within
        `availability`).  For instance, the operation label for the `"Gx"` gate on
        qubit 2 might be `Label("Gx",1)`.
    """
    return _LocalNoiseModel.build_from_parameterization(
        nQubits, gate_names, nonstd_gate_unitaries, custom_gates,
        availability, qubit_labels, geometry, parameterization, evotype,
        sim_type, on_construction_error, independent_gates,
        ensure_composed_gates, globalIdle)


def build_crosstalk_free_model(nQubits, gate_names, error_rates, nonstd_gate_unitaries=None, custom_gates=None,
                               availability=None, qubit_labels=None, geometry="line", parameterization='auto',
                               evotype="auto", sim_type="auto", on_construction_error='raise',
                               independent_gates=False, ensure_composed_gates=False):
    """
    Create a n-qubit "crosstalk-free" model: one whose operations only act
    nontrivially on their target qubits.

    Parameters
    ----------
    nQubits : int
        The total number of qubits.

    gate_names : list
        A list of string-type gate names (e.g. `"Gx"`) either taken from
        the list of builtin "standard" gate names or from the
        keys of `nonstd_gate_unitaries`.  These are the typically 1- and 2-qubit
        gates that are repeatedly embedded (based on `availability`) to form
        the resulting model.

    error_rates : dict
        A dictionary whose keys are gate names (e.g. `"Gx"`) and whose values
        determine the type and amount of error placed on that gate.  Values can
        be floats, tuples or "error-dictionaries".  A float specifies a rate of
        uniform depolarization, and a tuple of floats specifies Pauli-stochastic
        error rates for each of the non-trivial Paulis (so a 3-tuple would be
        expected for a 1Q gate and a 15-tuple for a 2Q gate).  Finally, an error
        dictionary is a `dict` with keys that specify types of errors and values
        that specify rates.  Keys are `(termType, basisLabel)` tuples, where
        `termType` can be `"H"` (Hamiltonian), `"S"` (Stochastic), or `"A"`
        (Affine), and `basisLabel` is a string of I, X, Y, or Z to describe a
        Pauli basis element appropriate for the gate (i.e. having the same
        number of letters as there are qubits in the gate).  For example, you
        could specify a 0.01-radian Z-rotation error and 0.05 rate of Pauli-
        stochastic X errors on a 1-qubit gate by using the error dictionary:
        `{('H','Z'): 0.01, ('S','X'): 0.05}`.  In addition to the gate names,
        the special values `"prep"`, `"povm"`, and `"idle"` may be used as
        keys of `error_rates` to specify the error on the state preparation,
        measurement, and global idle, respectively.

    nonstd_gate_unitaries : dict, optional
        A dictionary of numpy arrays which specifies the unitary gate action
        of the gate names given by the dictionary's keys.

    custom_gates : dict, optional
        A dictionary that associates with gate labels
        :class:`LinearOperator`, :class:`OpFactory`, or `numpy.ndarray`
        objects.  These objects override any other behavior for constructing
        their designated operations (e.g. from `error_rates` or
        `nonstd_gate_unitaries`).  Keys of this dictionary may
        be string-type gate *names* or labels that include target qubits.

    availability : dict, optional
        A dictionary whose keys are the same gate names as in
        `gatedict` and whose values are lists of qubit-label-tuples.  Each
        qubit-label-tuple must have length equal to the number of qubits
        the corresponding gate acts upon, and causes that gate to be
        embedded to act on the specified qubits.  For example,
        `{ 'Gx': [(0,),(1,),(2,)], 'Gcnot': [(0,1),(1,2)] }` would cause
        the `1-qubit `'Gx'`-gate to be embedded three times, acting on qubits
        0, 1, and 2, and the 2-qubit `'Gcnot'`-gate to be embedded twice,
        acting on qubits 0 & 1 and 1 & 2.  Instead of a list of tuples,
        values of `availability` may take the special values:

        - `"all-permutations"` and `"all-combinations"` equate to all possible
        permutations and combinations of the appropriate number of qubit labels
        (deterined by the gate's dimension).
        - `"all-edges"` equates to all the vertices, for 1Q gates, and all the
        edges, for 2Q gates of the graphy given by `geometry`.
        - `"arbitrary"` or `"*"` means that the corresponding gate can be placed
        on any target qubits via an :class:`EmbeddingOpFactory` (uses less
        memory but slower than `"all-permutations"`.

        If a gate name (a key of `gatedict`) is not present in `availability`,
        the default is `"all-edges"`.

    qubit_labels : tuple, optional
        The circuit-line labels for each of the qubits, which can be integers
        and/or strings.  Must be of length `nQubits`.  If None, then the
        integers from 0 to `nQubits-1` are used.

    geometry : {"line","ring","grid","torus"} or QubitGraph, optional
        The type of connectivity among the qubits, specifying a graph used to
        define neighbor relationships.  Alternatively, a :class:`QubitGraph`
        object with `qubit_labels` as the node labels may be passed directly.
        This argument is only used as a convenient way of specifying gate
        availability (edge connections are used for gates whose availability
        is unspecified by `availability` or whose value there is `"all-edges"`).

    parameterization : "auto"
        This argument is for future expansion and currently must be set to `"auto"`.

    evotype : {"auto","densitymx","statevec","stabilizer","svterm","cterm"}
        The evolution type.  If "auto" is specified, "densitymx" is used.

    sim_type : {"auto", "matrix", "map", "termorder:<N>"}
        The simulation method used to compute predicted probabilities for the
        resulting :class:`Model`.  Usually `"auto"` is fine, the default for
        each `evotype` is usually what you want.  Setting this to something
        else is expert-level tuning.

    on_construction_error : {'raise','warn',ignore'}
        What to do when the creation of a gate with the given
        `parameterization` fails.  Usually you'll want to `"raise"` the error.
        In some cases, for example when converting as many gates as you can
        into `parameterization="clifford"` gates, `"warn"` or even `"ignore"`
        may be useful.

    independent_gates : bool, optional
        Whether gates are allowed independent local noise or not.  If False,
        then all gates with the same name (e.g. "Gx") will have the *same*
        (local) noise (e.g. an overrotation by 1 degree), and the
        `operation_bks['gates']` dictionary contains a single key per gate
        name.  If True, then gates with the same name acting on different
        qubits may have different local noise, and so the
        `operation_bks['gates']` dictionary contains a key for each gate
         available gate placement.

    ensure_composed_gates : bool, optional
        If True then the elements of the `operation_bks['gates']` will always
        be either :class:`ComposedDenseOp` (if `sim_type == "matrix"`) or
        :class:`ComposedOp` (othewise) objects.  The purpose of this is to
        facilitate modifying the gate operations after the model is created.
        If False, then the appropriately parameterized gate objects (often
        dense gates) are used directly.

    Returns
    -------
    Model
        A model with `"rho0"` prep, `"Mdefault"` POVM, and gates labeled by
        gate name (keys of `gatedict`) and qubit labels (from within
        `availability`).  For instance, the operation label for the `"Gx"` gate on
        qubit 2 might be `Label("Gx",1)`.
    """
    # E.g. error_rates could == {'Gx': {('H','X'): 0.1, ('S','Y'): 0.2} } # Lindblad, b/c val is dict
    #                        or {'Gx': 0.1 } # Depolarization b/c val is a float
    #                        or {'Gx': (0.1,0.2,0.2) } # Pauli-Stochastic b/c val is a tuple

    if parameterization != "auto":
        raise NotImplementedError(("Future versions of pyGSTi may allow you to specify a non-automatic "
                                   "parameterization - for instance building DepolarizeOp objects "
                                   "instead of LindbladOps for depolarization errors."))

    if custom_gates is None: custom_gates = {}
    if nonstd_gate_unitaries is None: nonstd_gate_unitaries = {}
    std_unitaries = _itgs.get_standard_gatename_unitaries()

    if evotype == "auto":
        evotype = "densitymx"  # FUTURE: do something more sophisticated?

    def _parameterization_from_errgendict(errs):  # TODO: consolidate with same method in nqnoiseconstruction.py
        paramtypes = []
        if any([nm[0] == 'H' for nm in errs]): paramtypes.append('H')
        if any([nm[0] == 'S' for nm in errs]): paramtypes.append('S')
        if any([nm[0] == 'A' for nm in errs]): paramtypes.append('A')
        if any([nm[0] == 'S' and isinstance(nm, tuple) and len(nm) == 3 for nm in errs]):
            # parameterization must be "CPTP" if there are any ('S',b1,b2) keys
            parameterization = "CPTP"
        else:
            parameterization = '+'.join(paramtypes)
        return parameterization

    def create_gate(name, gateMx):
        """Create a gate object corresponding to a name with appropriate parameterization"""
        errs = error_rates.get(name, None)

        if isinstance(gateMx, _opfactory.OpFactory):
            factory = gateMx
            gateMx = _np.identity(factory.dim, 'd')  # we'll prefix with factory
        else:
            factory = None

        if errs is None:
            if factory: return factory  # gateMx is just identity
            else: return _op.StaticDenseOp(gateMx, evotype)

        elif isinstance(errs, dict):
            parameterization = _parameterization_from_errgendict(errs)
            _, _, nonham_mode, param_mode = _op.LindbladOp.decomp_paramtype(parameterization)
            gate_dim = gateMx.shape[0]
            basis = _BuiltinBasis('pp', gate_dim)  # assume we're always given basis els in a Pauli basis?
            errgen = _op.LindbladErrorgen(gate_dim, errs, basis, param_mode,
                                          nonham_mode, truncate=False, mxBasis="pp", evotype=evotype)
            gate = _op.LindbladOp(gateMx, errgen, dense_rep=not _sps.issparse(gateMx))

            #OLD TODO REMOVE
            #gate = _op.LindbladOp.from_operation_matrix(gateMx, gateMx, ham_basis="pp", nonham_basis="pp",
            #                                            param_mode=param_mode, nonham_mode=nonham_mode,
            #                                            truncate=True, mxBasis="pp", evotype=evotype)
            #gate.set_error_rates(errs)

        elif isinstance(errs, tuple):
            #tuple should have length 4^k-1 for a k-qubit gate (with dimension 4^k)
            assert(len(errs) + 1 == gateMx.shape[0]), \
                "Invalid number of Pauli stochastic rates: got %d but expected %d" % (len(errs), gateMx.shape[0] - 1)
            gate = _op.StochasticNoiseOp(len(errs) + 1, "pp", evotype, initial_rates=errs)

        elif isinstance(errs, float):
            #Make a depolarization operator:
            gate = _op.LindbladOp.from_operation_matrix(gateMx, ham_basis=None, nonham_basis="pp",
                                                        param_mode="depol", nonham_mode="diagonal",
                                                        truncate=True, mxBasis="pp", evotype=evotype)
            perPauliRate = errs / len(gate.errorgen.other_basis.labels)
            errdict = {('S', bl): perPauliRate for bl in gate.errorgen.other_basis.labels[1:]}  # skip identity el
            gate.set_error_rates(errdict)

        else:
            raise ValueError("Invalid `error_rates` value: %s (type %s)" % (str(errs), type(errs)))

        if factory:
            #just add errors after whatever factory produces.
            gate = _opfactory.ComposedOpFactory([factory, gate])

        return gate

    gatedict = _collections.OrderedDict()
    for name in gate_names:
        if name in custom_gates:
            gatedict[name] = custom_gates[name]
        else:
            U = nonstd_gate_unitaries.get(name, std_unitaries.get(name, None))
            if U is None: raise KeyError("'%s' gate unitary needs to be provided by `nonstd_gate_unitaries` arg" % name)
            if callable(U):  # then assume a function: args -> unitary
                U0 = U(None)  # U fns must return a sample unitary when passed None to get size.
                gateMx = _opfactory.UnitaryOpFactory(U, U0.shape[0], evotype=evotype)
            else:
                if evotype in ("densitymx", "svterm", "cterm"):
                    gateMx = _bt.change_basis(_gt.unitary_to_process_mx(U), "std", "pp")
                else:  # we just store the unitaries
                    raise NotImplementedError("Setting error rates on unitaries isn't implemented yet")
                    #assert(evotype in ("statevec", "stabilizer")), "Invalid evotype: %s" % evotype
                    #gateMx = U
            gatedict[name] = create_gate(name, gateMx)

    #Check for any error rates specific to sslbls that we missed, e.g. ('Gx',0)
    for errlbl, errdict in error_rates.items():
        if errlbl not in gate_names and _label.Label(errlbl).sslbls is not None:
            errlbl = _label.Label(errlbl)
            name = errlbl.name
            U = nonstd_gate_unitaries.get(name, std_unitaries.get(name, None))
            if U is None: raise KeyError("'%s' gate unitary needs to be provided by `nonstd_gate_unitaries` arg" % name)
            if evotype in ("densitymx", "svterm", "cterm"):
                gateMx = _bt.change_basis(_gt.unitary_to_process_mx(U), "std", "pp")
            else:  # we just store the unitaries
                raise NotImplementedError("Setting error rates on unitaries isn't implemented yet")
            gatedict[errlbl] = create_gate(errlbl, gateMx)

    #Add anything from custom_gates directly if it wasn't added already (allows overrides of, e.g. ('Gx',0))
    for lbl, gate in custom_gates.items():
        if lbl not in gate_names:
            gatedict[lbl] = gate

    if 'idle' in error_rates:
        idleOp = create_gate('idle', _np.identity(4))  # 1-qubit idle op
    else:
        idleOp = None

    prep_layers = {}
    if 'prep' in error_rates:
        assert(isinstance(error_rates['prep'], (dict, float))), "error_rates['prep'] can only be a dict or float!"
        rho_base1Q = _spamvec.ComputationalSPAMVec([0], evotype, 'prep')
        prep1Q = _spamvec.LindbladSPAMVec(rho_base1Q, create_gate('prep', _np.identity(4)), 'prep')
        prep_factors = [prep1Q.copy() for i in range(nQubits)] if independent_gates else [prep1Q] * nQubits
        prep_layers['rho0'] = _spamvec.TensorProdSPAMVec('prep', prep_factors)
    else:
        prep_layers['rho0'] = _spamvec.ComputationalSPAMVec([0] * nQubits, evotype, 'prep')

    povm_layers = {}
    if 'povm' in error_rates:
        assert(isinstance(error_rates['povm'], (dict, float))), "error_rates['povm'] can only be a dict or float!"
        Mdefault_base1Q = _povm.ComputationalBasisPOVM(1, evotype)
        povm1Q = _povm.LindbladPOVM(create_gate('povm', _np.identity(4)), Mdefault_base1Q, "pp")
        povm_factors = [povm1Q.copy() for i in range(nQubits)] if independent_gates else [povm1Q] * nQubits
        povm_layers['Mdefault'] = _povm.TensorProdPOVM(povm_factors)
    else:
        povm_layers['Mdefault'] = _povm.ComputationalBasisPOVM(nQubits, evotype)

    return _LocalNoiseModel(nQubits, gatedict, prep_layers, povm_layers, availability, qubit_labels,
                            geometry, evotype, sim_type, on_construction_error,
                            independent_gates, ensure_composed_gates, global_idle=idleOp)
