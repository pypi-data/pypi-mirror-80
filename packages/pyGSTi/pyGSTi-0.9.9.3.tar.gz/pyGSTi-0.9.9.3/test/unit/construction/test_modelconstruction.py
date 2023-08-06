import scipy
import numpy as np

from ..util import BaseCase

import pygsti
import pygsti.construction.modelconstruction as mc


class ModelConstructionTester(BaseCase):
    def setUp(self):
        #OK for these tests, since we test user interface?
        #Set Model objects to "strict" mode for testing
        pygsti.objects.ExplicitOpModel._strict = False

    def test_build_basis_gateset(self):
        modelA = mc.build_explicit_model(
            [('Q0',)], ['Gi', 'Gx', 'Gy'],
            ["I(Q0)", "X(pi/2,Q0)", "Y(pi/2,Q0)"]
        )
        modelB = mc.basis_build_explicit_model(
            [('Q0',)], pygsti.Basis.cast('gm', 4),
            ['Gi', 'Gx', 'Gy'], ["I(Q0)", "X(pi/2,Q0)", "Y(pi/2,Q0)"]
        )
        self.assertAlmostEqual(modelA.frobeniusdist(modelB), 0)
        # TODO assert correctness

    def test_build_model(self):
        # TODO this isn't a unit test
        stateSpace = [(4,)]  # density matrix is a 2x2 matrix
        spaceLabels = [('Q0',)]  # interpret the 2x2 density matrix as a single qubit named 'Q0'
        model1 = pygsti.objects.ExplicitOpModel(['Q0'])
        model1['rho0'] = mc.build_vector(stateSpace, spaceLabels, "0")
        model1['Mdefault'] = pygsti.obj.UnconstrainedPOVM([('0', mc.build_vector(stateSpace, spaceLabels, "0")),
                                                           ('1', mc.build_vector(stateSpace, spaceLabels, "1"))])
        model1['Gi'] = mc.build_operation(stateSpace, spaceLabels, "I(Q0)")
        model1['Gx'] = mc.build_operation(stateSpace, spaceLabels, "X(pi/2,Q0)")
        model1['Gy'] = mc.build_operation(stateSpace, spaceLabels, "Y(pi/2,Q0)")

    def test_build_explicit_model(self):
        model = mc.build_explicit_model([('Q0',)],
                                        ['Gi', 'Gx', 'Gy'], ["I(Q0)", "X(pi/2,Q0)", "Y(pi/2,Q0)"])
        self.assertEqual(set(model.operations.keys()), set(['Gi', 'Gx', 'Gy']))
        self.assertAlmostEqual(sum(model.probs(('Gx', 'Gi', 'Gy')).values()), 1.0)
        self.assertEqual(model.num_params(), 60)

        model2 = mc.build_explicit_model([('Q0',)], ['Gi', 'Gx', 'Gy'], ["I(Q0)", "X(pi/2,Q0)", "Y(pi/2,Q0)"])

        gateset2b = mc.build_explicit_model([('Q0',)], ['Gi', 'Gx', 'Gy'],
                                            ["I(Q0)", "X(pi/2,Q0)", "Y(pi/2,Q0)"],
                                            effectLabels=['1', '0'])

        std_gateset = mc.build_explicit_model([('Q0',)], ['Gi', 'Gx', 'Gy'],
                                              ["I(Q0)", "X(pi/8,Q0)", "Y(pi/8,Q0)"],
                                              basis="std")

        pp_gateset = mc.build_explicit_model([('Q0',)], ['Gi', 'Gx', 'Gy'],
                                             ["I(Q0)", "X(pi/8,Q0)", "Z(pi/8,Q0)"],
                                             basis="pp")
        # TODO assert correctness

    def test_build_crosstalk_free_model(self):
        nQubits = 2

        mdl = mc.build_crosstalk_free_model(
            nQubits, ('Gi', 'Gx', 'Gy', 'Gcnot'),
            {}, ensure_composed_gates=True,
            independent_gates=False
        )
        assert(set(mdl.operation_blks['gates'].keys()) == set(["Gi", "Gx", "Gy", "Gcnot"]))
        assert(set(mdl.operation_blks['layers'].keys()) == set(
            [('Gi', 0), ('Gi', 1), ('Gx', 0), ('Gx', 1), ('Gy', 0), ('Gy', 1), ('Gcnot', 0, 1), ('Gcnot', 1, 0)]))
        self.assertEqual(mdl.num_params(), 0)

        addlErr = pygsti.obj.TPDenseOp(np.identity(4, 'd'))  # adds 12 params
        addlErr2 = pygsti.obj.TPDenseOp(np.identity(4, 'd'))  # adds 12 params

        mdl.operation_blks['gates']['Gx'].append(addlErr)
        mdl.operation_blks['gates']['Gy'].append(addlErr2)
        mdl.operation_blks['gates']['Gi'].append(addlErr)

        self.assertEqual(mdl.num_params(), 24)

        self.assertEqual(mdl.operation_blks['layers'][('Gx', 0)].gpindices, slice(0, 12))
        self.assertEqual(mdl.operation_blks['layers'][('Gy', 0)].gpindices, slice(12, 24))
        self.assertEqual(mdl.operation_blks['layers'][('Gi', 0)].gpindices, slice(0, 12))
        self.assertEqual(mdl.operation_blks['gates']['Gx'].gpindices, slice(0, 12))
        self.assertEqual(mdl.operation_blks['gates']['Gy'].gpindices, slice(12, 24))
        self.assertEqual(mdl.operation_blks['gates']['Gi'].gpindices, slice(0, 12))

        # Case: ensure_composed_gates=False, independent_gates=True
        cfmdl = mc.build_crosstalk_free_model(
            nQubits, ('Gx', 'Gy', 'Gcnot'),
            {'Gx': 0.1,  # depol
             'Gy': (0.02, 0.02, 0.02),  # pauli stochastic
             # errgen: BUG? when SIX too large -> no coeff corresponding to rate?
             'Gcnot': {('H', 'ZZ'): 0.01, ('S', 'IX'): 0.01},
             'idle': 0.01, 'prep': 0.01, 'povm': 0.01
             }, qubit_labels=['qb{}'.format(i) for i in range(nQubits)],
            ensure_composed_gates=False, independent_gates=True)

        self.assertEqual(cfmdl.num_params(), 17)

        # Case: ensure_composed_gates=True, independent_gates=False
        cfmdl2 = mc.build_crosstalk_free_model(
            nQubits, ('Gx', 'Gy', 'Gcnot'),
            {'Gx': 0.1,  # depol
             'Gy': (0.02, 0.02, 0.02),  # pauli stochastic
             'Gcnot': {'HZZ': 0.01, 'SIX': 0.01},  # errgen: BUG? when SIX too large -> no coeff corresponding to rate?
             'idle': 0.01, 'prep': 0.01, 'povm': 0.01
             }, qubit_labels=['qb{}'.format(i) for i in range(nQubits)],
            ensure_composed_gates=True, independent_gates=False)
        self.assertEqual(cfmdl2.num_params(), 11)

        # Same as above but add ('Gx','qb0') to test giving qubit-specific error rates
        cfmdl3 = mc.build_crosstalk_free_model(
            nQubits, ('Gx', 'Gy', 'Gcnot'),
            {'Gx': 0.1,  # depol
             ('Gx', 'qb0'): 0.2,  # adds another independent depol param for Gx:qb0
             'Gy': (0.02, 0.02, 0.02),  # pauli stochastic
             'Gcnot': {'HZZ': 0.01, 'SIX': 0.01},  # errgen: BUG? when SIX too large -> no coeff corresponding to rate?
             'idle': 0.01, 'prep': 0.01, 'povm': 0.01
             }, qubit_labels=['qb{}'.format(i) for i in range(nQubits)],
            ensure_composed_gates=True, independent_gates=False)
        self.assertEqual(cfmdl3.num_params(), 12)

    def test_build_crosstalk_free_model_with_nonstd_gate_unitary_factory(self):
        nQubits = 2

        def fn(args):
            if args is None: args = (0,)
            a, = args
            sigmaZ = np.array([[1, 0], [0, -1]], 'd')
            return scipy.linalg.expm(1j * float(a) * sigmaZ)

        cfmdl = mc.build_crosstalk_free_model(nQubits, ('Gx', 'Gy', 'Gcnot', 'Ga'),
                                              {}, nonstd_gate_unitaries={'Ga': fn})

        c = pygsti.obj.Circuit("Gx:1Ga;0.3:1Gx:1@(0,1)")
        p = cfmdl.probs(c)

        self.assertAlmostEqual(p['00'], 0.08733219254516078)
        self.assertAlmostEqual(p['01'], 0.9126678074548386)

    def test_build_operation_raises_on_bad_parameterization(self):
        with self.assertRaises(ValueError):
            mc.build_operation([(4, 4)], [('Q0', 'Q1')], "X(pi,Q0)", "gm", parameterization="FooBar")

    def test_build_explicit_model_raises_on_bad_state(self):
        with self.assertRaises(ValueError):
            mc.build_explicit_model([('A0',)], ['Gi', 'Gx', 'Gy'],
                                    ["I(Q0)", "X(pi/8,Q0)", "Y(pi/8,Q0)"])

    def test_build_explicit_model_raises_on_bad_basis(self):
        with self.assertRaises(AssertionError):
            mc.build_explicit_model([('Q0',)], ['Gi', 'Gx', 'Gy'],
                                    ["I(Q0)", "X(pi/8,Q0)", "Y(pi/8,Q0)"],
                                    basis="FooBar")

    def test_build_explicit_model_raises_on_bad_rho_expression(self):
        with self.assertRaises(ValueError):
            mc.build_explicit_model([('Q0',)], ['Gi', 'Gx', 'Gy'],
                                    ["I(Q0)", "X(pi/8,Q0)", "Y(pi/8,Q0)"],
                                    prepLabels=['rho0'], prepExpressions=["FooBar"],)

    def test_build_explicit_model_raises_on_bad_effect_expression(self):
        with self.assertRaises(ValueError):
            mc.build_explicit_model([('Q0',)], ['Gi', 'Gx', 'Gy'],
                                    ["I(Q0)", "X(pi/8,Q0)", "Y(pi/8,Q0)"],
                                    effectLabels=['0', '1'], effectExpressions=["FooBar", "1"])


