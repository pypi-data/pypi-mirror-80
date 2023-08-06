""" Functions for writing GST objects to text files."""
#***************************************************************************************************
# Copyright 2015, 2019 National Technology & Engineering Solutions of Sandia, LLC (NTESS).
# Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains certain rights
# in this software.
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
# in compliance with the License.  You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0 or in the LICENSE file in the root pyGSTi directory.
#***************************************************************************************************

import warnings as _warnings
import numpy as _np
import pathlib as _pathlib

# from . import stdinput as _stdinput
from .. import tools as _tools
from .. import objects as _objs
from . import loaders as _loaders


def write_empty_dataset(filename, circuit_list,
                        headerString='## Columns = 1 frequency, count total', numZeroCols=None,
                        appendWeightsColumn=False):
    """
    Write an empty dataset file to be used as a template.

    Parameters
    ----------
    filename : string
        The filename to write.

    circuit_list : list of Circuits
        List of operation sequences to write, each to be followed by numZeroCols zeros.

    headerString : string, optional
        Header string for the file; should start with a pound (#) or double-pound (##)
        so it is treated as a commend or directive, respectively.

    numZeroCols : int, optional
        The number of zero columns to place after each operation sequence.  If None,
        then headerString must begin with "## Columns = " and number of zero
        columns will be inferred.

    appendWeightsColumn : bool, optional
        Add an additional 'weights' column.

    """

    if len(circuit_list) > 0 and not isinstance(circuit_list[0], _objs.Circuit):
        raise ValueError("Argument circuit_list must be a list of Circuit objects!")

    if numZeroCols is None:  # TODO: cleaner way to extract number of columns from headerString?
        if headerString.startswith('## Columns = '):
            numZeroCols = len(headerString.split(','))
        else:
            raise ValueError("Must specify numZeroCols since I can't figure it out from the header string")

    with open(str(filename), 'w') as output:
        zeroCols = "  ".join(['0'] * numZeroCols)
        output.write(headerString + '\n')
        for circuit in circuit_list:  # circuit should be a Circuit object here
            output.write(circuit.str + "  " + zeroCols + (("  %f" %
                                                           circuit.weight) if appendWeightsColumn else "") + '\n')


def _outcome_to_str(x):
    if isinstance(x, str): return x
    else: return ":".join([str(i) for i in x])


