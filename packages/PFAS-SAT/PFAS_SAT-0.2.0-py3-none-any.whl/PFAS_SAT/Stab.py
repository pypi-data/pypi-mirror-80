# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 18:18:05 2020

@author: msmsa
"""
import pandas as pd
from .Flow import Flow
from .SubProcesses import mix, stabilization
from .StabInput import StabInput
from .ProcessModel import ProcessModel


class Stab(ProcessModel):
    """
    Assumptions:
        1. No volatilization or degradation of PFAS.
        2. Steady state.
        3. Soil and amendments are well mixed.
        4. Annual time horizon.
    """
    ProductsType = ['StabilizedSoil']

    def __init__(self, input_data_path=None, CommonDataObjct=None, InventoryObject=None, Name=None):
        super().__init__(CommonDataObjct, InventoryObject)
        self.InputData = StabInput(input_data_path)
        self.Name = Name if Name else 'Stabilization'

    def calc(self, Inc_flow):
        # Initialize the Incoming flow
        self.Inc_flow = Inc_flow

        # PFAS loss to volatilization
        self.Volatilized = Flow()
        self.Volatilized.PFAS = self.Inc_flow.PFAS * self.InputData.Volatilization['frac_vol_loss']['amount']
        self.Inc_flow.PFAS = self.Inc_flow.PFAS - self.Volatilized.PFAS

        # Calculating the mass of additive mixed with the Incoming flow
        additive_mass_mix = self.InputData.Stabil['add_mass_ratio']['amount'] * self.Inc_flow.mass

        # Initializing the additive flow
        self.Add_flow = Flow()
        kwargs = {}
        for key, data in self.InputData.AddProp.items():
            kwargs[key] = data['amount']
        kwargs['mass_flow'] = additive_mass_mix

        kwargs['C_cont'] = 0

        self.Add_flow.set_flow(**kwargs)

        # Mixing the Incoming flow with additive
        self.Mixed_flow = mix(self.Inc_flow, self.Add_flow)

        # Calculating the volume of Precipitation (includes RunOff and Leachate)
        Precip_Vol = self.Inc_flow.mass / self.InputData.Stabil['bulk_dens']['amount'] / self.InputData.Stabil['depth_mix']['amount'] *\
            self.InputData.Precip['ann_precip']['amount'] * 1000  # L/yr

        total = self.InputData.Precip['frac_ET']['amount']+self.InputData.Precip['frac_runoff']['amount']
        if total > 1:
            self.InputData.Precip['frac_ET']['amount'] /= total
            self.InputData.Precip['frac_runoff']['amount'] /= total
        ET_Vol = Precip_Vol * self.InputData.Precip['frac_ET']['amount']  # L/yr
        RunOff_Vol = Precip_Vol * self.InputData.Precip['frac_runoff']['amount']  # L/yr
        Leachate_Vol = Precip_Vol - ET_Vol - RunOff_Vol  # L/yr

        # Calculating the PFAS in water and soil partitions
        if self.InputData.Stabil['is_stay_inplace']['amount']:
            self.Stabilized, self.Leachate, self.RunOff = stabilization(self.Mixed_flow, self.InputData.SoilLogPartCoef,
                                                                        self.InputData.AddLogPartCoef,
                                                                        additive_mass_mix, Leachate_Vol, RunOff_Vol)
        else:
            self.Stabilized, self.Leachate, self.RunOff = stabilization(self.Mixed_flow, self.InputData.SoilLogPartCoef,
                                                                        self.InputData.AddLogPartCoef,
                                                                        additive_mass_mix, 0, 0)

        # FlowType, Additive_mass and Additive_LiqSolCoef will be used in landfill model.
        self.Stabilized.set_FlowType('StabilizedSoil')
        self.Stabilized.Additive_mass = additive_mass_mix
        self.Stabilized.AddLogPartCoef = self.InputData.AddLogPartCoef

        # add to Inventory
        self.Inventory.add('Volatilized', self.Name, 'Air', self.Volatilized)
        self.Inventory.add('Leachate', self.Name, 'Water', self.Leachate)
        self.Inventory.add('RunOff', self.Name, 'Water', self.RunOff)
        if self.InputData.Stabil['is_stay_inplace']['amount']:
            self.Inventory.add('Stabilized', self.Name, 'Soil', self.Stabilized)
        else:
            self.Inventory.add('Stabilized', self.Name, 'Soil', Flow(ZeroFlow=True))

    def products(self):
        Products = {}
        if self.InputData.Stabil['is_stay_inplace']['amount']:
            Products['StabilizedSoil'] = Flow(ZeroFlow=True)
        else:
            Products['StabilizedSoil'] = self.Stabilized
        return(Products)

    def setup_MC(self, seed=None):
        self.InputData.setup_MC(seed)

    def MC_Next(self):
        input_list = self.InputData.gen_MC()
        return(input_list)

    def report(self, normalized=False):
        report = pd.DataFrame(index=self.Inc_flow._PFAS_Index)
        if not normalized:
            report['Volatilized'] = self.Volatilized.PFAS
            report['Remaining in Soil'] = self.Stabilized.PFAS
            report['Leachate'] = self.Leachate.PFAS
            report['RunOff'] = self.RunOff.PFAS
        else:
            report['Volatilized'] = round(self.Volatilized.PFAS / self.Inc_flow.PFAS * 100, 2)
            report['Remaining in Soil'] = round(self.Stabilized.PFAS / self.Inc_flow.PFAS * 100, 2)
            report['Leachate'] = round(self.Leachate.PFAS / self.Inc_flow.PFAS * 100, 2)
            report['RunOff'] = round(self.RunOff.PFAS / self.Inc_flow.PFAS * 100, 2)
        return(report)
