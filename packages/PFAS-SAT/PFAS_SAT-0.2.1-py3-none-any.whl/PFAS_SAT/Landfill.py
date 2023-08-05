# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 21:04:20 2020

@author: msmsa
"""
import pandas as pd
from .Flow import Flow
from .SubProcesses import mix, landfil_sorption, stabilization
from .LandfillInput import LandfillInput
from .ProcessModel import ProcessModel


class Landfill(ProcessModel):
    """
    Assumptions:
        1. No volatilization or degradation of PFAS.
        2. Steady state.
        3. PFAS-containing waste and bulk MSW are well mixed.
        4. Annual time horizon.
    """
    ProductsType = ['LFLeachate']

    def __init__(self, input_data_path=None, CommonDataObjct=None, InventoryObject=None, Name=None):
        super().__init__(CommonDataObjct, InventoryObject)
        self.InputData = LandfillInput(input_data_path)
        self.Name = Name if Name else 'Landfill'

    def calc(self, Inc_flow):
        # Initialize the Incoming flow
        self.Inc_flow = Inc_flow

        # Calculating the mass of MSW in Landfill
        MSW_Mass = self.Inc_flow.mass / self.InputData.LFMSW['frac_of_msw']['amount'] - self.Inc_flow.mass

        # Initializing the MSW in Landfill
        self.MSW_flow = Flow()
        kwargs = {}
        kwargs['mass_flow'] = MSW_Mass
        kwargs['ts_cont'] = self.InputData.LFMSW['ts_cont']['amount']
        kwargs['C_cont'] = self.InputData.LFMSW['C_cont']['amount']
        kwargs['bulk_dens'] = self.InputData.LFMSW['bulk_dens']['amount']
        self.MSW_flow.set_flow(**kwargs)

        # Mixing the Incoming flow with MSW in landfill
        self.Mixture = mix(self.Inc_flow, self.MSW_flow)

        # PFAS loss to volatilization
        self.Volatilized = Flow()
        self.Volatilized.PFAS = self.Mixture.PFAS * self.InputData.Volatilization['frac_vol_loss']['amount']
        self.Mixture.PFAS = self.Mixture.PFAS - self.Volatilized.PFAS

        # Calculating the volume of percipitation (includes RunOff and Leachate)
        area = self.Mixture.mass / 1000 / self.InputData.LF['lf_ton_area']['amount']
        LF_Leachate_Vol = area * self.InputData.Water_Blnc['leach_gpad']['amount'] * 365.25 * self.InputData.Water_Blnc['is_leach_col']['amount'] * \
            self.InputData.Water_Blnc['frac_leach_col']['amount'] / 264.172 * 1000  # L/yr
        Leachate_Vol = (area * self.InputData.Water_Blnc['leach_gpad']['amount'] * (1-self.InputData.Water_Blnc['is_leach_col']['amount']) +
                        area * self.InputData.Water_Blnc['leach_gpad']['amount'] * self.InputData.Water_Blnc['is_leach_col']['amount'] *
                        (1 - self.InputData.Water_Blnc['frac_leach_col']['amount'])) * 365.25 / 264.172 * 1000  # L/yr

        # Calculating the PFAS in water and soil partitions
        if 'FlowType' in self.Inc_flow.__dict__:
            if self.Inc_flow.FlowType == 'SpentGAC':
                self.LF_storage, self.LF_Leachate, self.Leachate = stabilization(mixture=self.Mixture,
                                                                                 LogPartCoef_data=self.InputData.LogPartCoef,
                                                                                 Additive_LogPartCoef=self.InputData.LogPartCoef_GAC,
                                                                                 Additive_mass=self.Inc_flow.ts,
                                                                                 Leachate_vol=Leachate_Vol,
                                                                                 Runoff_vol=Leachate_Vol)
            elif self.Inc_flow.FlowType == 'StabilizedSoil':
                self.LF_storage, self.LF_Leachate, self.Leachate = stabilization(mixture=self.Mixture,
                                                                                 LogPartCoef_data=self.InputData.LogPartCoef,
                                                                                 Additive_LogPartCoef=self.Inc_flow.AddLogPartCoef,
                                                                                 Additive_mass=self.Inc_flow.Additive_mass,
                                                                                 Leachate_vol=Leachate_Vol,
                                                                                 Runoff_vol=Leachate_Vol)
            elif self.Inc_flow.FlowType == 'SpentIER':
                self.LF_storage, self.LF_Leachate, self.Leachate = stabilization(mixture=self.Mixture,
                                                                                 LogPartCoef_data=self.InputData.LogPartCoef,
                                                                                 Additive_LogPartCoef=self.InputData.LogPartCoef_SpentIER,
                                                                                 Additive_mass=self.Inc_flow.ts,
                                                                                 Leachate_vol=Leachate_Vol,
                                                                                 Runoff_vol=Leachate_Vol)
            else:
                self.LF_storage, self.LF_Leachate, self.Leachate = landfil_sorption(self.Mixture, self.InputData.LogPartCoef,
                                                                                    LF_Leachate_Vol, Leachate_Vol)
        else:
            self.LF_storage, self.LF_Leachate, self.Leachate = landfil_sorption(self.Mixture, self.InputData.LogPartCoef,
                                                                                LF_Leachate_Vol, Leachate_Vol)

        # add to Inventory
        self.Inventory.add('Volatilized', self.Name, 'Air', self.Volatilized)
        self.Inventory.add('Leachate', self.Name, 'Water', self.Leachate)
        self.Inventory.add('Storage', self.Name, 'Stored', self.LF_storage)

    def products(self):
        Products = {}
        Products['LFLeachate'] = self.LF_Leachate
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
            report['Collected Leachate'] = self.LF_Leachate.PFAS
            report['Fugitive Leachate'] = self.Leachate.PFAS
            report['Remaining in Landfill'] = self.LF_storage.PFAS
        else:
            report['Volatilized'] = round(self.Volatilized.PFAS / self.Inc_flow.PFAS * 100, 4)
            report['Collected Leachate'] = round(self.LF_Leachate.PFAS / self.Inc_flow.PFAS * 100, 4)
            report['Fugitive Leachate'] = round(self.Leachate.PFAS / self.Inc_flow.PFAS * 100, 4)
            report['Remaining in Landfill'] = round(self.LF_storage.PFAS / self.Inc_flow.PFAS * 100, 4)
        return(report)