def write_dataset(filename, dataset, circuit_list=None,
                  outcomeLabelOrder=None, fixedColumnMode=True, withTimes="auto"):
    """
    Write a text-formatted dataset file.

    Parameters
    ----------
    filename : string
        The filename to write.

    dataset : DataSet
        The data set from which counts are obtained.

    circuit_list : list of Circuits, optional
        The list of operation sequences to include in the written dataset.
        If None, all operation sequences are output.

    outcomeLabelOrder : list, optional
        A list of the outcome labels in dataset which specifies
        the column order in the output file.

    fixedColumnMode : bool, optional
        When `True`, a file is written with column headers indicating which
        outcome each column of counts corresponds to.  If a row doesn't have
        any counts for an outcome, `'--'` is used in its place.  When `False`,
        each row's counts are written in an expanded form that includes the
        outcome labels (each "count" has the format <outcomeLabel>:<count>).

    withTimes : bool or "auto", optional
        Whether to include (save) time-stamp information in output.  This
        can only be True when `fixedColumnMode=False`.  `"auto"` will set
        this to True if `fixedColumnMode=False` and `dataset` has data at
        non-trivial (non-zero) times.
    """
    if circuit_list is not None:
        if len(circuit_list) > 0 and not isinstance(circuit_list[0], _objs.Circuit):
            raise ValueError("Argument circuit_list must be a list of Circuit objects!")
    else:
        circuit_list = list(dataset.keys())

    if outcomeLabelOrder is not None:  # convert to tuples if needed
        outcomeLabelOrder = [(ol,) if isinstance(ol, str) else ol
                             for ol in outcomeLabelOrder]

    outcomeLabels = dataset.get_outcome_labels()
    if outcomeLabelOrder is not None:
        assert(len(outcomeLabelOrder) == len(outcomeLabels))
        assert(all([ol in outcomeLabels for ol in outcomeLabelOrder]))
        assert(all([ol in outcomeLabelOrder for ol in outcomeLabels]))
        outcomeLabels = outcomeLabelOrder

    headerString = ""
    if hasattr(dataset, 'comment') and dataset.comment is not None:
        for commentLine in dataset.comment.split('\n'):
            if commentLine.startswith('#'):
                headerString += commentLine + '\n'
            else:
                headerString += "# " + commentLine + '\n'

    if fixedColumnMode is True:
        headerString += '## Columns = ' + ", ".join(["%s count" % _outcome_to_str(ol)
                                                     for ol in outcomeLabels]) + '\n'
        assert(not (withTimes is True)), "Cannot set `witTimes=True` when `fixedColumnMode=True`"
    elif withTimes == "auto":
        trivial_times = dataset.has_trivial_timedependence()
    else:
        trivial_times = not withTimes

    with open(str(filename), 'w') as output:
        output.write(headerString)
        for circuit in circuit_list:  # circuit should be a Circuit object here
            dataRow = dataset[circuit]
            counts = dataRow.counts
            circuit_to_write = _objs.DataSet.strip_occurence_tag(circuit) \
                if dataset.collisionAction == "keepseparate" else circuit

            if fixedColumnMode:
                #output '--' for outcome labels that aren't present in this row
                output.write(circuit_to_write.str + "  "
                             + "  ".join([(("%g" % counts[ol]) if (ol in counts) else '--')
                                          for ol in outcomeLabels]))
                if dataRow.aux: output.write(" # %s" % str(repr(dataRow.aux)))  # write aux info
                output.write('\n')  # finish the line

            elif trivial_times:  # use expanded label:count format
                output.write(circuit_to_write.str + "  "
                             + "  ".join([("%s:%g" % (_outcome_to_str(ol), counts[ol]))
                                          for ol in outcomeLabels if ol in counts]))
                if dataRow.aux: output.write(" # %s" % str(repr(dataRow.aux)))  # write aux info
                output.write('\n')  # finish the line

            else:
                output.write(circuit_to_write.str + "\n"
                             + "times: " + "  ".join(["%g" % tm for tm in dataRow.time]) + "\n"
                             + "outcomes: " + "  ".join([_outcome_to_str(ol) for ol in dataRow.outcomes]) + "\n")
                if dataRow.reps is not None:
                    output.write("repetitions: " + "  ".join(["%d" % rep for rep in dataRow.reps]) + "\n")
                if dataRow.aux:
                    output.write("aux: " + str(repr(dataRow.aux)) + "\n")
                output.write('\n')  # blank line between circuits


def write_multidataset(filename, multidataset, circuit_list=None, outcomeLabelOrder=None):
    """
    Write a text-formatted multi-dataset file.

    Parameters
    ----------
    filename : string
        The filename to write.

    multidataset : MultiDataSet
        The multi data set from which counts are obtained.

    circuit_list : list of Circuits
        The list of operation sequences to include in the written dataset.
        If None, all operation sequences are output.

    outcomeLabelOrder : list, optional
        A list of the SPAM labels in multidataset which specifies
        the column order in the output file.
    """

    if circuit_list is not None:
        if len(circuit_list) > 0 and not isinstance(circuit_list[0], _objs.Circuit):
            raise ValueError("Argument circuit_list must be a list of Circuit objects!")
    else:
        circuit_list = list(multidataset.cirIndex.keys())  # TODO: make access function for circuits?

    if outcomeLabelOrder is not None:  # convert to tuples if needed
        outcomeLabelOrder = [(ol,) if isinstance(ol, str) else ol
                             for ol in outcomeLabelOrder]

    outcomeLabels = multidataset.get_outcome_labels()
    if outcomeLabelOrder is not None:
        assert(len(outcomeLabelOrder) == len(outcomeLabels))
        assert(all([ol in outcomeLabels for ol in outcomeLabelOrder]))
        assert(all([ol in outcomeLabelOrder for ol in outcomeLabels]))
        outcomeLabels = outcomeLabelOrder

    dsLabels = list(multidataset.keys())

    headerString = ""
    if hasattr(multidataset, 'comment') and multidataset.comment is not None:
        for commentLine in multidataset.comment.split('\n'):
            if commentLine.startswith('#'):
                headerString += commentLine + '\n'
            else:
                headerString += "# " + commentLine + '\n'
    headerString += '## Columns = ' + ", ".join(["%s %s count" % (dsl, _outcome_to_str(ol))
                                                 for dsl in dsLabels
                                                 for ol in outcomeLabels])
    # parser = _stdinput.StdInputParser()

    # strip_occurence_tags = any([ca == "keepseparate" for ca in multidataset.collisionActions.values()])
    datasets = [multidataset[dsl] for dsl in dsLabels]
    with open(str(filename), 'w') as output:
        output.write(headerString + '\n')
        for circuit in circuit_list:  # circuit should be a Circuit object here
            # circuit_to_write = _objs.DataSet.strip_occurence_tag(circuit) \
            #     if strip_occurence_tags else circuit
            cnts = [ds[circuit].counts.get(ol, '--') for ds in datasets for ol in outcomeLabels]
            output.write(circuit.str + "  " + "  ".join([(("%g" % cnt) if (cnt != '--') else cnt)
                                                         for cnt in cnts]) + '\n')
            #write aux info
            if multidataset.auxInfo[circuit]:
                output.write(" # %s" % str(repr(multidataset.auxInfo[circuit])))
            output.write('\n')  # finish the line


