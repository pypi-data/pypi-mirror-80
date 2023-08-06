""" Gauge-invariant and -dependent sections """
#***************************************************************************************************
# Copyright 2015, 2019 National Technology & Engineering Solutions of Sandia, LLC (NTESS).
# Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains certain rights
# in this software.
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
# in compliance with the License.  You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0 or in the LICENSE file in the root pyGSTi directory.
#***************************************************************************************************

from . import Section as _Section
from .. import reportables as _reportables


class GaugeInvariantsGatesSection(_Section):
    _HTML_TEMPLATE = 'tabs/GaugeInvariants_gates.html'

    def render(self, workspace, results=None, dataset_labels=None, est_labels=None, embed_figures=True, **kwargs):
        # This section's figures depend on switchboards, which must be rendered in advance:
        # XXX this is so wack
        gi_switchboard = _create_single_metric_switchboard(
            workspace, results, True, dataset_labels, est_labels, embed_figures
        )
        gr_switchboard = _create_single_metric_switchboard(
            workspace, {}, False, [], embed_figures=embed_figures
        )

        return {
            'metricSwitchboard_gi': gi_switchboard,
            'metricSwitchboard_gr': gr_switchboard,
            **super().render(
                workspace, gr_switchboard=gr_switchboard,
                gi_switchboard=gi_switchboard,
                dataset_labels=dataset_labels, est_labels=est_labels,
                embed_figures=embed_figures, **kwargs
            )
        }

    @_Section.figure_factory(4)
    def bestGatesetSpamParametersTable(workspace, switchboard=None, confidence_level=None, ci_brevity=1, **kwargs):
        return workspace.SpamParametersTable(
            switchboard.gsTargetAndFinal, ['Target', 'Estimated'], _cri(1, switchboard, confidence_level, ci_brevity)
        )

    @_Section.figure_factory(4)
    def bestGatesetEvalTable(workspace, switchboard=None, confidence_level=None, ci_brevity=1, **kwargs):
        return workspace.GateEigenvalueTable(
            switchboard.gsGIRep, switchboard.gsTarget, _criGI(1, switchboard, confidence_level, ci_brevity),
            display=('evals', 'target', 'absdiff-evals', 'infdiff-evals', 'log-evals', 'absdiff-log-evals')
        )

    @_Section.figure_factory(4)
    def bestGatesetVsTargetTable(workspace, switchboard=None, confidence_level=None, ci_brevity=1, **kwargs):
        return workspace.ModelVsTargetTable(
            switchboard.gsFinal, switchboard.gsTarget, switchboard.clifford_compilation,
            _cri(1, switchboard, confidence_level, ci_brevity)
        )

    @_Section.figure_factory(4)
    def bestGatesVsTargetTable_gi(workspace, switchboard=None, confidence_level=None, ci_brevity=1, **kwargs):
        return workspace.GatesVsTargetTable(
            switchboard.gsGIRep, switchboard.gsTarget, _criGI(0, switchboard, confidence_level, ci_brevity),
            display=('evinf', 'evagi', 'evnuinf', 'evnuagi', 'evdiamond', 'evnudiamond')
        )

    @_Section.figure_factory(4)
    def bestGIGatesetTable(workspace, switchboard=None, confidence_level=None, ci_brevity=1, **kwargs):
        return workspace.GaugeRobustModelTable(
            switchboard.gsFinal, switchboard.gsTarget, 'boxes', _cri(1, switchboard, confidence_level, ci_brevity)
        )

    @_Section.figure_factory(4)
    def singleMetricTable_gi(workspace, switchboard=None, dataset_labels=None, est_labels=None, gi_switchboard=None,
                             **kwargs):
        if len(dataset_labels) > 1:
            # Multiple datasets
            return workspace.GatesSingleMetricTable(
                gi_switchboard.metric, switchboard.gsFinalGrid,
                switchboard.gsTargetGrid, est_labels, dataset_labels,
                gi_switchboard.cmpTableTitle, gi_switchboard.opLabel,
                confidenceRegionInfo=None
            )
        else:
            return workspace.GatesSingleMetricTable(
                gi_switchboard.metric, switchboard.gsFinalGrid,
                switchboard.gsTargetGrid, est_labels, None,
                gi_switchboard.cmpTableTitle,
                confidenceRegionInfo=None
            )

    @_Section.figure_factory(4)
    def bestGIMetricTable(workspace, switchboard=None, confidence_level=None, ci_brevity=1, gr_switchboard=None,
                          **kwargs):
        return workspace.GaugeRobustMetricTable(
            switchboard.gsFinal, switchboard.gsTarget, gr_switchboard.metric,
            _cri(1, switchboard, confidence_level, ci_brevity)
        )

    @_Section.figure_factory(4)
    def gramBarPlot(workspace, switchboard=None, **kwargs):
        return workspace.GramMatrixBarPlot(switchboard.ds, switchboard.gsTarget, 10, switchboard.strs)


