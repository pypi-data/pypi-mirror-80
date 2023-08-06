""" Defines the Label class """
#***************************************************************************************************
# Copyright 2015, 2019 National Technology & Engineering Solutions of Sandia, LLC (NTESS).
# Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains certain rights
# in this software.
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
# in compliance with the License.  You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0 or in the LICENSE file in the root pyGSTi directory.
#***************************************************************************************************

import numbers as _numbers
import itertools as _itertools

import os
import inspect
debug_record = {}


class Label(object):
    """
    A label consisting of a string along with a tuple of
    integers or sector-names specifying which qubits, or
    more generally, parts of the Hilbert space that is
    acted upon by an object so-labeled.
    """

    # this is just an abstract base class for isinstance checking.
    # actual labels will either be LabelTup or LabelStr instances,
    # depending on whether the tuple of sector names exists or not.
    # (the reason for separate classes is for hashing speed)

    def __new__(cls, name, stateSpaceLabels=None, time=None, args=None):
        """
        Creates a new Model-item label, which is divided into a simple string
        label and a tuple specifying the part of the Hilbert space upon which the
        item acts (often just qubit indices).

        Parameters
        ----------
        name : str
            The item name. E.g., 'CNOT' or 'H'.

        stateSpaceLabels : list or tuple, optional
            A list or tuple that identifies which sectors/parts of the Hilbert
            space is acted upon.  In many cases, this is a list of integers
            specifying the qubits on which a gate acts, when the ordering in the
            list defines the 'direction' of the gate.  If something other than
            a list or tuple is passed, a single-element tuple is created
            containing the passed object.

        time : float
            The time at which this label occurs (can be relative or absolute)

        args : iterable of hashable types, optional
            A list of "arguments" for this label.  Having arguments makes the
            Label even more resemble a function call, and supplies parameters
            for the object (often a gate or layer operation) being labeled that
            are fixed at circuit-creation time (i.e. are not optimized over).
            For example, the angle of a continuously-variable X-rotation gate
            could be an argument of a gate label, and one might create a label:
            `Label('Gx', (0,), args=(pi/3,))`
        """
        #print("Label.__new__ with name=", name, "sslbls=", stateSpaceLabels, "t=", time, "args=", args)
        if isinstance(name, Label) and stateSpaceLabels is None:
            return name  # Note: Labels are immutable, so no need to copy

        if not isinstance(name, str) and stateSpaceLabels is None \
           and isinstance(name, (tuple, list)):

            #We're being asked to initialize from a non-string with no
            # stateSpaceLabels, explicitly given.  `name` could either be:
            # 0) an empty tuple: () -> LabelTupTup with *no* subLabels.
            # 1) a (name, ssl0, ssl1, ...) tuple -> LabelTup
            # 2) a (subLabel1_tup, subLabel2_tup, ...) tuple -> LabelTupTup if
            #     length > 1 otherwise just initialize from subLabel1_tup.
            # Note: subLabelX_tup could also be identified as a Label object
            #       (even a LabelStr)

            if len(name) == 0:
                if args: return LabelTupTupWithArgs.init((), time, args)
                else: return LabelTupTup.init((), time)
            elif isinstance(name[0], (tuple, list, Label)):
                if len(name) > 1:
                    if args: return LabelTupTupWithArgs.init(name, time, args)
                    else: return LabelTupTup.init(name, time)
                else:
                    return Label(name[0], time=time, args=args)
            else:
                #Case when stateSpaceLabels, etc, are given after name in a single tuple
                tup = name
                name = tup[0]
                tup_args = []; stateSpaceLabels = []
                next_is_arg = False
                next_is_time = False
                for x in tup[1:]:
                    if next_is_arg:
                        next_is_arg = False
                        tup_args.append(x); continue
                    if next_is_time:
                        next_is_time = False
                        time = x; continue

                    if isinstance(x, str):
                        if x.startswith(';'):
                            assert(args is None), "Cannot supply args in tuple when `args` is given!"
                            if x == ';':
                                next_is_arg = True
                            else:
                                tup_args.append(x[1:])
                            continue
                        if x.startswith('!'):
                            assert(time is None), "Cannot supply time in tuple when `time` is given!"
                            if x == '!':
                                next_is_time = True
                            else:
                                time = float(x[1:])
                            continue
                    stateSpaceLabels.append(x)
                args = tup_args if len(tup_args) > 0 else None
                stateSpaceLabels = tuple(stateSpaceLabels)  # needed for () and (None,) comparison below

        if time is None:
            time = 0.0  # for non-TupTup labels not setting a time is equivalent to setting it to 0.0

        #print(" -> preproc with name=", name, "sslbls=", stateSpaceLabels, "t=", time, "args=", args)
        if stateSpaceLabels is None or stateSpaceLabels in ((), (None,)):
            if args:
                return LabelTupWithArgs.init(name, (), time, args)  # just use empty sslbls
            else:
                return LabelStr.init(name, time)

        else:
            if args: return LabelTupWithArgs.init(name, stateSpaceLabels, time, args)
            else: return LabelTup.init(name, stateSpaceLabels, time)

    def depth(self):
        return 1  # most labels are depth=1

    @property
    def reps(self):
        return 1  # most labels have only reps==1

    def expand_subcircuits(self):
        """
        Expand any sub-circuits within this label and return a resulting list
        of component labels which doesn't include any :class:`CircuitLabel`
        labels.  This effectively expands any "boxes" or "exponentiation"
        within this label.

        Returns
        -------
        tuple
            A tuple of component Labels (none of which should be
            :class:`CircuitLabel`s).
        """
        return (self,)  # most labels just expand to themselves


