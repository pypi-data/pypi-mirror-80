""" Defines the SimplifierHelper class and supporting functionality."""
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
from .label import Label as _Label


class SimplifierHelper(object):
    """
    Defines the minimal interface for performing :class:`Circuit` "compiling"
    (pre-processing for forward simulators, which only deal with preps, ops,
    and effects) needed by :class:`Model`.

    To simplify a circuit a `Model` doesn't, for instance, need to know *all*
    possible state preparation labels, as a dict of preparation operations
    would provide - it only needs a function to check if a given value is a
    viable state-preparation label.
    """

    def __init__(self, sslbls):
        self.sslbls = sslbls  # the state space labels for the model this helper is associated with


class BasicSimplifierHelper(SimplifierHelper):
    """
    Performs the work of a :class:`SimplifierHelper` using user-supplied lists
    """

    def __init__(self, preplbls, povmlbls, instrumentlbls,
                 povm_effect_lbls, instrument_member_lbls, sslbls):
        """
        Create a new BasicSimplifierHelper.

        preplbls, povmlbls, instrumentlbls, povm_effect_lbls,
        instrument_member_lbls : list
            Lists of all the state-preparation, POVM, instrument,
            POVM-effect, and instrument-member labels of a model.
        """
        self.preplbls = preplbls
        self.povmlbls = povmlbls
        self.instrumentlbls = instrumentlbls
        self.povm_effect_lbls = povm_effect_lbls
        self.instrument_member_lbls = instrument_member_lbls
        super().__init__(sslbls)

    def is_prep_lbl(self, lbl):
        """Whether `lbl` is a valid state prep label (returns boolean)"""
        return lbl in self.preplbls

    def is_povm_lbl(self, lbl):
        """Whether `lbl` is a valid POVM label (returns boolean)"""
        return lbl in self.povmlbls

    def is_instrument_lbl(self, lbl):
        """Whether `lbl` is a valid instrument label (returns boolean)"""
        return lbl in self.instrumentlbls

    def get_default_prep_lbl(self):
        """
        Gets the default state prep label (used when a circuit
        is specified without one).  Returns `None` if there is
        no default and one *must* be specified.

        Returns
        -------
        Label or None
        """
        return self.preplbls[0] \
            if len(self.preplbls) == 1 else None

    def get_default_povm_lbl(self, sslbls):
        """
        Gets the default POVM label (used when a circuit
        is specified without one).  Returns `None` if there is
        no default and one *must* be specified.

        Returns
        -------
        Label or None
        """
        assert(sslbls is None or sslbls == ('*',))
        return self.povmlbls[0] \
            if len(self.povmlbls) == 1 else None

    def has_preps(self):
        """Whether this model contains any state preps (returns boolean)"""
        return len(self.preplbls) > 0

    def has_povms(self):
        """Whether this model contains any POVM (returns boolean)"""
        return len(self.povmlbls) > 0

    def get_effect_labels_for_povm(self, povm_lbl):
        """
        Gets the effect labels corresponding to the possible outcomes of POVM
        label `povm_lbl`.

        Parameters
        ----------
        pomv_lbl : Label

        Returns
        -------
        list
            A list of strings which label the POVM outcomes.
        """
        return self.povm_effect_lbls[povm_lbl]

    def get_member_labels_for_instrument(self, inst_lbl):
        """
        Gets the member labels corresponding to the possible outcomes of
        the instrument labeled by `inst_lbl`.

        Parameters
        ----------
        inst_lbl : Label

        Returns
        -------
        list
            A list of strings which label the instrument members.
        """
        return self.instrument_member_lbls[inst_lbl]


class MemberDictSimplifierHelper(SimplifierHelper):
    """
    Performs the work of a :class:`SimplifierHelper` using a set of
    `OrderedMemberDict` objects, such as those contained in an
    :class:`ExplicitOpModel`.
    """

    def __init__(self, preps, povms, instruments, sslbls):
        """
        Create a new MemberDictSimplifierHelper.

        Parameters
        ----------
        preps, povms, instruments : OrderedMemberDict
        """
        self.preps = preps
        self.povms = povms
        self.instruments = instruments
        super().__init__(sslbls)

    def is_prep_lbl(self, lbl):
        """Whether `lbl` is a valid state prep label (returns boolean)"""
        return lbl in self.preps

    def is_povm_lbl(self, lbl):
        """Whether `lbl` is a valid POVM label (returns boolean)"""
        return lbl in self.povms

    def is_instrument_lbl(self, lbl):
        """Whether `lbl` is a valid instrument label (returns boolean)"""
        return lbl in self.instruments

    def get_default_prep_lbl(self):
        """
        Gets the default state prep label (used when a circuit
        is specified without one).  Returns `None` if there is
        no default and one *must* be specified.

        Returns
        -------
        Label or None
        """
        return tuple(self.preps.keys())[0] \
            if len(self.preps) == 1 else None

    def get_default_povm_lbl(self, sslbls):
        """
        Gets the default POVM label (used when a circuit
        is specified without one).  Returns `None` if there is
        no default and one *must* be specified.

        Returns
        -------
        Label or None
        """
        assert(sslbls in (None, ('*',)) or (len(self.sslbls.labels) == 1 and self.sslbls.labels[0] == sslbls)), \
            "No default POVM label for sslbls=%s (less than *all* the state space labels, which are %s)" % (
                str(sslbls), str(self.sslbls.labels))
        return tuple(self.povms.keys())[0] \
            if len(self.povms) == 1 else None

    def has_preps(self):
        """Whether this model contains any state preps (returns boolean)"""
        return len(self.preps) > 0

    def has_povms(self):
        """Whether this model contains any POVM (returns boolean)"""
        return len(self.povms) > 0

    def get_effect_labels_for_povm(self, povm_lbl):
        """
        Gets the effect labels corresponding to the possible outcomes of POVM
        label `povm_lbl`.

        Parameters
        ----------
        pomv_lbl : Label

        Returns
        -------
        list
            A list of strings which label the POVM outcomes.
        """
        return tuple(self.povms[povm_lbl].keys())

    def get_member_labels_for_instrument(self, inst_lbl):
        """
        Gets the member labels corresponding to the possible outcomes of
        the instrument labeled by `inst_lbl`.

        Parameters
        ----------
        inst_lbl : Label

        Returns
        -------
        list
            A list of strings which label the instrument members.
        """
        return tuple(self.instruments[inst_lbl].keys())


