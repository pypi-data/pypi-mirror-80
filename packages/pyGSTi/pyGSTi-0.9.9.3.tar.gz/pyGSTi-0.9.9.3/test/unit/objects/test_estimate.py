import pickle
from unittest import mock

from ..util import BaseCase
from . import fixtures as pkg

from pygsti.modelpacks.legacy import std1Q_XYI as std
from pygsti.objects.results import Results
from pygsti.objects import estimate


class EstimateBase(object):
    @classmethod
    def setUpClass(cls):
        cls.model = pkg.mdl_lsgst_go
        cls.maxLengthList = pkg.maxLengthList

        cls.res = Results()
        cls.res.init_dataset(pkg.dataset)
        cls.res.init_circuits(pkg.lsgstStructs)

    def setUp(self):
        self.model = self.model.copy()
        self.res = self.res.copy()

    def test_get_effective_dataset(self):
        # Get effective estimate dataset
        effds = self.est.get_effective_dataset()
        effds, subMxs = self.est.get_effective_dataset(return_subMxs=True)
        # TODO assert correctness

    def test_view(self):
        #Estimate views
        est_view = self.est.view(None)
        est_view = self.est.view(['test'])
        # TODO assert correctness

    def test_to_string(self):
        #Estimate & results render as str
        s = str(self.est)
        # TODO assert correctness

    def test_pickle(self):
        s = pickle.dumps(self.est)
        est_pickled = pickle.loads(s)
        # TODO assert correctness


class ResultsEstimateTester(EstimateBase, BaseCase):
    def setUp(self):
        super(ResultsEstimateTester, self).setUp()
        self.res.add_estimate(
            std.target_model(), std.target_model(),
            [self.model] * len(self.maxLengthList),
            parameters={'objective': 'logl'},
            estimate_key="default"
        )
        self.est = self.res.estimates['default']

    def test_add_gaugeoptimized(self):
        # TODO optimize
        goparams = {'itemWeights': {'gates': 1.0, 'spam': 0.1},
                    'method': 'BFGS'}  # method so we don't need a legit comm
        self.est.add_gaugeoptimized(goparams, label="test", comm=None, verbosity=None)
        # TODO assert correctness


class EmptyEstimateTester(EstimateBase, BaseCase):
    def setUp(self):
        super(EmptyEstimateTester, self).setUp()
        self.est = estimate.Estimate(self.res)

    def test_add_gaugeoptimized_raises_on_no_model(self):
        with self.assertRaises(ValueError):
            goparams = {'itemWeights': {'gates': 1.0, 'spam': 0.1}, 'targetModel': self.model}
            self.est.add_gaugeoptimized(goparams, label="test", comm=None, verbosity=None)  # goparams must have 'model'

    def test_add_gaugeoptimized_raises_on_no_target_model(self):
        with self.assertRaises(ValueError):
            goparams = {'itemWeights': {'gates': 1.0, 'spam': 0.1}, 'model': self.model}
            self.est.add_gaugeoptimized(goparams, label="test", comm=None,
                                        verbosity=None)  # goparams must have 'targetModel'