class LabelTup(Label, tuple):
    """
    A label consisting of a string along with a tuple of
    integers or sector-names specifying which qubits, or
    more generally, parts of the Hilbert space that is
    acted upon by an object so-labeled.
    """

    @classmethod
    def init(cls, name, stateSpaceLabels, time=0.0):
        """
        Creates a new Model-item label, which is divided into a simple string
        label and a tuple specifying the part of the Hilbert space upon which the
        item acts (often just qubit indices).

        Parameters
        ----------
        name : str
            The item name. E.g., 'CNOT' or 'H'.

        stateSpaceLabels : list or tuple
            A list or tuple that identifies which sectors/parts of the Hilbert
            space is acted upon.  In many cases, this is a list of integers
            specifying the qubits on which a gate acts, when the ordering in the
            list defines the 'direction' of the gate.  If something other than
            a list or tuple is passed, a single-element tuple is created
            containing the passed object.

        time : float
            The time at which this label occurs (can be relative or absolute)
        """

        #Type checking
        assert(isinstance(name, str)), "`name` must be a string, but it's '%s'" % str(name)
        assert(stateSpaceLabels is not None), "LabelTup must be initialized with non-None state-space labels"
        assert(isinstance(time, float)), "`time` must be a floating point value, received: " + str(time)
        if not isinstance(stateSpaceLabels, (tuple, list)):
            stateSpaceLabels = (stateSpaceLabels,)
        for ssl in stateSpaceLabels:
            assert(isinstance(ssl, str) or isinstance(ssl, _numbers.Integral)), \
                "State space label '%s' must be a string or integer!" % str(ssl)

        #Try to convert integer-strings to ints (for parsing from files...)
        integerized_sslbls = []
        for ssl in stateSpaceLabels:
            try: integerized_sslbls.append(int(ssl))
            except: integerized_sslbls.append(ssl)

        # Regardless of whether the input is a list, tuple, or int, the state space labels
        # (qubits) that the item/gate acts on are stored as a tuple (because tuples are immutable).
        sslbls = tuple(integerized_sslbls)
        tup = (name,) + sslbls
        return cls.__new__(cls, tup, time)

    def __new__(cls, tup, time=0.0):
        ret = tuple.__new__(cls, tup)  # creates a LabelTup object using tuple's __new__
        ret.time = time
        return ret

    @property
    def name(self):
        return self[0]

    @property
    def sslbls(self):
        if len(self) > 1:
            return self[1:]
        else: return None

    @property
    def args(self):
        return ()

    @property
    def components(self):
        return (self,)  # just a single "sub-label" component

    @property
    def qubits(self):  # Used in Circuit
        """An alias for sslbls, since commonly these are just qubit indices"""
        return self.sslbls

    @property
    def number_of_qubits(self):  # Used in Circuit
        return len(self.sslbls) if (self.sslbls is not None) else None

    def has_prefix(self, prefix, typ="all"):
        """
        Whether this label has the given `prefix`.  Usually used to test whether
        the label names a given type.

        Parameters
        ----------
        prefix : str
            The prefix to check for.

        typ : {"any","all"}
            Whether, when there are multiple parts to the label, the prefix
            must occur in any or all of the parts.

        Returns
        -------
        bool
        """
        return self.name.startswith(prefix)

    def map_state_space_labels(self, mapper):
        """
        Return a copy of this Label with all of the state-space-labels
        (often just qubit labels) updated according to a mapping function.

        For example, calling this function with `mapper = {0: 1, 1: 3}`
        on the Label "Gcnot:0:1" would return "Gcnot:1:3".

        Parameters
        ----------
        mapper : dict or function
            A dictionary whose keys are the existing state-space-label values
            and whose value are the new labels, or a function which takes a
            single (existing label) argument and returns a new label.

        Returns
        -------
        Label
        """
        if isinstance(mapper, dict):
            mapped_sslbls = [mapper[sslbl] for sslbl in self.sslbls]
        else:  # assume mapper is callable
            mapped_sslbls = [mapper(sslbl) for sslbl in self.sslbls]
        return Label(self.name, mapped_sslbls)

    #OLD
    #def __iter__(self):
    #    return self.tup.__iter__()

    #OLD
    #def __iter__(self):
    #    """ Iterate over the name + state space labels """
    #    # Note: tuple(.) uses __iter__ to construct tuple rep.
    #    yield self.name
    #    if self.sslbls is not None:
    #        for ssl in self.sslbls:
    #            yield ssl

    def __str__(self):
        """
        Defines how a Label is printed out, e.g. Gx:0 or Gcnot:1:2
        """
        #caller = inspect.getframeinfo(inspect.currentframe().f_back)
        #ky = "%s:%s:%d" % (caller[2],os.path.basename(caller[0]),caller[1])
        #debug_record[ky] = debug_record.get(ky, 0) + 1
        s = str(self.name)
        if self.sslbls:  # test for None and len == 0
            s += ":" + ":".join(map(str, self.sslbls))
        if self.time != 0.0:
            s += ("!%f" % self.time).rstrip('0').rstrip('.')
        return s

    def __repr__(self):
        return "Label[" + str(self) + "]"

    def __add__(self, s):
        if isinstance(s, str):
            return LabelTup(self.name + s, self.sslbls)
        else:
            raise NotImplementedError("Cannot add %s to a Label" % str(type(s)))

    def __eq__(self, other):
        """
        Defines equality between gates, so that they are equal if their values
        are equal.
        """
        #Unnecessary now that we have a separate LabelStr
        #if isinstance(other, str):
        #    if self.sslbls: return False # tests for None and len > 0
        #    return self.name == other

        return tuple.__eq__(self, other)
        #OLD return self.name == other.name and self.sslbls == other.sslbls # ok to compare None

    def __lt__(self, x):
        return tuple.__lt__(self, tuple(x))

    def __gt__(self, x):
        return tuple.__gt__(self, tuple(x))

    def __pygsti_reduce__(self):
        return self.__reduce__()

    def __reduce__(self):
        # Need to tell serialization logic how to create a new Label since it's derived
        # from the immutable tuple type (so cannot have its state set after creation)
        return (LabelTup, (self[:], self.time), None)

    def tonative(self):
        """ Returns this label as native python types.  Useful for
            faster serialization.
        """
        return tuple(self)

    def replacename(self, oldname, newname):
        """ Returns a label with `oldname` replaced by `newname`."""
        return LabelTup(newname, self.sslbls) if (self.name == oldname) else self

    def issimple(self):
        """ Whether this is a "simple" (opaque w/a true name, from a
            circuit perspective) label or not """
        return True

    __hash__ = tuple.__hash__  # this is why we derive from tuple - using the
    # native tuple.__hash__ directly == speed boost


