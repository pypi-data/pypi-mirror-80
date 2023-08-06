# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 10:44:45 2020

@author: msmsa
"""
import pandas as pd
from .Flow import Flow
from .ThermalTreatmentInput import ThermalTreatmentInput
from .ProcessModel import ProcessModel


class ThermalTreatment(ProcessModel):
    """
***********************
Thermal Treatment
***********************

Combustion systems include mass burn incinerators for MSW, hazardous solid waste, and medical waste, as well as cement kilns.
The combustion process model in the SAT framework was designed so that by changing default parameters, a variety of conventional
and emerging thermal treatment processes can be represented. In addition to MSW incinerators, other potential thermal processes
include gasification/pyrolysis systems, and thermomechanochemical systems, which may include mechanical and chemical processing
prior to combustion.

To begin, the incoming materials are partially or fully combusted. During combustion, a fraction of the PFAS may be volatilized
and/or destroyed, but data on destruction and release of volatilized PFAS and/or products of incomplete combustion are limited.
The volatilized compounds may be transformed into chlorofluorocarbons, which deplete stratospheric ozone and are potent greenhouse
gases. The incineration process produces combustion residuals that may include bottom ash, fly ash, and air pollution control (APC)
residues. The mass of PFAS flows are modeled using a destruction and removal efficiency (DRE), and fraction of the DRE that remains
in the residual. Based on these inputs, the model calculates the PFAS destroyed, released to the air and remaining in the ash. The
ash is then sent to landfill.

=============================
Assumptions and Limitations:
=============================

#. The model assumes a single DRE and fraction remaining on the residual for each material and type of PFAS. Data is relatively
   limited, but this can be readily updated as more data becomes available.
#. The model assumes there is a single ash stream with a common set of parameters.
#. The model assumes a single VS destruction efficiency, but this could vary by material.
#. The model does not consider transformations of PFAS.
    """
    ProductsType = ['CombustionResiduals']

    def __init__(self, input_data_path=None, CommonDataObjct=None, InventoryObject=None, Name=None):
        super().__init__(CommonDataObjct, InventoryObject)
        self.InputData = ThermalTreatmentInput(input_data_path)
        self.Name = Name if Name else 'Thermal Treatment'

    def calc(self, Inc_flow):
        # Initialize the Incoming flow
        self.Inc_flow = Inc_flow

        # PFAS Balance
        self.CombRes = Flow()
        self.Exhaust = Flow()
        self.Destructed = Flow()
        for i in self.Inc_flow._PFAS_Index:
            self.Exhaust.PFAS[i] = self.Inc_flow.PFAS[i] * (1 - self.InputData.DRE[i]['amount']) * (1 - self.InputData.Frac_to_res[i]['amount'])
            self.Destructed.PFAS[i] = self.Inc_flow.PFAS[i] * self.InputData.DRE[i]['amount']
            self.CombRes.PFAS[i] = self.Inc_flow.PFAS[i] - self.Destructed.PFAS[i] - self.Exhaust.PFAS[i]

        # Combustion Residual
        self.CombRes.ts = self.Inc_flow.VS * self.InputData.Comb_param['frac_vs_to_res']['amount'] + (self.Inc_flow.ts - self.Inc_flow.VS)
        self.CombRes.VS = self.Inc_flow.VS * self.InputData.Comb_param['frac_vs_to_res']['amount']
        self.CombRes.C = self.Inc_flow.C * self.InputData.Comb_param['frac_vs_to_res']['amount']
        self.CombRes.mass = self.CombRes.ts / self.InputData.Comb_param['res_ts_cont']['amount']
        self.CombRes.moist = self.CombRes.mass - self.CombRes.ts

        # add to Inventory
        self.Inventory.add('Exhaust', self.Name, 'Air', self.Exhaust)
        self.Inventory.add('Destructed', self.Name, 'Destroyed', self.Destructed)

    def products(self):
        Products = {}
        Products['CombustionResiduals'] = self.CombRes
        return(Products)

    def setup_MC(self, seed=None):
        self.InputData.setup_MC(seed)

    def MC_Next(self):
        input_list = self.InputData.gen_MC()
        return(input_list)

    def report(self, normalized=False):
        report = pd.DataFrame(index=self.Inc_flow._PFAS_Index)
        if not normalized:
            report['Air Emission'] = self.Exhaust.PFAS
            report['Combustion Residuals'] = self.CombRes.PFAS
            report['Destructed'] = self.Destructed.PFAS
        else:
            report['Air Emission'] = round(self.Exhaust.PFAS / self.Inc_flow.PFAS * 100, 2)
            report['Combustion Residuals'] = round(self.CombRes.PFAS / self.Inc_flow.PFAS * 100, 2)
            report['Destructed'] = round(self.Destructed.PFAS / self.Inc_flow.PFAS * 100, 2)
        return(report)