def write_circuit_list(filename, circuit_list, header=None):
    """
    Write a text-formatted operation sequence list file.

    Parameters
    ----------
    filename : string
        The filename to write.

    circuit_list : list of Circuits
        The list of operation sequences to include in the written dataset.

    header : string, optional
        Header line (first line of file).  Prepended with a pound sign (#), so no
        need to include one.

    """
    if len(circuit_list) > 0 and not isinstance(circuit_list[0], _objs.Circuit):
        raise ValueError("Argument circuit_list must be a list of Circuit objects!")

    with open(str(filename), 'w') as output:
        if header is not None:
            output.write("# %s" % header + '\n')

        for circuit in circuit_list:
            output.write(circuit.str + '\n')


def write_model(mdl, filename, title=None):
    """
    Write a text-formatted model file.

    Parameters
    ----------
    mdl : Model
        The model to write to file.

    filename : string
        The filename to write.

    title : string, optional
        Header line (first line of file).  Prepended with a pound sign (#), so no
        need to include one.

    """

    def writeprop(f, lbl, val):
        """ Write (label,val) property to output file """
        if isinstance(val, _np.ndarray):  # then write as rows
            f.write("%s\n" % lbl)
            if val.ndim == 1:
                f.write(" ".join("%.8g" % el for el in val) + '\n')
            elif val.ndim == 2:
                f.write(_tools.mx_to_string(val, width=16, prec=8))
            else:
                raise ValueError("Cannot write an ndarray with %d dimensions!" % val.ndim)
            f.write("\n")
        else:
            f.write("%s = %s\n" % (lbl, repr(val)))

    with open(str(filename), 'w') as output:

        if title is not None:
            output.write("# %s" % title + '\n')
        output.write('\n')

        for prepLabel, rhoVec in mdl.preps.items():
            props = None
            if isinstance(rhoVec, _objs.FullSPAMVec): typ = "PREP"
            elif isinstance(rhoVec, _objs.TPSPAMVec): typ = "TP-PREP"
            elif isinstance(rhoVec, _objs.StaticSPAMVec): typ = "STATIC-PREP"
            elif isinstance(rhoVec, _objs.LindbladSPAMVec):
                typ = "CPTP-PREP"
                props = [("PureVec", rhoVec.state_vec.todense()),
                         ("ErrgenMx", rhoVec.error_map.todense())]
            else:
                _warnings.warn(
                    ("Non-standard prep of type {typ} cannot be described by"
                     "text format model files.  It will be read in as a"
                     "fully parameterized spam vector").format(typ=str(type(rhoVec))))
                typ = "PREP"

            if props is None: props = [("LiouvilleVec", rhoVec.todense())]
            output.write("%s: %s\n" % (typ, prepLabel))
            for lbl, val in props:
                writeprop(output, lbl, val)

        for povmLabel, povm in mdl.povms.items():
            props = None; povm_to_write = povm
            if isinstance(povm, _objs.UnconstrainedPOVM): povmType = "POVM"
            elif isinstance(povm, _objs.TPPOVM): povmType = "TP-POVM"
            elif isinstance(povm, _objs.LindbladPOVM):
                povmType = "CPTP-POVM"
                props = [("ErrgenMx", povm.error_map.todense())]
                povm_to_write = povm.base_povm
            else:
                _warnings.warn(
                    ("Non-standard POVM of type {typ} cannot be described by"
                     "text format model files.  It will be read in as a"
                     "standard POVM").format(typ=str(type(povm))))
                povmType = "POVM"

            output.write("%s: %s\n\n" % (povmType, povmLabel))
            if props is not None:
                for lbl, val in props:
                    writeprop(output, lbl, val)

            for ELabel, EVec in povm_to_write.items():
                if isinstance(EVec, _objs.FullSPAMVec): typ = "EFFECT"
                elif isinstance(EVec, _objs.ComplementSPAMVec): typ = "EFFECT"  # ok
                elif isinstance(EVec, _objs.TPSPAMVec): typ = "TP-EFFECT"
                elif isinstance(EVec, _objs.StaticSPAMVec): typ = "STATIC-EFFECT"
                else:
                    _warnings.warn(
                        ("Non-standard effect of type {typ} cannot be described by"
                         "text format model files.  It will be read in as a"
                         "fully parameterized spam vector").format(typ=str(type(EVec))))
                    typ = "EFFECT"
                output.write("%s: %s\n" % (typ, ELabel))
                writeprop(output, "LiouvilleVec", EVec.todense())

            output.write("END POVM\n\n")

        for label, gate in mdl.operations.items():
            props = None
            if isinstance(gate, _objs.FullDenseOp): typ = "GATE"
            elif isinstance(gate, _objs.TPDenseOp): typ = "TP-GATE"
            elif isinstance(gate, _objs.StaticDenseOp): typ = "STATIC-GATE"
            elif isinstance(gate, _objs.LindbladDenseOp):
                typ = "CPTP-GATE"
                props = [("LiouvilleMx", gate.todense())]
                if gate.unitary_postfactor is not None:
                    upost = gate.unitary_postfactor.todense() \
                        if isinstance(gate.unitary_postfactor, _objs.LinearOperator) \
                        else gate.unitary_postfactor
                    props.append(("RefLiouvilleMx", upost))
            else:
                _warnings.warn(
                    ("Non-standard gate of type {typ} cannot be described by"
                     "text format model files.  It will be read in as a"
                     "fully parameterized gate").format(typ=str(type(gate))))
                typ = "GATE"

            if props is None: props = [("LiouvilleMx", gate.todense())]
            output.write(typ + ": " + str(label) + '\n')
            for lbl, val in props:
                writeprop(output, lbl, val)

        for instLabel, inst in mdl.instruments.items():
            if isinstance(inst, _objs.Instrument): typ = "Instrument"
            elif isinstance(inst, _objs.TPInstrument): typ = "TP-Instrument"
            else:
                _warnings.warn(
                    ("Non-standard Instrument of type {typ} cannot be described by"
                     "text format model files.  It will be read in as a"
                     "standard Instrument").format(typ=str(type(inst))))
                typ = "Instrument"
            output.write(typ + ": " + str(instLabel) + '\n\n')

            for label, gate in inst.items():
                if isinstance(gate, _objs.FullDenseOp): typ = "IGATE"
                elif isinstance(gate, _objs.TPInstrumentOp): typ = "IGATE"  # ok b/c instrument itself is marked as TP
                elif isinstance(gate, _objs.StaticDenseOp): typ = "STATIC-IGATE"
                else:
                    _warnings.warn(
                        ("Non-standard gate of type {typ} cannot be described by"
                         "text format model files.  It will be read in as a"
                         "fully parameterized gate").format(typ=str(type(gate))))
                    typ = "IGATE"
                output.write(typ + ": " + str(label) + '\n')
                writeprop(output, "LiouvilleMx", gate.todense())
            output.write("END Instrument\n\n")

        if mdl.state_space_labels is not None:
            output.write("STATESPACE: " + str(mdl.state_space_labels) + "\n")
            # StateSpaceLabels.__str__ formats the output properly

        basisdim = mdl.basis.dim

        if basisdim is None:
            output.write("BASIS: %s\n" % mdl.basis.name)
        else:
            if mdl.basis.name not in ('std', 'pp', 'gm', 'qt'):  # a "fancy" basis
                assert(mdl.state_space_labels is not None), \
                    "Must set a Model's state space labels when using fancy a basis!"
                # don't write the dim - the state space labels will cover this.
                output.write("BASIS: %s\n" % mdl.basis.name)
            else:
                output.write("BASIS: %s %d\n" % (mdl.basis.name, basisdim))

        if isinstance(mdl.default_gauge_group, _objs.FullGaugeGroup):
            output.write("GAUGEGROUP: Full\n")
        elif isinstance(mdl.default_gauge_group, _objs.TPGaugeGroup):
            output.write("GAUGEGROUP: TP\n")
        elif isinstance(mdl.default_gauge_group, _objs.UnitaryGaugeGroup):
            output.write("GAUGEGROUP: Unitary\n")