class LabelStr(Label, str):
    """
    A Label for the special case when only a name is present (no
    state-space-labels).  We create this as a separate class
    so that we can use the string hash function in a
    "hardcoded" way - if we put switching logic in __hash__
    the hashing gets *much* slower.
    """

    @classmethod
    def init(cls, name, time=0.0):
        """
        Creates a new Model-item label, which is just a simple string label.

        Parameters
        ----------
        name : str
            The item name. E.g., 'CNOT' or 'H'.

        time : float
            The time at which this label occurs (can be relative or absolute)
        """

        #Type checking
        assert(isinstance(name, str)), "`name` must be a string, but it's '%s'" % str(name)
        assert(isinstance(time, float)), "`time` must be a floating point value, received: " + str(time)
        return cls.__new__(cls, name, time)

    def __new__(cls, name, time=0.0):
        ret = str.__new__(cls, name)
        ret.time = time
        return ret

    @property
    def name(self):
        return str(self[:])

    @property
    def sslbls(self):
        return None

    @property
    def args(self):
        return ()

    @property
    def components(self):
        return (self,)  # just a single "sub-label" component

    @property
    def qubits(self):  # Used in Circuit
        """An alias for sslbls, since commonly these are just qubit indices"""
        return None

    @property
    def number_of_qubits(self):  # Used in Circuit
        return None

    def has_prefix(self, prefix, typ="all"):
        """
        Whether this label has the given `prefix`.  Usually used to test whether
        the label names a given type.

        Parameters
        ----------
        prefix : str
            The prefix to check for.

        typ : {"any","all"}
            Whether, when there are multiple parts to the label, the prefix
            must occur in any or all of the parts.

        Returns
        -------
        bool
        """
        return self.startswith(prefix)

    def __str__(self):
        s = self[:]  # converts to a normal str
        if self.time != 0.0:
            s += ("!%f" % self.time).rstrip('0').rstrip('.')
        return s

    def __repr__(self):
        return "Label{" + str(self) + "}"

    def __add__(self, s):
        if isinstance(s, str):
            return LabelStr(self.name + str(s))
        else:
            raise NotImplementedError("Cannot add %s to a Label" % str(type(s)))

    def __eq__(self, other):
        """
        Defines equality between gates, so that they are equal if their values
        are equal.
        """
        return str.__eq__(self, other)

    def __lt__(self, x):
        return str.__lt__(self, str(x))

    def __gt__(self, x):
        return str.__gt__(self, str(x))

    def __pygsti_reduce__(self):
        return self.__reduce__()

    def __reduce__(self):
        # Need to tell serialization logic how to create a new Label since it's derived
        # from the immutable tuple type (so cannot have its state set after creation)
        return (LabelStr, (str(self), self.time), None)

    def tonative(self):
        """ Returns this label as native python types.  Useful for
            faster serialization.
        """
        return str(self)

    def replacename(self, oldname, newname):
        """ Returns a label with `oldname` replaced by `newname`."""
        return LabelStr(newname) if (self.name == oldname) else self

    def issimple(self):
        """ Whether this is a "simple" (opaque w/a true name, from a
            circuit perspective) label or not """
        return True

    __hash__ = str.__hash__  # this is why we derive from tuple - using the
    # native tuple.__hash__ directly == speed boost


