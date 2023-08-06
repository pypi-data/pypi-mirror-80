""" Functions for interfacing pyGSTi with external devices, including IBM Q and Rigetti """
#***************************************************************************************************
# Copyright 2015, 2019 National Technology & Engineering Solutions of Sandia, LLC (NTESS).
# Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains certain rights
# in this software.
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
# in compliance with the License.  You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0 or in the LICENSE file in the root pyGSTi directory.
#***************************************************************************************************

from ..rb import analysis as _anl
from ...objects import oplessmodel as _oplessmodel
from ...objects import processorspec as _pspec
from ...objects import povm as _povm
from ...construction import modelconstruction as _mconst

from . import ibmq_melbourne
from . import ibmq_ourense
from . import ibmq_rueschlikon
from . import ibmq_tenerife
from . import ibmq_vigo
from . import ibmq_essex
from . import ibmq_burlington
from . import ibmq_london
from . import ibmq_yorktown
from . import rigetti_agave
from . import rigetti_aspen4
from . import rigetti_aspen6
from . import rigetti_aspen7

import numpy as _np


def get_device_specs(devname):
    return _get_dev_specs(devname)


def _get_dev_specs(devname):

    if devname == 'ibmq_melbourne' or devname == 'ibmq_16_melbourne': dev = ibmq_melbourne
    elif devname == 'ibmq_ourense': dev = ibmq_ourense
    elif devname == 'ibmq_rueschlikon': dev = ibmq_rueschlikon
    elif devname == 'ibmq_tenerife': dev = ibmq_tenerife
    elif devname == 'ibmq_vigo': dev = ibmq_vigo
    elif devname == 'ibmq_essex': dev = ibmq_essex
    elif devname == 'ibmq_burlington': dev = ibmq_burlington
    elif devname == 'ibmq_london': dev = ibmq_london
    elif devname == 'ibmq_yorktown' or devname == 'ibmqx2': dev = ibmq_yorktown
    elif devname == 'rigetti_agave': dev = rigetti_agave
    elif devname == 'rigetti_aspen4': dev = rigetti_aspen4
    elif devname == 'rigetti_aspen6': dev = rigetti_aspen6
    elif devname == 'rigetti_aspen7': dev = rigetti_aspen7
    else:
        raise ValueError("This device name is not known!")

    return dev


def get_edgelist(device):

    specs = _get_dev_specs(device)

    return specs.edgelist


def create_processor_spec(device, oneQgates, qubitsubset=None, removeedges=[],
                          construct_clifford_compilations={'paulieq': ('1Qcliffords',),
                                                           'absolute': ('paulis', '1Qcliffords')},
                          verbosity=0):
    """
    todo

    """
    dev = _get_dev_specs(device)

    if qubitsubset is not None:
        qubits = qubitsubset
        assert(set(qubitsubset).issubset(set(dev.qubits)))
    else:
        qubits = dev.qubits.copy()

    total_qubits = len(qubits)
    twoQgate = dev.twoQgate
    gate_names = [twoQgate] + oneQgates

    edgelist = dev.edgelist.copy()

    if qubitsubset is not None:
        subset_edgelist = []
        for edge in edgelist:
            if edge[0] in qubits and edge[1] in qubits:
                subset_edgelist.append(edge)

        edgelist = subset_edgelist

    for edge in removeedges: del edgelist[edgelist.index(edge)]

    availability = {twoQgate: edgelist}
    #print(availability)
    pspec = _pspec.ProcessorSpec(total_qubits, gate_names, availability=availability,
                                 construct_clifford_compilations=construct_clifford_compilations,
                                 verbosity=verbosity, qubit_labels=qubits)

    return pspec


