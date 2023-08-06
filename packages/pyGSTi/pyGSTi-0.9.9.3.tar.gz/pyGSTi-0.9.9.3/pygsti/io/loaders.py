""" Functions for loading GST objects from text files."""
#***************************************************************************************************
# Copyright 2015, 2019 National Technology & Engineering Solutions of Sandia, LLC (NTESS).
# Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains certain rights
# in this software.
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
# in compliance with the License.  You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0 or in the LICENSE file in the root pyGSTi directory.
#***************************************************************************************************

import os as _os
import pathlib as _pathlib

from . import stdinput as _stdinput
from .. import objects as _objs
from . import metadir as _metadir


def load_dataset(filename, cache=False, collisionAction="aggregate",
                 recordZeroCnts=True, ignoreZeroCountLines=True,
                 withTimes="auto", verbosity=1):
    """
    Load a DataSet from a file.  First tries to load file as a
    saved DataSet object, then as a standard text-formatted DataSet.

    Parameters
    ----------
    filename : string
        The name of the file

    cache : bool, optional
        When set to True, a pickle file with the name filename + ".cache"
        is searched for and loaded instead of filename if it exists
        and is newer than filename.  If no cache file exists or one
        exists but it is older than filename, a cache file will be
        written after loading from filename.

    collisionAction : {"aggregate", "keepseparate"}
        Specifies how duplicate operation sequences should be handled.  "aggregate"
        adds duplicate-sequence counts, whereas "keepseparate" tags duplicate-
        sequence data with by appending a final "#<number>" operation label to the
        duplicated gate sequence.

    recordZeroCnts : bool, optional
        Whether zero-counts are actually recorded (stored) in the returned
        DataSet.  If False, then zero counts are ignored, except for potentially
        registering new outcome labels.  When reading from a cache file
        (using `cache==True`) this argument is ignored: the presence of zero-
        counts is dictated by the value of `recordZeroCnts` when the cache file
        was created.

    ignoreZeroCountLines : bool, optional
        Whether circuits for which there are no counts should be ignored
        (i.e. omitted from the DataSet) or not.

    withTimes : bool or "auto", optional
        Whether to the time-stamped data format should be read in.  If
        "auto", then the time-stamped format is allowed but not required on a
        per-circuit basis (so the dataset can contain both formats).  Typically
        you only need to set this to False when reading in a template file.

    verbosity : int, optional
        If zero, no output is shown.  If greater than zero,
        loading progress is shown.

    Returns
    -------
    DataSet
    """

    printer = _objs.VerbosityPrinter.build_printer(verbosity)
    try:
        # a saved Dataset object is ok
        ds = _objs.DataSet(fileToLoadFrom=filename)
    except:

        #Parser functions don't take a VerbosityPrinter yet, and so
        # always output to stdout (TODO)
        bToStdout = (printer.verbosity > 0 and printer.filename is None)

        if cache:
            #bReadCache = False
            cache_filename = filename + ".cache"
            if _os.path.exists(cache_filename) and \
               _os.path.getmtime(filename) < _os.path.getmtime(cache_filename):
                try:
                    printer.log("Loading from cache file: %s" % cache_filename)
                    ds = _objs.DataSet(fileToLoadFrom=cache_filename)
                    return ds
                except: print("WARNING: Failed to load from cache file")  # pragma: no cover
            else:
                printer.log("Cache file not found or is tool old -- one will"
                            + "be created after loading is completed")

            # otherwise must use standard dataset file format
            parser = _stdinput.StdInputParser()
            ds = parser.parse_datafile(filename, bToStdout,
                                       collisionAction=collisionAction,
                                       recordZeroCnts=recordZeroCnts,
                                       ignoreZeroCountLines=ignoreZeroCountLines,
                                       withTimes=withTimes)

            printer.log("Writing cache file (to speed future loads): %s"
                        % cache_filename)
            ds.save(cache_filename)
        else:
            # otherwise must use standard dataset file format
            parser = _stdinput.StdInputParser()
            ds = parser.parse_datafile(filename, bToStdout,
                                       collisionAction=collisionAction,
                                       recordZeroCnts=recordZeroCnts,
                                       ignoreZeroCountLines=ignoreZeroCountLines,
                                       withTimes=withTimes)
        return ds


