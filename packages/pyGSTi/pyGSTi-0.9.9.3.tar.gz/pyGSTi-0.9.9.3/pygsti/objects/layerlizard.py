""" Defines the LayerLizard class and supporting functionality."""
#***************************************************************************************************
# Copyright 2015, 2019 National Technology & Engineering Solutions of Sandia, LLC (NTESS).
# Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains certain rights
# in this software.
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
# in compliance with the License.  You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0 or in the LICENSE file in the root pyGSTi directory.
#***************************************************************************************************


import numpy as _np
import scipy as _scipy
import itertools as _itertools
import collections as _collections
import warnings as _warnings
import time as _time
import uuid as _uuid
import bisect as _bisect
import copy as _copy

from ..tools import matrixtools as _mt
from ..tools import optools as _gt
from ..tools import slicetools as _slct
from ..tools import likelihoodfns as _lf
from ..tools import jamiolkowski as _jt
from ..tools import basistools as _bt
from ..tools import listtools as _lt
from ..tools import symplectic as _symp

from . import modelmember as _gm
from . import circuit as _cir
from . import operation as _op
from . import spamvec as _sv
from . import povm as _povm
from . import instrument as _instrument
from . import labeldicts as _ld
from . import gaugegroup as _gg
from . import matrixforwardsim as _matrixfwdsim
from . import mapforwardsim as _mapfwdsim
from . import termforwardsim as _termfwdsim
from . import explicitcalc as _explicitcalc

from .verbosityprinter import VerbosityPrinter as _VerbosityPrinter
from .basis import Basis as _Basis
from .label import Label as _Label, CircuitLabel as _CircuitLabel


class LayerLizard(object):
    """
    Helper class for interfacing a Model and a forward simulator
    (which just deals with *simplified* operations).  Can be thought
    of as a "server" of simplified operations for a forward simulator
    which pieces together layer operations from components.
    """

    def __init__(self, model):
        """
        Create a new LayerLizard.

        Parameters
        ----------
        model : Model
            The "parent" model for this layer lizard.
        """
        self.model = model
        self.opcache = {}  # a cache of operators, which should get initialized by from_vector calls

    def set_opcache(self, cache_dict, v):
        """ TODO: docstring - v is optional paramvec to init ops"""
        self.opcache = cache_dict
        if v is not None:
            for _, obj in self.opcache.items():
                obj.from_vector(v[obj.gpindices])  # , close, nodirty)

    #Helper functions for derived classes:
    def get_circuitlabel_op(self, circuitlbl, dense):
        """
        A helper function for derived classes, used for processing
        :class:`CircuitLabel` labels (which encapsulate sub-circuits
        repeated some integer number of times).

        This method build an operator for `circuitlbl` by creating a composed-op
        (using either :class:`ComposedOp` or :class:`ComposedDenseOp` depending
        on the value of `dense`) of the sub-circuit that is exponentiated (using
        :class:`ExponentiatedOp`) to the power `circuitlbl.reps`.

        Parameters
        ----------
        circuitlbl : CircuitLabel
            The (sub-circuit)^power to create an operator for.

        dense : boolean
            Whether a dense composed-op should be created (see above).

        Returns
        -------
        LinearOperator
        """
        Composed = _op.ComposedDenseOp if dense else _op.ComposedOp
        if len(circuitlbl.components) != 1:  # works for 0 components too
            subCircuitOp = Composed([self.get_operation(l) for l in circuitlbl.components],
                                    dim=self.model.dim, evotype=self.model._evotype)
        else:
            subCircuitOp = self.get_operation(circuitlbl.components[0])
        if circuitlbl.reps != 1:
            #finalOp = Composed([subCircuitOp]*circuitlbl.reps,
            #                   dim=self.model.dim, evotype=self.model._evotype)
            finalOp = _op.ExponentiatedOp(subCircuitOp, circuitlbl.reps, evotype=self.model._evotype)
        else:
            finalOp = subCircuitOp
        return finalOp


