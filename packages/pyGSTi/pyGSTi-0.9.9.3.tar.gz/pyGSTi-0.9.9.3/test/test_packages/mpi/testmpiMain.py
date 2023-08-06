import unittest
import itertools
import time
import sys
import pickle
import numpy as np
from mpinoseutils import *

import pygsti
from pygsti.modelpacks.legacy import std1Q_XYI as std
from pygsti.objects import profiler

g_maxLengths = [1,2,4,8]
g_numSubTrees = 3

def assertGatesetsInSync(mdl, comm):
    if comm is not None:
        bc = mdl if comm.Get_rank() == 0 else None
        mdl_cmp = comm.bcast(bc, root=0)
        assert(mdl.frobeniusdist(mdl_cmp) < 1e-6)


def runAnalysis(obj, ds, prepStrs, effectStrs, gsTarget, lsgstStringsToUse,
                useFreqWeightedChiSq=False,
                minProbClipForWeighting=1e-4, fidPairList=None,
                comm=None, distributeMethod="circuits"):

    #Run LGST to get starting model
    assertGatesetsInSync(gsTarget, comm)
    mdl_lgst = pygsti.do_lgst(ds, prepStrs, effectStrs, gsTarget,
                             svdTruncateTo=gsTarget.dim, verbosity=3)

    assertGatesetsInSync(mdl_lgst, comm)
    mdl_lgst_go = pygsti.gaugeopt_to_target(mdl_lgst,gsTarget)

    assertGatesetsInSync(mdl_lgst_go, comm)

    #Run full iterative LSGST
    tStart = time.time()
    if obj == "chi2":
        all_gs_lsgst = pygsti.do_iterative_mc2gst(
            ds, mdl_lgst_go, lsgstStringsToUse,
            minProbClipForWeighting=minProbClipForWeighting,
            probClipInterval=(-1e5,1e5),
            verbosity=1, memLimit=3*(1024)**3, returnAll=True,
            useFreqWeightedChiSq=useFreqWeightedChiSq, comm=comm,
            distributeMethod=distributeMethod)
    elif obj == "logl":
        all_gs_lsgst = pygsti.do_iterative_mlgst(
            ds, mdl_lgst_go, lsgstStringsToUse,
            minProbClip=minProbClipForWeighting,
            probClipInterval=(-1e5,1e5),
            verbosity=1, memLimit=3*(1024)**3, returnAll=True,
            useFreqWeightedChiSq=useFreqWeightedChiSq, comm=comm,
            distributeMethod=distributeMethod)

    tEnd = time.time()
    print("Time = ",(tEnd-tStart)/3600.0,"hours")

    return all_gs_lsgst


def runOneQubit(obj, ds, lsgstStrings, comm=None, distributeMethod="circuits"):
    #specs = pygsti.construction.build_spam_specs(
    #    std.fiducials, prep_labels=std.target_model().get_prep_labels(),
    #    effect_labels=std.target_model().get_effect_labels())

    return runAnalysis(obj, ds, std.fiducials, std.fiducials, std.target_model(),
                        lsgstStrings, comm=comm,
                        distributeMethod=distributeMethod)


def create_fake_dataset(comm):
    fidPairList = None
    maxLengths = [1,2,4,8,16]
    nSamples = 1000
    #specs = pygsti.construction.build_spam_specs(
    #    std.fiducials, prep_labels=std.target_model().get_prep_labels(),
    #    effect_labels=std.target_model().get_effect_labels())
    #rhoStrs, EStrs = pygsti.construction.get_spam_strs(specs)

    rhoStrs = EStrs = std.fiducials
    lgstStrings = pygsti.construction.list_lgst_circuits(
        rhoStrs, EStrs, list(std.target_model().operations.keys()))
    lsgstStrings = pygsti.construction.make_lsgst_lists(
            list(std.target_model().operations.keys()), rhoStrs, EStrs,
            std.germs, maxLengths, fidPairList )

    lsgstStringsToUse = lsgstStrings
    allRequiredStrs = pygsti.remove_duplicates(lgstStrings + lsgstStrings[-1])

    if comm is None or comm.Get_rank() == 0:
        mdl_dataGen = std.target_model().depolarize(op_noise=0.1)
        dsFake = pygsti.construction.generate_fake_data(
            mdl_dataGen, allRequiredStrs, nSamples, sampleError="multinomial",
            seed=1234)
        dsFake = comm.bcast(dsFake, root=0)
    else:
        dsFake = comm.bcast(None, root=0)

    #for mdl in dsFake:
    #    if abs(dsFake[mdl]['0']-dsFake_cmp[mdl]['0']) > 0.5:
    #        print("DS DIFF: ",mdl, dsFake[mdl]['0'], "vs", dsFake_cmp[mdl]['0'] )
    return dsFake, lsgstStrings


