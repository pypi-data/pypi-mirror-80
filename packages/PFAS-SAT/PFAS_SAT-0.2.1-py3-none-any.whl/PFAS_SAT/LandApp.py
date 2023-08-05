# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 11:51:33 2020

@author: msmsa
"""
import pandas as pd
from .Flow import Flow
from .SubProcesses import mix, soil_sorption
from .LandAppInput import LandAppInput
from .ProcessModel import ProcessModel


class LandApp(ProcessModel):
    """
    Assumptions:
        1. No volatilization or degradation of PFAS.
        2. Steady state.
        3. Soil and amendments are well mixed.
        4. Annual time horizon.
    """
    ProductsType = []

    def __init__(self, input_data_path=None, CommonDataObjct=None, InventoryObject=None, Name=None):
        super().__init__(CommonDataObjct, InventoryObject)
        self.InputData = LandAppInput(input_data_path)
        self.Name = Name if Name else 'Land Application'

    def calc(self, Inc_flow):
        # Initialize the Incoming flow
        self.Inc_flow = Inc_flow

        # Calculating the mass of soil mixed with the Incoming flow
        soil_mass_mix = self.InputData.LandApp['depth_mix']['amount'] * self.Inc_flow.ts \
            / self.InputData.LandApp['appl_dens']['amount'] * self.InputData.SoilProp['bulk_dens']['amount']

        # Initializing the Soil flow
        self.Soil_flow = Flow()
        kwargs = {}
        for key, data in self.InputData.SoilProp.items():
            kwargs[key] = data['amount']
        kwargs['mass_flow'] = soil_mass_mix
        self.Soil_flow.set_flow(**kwargs)

        # Mixing the Incoming flow with soil
        self.Mixed_flow = mix(self.Inc_flow, self.Soil_flow)

        # PFAS loss to volatilization
        self.Volatilized = Flow()
        self.Volatilized.PFAS = self.Mixed_flow.PFAS * self.InputData.Volatilization['frac_vol_loss']['amount']
        self.Mixed_flow.PFAS = self.Mixed_flow.PFAS - self.Volatilized.PFAS

        # Calculating the volume of precipitation (includes RunOff and Leachate)
        Precip_Vol = self.Inc_flow.ts / self.InputData.LandApp['appl_dens']['amount'] * self.InputData.Precip['ann_precip']['amount'] * 1000  # L/yr
        total = self.InputData.Precip['frac_ET']['amount']+self.InputData.Precip['frac_runoff']['amount']
        if total > 1:
            self.InputData.Precip['frac_ET']['amount'] /= total
            self.InputData.Precip['frac_runoff']['amount'] /= total

        ET_Vol = Precip_Vol * self.InputData.Precip['frac_ET']['amount']  # L/yr
        RunOff_Vol = Precip_Vol * self.InputData.Precip['frac_runoff']['amount']  # L/yr
        Leachate_Vol = Precip_Vol - ET_Vol - RunOff_Vol
        if Leachate_Vol < 0 and Leachate_Vol > -0.0001:
            Leachate_Vol = 0.0

        # Calculating the PFAS in water and soil partitions
        self.Remaining, self.Leachate, self.RunOff = soil_sorption(self.Mixed_flow, self.InputData.LogPartCoef, Leachate_Vol, RunOff_Vol)

        # add to Inventory
        self.Inventory.add('Volatilized', self.Name, 'Air', self.Volatilized)
        self.Inventory.add('Leachate', self.Name, 'Water', self.Leachate)
        self.Inventory.add('RunOff', self.Name, 'Water', self.RunOff)
        self.Inventory.add('Remaining', self.Name, 'Soil', self.Remaining)

    def products(self):
        Products = {}
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
            report['Remaining in Soil'] = self.Remaining.PFAS
            report['Leachate'] = self.Leachate.PFAS
            report['Runoff'] = self.RunOff.PFAS
        else:
            report['Volatilized'] = round(self.Volatilized.PFAS / self.Inc_flow.PFAS * 100, 2)
            report['Remaining in Soil'] = round(self.Remaining.PFAS / self.Inc_flow.PFAS * 100, 2)
            report['Leachate'] = round(self.Leachate.PFAS / self.Inc_flow.PFAS * 100, 2)
            report['Runoff'] = round(self.RunOff.PFAS / self.Inc_flow.PFAS * 100, 2)
        return(report)