def load_multidataset(filename, cache=False, collisionAction="aggregate",
                      recordZeroCnts=True, verbosity=1):
    """
    Load a MultiDataSet from a file.  First tries to load file as a
    saved MultiDataSet object, then as a standard text-formatted MultiDataSet.

    Parameters
    ----------
    filename : string
        The name of the file

    cache : bool, optional
        When set to True, a pickle file with the name filename + ".cache"
        is searched for and loaded instead of filename if it exists
        and is newer than filename.  If no cache file exists or one
        exists but it is older than filename, a cache file will be
        written after loading from filename.

    collisionAction : {"aggregate", "keepseparate"}
        Specifies how duplicate operation sequences should be handled.  "aggregate"
        adds duplicate-sequence counts, whereas "keepseparate" tags duplicate-
        sequence data with by appending a final "#<number>" operation label to the
        duplicated gate sequence.

    recordZeroCnts : bool, optional
        Whether zero-counts are actually recorded (stored) in the returned
        MultiDataSet.  If False, then zero counts are ignored, except for
        potentially registering new outcome labels.  When reading from a cache
        file (using `cache==True`) this argument is ignored: the presence of
        zero-counts is dictated by the value of `recordZeroCnts` when the cache
        file was created.

    verbosity : int, optional
        If zero, no output is shown.  If greater than zero,
        loading progress is shown.


    Returns
    -------
    MultiDataSet
    """

    printer = _objs.VerbosityPrinter.build_printer(verbosity)
    try:
        # a saved MultiDataset object is ok
        mds = _objs.MultiDataSet(fileToLoadFrom=filename)
    except:

        #Parser functions don't take a VerbosityPrinter yet, and so
        # always output to stdout (TODO)
        bToStdout = (printer.verbosity > 0 and printer.filename is None)

        if cache:
            # bReadCache = False
            cache_filename = filename + ".cache"
            if _os.path.exists(cache_filename) and \
               _os.path.getmtime(filename) < _os.path.getmtime(cache_filename):
                try:
                    printer.log("Loading from cache file: %s" % cache_filename)
                    mds = _objs.MultiDataSet(fileToLoadFrom=cache_filename)
                    return mds
                except: print("WARNING: Failed to load from cache file")  # pragma: no cover
            else:
                printer.log("Cache file not found or is too old -- one will be"
                            + "created after loading is completed")

            # otherwise must use standard dataset file format
            parser = _stdinput.StdInputParser()
            mds = parser.parse_multidatafile(filename, bToStdout,
                                             collisionAction=collisionAction,
                                             recordZeroCnts=recordZeroCnts)

            printer.log("Writing cache file (to speed future loads): %s"
                        % cache_filename)
            mds.save(cache_filename)

        else:
            # otherwise must use standard dataset file format
            parser = _stdinput.StdInputParser()
            mds = parser.parse_multidatafile(filename, bToStdout,
                                             collisionAction=collisionAction,
                                             recordZeroCnts=recordZeroCnts)
    return mds


def load_tddataset(filename, cache=False, recordZeroCnts=True):
    """
    Load time-dependent (time-stamped) data as a DataSet.

    Parameters
    ----------
    filename : string
        The name of the file

    cache : bool, optional
        Reserved to perform caching similar to `load_dataset`.  Currently
        this argument doesn't do anything.

    recordZeroCnts : bool, optional
        Whether zero-counts are actually recorded (stored) in the returned
        DataSet.  If False, then zero counts are ignored, except for
        potentially registering new outcome labels.

    Returns
    -------
    DataSet
    """
    parser = _stdinput.StdInputParser()
    tdds = parser.parse_tddatafile(filename, recordZeroCnts=recordZeroCnts)
    return tdds


def load_model(filename):
    """
    Load a Model from a file, formatted using the
    standard text-format for models.

    Parameters
    ----------
    filename : string
        The name of the file

    Returns
    -------
    Model
    """
    return _stdinput.read_model(filename)


def load_circuit_dict(filename):
    """
    Load a operation sequence dictionary from a file, formatted
    using the standard text-format.

    Parameters
    ----------
    filename : string
        The name of the file.

    Returns
    -------
    Dictionary with keys = operation sequence labels and
      values = Circuit objects.
    """
    std = _stdinput.StdInputParser()
    return std.parse_dictfile(filename)