@mpitest(4)
def test_MPI_products(comm):
    assert(comm.Get_size() == 4)
    #Create some model
    mdl = std.target_model()

    #Remove spam elements so product calculations have element indices <=> product indices
    del mdl.preps['rho0']
    del mdl.povms['Mdefault']

    mdl.kick(0.1,seed=1234)

    #Get some operation sequences
    maxLengths = [1,2,4,8]
    gstrs = pygsti.construction.make_lsgst_experiment_list(
        list(std.target_model().operations.keys()), std.fiducials, std.fiducials, std.germs, maxLengths)
    tree,lookup,outcome_lookup = mdl.bulk_evaltree(gstrs)
    split_tree = tree.copy()
    split_lookup = split_tree.split(lookup,numSubTrees=g_numSubTrees)

    # Check wrtFilter functionality in dproduct
    some_wrtFilter = [0,2,3,5,10]
    for s in gstrs[0:20]:
        result = mdl._fwdsim().dproduct(s, wrtFilter=some_wrtFilter)
        chk_result = mdl.dproduct(s) #no filtering
        for ii,i in enumerate(some_wrtFilter):
            assert(np.linalg.norm(chk_result[i]-result[ii]) < 1e-6)
        taken_chk_result = chk_result.take( some_wrtFilter, axis=0 )
        assert(np.linalg.norm(taken_chk_result-result) < 1e-6)


    #Check bulk products

      #bulk_product - no parallelization unless tree is split
    serial = mdl.bulk_product(tree, bScale=False)
    parallel = mdl.bulk_product(tree, bScale=False, comm=comm)
    assert(np.linalg.norm(serial-parallel) < 1e-6)

    serial_scl, sscale = mdl.bulk_product(tree, bScale=True)
    parallel, pscale = mdl.bulk_product(tree, bScale=True, comm=comm)
    assert(np.linalg.norm(serial_scl*sscale[:,None,None] -
                          parallel*pscale[:,None,None]) < 1e-6)

      # will use a split tree to parallelize
    parallel = mdl.bulk_product(split_tree, bScale=False, comm=comm)
    for i,opstr in enumerate(gstrs):
        assert(np.linalg.norm(serial[lookup[i]]-parallel[split_lookup[i]]) < 1e-6)

    parallel, pscale = mdl.bulk_product(split_tree, bScale=True, comm=comm)
    for i,opstr in enumerate(gstrs):
        assert(np.linalg.norm(serial_scl[lookup[i]]*sscale[lookup[i],None,None] -
                              parallel[split_lookup[i]]*pscale[split_lookup[i],None,None]) < 1e-6)


      #bulk_dproduct - no split tree => parallel by col
    serial = mdl.bulk_dproduct(tree, bScale=False)
    parallel = mdl.bulk_dproduct(tree, bScale=False, comm=comm)
    assert(np.linalg.norm(serial-parallel) < 1e-6)

    serial_scl, sscale = mdl.bulk_dproduct(tree, bScale=True)
    parallel, pscale = mdl.bulk_dproduct(tree, bScale=True, comm=comm)
    assert(np.linalg.norm(serial_scl*sscale[:,None,None,None] -
                          parallel*pscale[:,None,None,None]) < 1e-6)

      # will just ignore a split tree for now (just parallel by col)
    parallel = mdl.bulk_dproduct(split_tree, bScale=False, comm=comm)
    for i,opstr in enumerate(gstrs):
        assert(np.linalg.norm(serial[lookup[i]] - parallel[split_lookup[i]]) < 1e-6)

    parallel, pscale = mdl.bulk_dproduct(split_tree, bScale=True, comm=comm)
    for i,opstr in enumerate(gstrs):
        assert(np.linalg.norm(serial_scl[lookup[i]]*sscale[lookup[i],None,None,None] -
                              parallel[split_lookup[i]]*pscale[split_lookup[i],None,None,None]) < 1e-6)



      #bulk_hproduct - no split tree => parallel by col
    serial = mdl.bulk_hproduct(tree, bScale=False)
    parallel = mdl.bulk_hproduct(tree, bScale=False, comm=comm)
    assert(np.linalg.norm(serial-parallel) < 1e-6)

    serial_scl, sscale = mdl.bulk_hproduct(tree, bScale=True)
    parallel, pscale = mdl.bulk_hproduct(tree, bScale=True, comm=comm)
    assert(np.linalg.norm(serial_scl*sscale[:,None,None,None,None] -
                          parallel*pscale[:,None,None,None,None]) < 1e-6)

      # will just ignore a split tree for now (just parallel by col)
    parallel = mdl.bulk_hproduct(split_tree, bScale=False, comm=comm)
    for i,opstr in enumerate(gstrs):
        assert(np.linalg.norm(serial[lookup[i]] - parallel[split_lookup[i]]) < 1e-6)

    parallel, pscale = mdl.bulk_hproduct(split_tree, bScale=True, comm=comm)
    for i,opstr in enumerate(gstrs):
        assert(np.linalg.norm(serial_scl[lookup[i]]*sscale[lookup[i],None,None,None,None] -
                              parallel[split_lookup[i]]*pscale[split_lookup[i],None,None,None,None]) < 1e-6)



#OLD: pr functions deprecated
#@mpitest(4)
#def test_MPI_pr(comm):
#
#    #Create some model
#    mdl = std.target_model()
#    mdl.kick(0.1,seed=1234)
#
#    #Get some operation sequences
#    maxLengths = g_maxLengths
#    gstrs = pygsti.construction.make_lsgst_experiment_list(
#        list(std.target_model().operations.keys()), std.fiducials, std.fiducials, std.germs, maxLengths)
#    tree,lookup,outcome_lookup = mdl.bulk_evaltree(gstrs)
#    split_tree = tree.copy()
#    lookup = split_tree.split(lookup,numSubTrees=g_numSubTrees)
#
#    #Check single-spam-label bulk probabilities
#
#    # non-split tree => automatically adjusts wrtBlockSize to accomodate
#    #                    the number of processors
#    serial = mdl.bulk_pr('0', tree, clipTo=(-1e6,1e6))
#    parallel = mdl.bulk_pr('0', tree, clipTo=(-1e6,1e6), comm=comm)
#    assert(np.linalg.norm(serial-parallel) < 1e-6)
#
#    serial = mdl.bulk_dpr('0', tree, clipTo=(-1e6,1e6))
#    parallel = mdl.bulk_dpr('0', tree, clipTo=(-1e6,1e6), comm=comm)
#    assert(np.linalg.norm(serial-parallel) < 1e-6)
#
#    serial, sp = mdl.bulk_dpr('0', tree, returnPr=True, clipTo=(-1e6,1e6))
#    parallel, pp = mdl.bulk_dpr('0', tree, returnPr=True, clipTo=(-1e6,1e6), comm=comm)
#    assert(np.linalg.norm(serial-parallel) < 1e-6)
#    assert(np.linalg.norm(sp-pp) < 1e-6)
#
#    serial, sdp, sp = mdl.bulk_hpr('0', tree, returnPr=True, returnDeriv=True,
#                             clipTo=(-1e6,1e6))
#    parallel, pdp, pp = mdl.bulk_hpr('0', tree, returnPr=True,
#                                 returnDeriv=True, clipTo=(-1e6,1e6), comm=comm)
#    assert(np.linalg.norm(serial-parallel) < 1e-6)
#    assert(np.linalg.norm(sdp-pdp) < 1e-6)
#    assert(np.linalg.norm(sp-pp) < 1e-6)
#
#
#    # split tree =>  distribures on sub-trees prior to adjusting
#    #                wrtBlockSize to accomodate remaining processors
#    serial = mdl.bulk_pr('0', tree, clipTo=(-1e6,1e6))
#    parallel = mdl.bulk_pr('0', split_tree, clipTo=(-1e6,1e6), comm=comm)
#    parallel = split_tree.permute_computation_to_original(parallel)
#    assert(np.linalg.norm(serial-parallel) < 1e-6)
#
#    serial = mdl.bulk_dpr('0', tree, clipTo=(-1e6,1e6))
#    parallel = mdl.bulk_dpr('0', split_tree, clipTo=(-1e6,1e6), comm=comm)
#    parallel = split_tree.permute_computation_to_original(parallel)
#    assert(np.linalg.norm(serial-parallel) < 1e-6)
#
#    serial, sp = mdl.bulk_dpr('0', tree, returnPr=True, clipTo=(-1e6,1e6))
#    parallel, pp = mdl.bulk_dpr('0', split_tree, returnPr=True, clipTo=(-1e6,1e6), comm=comm)
#    parallel = split_tree.permute_computation_to_original(parallel)
#    pp = split_tree.permute_computation_to_original(pp)
#    assert(np.linalg.norm(serial-parallel) < 1e-6)
#    assert(np.linalg.norm(sp-pp) < 1e-6)
#
#    serial, sdp, sp = mdl.bulk_hpr('0', tree, returnPr=True, returnDeriv=True,
#                             clipTo=(-1e6,1e6))
#    parallel, pdp, pp = mdl.bulk_hpr('0', split_tree, returnPr=True,
#                                 returnDeriv=True, clipTo=(-1e6,1e6), comm=comm)
#    parallel = split_tree.permute_computation_to_original(parallel)
#    pdp = split_tree.permute_computation_to_original(pdp)
#    pp = split_tree.permute_computation_to_original(pp)
#    assert(np.linalg.norm(serial-parallel) < 1e-6)
#    assert(np.linalg.norm(sdp-pdp) < 1e-6)
#    assert(np.linalg.norm(sp-pp) < 1e-6)



