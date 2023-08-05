# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 11:29:42 2020

@author: Mojtaba Sardarmehni
"""
import pandas as pd
from .CommonData import CommonData


class Flow:
    def __init__(self, ZeroFlow=False, **kwargs):
        self._PFAS_Index = CommonData.PFAS_Index
        if not ZeroFlow:
            self.mass = None        # kg
            self.ts = None          # kg
            self.moist = None       # kg
            self.C = None           # kg
            self.bulk_dens = None   # kg/m3
            self.PFAS = pd.Series(data=[0 for i in self._PFAS_Index], index=self._PFAS_Index, dtype=float)  # μg
        else:
            self.mass = 0        # kg
            self.ts = 0          # kg
            self.moist = 0       # kg
            self.C = 0           # kg
            self.bulk_dens = 0   # kg/m3
            self.PFAS = pd.Series(data=[0 for i in self._PFAS_Index], index=self._PFAS_Index, dtype=float)  # μg

        for key, value in kwargs.items():
            setattr(self, key, value)

    def set_flow(self, mass_flow, ts_cont=None, C_cont=None, PFAS_cont=None, bulk_dens=None, **kwargs):
        self.mass = mass_flow
        self.ts = mass_flow * ts_cont if not pd.isna(ts_cont) else None
        self.moist = mass_flow * (1 - ts_cont) if not pd.isna(ts_cont) else None
        self.C = self.ts * C_cont if (not pd.isna(ts_cont) and not pd.isna(C_cont)) else None
        self.bulk_dens = bulk_dens if not pd.isna(bulk_dens) else None

        if PFAS_cont:
            self.PFAS = pd.Series([PFAS_cont[i] * self.mass for i in self._PFAS_Index], index=self._PFAS_Index, dtype=float)

        for key, value in kwargs.items():
            if key == 'VS_cont':
                setattr(self, 'VS', value * self.ts)
                setattr(self, 'Ash', (1-value) * self.ts)

            if key == 'Ash_cont':
                setattr(self, 'VS', (1-value) * self.ts)
                setattr(self, 'Ash', value * self.ts)

            elif key == 'vol_flow':
                setattr(self, 'vol', value)
            elif key == 'density':
                setattr(self, 'vol', self.mass / value)
            else:
                setattr(self, key, value)

    def get_Ccont(self):
        return (self.C/self.ts)

    def get_TScont(self):
        return (self.ts/self.mass)

    def get_Moistcont(self):
        return (self.moist/self.mass)

    def get_PFAScont(self):
        if self.mass == 0 and self.vol > 0:
            return (self.PFAS/self.vol)
        return (self.PFAS/self.mass)

    def set_FlowType(self, FlowType):
        self.FlowType = FlowType

    def report(self):
        report = pd.DataFrame(columns=['Parameter', 'Unit', 'Amount'])
        report.loc[0] = ['Mass flow', 'kg', self.mass]
        report.loc[1] = ['Solids flow', 'kg', self.ts]
        report.loc[2] = ['Moisture flow', 'kg', self.moist]
        i = 3
        if 'vol' in self.__dict__:
            report.loc[i] = ['Volume flow', 'L', self.vol]
            i += 1
        if 'VS' in self.__dict__:
            report.loc[i] = ['VS flow', 'kg', self.VS]
            i += 1
        report.loc[i] = ['Carbon flow', 'kg', self.C]
        i += 1
        for j in self.PFAS.index:
            report.loc[i] = [j, 'μg', self.PFAS[j]]
            i += 1
        return(report)