class MemberDictDictSimplifierHelper(SimplifierHelper):
    """
    Performs the work of a :class:`SimplifierHelper` using a set of
    dictionaries of `OrderedMemberDict` objects, such as those
    contained in an :class:`ImplicitOpModel`.
    """

    def __init__(self, prep_blks, povm_blks, instrument_blks, sslbls):
        """
        Create a new MemberDictDictSimplifierHelper.

        Parameters
        ----------
        prep_blks, povm_blks, instrument_blks : dict of OrderedMemberDict
        """
        self.prep_blks = prep_blks
        self.povm_blks = povm_blks
        self.instrument_blks = instrument_blks
        super().__init__(sslbls)

    def is_prep_lbl(self, lbl):
        """Whether `lbl` is a valid state prep label (returns boolean)"""
        return any([(lbl in prepdict) for prepdict in self.prep_blks.values()])

    def is_povm_lbl(self, lbl):
        """Whether `lbl` is a valid POVM label (returns boolean)"""
        return any([(lbl in povmdict) for povmdict in self.povm_blks.values()])

    def is_instrument_lbl(self, lbl):
        """Whether `lbl` is a valid instrument label (returns boolean)"""
        return any([(lbl in idict) for idict in self.instrument_blks.values()])

    def get_default_prep_lbl(self):
        """
        Gets the default state prep label (used when a circuit
        is specified without one).  Returns `None` if there is
        no default and one *must* be specified.

        Returns
        -------
        Label or None
        """
        npreps = sum([len(prepdict) for prepdict in self.prep_blks.values()])
        if npreps == 1:
            for prepdict in self.prep_blks.values():
                if len(prepdict) > 0:
                    return tuple(prepdict.keys())[0]
            assert(False), "Logic error: one prepdict should have had length > 0!"
        else:
            return None

    def get_default_povm_lbl(self, sslbls):
        """
        Gets the default POVM label (used when a circuit
        is specified without one).  Returns `None` if there is
        no default and one *must* be specified.

        Returns
        -------
        Label or None
        """
        npovms = sum([len(povmdict) for povmdict in self.povm_blks.values()])
        if npovms == 1:
            for povmdict in self.povm_blks.values():
                if len(povmdict) > 0:
                    povmName = tuple(povmdict.keys())[0]  # assume this is a POVM for all of model's sslbls
                    if len(self.sslbls.labels) == 1 and self.sslbls.labels[0] == sslbls or sslbls == ('*',):
                        return _Label(povmName)  # because sslbls == all of model's sslbls
                    else:
                        return _Label(povmName, sslbls)
            assert(False), "Logic error: one povmdict should have had length > 0!"
        else:
            return None

    def has_preps(self):
        """Whether this model contains any state preps (returns boolean)"""
        return any([(len(prepdict) > 0) for prepdict in self.prep_blks.values()])

    def has_povms(self):
        """Whether this model contains any POVM (returns boolean)"""
        return any([(len(povmdict) > 0) for povmdict in self.povm_blks.values()])

    def get_effect_labels_for_povm(self, povm_lbl):
        """
        Gets the effect labels corresponding to the possible outcomes of POVM
        label `povm_lbl`.

        Parameters
        ----------
        pomv_lbl : Label

        Returns
        -------
        list
            A list of strings which label the POVM outcomes.
        """
        for povmdict in self.povm_blks.values():
            if povm_lbl in povmdict:
                return tuple(povmdict[povm_lbl].keys())
            if isinstance(povm_lbl, _Label) and povm_lbl.name in povmdict:
                return tuple(_povm.MarginalizedPOVM(povmdict[povm_lbl.name], self.sslbls, povm_lbl.sslbls).keys())

        raise KeyError("No POVM labeled %s!" % str(povm_lbl))

    def get_member_labels_for_instrument(self, inst_lbl):
        """
        Gets the member labels corresponding to the possible outcomes of
        the instrument labeled by `inst_lbl`.

        Parameters
        ----------
        inst_lbl : Label

        Returns
        -------
        list
            A list of strings which label the instrument members.
        """
        for idict in self.instrument_blks.values():
            if inst_lbl in idict:
                return tuple(idict[inst_lbl].keys())
        raise KeyError("No instrument labeled %s!" % inst_lbl)


class ImplicitModelSimplifierHelper(MemberDictDictSimplifierHelper):
    """ Performs the work of a "Simplifier Helper" using user-supplied dicts """

    def __init__(self, implicitModel):
        """
        Create a new ImplicitModelSimplifierHelper.

        Parameters
        ----------
        implicitModel : ImplicitOpModel
        """
        super(ImplicitModelSimplifierHelper, self).__init__(
            implicitModel.prep_blks, implicitModel.povm_blks, implicitModel.instrument_blks,
            implicitModel.state_space_labels)