@mpitest(4)
def test_MPI_probs(comm):

    #Create some model
    mdl = std.target_model()
    mdl.kick(0.1,seed=1234)

    #Get some operation sequences
    maxLengths = g_maxLengths
    gstrs = pygsti.construction.make_lsgst_experiment_list(
        list(std.target_model().operations.keys()), std.fiducials, std.fiducials, std.germs, maxLengths)
    #tree,lookup,outcome_lookup = mdl.bulk_evaltree(gstrs)
    #split_tree = tree.copy()
    #lookup = split_tree.split(lookup, numSubTrees=g_numSubTrees)

    #Check all-spam-label bulk probabilities
    def compare_prob_dicts(a,b,indices=None):
        for opstr in gstrs:
            for outcome in a[opstr].keys():
                if indices is None:
                    assert(np.linalg.norm(a[opstr][outcome] -b[opstr][outcome]) < 1e-6)
                else:
                    for i in indices:
                        assert(np.linalg.norm(a[opstr][outcome][i] -b[opstr][outcome][i]) < 1e-6)

    # non-split tree => automatically adjusts wrtBlockSize to accomodate
    #                    the number of processors
    serial = mdl.bulk_probs(gstrs, clipTo=(-1e6,1e6))
    parallel = mdl.bulk_probs(gstrs, clipTo=(-1e6,1e6), comm=comm)
    compare_prob_dicts(serial,parallel)

    serial = mdl.bulk_dprobs(gstrs, clipTo=(-1e6,1e6))
    parallel = mdl.bulk_dprobs(gstrs, clipTo=(-1e6,1e6), comm=comm)
    compare_prob_dicts(serial,parallel)

    serial = mdl.bulk_dprobs(gstrs, returnPr=True, clipTo=(-1e6,1e6))
    parallel = mdl.bulk_dprobs(gstrs, returnPr=True, clipTo=(-1e6,1e6), comm=comm)
    compare_prob_dicts(serial,parallel,(0,1))

    serial = mdl.bulk_hprobs(gstrs, returnPr=True, returnDeriv=True,
                             clipTo=(-1e6,1e6))
    parallel = mdl.bulk_hprobs(gstrs, returnPr=True,
                                 returnDeriv=True, clipTo=(-1e6,1e6), comm=comm)
    compare_prob_dicts(serial,parallel,(0,1,2))

    ##OLD: cannot tell bulk_probs to use a split tree anymore (just give list)
    ## split tree =>  distribures on sub-trees prior to adjusting
    ##                wrtBlockSize to accomodate remaining processors
    #serial = mdl.bulk_probs(tree, clipTo=(-1e6,1e6))
    #parallel = mdl.bulk_probs(split_tree, clipTo=(-1e6,1e6), comm=comm)
    #for sl in serial:
    #    p = split_tree.permute_computation_to_original(parallel[sl])
    #    assert(np.linalg.norm(serial[sl]-p) < 1e-6)
    #
    #serial = mdl.bulk_dprobs(tree, clipTo=(-1e6,1e6))
    #parallel = mdl.bulk_dprobs(split_tree, clipTo=(-1e6,1e6), comm=comm)
    #for sl in serial:
    #    p = split_tree.permute_computation_to_original(parallel[sl])
    #    assert(np.linalg.norm(serial[sl]-p) < 1e-6)
    #
    #serial = mdl.bulk_dprobs(tree, returnPr=True, clipTo=(-1e6,1e6))
    #parallel = mdl.bulk_dprobs(split_tree, returnPr=True, clipTo=(-1e6,1e6), comm=comm)
    #for sl in serial:
    #    p0 = split_tree.permute_computation_to_original(parallel[sl][0])
    #    p1 = split_tree.permute_computation_to_original(parallel[sl][1])
    #    assert(np.linalg.norm(serial[sl][0]-p0) < 1e-6)
    #    assert(np.linalg.norm(serial[sl][1]-p1) < 1e-6)
    #
    #serial = mdl.bulk_hprobs(tree, returnPr=True, returnDeriv=True,
    #                        clipTo=(-1e6,1e6))
    #parallel = mdl.bulk_hprobs(split_tree, returnPr=True,
    #                          returnDeriv=True, clipTo=(-1e6,1e6), comm=comm)
    #for sl in serial:
    #    p0 = split_tree.permute_computation_to_original(parallel[sl][0])
    #    p1 = split_tree.permute_computation_to_original(parallel[sl][1])
    #    p2 = split_tree.permute_computation_to_original(parallel[sl][2])
    #    assert(np.linalg.norm(serial[sl][0]-p0) < 1e-6)
    #    assert(np.linalg.norm(serial[sl][1]-p1) < 1e-6)
    #    assert(np.linalg.norm(serial[sl][2]-p2) < 1e-6)



