# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 21:31:49 2020

@author: msmsa
"""
from abc import ABC, abstractmethod
from .CommonData import CommonData
from .Inventory import Inventory
from matplotlib.sankey import Sankey
import matplotlib.pyplot as plt
import pandas as pd
from copy import deepcopy


class ProcessModel(ABC):
    def __init__(self, CommonDataObjct, InventoryObject):
        if CommonDataObjct:
            self.CommonData = CommonDataObjct
        else:
            self.CommonData = CommonData()

        if InventoryObject:
            self.Inventory = InventoryObject
        else:
            self.Inventory = Inventory()

    @property
    @abstractmethod
    def ProductsType(self):
        pass

    @abstractmethod
    def calc(self):
        pass

    @abstractmethod
    def setup_MC(self, seed=None):
        pass

    @abstractmethod
    def MC_Next(self):
        pass

    @abstractmethod
    def report(self):
        pass

    def plot_sankey(self, **kwargs):
        Data = self.report().sum().sort_values(ascending=False)
        Total = sum(self.Inc_flow.PFAS)
        flows = [1]
        labels = ['Incoming PFAS']
        orientations = [0]
        pathlengths = [0.7]
        for j, i in enumerate(Data.index):
            flows.append(-round(Data[i]/Total, 4))
            labels.append(i.replace(' ', '\n'))
            if j in [0, 1, 2]:
                pathlengths.append(0.35)
            elif j in [3, 4]:
                pathlengths.append(0.8)
            else:
                pathlengths.append(1.2)

            if j == 0:
                Or = 0
            elif j % 2 == 1:
                Or = -1
            else:
                Or = 1
            orientations.append(Or)

        margin = 1.4 if 'margin' not in kwargs else kwargs['margin']
        offset = 0.25 if 'offset' not in kwargs else kwargs['offset']
        gap = 0.7 if 'gap' not in kwargs else kwargs['gap']

        Sankey(flows=flows, labels=labels, orientations=orientations, pathlengths=pathlengths, gap=gap, offset=offset, margin=margin).finish()

    def plot_sankey_report(self, **kwargs):
        margin = 1.4 if 'margin' not in kwargs else kwargs['margin']
        offset = 0.25 if 'offset' not in kwargs else kwargs['offset']
        gap = 0.7 if 'gap' not in kwargs else kwargs['gap']
        figsize = (12, 5) if 'figsize' not in kwargs else kwargs['figsize']

        fig = plt.figure(figsize=figsize)

        Data = self.report().loc['PFOA'].sort_values(ascending=False)
        Total = self.Inc_flow.PFAS['PFOA']
        flows = [1]
        labels = ['Incoming PFOA']
        orientations = [0]
        pathlengths = [0.7]

        for j, i in enumerate(Data.index):
            if float('%.1g' % (Data[i]/Total)) >= 0.11:
                flows.append(-float('%.2g' % (Data[i]/Total)))
            else:
                flows.append(-float('%.1g' % (Data[i]/Total)))
            labels.append(i.replace(' ', '\n'))
            if j in [0, 1, 2]:
                pathlengths.append(0.35)
            elif j in [3, 4]:
                pathlengths.append(0.8)
            else:
                pathlengths.append(1.2)

            if j == 0:
                Or = 0
            elif j % 2 == 1:
                Or = -1
            else:
                Or = 1
            orientations.append(Or)

        ax1 = fig.add_subplot(1, 2, 1, xticks=[], yticks=[], title="Total Incoming PFOA: "+format(Total, '.2E')+" μg")
        Sankey(ax=ax1, flows=flows, labels=labels, orientations=orientations, pathlengths=pathlengths, gap=gap, offset=offset, margin=margin).finish()

        Data = self.report().loc['PFOS'].sort_values(ascending=False)
        Total = self.Inc_flow.PFAS['PFOS']
        flows = [1]
        labels = ['Incoming PFOS']
        orientations = [0]
        pathlengths = [0.7]
        for j, i in enumerate(Data.index):
            if float('%.1g' % (Data[i]/Total)) >= 0.11:
                flows.append(-float('%.2g' % (Data[i]/Total)))
            else:
                flows.append(-float('%.1g' % (Data[i]/Total)))
            labels.append(i.replace(' ', '\n'))
            if j in [0, 1, 2]:
                pathlengths.append(0.35)
            elif j in [3, 4]:
                pathlengths.append(0.8)
            else:
                pathlengths.append(1.2)

            if j == 0:
                Or = 0
            elif j % 2 == 1:
                Or = -1
            else:
                Or = 1
            orientations.append(Or)

        ax2 = fig.add_subplot(1, 2, 2, xticks=[], yticks=[], title="Total Incoming PFOS: "+format(Total, '.2E')+" μg")
        Sankey(ax=ax2, flows=flows, labels=labels, orientations=orientations, pathlengths=pathlengths, gap=gap, offset=offset, margin=margin).finish()

    def SA(self, inputflow, stream, n, figsize):
        self.setup_MC()
        for i in range(100):
            inpt = self.MC_Next()
            self.calc(inputflow)
            res = self.report().loc['PFOA']
            if i == 0:
                columns = []
                for j in inpt:
                    columns.append(j[0])
                for j in res.index:
                    columns.append(j)
                output = pd.DataFrame(columns=columns)
            row = []
            for j in inpt:
                row.append(j[1])
            for j in res:
                row.append(j)
            output.loc[i] = row

        corr_data = output[columns[1:]].corr(method='pearson')

        # ploting the DataFrame
        for x in res.index:
            columns.remove(x)

        col = deepcopy(columns)

        for j in col:
            for x in ['PFOS', 'PFBA', 'PFPeA', 'PFHxA', 'PFHpA', 'PFNA', 'PFDA', 'PFBS', 'PFHxS']:
                if x in str(j):
                    try:
                        columns.remove(j)
                    except:
                        pass

        corr_data_plot = corr_data[stream][columns]
        sorted_corr = corr_data_plot.abs().sort_values(ascending=False)

        if len(sorted_corr.index) <= n:
            index = sorted_corr.index
        else:
            index = sorted_corr.index[0:n]
        fig = plt.figure(figsize=figsize)
        ax_plot_corr = fig.add_subplot(1, 1, 1)
        ax_plot_corr = corr_data_plot[index].plot(kind='barh', ax=ax_plot_corr)
        # set lables
        ax_plot_corr.set_xlabel('Correlation with mass of PFOA in {}'.format(stream), fontsize=18)
        ax_plot_corr.set_xlim(-1, 1)
        ax_plot_corr.tick_params(axis='both', which='major', labelsize=18, rotation='auto')
        ax_plot_corr.tick_params(axis='both', which='minor', labelsize=16, rotation='auto')
        return(output)