def create_error_rates_model(caldata, device, oneQgates, oneQgates_to_native={}, calformat=None,
                             model_type='TwirledLayers', idlename=None):
    """
    calformat: 'ibmq-v2018', 'ibmq-v2019', 'rigetti', 'native'.
    """

    specs = _get_dev_specs(device)
    twoQgate = specs.twoQgate
    if 'Gc0' in oneQgates:
        assert('Gi' not in oneQgates), "Cannot ascertain idle gate name!"
        idlename = 'Gc0'
    elif 'Gi' in oneQgates:
        assert('Gc0' not in oneQgates), "Cannot ascertain idle gate name!"
        idlename = 'Gi'
    else:
        if model_type == 'dict':
            pass
        else:
            raise ValueError("Must specify the idle gate!")

    assert(not ((calformat is None) and (device is None))), "Must specify `calformat` or `device`"
    if calformat is None:
        calformat = specs.spec_format

    def average_gate_infidelity_to_entanglement_infidelity(agi, numqubits):

        dep = _anl.r_to_p(agi, 2**numqubits, 'AGI')
        ent_inf = _anl.p_to_r(dep, 2**numqubits, 'EI')

        return ent_inf

    error_rates = {}
    error_rates['gates'] = {}
    error_rates['readout'] = {}

    if calformat == 'ibmq-v2018':

        assert(oneQgates_to_native == {}), \
            "There is only a single one-qubit gate error rate for this calibration data format!"
        # This goes through the multi-qubit gates and records their error rates
        for dct in caldata['multiQubitGates']:

            # Converts to our gate name convention.
            gatename = twoQgate + ':Q' + str(dct['qubits'][0]) + ':Q' + str(dct['qubits'][1])
            # Assumes that the error rate is an average gate infidelity (as stated in qiskit docs).
            agi = dct['gateError']['value']
            # Maps the AGI to an entanglement infidelity.
            error_rates['gates'][gatename] = average_gate_infidelity_to_entanglement_infidelity(agi, 2)

        # This goes through the 1-qubit gates and readouts and stores their error rates.
        for dct in caldata['qubits']:

            q = dct['name']
            agi = dct['gateError']['value']
            error_rates['gates'][q] = average_gate_infidelity_to_entanglement_infidelity(agi, 1)

            # This assumes that this error rate is the rate of bit-flips.
            error_rates['readout'][q] = dct['readoutError']['value']

        # Because the one-qubit gates are all set to the same error rate, we have an alias dict that maps each one-qubit
        # gate on each qubit to that qubits label (the error rates key in error_rates['gates'])
        alias_dict = {}
        for q in specs.qubits:
            alias_dict.update({oneQgate + ':' + q: q for oneQgate in oneQgates})

    elif calformat == 'ibmq-v2019':

        # These'll be the keys in the error model, with the pyGSTi gate names aliased to these keys. If unspecified,
        # we set the error rate of a gate to the 'u3' gate error rate.
        oneQgatekeys = []
        for oneQgate in oneQgates:
            try:
                nativekey = oneQgates_to_native[oneQgate]
            except:
                oneQgates_to_native[oneQgate] = 'u3'
                nativekey = 'u3'
            assert(nativekey in ('id', 'u1', 'u2', 'u3')
                   ), "{} is not a gate specified in the IBM Q calibration data".format(nativekey)
            if nativekey not in oneQgatekeys:
                oneQgatekeys.append(nativekey)

        alias_dict = {}
        for q in specs.qubits:
            alias_dict.update({oneQgate + ':' + q: oneQgates_to_native[oneQgate] + ':' + q for oneQgate in oneQgates})

        # Loop through all the gates, and record the error rates that we use in our error model.
        for gatecal in caldata['gates']:

            if gatecal['gate'] == 'cx':

                # The qubits the gate is on, in the IBM Q notation
                qubits = gatecal['qubits']
                # Converts to our gate name convention.
                gatename = twoQgate + ':Q' + str(qubits[0]) + ':Q' + str(qubits[1])
                # Assumes that the error rate is an average gate infidelity (as stated in qiskit docs).
                agi = gatecal['parameters'][0]['value']
                # Maps the AGI to an entanglement infidelity.
                error_rates['gates'][gatename] = average_gate_infidelity_to_entanglement_infidelity(agi, 2)

            if gatecal['gate'] in oneQgatekeys:

                # The qubits the gate is on, in the IBM Q notation
                qubits = gatecal['qubits']
                # Converts to pyGSTi-like gate name convention, but using the IBM Q name.
                gatename = gatecal['gate'] + ':Q' + str(qubits[0])
                # Assumes that the error rate is an average gate infidelity (as stated in qiskit docs).
                agi = gatecal['parameters'][0]['value']
                # Maps the AGI to an entanglement infidelity.
                error_rates['gates'][gatename] = average_gate_infidelity_to_entanglement_infidelity(agi, 1)

        # Record the readout error rates. Because we don't do any rescaling, this assumes that this error
        # rate is the rate of bit-flips.
        for q, qcal in enumerate(caldata['qubits']):

            for qcaldatum in qcal:
                if qcaldatum['name'] == 'readout_error':
                    error_rates['readout']['Q' + str(q)] = qcaldatum['value']

    elif calformat == 'rigetti':

        # This goes through the multi-qubit gates and records their error rates
        for qs, gatedata in caldata['2Q'].items():

            # The qubits the qubit is on.
            qslist = qs.split('-')
            # Converts to our gate name convention. Do both orderings of the qubits as symmetric and we
            # are not necessarily consistent with Rigetti's ordering in the cal dict.
            gatename1 = twoQgate + ':Q' + qslist[0] + ':Q' + qslist[1]
            gatename2 = twoQgate + ':Q' + qslist[1] + ':Q' + qslist[0]

            # We use the controlled-Z fidelity if available, and the Bell state fidelity otherwise.
            # Here we are assuming that this is an average gate fidelity (as stated in the pyQuil docs)
            if gatedata['fCZ'] is not None:
                agi = 1 - gatedata['fCZ']
            else:
                agi = 1 - gatedata['fBellState']
            # We map the infidelity to 0 if it is less than 0 (sometimes this occurs with Rigetti
            # calibration data).
            agi = max([0, agi])
            # Maps the AGI to an entanglement infidelity.
            error_rates['gates'][gatename1] = average_gate_infidelity_to_entanglement_infidelity(agi, 2)
            error_rates['gates'][gatename2] = average_gate_infidelity_to_entanglement_infidelity(agi, 2)

        for q, qdata in caldata['1Q'].items():

            qlabel = 'Q' + q
            # We are assuming that this is an average gate fidelity (as stated in the pyQuil docs).
            agi = 1 - qdata['f1QRB']
            # We map the infidelity to 0 if it is less than 0 (sometimes this occurs with Rigetti
            # calibration data).
            agi = max([0, agi])
            # Maps the AGI to an entanglement infidelity. Use the qlabel, ..... TODO
            error_rates['gates'][qlabel] = average_gate_infidelity_to_entanglement_infidelity(agi, 1)
            # Record the readout error rates. Because we don't do any rescaling (except forcing to be
            # non-negative) this assumes that this error rate is the rate of bit-flips.
            error_rates['readout'][qlabel] = 1 - min([1, qdata['fRO']])

        # Because the one-qubit gates are all set to the same error rate, we have an alias dict that maps each one-qubit
        # gate on each qubit to that qubits label (the error rates key in error_rates['gates'])
        alias_dict = {}
        for q in specs.qubits:
            alias_dict.update({oneQgate + ':' + q: q for oneQgate in oneQgates})

    elif calformat == 'native':
        error_rates = caldata['error_rates'].copy()
        alias_dict = caldata['alias_dict'].copy()

    else:
        raise ValueError("Calibration data format not understood!")

    nQubits = len(specs.qubits)
    if model_type == 'dict':
        model = {'error_rates': error_rates, 'alias_dict': alias_dict}

    elif model_type == 'TwirledLayers':
        model = _oplessmodel.TwirledLayersModel(error_rates, nQubits, state_space_labels=specs.qubits,
                                                alias_dict=alias_dict, idlename=idlename)
    elif model_type == 'TwirledGates':
        model = _oplessmodel.TwirledGatesModel(error_rates, nQubits, state_space_labels=specs.qubits,
                                               alias_dict=alias_dict, idlename=idlename)
    elif model_type == 'AnyErrorCausesFailure':
        model = _oplessmodel.AnyErrorCausesFailureModel(error_rates, nQubits, state_space_labels=specs.qubits,
                                                        alias_dict=alias_dict, idlename=idlename)
    elif model_type == 'AnyErrorCausesRandomOutput':
        model = _oplessmodel.AnyErrorCausesRandomOutputModel(error_rates, nQubits, state_space_labels=specs.qubits,
                                                             alias_dict=alias_dict, idlename=idlename)
    else:
        raise ValueError("Model type not understood!")

    return model


