""" Report generation functions. """
#***************************************************************************************************
# Copyright 2015, 2019 National Technology & Engineering Solutions of Sandia, LLC (NTESS).
# Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains certain rights
# in this software.
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
# in compliance with the License.  You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0 or in the LICENSE file in the root pyGSTi directory.
#***************************************************************************************************

import pickle as _pickle
import os as _os
import time as _time
import collections as _collections
import warnings as _warnings
import zipfile as _zipfile
import numpy as _np

from ..objects.verbosityprinter import VerbosityPrinter as _VerbosityPrinter
from ..objects import DataComparator as _DataComparator
from ..tools import timed_block as _timed_block

from ..tools.mpitools import distribute_indices as _distribute_indices
from ..tools.legacytools import deprecated_fn as _deprecated_fn

from .. import tools as _tools
from .. import objects as _objs
from .. import _version

from . import workspace as _ws
from . import autotitle as _autotitle
from . import merge_helpers as _merge
from . import reportables as _reportables
from . import Report as _Report
from . import section as _section
from .notebook import Notebook as _Notebook
from ..objects.label import Label as _Lbl
from ..modelpacks import RBModelPack as _RBModelPack

#maybe import these from drivers.longsequence so they stay synced?
ROBUST_SUFFIX_LIST = [".robust", ".Robust", ".robust+", ".Robust+"]  # ".wildcard" (not a separate estimate anymore)
DEFAULT_BAD_FIT_THRESHOLD = 2.0


def _add_new_labels(running_lbls, current_lbls):
    """
    Simple routine to add current-labels to a list of
    running-labels without introducing duplicates and
    preserving order as best we can.
    """
    if running_lbls is None:
        return current_lbls[:]  # copy!
    elif running_lbls != current_lbls:
        for lbl in current_lbls:
            if lbl not in running_lbls:
                running_lbls.append(lbl)
    return running_lbls


def _add_new_estimate_labels(running_lbls, estimates, combine_robust):
    """
    Like _add_new_labels but perform robust-suffix processing.

    In particular, if `combine_robust == True` then do not add
    labels which have a ".robust" counterpart.
    """
    current_lbls = list(estimates.keys())

    def _add_lbl(lst, lbl):
        if combine_robust and any([(lbl + suffix in current_lbls)
                                   for suffix in ROBUST_SUFFIX_LIST]):
            return  # don't add label
        lst.append(lbl)  # add label

    if running_lbls is None:
        running_lbls = []

    if running_lbls != current_lbls:
        for lbl in current_lbls:
            if lbl not in running_lbls:
                _add_lbl(running_lbls, lbl)

    return running_lbls


#def _robust_estimate_has_same_models(estimates, est_lbl):
#    lbl_robust = est_lbl+ROBUST_SUFFIX
#    if lbl_robust not in estimates: return False #no robust estimate
#
#    for mdl_lbl in list(estimates[est_lbl].goparameters.keys()) \
#        + ['final iteration estimate']:
#        if mdl_lbl not in estimates[lbl_robust].models:
#            return False #robust estimate is missing mdl_lbl!
#
#        mdl = estimates[lbl_robust].models[mdl_lbl]
#        if estimates[est_lbl].models[mdl_lbl].frobeniusdist(mdl) > 1e-8:
#            return False #model mismatch!
#
#    return True

def _get_viewable_crf(est, est_lbl, mdl_lbl, verbosity=0):
    printer = _VerbosityPrinter.build_printer(verbosity)

    if est.has_confidence_region_factory(mdl_lbl, 'final'):
        crf = est.get_confidence_region_factory(mdl_lbl, 'final')
        if crf.can_construct_views():
            return crf
        else:
            printer.log(
                ("Note: Confidence interval factory for {estlbl}.{gslbl} "
                 "model exists but cannot create views.  This could be "
                 "because you forgot to create a Hessian *projection*"
                 ).format(estlbl=est_lbl, gslbl=mdl_lbl))
    else:
        printer.log(
            ("Note: no factory to compute confidence "
             "intervals for the '{estlbl}.{gslbl}' model."
             ).format(estlbl=est_lbl, gslbl=mdl_lbl))

    return None


def create_offline_zip(outputDir="."):
    """
    Creates a zip file containing the a directory ("offline") of files
    need to display "offline" reports (generated with `connected=False`).

    For offline reports to display, the "offline" folder must be placed
    in the same directory as the report's HTML file.  This function can
    be used to easily obtain a copy of the offline folder for the purpose
    of sharing offline reports with other people.  If you're just creating
    your own offline reports using pyGSTi, the offline folder is
    automatically copied into it's proper position - so you don't need
    to call this function.

    Parameters
    ----------
    outputDir : str, optional
        The directory in which "offline.zip" should be place.

    Returns
    -------
    None
    """
    templatePath = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)),
                                 "templates")

    zipFName = _os.path.join(outputDir, "offline.zip")
    zipHandle = _zipfile.ZipFile(zipFName, 'w', _zipfile.ZIP_DEFLATED)
    for root, _, files in _os.walk(_os.path.join(templatePath, "offline")):
        for f in files:
            fullPath = _os.path.join(root, f)
            zipHandle.write(fullPath, _os.path.relpath(fullPath, templatePath))
    zipHandle.close()


# TODO remove
def _set_toggles(results_dict, brevity, combine_robust):
    #Determine when to get circuit weight (scaling) values and show via
    # ColorBoxPlots below by checking whether any estimate has "weights"
    # parameter (a dict) with > 0 entries.
    toggles = {}

    toggles["ShowScaling"] = False
    toggles["ShowUnmodeledError"] = False
    for res in results_dict.values():
        for est in res.estimates.values():
            weights = est.parameters.get("weights", None)
            if (weights is not None and len(weights) > 0):
                toggles["ShowScaling"] = True
            if est.parameters.get("unmodeled_error", None):
                toggles["ShowUnmodeledError"] = True

    toggles['BrevityLT1'] = bool(brevity < 1)
    toggles['BrevityLT2'] = bool(brevity < 2)
    toggles['BrevityLT3'] = bool(brevity < 3)
    toggles['BrevityLT4'] = bool(brevity < 4)

    toggles['CombineRobust'] = bool(combine_robust)
    return toggles