@mpitest(4)
def test_MPI_fills(comm):

    #Create some model
    mdl = std.target_model()
    mdl.kick(0.1,seed=1234)

    #Get some operation sequences
    maxLengths = g_maxLengths
    gstrs = pygsti.construction.make_lsgst_experiment_list(
        list(std.target_model().operations.keys()), std.fiducials, std.fiducials, std.germs, maxLengths)
    tree,lookup,outcome_lookup = mdl.bulk_evaltree(gstrs)
    split_tree = tree.copy()
    split_lookup = split_tree.split(lookup,numSubTrees=g_numSubTrees)


    #Check fill probabilities
    nEls = tree.num_final_elements()
    nCircuits = len(gstrs)
    nDerivCols = mdl.num_params()

    #Get serial results
    vhp_serial = np.empty( (nEls,nDerivCols,nDerivCols),'d')
    vdp_serial = np.empty( (nEls,nDerivCols), 'd' )
    vp_serial  = np.empty(  nEls, 'd' )

    vhp_serial2 = np.empty( (nEls,nDerivCols,nDerivCols),'d')
    vdp_serial2 = np.empty( (nEls,nDerivCols), 'd' )
    vp_serial2  = np.empty(  nEls, 'd' )

    mdl.bulk_fill_probs(vp_serial, tree,
                       (-1e6,1e6), comm=None)

    mdl.bulk_fill_dprobs(vdp_serial, tree,
                        vp_serial2, (-1e6,1e6), comm=None,
                        wrtBlockSize=None)
    assert(np.linalg.norm(vp_serial2-vp_serial) < 1e-6)

    mdl.bulk_fill_hprobs(vhp_serial, tree,
                        vp_serial2, vdp_serial2, (-1e6,1e6), comm=None,
                        wrtBlockSize1=None, wrtBlockSize2=None)
    assert(np.linalg.norm(vp_serial2-vp_serial) < 1e-6)
    assert(np.linalg.norm(vdp_serial2-vdp_serial) < 1e-6)


    #Check serial results with a split tree, just to be sure
    mdl.bulk_fill_probs(vp_serial2, split_tree,
                       (-1e6,1e6), comm=None)
    for i,opstr in enumerate(gstrs):
        assert(np.linalg.norm(vp_serial[ lookup[i] ] -
                              vp_serial2[ split_lookup[i] ]) < 1e-6)

    mdl.bulk_fill_dprobs(vdp_serial2, split_tree,
                        vp_serial2, (-1e6,1e6), comm=None,
                        wrtBlockSize=None)
    for i,opstr in enumerate(gstrs):
        assert(np.linalg.norm(vp_serial[ lookup[i] ] -
                              vp_serial2[ split_lookup[i] ]) < 1e-6)
        assert(np.linalg.norm(vdp_serial[ lookup[i] ] -
                              vdp_serial2[ split_lookup[i] ]) < 1e-6)

    mdl.bulk_fill_hprobs(vhp_serial2, split_tree,
                        vp_serial2, vdp_serial2, (-1e6,1e6), comm=None,
                        wrtBlockSize1=None, wrtBlockSize2=None)
    for i,opstr in enumerate(gstrs):
        assert(np.linalg.norm(vp_serial[ lookup[i] ] -
                              vp_serial2[ split_lookup[i] ]) < 1e-6)
        assert(np.linalg.norm(vdp_serial[ lookup[i] ] -
                              vdp_serial2[ split_lookup[i] ]) < 1e-6)
        assert(np.linalg.norm(vhp_serial[ lookup[i] ] -
                              vhp_serial2[ split_lookup[i] ]) < 1e-6)

    #Get parallel results - with and without split tree
    vhp_parallel = np.empty( (nEls,nDerivCols,nDerivCols),'d')
    vdp_parallel = np.empty( (nEls,nDerivCols), 'd' )
    vp_parallel = np.empty( nEls, 'd' )

    for tstTree,tstLookup in zip([tree, split_tree],[lookup,split_lookup]):

        mdl.bulk_fill_probs(vp_parallel, tstTree,
                           (-1e6,1e6), comm=comm)
        for i,opstr in enumerate(gstrs):
            assert(np.linalg.norm(vp_parallel[ tstLookup[i] ] -
                                  vp_serial[ lookup[i] ]) < 1e-6)

        for blkSize in [None, 4]:
            mdl.bulk_fill_dprobs(vdp_parallel, tstTree,
                                vp_parallel, (-1e6,1e6), comm=comm,
                                wrtBlockSize=blkSize)
            for i,opstr in enumerate(gstrs):
                assert(np.linalg.norm(vp_parallel[ tstLookup[i] ] -
                                      vp_serial[ lookup[i] ]) < 1e-6)
                assert(np.linalg.norm(vdp_parallel[ tstLookup[i] ] -
                                      vdp_serial[ lookup[i] ]) < 1e-6)

            for blkSize2 in [None, 2, 4]:
                mdl.bulk_fill_hprobs(vhp_parallel, tstTree,
                                    vp_parallel, vdp_parallel, (-1e6,1e6), comm=comm,
                                    wrtBlockSize1=blkSize, wrtBlockSize2=blkSize2)
                for i,opstr in enumerate(gstrs):
                    assert(np.linalg.norm(vp_parallel[ tstLookup[i] ] -
                                          vp_serial[ lookup[i] ]) < 1e-6)
                    assert(np.linalg.norm(vdp_parallel[ tstLookup[i] ] -
                                          vdp_serial[ lookup[i] ]) < 1e-6)
                    assert(np.linalg.norm(vhp_parallel[ tstLookup[i] ] -
                                          vhp_serial[ lookup[i] ]) < 1e-6)

    #Test Serial vs Parallel use of wrtFilter
    some_wrtFilter = [0,1,2,3,4,5,6,7] #must be contiguous now - not arbitraray
    some_wrtFilter2 = [6,7,8,9,10,11,12] #must be contiguous now - not arbitraray
    vhp_parallelF = np.empty( (nEls,nDerivCols,len(some_wrtFilter)),'d')
    vhp_parallelF2 = np.empty( (nEls,len(some_wrtFilter),len(some_wrtFilter2)),'d')
    vdp_parallelF = np.empty( (nEls,len(some_wrtFilter)), 'd' )

    for tstTree,tstLookup in zip([tree, split_tree],[lookup, split_lookup]):

        mdl._fwdsim().bulk_fill_dprobs(vdp_parallelF, tstTree,
                            None, (-1e6,1e6), comm=comm,
                            wrtFilter=some_wrtFilter, wrtBlockSize=None)
        for k,opstr in enumerate(gstrs):
            for ii,i in enumerate(some_wrtFilter):
                assert(np.linalg.norm(vdp_serial[lookup[k],i]-vdp_parallelF[tstLookup[k],ii]) < 1e-6)
        taken_result = vdp_serial.take( some_wrtFilter, axis=1 )
        for k,opstr in enumerate(gstrs):
            assert(np.linalg.norm(taken_result[lookup[k]]-vdp_parallelF[tstLookup[k]]) < 1e-6)

        mdl._fwdsim().bulk_fill_hprobs(vhp_parallelF, tstTree,
                        None, None,None, (-1e6,1e6), comm=comm,
                        wrtFilter2=some_wrtFilter, wrtBlockSize2=None)
        for k,opstr in enumerate(gstrs):
            for ii,i in enumerate(some_wrtFilter):
                assert(np.linalg.norm(vhp_serial[lookup[k],:,i]-vhp_parallelF[tstLookup[k],:,ii]) < 1e-6)
        taken_result = vhp_serial.take( some_wrtFilter, axis=2 )
        for k,opstr in enumerate(gstrs):
            assert(np.linalg.norm(taken_result[lookup[k]]-vhp_parallelF[tstLookup[k]]) < 1e-6)

        mdl._fwdsim().bulk_fill_hprobs(vhp_parallelF2, tstTree,
                        None, None,None, (-1e6,1e6), comm=comm,
                        wrtFilter1=some_wrtFilter, wrtFilter2=some_wrtFilter2)
        for k,opstr in enumerate(gstrs):
            for ii,i in enumerate(some_wrtFilter):
                for jj,j in enumerate(some_wrtFilter2):
                    assert(np.linalg.norm(vhp_serial[lookup[k],i,j]-vhp_parallelF2[tstLookup[k],ii,jj]) < 1e-6)
        taken_result = vhp_serial.take( some_wrtFilter, axis=1 ).take( some_wrtFilter2, axis=2)
        for k,opstr in enumerate(gstrs):
            assert(np.linalg.norm(taken_result[lookup[k]]-vhp_parallelF2[tstLookup[k]]) < 1e-6)

