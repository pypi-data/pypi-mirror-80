'''_5013.py

ClutchHalfMultiBodyDynamicsAnalysis
'''


from mastapy.system_model.part_model.couplings import _2136
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6097
from mastapy.system_model.analyses_and_results.mbd_analyses import _5030
from mastapy._internal.python_net import python_net_import

_CLUTCH_HALF_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'ClutchHalfMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchHalfMultiBodyDynamicsAnalysis',)


class ClutchHalfMultiBodyDynamicsAnalysis(_5030.CouplingHalfMultiBodyDynamicsAnalysis):
    '''ClutchHalfMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_HALF_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchHalfMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2136.ClutchHalf':
        '''ClutchHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2136.ClutchHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6097.ClutchHalfLoadCase':
        '''ClutchHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6097.ClutchHalfLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
