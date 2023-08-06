import numpy as np

from ..util import BaseCase
from . import fixtures

from pygsti.objects import StaticDenseOp
import pygsti.construction as pc
from pygsti.algorithms import germselection as germsel, scoring

_SEED = 2019


class GermSelectionData(object):
    @classmethod
    def setUpClass(cls):
        super(GermSelectionData, cls).setUpClass()
        # XXX are these acceptible test fixtures?
        cls.good_germs = fixtures.germs
        cls.germ_set = cls.good_germs + \
            pc.list_random_circuits_onelen(fixtures.opLabels, 4, 1, seed=_SEED) + \
            pc.list_random_circuits_onelen(fixtures.opLabels, 5, 1, seed=_SEED) + \
            pc.list_random_circuits_onelen(fixtures.opLabels, 6, 1, seed=_SEED)

    def setUp(self):
        super(GermSelectionData, self).setUp()
        self.mdl_target_noisy = fixtures.mdl_target_noisy.copy()


class GermSelectionWithNeighbors(GermSelectionData):
    @classmethod
    def setUpClass(cls):
        super(GermSelectionWithNeighbors, cls).setUpClass()
        cls.neighbors = germsel.randomize_model_list(
            [fixtures.model], randomizationStrength=1e-3, numCopies=5, seed=_SEED
        )


class GermSelectionTester(GermSelectionData, BaseCase):
    def test_test_germ_list_finitel(self):
        bSuccess, eigvals_finiteL = germsel.test_germ_list_finitel(
            self.mdl_target_noisy, self.germ_set, L=16, returnSpectrum=True, tol=1e-3
        )
        self.assertTrue(bSuccess)
        # TODO assert correctness

    def test_test_germ_list_infl(self):
        bSuccess, eigvals_infiniteL = germsel.test_germ_list_infl(
            self.mdl_target_noisy, self.germ_set, returnSpectrum=True, check=True
        )
        self.assertTrue(bSuccess)
        # TODO assert correctness

    def test_num_non_spam_gauge_params(self):
        # XXX hey why is this under germselection? EGN: probabaly b/c it was/is used exclusively here - could move it to a tools module?
        N = germsel.num_non_spam_gauge_params(self.mdl_target_noisy)
        # TODO assert correctness

    def test_calculate_germset_score(self):
        # TODO remove randomness
        maxscore = germsel.calculate_germset_score(
            self.germ_set, self.mdl_target_noisy
        )
        # TODO assert correctness

    def test_compute_composite_germ_score(self):
        score = germsel.compute_composite_germ_score(
            np.sum, model=self.mdl_target_noisy, partialGermsList=self.germ_set,
            eps=1e-5, germLengths=np.array([len(g) for g in self.germ_set])
        )
        # TODO assert correctness

        pDDD = np.zeros((len(self.germ_set), self.mdl_target_noisy.num_params(),
                         self.mdl_target_noisy.num_params()), 'd')
        score_pDDD = germsel.compute_composite_germ_score(
            np.sum, model=self.mdl_target_noisy, partialGermsList=self.germ_set,
            partialDerivDaggerDeriv=pDDD, opPenalty=1.0
        )
        # TODO assert correctness

    def test_randomize_model_list(self):
        # XXX does this need coverage?  EGN: does it take a long time?
        neighborhood = germsel.randomize_model_list(
            [fixtures.model], numCopies=3, randomizationStrength=1e-3,
            seed=_SEED
        )
        # TODO assert consistency
        # XXX numCopies and randomizationStrength really should be optional kwargs
        neighborhood_2 = germsel.randomize_model_list(
            [fixtures.model, fixtures.model], numCopies=None,
            randomizationStrength=1e-3, seed=_SEED
        )
        # TODO assert consistency

    def test_get_model_params_raises_on_model_param_mismatch(self):
        gs1 = fixtures.model.copy()
        gs2 = fixtures.model.copy()
        gs3 = fixtures.model.copy()
        gs4 = fixtures.model.copy()
        gs1.set_all_parameterizations("full")
        gs2.set_all_parameterizations("TP")
        gs3.set_all_parameterizations("full")
        gs4.set_all_parameterizations("full")
        gs3.operations['Gi2'] = np.identity(4, 'd')  # adds non-gauge params but not gauge params
        gs4.operations['Gi2'] = StaticDenseOp(np.identity(4, 'd'))  # keeps param counts the same but adds gate

        with self.assertRaises(ValueError):
            germsel.get_model_params([gs1, gs2])  # different number of gauge params
        with self.assertRaises(ValueError):
            germsel.get_model_params([gs1, gs3])  # different number of non-gauge params
        with self.assertRaises(ValueError):
            germsel.get_model_params([gs1, gs4])  # different number of gates

    def test_setup_model_list_warns_on_list_copy(self):
        with self.assertWarns(Warning):
            models = germsel.setup_model_list(
                [self.mdl_target_noisy, self.mdl_target_noisy], numCopies=3,
                randomize=False, randomizationStrength=0, seed=_SEED
            )
            # TODO assert correctness

    def test_compute_composite_germ_score_raises_on_missing_data(self):
        with self.assertRaises(ValueError):
            germsel.compute_composite_germ_score(np.sum)

        pDDD = np.zeros((len(self.germ_set), self.mdl_target_noisy.num_params(),
                         self.mdl_target_noisy.num_params()), 'd')
        with self.assertRaises(ValueError):
            germsel.compute_composite_germ_score(np.sum, partialDerivDaggerDeriv=pDDD)
        with self.assertRaises(ValueError):
            germsel.compute_composite_germ_score(
                np.sum, model=self.mdl_target_noisy,
                partialDerivDaggerDeriv=pDDD, opPenalty=1.0
            )

    def test_randomize_model_list_raises_on_conflicting_arg_spec(self):
        with self.assertRaises(ValueError):
            germsel.randomize_model_list(
                [fixtures.model, fixtures.model], numCopies=3,
                randomizationStrength=0, seed=_SEED
            )