@mpitest(4)
def test_MPI_compute_cache(comm):
    #try to run hard-to-reach cases where there are lots of processors compared to
    # the number of elements being computed:
    from pygsti.modelpacks.legacy import std1Q_XY #nice b/c only 2 gates

    #Create some model
    mdl = std.target_model()
    mdl.kick(0.1,seed=1234)

    #Get some operation sequences
    gstrs = pygsti.construction.circuit_list([('Gx',), ('Gy')])
    tree,lookup,outcome_lookup = mdl.bulk_evaltree(gstrs)

    #Check fill probabilities
    nEls = tree.num_final_elements()
    nCircuits = len(gstrs)
    nDerivCols = mdl.num_params()
    print("NUMS = ",nEls,nCircuits,nDerivCols)

    #Get serial results
    vhp_serial = np.empty( (nEls,nDerivCols,nDerivCols),'d')

    d = mdl.dim
    slc1 = slice(0,2)
    slc2 = slice(0,2)
    scache = np.empty(nEls,'d')
    pcache = np.empty((nEls,d,d),'d')
    dcache1 = np.empty((nEls,2,d,d),'d')
    dcache2 = np.empty((nEls,2,d,d),'d')
    hcache = mdl._fwdsim()._compute_hproduct_cache(tree, pcache, dcache1, dcache2, scache,
                                                comm, wrtSlice1=slc1, wrtSlice2=slc2)

    #without comm
    hcache_chk = mdl._fwdsim()._compute_hproduct_cache(tree, pcache, dcache1, dcache2, scache,
                                                comm=None, wrtSlice1=slc1, wrtSlice2=slc2)
    assert(np.linalg.norm(hcache-hcache_chk) < 1e-6)



@mpitest(4)
def test_MPI_by_block(comm):

    #Create some model
    if comm is None or comm.Get_rank() == 0:
        mdl = std.target_model()
        mdl.kick(0.1,seed=1234)
        mdl = comm.bcast(mdl, root=0)
    else:
        mdl = comm.bcast(None, root=0)

    #Get some operation sequences
    maxLengths = g_maxLengths
    gstrs = pygsti.construction.make_lsgst_experiment_list(
        list(std.target_model().operations.keys()), std.fiducials, std.fiducials, std.germs, maxLengths)
    tree,lookup,outcome_lookkup = mdl.bulk_evaltree(gstrs)
    #split_tree = tree.copy()
    #split_lookup = split_tree.split(lookup,numSubTrees=g_numSubTrees)


    #Check that "by column" matches standard "at once" methods:
    nEls = tree.num_final_elements()
    nCircuits = len(gstrs)
    nDerivCols = mdl.num_params()

    #Get serial results
    vhp_serial = np.empty( (nEls,nDerivCols,nDerivCols),'d')
    vdp_serial = np.empty( (nEls,nDerivCols), 'd' )
    vp_serial = np.empty( nEls, 'd' )

    mdl.bulk_fill_hprobs(vhp_serial, tree,
                        vp_serial, vdp_serial, (-1e6,1e6), comm=None)
    dprobs12_serial = vdp_serial[:,:,None] * vdp_serial[:,None,:]


    for tstTree,tstLookup in zip([tree],[lookup]): # currently no split trees allowed (ValueError), split_tree]:
        hcols = []
        d12cols = []
        slicesList = [ (slice(0,nDerivCols),slice(i,i+1)) for i in range(nDerivCols) ]
        for s1,s2, hprobs, dprobs12 in mdl.bulk_hprobs_by_block(
            tstTree, slicesList, True, comm):
            hcols.append(hprobs)
            d12cols.append(dprobs12)

        all_hcols = np.concatenate( hcols, axis=2 )
        all_d12cols = np.concatenate( d12cols, axis=2 )


        #print "SHAPES:"
        #print "hcols[0] = ",hcols[0].shape
        #print "all_hcols = ",all_hcols.shape
        #print "all_d12cols = ",all_d12cols.shape
        #print "vhp_serial = ",vhp_serial.shape
        #print "dprobs12_serial = ",dprobs12_serial.shape

        #for i in range(all_hcols.shape[3]):
        #    print "Diff(%d) = " % i, np.linalg.norm(all_hcols[0,:,8:,i]-vhp_serial[0,:,8:,i])
        #    if np.linalg.norm(all_hcols[0,:,8:,i]-vhp_serial[0,:,8:,i]) > 1e-6:
        #        for j in range(all_hcols.shape[3]):
        #            print "Diff(%d,%d) = " % (i,j), np.linalg.norm(all_hcols[0,:,8:,i]-vhp_serial[0,:,8:,j])
        #    assert(np.linalg.norm(all_hcols[0,:,8:,i]-vhp_serial[0,:,8:,i]) < 1e-6)

        for i,opstr in enumerate(gstrs):
            assert(np.linalg.norm(all_hcols[tstLookup[i]]-vhp_serial[lookup[i]]) < 1e-6)

        #for i in range(all_d12cols.shape[3]):
        #    print "Diff(%d) = " % i, np.linalg.norm(all_d12cols[0,:,8:,i]-dprobs12_serial[0,:,8:,i])
        #    if np.linalg.norm(all_d12cols[0,:,8:,i]-dprobs12_serial[0,:,8:,i]) > 1e-6:
        #        for j in range(all_d12cols.shape[3]):
        #            print "Diff(%d,%d) = " % (i,j), np.linalg.norm(all_d12cols[0,:,8:,i]-dprobs12_serial[0,:,8:,j])

        for i,opstr in enumerate(gstrs):
            assert(np.linalg.norm(all_d12cols[tstLookup[i]]-dprobs12_serial[lookup[i]]) < 1e-6)


        hcols = []
        d12cols = []
        slicesList = [ (slice(2,12),slice(i,i+1)) for i in range(1,10) ]
        for s1,s2, hprobs, dprobs12 in mdl.bulk_hprobs_by_block(
            tstTree, slicesList, True, comm):
            hcols.append(hprobs)
            d12cols.append(dprobs12)

        all_hcols = np.concatenate( hcols, axis=2 )
        all_d12cols = np.concatenate( d12cols, axis=2 )
        for i,opstr in enumerate(gstrs):
            assert(np.linalg.norm(all_hcols[tstLookup[i]]-vhp_serial[lookup[i],2:12,1:10]) < 1e-6)
            assert(np.linalg.norm(all_d12cols[tstLookup[i]]-dprobs12_serial[lookup[i],2:12,1:10]) < 1e-6)


        hprobs_by_block = np.zeros(vhp_serial.shape,'d')
        dprobs12_by_block = np.zeros(dprobs12_serial.shape,'d')
        blocks1 = pygsti.tools.mpitools.slice_up_range(nDerivCols, 3)
        blocks2 = pygsti.tools.mpitools.slice_up_range(nDerivCols, 5)
        slicesList = list(itertools.product(blocks1,blocks2))
        for s1,s2, hprobs_blk, dprobs12_blk in mdl.bulk_hprobs_by_block(
            tstTree, slicesList, True, comm):
            hprobs_by_block[:,s1,s2] = hprobs_blk
            dprobs12_by_block[:,s1,s2] = dprobs12_blk

        for i,opstr in enumerate(gstrs):
            assert(np.linalg.norm(hprobs_by_block[tstLookup[i]]-vhp_serial[lookup[i]]) < 1e-6)
            assert(np.linalg.norm(dprobs12_by_block[tstLookup[i]]-dprobs12_serial[lookup[i]]) < 1e-6)