class GaugeInvariantsGermsSection(_Section):
    _HTML_TEMPLATE = 'tabs/GaugeInvariants_germs.html'

    @_Section.figure_factory(3)
    def bestGatesVsTargetTable_gigerms(workspace, switchboard=None, confidence_level=None, ci_brevity=1, **kwargs):
        return workspace.GatesVsTargetTable(
            switchboard.gsGIRep, switchboard.gsGIRepEP, _criGI(0, switchboard, confidence_level, ci_brevity),
            display=('evdiamond', 'evnudiamond'), virtual_ops=switchboard.germs
        )

    @_Section.figure_factory(3)
    def bestGermsEvalTable(workspace, switchboard=None, confidence_level=None, ci_brevity=1, **kwargs):
        return workspace.GateEigenvalueTable(
            switchboard.gsGIRep, switchboard.gsGIRepEP, _criGI(1, switchboard, confidence_level, ci_brevity),
            display=('evals', 'target', 'absdiff-evals', 'infdiff-evals', 'log-evals', 'absdiff-log-evals'),
            virtual_ops=switchboard.germs
        )


class GaugeVariantSection(_Section):
    _HTML_TEMPLATE = 'tabs/GaugeVariants.html'

    def render(self, workspace, results=None, dataset_labels=None, est_labels=None, embed_figures=True, **kwargs):
        # This section's figures depend on switchboards, which must be rendered in advance:
        # XXX this is SO wack
        gv_switchboard = _create_single_metric_switchboard(
            workspace, results, False, dataset_labels, est_labels, embed_figures
        )

        return {
            'metricSwitchboard_gv': gv_switchboard,
            **super().render(
                workspace, gv_switchboard=gv_switchboard,
                dataset_labels=dataset_labels, est_labels=est_labels,
                embed_figures=embed_figures, **kwargs
            )
        }

    @_Section.figure_factory(4)
    def bestGatesetSpamVsTargetTable(workspace, switchboard=None, confidence_level=None, ci_brevity=1, **kwargs):
        return workspace.SpamVsTargetTable(
            switchboard.gsFinal, switchboard.gsTarget, _cri(1, switchboard, confidence_level, ci_brevity)
        )

    @_Section.figure_factory(4)
    def bestGatesVsTargetTable_gv(workspace, switchboard=None, confidence_level=None, ci_brevity=1, **kwargs):
        return workspace.GatesVsTargetTable(
            switchboard.gsFinal, switchboard.gsTarget, _cri(1, switchboard, confidence_level, ci_brevity),
            display=('inf', 'agi', 'trace', 'diamond', 'nuinf', 'nuagi')
        )

    @_Section.figure_factory(3)
    def bestGatesVsTargetTable_gvgerms(workspace, switchboard=None, confidence_level=None, ci_brevity=1, **kwargs):
        return workspace.GatesVsTargetTable(
            switchboard.gsFinal, switchboard.gsTarget, _cri(0, switchboard, confidence_level, ci_brevity),
            display=('inf', 'trace', 'nuinf'), virtual_ops=switchboard.germs
        )

    @_Section.figure_factory(4)
    def singleMetricTable_gv(workspace, switchboard=None, dataset_labels=None, est_labels=None, gv_switchboard=None,
                             **kwargs):
        if len(dataset_labels) > 1:
            # Multiple datasets
            return workspace.GatesSingleMetricTable(
                gv_switchboard.metric, switchboard.gsFinalGrid,
                switchboard.gsTargetGrid, est_labels, dataset_labels,
                gv_switchboard.cmpTableTitle, gv_switchboard.opLabel,
                confidenceRegionInfo=None
            )
        else:
            return workspace.GatesSingleMetricTable(
                gv_switchboard.metric, switchboard.gsFinalGrid,
                switchboard.gsTargetGrid, est_labels, None,
                gv_switchboard.cmpTableTitle,
                confidenceRegionInfo=None
            )