def write_empty_protocol_data(edesign, dirname, sparse="auto", clobber_ok=False):
    """
    Write to a directory an experimental design (`edesign`) and the dataset
    template files needed to load in a :class:`ProtocolData` object, e.g.
    using the :function:`load_data_from_dir` function, after the template
    files are filled in.

    Parameters
    ----------
    edesign : ExperimentDesign
        The experiment design defining the circuits that need to be performed.

    dirname : str
        The *root* directory to write into.  This directory will have 'edesign'
        and 'data' subdirectories created beneath it.

    sparse : bool or "auto", optional
        If True, then the template data set(s) are written in a sparse-data
        format, i.e. in a format where not all the outcomes need to be given.
        If False, then a dense data format is used, where counts for *all*
        possible bit strings are given.  `"auto"` causes the sparse format
        to be used when the number of qubits is > 2.

    clobber_ok : bool, optional
        If True, then a template dataset file will be written even if a file
        of the same name already exists (this may overwrite existing data
        with an empty template file, so be careful!).

    Returns
    -------
    None
    """

    dirname = _pathlib.Path(dirname)
    data_dir = dirname / 'data'
    circuits = edesign.all_circuits_needing_data
    nQubits = "multiple" if edesign.qubit_labels == "multiple" else len(edesign.qubit_labels)
    if sparse == "auto":
        sparse = bool(nQubits == "multiple" or nQubits > 3)  # HARDCODED

    if sparse:
        header_str = "# Note: on each line, put comma-separated <outcome:count> items, i.e. 00110:23"
        nZeroCols = 0
    else:
        fstr = '{0:0%db} count' % nQubits
        nZeroCols = 2**nQubits
        header_str = "## Columns = " + ", ".join([fstr.format(i) for i in range(nZeroCols)])

    pth = data_dir / 'dataset.txt'
    if pth.exists() and clobber_ok is False:
        raise ValueError(("Template data file would clobber %s, which already exists!  Set `clobber_ok=True`"
                          " to allow overwriting." % pth))
    data_dir.mkdir(parents=True, exist_ok=True)

    from ..protocols import ProtocolData as _ProtocolData
    data = _ProtocolData(edesign, None)
    data.write(dirname)
    write_empty_dataset(pth, circuits, header_str, nZeroCols)