#SCRATCH
#if np.linalg.norm(chk_ret[0]-dGs) >= 1e-6:
#    #if bScale:
#    #    print "SCALED"
#    #    print chk_ret[-1]
#
#    rank = comm.Get_rank()
#    if rank == 0:
#        print "DEBUG: parallel mismatch"
#        print "len(all_results) = ",len(all_results)
#        print "diff = ",np.linalg.norm(chk_ret[0]-dGs)
#        for row in range(dGs.shape[0]):
#            rowA = my_results[0][row,:].flatten()
#            rowB = all_results[rank][0][row,:].flatten()
#            rowC = dGs[row,:].flatten()
#            chk_C = chk_ret[0][row,:].flatten()
#
#            def sp(ar):
#                for i,x in enumerate(ar):
#                    if abs(x) > 1e-4:
#                        print i,":", x
#            def spc(ar1,ar2):
#                for i,x in enumerate(ar1):
#                    if (abs(x) > 1e-4 or abs(ar2[i]) > 1e-4): # and abs(x-ar2[i]) > 1e-6:
#                        print i,":", x, ar2[i], "(", (x-ar2[i]), ")", "[",x/ar2[i],"]"
#
#            assert( _np.linalg.norm(rowA-rowB) < 1e-6)
#            assert( _np.linalg.norm(rowC[0:len(rowA)]-rowA) < 1e-6)
#            #if _np.linalg.norm(rowA) > 1e-6:
#            if _np.linalg.norm(rowC - chk_C) > 1e-6:
#                print "SCALE for row%d = %g" % (row,rest_of_result[-1][row])
#                print "CHKSCALE for row%d = %g" % (row,chk_ret[-1][row])
#                print "row%d diff = " % row, _np.linalg.norm(rowC - chk_C)
#                print "row%d (rank%d)A = " % (row,rank)
#                sp(rowA)
#                print "row%d (all vs check) = " % row
#                spc(rowC, chk_C)
#
#                assert(False)
#    assert(False)





@mpitest(4)
def test_MPI_gatestrings_chi2(comm):
    #Create dataset for serial and parallel runs
    ds,lsgstStrings = create_fake_dataset(comm)

    #Individual processors
    my1ProcResults = runOneQubit("chi2",ds,lsgstStrings)

    #Using all processors
    myManyProcResults = runOneQubit("chi2",ds,lsgstStrings,comm,"circuits")

    for i,(gs1,gs2) in enumerate(zip(my1ProcResults,myManyProcResults)):
        assertGatesetsInSync(gs1, comm)
        assertGatesetsInSync(gs2, comm)

        gs2_go = pygsti.gaugeopt_to_target(gs2, gs1, {'gates': 1.0, 'spam': 1.0})
        print("Frobenius distance %d (rank %d) = " % (i,comm.Get_rank()), gs1.frobeniusdist(gs2_go))
        if gs1.frobeniusdist(gs2_go) >= 1e-5:
            print("DIFF (%d) = " % comm.Get_rank(), gs1.strdiff(gs2_go))
        assert(gs1.frobeniusdist(gs2_go) < 1e-5)
    return


@mpitest(4)
def test_MPI_gaugeopt(comm):
    #Gauge Opt to Target
    mdl_other = std.target_model().depolarize(op_noise=0.01, spam_noise=0.01)
    mdl_other['Gx'].rotate( (0,0,0.01) )
    mdl_other['Gy'].rotate( (0,0,0.01) )
    mdl_gopt = pygsti.gaugeopt_to_target(mdl_other, std.target_model(), verbosity=10, comm=comm)

    #use a method that isn't parallelized with non-None comm (warning is given)
    mdl_gopt_slow = pygsti.gaugeopt_to_target(mdl_other, std.target_model(), verbosity=10, method="BFGS", comm=comm)


@mpitest(4)
def test_MPI_gatestrings_logl(comm):
    #Create dataset for serial and parallel runs
    ds,lsgstStrings = create_fake_dataset(comm)

    #Individual processors
    my1ProcResults = runOneQubit("logl",ds,lsgstStrings)

    #Using all processors
    myManyProcResults = runOneQubit("logl",ds,lsgstStrings,comm,"circuits")

    for i,(gs1,gs2) in enumerate(zip(my1ProcResults,myManyProcResults)):
        assertGatesetsInSync(gs1, comm)
        assertGatesetsInSync(gs2, comm)

        gs2_go = pygsti.gaugeopt_to_target(gs2, gs1, {'gates': 1.0, 'spam': 1.0})
        print("Frobenius distance %d (rank %d) = " % (i,comm.Get_rank()), gs1.frobeniusdist(gs2_go))
        if gs1.frobeniusdist(gs2_go) >= 1e-5:
            print("DIFF (%d) = " % comm.Get_rank(), gs1.strdiff(gs2_go))
        assert(gs1.frobeniusdist(gs2_go) < 1e-5)
    return

@mpitest(4)
def test_MPI_mlgst_forcefn(comm):
    fiducials = std.fiducials
    target_model = std.target_model()
    lgstStrings = pygsti.construction.list_lgst_circuits(fiducials, fiducials,
                                                             list(target_model.operations.keys()))
    #Create dataset on root proc
    if comm is None or comm.Get_rank() == 0:
        datagen_gateset = target_model.depolarize(op_noise=0.01, spam_noise=0.01)
        ds = pygsti.construction.generate_fake_data(datagen_gateset, lgstStrings,
                                                    nSamples=10000, sampleError='binomial', seed=100)
        ds = comm.bcast(ds, root=0)
    else:
        ds = comm.bcast(None, root=0)


    mdl_lgst = pygsti.do_lgst(ds, fiducials, fiducials, target_model, svdTruncateTo=4, verbosity=0)
    mdl_lgst_go = pygsti.gaugeopt_to_target(mdl_lgst,target_model, {'spam':1.0, 'gates': 1.0})

    forcingfn_grad = np.ones((1,mdl_lgst_go.num_params()), 'd')
    mdl_lsgst_chk_opts3 = pygsti.algorithms.core._do_mlgst_base(
        ds, mdl_lgst_go, lgstStrings, verbosity=3,
        minProbClip=1e-4, probClipInterval=(-1e2,1e2),
        forcefn_grad=forcingfn_grad, comm=comm)