class GaugeVariantsDecompSection(_Section):
    _HTML_TEMPLATE = 'tabs/GaugeVariants_decomp.html'

    @_Section.figure_factory(4)
    def bestGatesetChoiEvalTable(workspace, switchboard=None, confidence_level=None, ci_brevity=1, **kwargs):
        return workspace.ChoiTable(
            switchboard.gsFinal, None, _cri(1, switchboard, confidence_level, ci_brevity),
            display=('boxplot', 'barplot')
        )

    @_Section.figure_factory(4)
    def bestGatesetDecompTable(workspace, switchboard=None, confidence_level=None, ci_brevity=1, **kwargs):
        return workspace.GateDecompTable(
            switchboard.gsFinal, switchboard.gsTarget, _cri(0, switchboard, confidence_level, ci_brevity)
        )


class GaugeVariantsErrGenSection(_Section):
    _HTML_TEMPLATE = 'tabs/GaugeVariants_errgen.html'

    @_Section.figure_factory(4)
    def bestGatesetErrGenBoxTable(workspace, switchboard=None, confidence_level=None, ci_brevity=1,
                                  errgen_type='logGTi', **kwargs):
        return workspace.ErrgenTable(
            switchboard.gsFinal, switchboard.gsTarget, _cri(1, switchboard, confidence_level, ci_brevity),
            ('errgen', 'H', 'S', 'A'), 'boxes', errgen_type
        )

    @_Section.figure_factory(4)
    def errorgenType(workspace, errgen_type='logGTi', **kwargs):
        # Not a figure, but who cares?
        return errgen_type


class GaugeVariantsErrGenNQubitSection(GaugeVariantsErrGenSection):
    @_Section.figure_factory(4)
    def bestGatesetErrGenBoxTable(workspace, switchboard=None, confidence_level=None, ci_brevity=1,
                                  errgen_type='logGTi', **kwargs):
        return workspace.NQubitErrgenTable(
            switchboard.gsGIRep, _cri(1, switchboard, confidence_level, ci_brevity),
            ('H', 'S'), 'boxes'
        )  # 'errgen' not allowed - 'A'?


class GaugeVariantsRawSection(_Section):
    _HTML_TEMPLATE = 'tabs/GaugeVariants_raw.html'

    @_Section.figure_factory(4)
    def bestGatesetGatesBoxTable(workspace, switchboard=None, confidence_level=None, ci_brevity=1, **kwargs):
        return workspace.GatesTable(
            switchboard.gsTargetAndFinal, ['Target', 'Estimated'], 'boxes',
            _cri(1, switchboard, confidence_level, ci_brevity)
        )

    @_Section.figure_factory(4)
    def bestGatesetSpamBriefTable(workspace, switchboard=None, confidence_level=None, ci_brevity=1, **kwargs):
        return workspace.SpamTable(
            switchboard.gsTargetAndFinal, ['Target', 'Estimated'], 'boxes',
            _cri(1, switchboard, confidence_level, ci_brevity), includeHSVec=False
        )


# Helper functions
def _cri(el, switchboard, confidence_level, ci_brevity):
    return switchboard.cri if confidence_level is not None and ci_brevity <= el else None


def _criGI(el, switchboard, confidence_level, ci_brevity):
    return switchboard.criGIRep if confidence_level is not None and ci_brevity <= el else None


def _create_single_metric_switchboard(ws, results_dict, bGaugeInv,
                                      dataset_labels, est_labels=None, embed_figures=True):
    op_labels = []
    for results in results_dict.values():
        for est in results.estimates.values():
            if 'target' in est.models:
                # append non-duplicate labels
                op_labels.extend([op for op in est.models['target'].operations.keys() if op not in op_labels])

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