class GenerateGermsTester(GermSelectionData, BaseCase):
    def test_generate_germs_with_candidate_germ_counts(self):
        germs = germsel.generate_germs(
            self.mdl_target_noisy, randomize=False,
            candidateGermCounts={3: 'all upto', 4: 10, 5: 10, 6: 10}
        )
        # TODO assert correctness

    def test_generate_germs_raises_on_bad_algorithm(self):
        with self.assertRaises(ValueError):
            germsel.generate_germs(self.mdl_target_noisy, algorithm='foobar')


class SlackGermSetOptimizationTester(GermSelectionData, BaseCase):
    def test_optimize_integer_germs_slack_with_fixed_slack(self):
        finalGerms = germsel.optimize_integer_germs_slack(
            self.mdl_target_noisy, self.germ_set, fixedSlack=0.1,
            verbosity=4
        )
        # TODO assert correctness

        finalGerms_all, weights, scores = germsel.optimize_integer_germs_slack(
            self.mdl_target_noisy, self.germ_set, fixedSlack=0.1,
            returnAll=True, verbosity=4
        )
        self.assertEqual(finalGerms, finalGerms_all)

        algorithm_kwargs = dict(
            germsList=self.germ_set,
            fixedSlack=0.1
        )
        finalGerms_driver = germsel.generate_germs(
            self.mdl_target_noisy, randomize=False, algorithm='slack',
            algorithm_kwargs=algorithm_kwargs, verbosity=4
        )
        self.assertEqual(finalGerms_driver, finalGerms)

    def test_optimize_integer_germs_slack_with_slack_fraction(self):
        finalGerms = germsel.optimize_integer_germs_slack(
            self.mdl_target_noisy, self.germ_set, slackFrac=0.1,
            verbosity=4
        )
        # TODO assert correctness

    def test_optimize_integer_germs_slack_with_initial_weights(self):
        finalGerms = germsel.optimize_integer_germs_slack(
            self.mdl_target_noisy, self.germ_set,
            initialWeights=np.ones(len(self.germ_set), 'd'),
            fixedSlack=0.1, verbosity=4
        )
        # TODO assert correctness

    def test_optimize_integer_germs_slack_force_strings(self):
        forceStrs = pc.circuit_list([('Gx',), ('Gy')])
        finalGerms = germsel.optimize_integer_germs_slack(
            self.mdl_target_noisy, self.germ_set, fixedSlack=0.1,
            force=forceStrs, verbosity=4,
        )

    def test_optimize_integer_germs_slack_max_iterations(self):
        finalGerms = germsel.optimize_integer_germs_slack(
            self.mdl_target_noisy, self.germ_set, fixedSlack=0.1,
            maxIter=1, verbosity=4,
        )
        self.assertEqual(finalGerms, self.germ_set)

    def test_optimize_integer_germs_slack_raises_on_initial_weight_length_mismatch(self):
        with self.assertRaises(ValueError):
            germsel.optimize_integer_germs_slack(
                self.mdl_target_noisy, self.germ_set,
                initialWeights=np.ones(1, 'd'),
                fixedSlack=0.1, verbosity=4
            )

    def test_optimize_integer_germs_slack_raises_on_missing_param(self):
        # XXX is this a useful test?  EGN: Probably not.
        with self.assertRaises(ValueError):
            germsel.optimize_integer_germs_slack(self.mdl_target_noisy, self.germ_set)


