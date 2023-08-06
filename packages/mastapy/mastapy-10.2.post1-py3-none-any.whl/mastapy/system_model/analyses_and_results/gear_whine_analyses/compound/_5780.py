﻿'''_5780.py

RootAssemblyCompoundGearWhineAnalysis
'''


from mastapy.system_model.analyses_and_results.gear_whine_analyses.compound import _5699
from mastapy._internal.python_net import python_net_import

_ROOT_ASSEMBLY_COMPOUND_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.Compound', 'RootAssemblyCompoundGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('RootAssemblyCompoundGearWhineAnalysis',)


class RootAssemblyCompoundGearWhineAnalysis(_5699.AssemblyCompoundGearWhineAnalysis):
    '''RootAssemblyCompoundGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _ROOT_ASSEMBLY_COMPOUND_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RootAssemblyCompoundGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