def load_circuit_list(filename, readRawStrings=False, line_labels='auto', num_lines=None):
    """
    Load a operation sequence list from a file, formatted
    using the standard text-format.

    Parameters
    ----------
    filename : string
        The name of the file

    readRawStrings : boolean
        If True, operation sequences are not converted
        to tuples of operation labels.

    line_labels : iterable, optional
        The (string valued) line labels used to initialize :class:`Circuit`
        objects when line label information is absent from the one-line text
        representation contained in `filename`.  If `'auto'`, then line labels
        are taken to be the list of all state-space labels present in the
        circuit's layers.  If there are no such labels then the special value
        `'*'` is used as a single line label.

    num_lines : int, optional
        Specify this instead of `line_labels` to set the latter to the
        integers between 0 and `num_lines-1`.

    Returns
    -------
    list of Circuit objects
    """
    if readRawStrings:
        rawList = []
        with open(str(filename), 'r') as circuitlist:
            for line in circuitlist:
                if len(line.strip()) == 0: continue
                if len(line) == 0 or line[0] == '#': continue
                rawList.append(line.strip())
        return rawList
    else:
        std = _stdinput.StdInputParser()
        return std.parse_stringfile(filename, line_labels, num_lines)


def load_protocol_from_dir(dirname, comm=None):
    """
    Load a :class:`Protocol` from a directory on disk.

    Parameters
    ----------
    dirname : string
        Directory name.

    comm : mpi4py.MPI.Comm, optional
        When not ``None``, an MPI communicator used to synchronize file access.

    Returns
    -------
    Protocol
    """
    dirname = _pathlib.Path(dirname)
    return _metadir.cls_from_meta_json(dirname).from_dir(dirname)


def load_edesign_from_dir(dirname, comm=None):
    """
    Load a :class:`ExperimentDesign` from a directory on disk.

    Parameters
    ----------
    dirname : string
        Directory name.

    comm : mpi4py.MPI.Comm, optional
        When not ``None``, an MPI communicator used to synchronize file access.

    Returns
    -------
    ExperimentDesign
    """
    dirname = _pathlib.Path(dirname)
    return _metadir.cls_from_meta_json(dirname / 'edesign').from_dir(dirname)


def load_data_from_dir(dirname, comm=None):
    """
    Load a :class:`ProtocolData` from a directory on disk.

    Parameters
    ----------
    dirname : string
        Directory name.

    comm : mpi4py.MPI.Comm, optional
        When not ``None``, an MPI communicator used to synchronize file access.

    Returns
    -------
    ProtocolData
    """
    dirname = _pathlib.Path(dirname)
    return _metadir.cls_from_meta_json(dirname / 'data').from_dir(dirname)


def load_results_from_dir(dirname, name=None, preloaded_data=None, comm=None):
    """
    Load a :class:`ProtocolResults` or :class:`ProtocolsResultsDir` from a
    directory on disk (depending on whether `name` is given).

    Parameters
    ----------
    dirname : string
        Directory name.  This should be a "base" directory, containing
        subdirectories like "edesign", "data", and "results"

    name : string or None
        The 'name' of a particular :class:`ProtocolResults` object, which
        is a sub-directory beneath `dirname/results/`.  If None, then *all*
        the results (all names) at the given base-directory are loaded and
        returned as a :class:`ProtocolResultsDir` object.

    preloaded_data : ProtocolData, optional
        The data object belonging to the to-be-loaded results, in cases
        when this has been loaded already (only use this if you know what
        you're doing).

    comm : mpi4py.MPI.Comm, optional
        When not ``None``, an MPI communicator used to synchronize file access.

    Returns
    -------
    ProtocolResults or ProtocolResultsDir
    """
    from ..protocols import ProtocolResultsDir as _ProtocolResultsDir
    dirname = _pathlib.Path(dirname)
    results_dir = dirname / 'results'
    if name is None:  # then it's a directory object
        cls = _metadir.cls_from_meta_json(results_dir) if (results_dir / 'meta.json').exists() \
            else _ProtocolResultsDir  # default if no meta.json (if only a results obj has been written inside dir)
        return cls.from_dir(dirname)
    else:  # it's a ProtocolResults object
        return _metadir.cls_from_meta_json(results_dir / name).from_dir(dirname, name, preloaded_data)
