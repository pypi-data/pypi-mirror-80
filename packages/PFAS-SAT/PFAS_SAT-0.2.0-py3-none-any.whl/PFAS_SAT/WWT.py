# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 10:44:45 2020

@author: msmsa
"""
import pandas as pd
from .Flow import Flow
from .SubProcesses import split, mix, dewatering, drying, solid_water_partition
from .WWTInput import WWTInput
from .ProcessModel import ProcessModel


class WWT(ProcessModel):
    """
    Assumptions:
        1. No volatilization or degradation of PFAS.
        2. Steady state.
        3. Annual time horizon.
    """
    ProductsType = ['WWTEffluent', 'DewateredWWTSolids', 'DriedWWTSolids', 'RawWWTSolids', 'WWTScreenRejects']

    def __init__(self, input_data_path=None, CommonDataObjct=None, InventoryObject=None, Name=None):
        super().__init__(CommonDataObjct, InventoryObject)
        self.InputData = WWTInput(input_data_path)
        self.Name = Name if Name else 'WWT'

    def calc(self, Inc_flow):
        # Initialize the Incoming flow
        self.Inc_flow = Inc_flow

        # Mix incoming PFAS Contaminated waste water with Waste water in WWT
        self.WasteWater = Flow()
        self.WasteWater.ts = 0
        self.WasteWater.C = 0
        self.WasteWater.vol = self.InputData.WWT['Des_Cap']['amount'] * 10**6 - self.Inc_flow.vol
        self.WasteWater.moist = self.WasteWater.vol * 1
        self.WasteWater.mass = self.WasteWater.moist + self.WasteWater.ts

        # Mixing the Incoming flow with WasteWater
        self.Mixture = mix(self.Inc_flow, self.WasteWater)

        # PFAS loss to volatilization
        self.Volatilized = Flow()
        self.Volatilized.PFAS = self.Mixture.PFAS * self.InputData.Volatilization['frac_vol_loss']['amount']
        self.Mixture.PFAS = self.Mixture.PFAS - self.Volatilized.PFAS

        # Screen and Grit Removal
        rmvd_frac = self.InputData.Screen['frac_sr-grit']['amount']
        self.screen = split(self.Mixture, **{'effluent': 1-rmvd_frac, 'rmvd': rmvd_frac})

        # set properties for screen rejects
        self.screen['rmvd'].mass = self.screen['rmvd'].vol * 1 / (1 - self.InputData.Screen['sol_cont_sr_grit']['amount'])
        self.screen['rmvd'].ts = self.screen['rmvd'].mass * self.InputData.Screen['sol_cont_sr_grit']['amount']
        self.screen['rmvd'].C = 0 if self.Inc_flow.ts == 0 else self.screen['rmvd'].ts / self.Inc_flow.ts * self.Inc_flow.C
        self.screen['rmvd'].VS = 0 if self.Inc_flow.ts == 0 else (0 if 'VS' not in self.Inc_flow.__dict__
                                                                  else self.screen['rmvd'].ts / self.Inc_flow.ts * self.Inc_flow.VS)
        self.screen['rmvd'].moist = self.screen['rmvd'].mass - self.screen['rmvd'].ts

        # Primary Settling
        rmvd_frac = self.InputData.PrimSet['is_prim_set']['amount'] * self.InputData.PrimSet['frac_prim_solids']['amount']
        self.prim_set = split(self.screen['effluent'], **{'effluent': 1-rmvd_frac, 'rmvd': rmvd_frac})

        # Set the mass flow for rmvd solids in Primary Settling
        self.prim_set['rmvd'].mass = self.prim_set['rmvd'].vol * 1 / (1 - self.InputData.PrimSet['sol_cont_prim_solids']['amount'])
        self.prim_set['rmvd'].ts = self.prim_set['rmvd'].mass * self.InputData.PrimSet['sol_cont_prim_solids']['amount']
        self.prim_set['rmvd'].C = 0 if self.Inc_flow.ts == 0 else self.prim_set['rmvd'].ts / self.Inc_flow.ts * self.Inc_flow.C
        self.prim_set['rmvd'].VS = 0 if self.Inc_flow.ts == 0 else (0 if 'VS' not in self.Inc_flow.__dict__
                                                                    else self.prim_set['rmvd'].ts / self.Inc_flow.ts * self.Inc_flow.VS)
        self.prim_set['rmvd'].moist = self.prim_set['rmvd'].mass - self.prim_set['rmvd'].ts

        # Biological Treatment (Partition PFAS to water and biosolids produced in biological treatment)
        self.prim_set['effluent'].ts = self.prim_set['effluent'].mass * self.InputData.BioTrtmnt['sol_cont']['amount'] / 10**6
        self.prim_set['effluent'].C = self.prim_set['effluent'].ts * self.InputData.BioTrtmnt['C_cont']['amount']
        self.prim_set['effluent'].VS = self.prim_set['effluent'].ts * self.InputData.BioTrtmnt['VS_cont']['amount']
        self.prim_set['effluent'].moist = self.screen['effluent'].moist - self.prim_set['rmvd'].moist
        self.prim_set['effluent'].vol = self.prim_set['effluent'].moist * 1
        self.prim_set['effluent'].mass = self.prim_set['effluent'].ts + self.prim_set['effluent'].moist

        _, self.C_effluent = solid_water_partition(self.prim_set['effluent'], self.prim_set['effluent'].moist, self.InputData.LogPartCoef)

        # Secondary Settling
        rmvd_frac = self.InputData.SecSet['frac_sec_solids']['amount']
        self.sec_set = split(self.prim_set['effluent'], **{'effluent': 1-rmvd_frac, 'rmvd': rmvd_frac})

        # Set the mass flow for rmvd solids in Secondary Settling
        self.sec_set['rmvd'].ts = self.prim_set['effluent'].ts
        self.sec_set['rmvd'].C = self.prim_set['effluent'].C
        self.sec_set['rmvd'].VS = self.prim_set['effluent'].VS
        self.sec_set['rmvd'].moist = self.sec_set['rmvd'].vol * 1
        self.sec_set['rmvd'].mass = self.sec_set['rmvd'].ts + self.sec_set['rmvd'].moist

        self.sec_set['effluent'].ts = 0
        self.sec_set['effluent'].C = 0
        self.sec_set['effluent'].VS = 0
        self.sec_set['effluent'].mass = self.sec_set['effluent'].vol * 1 + self.sec_set['effluent'].ts

        self.sec_set['effluent'].PFAS = self.C_effluent * self.sec_set['effluent'].moist
        self.sec_set['rmvd'].PFAS = self.prim_set['effluent'].PFAS - self.sec_set['effluent'].PFAS

        # Calc mass to Thickening
        if self.InputData.Thick['is_prim_thick']['amount'] and self.InputData.Thick['is_sec_thick']['amount']:
            self.flow_to_thick = mix(self.prim_set['rmvd'], self.sec_set['rmvd'])
            self.RawWWTSolids = Flow(ZeroFlow=True)
            self.RawWWTSolids.VS = 0
        elif self.InputData.Thick['is_prim_thick']['amount']:
            self.flow_to_thick = self.prim_set['rmvd']
            self.RawWWTSolids = self.sec_set['rmvd']
        elif self.InputData.Thick['is_sec_thick']['amount']:
            self.flow_to_thick = self.sec_set['rmvd']
            self.RawWWTSolids = self.prim_set['rmvd']
        else:
            self.flow_to_thick = Flow(ZeroFlow=True)
            self.flow_to_thick.VS = 0
            self.RawWWTSolids = mix(self.prim_set['rmvd'], self.sec_set['rmvd'])

        # Thickening: assumed that the removed water has the same PFAS concentration as input flow
        # Dewatering and thickening are active or inactive together.
        self.thick = {}
        self.thick['solids'], self.thick['rmvd_water'] = dewatering(mixture=self.flow_to_thick,
                                                                    final_sol_cont=self.InputData.Thick['sol_cont_thick']['amount'],
                                                                    cont_PFAS_water=self.C_effluent,
                                                                    is_active=self.InputData.Dew['is_sol_dew']['amount'])

        # Dewatering: assumed that the removed water has the same PFAS concentration as input flow
        self.Dew = {}
        self.Dew['solids'], self.Dew['rmvd_water'] = dewatering(mixture=self.thick['solids'],
                                                                final_sol_cont=self.InputData.Dew['sol_cont_dewat']['amount'],
                                                                cont_PFAS_water=self.C_effluent,
                                                                is_active=self.InputData.Dew['is_sol_dew']['amount'])

        # Drying: assumed that the removed water has the same PFAS concentration as input flow
        self.Dry = {}
        if self.InputData.Dry['is_sol_dry']['amount']:
            self.Dry['solids'], self.Dry['DryerExhaust'] = drying(mixture=self.Dew['solids'],
                                                                  dryer_param=self.InputData.Dry,
                                                                  cont_PFAS_water=self.Inc_flow.get_PFAScont())
        else:
            self.Dry['solids'] = Flow(ZeroFlow=True)
            self.Dry['solids'].VS = 0
            self.Dry['DryerExhaust'] = Flow(ZeroFlow=True)
            self.Dry['DryerExhaust'].VS = 0

        # Efflunet
        self.Efflunet = mix(self.sec_set['effluent'], self.thick['rmvd_water'], self.Dew['rmvd_water'])

        # Allocating the Effluent and produced biosolids to the incoming PFAS contaminated water
        self._AllocationFactor = self.Inc_flow.vol / self.Mixture.vol
        # Effluent
        self.Efflunet.mass *= self._AllocationFactor
        self.Efflunet.vol *= self._AllocationFactor
        self.Efflunet.moist *= self._AllocationFactor
        self.Efflunet.ts *= self._AllocationFactor
        self.Efflunet.C *= self._AllocationFactor

        # Biosolids
        for flow in [self.screen['rmvd'], self.RawWWTSolids, self.thick['solids'], self.Dew['solids'], self.Dry['solids']]:
            flow.mass *= self._AllocationFactor
            if 'vol' in flow.__dict__:
                flow.vol *= self._AllocationFactor
            flow.moist *= self._AllocationFactor
            flow.ts *= self._AllocationFactor
            flow.C *= self._AllocationFactor
            flow.VS *= self._AllocationFactor

        # add to Inventory
        self.Inventory.add('Volatilized', self.Name, 'Air', self.Volatilized)
        self.Inventory.add('DryerExhaust', self.Name, 'Air', self.Dry['DryerExhaust'])

    def products(self):
        Products = {}
        Products['WWTScreenRejects'] = self.screen['rmvd']
        Products['WWTEffluent'] = self.Efflunet
        Products['RawWWTSolids'] = self.RawWWTSolids
        if self.InputData.Dry['is_sol_dry']['amount']:
            Products['DewateredWWTSolids'] = Flow(ZeroFlow=True)
            Products['DriedWWTSolids'] = self.Dry['solids']
        elif self.InputData.Dew['is_sol_dew']['amount']:
            Products['DewateredWWTSolids'] = self.Dew['solids']
            Products['DriedWWTSolids'] = Flow(ZeroFlow=True)
        else:
            Products['DewateredWWTSolids'] = Flow(ZeroFlow=True)
            Products['DriedWWTSolids'] = Flow(ZeroFlow=True)
            Products['RawWWTSolids'] = self.RawWWTSolids
        return(Products)

    def setup_MC(self, seed=None):
        self.InputData.setup_MC(seed)

    def MC_Next(self):
        input_list = self.InputData.gen_MC()
        return(input_list)

    def report(self, normalized=False):
        report = pd.DataFrame(index=self.Inc_flow._PFAS_Index)
        products = self.products()
        if not normalized:
            report['Volatilized'] = self.Volatilized.PFAS
            report['DryerExhaust'] = self.Dry['DryerExhaust'].PFAS
            report['WWT Effluent'] = self.Efflunet.PFAS
            report['solids'] = products['RawWWTSolids'].PFAS + products['DewateredWWTSolids'].PFAS + products['DriedWWTSolids'].PFAS
            report['Screen Rejects'] = products['WWTScreenRejects'].PFAS
        else:
            report['Volatilized'] = round(self.Volatilized.PFAS / self.Inc_flow.PFAS * 100, 2)
            report['DryerExhaust'] = round(self.Dry['DryerExhaust'].PFAS / self.Inc_flow.PFAS * 100, 2)
            report['WWT Effluent'] = round(self.Efflunet.PFAS / self.Inc_flow.PFAS * 100, 2)
            report['solids'] = round((products['RawWWTSolids'].PFAS + products['DewateredWWTSolids'].PFAS + products['DriedWWTSolids'].PFAS) /
                                     self.Inc_flow.PFAS * 100, 2)
            report['Screen Rejects'] = round(products['WWTScreenRejects'].PFAS / self.Inc_flow.PFAS * 100, 2)
        return(report)