class ExplicitLayerLizard(LayerLizard):
    """
    This layer lizard (see :class:`LayerLizard`) only serves up layer
    operations it have been explicitly provided upon initialization.
    """

    def __init__(self, preps, operations, povms, instruments, model):
        """
        Creates a new ExplicitLayerLizard.

        Parameters
        ----------
        preps, ops, effects : OrderedMemberDict
            Dictionaries of simplified layer operations available for
            serving to a forwared simulator.

        model : Model
            The model associated with the simplified operations.
        """

        simplified_effects = _collections.OrderedDict()
        for povm_lbl, povm in povms.items():
            for k, e in povm.simplify_effects(povm_lbl).items():
                simplified_effects[k] = e

        simplified_ops = _collections.OrderedDict()
        for k, g in operations.items(): simplified_ops[k] = g
        for inst_lbl, inst in instruments.items():
            for k, g in inst.simplify_operations(inst_lbl).items():
                simplified_ops[k] = g

        #Note: maybe copies not needed here?
        self.preps = {k: v for k, v in preps.items()}  # no compilation needed
        self.operations = {k: v for k, v in operations.items()}  # shallow copy
        self.povms = {k: v for k, v in povms.items()}
        self.instruments = {k: v for k, v in instruments.items()}

        self.simpleops = simplified_ops
        self.effects = simplified_effects
        super(ExplicitLayerLizard, self).__init__(model)

    def get_evotype(self):
        """
        Return the evolution type of the operations being served.

        Returns
        -------
        str
        """
        return self.model._evotype

    def get_prep(self, layerlbl):
        """
        Return the (simplified) preparation layer operator given by `layerlbl`.

        Returns
        -------
        LinearOperator
        """
        return self.preps[layerlbl]

    def get_effect(self, layerlbl):
        """
        Return the (simplified) POVM effect layer operator given by `layerlbl`.

        Returns
        -------
        LinearOperator
        """
        return self.effects[layerlbl]

    def get_operation(self, layerlbl):
        """
        Return the (simplified) layer operation given by `layerlbl`.

        Returns
        -------
        LinearOperator
        """
        if isinstance(layerlbl, _CircuitLabel):
            dense = bool(self.model._sim_type == "matrix")  # whether dense matrix gates should be created
            return self.get_circuitlabel_op(layerlbl, dense)
        else:
            return self.simpleops[layerlbl]

    def from_vector(self, v, close=False, nodirty=False):
        """
        Re-initialize the simplified operators from model-parameter-vector `v`.

        Parameters
        ----------
        v : numpy.ndarray
            A vector of parameters for `Model` associated with this layer lizard.
        """
        for _, obj in _itertools.chain(self.preps.items(),
                                       self.effects.items(),
                                       self.simpleops.items(),
                                       self.opcache.items()):
            obj.from_vector(v[obj.gpindices], close, nodirty)


class ImplicitLayerLizard(LayerLizard):
    """
    This layer lizard (see :class:`LayerLizard`) is used as a base class for
    objects which serve up layer operations for implicit models (and so provide
    logic for how to construct layer operations from model components).
    """

    def __init__(self, prep_blks, op_blks, povm_blks, instrument_blks, model):
        """
        Creates a new ExplicitLayerLizard.

        Parameters
        ----------
        prep_blks, op_blks, povm_blks, instrument_blks : dict
            Dictionaries of :class:`OrderedMemberDict` objects, one per
            "category" of operators.  These are stored and used
            to build layer operations for serving to a forwared simulator.

        model : Model
            The model associated with the operations.
        """
        #Create dicts of all "POVMName_EffectName" effects, one dict per category
        # This simplification also ensures all gpindices are pointing to the parent model's paramvec
        simplified_effect_blks = _collections.OrderedDict()
        for povm_dict_lbl, povmdict in povm_blks.items():
            simplified_effect_blks[povm_dict_lbl] = _collections.OrderedDict(
                [(k, e) for povm_lbl, povm in povmdict.items()
                 for k, e in povm.simplify_effects(povm_lbl).items()])

        simplified_op_blks = op_blks.copy()  # no compilation needed
        for inst_dict_lbl, instdict in instrument_blks.items():
            if inst_dict_lbl not in simplified_op_blks:  # only create when needed
                simplified_op_blks[inst_dict_lbl] = _collections.OrderedDict()
            for inst_lbl, inst in instdict.items():
                for k, g in inst.simplify_operations(inst_lbl).items():
                    simplified_op_blks[inst_dict_lbl][k] = g

        self.prep_blks = prep_blks.copy()  # no compilation needed
        self.operation_blks = op_blks.copy()  # shallow copy of normal dict
        self.povm_blks = povm_blks.copy()
        self.instrument_blks = instrument_blks.copy()

        self.simpleop_blks = simplified_op_blks
        self.effect_blks = simplified_effect_blks
        super(ImplicitLayerLizard, self).__init__(model)

    def get_prep(self, layerlbl):
        """
        Return the (simplified) preparation layer operator given by `layerlbl`.

        Returns
        -------
        LinearOperator
        """
        raise NotImplementedError("ImplicitLayerLizard-derived classes must implement `get_preps`")

    def get_effect(self, layerlbl):
        """
        Return the (simplified) POVM effect layer operator given by `layerlbl`.

        Returns
        -------
        LinearOperator
        """
        raise NotImplementedError("ImplicitLayerLizard-derived classes must implement `get_effect`")

    def get_operation(self, layerlbl):
        """
        Return the (simplified) layer operation given by `layerlbl`.

        Returns
        -------
        LinearOperator
        """
        raise NotImplementedError("ImplicitLayerLizard-derived classes must implement `get_operation`")

    def get_evotype(self):
        """
        Return the evolution type of the operations being served.

        Returns
        -------
        str
        """
        return self.model._evotype

    def from_vector(self, v, close=False, nodirty=False):
        """
        Re-initialize the simplified operators from model-parameter-vector `v`.

        Parameters
        ----------
        v : numpy.ndarray
            A vector of parameters for `Model` associated with this layer lizard.
        """
        for _, objdict in _itertools.chain(self.prep_blks.items(),
                                           self.effect_blks.items(),
                                           self.simpleop_blks.items()):
            for _, obj in objdict.items():
                obj.from_vector(v[obj.gpindices], close, nodirty)

        for _, obj in self.opcache.items():
            obj.from_vector(v[obj.gpindices], close, nodirty)