@mpitest(4)
def test_MPI_derivcols(comm):
    #Create dataset for serial and parallel runs
    ds,lsgstStrings = create_fake_dataset(comm)

    #Individual processors
    my1ProcResults = runOneQubit("chi2",ds,lsgstStrings)

    #Using all processors
    myManyProcResults = runOneQubit("chi2",ds,lsgstStrings,comm,"deriv")

    for i,(gs1,gs2) in enumerate(zip(my1ProcResults,myManyProcResults)):
        assertGatesetsInSync(gs1, comm)
        assertGatesetsInSync(gs2, comm)

        gs2_go = pygsti.gaugeopt_to_target(gs2, gs1, {'gates': 1.0, 'spam': 1.0})
        print("Frobenius distance %d (rank %d) = " % (i,comm.Get_rank()), gs1.frobeniusdist(gs2_go))
        if gs1.frobeniusdist(gs2_go) >= 1e-5:
            print("DIFF (%d) = " % comm.Get_rank(), gs1.strdiff(gs2_go))
        assert(gs1.frobeniusdist(gs2_go) < 1e-5)
    return

@mpitest(4)
def test_run1Q_end2end(comm):
    from pygsti.modelpacks.legacy import std1Q_XYI
    target_model = std1Q_XYI.target_model()
    fiducials = std1Q_XYI.fiducials
    germs = std1Q_XYI.germs
    maxLengths = [1,2,4]

    mdl_datagen = target_model.depolarize(op_noise=0.1, spam_noise=0.001)
    listOfExperiments = pygsti.construction.make_lsgst_experiment_list(
        list(target_model.operations.keys()), fiducials, fiducials, germs, maxLengths)
    ds = pygsti.construction.generate_fake_data(mdl_datagen, listOfExperiments,
                                                nSamples=1000,
                                                sampleError="binomial",
                                                seed=1234, comm=comm)
    if comm.Get_rank() == 0:
        pickle.dump(ds, open("mpi_dataset.pkl","wb"))
    comm.barrier() #to make sure dataset file is written

    #test with pkl file - should only read in on rank0 then broadcast
    results = pygsti.do_long_sequence_gst("mpi_dataset.pkl", target_model, fiducials, fiducials,
                                          germs, [1], comm=comm)

    #test with dataset object
    results = pygsti.do_long_sequence_gst(ds, target_model, fiducials, fiducials,
                                          germs, maxLengths, comm=comm)

    #Use dummy duplicate of results to trigger MPI data-comparison processing:
    pygsti.report.create_standard_report({"one": results, "two": results}, "mpi_test_report",
                                         "MPI test report", confidenceLevel=95,
                                         verbosity=2, comm=comm)


@mpitest(4)
def test_MPI_germsel(comm):
    if comm is None or comm.Get_rank() == 0:
        gatesetNeighborhood = pygsti.alg.randomize_model_list(
            [std.target_model()], randomizationStrength=1e-3,
            numCopies=3, seed=2018)
        comm.bcast(gatesetNeighborhood, root=0)
    else:
        gatesetNeighborhood = comm.bcast(None, root=0)

    max_length   = 6
    gates        = std.target_model().operations.keys()
    superGermSet = pygsti.construction.list_all_circuits_without_powers_and_cycles(gates, max_length)

    #germs = pygsti.alg.build_up_breadth(gatesetNeighborhood, superGermSet,
    #                                    randomize=False, seed=2018, scoreFunc='all',
    #                                    threshold=1e6, verbosity=1, opPenalty=1.0,
    #                                    memLimit=3*(1024**3), comm=comm)

    germs_lowmem = pygsti.alg.build_up_breadth(gatesetNeighborhood, superGermSet,
                                               randomize=False, seed=2018, scoreFunc='all',
                                               threshold=1e6, verbosity=1, opPenalty=1.0,
                                               memLimit=3*(1024**2), comm=comm) # force "single-Jac" mode

@mpitest(4)
def test_MPI_profiler(comm):
    mem = profiler._get_root_mem_usage(comm)
    mem = profiler._get_max_mem_usage(comm)

    start_time = time.time()
    p = profiler.Profiler(comm, default_print_memcheck=True)
    p.add_time("My Name", start_time, prefix=1)
    p.add_count("My Count", inc=1, prefix=1)
    p.add_count("My Count", inc=2, prefix=1)
    p.mem_check("My Memcheck", prefix=1)
    p.mem_check("My Memcheck", prefix=1)
    p.print_mem("My Memcheck just to print")
    p.print_mem("My Memcheck just to print", show_minmax=True)
    p.print_msg("My Message")
    p.print_msg("My Message", all_ranks=True)

    s = p.format_times(sortBy="name")
    s = p.format_times(sortBy="time")
    #with self.assertRaises(ValueError):
    #    p.format_times(sortBy="foobar")

    s = p.format_counts(sortBy="name")
    s = p.format_counts(sortBy="count")
    #with self.assertRaises(ValueError):
    #    p.format_counts(sortBy="foobar")

    s = p.format_memory(sortBy="name")
    s = p.format_memory(sortBy="usage")
    #with self.assertRaises(ValueError):
    #    p.format_memory(sortBy="foobar")
    #with self.assertRaises(NotImplementedError):
    #    p.format_memory(sortBy="timestamp")