class LabelTupTup(Label, tuple):
    """
    A label consisting of a *tuple* of (string, state-space-labels) tuples
    which labels a parallel layer/level of a circuit.
    """

    @classmethod
    def init(cls, tupOfTups, time=None):
        """
        Creates a new Model-item label, which is a tuple of tuples of simple
        string labels and tuples specifying the part of the Hilbert space upon
        which that item acts (often just qubit indices).

        Parameters
        ----------
        tupOfTups : tuple
            The item data - a tuple of (string, state-space-labels) tuples
            which labels a parallel layer/level of a circuit.
        """
        assert(time is None or isinstance(time, float)), "`time` must be a floating point value, received: " + str(time)
        tupOfLabels = tuple((Label(tup) for tup in tupOfTups))  # Note: tup can also be a Label obj
        if time is None:
            time = 0.0 if len(tupOfLabels) == 0 else \
                max([lbl.time for lbl in tupOfLabels])
        return cls.__new__(cls, tupOfLabels, time)

    def __new__(cls, tupOfLabels, time=0.0):
        ret = tuple.__new__(cls, tupOfLabels)  # creates a LabelTupTup object using tuple's __new__
        ret.time = time
        return ret

    @property
    def name(self):
        # TODO - something intelligent here?
        # no real "name" for a compound label... but want it to be a string so
        # users can use .startswith, etc.
        return "COMPOUND"

    @property
    def sslbls(self):
        # Note: if any component has sslbls == None, which signifies operating
        # on *all* qubits, then this label is on *all* qubites
        if len(self) == 0: return None  # "idle" label containing no gates - *all* qubits idle
        s = set()
        for lbl in self:
            if lbl.sslbls is None: return None
            s.update(lbl.sslbls)
        return tuple(sorted(list(s)))

    @property
    def args(self):
        return ()

    @property
    def components(self):
        return self  # self is a tuple of "sub-label" components

    @property
    def qubits(self):  # Used in Circuit
        """An alias for sslbls, since commonly these are just qubit indices"""
        return self.sslbls

    @property
    def number_of_qubits(self):  # Used in Circuit
        return len(self.sslbls) if (self.sslbls is not None) else None

    def has_prefix(self, prefix, typ="all"):
        """
        Whether this label has the given `prefix`.  Usually used to test whether
        the label names a given type.

        Parameters
        ----------
        prefix : str
            The prefix to check for.

        typ : {"any","all"}
            Whether, when there are multiple parts to the label, the prefix
            must occur in any or all of the parts.

        Returns
        -------
        bool
        """
        if typ == "all":
            return all([lbl.has_prefix(prefix) for lbl in self])
        elif typ == "any":
            return any([lbl.has_prefix(prefix) for lbl in self])
        else: raise ValueError("Invalid `typ` arg: %s" % str(typ))

    def map_state_space_labels(self, mapper):
        """
        Return a copy of this Label with all of the state-space-labels
        (often just qubit labels) updated according to a mapping function.

        For example, calling this function with `mapper = {0: 1, 1: 3}`
        on the Label "Gcnot:0:1" would return "Gcnot:1:3".

        Parameters
        ----------
        mapper : dict or function
            A dictionary whose keys are the existing state-space-label values
            and whose value are the new labels, or a function which takes a
            single (existing label) argument and returns a new label.

        Returns
        -------
        Label
        """
        return LabelTupTup(tuple((lbl.map_state_space_labels(mapper) for lbl in self)))

    def __str__(self):
        """
        Defines how a Label is printed out, e.g. Gx:0 or Gcnot:1:2
        """
        return "[" + "".join([str(lbl) for lbl in self]) + "]"

    def __repr__(self):
        return "Label[" + str(self) + "]"

    def __add__(self, s):
        raise NotImplementedError("Cannot add %s to a Label" % str(type(s)))

    def __eq__(self, other):
        """
        Defines equality between gates, so that they are equal if their values
        are equal.
        """
        #Unnecessary now that we have a separate LabelStr
        #if isinstance(other, str):
        #    if self.sslbls: return False # tests for None and len > 0
        #    return self.name == other

        return tuple.__eq__(self, other)
        #OLD return self.name == other.name and self.sslbls == other.sslbls # ok to compare None

    def __lt__(self, x):
        return tuple.__lt__(self, tuple(x))

    def __gt__(self, x):
        return tuple.__gt__(self, tuple(x))

    def __pygsti_reduce__(self):
        return self.__reduce__()

    def __reduce__(self):
        # Need to tell serialization logic how to create a new Label since it's derived
        # from the immutable tuple type (so cannot have its state set after creation)
        return (LabelTupTup, (self[:], self.time), None)

    def __contains__(self, x):
        # "recursive" contains checks component containers
        return any([(x == layer or x in layer) for layer in self.components])

    def tonative(self):
        """ Returns this label as native python types.  Useful for
            faster serialization.
        """
        return tuple((x.tonative() for x in self))

    def replacename(self, oldname, newname):
        """ Returns a label with `oldname` replaced by `newname`."""
        return LabelTupTup(tuple((x.replacename(oldname, newname) for x in self)))

    def issimple(self):
        """ Whether this is a "simple" (opaque w/a true name, from a
            circuit perspective) label or not """
        return False

    def depth(self):
        if len(self.components) == 0: return 1  # still depth 1 even if empty
        return max([x.depth() for x in self.components])

    def expand_subcircuits(self):
        """
        Expand any sub-circuits within this label and return a resulting list
        of component labels which doesn't include any :class:`CircuitLabel`
        labels.  This effectively expands any "boxes" or "exponentiation"
        within this label.

        Returns
        -------
        tuple
            A tuple of component Labels (none of which should be
            :class:`CircuitLabel`s).
        """
        ret = []
        expanded_comps = [x.expand_subcircuits() for x in self.components]

        #DEBUG TODO REMOVE
        #print("DB: expaned comps:")
        #for i,x in enumerate(expanded_comps):
        #    print(i,": ",x)

        for i in range(self.depth()):  # depth == # of layers when expanded
            ec = []
            for expanded_comp in expanded_comps:
                if i < len(expanded_comp):
                    ec.extend(expanded_comp[i].components)  # .components = vertical expansion
            #assert(len(ec) > 0), "Logic error!" #this is ok (e.g. an idle subcircuit)
            ret.append(LabelTupTup.init(ec))
        return tuple(ret)

    __hash__ = tuple.__hash__  # this is why we derive from tuple - using the
    # native tuple.__hash__ directly == speed boost