def _create_master_switchboard(ws, results_dict, confidenceLevel,
                               nmthreshold, printer, fmt,
                               combine_robust, idt_results_dict=None, embed_figures=True):
    """
    Creates the "master switchboard" used by several of the reports
    """

    if isinstance(results_dict, _collections.OrderedDict):
        dataset_labels = list(results_dict.keys())
    else:
        dataset_labels = sorted(list(results_dict.keys()))

    est_labels = None
    gauge_opt_labels = None
    Ls = None

    for results in results_dict.values():
        est_labels = _add_new_estimate_labels(est_labels, results.estimates,
                                              combine_robust)
        Ls = _add_new_labels(Ls, results.circuit_structs['final'].Ls)
        for est in results.estimates.values():
            gauge_opt_labels = _add_new_labels(gauge_opt_labels,
                                               list(est.goparameters.keys()))

    Ls = list(sorted(Ls))  # make sure Ls are sorted in increasing order

    # XXX i suspect it's not actually this easy
    # if fmt == "latex" and len(Ls) > 0:
    #     swLs = [Ls[-1]]  # "switched Ls" = just take the single largest L
    # else:
    #     swLs = Ls  # switch over all Ls
    swLs = Ls

    multidataset = bool(len(dataset_labels) > 1)
    multiest = bool(len(est_labels) > 1)
    multiGO = bool(len(gauge_opt_labels) > 1)
    #multiL = bool(len(swLs) > 1)

    switchBd = ws.Switchboard(
        ["Dataset", "Estimate", "Gauge-Opt", "max(L)"],
        [dataset_labels, est_labels, gauge_opt_labels, list(map(str, swLs))],
        ["dropdown", "dropdown", "buttons", "slider"], [0, 0, 0, len(swLs) - 1],
        show=[multidataset, multiest, multiGO, False],  # "global" switches only + gauge-opt (OK if doesn't apply)
        use_loadable_items=embed_figures
    )

    switchBd.add("ds", (0,))
    switchBd.add("prepStrs", (0,))
    switchBd.add("effectStrs", (0,))
    switchBd.add("strs", (0,))
    switchBd.add("germs", (0,))

    switchBd.add("eff_ds", (0, 1))
    switchBd.add("modvi_ds", (0, 1))
    switchBd.add("wildcardBudget", (0, 1))
    switchBd.add("wildcardBudgetOptional", (0, 1))
    switchBd.add("scaledSubMxsDict", (0, 1))
    switchBd.add("gsTarget", (0, 1))
    switchBd.add("params", (0, 1))
    switchBd.add("objective", (0, 1))
    switchBd.add("objective_tvd_tuple", (0, 1))
    switchBd.add("objective_modvi", (0, 1))
    switchBd.add("mpc", (0, 1))
    switchBd.add("mpc_modvi", (0, 1))
    switchBd.add("clifford_compilation", (0, 1))
    switchBd.add("meta_stdout", (0, 1))
    switchBd.add("profiler", (0, 1))

    switchBd.add("gsGIRep", (0, 1))
    switchBd.add("gsGIRepEP", (0, 1))
    switchBd.add("gsFinal", (0, 1, 2))
    switchBd.add("gsEvalProjected", (0, 1, 2))
    switchBd.add("gsTargetAndFinal", (0, 1, 2))  # general only!
    switchBd.add("goparams", (0, 1, 2))
    switchBd.add("gsL", (0, 1, 3))
    switchBd.add("gsL_modvi", (0, 1, 3))
    switchBd.add("gss", (0, 3))
    switchBd.add("gssFinal", (0,))
    switchBd.add("gsAllL", (0, 1))
    switchBd.add("gsAllL_modvi", (0, 1))
    switchBd.add("gssAllL", (0,))
    switchBd.add("gsFinalGrid", (2,))

    switchBd.add("idtresults", (0,))

    if confidenceLevel is not None:
        switchBd.add("cri", (0, 1, 2))
        switchBd.add("criGIRep", (0, 1))

    for d, dslbl in enumerate(dataset_labels):
        results = results_dict[dslbl]

        switchBd.ds[d] = results.dataset
        switchBd.prepStrs[d] = results.circuit_lists['prep fiducials']
        switchBd.effectStrs[d] = results.circuit_lists['meas fiducials']
        switchBd.strs[d] = (results.circuit_lists['prep fiducials'],
                            results.circuit_lists['meas fiducials'])
        switchBd.germs[d] = results.circuit_lists['germs']

        switchBd.gssFinal[d] = results.circuit_structs['final']
        for iL, L in enumerate(swLs):  # allow different results to have different Ls
            if L in results.circuit_structs['final'].Ls:
                k = results.circuit_structs['final'].Ls.index(L)
                switchBd.gss[d, iL] = results.circuit_structs['iteration'][k]
        switchBd.gssAllL[d] = results.circuit_structs['iteration']

        if idt_results_dict is not None:
            switchBd.idtresults[d] = idt_results_dict.get(dslbl, None)

        for i, lbl in enumerate(est_labels):
            est = results.estimates.get(lbl, None)
            if est is None: continue

            for suffix in ROBUST_SUFFIX_LIST:
                if combine_robust and lbl.endswith(suffix):
                    est_modvi = results.estimates.get(lbl[:-len(suffix)], est)
                    break
            else:
                est_modvi = est

            def rpt_objective(opt_objective):
                """ If optimized using just LGST, compute logl values """
                if opt_objective == "lgst": return "logl"
                else: return opt_objective

            switchBd.params[d, i] = est.parameters
            switchBd.objective[d, i] = rpt_objective(est.parameters['objective'])
            switchBd.objective_tvd_tuple[d, i] = (rpt_objective(est.parameters['objective']), 'tvd')
            switchBd.objective_modvi[d, i] = rpt_objective(est_modvi.parameters['objective'])
            if est.parameters['objective'] == "logl":
                switchBd.mpc[d, i] = est.parameters['minProbClip']
                switchBd.mpc_modvi[d, i] = est_modvi.parameters['minProbClip']
            elif est.parameters['objective'] == "chi2":
                switchBd.mpc[d, i] = est.parameters['minProbClipForWeighting']
                switchBd.mpc_modvi[d, i] = est_modvi.parameters['minProbClipForWeighting']
            else:  # "lgst" - just use defaults for logl
                switchBd.mpc[d, i] = 1e-4
                switchBd.mpc_modvi[d, i] = 1e-4
            switchBd.clifford_compilation[d, i] = est.parameters.get("clifford compilation", 'auto')
            if switchBd.clifford_compilation[d, i] == 'auto':
                switchBd.clifford_compilation[d, i] = find_std_clifford_compilation(
                    est.models['target'], printer)

            switchBd.profiler[d, i] = est_modvi.parameters.get('profiler', None)
            switchBd.meta_stdout[d, i] = est_modvi.meta.get('stdout', [('LOG', 1, "No standard output recorded")])

            GIRepLbl = 'final iteration estimate'  # replace with a gauge-opt label if it has a CI factory
            if confidenceLevel is not None:
                if _get_viewable_crf(est, lbl, GIRepLbl) is None:
                    for l in gauge_opt_labels:
                        if _get_viewable_crf(est, lbl, l) is not None:
                            GIRepLbl = l; break

            # NOTE on modvi_ds (the dataset used in model violation plots)
            # if combine_robust is True, modvi_ds is the unscaled dataset.
            # if combine_robust is False, modvi_ds is the effective dataset
            #     for the estimate (potentially just the unscaled one)

            #if this estimate uses robust scaling or wildcard budget
            NA = ws.NotApplicable()
            if est.parameters.get("weights", None):
                effds, scale_subMxs = est.get_effective_dataset(True)
                switchBd.eff_ds[d, i] = effds
                switchBd.scaledSubMxsDict[d, i] = {'scaling': scale_subMxs, 'scaling.colormap': "revseq"}
                switchBd.modvi_ds[d, i] = results.dataset if combine_robust else effds
            else:
                switchBd.modvi_ds[d, i] = results.dataset
                switchBd.eff_ds[d, i] = NA
                switchBd.scaledSubMxsDict[d, i] = NA

            switchBd.wildcardBudgetOptional[d, i] = est.parameters.get("unmodeled_error", None)
            if est.parameters.get("unmodeled_error", None):
                switchBd.wildcardBudget[d, i] = est.parameters['unmodeled_error']
            else:
                switchBd.wildcardBudget[d, i] = NA

            switchBd.gsTarget[d, i] = est.models['target']
            switchBd.gsGIRep[d, i] = est.models[GIRepLbl]
            try:
                switchBd.gsGIRepEP[d, i] = _tools.project_to_target_eigenspace(est.models[GIRepLbl],
                                                                               est.models['target'])
            except AttributeError:  # Implicit models don't support everything, like set_all_parameterizations
                switchBd.gsGIRepEP[d, i] = None
            except AssertionError:  # if target is badly off, this can fail with an imaginary part assertion
                switchBd.gsGIRepEP[d, i] = None

            switchBd.gsFinal[d, i, :] = [est.models.get(l, NA) for l in gauge_opt_labels]
            switchBd.gsTargetAndFinal[d, i, :] = \
                [[est.models['target'], est.models[l]] if (l in est.models) else NA
                 for l in gauge_opt_labels]
            switchBd.goparams[d, i, :] = [est.goparameters.get(l, NA) for l in gauge_opt_labels]

            for iL, L in enumerate(swLs):  # allow different results to have different Ls
                if L in results.circuit_structs['final'].Ls:
                    k = results.circuit_structs['final'].Ls.index(L)
                    switchBd.gsL[d, i, iL] = est.models['iteration estimates'][k]
                    switchBd.gsL_modvi[d, i, iL] = est_modvi.models['iteration estimates'][k]
            switchBd.gsAllL[d, i] = est.models['iteration estimates']
            switchBd.gsAllL_modvi[d, i] = est_modvi.models['iteration estimates']

            if confidenceLevel is not None:
                misfit_sigma = est.misfit_sigma(use_accurate_Np=True)

                for il, l in enumerate(gauge_opt_labels):
                    if l in est.models:
                        switchBd.cri[d, i, il] = None  # default
                        crf = _get_viewable_crf(est, lbl, l, printer - 2)

                        if crf is not None:
                            #Check whether we should use non-Markovian error bars:
                            # If fit is bad, check if any reduced fits were computed
                            # that we can use with in-model error bars.  If not, use
                            # experimental non-markovian error bars.
                            region_type = "normal" if misfit_sigma <= nmthreshold \
                                          else "non-markovian"
                            switchBd.cri[d, i, il] = crf.view(confidenceLevel, region_type)

                    else: switchBd.cri[d, i, il] = NA

                # "Gauge Invariant Representation" model
                # If we can't compute CIs for this, ignore SILENTLY, since any
                #  relevant warnings/notes should have been given above.
                switchBd.criGIRep[d, i] = None  # default
                crf = _get_viewable_crf(est, lbl, GIRepLbl)
                if crf is not None:
                    region_type = "normal" if misfit_sigma <= nmthreshold \
                                  else "non-markovian"
                    switchBd.criGIRep[d, i] = crf.view(confidenceLevel, region_type)

    results_list = [results_dict[dslbl] for dslbl in dataset_labels]
    for i, gokey in enumerate(gauge_opt_labels):
        if multidataset:
            switchBd.gsFinalGrid[i] = [
                [(res.estimates[el].models.get(gokey, None)
                  if el in res.estimates else None) for el in est_labels]
                for res in results_list]
        else:
            switchBd.gsFinalGrid[i] = [
                (results_list[0].estimates[el].models.get(gokey, None)
                 if el in results_list[0].estimates else None) for el in est_labels]

    if multidataset:
        switchBd.add_unswitched('gsTargetGrid', [
            [(res.estimates[el].models.get('target', None)
              if el in res.estimates else None) for el in est_labels]
            for res in results_list])
    else:
        switchBd.add_unswitched('gsTargetGrid', [
            (results_list[0].estimates[el].models.get('target', None)
             if el in results_list[0].estimates else None) for el in est_labels])

    return switchBd, dataset_labels, est_labels, gauge_opt_labels, Ls, swLs