@mpitest(4)
def test_MPI_tools(comm):
    from pygsti.tools import mpitools as mpit

    indices = list(range(10))
    nprocs = comm.Get_size()
    rank = comm.Get_rank()

    # ------------------ distribute_indices_base --------------------------------

    #case of procs < nIndices
    loc_indices, owners = mpit.distribute_indices_base(indices, nprocs, rank, allow_split_comm=True)
    if nprocs == 4: #should always be the case
        if rank == 0: assert(loc_indices == [0,1,2])
        if rank == 1: assert(loc_indices == [3,4,5])
        if rank == 2: assert(loc_indices == [6,7])
        if rank == 3: assert(loc_indices == [8,9])
        assert(owners == {0: 0, 1: 0, 2: 0,
                          3: 1, 4: 1, 5: 1,
                          6: 2, 7: 2,
                          8: 3, 9: 3}) # index : owner-rank

    #case of nIndices > procs, allow_split_comm = True, no extras
    indices = list(range(2))
    loc_indices, owners = mpit.distribute_indices_base(indices, nprocs, rank, allow_split_comm=True)
    if nprocs == 4: #should always be the case
        if rank == 0: assert(loc_indices == [0])
        if rank == 1: assert(loc_indices == [0])
        if rank == 2: assert(loc_indices == [1])
        if rank == 3: assert(loc_indices == [1])
        assert(owners == {0: 0, 1: 2}) # only gives *first* owner

    #case of nIndices > procs, allow_split_comm = True, 1 extra proc
    indices = list(range(3))
    loc_indices, owners = mpit.distribute_indices_base(indices, nprocs, rank, allow_split_comm=True)
    if nprocs == 4: #should always be the case
        if rank == 0: assert(loc_indices == [0])
        if rank == 1: assert(loc_indices == [0])
        if rank == 2: assert(loc_indices == [1])
        if rank == 3: assert(loc_indices == [2])
        assert(owners == {0: 0, 1: 2, 2: 3}) # only gives *first* owner

    #case of nIndices > procs, allow_split_comm = False
    indices = list(range(3))
    loc_indices, owners = mpit.distribute_indices_base(indices, nprocs, rank, allow_split_comm=False)
    if nprocs == 4: #should always be the case
        if rank == 0: assert(loc_indices == [0])
        if rank == 1: assert(loc_indices == [1])
        if rank == 2: assert(loc_indices == [2])
        if rank == 3: assert(loc_indices == [])  #only one proc per index
        assert(owners == {0: 0, 1: 1, 2: 2}) # only gives *first* owner

    #Boundary case of no indices
    loc_indices, owners = mpit.distribute_indices_base([], nprocs, rank, allow_split_comm=False)
    assert(loc_indices == [])
    assert(owners == {})


    # ------------------ slice_up_slice --------------------------------
    slices = mpit.slice_up_slice( slice(0,4), num_slices=2)
    assert(slices[0] == slice(0,2))
    assert(slices[1] == slice(2,4))
    slices = mpit.slice_up_slice( slice(None,None), num_slices=2)
    assert(slices[0] == slice(0,0))
    assert(slices[1] == slice(0,0))


    # ------------------ distribute & gather slices--------------------------------
    master = np.arange(100)

    def test(slc, allow_split_comm=True, maxbuf=None):
        slices, loc_slice, owners, loc_comm = mpit.distribute_slice(slc,comm,allow_split_comm)
        my_array = np.zeros(100,'d')
        my_array[loc_slice] = master[loc_slice] # ~ computation (just copy from "master")
        mpit.gather_slices(slices, owners, my_array,
                           arToFillInds=[], axes=0, comm=comm,
                           max_buffer_size=maxbuf)
        assert(np.linalg.norm(my_array[slc] - master[slc]) < 1e-6)

        my_array2 = np.zeros(100,'d')
        my_array2[loc_slice] = master[loc_slice] # ~ computation (just copy from "master")
        mpit.gather_slices_by_owner([loc_slice], my_array2, arToFillInds=[],
                                    axes=0, comm=comm, max_buffer_size=maxbuf)
        assert(np.linalg.norm(my_array2[slc] - master[slc]) < 1e-6)

        indices = [ pygsti.tools.slicetools.as_array(s) for s in slices ]
        loc_indices = pygsti.tools.slicetools.as_array(loc_slice)
        my_array3 = np.zeros(100,'d')
        my_array3[loc_indices] = master[loc_indices] # ~ computation (just copy from "master")
        mpit.gather_indices(indices, owners, my_array3, arToFillInds=[], axes=0,
                            comm=comm, max_buffer_size=maxbuf)
        assert(np.linalg.norm(my_array3[slc] - master[slc]) < 1e-6)

    test(slice(0,8)) #more indices than processors
    test(slice(0,8),False) #more indices than processors w/out split comm
    test(slice(0,3)) #fewer indices than processors
    test(slice(0,3),False) #fewer indices than processors w/out split comm
    test(slice(0,10),maxbuf=12) #with max-buffer
    test(slice(0,10),maxbuf=0) #with max-buffer that cannot be attained - should WARN

    master2D = np.arange(100).reshape((10,10))

    def test2D(slc1,slc2, allow_split_comm=True, maxbuf=None):
        slices1, loc_slice1, owners1, loc_comm1 = mpit.distribute_slice(slc1,comm,allow_split_comm)
        slices2, loc_slice2, owners2, loc_comm2 = mpit.distribute_slice(slc2,loc_comm1,allow_split_comm)

        my_array = np.zeros((10,10),'d')
        my_array[loc_slice1,loc_slice2] = master2D[loc_slice1,loc_slice2].copy() # ~ computation (just copy from "master")

    #Can't do this until distribute_slice gets upgraded to work with multiple dims...
    #     mpit.gather_slices(slices, owners, my_array,
    #                        arToFillInds=[], axes=0, comm=comm,
    #                        max_buffer_size=maxbuf)
    #     assert(np.linalg.norm(my_array[slc] - master2D[slc]) < 1e-6)

        my_array2 = np.zeros((10,10),'d')
        my_array2[loc_slice1,loc_slice2] = master2D[loc_slice1,loc_slice2].copy() # ~ computation (just copy from "master")
        mpit.gather_slices_by_owner([(loc_slice1,loc_slice2)], my_array2, arToFillInds=[],
                                    axes=(0,1), comm=comm, max_buffer_size=maxbuf)
        #print("Rank %d: locslc1 = %s, locslc2 = %s, loc_comm1_size=%d" % (rank, str(loc_slice1),str(loc_slice2),
        #                                                                  loc_comm1.Get_size() if loc_comm1 else -1))
        assert(np.linalg.norm(my_array2[slc1,slc2] - master2D[slc1,slc2]) < 1e-6)


    test2D(slice(0,8),slice(0,4)) #more indices than processors
    test2D(slice(0,3),slice(0,3)) #fewer indices than processors
    test2D(slice(0,3),slice(0,3),False) #fewer indices than processors w/split comm
    test2D(slice(0,10), slice(0,5), maxbuf=20) #with max-buffer

    #trivial case with comm = None => nothing to do
    mpit.gather_slices(None, None, master, arToFillInds=[], axes=0, comm=None)
    mpit.gather_slices_by_owner(slice(0,100), master, arToFillInds=[], axes=0, comm=None)

    # ------------------ parallel apply --------------------------------

    #Doesn't work in python3 b/c comm.split hands in distribute_indices...
    #def f(x):
    #    return x + "!"
    #results = mpit.parallel_apply( f,["Hi","there"], comm)
    #assert(results == ["Hi!","there!"])

    def f(i):
        return i + 10
    results = mpit.parallel_apply( f,[1,2], comm)
    assert(results == [11,12])

    # convenience method to avoid importing mpi4py at the top level
    c = mpit.get_comm()


@mpitest(4)
def test_MPI_printer(comm):
    #Test output of each rank to separate file:
    pygsti.obj.VerbosityPrinter._commPath = "./"
    pygsti.obj.VerbosityPrinter._commFileName = "mpi_test_output"
    printer = pygsti.obj.VerbosityPrinter(verbosity=1, comm=comm)
    printer.log("HELLO!")
    pygsti.obj.VerbosityPrinter._commPath = "./"
    pygsti.obj.VerbosityPrinter._commFileName = "mpi_test_output"


if __name__ == "__main__":
    unittest.main(verbosity=2)