def fill_in_empty_dataset_with_fake_data(model, dataset_filename, nSamples,
                                         sampleError="multinomial", seed=None, randState=None,
                                         aliasDict=None, collisionAction="aggregate",
                                         recordZeroCnts=True, comm=None, memLimit=None, times=None,
                                         fixedColumnMode="auto"):
    """
    Fills in the text-format data set file `dataset_fileame` with simulated data counts using `model`.

    Parameters
    ----------
    model : Model
        the model to use to simulate the data.

    dataset_filename : strictly
        the path to the text-formatted data set file.

    rest_of_args : various
        same as :function:`pygsti.construction.generate_fake_data`.

    Returns
    -------
    DataSet
        The generated data set (also written in place of the template file).
    """
    from ..construction import generate_fake_data as _generate_fake_data
    ds_template = _loaders.load_dataset(dataset_filename, ignoreZeroCountLines=False, withTimes=False, verbosity=0)
    ds = _generate_fake_data(model, list(ds_template.keys()), nSamples,
                             sampleError, seed, randState, aliasDict,
                             collisionAction, recordZeroCnts, comm,
                             memLimit, times)
    if fixedColumnMode == "auto":
        fixedColumnMode = bool(len(ds_template.get_outcome_labels()) <= 8 and times is None)
    write_dataset(dataset_filename, ds, fixedColumnMode=fixedColumnMode)
    return ds