class CircuitLabel(Label, tuple):
    def __new__(cls, name, tupOfLayers, stateSpaceLabels, reps=1, time=None):
        # Note: may need default args for all but 1st for pickling!
        """
        Creates a new Model-item label, which defines a set of other labels
        as a sub-circuit and allows that sub-circuit to be repeated some integer
        number of times.  A `CircuitLabel` can be visualized as placing a
        (named) box around some set of labels and optionally exponentiating
        that box.

        Internally, a circuit labels look very similar to `LabelTupTup` objects,
        holding a tuple of tuples defining the component labels (circuit layers).

        Parameters
        ----------
        name : str
            The name of the sub-circuit (box).  Cannot be `None`, but can be
            empty.

        tupOfLayers : tuple
            The item data - a tuple of tuples which label the components
            (layers) within this label.

        stateSpaceLabels : list or tuple
            A list or tuple that identifies which sectors/parts of the Hilbert
            space is acted upon.  In many cases, this is a list of integers
            specifying the qubits on which a gate acts, when the ordering in the
            list defines the 'direction' of the gate.

        reps : int, optional
            The "exponent" - the number of times the `tupOfLayers` labels are
            repeated.

        time : float
            The time at which this label occurs (can be relative or absolute)
        """
        #if name is None: name = '' # backward compatibility (temporary - TODO REMOVE)
        assert(isinstance(reps, _numbers.Integral) and isinstance(name, str)
               ), "Invalid name or reps: %s %s" % (str(name), str(reps))
        tupOfLabels = tuple((Label(tup) for tup in tupOfLayers))  # Note: tup can also be a Label obj
        # creates a CircuitLabel object using tuple's __new__
        ret = tuple.__new__(cls, (name, stateSpaceLabels, reps) + tupOfLabels)
        if time is None:
            ret.time = 0.0 if len(tupOfLabels) == 0 else \
                sum([lbl.time for lbl in tupOfLabels])  # sum b/c components are *layers* of sub-circuit
        else:
            ret.time = time
        return ret

    @property
    def name(self):
        return self[0]

    @property
    def sslbls(self):
        return self[1]

    @property
    def reps(self):
        return self[2]

    @property
    def args(self):
        raise NotImplementedError("TODO!")

    @property
    def components(self):
        return self[3:]

    @property
    def qubits(self):  # Used in Circuit
        """An alias for sslbls, since commonly these are just qubit indices"""
        return self.sslbls

    @property
    def number_of_qubits(self):  # Used in Circuit
        return len(self.sslbls) if (self.sslbls is not None) else None

    def has_prefix(self, prefix, typ="all"):
        """
        Whether this label has the given `prefix`.  Usually used to test whether
        the label names a given type.

        Parameters
        ----------
        prefix : str
            The prefix to check for.

        typ : {"any","all"}
            Whether, when there are multiple parts to the label, the prefix
            must occur in any or all of the parts.

        Returns
        -------
        bool
        """
        return self.name.startswith(prefix)

    def map_state_space_labels(self, mapper):
        """
        Return a copy of this Label with all of the state-space-labels
        (often just qubit labels) updated according to a mapping function.

        For example, calling this function with `mapper = {0: 1, 1: 3}`
        on the Label "Gcnot:0:1" would return "Gcnot:1:3".

        Parameters
        ----------
        mapper : dict or function
            A dictionary whose keys are the existing state-space-label values
            and whose value are the new labels, or a function which takes a
            single (existing label) argument and returns a new label.

        Returns
        -------
        Label
        """
        if isinstance(mapper, dict):
            mapped_sslbls = [mapper[sslbl] for sslbl in self.sslbls]
        else:  # assume mapper is callable
            mapped_sslbls = [mapper(sslbl) for sslbl in self.sslbls]
        return CircuitLabel(self.name,
                            tuple((lbl.map_state_space_labels(mapper) for lbl in self.components)),
                            mapped_sslbls,
                            self[2])

    def __str__(self):
        """
        Defines how a Label is printed out, e.g. Gx:0 or Gcnot:1:2
        """
        if len(self.name) > 0:
            s = self.name
            if self.time != 0.0:
                s += ("!%f" % self.time).rstrip('0').rstrip('.')
        else:
            s = "".join([str(lbl) for lbl in self.components])
            if self.time != 0.0:
                s += ("!%f" % self.time).rstrip('0').rstrip('.')
            if len(self.components) > 1:
                s = "(" + s + ")"  # add parenthesis
        if self[2] != 1: s += "^%d" % self[2]
        return s

    def __repr__(self):
        return "CircuitLabel[" + str(self) + "]"

    def __add__(self, s):
        raise NotImplementedError("Cannot add %s to a Label" % str(type(s)))

    def __eq__(self, other):
        """
        Defines equality between gates, so that they are equal if their values
        are equal.
        """
        #Unnecessary now that we have a separate LabelStr
        #if isinstance(other, str):
        #    if self.sslbls: return False # tests for None and len > 0
        #    return self.name == other

        return tuple.__eq__(self, other)
        #OLD return self.name == other.name and self.sslbls == other.sslbls # ok to compare None

    def __lt__(self, x):
        return tuple.__lt__(self, tuple(x))

    def __gt__(self, x):
        return tuple.__gt__(self, tuple(x))

    def __pygsti_reduce__(self):
        return self.__reduce__()

    def __reduce__(self):
        # Need to tell serialization logic how to create a new Label since it's derived
        # from the immutable tuple type (so cannot have its state set after creation)
        return (CircuitLabel, (self[0], self[3:], self[1], self[2], self.time), None)

    def __contains__(self, x):
        # "recursive" contains checks component containers
        return any([(x == layer or x in layer) for layer in self.components])

    def tonative(self):
        """ Returns this label as native python types.  Useful for
            faster serialization.
        """
        return self[0:3] + tuple((x.tonative() for x in self.components))

    def replacename(self, oldname, newname):
        """ Returns a label with `oldname` replaced by `newname`."""
        return CircuitLabel(self.name,
                            tuple((x.replacename(oldname, newname) for x in self.components)),
                            self.sslbls,
                            self[2])

    def issimple(self):
        """ Whether this is a "simple" (opaque w/a true name, from a
            circuit perspective) label or not """
        return True  # still true - even though can have components!

    def depth(self):
        return sum([x.depth() for x in self.components]) * self.reps

    def expand_subcircuits(self):
        """
        Expand any sub-circuits within this label and return a resulting list
        of component labels which doesn't include any :class:`CircuitLabel`
        labels.  This effectively expands any "boxes" or "exponentiation"
        within this label.

        Returns
        -------
        tuple
            A tuple of component Labels (none of which should be
            :class:`CircuitLabel`s).
        """
        #REMOVE print("Expanding subcircuit components: ",self.components)
        #REMOVE print(" --> ",[ x.expand_subcircuits() for x in self.components ])
        return tuple(_itertools.chain(*[x.expand_subcircuits() for x in self.components])) * self.reps

    __hash__ = tuple.__hash__  # this is why we derive from tuple - using the
    # native tuple.__hash__ directly == speed boost


