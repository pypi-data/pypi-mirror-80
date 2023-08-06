import unittest
import pygsti
import numpy as np
import warnings
import pickle
import os

from pygsti.modelpacks.legacy import std1Q_XYI as std

from ..testutils import BaseTestCase, compare_files, temp_files

# This class is for unifying some models that get used in this file and in testGateSets2.py
class InstrumentTestCase(BaseTestCase):

    def setUp(self):
        #Add an instrument to the standard target model
        self.target_model = std.target_model()
        E = self.target_model.povms['Mdefault']['0']
        Erem = self.target_model.povms['Mdefault']['1']
        Gmz_plus = np.dot(E,E.T)
        Gmz_minus = np.dot(Erem,Erem.T)
        self.target_model.instruments['Iz'] = pygsti.obj.Instrument({'plus': Gmz_plus, 'minus': Gmz_minus})
        self.povm_ident = self.target_model.povms['Mdefault']['0'] + self.target_model.povms['Mdefault']['1']

        self.mdl_target_wTP = self.target_model.copy()
        self.mdl_target_wTP.instruments['IzTP'] = pygsti.obj.TPInstrument({'plus': Gmz_plus, 'minus': Gmz_minus})

        super(InstrumentTestCase, self).setUp()

    def testFutureFunctionality(self):
        #Test instrument construction with elements whose gpindices are already initialized.
        # Since this isn't allowed currently (a future functionality), we need to do some hacking
        E = self.target_model.povms['Mdefault']['0']
        InstEl = pygsti.obj.FullDenseOp( np.dot(E,E.T) )
        InstEl2 = InstEl.copy()
        nParams = InstEl.num_params() # should be 16

        I = pygsti.obj.Instrument({})
        InstEl.set_gpindices(slice(0,16), I)
        InstEl2.set_gpindices(slice(8,24), I) # some overlap - to test _build_paramvec

        # TESTING ONLY - so we can add items!!!
        I._readonly = False
        I['A'] = InstEl
        I['B'] = InstEl2
        I._readonly = True

        I._paramvec = I._build_paramvec()
          # this whole test was to exercise this function's ability to
          # form a parameter vector with weird overlapping gpindices.
        self.assertEqual( len(I._paramvec) , 24 )


    def testInstrumentMethods(self):

        v = self.mdl_target_wTP.to_vector()

        mdl = self.mdl_target_wTP.copy()
        mdl.from_vector(v)
        mdl.basis = self.mdl_target_wTP.basis.copy()

        self.assertAlmostEqual(mdl.frobeniusdist(self.mdl_target_wTP),0.0)

        for lbl in ('Iz','IzTP'):
            v = mdl.to_vector()
            gates = mdl.instruments[lbl].simplify_operations(prefix="ABC")
            for igate in gates.values():
                igate.from_vector(v[igate.gpindices]) # gpindices should be setup relative to Model's param vec

        mdl.depolarize(0.01)
        mdl.rotate((0,0,0.01))
        mdl.rotate(max_rotate=0.01, seed=1234)

    def testChangeDimension(self):
        mdl = self.target_model.copy()
        new_gs = mdl.increase_dimension(6)
        new_gs = mdl.decrease_dimension(3)

        #TP
        mdl = self.target_model.copy()
        mdl.set_all_parameterizations("TP")
        new_gs = mdl.increase_dimension(6)
        new_gs = mdl.decrease_dimension(3)


    def testIntermediateMeas(self):
        # Mess with the target model to add some error to the povm and instrument
        self.assertEqual(self.target_model.num_params(),92) # 4*3 + 16*5 = 92
        mdl = self.target_model.depolarize(op_noise=0.01, spam_noise=0.01)
        gs2 = self.target_model.depolarize(max_op_noise=0.01, max_spam_noise=0.01, seed=1234) #another way to depolarize
        mdl.povms['Mdefault'].depolarize(0.01)

        # Introducing a rotation error to the measurement
        Uerr = pygsti.rotation_gate_mx([0,0.02,0]) # input angles are halved by the method
        E = np.dot(mdl.povms['Mdefault']['0'].T,Uerr).T # effect is stored as column vector
        Erem = self.povm_ident - E
        mdl.povms['Mdefault'] = pygsti.obj.UnconstrainedPOVM({'0': E, '1': Erem})

        # Now add the post-measurement gates from the vector E0 and remainder = id-E0
        Gmz_plus = np.dot(E,E.T) #since E0 is stored internally as column spamvec
        Gmz_minus = np.dot(Erem,Erem.T)
        mdl.instruments['Iz'] = pygsti.obj.Instrument({'plus': Gmz_plus, 'minus': Gmz_minus})
        self.assertEqual(mdl.num_params(),92) # 4*3 + 16*5 = 92
        #print(mdl)

        germs = std.germs
        fiducials = std.fiducials
        max_lengths = [1] #,2,4,8]
        glbls = list(mdl.operations.keys()) + list(mdl.instruments.keys())
        lsgst_list = pygsti.construction.make_lsgst_experiment_list(
            glbls,fiducials,fiducials,germs,max_lengths)
        lsgst_list2 = pygsti.construction.make_lsgst_experiment_list(
            mdl,fiducials,fiducials,germs,max_lengths) #use mdl as source
        self.assertEqual(lsgst_list, lsgst_list2)



        mdl_datagen = mdl
        ds = pygsti.construction.generate_fake_data(mdl,lsgst_list,1000,'none') #'multinomial')
        pygsti.io.write_dataset(temp_files + "/intermediate_meas_dataset.txt",ds)
        ds2 = pygsti.io.load_dataset(temp_files + "/intermediate_meas_dataset.txt")
        for opstr,dsRow in ds.items():
            for lbl,cnt in dsRow.counts.items():
                self.assertAlmostEqual(cnt, ds2[opstr].counts[lbl],places=2)
        #print(ds)

        #LGST
        mdl_lgst = pygsti.do_lgst(ds, fiducials,fiducials, self.target_model) #, guessModelForGauge=mdl_datagen)
        self.assertTrue("Iz" in mdl_lgst.instruments)
        mdl_opt = pygsti.gaugeopt_to_target(mdl_lgst,mdl_datagen) #, method="BFGS")
        print(mdl_datagen.strdiff(mdl_opt))
        print("Frobdiff = ",mdl_datagen.frobeniusdist( mdl_lgst))
        print("Frobdiff after GOpt = ",mdl_datagen.frobeniusdist(mdl_opt))
        self.assertAlmostEqual(mdl_datagen.frobeniusdist(mdl_opt), 0.0, places=4)
        #print(mdl_lgst)
        #print(mdl_datagen)

        #DEBUG compiling w/dataset
        #dbList = pygsti.construction.make_lsgst_experiment_list(self.target_model,fiducials,fiducials,germs,max_lengths)
        ##self.target_model.simplify_circuits(dbList, ds)
        #self.target_model.simplify_circuits([ pygsti.obj.Circuit(None,stringrep="Iz") ], ds )
        #assert(False),"STOP"

        #LSGST
        results = pygsti.do_long_sequence_gst(ds,self.target_model,fiducials,fiducials,germs,max_lengths)
        #print(results.estimates['default'].models['go0'])
        mdl_est = results.estimates['default'].models['go0']
        mdl_est_opt = pygsti.gaugeopt_to_target(mdl_est,mdl_datagen)
        print("Frobdiff = ", mdl_datagen.frobeniusdist(mdl_est))
        print("Frobdiff after GOpt = ", mdl_datagen.frobeniusdist(mdl_est_opt))
        self.assertAlmostEqual(mdl_datagen.frobeniusdist(mdl_est_opt), 0.0, places=4)

        #LGST w/TP gates
        mdl_targetTP = self.target_model.copy()
        mdl_targetTP.set_all_parameterizations("TP")
        self.assertEqual(mdl_targetTP.num_params(),71) # 3 + 4*2 + 12*5 = 71
        #print(mdl_targetTP)
        resultsTP = pygsti.do_long_sequence_gst(ds,mdl_targetTP,fiducials,fiducials,germs,max_lengths)
        mdl_est = resultsTP.estimates['default'].models['go0']
        mdl_est_opt = pygsti.gaugeopt_to_target(mdl_est,mdl_datagen)
        print("TP Frobdiff = ", mdl_datagen.frobeniusdist(mdl_est))
        print("TP Frobdiff after GOpt = ", mdl_datagen.frobeniusdist(mdl_est_opt))
        self.assertAlmostEqual(mdl_datagen.frobeniusdist(mdl_est_opt), 0.0, places=4)

    def testBasicGatesetOps(self):
        # This test was made from a debug script used to get the code working
        model = pygsti.construction.build_explicit_model(
            [('Q0',)],['Gi','Gx','Gy'],
            [ "I(Q0)","X(pi/8,Q0)", "Y(pi/8,Q0)"])
        #    prepLabels=["rho0"], prepExpressions=["0"],
        #    effectLabels=["0","1"], effectExpressions=["0","complement"])

        v0 = pygsti.construction.basis_build_vector("0", pygsti.obj.Basis.cast("pp",4))
        v1 = pygsti.construction.basis_build_vector("1", pygsti.obj.Basis.cast("pp",4))
        P0 = np.dot(v0,v0.T)
        P1 = np.dot(v1,v1.T)
        print("v0 = ",v0)
        print("P0 = ",P0)
        print("P1 = ",P0)
        #print("P0+P1 = ",P0+P1)

        model.instruments["Itest"] = pygsti.obj.Instrument( [('0',P0),('1',P1)] )

        for param in ("full","TP","CPTP"):
            print(param)
            model.set_all_parameterizations(param)
            model.to_vector() # builds & cleans paramvec for tests below
            for lbl,obj in model.preps.items():
                print(lbl,':',obj.gpindices, pygsti.tools.length(obj.gpindices))
            for lbl,obj in model.povms.items():
                print(lbl,':',obj.gpindices, pygsti.tools.length(obj.gpindices))
                for sublbl,subobj in obj.items():
                    print("  > ",sublbl,':',subobj.gpindices, pygsti.tools.length(subobj.gpindices))
            for lbl,obj in model.operations.items():
                print(lbl,':',obj.gpindices, pygsti.tools.length(obj.gpindices))
            for lbl,obj in model.instruments.items():
                print(lbl,':',obj.gpindices, pygsti.tools.length(obj.gpindices))
                for sublbl,subobj in obj.items():
                    print("  > ",sublbl,':',subobj.gpindices, pygsti.tools.length(subobj.gpindices))


            print("NPARAMS = ",model.num_params())
            print("")


        print("PICKLING")

        x = model.preps #.copy(None)
        p = pickle.dumps(x) #model.preps)
        print("loading")
        preps = pickle.loads(p)
        self.assertEqual(list(preps.keys()),list(model.preps.keys()))

        #p = pickle.dumps(model.effects)
        #effects = pickle.loads(p)
        #assert(list(effects.keys()) == list(model.effects.keys()))

        p = pickle.dumps(model.operations)
        gates = pickle.loads(p)
        self.assertEqual(list(gates.keys()),list(model.operations.keys()))

        p = pickle.dumps(model)
        g = pickle.loads(p)
        self.assertAlmostEqual(model.frobeniusdist(g), 0.0)


        print("Model IO")
        pygsti.io.write_model(model, temp_files + "/testGateset.txt")
        model2 = pygsti.io.load_model(temp_files + "/testGateset.txt")
        self.assertAlmostEqual(model.frobeniusdist(model2),0.0)
        print("Multiplication")

        gatestring1 = ('Gx','Gy')
        gatestring2 = ('Gx','Gy','Gy')

        p1 = np.dot( model.operations['Gy'], model.operations['Gx'] )
        p2 = model.product(gatestring1, bScale=False)
        p3,scale = model.product(gatestring1, bScale=True)

        print(p1)
        print(p2)
        print(p3*scale)
        self.assertAlmostEqual(np.linalg.norm(p1-scale*p3),0.0)

        dp = model.dproduct(gatestring1)
        dp_flat = model.dproduct(gatestring1,flat=True)

        evt, lookup, outcome_lookup = model.bulk_evaltree( [gatestring1,gatestring2] )

        p1 = np.dot( model.operations['Gy'], model.operations['Gx'] )
        p2 = np.dot( model.operations['Gy'], np.dot( model.operations['Gy'], model.operations['Gx'] ))

        bulk_prods = model.bulk_product(evt)
        bulk_prods_scaled, scaleVals = model.bulk_product(evt, bScale=True)
        bulk_prods2 = scaleVals[:,None,None] * bulk_prods_scaled
        self.assertArraysAlmostEqual(bulk_prods[0],p1)
        self.assertArraysAlmostEqual(bulk_prods[1],p2)
        self.assertArraysAlmostEqual(bulk_prods2[0],p1)
        self.assertArraysAlmostEqual(bulk_prods2[1],p2)

        print("Probabilities")
        gatestring1 = ('Gx','Gy') #,'Itest')
        gatestring2 = ('Gx','Gy','Gy')

        evt, lookup, outcome_lookup = model.bulk_evaltree( [gatestring1,gatestring2] )

        p1 = np.dot( np.transpose(model.povms['Mdefault']['0'].todense()),
                     np.dot( model.operations['Gy'],
                             np.dot(model.operations['Gx'],
                                    model.preps['rho0'].todense())))
        probs = model.probs(gatestring1)
        print(probs)
        p20,p21 = probs[('0',)],probs[('1',)]

        #probs = model.probs(gatestring1, bUseScaling=True)
        #print(probs)
        #p30,p31 = probs['0'],probs['1']

        self.assertArraysAlmostEqual(p1,p20)
        #assertArraysAlmostEqual(p1,p30)
        #assertArraysAlmostEqual(p21,p31)

        bulk_probs = model.bulk_probs([gatestring1,gatestring2],check=True)

        evt_split = evt.copy()
        new_lookup = evt_split.split(lookup, numSubTrees=2)
        print("SPLIT TREE: new elIndices = ",new_lookup)
        probs_to_fill = np.empty( evt_split.num_final_elements(), 'd')
        model.bulk_fill_probs(probs_to_fill,evt_split,check=True)

        dProbs = model.dprobs(gatestring1)
        bulk_dProbs = model.bulk_dprobs([gatestring1,gatestring2], returnPr=False, check=True)

        hProbs = model.hprobs(gatestring1)
        bulk_hProbs = model.bulk_hprobs([gatestring1,gatestring2], returnPr=False, check=True)


        print("DONE")

    def testAdvancedGateStrs(self):
        #specify prep and/or povm labels in operation sequence:
        mdl_normal = pygsti.obj.Circuit( ('Gx',) )
        mdl_wprep = pygsti.obj.Circuit( ('rho0','Gx') )
        mdl_wpovm = pygsti.obj.Circuit( ('Gx','Mdefault') )
        mdl_wboth = pygsti.obj.Circuit( ('rho0','Gx','Mdefault') )

        #Now compute probabilities for these:
        model = self.target_model.copy()
        probs_normal = model.probs(mdl_normal)
        probs_wprep = model.probs(mdl_wprep)
        probs_wpovm = model.probs(mdl_wpovm)
        probs_wboth = model.probs(mdl_wboth)

        print(probs_normal)
        print(probs_wprep)
        print(probs_wpovm)
        print(probs_wboth)

        self.assertEqual( probs_normal, probs_wprep )
        self.assertEqual( probs_normal, probs_wpovm )
        self.assertEqual( probs_normal, probs_wboth )

        #now try bulk op
        bulk_probs = model.bulk_probs([mdl_normal, mdl_wprep, mdl_wpovm, mdl_wboth],check=True)

    def testWriteAndLoad(self):
        mdl = self.target_model.copy()

        s = str(mdl) #stringify with instruments

        for param in ('full','TP','CPTP','static'):
            print("Param: ",param)
            mdl.set_all_parameterizations(param)
            filename = temp_files + "/gateset_with_instruments_%s.txt" % param
            pygsti.io.write_model(mdl, filename)
            gs2 = pygsti.io.read_model(filename)

            self.assertAlmostEqual( mdl.frobeniusdist(gs2), 0.0 )
            for lbl in mdl.operations:
                self.assertEqual( type(mdl.operations[lbl]), type(gs2.operations[lbl]))
            for lbl in mdl.preps:
                self.assertEqual( type(mdl.preps[lbl]), type(gs2.preps[lbl]))
            for lbl in mdl.povms:
                self.assertEqual( type(mdl.povms[lbl]), type(gs2.povms[lbl]))
            for lbl in mdl.instruments:
                self.assertEqual( type(mdl.instruments[lbl]), type(gs2.instruments[lbl]))
