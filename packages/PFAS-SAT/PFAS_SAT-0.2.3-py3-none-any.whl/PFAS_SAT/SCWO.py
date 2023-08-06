# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 10:44:45 2020

@author: msmsa
"""
import pandas as pd
from .Flow import Flow
from .SCWOInput import SCWOInput
from .ProcessModel import ProcessModel


class SCWO(ProcessModel):
    """
**************************************
Supercritical water oxidation (SCWO)
**************************************

SCWO systems use supercritical water (i.e., water above 373.946 C and 22.064 MPa) to facilitate the oxidation
of PFAS or other hazardous substances in aqueous streams. SCWO systems are already in operation in Japan and
Korea to manage PCBs and halogenated wastes, and the Chematur Engineering facility in the UK uses SCWO to recover
metals from catalysts. Research into the use the SCWO for PFAS destruction is ongoing, and there are several different
systems being developed. SCWO produces steam, water, and slurry outputs. The mineralized fluoride remains in the slurry.
The destruction of PFAS is modeled using a destruction and removal efficiency (DRE). Any PFAS that is not destroyed or
removed remains in the water. There may also be small amounts of PFAS volatilized in the steam and remaining in the slurry.
The process model estimates the fraction of incoming water that goes to each stream, and the PFAS remaining in each.

=============================
Assumptions and Limitations:
=============================

#. It assumes that the destruction and removal efficiency remains constant for each PFAS.
#. By default, the model assumes that all the remaining PFAS is in the water stream. However,
   this is a user input, and the user can send PFAS to the steam or slurry streams as well.
    """
    ProductsType = ['SCWOSteam', 'SCWOSlurry']

    def __init__(self, input_data_path=None, CommonDataObjct=None, InventoryObject=None, Name=None):
        super().__init__(CommonDataObjct, InventoryObject)
        self.InputData = SCWOInput(input_data_path)
        self.Name = Name if Name else 'SCWO'

    def calc(self, Inc_flow):
        # Initialize the Incoming flow
        self.Inc_flow = Inc_flow

        # PFAS Balance
        self.Steam = Flow()
        self.Slurry = Flow()
        self.Effluent = Flow()
        self.Destroyed = Flow()

        for i in self.Inc_flow._PFAS_Index:
            self.Effluent.PFAS[i] = self.Inc_flow.PFAS[i] * (1 - self.InputData.DRE[i]['amount'])
            self.Slurry.PFAS[i] = self.Inc_flow.PFAS[i] * self.InputData.DRE[i]['amount'] * self.InputData.SCWO['frac_PFAS_to_slurry']['amount']
            self.Steam.PFAS[i] = self.Inc_flow.PFAS[i] * self.InputData.DRE[i]['amount'] * self.InputData.SCWO['frac_PFAS_to_steam']['amount']
        self.Destroyed.PFAS = self.Inc_flow.PFAS - self.Effluent.PFAS - self.Slurry.PFAS - self.Steam.PFAS

        # Volume balance
        self.Slurry.vol = self.Inc_flow.vol * self.InputData.SCWO['frac_water_to_slurry']['amount']
        self.Steam.vol = self.Inc_flow.vol * self.InputData.SCWO['frac_water_to_steam']['amount']
        self.Effluent.vol = self.Inc_flow.vol - self.Slurry.vol - self.Steam.vol

        # add to Inventory
        self.Inventory.add('Effluent', self.Name, 'Water', self.Effluent)
        self.Inventory.add('Destroyed', self.Name, 'Destroyed', self.Destroyed)

    def products(self):
        Products = {}
        Products['SCWOSteam'] = self.Steam
        Products['SCWOSlurry'] = self.Slurry
        return(Products)

    def setup_MC(self, seed=None):
        self.InputData.setup_MC(seed)

    def MC_Next(self):
        input_list = self.InputData.gen_MC()
        return(input_list)

    def report(self, normalized=False):
        report = pd.DataFrame(index=self.Inc_flow._PFAS_Index)
        if not normalized:
            report['Effluent'] = self.Effluent.PFAS
            report['Slurry'] = self.Slurry.PFAS
            report['Steam'] = self.Steam.PFAS
            report['Destroyed'] = self.Destroyed.PFAS
        else:
            report['Effluent'] = round(self.Effluent.PFAS / self.Inc_flow.PFAS * 100, 2)
            report['Slurry'] = round(self.Slurry.PFAS / self.Inc_flow.PFAS * 100, 2)
            report['Steam'] = round(self.Steam.PFAS / self.Inc_flow.PFAS * 100, 2)
            report['Destroyed'] = round(self.Destroyed.PFAS / self.Inc_flow.PFAS * 100, 2)
        return(report)
