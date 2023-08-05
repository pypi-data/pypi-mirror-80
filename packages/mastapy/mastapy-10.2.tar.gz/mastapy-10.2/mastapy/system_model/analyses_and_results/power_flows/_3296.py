'''_3296.py

GuideDxfModelPowerFlow
'''


from mastapy.system_model.part_model import _2018
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6153
from mastapy.system_model.analyses_and_results.power_flows import _3264
from mastapy._internal.python_net import python_net_import

_GUIDE_DXF_MODEL_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'GuideDxfModelPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('GuideDxfModelPowerFlow',)


class GuideDxfModelPowerFlow(_3264.ComponentPowerFlow):
    '''GuideDxfModelPowerFlow

    This is a mastapy class.
    '''

    TYPE = _GUIDE_DXF_MODEL_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GuideDxfModelPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2018.GuideDxfModel':
        '''GuideDxfModel: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2018.GuideDxfModel)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6153.GuideDxfModelLoadCase':
        '''GuideDxfModelLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6153.GuideDxfModelLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
