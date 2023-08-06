# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 21:16:00 2020

@author: msmsa
"""
import PFAS_SAT as ps


def test_project():
    InventoryObject = ps.Inventory()

    CommonDataObjct = ps.CommonData()

    InputFlow = ps.IncomFlow()

    InputFlow.set_flow('FoodWaste', 1000)

    demo = ps.Project(InventoryObject, CommonDataObjct, ProcessModels=None)
    ProcessSet = demo.get_process_set(InputFlow.Inc_flow)
    demo.set_process_set(ProcessSet[0])
    FlowParams = demo.get_flow_params()
    demo.set_flow_params(FlowParams)
    demo.setup_network()
    demo.Inventory.Inv

    demo.setup_MC(InputFlow)
    demo.MC_Next()
    demo.Inventory.Inv

    AA = demo.MC_Run(100)

    demo.Result_to_DF(AA)