#class NamedLabelTupTup(Label,tuple):
#    def __new__(cls,name,tupOfTups):
#        pass


class LabelTupWithArgs(Label, tuple):
    """
    Same as LabelTup, but includes slots for args and time
    """

    @classmethod
    def init(cls, name, stateSpaceLabels, time=0.0, args=()):
        """
        Creates a new Model-item label, which is divided into a simple string
        label, a tuple specifying the part of the Hilbert space upon which the
        item acts (often just qubit indices), a time, and arguments.

        Parameters
        ----------
        name : str
            The item name. E.g., 'CNOT' or 'H'.

        stateSpaceLabels : list or tuple
            A list or tuple that identifies which sectors/parts of the Hilbert
            space is acted upon.  In many cases, this is a list of integers
            specifying the qubits on which a gate acts, when the ordering in the
            list defines the 'direction' of the gate.  If something other than
            a list or tuple is passed, a single-element tuple is created
            containing the passed object.

        time : float
            The time at which this label occurs (can be relative or absolute)

        args : iterable of hashable types
            A list of "arguments" for this label.
        """
        #Type checking
        assert(isinstance(name, str)), "`name` must be a string, but it's '%s'" % str(name)
        assert(stateSpaceLabels is not None), "LabelTup must be initialized with non-None state-space labels"
        if not isinstance(stateSpaceLabels, (tuple, list)):
            stateSpaceLabels = (stateSpaceLabels,)
        for ssl in stateSpaceLabels:
            assert(isinstance(ssl, str) or isinstance(ssl, _numbers.Integral)), \
                "State space label '%s' must be a string or integer!" % str(ssl)
        assert(isinstance(time, float)), "`time` must be a floating point value, received: " + str(time)
        assert(len(args) > 0), "`args` must be a nonempty list/tuple of hashable arguments"
        #TODO: check that all args are hashable?

        #Try to convert integer-strings to ints (for parsing from files...)
        integerized_sslbls = []
        for ssl in stateSpaceLabels:
            try: integerized_sslbls.append(int(ssl))
            except: integerized_sslbls.append(ssl)

        # Regardless of whether the input is a list, tuple, or int, the state space labels
        # (qubits) that the item/gate acts on are stored as a tuple (because tuples are immutable).
        sslbls = tuple(integerized_sslbls)
        args = tuple(args)
        tup = (name, 2 + len(args)) + args + sslbls  # stores: (name, K, args, sslbls)
        # where K is the index of the start of the sslbls (or 1 more than the last arg index)

        return cls.__new__(cls, tup, time)

    def __new__(cls, tup, time=0.0):
        ret = tuple.__new__(cls, tup)  # creates a LabelTup object using tuple's __new__
        ret.time = time
        return ret

    @property
    def name(self):
        return self[0]

    @property
    def sslbls(self):
        if len(self) > self[1]:
            return self[self[1]:]
        else: return None

    @property
    def args(self):
        return self[2:self[1]]

    @property
    def components(self):
        return (self,)  # just a single "sub-label" component

    @property
    def qubits(self):  # Used in Circuit
        """An alias for sslbls, since commonly these are just qubit indices"""
        return self.sslbls

    @property
    def number_of_qubits(self):  # Used in Circuit
        return len(self.sslbls) if (self.sslbls is not None) else None

    def has_prefix(self, prefix, typ="all"):
        """
        Whether this label has the given `prefix`.  Usually used to test whether
        the label names a given type.

        Parameters
        ----------
        prefix : str
            The prefix to check for.

        typ : {"any","all"}
            Whether, when there are multiple parts to the label, the prefix
            must occur in any or all of the parts.

        Returns
        -------
        bool
        """
        return self.name.startswith(prefix)

    def map_state_space_labels(self, mapper):
        """
        Return a copy of this Label with all of the state-space-labels
        (often just qubit labels) updated according to a mapping function.

        For example, calling this function with `mapper = {0: 1, 1: 3}`
        on the Label "Gcnot:0:1" would return "Gcnot:1:3".

        Parameters
        ----------
        mapper : dict or function
            A dictionary whose keys are the existing state-space-label values
            and whose value are the new labels, or a function which takes a
            single (existing label) argument and returns a new label.

        Returns
        -------
        Label
        """
        if isinstance(mapper, dict):
            mapped_sslbls = [mapper[sslbl] for sslbl in self.sslbls]
        else:  # assume mapper is callable
            mapped_sslbls = [mapper(sslbl) for sslbl in self.sslbls]
        return Label(self.name, mapped_sslbls, self.time, self.args)
        # FUTURE: use LabelTupWithArgs here instead of Label?

    def __str__(self):
        """
        Defines how a Label is printed out, e.g. Gx:0 or Gcnot:1:2
        """
        #caller = inspect.getframeinfo(inspect.currentframe().f_back)
        #ky = "%s:%s:%d" % (caller[2],os.path.basename(caller[0]),caller[1])
        #debug_record[ky] = debug_record.get(ky, 0) + 1
        s = str(self.name)
        if self.args:  # test for None and len == 0
            s += ";" + ";".join(map(str, self.args))
        if self.sslbls:  # test for None and len == 0
            s += ":" + ":".join(map(str, self.sslbls))
        if self.time != 0.0:
            s += ("!%f" % self.time).rstrip('0').rstrip('.')
        return s

    def __repr__(self):
        return "Label[" + str(self) + "]"

    def __add__(self, s):
        if isinstance(s, str):
            return LabelTupWithArgs(self.name + s, self.sslbls, self.time, self.args)
        else:
            raise NotImplementedError("Cannot add %s to a Label" % str(type(s)))

    def __eq__(self, other):
        """
        Defines equality between gates, so that they are equal if their values
        are equal.
        """
        #Unnecessary now that we have a separate LabelStr
        #if isinstance(other, str):
        #    if self.sslbls: return False # tests for None and len > 0
        #    return self.name == other

        return tuple.__eq__(self, other)
        #OLD return self.name == other.name and self.sslbls == other.sslbls # ok to compare None

    def __lt__(self, x):
        return tuple.__lt__(self, tuple(x))

    def __gt__(self, x):
        return tuple.__gt__(self, tuple(x))

    def __pygsti_reduce__(self):
        return self.__reduce__()

    def __reduce__(self):
        # Need to tell serialization logic how to create a new Label since it's derived
        # from the immutable tuple type (so cannot have its state set after creation)
        return (LabelTupWithArgs, (self[:], self.time), None)

    def tonative(self):
        """ Returns this label as native python types.  Useful for
            faster serialization.
        """
        return tuple(self)

    def replacename(self, oldname, newname):
        """ Returns a label with `oldname` replaced by `newname`."""
        return LabelTupWithArgs(newname, self.sslbls, self.time, self.args) if (self.name == oldname) else self

    def issimple(self):
        """ Whether this is a "simple" (opaque w/a true name, from a
            circuit perspective) label or not """
        return True

    __hash__ = tuple.__hash__  # this is why we derive from tuple - using the
    # native tuple.__hash__ directly == speed boost


