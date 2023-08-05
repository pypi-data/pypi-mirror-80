# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 22:09:10 2020

@author: msmsa
"""
import pandas as pd
from .CommonData import CommonData


class Inventory:
    def __init__(self):
        self._PFAS_Index = CommonData.PFAS_Index
        self._index = ['Flow_name', 'Source', 'Target', 'Unit'] + self._PFAS_Index
        self.Inv = pd.DataFrame(index=self._index)
        self.Col_index = 0
        self._acceptableError = 5  # acceptable percent error in PFAS mass Balance

    def add(self, Flow_name, Source, Target, flow):
        if min(flow.PFAS.values) < 0:
            raise Exception('Negative PFAS flow!! \n Flow Name: {} \n Source: {}'.format(Flow_name, Source))
        data = [Flow_name, Source, Target, 'μg'] + list(flow.PFAS.values)
        self.Inv[self.Col_index] = data
        self.Col_index += 1

    def report_Water(self):
        water_inv = self.Inv[self.Inv.columns[self.Inv.loc['Target'] == 'Water']]
        return(water_inv)

    def report_Soil(self):
        soil_inv = self.Inv[self.Inv.columns[self.Inv.loc['Target'] == 'Soil']]
        return(soil_inv)

    def report_Air(self):
        air_inv = self.Inv[self.Inv.columns[self.Inv.loc['Target'] == 'Air']]
        return(air_inv)

    def report_Destroyed(self):
        Destroyed_inv = self.Inv[self.Inv.columns[self.Inv.loc['Target'] == 'Destroyed']]
        return(Destroyed_inv)

    def report_Stored(self):
        Stored_inv = self.Inv[self.Inv.columns[self.Inv.loc['Target'] == 'Stored']]
        return(Stored_inv)

    def report_InjectionWell(self):
        InjectedWell_inv = self.Inv[self.Inv.columns[self.Inv.loc['Target'] == 'Injection Well']]
        return(InjectedWell_inv)

    def report_ReactivatedGAC(self):
        ReactivatedGAC_inv = self.Inv[self.Inv.columns[self.Inv.loc['Target'] == 'Reactivated GAC']]
        return(ReactivatedGAC_inv)

    def clear(self):
        self.Inv = pd.DataFrame(index=self._index)
        self.Col_index = 0

    def report(self, TypeOfPFAS='All'):
        if TypeOfPFAS == 'All':
            Index = self._PFAS_Index
        else:
            Index = [TypeOfPFAS]
        report = dict()
        report['Water (10e-6g)'] = self.report_Water().loc[Index].sum(axis=1).sum()
        report['Soil (10e-6g)'] = self.report_Soil().loc[Index].sum(axis=1).sum()
        report['Air (10e-6g)'] = self.report_Air().loc[Index].sum(axis=1).sum()
        report['Destroyed (10e-6g)'] = self.report_Destroyed().loc[Index].sum(axis=1).sum()
        report['Stored (10e-6g)'] = self.report_Stored().loc[Index].sum(axis=1).sum()
        report['Injection Well(10e-6g)'] = self.report_InjectionWell().loc[Index].sum(axis=1).sum()
        report['Reactivated GAC (10e-6g)'] = self.report_ReactivatedGAC().loc[Index].sum(axis=1).sum()
        return(report)

    def check_PFAS_balance(self, Start_flow, pop_up=None):
        PFAS_Input = round(sum(Start_flow.PFAS.values), 1)
        PFAS_Output = round(sum(self.report(TypeOfPFAS='All').values()), 1)
        Balance_Error = round((PFAS_Input - PFAS_Output) / PFAS_Input * 100, 1)

        if Balance_Error < self._acceptableError:
            msg = """PFAS mass balance is successfully converged!
Incoming PFAS: {}
Outgoin PFAS: {}
Balance Error: {} % """.format(PFAS_Input, PFAS_Output, Balance_Error)
            if pop_up:
                pop_up('PFAS Mass Balance!', msg, 'Information')
            print(msg)
        else:
            msg = """PFAS mass balance is not converged!
Incoming PFAS: {}
Outgoin PFAS: {}
Balance Error: {} % """.format(PFAS_Input, PFAS_Output, Balance_Error)
            if pop_up:
                pop_up('PFAS Mass Balance Warning!', msg, 'Warning')
            raise Exception(msg)