def _construct_idtresults(idtIdleOp, idtPauliDicts, gst_results_dict, printer):
    """
    Constructs a dictionary of idle tomography results, parallel
    to the GST results in `gst_results_dict`, where possible.
    """
    if idtPauliDicts is None:
        return {}

    idt_results_dict = {}
    GiStr = _objs.Circuit((idtIdleOp,))

    from ..extras import idletomography as _idt
    autodict = bool(idtPauliDicts == "auto")
    for ky, results in gst_results_dict.items():

        if autodict:
            for est in results.estimates.values():
                if 'target' in est.models:
                    idt_target = est.models['target']
                    break
            else: continue  # can't find any target models
            idtPauliDicts = _idt.determine_paulidicts(idt_target)
            if idtPauliDicts is None:
                continue  # automatic creation failed -> skip

        gss = results.circuit_structs['final']
        if GiStr not in gss.germs: continue

        try:  # to get a dimension -> nQubits
            estLabels = list(results.estimates.keys())
            estimate0 = results.estimates[estLabels[0]]
            dim = estimate0.models['target'].dim
            nQubits = int(round(_np.log2(dim) // 2))
            idStr = ('Gi',) if 'Gi' in estimate0.models['target'].get_primitive_op_labels() else ((),)
        except:
            printer.log(" ! Skipping idle tomography on %s dataset (can't get # qubits) !" % ky)
            continue  # skip if we can't get dimension

        maxLengths = gss.Ls
        # just use "L0" (first maxLength) - all should have same fidpairs
        plaq = gss.get_plaquette(maxLengths[0], GiStr)
        pauli_fidpairs = _idt.fidpairs_to_pauli_fidpairs(plaq.fidpairs, idtPauliDicts, nQubits)
        idt_advanced = {'pauli_fidpairs': pauli_fidpairs, 'jacobian mode': "together"}
        printer.log(" * Running idle tomography on %s dataset *" % ky)
        idtresults = _idt.do_idle_tomography(nQubits, results.dataset, maxLengths, idtPauliDicts,
                                             maxweight=2,  # HARDCODED for now (FUTURE)
                                             idle_string=idStr, advancedOptions=idt_advanced)
        idt_results_dict[ky] = idtresults

    return idt_results_dict


def _create_single_metric_switchboard(ws, results_dict, bGaugeInv,
                                      dataset_labels, est_labels=None, embed_figures=True):
    op_labels = None
    for results in results_dict.values():
        for est in results.estimates.values():
            if 'target' in est.models:
                op_labels = _add_new_labels(op_labels,
                                            list(est.models['target'].operations.keys()))

    if bGaugeInv:
        metric_abbrevs = ["evinf", "evagi", "evnuinf", "evnuagi", "evdiamond",
                          "evnudiamond"]
    else:
        metric_abbrevs = ["inf", "agi", "trace", "diamond", "nuinf", "nuagi",
                          "frob"]
    metric_names = [_reportables.info_of_opfn_by_name(abbrev)[0].replace('|', ' ')
                    for abbrev in metric_abbrevs]

    if len(dataset_labels) > 1:  # multidataset
        metric_switchBd = ws.Switchboard(
            ["Metric", "Operation"], [metric_names, op_labels],
            ["dropdown", "dropdown"], [0, 0], show=[True, True],
            use_loadable_items=embed_figures)
        metric_switchBd.add("opLabel", (1,))
        metric_switchBd.add("metric", (0,))
        metric_switchBd.add("cmpTableTitle", (0, 1))

        metric_switchBd.opLabel[:] = op_labels
        for i, gl in enumerate(op_labels):
            metric_switchBd.cmpTableTitle[:, i] = ["%s %s" % (gl, nm) for nm in metric_names]

    else:
        metric_switchBd = ws.Switchboard(
            ["Metric"], [metric_names],
            ["dropdown"], [0], show=[True],
            use_loadable_items=embed_figures)
        metric_switchBd.add("metric", (0,))
        metric_switchBd.add("cmpTableTitle", (0,))
        metric_switchBd.cmpTableTitle[:] = metric_names

    metric_switchBd.metric[:] = metric_abbrevs

    return metric_switchBd


@_deprecated_fn('pygsti.report.construct_standard_report(...).write_html(...)')
def create_general_report(results, filename, title="auto",
                          confidenceLevel=None,
                          linlogPercentile=5, errgen_type="logGTi",
                          nmthreshold=50, precision=None,
                          comm=None, ws=None, auto_open=False,
                          cachefile=None, brief=False, connected=False,
                          link_to=None, resizable=True, autosize='initial',
                          verbosity=1):
    """ DEPRECATED: use pygsti.report.create_standard_report(...)

    .. deprecated:: v0.9.9
        `create_general_report` will be removed in the next major release of pyGSTi. It is replaced by
        `construct_standard_report`, which returns a :class:`Report` object.
    """
    _warnings.warn(
        ('create_general_report(...) will be removed from pyGSTi.\n'
         '  This function only ever existed in beta versions and will\n'
         '  be removed completely soon.  Please update this call with:\n'
         '  pygsti.report.create_standard_report(...).write_html(...)\n'))


@_deprecated_fn('construct_standard_report(...).write_html(...)')
def create_standard_report(results, filename, title="auto",
                           confidenceLevel=None, comm=None, ws=None,
                           auto_open=False, link_to=None, brevity=0,
                           advancedOptions=None, verbosity=1):
    """
    Create a "standard" GST report, containing details about each estimate
    in `results` individually.

    Either a PDF or HTML report is generated, based on whether `filename` ends
    in ".pdf" or not.  In the richer HTML-mode, switches (drop-down boxes,
    buttons, etc.) allow the viewer to choose which estimate is displayed.  The
    estimates in multiple :class:`Results` objects can be viewed by providing
    a dictionary of `Results` objects as the `results` argument.  Note that
    when comparing many estimates it is often more convenient to view the report
    generated by :func:`create_comparison_report`, which is organized for this
    purpose.

    In PDF-mode this interactivity is not possible and so `results` may contain
    just a *single* estimate.  The chief advantage of this more limited mode
    is that is produces a highly-portable and self-contained PDF file.


    Parameters
    ----------
    results : Results
        An object which represents the set of results from one *or more* GST
        estimation runs, typically obtained from running
        :func:`do_long_sequence_gst` or :func:`do_stdpractice_gst`, OR a
        dictionary of such objects, representing multiple GST runs to be
        compared (typically all with *different* data sets). The keys of this
        dictionary are used to label different data sets that are selectable
        in the report.

    filename : string, optional
       The output filename where the report file(s) will be saved.  If
       None, then no output file is produced (but returned Workspace
       still caches all intermediate results).

    title : string, optional
       The title of the report.  "auto" causes a random title to be
       generated (which you may or may not like).

    confidenceLevel : int, optional
       If not None, then the confidence level (between 0 and 100) used in
       the computation of confidence regions/intervals. If None, no
       confidence regions or intervals are computed.

    comm : mpi4py.MPI.Comm, optional
        When not None, an MPI communicator for distributing the computation
        across multiple processors.

    ws : Workspace, optional
        The workspace used as a scratch space for performing the calculations
        and visualizations required for this report.  If you're creating
        multiple reports with similar tables, plots, etc., it may boost
        performance to use a single Workspace for all the report generation.

    auto_open : bool, optional
        If True, automatically open the report in a web browser after it
        has been generated.

    link_to : list, optional
        If not None, a list of one or more items from the set
        {"tex", "pdf", "pkl"} indicating whether or not to
        create and include links to Latex, PDF, and Python pickle
        files, respectively.  "tex" creates latex source files for
        tables; "pdf" renders PDFs of tables and plots ; "pkl" creates
        Python versions of plots (pickled python data) and tables (pickled
        pandas DataFrams).

    brevity : int, optional
        Amount of detail to include in the report.  Larger values mean smaller
        "more briefr" reports, which reduce generation time, load time, and
        disk space consumption.  In particular:

        - 1: Plots showing per-sequences quantities disappear at brevity=1
        - 2: Reference sections disappear at brevity=2
        - 3: Germ-level estimate tables disappear at brevity=3
        - 4: Everything but summary figures disappears at brevity=4

    advancedOptions : dict, optional
        A dictionary of advanced options for which the default values are usually
        are fine.  Here are the possible keys of `advancedOptions`:

        - connected : bool, optional
            Whether output HTML should assume an active internet connection.  If
            True, then the resulting HTML file size will be reduced because it
            will link to web resources (e.g. CDN libraries) instead of embedding
            them.

        - cachefile : str, optional
            filename with cached workspace results

        - linlogPercentile : float, optional
            Specifies the colorscale transition point for any logL or chi2 color
            box plots.  The lower `(100 - linlogPercentile)` percentile of the
            expected chi2 distribution is shown in a linear grayscale, and the
            top `linlogPercentile` is shown on a logarithmic colored scale.

        - errgen_type: {"logG-logT", "logTiG", "logGTi"}
            The type of error generator to compute.  Allowed values are:

            - "logG-logT" : errgen = log(gate) - log(target_op)
            - "logTiG" : errgen = log( dot(inv(target_op), gate) )
            - "logGTi" : errgen = log( dot(gate, inv(target_op)) )

        - nmthreshold : float, optional
            The threshold, in units of standard deviations, that triggers the
            usage of non-Markovian error bars.  If None, then non-Markovian
            error bars are never computed.

        - precision : int or dict, optional
            The amount of precision to display.  A dictionary with keys
            "polar", "sci", and "normal" can separately specify the
            precision for complex angles, numbers in scientific notation, and
            everything else, respectively.  If an integer is given, it this
            same value is taken for all precision types.  If None, then
            `{'normal': 6, 'polar': 3, 'sci': 0}` is used.

        - resizable : bool, optional
            Whether plots and tables are made with resize handles and can be
            resized within the report.

        - autosize : {'none', 'initial', 'continual'}
            Whether tables and plots should be resized, either initially --
            i.e. just upon first rendering (`"initial"`) -- or whenever
            the browser window is resized (`"continual"`).

        - embed_figures: bool, optional
            Whether figures should be embedded in the generated report.

        - combine_robust : bool, optional
            Whether robust estimates should automatically be combined with
            their non-robust counterpart when displayed in reports. (default
            is True).

        - confidence_interval_brevity : int, optional
            Roughly specifies how many figures will have confidence intervals
            (when applicable). Defaults to '1'.  Smaller values mean more
            tables will get confidence intervals (and reports will take longer
            to generate).

        - idt_basis_dicts : tuple, optional
            Tuple of (prepDict,measDict) pauli-basis dictionaries, which map
            between 1-qubit Pauli basis strings (e.g. `'-X'` or `'Y'`) and tuples
            of gate names (e.g. `('Gx','Gx')`).  If given, idle tomography will
            be performed on the 'Gi' gate and included in the report.

        - idt_idle_oplabel : Label, optional
            The label identifying the idle gate (for use with idle tomography).

        - colorboxplot_bgcolor : str, optional
            Background color for the color box plots in this report.  Can be common
            color names, e.g. `"black"`, or string RGB values, e.g. `"rgb(255,128,0)"`.

    verbosity : int, optional
       How much detail to send to stdout.


    Returns
    -------
    Workspace
        The workspace object used to create the report

    .. deprecated:: v0.9.9
        `create_standard_report` will be removed in the next major release of pyGSTi. It is replaced by
        `construct_standard_report`, which returns a :class:`Report` object.
    """

    # Wrap a call to the new factory method
    ws = ws or _ws.Workspace()

    report = construct_standard_report(
        results, title, confidenceLevel, comm, ws, advancedOptions, verbosity
    )

    advancedOptions = advancedOptions or {}
    precision = advancedOptions.get('precision', None)

    if filename is not None:
        if filename.endswith(".pdf"):
            report.write_pdf(
                filename, build_options=advancedOptions,
                brevity=brevity, precision=precision,
                auto_open=auto_open, verbosity=verbosity
            )
        else:
            resizable = advancedOptions.get('resizable', True)
            autosize = advancedOptions.get('autosize', 'initial')
            connected = advancedOptions.get('connected', False)
            single_file = filename.endswith(".html")

            report.write_html(
                filename, auto_open=auto_open, link_to=link_to,
                connected=connected, build_options=advancedOptions,
                brevity=brevity, precision=precision,
                resizable=resizable, autosize=autosize,
                single_file=single_file, verbosity=verbosity
            )

    return ws


@_deprecated_fn('construct_nqnoise_report(...).write_html(...)')
def create_nqnoise_report(results, filename, title="auto",
                          confidenceLevel=None, comm=None, ws=None,
                          auto_open=False, link_to=None, brevity=0,
                          advancedOptions=None, verbosity=1):
    """
    Creates a report designed to display results containing for n-qubit noisy
    model estimates.

    Such models are characterized by the fact that gates and SPAM objects may
    not have dense representations (or it may be very expensive to compute them)
    , and that these models are likely :class:`CloudNoiseModel` objects or have
    similar structure.

    Parameters
    ----------
    results : Results
        An object which represents the set of results from one *or more* GST
        estimation runs, typically obtained from running
        :func:`do_long_sequence_gst` or :func:`do_stdpractice_gst`, OR a
        dictionary of such objects, representing multiple GST runs to be
        compared (typically all with *different* data sets). The keys of this
        dictionary are used to label different data sets that are selectable
        in the report.

    filename : string, optional
       The output filename where the report file(s) will be saved.  If
       None, then no output file is produced (but returned Workspace
       still caches all intermediate results).

    title : string, optional
       The title of the report.  "auto" causes a random title to be
       generated (which you may or may not like).

    confidenceLevel : int, optional
       If not None, then the confidence level (between 0 and 100) used in
       the computation of confidence regions/intervals. If None, no
       confidence regions or intervals are computed.

    comm : mpi4py.MPI.Comm, optional
        When not None, an MPI communicator for distributing the computation
        across multiple processors.

    ws : Workspace, optional
        The workspace used as a scratch space for performing the calculations
        and visualizations required for this report.  If you're creating
        multiple reports with similar tables, plots, etc., it may boost
        performance to use a single Workspace for all the report generation.

    auto_open : bool, optional
        If True, automatically open the report in a web browser after it
        has been generated.

    link_to : list, optional
        If not None, a list of one or more items from the set
        {"tex", "pdf", "pkl"} indicating whether or not to
        create and include links to Latex, PDF, and Python pickle
        files, respectively.  "tex" creates latex source files for
        tables; "pdf" renders PDFs of tables and plots ; "pkl" creates
        Python versions of plots (pickled python data) and tables (pickled
        pandas DataFrams).

    brevity : int, optional
        Amount of detail to include in the report.  Larger values mean smaller
        "more briefr" reports, which reduce generation time, load time, and
        disk space consumption.  In particular:

        - 1: Plots showing per-sequences quantities disappear at brevity=1
        - 2: Reference sections disappear at brevity=2
        - 3: Germ-level estimate tables disappear at brevity=3
        - 4: Everything but summary figures disappears at brevity=4

    advancedOptions : dict, optional
        A dictionary of advanced options for which the default values are usually
        are fine.  Here are the possible keys of `advancedOptions`:

        - connected : bool, optional
            Whether output HTML should assume an active internet connection.  If
            True, then the resulting HTML file size will be reduced because it
            will link to web resources (e.g. CDN libraries) instead of embedding
            them.

        - cachefile : str, optional
            filename with cached workspace results

        - linlogPercentile : float, optional
            Specifies the colorscale transition point for any logL or chi2 color
            box plots.  The lower `(100 - linlogPercentile)` percentile of the
            expected chi2 distribution is shown in a linear grayscale, and the
            top `linlogPercentile` is shown on a logarithmic colored scale.

        - nmthreshold : float, optional
            The threshold, in units of standard deviations, that triggers the
            usage of non-Markovian error bars.  If None, then non-Markovian
            error bars are never computed.

        - precision : int or dict, optional
            The amount of precision to display.  A dictionary with keys
            "polar", "sci", and "normal" can separately specify the
            precision for complex angles, numbers in scientific notation, and
            everything else, respectively.  If an integer is given, it this
            same value is taken for all precision types.  If None, then
            `{'normal': 6, 'polar': 3, 'sci': 0}` is used.

        - resizable : bool, optional
            Whether plots and tables are made with resize handles and can be
            resized within the report.

        - autosize : {'none', 'initial', 'continual'}
            Whether tables and plots should be resized, either initially --
            i.e. just upon first rendering (`"initial"`) -- or whenever
            the browser window is resized (`"continual"`).

        - combine_robust : bool, optional
            Whether robust estimates should automatically be combined with
            their non-robust counterpart when displayed in reports. (default
            is True).

        - confidence_interval_brevity : int, optional
            Roughly specifies how many figures will have confidence intervals
            (when applicable). Defaults to '1'.  Smaller values mean more
            tables will get confidence intervals (and reports will take longer
            to generate).

        - colorboxplot_bgcolor : str, optional
            Background color for the color box plots in this report.  Can be common
            color names, e.g. `"black"`, or string RGB values, e.g. `"rgb(255,128,0)"`.

    verbosity : int, optional
       How much detail to send to stdout.


    Returns
    -------
    Workspace
        The workspace object used to create the report

    .. deprecated:: v0.9.9
        `create_nqnoise_report` will be removed in the next major release of pyGSTi. It is replaced by
        `construct_standard_report`, which returns a :class:`Report` object.
    """

    # Wrap a call to the new factory method
    ws = ws or _ws.Workspace()
    report = construct_nqnoise_report(
        results, title, confidenceLevel, comm, ws, advancedOptions, verbosity
    )

    advancedOptions = advancedOptions or {}
    precision = advancedOptions.get('precision', None)

    if filename is not None:
        if filename.endswith(".pdf"):
            report.write_pdf(
                filename, build_options=advancedOptions,
                brevity=brevity, precision=precision,
                auto_open=auto_open, verbosity=verbosity
            )
        else:
            resizable = advancedOptions.get('resizable', True)
            autosize = advancedOptions.get('autosize', 'initial')
            connected = advancedOptions.get('connected', False)
            single_file = filename.endswith(".html")

            report.write_html(
                filename, auto_open=auto_open, link_to=link_to,
                connected=connected, build_options=advancedOptions,
                brevity=brevity, precision=precision,
                resizable=resizable, autosize=autosize,
                single_file=single_file, verbosity=verbosity
            )

    return ws


@_deprecated_fn('construct_standard_report(...).write_notebook(...)')
def create_report_notebook(results, filename, title="auto",
                           confidenceLevel=None,
                           auto_open=False, connected=False, verbosity=0):
    """
    Create a "report notebook": a Jupyter ipython notebook file which, when its
    cells are executed, will generate similar figures to those contained in an
    html report (via :func:`create_standard_report`).

    A notebook report allows the user to interact more flexibly with the data
    underlying the figures, and to easily generate customized variants on the
    figures.  As such, this type of report will be most useful for experts
    who want to tinker with the standard analysis presented in the static
    HTML or LaTeX format reports.

    Parameters
    ----------
    results : Results
        An object which represents the set of results from one *or more* GST
        estimation runs, typically obtained from running
        :func:`do_long_sequence_gst` or :func:`do_stdpractice_gst`, OR a
        dictionary of such objects, representing multiple GST runs to be
        compared (typically all with *different* data sets). The keys of this
        dictionary are used to label different data sets that are selectable
        (via setting Python variables) in the report.

    filename : string, optional
       The output filename where the report file(s) will be saved.  Must end
       in ".ipynb".

    title : string, optional
       The title of the report.  "auto" causes a random title to be
       generated (which you may or may not like).

    confidenceLevel : int, optional
       If not None, then the confidence level (between 0 and 100) used in
       the computation of confidence regions/intervals. If None, no
       confidence regions or intervals are computed.

    auto_open : bool, optional
        If True, automatically open the report in a web browser after it
        has been generated.

    connected : bool, optional
        Whether output notebook should assume an active internet connection.  If
        True, then the resulting file size will be reduced because it will link
        to web resources (e.g. CDN libraries) instead of embedding them.

    verbosity : int, optional
       How much detail to send to stdout.


    Returns
    -------
    None

    .. deprecated:: v0.9.9
        `create_report_notebook` will be removed in the next major release of pyGSTi. It is replaced by
        the `Report.write_notebook`
    """
    report = construct_standard_report(results, title=title, confidenceLevel=confidenceLevel, verbosity=verbosity)
    report.write_notebook(filename, auto_open=auto_open, connected=connected, verbosity=verbosity)


def find_std_clifford_compilation(model, verbosity=0):
    """
    Returns the standard Clifford compilation for `model`, if
    one exists.  Otherwise returns None.

    Parameters
    ----------
    model : Model
        The ideal (target) model of primitive gates.

    verbosity : int, optional
        How much detail to send to stdout.

    Returns
    -------
    dict or None
        The Clifford compilation dictionary (if one can be found).
    """
    printer = _VerbosityPrinter.build_printer(verbosity)
    if not isinstance(model, _objs.ExplicitOpModel):
        return None  # only match explicit models

    import importlib

    legacy_std_modules = ("std1Q_XY",
                          "std1Q_XYI",
                          "std1Q_XYZI",
                          "std1Q_XZ",
                          "std1Q_ZN",
                          "std1Q_pi4_pi2_XZ",
                          "std2Q_XXII",
                          "std2Q_XXYYII",
                          "std2Q_XY",
                          "std2Q_XYCNOT",
                          "std2Q_XYCPHASE",
                          "std2Q_XYI",
                          "std2Q_XYI1",
                          "std2Q_XYI2",
                          "std2Q_XYICNOT",
                          "std2Q_XYICPHASE",
                          "std2Q_XYZICNOT")
    for module_name in legacy_std_modules:
        mod = importlib.import_module("pygsti.modelpacks.legacy." + module_name)
        target_model = mod.target_model()
        if target_model.dim == model.dim and \
           set(target_model.operations.keys()) == set(model.operations.keys()) and \
           set(target_model.preps.keys()) == set(model.preps.keys()) and \
           set(target_model.povms.keys()) == set(model.povms.keys()):
            if target_model.frobeniusdist(model) < 1e-6:
                if hasattr(mod, "clifford_compilation"):
                    printer.log("Found standard clifford compilation from %s" % module_name)
                    return mod.clifford_compilation

    smq_modules = ("smq1Q_XY",
                   "smq1Q_XYI",
                   "smq1Q_XYZI",
                   "smq1Q_XZ",
                   "smq1Q_ZN",
                   "smq1Q_pi4_pi2_XZ",
                   "smq2Q_XXII",
                   "smq2Q_XXYYII",
                   "smq2Q_XY",
                   "smq2Q_XYCNOT",
                   "smq2Q_XYCPHASE",
                   "smq2Q_XYI",
                   "smq2Q_XYI1",
                   "smq2Q_XYI2",
                   "smq2Q_XYICNOT",
                   "smq2Q_XYICPHASE",
                   "smq2Q_XYZICNOT")
    for module_name in smq_modules:
        mod = importlib.import_module("pygsti.modelpacks." + module_name)
        qubit_labels = model.state_space_labels.labels[0]  # this usually gets the qubit labels
        if len(mod._sslbls) != len(qubit_labels): continue  # wrong number of qubits!

        target_model = mod.target_model(qubit_labels=qubit_labels)
        if target_model.dim == model.dim and \
           set(target_model.operations.keys()) == set(model.operations.keys()) and \
           set(target_model.preps.keys()) == set(model.preps.keys()) and \
           set(target_model.povms.keys()) == set(model.povms.keys()):
            if target_model.frobeniusdist(model) < 1e-6:
                if isinstance(mod, _RBModelPack):
                    printer.log("Found standard clifford compilation from %s" % module_name)
                    return mod.clifford_compilation(qubit_labels)

    return None


# TODO these factories should really be Report subclasses
def construct_standard_report(results, title="auto",
                              confidenceLevel=None, comm=None, ws=None,
                              advancedOptions=None, verbosity=1):
    """
    Create a "standard" GST report, containing details about each estimate
    in `results` individually.

    Parameters
    ----------
    results : Results
        An object which represents the set of results from one *or more* GST
        estimation runs, typically obtained from running
        :func:`do_long_sequence_gst` or :func:`do_stdpractice_gst`, OR a
        dictionary of such objects, representing multiple GST runs to be
        compared (typically all with *different* data sets). The keys of this
        dictionary are used to label different data sets that are selectable
        in the report.

    title : string, optional
       The title of the report.  "auto" causes a random title to be
       generated (which you may or may not like).

    confidenceLevel : int, optional
       If not None, then the confidence level (between 0 and 100) used in
       the computation of confidence regions/intervals. If None, no
       confidence regions or intervals are computed.

    comm : mpi4py.MPI.Comm, optional
        When not None, an MPI communicator for distributing the computation
        across multiple processors.

    ws : Workspace, optional
        The workspace used as a scratch space for performing the calculations
        and visualizations required for this report.  If you're creating
        multiple reports with similar tables, plots, etc., it may boost
        performance to use a single Workspace for all the report generation.

    advancedOptions : dict, optional
        A dictionary of advanced options for which the default values are usually
        are fine.  Here are the possible keys of `advancedOptions`:

        - linlogPercentile : float, optional
            Specifies the colorscale transition point for any logL or chi2 color
            box plots.  The lower `(100 - linlogPercentile)` percentile of the
            expected chi2 distribution is shown in a linear grayscale, and the
            top `linlogPercentile` is shown on a logarithmic colored scale.

        - nmthreshold : float, optional
            The threshold, in units of standard deviations, that triggers the
            usage of non-Markovian error bars.  If None, then non-Markovian
            error bars are never computed.

        - embed_figures: bool, optional
            Whether figures should be embedded in the generated report.

        - combine_robust : bool, optional
            Whether robust estimates should automatically be combined with
            their non-robust counterpart when displayed in reports. (default
            is True).

        - idt_basis_dicts : tuple, optional
            Tuple of (prepDict,measDict) pauli-basis dictionaries, which map
            between 1-qubit Pauli basis strings (e.g. `'-X'` or `'Y'`) and tuples
            of gate names (e.g. `('Gx','Gx')`).  If given, idle tomography will
            be performed on the 'Gi' gate and included in the report.

        - idt_idle_oplabel : Label, optional
            The label identifying the idle gate (for use with idle tomography).

    verbosity : int, optional
       How much detail to send to stdout.


    Returns
    -------
    Workspace
        The workspace object used to create the report
    """

    printer = _VerbosityPrinter.build_printer(verbosity, comm=comm)
    ws = ws or _ws.Workspace()

    advancedOptions = advancedOptions or {}
    linlogPercentile = advancedOptions.get('linlog percentile', 5)
    nmthreshold = advancedOptions.get('nmthreshold', DEFAULT_BAD_FIT_THRESHOLD)
    embed_figures = advancedOptions.get('embed_figures', True)
    combine_robust = advancedOptions.get('combine_robust', True)
    idtPauliDicts = advancedOptions.get('idt_basis_dicts', 'auto')
    idtIdleOp = advancedOptions.get('idt_idle_oplabel', _Lbl('Gi'))

    if isinstance(title, int):  # to catch backward compatibility issues
        raise ValueError(("'title' argument must be a string.  You may be accidentally"
                          " specifying an int here because in older versions of pyGSTi"
                          " the third argument to general_report was the"
                          " confidence interval - please note the updated function signature"))

    if title is None or title == "auto":
        autoname = _autotitle.generate_name()
        title = "GST Report for " + autoname
        _warnings.warn(("You should really specify `title=` when generating reports,"
                        " as this makes it much easier to identify them later on.  "
                        "Since you didn't, pyGSTi has generated a random one"
                        " for you: '{}'.").format(autoname))

    pdfInfo = [('Author', 'pyGSTi'), ('Title', title),
               ('Keywords', 'GST'), ('pyGSTi Version', _version.__version__)]

    results = results if isinstance(results, dict) else {"unique": results}

    # set flags
    flags = set()
    for res in results.values():
        for est in res.estimates.values():
            weights = est.parameters.get('weights', None)
            if weights is not None and len(weights) > 0:
                flags.add('ShowScaling')
            if est.parameters.get('unmodeled_error', None):
                flags.add('ShowUnmodeledError')
    if combine_robust:
        flags.add('CombineRobust')

    # build section list
    sections = [
        _section.SummarySection(),
        _section.GoodnessSection(),
        _section.GoodnessColorBoxPlotSection(),
        _section.GaugeInvariantsGatesSection(),
        _section.GaugeInvariantsGermsSection(),
        _section.GaugeVariantSection(),
        _section.GaugeVariantsRawSection(),
        _section.GaugeVariantsDecompSection(),
        _section.GaugeVariantsErrGenSection(),
        _section.InputSection(),
        _section.MetaSection(),
        _section.HelpSection()
    ]

    if 'ShowScaling' in flags:
        sections.append(_section.GoodnessScalingSection())
    if 'ShowUnmodeledError' in flags:
        sections.append(_section.GoodnessUnmodeledSection())

    # Perform idle tomography on datasets if desired (need to do
    #  this before creating main switchboard)
    printer.log("Running idle tomography")
    try:
        idt_results = _construct_idtresults(idtIdleOp, idtPauliDicts, results, printer)
    except Exception as e:
        _warnings.warn("Idle tomography failed:\n" + str(e))
        idt_results = {}
    if len(idt_results) > 0:
        sections.append(_section.IdleTomographySection())
        flags.add('IdleTomography')

    if len(results) > 1:
        #check if data sets are comparable (if they have the same sequences)
        arbitrary = next(iter(results.values()))
        comparable = all([list(v.dataset.keys()) == arbitrary.dataset.keys() for v in results.values()])
        if comparable:
            flags.add('CompareDatasets')
            sections.append(_section.DataComparisonSection())
        else:
            _warnings.warn("Not all data sets are comparable - no comparisions will be made.")

    printer.log("Computing switchable properties")
    switchBd, dataset_labels, est_labels, gauge_opt_labels, Ls, swLs = \
        _create_master_switchboard(ws, results, confidenceLevel,
                                   nmthreshold, printer, None,
                                   combine_robust, idt_results, embed_figures)

    if len(Ls) > 0 and Ls[0] == 0:
        _warnings.warn(("Setting the first 'max-length' to zero, e.g. using"
                        " [0,1,2,4] instead of [1,2,4], is deprecated and"
                        " may cause 'no data to plot' errors when creating"
                        " this report.  Please remove this leading zero."))

    global_qtys = {
        'title': title,
        'date': _time.strftime("%B %d, %Y"),
        'pdfinfo': _merge.to_pdfinfo(pdfInfo),
        'linlg_pcntle': "%d" % round(linlogPercentile),  # to nearest %
        'linlg_pcntle_inv': "%d" % (100 - int(round(linlogPercentile))),
        'topSwitchboard': switchBd,
        'colorBoxPlotKeyPlot': ws.BoxKeyPlot(switchBd.prepStrs, switchBd.effectStrs),
        'bestGatesetGaugeOptParamsTable': ws.GaugeOptParamsTable(switchBd.goparams)
    }

    report_params = {
        'linlog_percentile': linlogPercentile,
        'confidence_level': confidenceLevel,
        'nm_threshold': nmthreshold,
        'embed_figures': embed_figures,
        'combine_robust': combine_robust,
        'switchboard': switchBd,
        'dataset_labels': tuple(dataset_labels),
        'est_labels': tuple(est_labels),
        'gauge_opt_labels': tuple(gauge_opt_labels),
        'Ls': tuple(Ls),
        'swLs': tuple(swLs)
    }

    templates = dict(
        html='~standard_html_report',
        pdf='standard_pdf_report.tex',
        notebook='report_notebook'
    )

    build_defaults = dict(
        errgen_type='logGTi',
        ci_brevity=1,
        bgcolor='white'
    )

    pdf_available = True
    if len(results) > 1:
        pdf_available = False
    else:
        for est in next(iter(results.values())).estimates.values():
            if len(est.goparameters) > 1:
                pdf_available = False

    return _Report(templates, results, sections, flags, global_qtys,
                   report_params, build_defaults, pdf_available=pdf_available,
                   workspace=ws)


def construct_nqnoise_report(results, title="auto",
                             confidenceLevel=None, comm=None, ws=None,
                             advancedOptions=None, verbosity=1):
    """
    Creates a report designed to display results containing for n-qubit noisy
    model estimates.

    Such models are characterized by the fact that gates and SPAM objects may
    not have dense representations (or it may be very expensive to compute them)
    , and that these models are likely :class:`CloudNoiseModel` objects or have
    similar structure.

    Parameters
    ----------
    results : Results
        An object which represents the set of results from one *or more* GST
        estimation runs, typically obtained from running
        :func:`do_long_sequence_gst` or :func:`do_stdpractice_gst`, OR a
        dictionary of such objects, representing multiple GST runs to be
        compared (typically all with *different* data sets). The keys of this
        dictionary are used to label different data sets that are selectable
        in the report.

    title : string, optional
       The title of the report.  "auto" causes a random title to be
       generated (which you may or may not like).

    confidenceLevel : int, optional
       If not None, then the confidence level (between 0 and 100) used in
       the computation of confidence regions/intervals. If None, no
       confidence regions or intervals are computed.

    comm : mpi4py.MPI.Comm, optional
        When not None, an MPI communicator for distributing the computation
        across multiple processors.

    ws : Workspace, optional
        The workspace used as a scratch space for performing the calculations
        and visualizations required for this report.  If you're creating
        multiple reports with similar tables, plots, etc., it may boost
        performance to use a single Workspace for all the report generation.

    advancedOptions : dict, optional
        A dictionary of advanced options for which the default values are usually
        are fine.  Here are the possible keys of `advancedOptions`:

        - linlogPercentile : float, optional
            Specifies the colorscale transition point for any logL or chi2 color
            box plots.  The lower `(100 - linlogPercentile)` percentile of the
            expected chi2 distribution is shown in a linear grayscale, and the
            top `linlogPercentile` is shown on a logarithmic colored scale.

        - nmthreshold : float, optional
            The threshold, in units of standard deviations, that triggers the
            usage of non-Markovian error bars.  If None, then non-Markovian
            error bars are never computed.

        - combine_robust : bool, optional
            Whether robust estimates should automatically be combined with
            their non-robust counterpart when displayed in reports. (default
            is True).

        - confidence_interval_brevity : int, optional
            Roughly specifies how many figures will have confidence intervals
            (when applicable). Defaults to '1'.  Smaller values mean more
            tables will get confidence intervals (and reports will take longer
            to generate).

        - embed_figures: bool, optional
            Whether figures should be embedded in the generated report.

    verbosity : int, optional
       How much detail to send to stdout.

    Returns
    -------
    :class:`Report` : A constructed report object
    """

    printer = _VerbosityPrinter.build_printer(verbosity, comm=comm)
    ws = ws or _ws.Workspace()

    advancedOptions = advancedOptions or {}
    linlogPercentile = advancedOptions.get('linlog percentile', 5)
    nmthreshold = advancedOptions.get('nmthreshold', DEFAULT_BAD_FIT_THRESHOLD)
    embed_figures = advancedOptions.get('embed_figures', True)
    combine_robust = advancedOptions.get('combine_robust', True)
    idtPauliDicts = advancedOptions.get('idt_basis_dicts', 'auto')
    idtIdleOp = advancedOptions.get('idt_idle_oplabel', _Lbl('Gi'))

    if isinstance(title, int):  # to catch backward compatibility issues
        raise ValueError(("'title' argument must be a string.  You may be accidentally"
                          " specifying an int here because in older versions of pyGSTi"
                          " the third argument to create_general_report was the"
                          " confidence interval - please note the updated function signature"))

    if title is None or title == "auto":
        autoname = _autotitle.generate_name()
        title = "GST Report for " + autoname
        _warnings.warn(("You should really specify `title=` when generating reports,"
                        " as this makes it much easier to identify them later on.  "
                        "Since you didn't, pyGSTi has generated a random one"
                        " for you: '{}'.").format(autoname))

    pdfInfo = [('Author', 'pyGSTi'), ('Title', title),
               ('Keywords', 'GST'), ('pyGSTi Version', _version.__version__)]

    results = results if isinstance(results, dict) else {"unique": results}

    # set flags
    flags = set()
    for res in results.values():
        for est in res.estimates.values():
            weights = est.parameters.get('weights', None)
            if weights is not None and len(weights) > 0:
                flags.add('ShowScaling')
            if est.parameters.get('unmodeled_error', None):
                flags.add('ShowUnmodeledError')
    if combine_robust:
        flags.add('CombineRobust')

    # build section list
    sections = [
        _section.SummarySection(bestGatesVsTargetTable_sum=False),
        _section.GoodnessSection(),
        _section.GoodnessColorBoxPlotSection(),
        _section.GaugeVariantsErrGenNQubitSection(),
        _section.InputSection(fiducialListTable=False, targetGatesBoxTable=False, targetSpamBriefTable=False),
        _section.MetaSection(),
        _section.HelpSection()
    ]

    if 'ShowScaling' in flags:
        sections.append(_section.GoodnessScalingSection())

    # Perform idle tomography on datasets if desired (need to do
    #  this before creating main switchboard)
    printer.log("Running idle tomography")
    try:
        idt_results = _construct_idtresults(idtIdleOp, idtPauliDicts, results, printer)
    except Exception as e:
        _warnings.warn("Idle tomography failed:\n" + str(e))
        idt_results = {}
    if len(idt_results) > 0:
        sections.append(_section.IdleTomographySection())
        flags.add('IdleTomography')

    if len(results) > 1:
        #check if data sets are comparable (if they have the same sequences)
        arbitrary = next(iter(results.values()))
        comparable = all([list(v.dataset.keys()) == arbitrary.dataset.keys() for v in results.values()])
        if comparable:
            flags.add('CompareDatasets')
            sections.append(_section.DataComparisonSection())
        else:
            _warnings.warn("Not all data sets are comparable - no comparisions will be made.")

    printer.log("Computing switchable properties")
    switchBd, dataset_labels, est_labels, gauge_opt_labels, Ls, swLs = \
        _create_master_switchboard(ws, results, confidenceLevel,
                                   nmthreshold, printer, None,
                                   combine_robust, idt_results, embed_figures)

    if len(Ls) > 0 and Ls[0] == 0:
        _warnings.warn(("Setting the first 'max-length' to zero, e.g. using"
                        " [0,1,2,4] instead of [1,2,4], is deprecated and"
                        " may cause 'no data to plot' errors when creating"
                        " this report.  Please remove this leading zero."))

    global_qtys = {
        'title': title,
        'date': _time.strftime("%B %d, %Y"),
        'pdfinfo': _merge.to_pdfinfo(pdfInfo),
        'linlg_pcntle': "%d" % round(linlogPercentile),  # to nearest %
        'linlg_pcntle_inv': "%d" % (100 - int(round(linlogPercentile))),
        'topSwitchboard': switchBd,
        'colorBoxPlotKeyPlot': ws.BoxKeyPlot(switchBd.prepStrs, switchBd.effectStrs),
        'bestGatesetGaugeOptParamsTable': ws.GaugeOptParamsTable(switchBd.goparams),
        'gramBarPlot': ws.GramMatrixBarPlot(switchBd.ds, switchBd.gsTarget, 10, switchBd.strs)
    }

    report_params = {
        'linlog_percentile': linlogPercentile,
        'confidence_level': confidenceLevel,
        'nm_threshold': nmthreshold,
        'embed_figures': embed_figures,
        'combine_robust': combine_robust,
        'switchboard': switchBd,
        'dataset_labels': tuple(dataset_labels),
        'est_labels': tuple(est_labels),
        'gauge_opt_labels': tuple(gauge_opt_labels),
        'Ls': tuple(Ls),
        'swLs': tuple(swLs)
    }

    templates = dict(
        html='~standard_html_report',
        pdf='standard_pdf_report.tex'
    )

    build_defaults = dict(
        errgen_type='logGTi',
        ci_brevity=1,
        bgcolor='white'
    )

    pdf_available = True
    if len(results) > 1:
        pdf_available = False
    else:
        for est in next(iter(results.values())).estimates.values():
            if len(est.goparameters) > 1:
                pdf_available = False

    return _Report(templates, results, sections, flags, global_qtys,
                   report_params, build_defaults, pdf_available=pdf_available,
                   workspace=ws)


def construct_drift_report(results, title='auto', ws=None, verbosity=1):
    """
    Creates a Drift report.

    TODO docstring

    Returns
    -------
    :class:`Report` : A constructed report object
    """
    from ..protocols import StabilityAnalysisResults as _StabilityAnalysisResults
    from ..extras.drift.stabilityanalyzer import StabilityAnalyzer
    from ..extras.drift import driftreport
    assert(isinstance(results, _StabilityAnalysisResults)), \
        "Support for multiple results as a Dict is not yet included!"
    gss = results.data.edesign.circuit_structs[-1]
    singleresults = results.stabilityanalyzer

    printer = _VerbosityPrinter.build_printer(verbosity)  # , comm=comm)

    printer.log('*** Creating workspace ***')
    ws = ws or _ws.Workspace()

    if title is None or title == "auto":
        autoname = _autotitle.generate_name()
        title = "Drift Report for " + autoname
        _warnings.warn(("You should really specify `title=` when generating reports,"
                        " as this makes it much easier to identify them later on.  "
                        "Since you didn't, pyGSTi has generated a random one"
                        " for you: '{}'.").format(autoname))

    pdfInfo = [('Author', 'pyGSTi'), ('Title', title),
               ('Keywords', 'GST'), ('pyGSTi Version', _version.__version__)]

    results_dict = results if isinstance(results, dict) else {"unique": results}

    drift_switchBd = driftreport._create_drift_switchboard(ws, results.stabilityanalyzer, gss)

    # Sets whether or not the dataset key is a switchboard or not.
    if len(singleresults.data.keys()) > 1:
        dskey = drift_switchBd.dataset
        arb_dskey = list(singleresults.data.keys())[0]
    else:
        dskey = list(singleresults.data.keys())[0]
        arb_dskey = dskey

    # Generate Switchboard
    printer.log("*** Generating switchboard ***")

    #Create master switchboard
    stabilityanalyzer_dict = {k: res.stabilityanalyzer for k, res in results_dict.items()}
    switchBd, _dataset_labels = \
        driftreport._create_switchboard(ws, stabilityanalyzer_dict)

    global_qtys = {
        'title': title,
        'date': _time.strftime("%B %d, %Y"),
        'pdfinfo': _merge.to_pdfinfo(pdfInfo),
        'drift_switchBd': drift_switchBd,
        'topSwitchboard': switchBd
    }

    report_params = {
        'results': switchBd.results,
        'gss': gss,
        'dskey': dskey,
        'switchboard': drift_switchBd
    }

    averaging_allowed = singleresults.averaging_allowed({'dataset': arb_dskey}, checklevel=1)
    sections = [
        _section.DriftSection(GlobalPowerSpectraPlot=averaging_allowed)
    ]

    templates = dict(
        html='~drift_html_report',
        pdf='drift_pdf_report.tex'
    )
    return _Report(templates, singleresults, sections, set(), global_qtys, report_params, workspace=ws)


# # XXX this needs to be revised into a script
# # Scratch: SAVE!!! this code generates "projected" models which can be sent to
# # FitComparisonTable (with the same gss for each) to make a nice comparison plot.
#        opLabels = list(model.operations.keys())  # operation labels
#        basis = model.basis
#
#        if basis.name != targetModel.basis.name:
#            raise ValueError("Basis mismatch between model (%s) and target (%s)!"\
#                                 % (basis.name, targetModel.basis.name))
#
#        #Do computation first
#        # Note: set to "full" parameterization so we can set the gates below
#        #  regardless of what to fo parameterization the original model had.
#        gsH = model.copy(); gsH.set_all_parameterizations("full"); Np_H = 0
#        gsS = model.copy(); gsS.set_all_parameterizations("full"); Np_S = 0
#        gsHS = model.copy(); gsHS.set_all_parameterizations("full"); Np_HS = 0
#        gsLND = model.copy(); gsLND.set_all_parameterizations("full"); Np_LND = 0
#        #gsHSCP = model.copy()
#        gsLNDCP = model.copy(); gsLNDCP.set_all_parameterizations("full")
#        for gl in opLabels:
#            gate = model.operations[gl]
#            targetOp = targetModel.operations[gl]
#
#            errgen = _tools.error_generator(gate, targetOp, genType)
#            hamProj, hamGens = _tools.std_errgen_projections(
#                errgen, "hamiltonian", basis.name, basis, True)
#            stoProj, stoGens = _tools.std_errgen_projections(
#                errgen, "stochastic", basis.name, basis, True)
#            HProj, OProj, HGens, OGens = \
#                _tools.lindblad_errgen_projections(
#                    errgen, basis, basis, basis, normalize=False,
#                    return_generators=True)
#                #Note: return values *can* be None if an empty/None basis is given
#
#            ham_error_gen = _np.einsum('i,ijk', hamProj, hamGens)
#            sto_error_gen = _np.einsum('i,ijk', stoProj, stoGens)
#            lnd_error_gen = _np.einsum('i,ijk', HProj, HGens) + \
#                _np.einsum('ij,ijkl', OProj, OGens)
#
#            ham_error_gen = _tools.change_basis(ham_error_gen,"std",basis)
#            sto_error_gen = _tools.change_basis(sto_error_gen,"std",basis)
#            lnd_error_gen = _tools.change_basis(lnd_error_gen,"std",basis)
#
#            gsH.operations[gl]  = _tools.operation_from_error_generator(
#                ham_error_gen, targetOp, genType)
#            gsS.operations[gl]  = _tools.operation_from_error_generator(
#                sto_error_gen, targetOp, genType)
#            gsHS.operations[gl] = _tools.operation_from_error_generator(
#                ham_error_gen+sto_error_gen, targetOp, genType)
#            gsLND.operations[gl] = _tools.operation_from_error_generator(
#                lnd_error_gen, targetOp, genType)
#
#            #CPTP projection
#
#            evals,U = _np.linalg.eig(OProj)
#            pos_evals = evals.clip(0,1e100) #clip negative eigenvalues to 0
#            OProj_cp = _np.dot(U,_np.dot(_np.diag(pos_evals),_np.linalg.inv(U))) #OProj_cp is now a pos-def matrix
#            lnd_error_gen_cp = _np.einsum('i,ijk', HProj, HGens) + \
#                _np.einsum('ij,ijkl', OProj_cp, OGens)
#            lnd_error_gen_cp = _tools.change_basis(lnd_error_gen_cp,"std",basis)
#
#            gsLNDCP.operations[gl] = _tools.operation_from_error_generator(
#                lnd_error_gen_cp, targetOp, genType)
#
#            Np_H += len(hamProj)
#            Np_S += len(stoProj)
#            Np_HS += len(hamProj) + len(stoProj)
#            Np_LND += HProj.size + OProj.size
#
#        #DEBUG!!!
#        #print("DEBUG: BEST sum neg evals = ",_tools.sum_of_negative_choi_evals(model))
#        #print("DEBUG: LNDCP sum neg evals = ",_tools.sum_of_negative_choi_evals(gsLNDCP))
#
#        #Check for CPTP where expected
#        #assert(_tools.sum_of_negative_choi_evals(gsHSCP) < 1e-6)
#        assert(_tools.sum_of_negative_choi_evals(gsLNDCP) < 1e-6)
#
#        # ...
#        models = (model, gsHS, gsH, gsS, gsLND, cptpGateset, gsLNDCP, gsHSCPTP)
#        modelTyps = ("Full","H + S","H","S","LND","CPTP","LND CPTP","H + S CPTP")
#        Nps = (Nng, Np_HS, Np_H, Np_S, Np_LND, Nng, Np_LND, Np_HS)