class LabelTupTupWithArgs(Label, tuple):
    """
    A label consisting of a *tuple* of (string, state-space-labels) tuples
    which labels a parallel layer/level of a circuit at a single time.
    This label also supports having arguments.
    """

    @classmethod
    def init(cls, tupOfTups, time=None, args=()):
        """
        Creates a new Model-item label, which is a tuple of tuples of simple
        string labels and tuples specifying the part of the Hilbert space upon
        which that item acts (often just qubit indices).

        Parameters
        ----------
        tupOfTups : tuple
            The item data - a tuple of (string, state-space-labels) tuples
            which labels a parallel layer/level of a circuit.

        time : float
            The time at which this label occurs (can be relative or absolute)

        args : iterable of hashable types
            A list of "arguments" for this label.
        """
        assert(time is None or isinstance(time, float)), "`time` must be a floating point value, received: " + str(time)
        assert(len(args) > 0), "`args` must be a nonempty list/tuple of hashable arguments"
        tupOfLabels = (1 + len(args),) + args + tuple((Label(tup) for tup in tupOfTups))  # Note tup can be a Label
        # stores: (K, args, subLabels) where K is the index of the start of subLabels

        #if time is not None:
        #    assert(all([(time == l.time or l.time is None) for l in tupOfLabels[1 + len(args):]])), \
        #        "Component times do not match compound label time!"
        if time is None:
            time = 0.0 if len(tupOfLabels) == 0 else \
                max([lbl.time for lbl in tupOfLabels])
        return cls.__new__(cls, tupOfLabels, time)

    def __new__(cls, tupOfLabels, time=0.0):
        ret = tuple.__new__(cls, tupOfLabels)  # creates a LabelTupTup object using tuple's __new__
        ret.time = time
        return ret

    @property
    def name(self):
        # TODO - something intelligent here?
        # no real "name" for a compound label... but want it to be a string so
        # users can use .startswith, etc.
        return "COMPOUND"

    @property
    def sslbls(self):
        # Note: if any component has sslbls == None, which signifies operating
        # on *all* qubits, then this label is on *all* qubits
        s = set()
        for lbl in self[self[0]:]:
            if lbl.sslbls is None: return None
            s.update(lbl.sslbls)
        return tuple(sorted(list(s)))

    @property
    def args(self):
        return self[1:self[0]]

    @property
    def components(self):
        return self[self[0]:]  # a tuple of "sub-label" components

    @property
    def qubits(self):  # Used in Circuit
        """An alias for sslbls, since commonly these are just qubit indices"""
        return self.sslbls

    @property
    def number_of_qubits(self):  # Used in Circuit
        return len(self.sslbls) if (self.sslbls is not None) else None

    def has_prefix(self, prefix, typ="all"):
        """
        Whether this label has the given `prefix`.  Usually used to test whether
        the label names a given type.

        Parameters
        ----------
        prefix : str
            The prefix to check for.

        typ : {"any","all"}
            Whether, when there are multiple parts to the label, the prefix
            must occur in any or all of the parts.

        Returns
        -------
        bool
        """
        if typ == "all":
            return all([lbl.has_prefix(prefix) for lbl in self.components])
        elif typ == "any":
            return any([lbl.has_prefix(prefix) for lbl in self.components])
        else: raise ValueError("Invalid `typ` arg: %s" % str(typ))

    def map_state_space_labels(self, mapper):
        """
        Return a copy of this Label with all of the state-space-labels
        (often just qubit labels) updated according to a mapping function.

        For example, calling this function with `mapper = {0: 1, 1: 3}`
        on the Label "Gcnot:0:1" would return "Gcnot:1:3".

        Parameters
        ----------
        mapper : dict or function
            A dictionary whose keys are the existing state-space-label values
            and whose value are the new labels, or a function which takes a
            single (existing label) argument and returns a new label.

        Returns
        -------
        Label
        """
        return LabelTupTupWithArgs(tuple((lbl.map_state_space_labels(mapper)
                                          for lbl in self.components)), self.time, self.args)

    def __str__(self):
        """
        Defines how a Label is printed out, e.g. Gx:0 or Gcnot:1:2
        """
        if self.args:  # test for None and len == 0
            argstr = ";" + ";".join(map(str, self.args))
        else:
            argstr = ""

        if self.time != 0.0:  # if we're supposed to be holding a time
            timestr = ("!%f" % self.time).rstrip('0').rstrip('.')
        else:
            timestr = ""

        return "[" + "".join([str(lbl) for lbl in self]) + argstr + timestr + "]"

    def __repr__(self):
        return "Label[" + str(self) + "]"

    def __add__(self, s):
        raise NotImplementedError("Cannot add %s to a Label" % str(type(s)))

    def __eq__(self, other):
        """
        Defines equality between gates, so that they are equal if their values
        are equal.
        """
        #Unnecessary now that we have a separate LabelStr
        #if isinstance(other, str):
        #    if self.sslbls: return False # tests for None and len > 0
        #    return self.name == other

        return tuple.__eq__(self, other)
        #OLD return self.name == other.name and self.sslbls == other.sslbls # ok to compare None

    def __lt__(self, x):
        return tuple.__lt__(self, tuple(x))

    def __gt__(self, x):
        return tuple.__gt__(self, tuple(x))

    def __pygsti_reduce__(self):
        return self.__reduce__()

    def __reduce__(self):
        # Need to tell serialization logic how to create a new Label since it's derived
        # from the immutable tuple type (so cannot have its state set after creation)
        return (LabelTupTupWithArgs, (self[:], self.time), None)

    def __contains__(self, x):
        # "recursive" contains checks component containers
        return any([(x == layer or x in layer) for layer in self.components])

    def tonative(self):
        """ Returns this label as native python types.  Useful for
            faster serialization.
        """
        return self[0:self[0]] + tuple((x.tonative() for x in self[self[0]:]))

    def replacename(self, oldname, newname):
        """ Returns a label with `oldname` replaced by `newname`."""
        return LabelTupTupWithArgs(tuple((x.replacename(oldname, newname) for x in self.components)),
                                   self.time, self.args)

    def issimple(self):
        """ Whether this is a "simple" (opaque w/a true name, from a
            circuit perspective) label or not """
        return False

    def depth(self):
        if len(self.components) == 0: return 1  # still depth 1 even if empty
        return max([x.depth() for x in self.components])

    __hash__ = tuple.__hash__  # this is why we derive from tuple - using the
    # native tuple.__hash__ directly == speed boost
