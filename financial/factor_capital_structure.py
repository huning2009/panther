#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version:
@author: Wang
@file: factor_operation_capacity.py
@time: 2019-05-30
"""
import gc, six
import sys
sys.path.append('../')
sys.path.append('../../')
sys.path.append('../../../')
import json
import numpy as np
import pandas as pd
from pandas.io.json import json_normalize
from utilities.calc_tools import CalcTools
from utilities.singleton import Singleton


# from basic_derivation import app
# from ultron.cluster.invoke.cache_data import cache_data
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


@six.add_metaclass(Singleton)
class CapitalStructure(object):
    """
    资本结构
    """
    def __init__(self):
        __str__ = 'factor_capital_structure'
        self.name = '财务指标'
        self.factor_type1 = '财务指标'
        self.factor_type2 = '资本结构'
        self.desciption = '财务指标二级指标- 资本结构'

    @staticmethod
    def NonCurrAssetRatio(tp_management, factor_management, dependencies=['total_non_current_assets', 'total_assets']):
        """
        非流动资产比率
        非流动资产比率 = 非流动资产合计 / 总资产
        :param dependencies:
        :param tp_management:
        :param factor_management:
        :return:
        """

        management = tp_management.loc[:, dependencies]
        management['NonCurrAssetRatio'] = np.where(
            CalcTools.is_zero(management.total_assets.values), 0,
            management.total_non_current_assets.values / management.total_assets.values)
        management = management.drop(dependencies, axis=1)
        factor_management = pd.merge(factor_management, management, how='outer', on="security_code")
        return factor_management

    @staticmethod
    def LongDebtToAsset(tp_management, factor_management, dependencies=['total_non_current_liability', 'total_assets']):
        """
        长期负债与资产总计之比
        长期负债与资产总计之比 = 非流动性负债合计/总资产
        :param dependencies:
        :param tp_management:
        :param factor_management:
        :return:
        """

        management = tp_management.loc[:, dependencies]
        management['LongDebtToAsset'] = np.where(
            CalcTools.is_zero(management.total_assets.values), 0,
            management.total_non_current_liability.values / management.total_assets.values)
        management = management.drop(dependencies, axis=1)
        factor_management = pd.merge(factor_management, management, how='outer', on="security_code")
        return factor_management

    @staticmethod
    def LongBorrToAssert(tp_management, factor_management, dependencies=['longterm_loan', 'total_assets']):
        """
        长期借款与资产总计之比
        长期借款与资产总计之比 = 长期借款/总资产
        :param dependencies:
        :param tp_management:
        :param factor_management:
        :return:
        """

        management = tp_management.loc[:, dependencies]
        management['LongBorrToAssert'] = np.where(
            CalcTools.is_zero(management.total_assets.values), 0,
            management.longterm_loan.values / management.total_assets.values)
        management = management.drop(dependencies, axis=1)
        factor_management = pd.merge(factor_management, management, how='outer', on="security_code")
        return factor_management

    @staticmethod
    def IntangibleAssetRatio(tp_management, factor_management, dependencies=['intangible_assets', 'development_expenditure', 'good_will', 'total_assets']):
        """
        无形资产比率
        无形资产比率 = （无形资产 + 研发支出 + 商誉）/ 总资产
        :param dependencies:
        :param tp_management:
        :param factor_management:
        :return:
        """

        management = tp_management.loc[:, dependencies]
        management["ia"] = (management.intangible_assets + management.development_expenditure + management.good_will)
        management['IntangibleAssetRatio'] = np.where(
            CalcTools.is_zero(management.total_assets.values), 0,
            management.ia.values / management.total_assets.values)
        dependencies = dependencies + ['ia']
        management = management.drop(dependencies, axis=1)
        factor_management = pd.merge(factor_management, management, how='outer', on="security_code")
        # factor_management['IntangibleAssetRatio'] = management['IntangibleAssetRatio']
        return factor_management

    @staticmethod
    def FixAssetsRt(tp_management, factor_management, dependencies=['fixed_assets', 'construction_materials', 'constru_in_process', 'total_assets']):
        """
        固定资产比率
        固定资产比率 = （固定资产+工程物资+在建工程）/总资产
        :param dependencies:
        :param tp_management:
        :param factor_management:
        :return:
        """

        management = tp_management.loc[:, dependencies]
        management['FixAssetsRt'] = np.where(
            CalcTools.is_zero(management.total_assets.values), 0,
            (management.fixed_assets.values +
             management.construction_materials.values +
             management.constru_in_process.values) / management.total_assets.values)
        management = management.drop(dependencies, axis=1)
        factor_management = pd.merge(factor_management, management, how='outer', on="security_code")
        return factor_management

    @staticmethod
    def EquityToAsset(tp_management, factor_management, dependencies=['total_owner_equities', 'total_assets']):
        """
        股东权益比率
        股东权益比率 = 股东权益/总资产
        :param dependencies:
        :param tp_management:
        :param factor_management:
        :return:
        """

        management = tp_management.loc[:, dependencies]
        management['EquityToAsset'] = np.where(
            CalcTools.is_zero(management.total_assets.values), 0,
            management.total_owner_equities.values / management.total_assets.values)
        management = management.drop(dependencies, axis=1)
        factor_management = pd.merge(factor_management, management, how='outer', on="security_code")
        return factor_management

    @staticmethod
    def EquityToFixedAsset(tp_management, factor_management, dependencies=['total_owner_equities', 'fixed_assets', 'construction_materials', 'constru_in_process']):
        """
        股东权益与固定资产比率
        股东权益与固定资产比率 = 股东权益/（固定资产+工程物资+在建工程）
        :param dependencies:
        :param tp_management:
        :param factor_management:
        :return:
        """
        management = tp_management.loc[:, dependencies]
        management['EquityToFixedAsset'] = np.where(
            CalcTools.is_zero(management.fixed_assets.values +
                              management.construction_materials.values +
                              management.constru_in_process.values), 0,
            management.total_owner_equities.values
            / (management.fixed_assets.values
               + management.construction_materials.values
               + management.constru_in_process.values))
        management = management.drop(dependencies, axis=1)
        factor_management = pd.merge(factor_management, management, how='outer', on="security_code")
        return factor_management

    @staticmethod
    def CurAssetsR(tp_management, factor_management, dependencies=['total_current_assets', 'total_assets']):
        """
        流动资产比率
        流动资产比率 = 流动资产合计M/总资产M
        :param dependencies:
        :param tp_management:
        :param factor_management:
        :return:
        """

        management = tp_management.loc[:, dependencies]
        management['CurAssetsR'] = np.where(
            CalcTools.is_zero(management.total_assets.values), 0,
            management.total_current_assets.values / management.total_assets.values)
        management = management.drop(dependencies, axis=1)
        factor_management = pd.merge(factor_management, management, how='outer', on="security_code")
        return factor_management