def create_local_depolarizing_model(caldata, device, oneQgates, oneQgates_to_native={}, calformat=None, qubits=None):
    """
    todo

    Note: this model is *** NOT *** suitable for optimization: it is not aware that it is a local depolarization
    with non-independent error rates model.
    """

    def get_local_depolarization_channel(rate, numQs):

        if numQs == 1:

            channel = _np.identity(4, float)
            channel[1, 1] = _anl.r_to_p(rate, 2, 'EI')
            channel[2, 2] = _anl.r_to_p(rate, 2, 'EI')
            channel[3, 3] = _anl.r_to_p(rate, 2, 'EI')

            return channel

        if numQs == 2:

            perQrate = 1 - _np.sqrt(1 - rate)
            channel = _np.identity(4, float)
            channel[1, 1] = _anl.r_to_p(perQrate, 2, 'EI')
            channel[2, 2] = _anl.r_to_p(perQrate, 2, 'EI')
            channel[3, 3] = _anl.r_to_p(perQrate, 2, 'EI')

            return _np.kron(channel, channel)

    def get_local_povm(rate):

        # Increase the error rate of X,Y,Z, as rate correpsonds to bit-flip rate.
        deprate = 3 * rate / 2
        p = _anl.r_to_p(deprate, 2, 'EI')
        povm = _povm.UnconstrainedPOVM({'0': [1 / _np.sqrt(2), 0, 0, p / _np.sqrt(2)],
                                        '1': [1 / _np.sqrt(2), 0, 0, -p / _np.sqrt(2)]
                                        })
        return povm

    tempdict = create_error_rates_model(caldata, device, oneQgates, oneQgates_to_native=oneQgates_to_native,
                                        calformat=calformat, model_type='dict')

    error_rates = tempdict['error_rates']
    alias_dict = tempdict['alias_dict']
    devspecs = get_device_specs(device)

    if qubits is None:
        qubits = devspecs.qubits
        edgelist = devspecs.edgelist
    else:
        edgelist = [edge for edge in devspecs.edgelist if set(edge).issubset(set(qubits))]

    print(qubits)
    print(edgelist)

    model = _mconst.build_localnoise_model(nQubits=len(qubits),
                                           qubit_labels=qubits,
                                           gate_names=[devspecs.twoQgate] + oneQgates,
                                           availability={devspecs.twoQgate: edgelist},
                                           parameterization='full', independent_gates=True)

    for lbl in model.operation_blks['gates'].keys():

        gatestr = str(lbl)

        if len(lbl.qubits) == 1:
            errormap = get_local_depolarization_channel(error_rates['gates'][alias_dict.get(gatestr, gatestr)], 1)
            model.operation_blks['gates'][lbl] = _np.dot(errormap, model.operation_blks['gates'][lbl])

        if len(lbl.qubits) == 2:
            errormap = get_local_depolarization_channel(error_rates['gates'][alias_dict.get(gatestr, gatestr)], 2)
            model.operation_blks['gates'][lbl] = _np.dot(errormap, model.operation_blks['gates'][lbl])

    povms = [get_local_povm(error_rates['readout'][q]) for q in model.qubit_labels]
    model.povm_blks['layers']['Mdefault'] = _povm.TensorProdPOVM(povms)

    return model