class GateConstructionBase(object):
    def setUp(self):
        pygsti.objects.ExplicitOpModel._strict = False

    def _construct_gates(self, param):
        # TODO these aren't really unit tests
        #CNOT gate
        Ucnot = np.array([[1, 0, 0, 0],
                          [0, 1, 0, 0],
                          [0, 0, 0, 1],
                          [0, 0, 1, 0]], 'd')
        cnotMx = pygsti.tools.unitary_to_process_mx(Ucnot)
        self.CNOT_chk = pygsti.tools.change_basis(cnotMx, "std", self.basis)

        #CPHASE gate
        Ucphase = np.array([[1, 0, 0, 0],
                            [0, 1, 0, 0],
                            [0, 0, 1, 0],
                            [0, 0, 0, -1]], 'd')
        cphaseMx = pygsti.tools.unitary_to_process_mx(Ucphase)
        self.CPHASE_chk = pygsti.tools.change_basis(cphaseMx, "std", self.basis)
        self.ident = mc.build_operation([(4,)], [('Q0',)], "I(Q0)", self.basis, param)
        self.rotXa = mc.build_operation([(4,)], [('Q0',)], "X(pi/2,Q0)", self.basis, param)
        self.rotX2 = mc.build_operation([(4,)], [('Q0',)], "X(pi,Q0)", self.basis, param)
        self.rotYa = mc.build_operation([(4,)], [('Q0',)], "Y(pi/2,Q0)", self.basis, param)
        self.rotZa = mc.build_operation([(4,)], [('Q0',)], "Z(pi/2,Q0)", self.basis, param)
        self.rotNa = mc.build_operation([(4,)], [('Q0',)], "N(pi/2,1.0,0.5,0,Q0)", self.basis, param)
        self.iwL = mc.build_operation([(4, 1)], [('Q0', 'L0')], "I(Q0)", self.basis, param)
        self.CnotA = mc.build_operation([(4, 4)], [('Q0', 'Q1')], "CX(pi,Q0,Q1)", self.basis, param)
        self.CY = mc.build_operation([(4, 4)], [('Q0', 'Q1')], "CY(pi,Q0,Q1)", self.basis, param)
        self.CZ = mc.build_operation([(4, 4)], [('Q0', 'Q1')], "CZ(pi,Q0,Q1)", self.basis, param)
        self.CNOT = mc.build_operation([(4, 4)], [('Q0', 'Q1')], "CNOT(Q0,Q1)", self.basis, param)
        self.CPHASE = mc.build_operation([(4, 4)], [('Q0', 'Q1')], "CPHASE(Q0,Q1)", self.basis, param)

    def test_construct_gates_static(self):
        self._construct_gates('static')

    def test_construct_gates_TP(self):
        self._construct_gates('TP')

    def test_construct_gates_full(self):
        self._construct_gates('full')

        self.leakA = mc.build_operation([(1,), (1,), (1,)], [('L0',), ('L1',), ('L2',)],
                                        "LX(pi,0,1)", self.basis, 'full')
        self.rotLeak = mc.build_operation([(4,), (1,)], [('Q0',), ('L0',)],
                                          "X(pi,Q0):LX(pi,0,2)", self.basis, 'full')
        self.leakB = mc.build_operation([(4,), (1,)], [('Q0',), ('L0',)], "LX(pi,0,2)", self.basis, 'full')
        self.rotXb = mc.build_operation([(4,), (1,), (1,)], [('Q0',), ('L0',), ('L1',)],
                                        "X(pi,Q0)", self.basis, 'full')
        self.CnotB = mc.build_operation([(4, 4), (1,)], [('Q0', 'Q1'), ('L0',)], "CX(pi,Q0,Q1)", self.basis, 'full')

    def _test_leakA(self):
        leakA_ans = np.array([[0., 1., 0.],
                              [1., 0., 0.],
                              [0., 0., 1.]], 'd')
        self.assertArraysAlmostEqual(self.leakA, leakA_ans)

    def _test_rotXa(self):
        rotXa_ans = np.array([[1., 0., 0., 0.],
                              [0., 1., 0., 0.],
                              [0., 0., 0, -1.],
                              [0., 0., 1., 0]], 'd')
        self.assertArraysAlmostEqual(self.rotXa, rotXa_ans)

    def _test_rotX2(self):
        rotX2_ans = np.array([[1., 0., 0., 0.],
                              [0., 1., 0., 0.],
                              [0., 0., -1., 0.],
                              [0., 0., 0., -1.]], 'd')
        self.assertArraysAlmostEqual(self.rotX2, rotX2_ans)

    def _test_rotLeak(self):
        rotLeak_ans = np.array([[0.5, 0., 0., -0.5, 0.70710678],
                                [0., 0., 0., 0., 0.],
                                [0., 0., 0., 0., 0.],
                                [0.5, 0., 0., -0.5, -0.70710678],
                                [0.70710678, 0., 0., 0.70710678, 0.]], 'd')
        self.assertArraysAlmostEqual(self.rotLeak, rotLeak_ans)

    def _test_leakB(self):
        leakB_ans = np.array([[0.5, 0., 0., -0.5, 0.70710678],
                              [0., 0., 0., 0., 0.],
                              [0., 0., 0., 0., 0.],
                              [-0.5, 0., 0., 0.5, 0.70710678],
                              [0.70710678, 0., 0., 0.70710678, 0.]], 'd')
        self.assertArraysAlmostEqual(self.leakB, leakB_ans)

    def _test_rotXb(self):
        rotXb_ans = np.array([[1., 0., 0., 0., 0., 0.],
                              [0., 1., 0., 0., 0., 0.],
                              [0., 0., -1., 0., 0., 0.],
                              [0., 0., 0., -1., 0., 0.],
                              [0., 0., 0., 0., 1., 0.],
                              [0., 0., 0., 0., 0., 1.]], 'd')
        self.assertArraysAlmostEqual(self.rotXb, rotXb_ans)

    def _test_CnotA(self):
        CnotA_ans = np.array([[1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 1.0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, -1.0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, -1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, -1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1.0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 0, 0],
                              [0, 0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
        self.assertArraysAlmostEqual(self.CnotA, CnotA_ans)

    def _test_CnotB(self):
        CnotB_ans = np.array([[1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, -1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, -1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, -1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1.0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 0, 0, 0],
                              [0, 0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0]])
        self.assertArraysAlmostEqual(self.CnotB, CnotB_ans)

    def test_raises_on_bad_basis(self):
        with self.assertRaises(AssertionError):
            mc.build_operation([(4,)], [('Q0',)], "X(pi/2,Q0)", "FooBar", 'std')

    def test_raises_on_bad_gate_name(self):
        with self.assertRaises(ValueError):
            mc.build_operation([(4,)], [('Q0',)], "FooBar(Q0)", self.basis, 'std')

    def test_raises_on_bad_state_spec(self):
        with self.assertRaises(KeyError):
            mc.build_operation([(4,)], [('A0',)], "I(Q0)", self.basis, 'std')

    def test_raises_on_bad_label(self):
        with self.assertRaises(KeyError):
            mc.build_operation([(4,)], [('Q0', 'L0')], "I(Q0,A0)", self.basis, 'std')

    def test_raises_on_state_space_dim_mismatch(self):
        with self.assertRaises(TypeError):
            mc.build_operation([2], [('Q0',)], "I(Q0)", self.basis, 'std')

    def test_raises_on_qubit_state_space_mismatch(self):
        with self.assertRaises(ValueError):
            mc.build_operation([(4,), (4,)], [('Q0',), ('Q1',)], "CZ(pi,Q0,Q1)", self.basis, 'std')

    def test_raises_on_LX_with_bad_basis_spec(self):
        with self.assertRaises(AssertionError):
            mc.build_operation([(4,), (1,)], [('Q0',), ('L0',)], "LX(pi,0,2)", "foobar", 'std')


class PauliGateConstructionTester(GateConstructionBase, BaseCase):
    basis = 'pp'


class StdGateConstructionTester(GateConstructionBase, BaseCase):
    basis = 'std'

    def test_construct_gates_full(self):
        super(StdGateConstructionTester, self).test_construct_gates_full()
        self._test_leakA()


class GellMannGateConstructionTester(GateConstructionBase, BaseCase):
    basis = 'gm'

    def test_construct_gates_TP(self):
        super(GellMannGateConstructionTester, self).test_construct_gates_TP()
        self._test_rotXa()
        self._test_rotX2()

        self._test_CnotA()

    def test_construct_gates_static(self):
        super(GellMannGateConstructionTester, self).test_construct_gates_static()
        self._test_rotXa()
        self._test_rotX2()

        self._test_CnotA()

    def test_construct_gates_full(self):
        super(GellMannGateConstructionTester, self).test_construct_gates_full()
        self._test_leakA()
        self._test_rotXa()
        self._test_rotX2()

        self._test_rotLeak()
        self._test_leakB()
        self._test_rotXb()

        self._test_CnotA()
        self._test_CnotB()