class GRASPGermSetOptimizationTester(GermSelectionWithNeighbors, BaseCase):
    def setUp(self):
        super(GRASPGermSetOptimizationTester, self).setUp()
        self.options = dict(
            randomize=False,
            threshold=1e6,
            l1Penalty=1.0,
            iterations=1,
            seed=_SEED,
            verbosity=1
        )

    def test_grasp_germ_set_optimization(self):
        soln = germsel.grasp_germ_set_optimization(
            self.neighbors, self.germ_set, alpha=0.1, **self.options
        )
        # TODO assert correctness

        best, initial, local = germsel.grasp_germ_set_optimization(
            self.neighbors, self.germ_set, alpha=0.1, returnAll=True,
            **self.options
        )
        # TODO shouldn't this pass?
        # self.assertEqual(soln, best)

        algorithm_kwargs = dict(
            germsList=self.germ_set,
            **self.options
        )
        soln_driver = germsel.generate_germs(
            self.mdl_target_noisy, randomize=False, algorithm='grasp',
            algorithm_kwargs=algorithm_kwargs
        )
        # TODO assert correctness

    def test_grasp_germ_set_optimization_force_strings(self):
        forceStrs = pc.circuit_list([('Gx',), ('Gy')])
        soln = germsel.grasp_germ_set_optimization(
            self.neighbors, self.germ_set, alpha=0.1, force=forceStrs,
            **self.options
        )
        for string in forceStrs:
            self.assertIn(string, soln)

    def test_grasp_germ_set_optimization_returns_none_on_incomplete_initial_set(self):
        soln = germsel.grasp_germ_set_optimization(
            self.neighbors, self.good_germs[:-1], alpha=0.1, **self.options
        )
        self.assertIsNone(soln)


class GreedyGermSelectionTester(GermSelectionWithNeighbors, BaseCase):
    def setUp(self):
        super(GreedyGermSelectionTester, self).setUp()
        self.options = dict(
            randomize=False,
            threshold=1e6,
            opPenalty=1.0,
            seed=_SEED,
            verbosity=1
        )

    def test_build_up(self):
        germs = germsel.build_up(self.neighbors, self.germ_set, **self.options)
        # TODO assert correctness

    def test_build_up_force_strings(self):
        forceStrs = pc.circuit_list([('Gx',), ('Gy')])
        germs = germsel.build_up(
            self.neighbors, self.germ_set, force=forceStrs, **self.options
        )
        # TODO assert correctness

    def test_build_up_returns_none_on_incomplete_initial_set(self):
        germs = germsel.build_up(
            self.neighbors, self.good_germs[:-1], **self.options
        )
        self.assertIsNone(germs)

    def test_build_up_breadth(self):
        germs = germsel.build_up_breadth(self.neighbors, self.germ_set, **self.options)
        # TODO assert correctness

        algorithm_kwargs = dict(
            germsList=self.germ_set,
            **self.options
        )
        germs_driver = germsel.generate_germs(
            self.mdl_target_noisy, randomize=False, algorithm='greedy',
            algorithm_kwargs=algorithm_kwargs
        )
        # TODO assert correctness

    def test_build_up_breadth_force_strings(self):
        forceStrs = pc.circuit_list([('Gx',), ('Gy')])
        germs = germsel.build_up_breadth(
            self.neighbors, self.germ_set, force=forceStrs, **self.options
        )
        # TODO assert correctness

    def test_build_up_breadth_returns_none_on_incomplete_initial_set(self):
        germs = germsel.build_up_breadth(
            self.neighbors, self.good_germs[:-1], **self.options
        )
        self.assertIsNone(germs)

    def test_build_up_breadth_raises_on_out_of_memory(self):
        with self.assertRaises(MemoryError):
            germsel.build_up_breadth(
                self.neighbors, self.germ_set, memLimit=1024,
                **self.options
            )
