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
********************
Soil Stabilization
********************

The process includes mixing an additive into the soil to which the PFAS will preferentially sorb. The PFAS in the
contaminated soil will either be released to surface or ground- water, and the remainder will sorbed to the soil/additive
mixture. The flow of PFAS from soil stabilization is modeled using a liquid-solid partition coefficient normalized to the
amount of organic carbon, combined with a water balance to track the flow of PFAS through the soil. Model predictions are
based on achievement of equilibrium. It is further assumed that the soil and additive are well mixed. The partition
coefficient is used to estimate the concentration of PFAS in the liquid and solids. By default, it is assumed that no
volatilization occurs, but a user can enter a fraction of PFAS that is volatilized.

The concentration in the liquid changes throughout the year as PFAS is leached to the groundwater (i.e., it is assumed
that annual precipitation is uniform throughout the year and continuously removes PFAS from the mixture). The user enters
a run-off coefficient based on the soil type, land use, grade, and vegetation. The run-off is assumed to be released to
surface water. Another fraction of the precipitation is removed via evapotranspiration (ET) based on the location and vegetation.
The remaining precipitation is assumed to leach into groundwater. The PFAS remaining in the soil may be taken up by and
bioaccumulate in plants; however, this is outside the scope of the current effort and will depend on how the land is used.

=============================
Assumptions and Limitations:
=============================

#. The water balance model is averaged over a year and ignores potential effects from intense rains that may lead to substantial
   additional erosion and loss of solids and associated PFAS.
#. Volatilization is assumed to be zero by default due to a lack of data. However, the user may assign a fraction of the PFAS to
   be volatilized.
#. Future work is required to implement a dynamic (i.e., non-equilibrium) model to account for changes in the organic C content of
   over time as land-applied materials decompose, and to account for episodic precipitation events.
#. Default soil properties reflect representative values for loam and silty clay loams, but the values for different situations are
   provided and may be input by the user.
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
