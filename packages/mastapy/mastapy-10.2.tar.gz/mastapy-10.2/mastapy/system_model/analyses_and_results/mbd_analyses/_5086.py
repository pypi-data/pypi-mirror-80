'''_5086.py

RollingRingAssemblyMultiBodyDynamicsAnalysis
'''


from mastapy.system_model.part_model.couplings import _2153
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6198
from mastapy.system_model.analyses_and_results.mbd_analyses import _5096
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_ASSEMBLY_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'RollingRingAssemblyMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingAssemblyMultiBodyDynamicsAnalysis',)


class RollingRingAssemblyMultiBodyDynamicsAnalysis(_5096.SpecialisedAssemblyMultiBodyDynamicsAnalysis):
    '''RollingRingAssemblyMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _ROLLING_RING_ASSEMBLY_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingRingAssemblyMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2153.RollingRingAssembly':
        '''RollingRingAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2153.RollingRingAssembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6198.RollingRingAssemblyLoadCase':
        '''RollingRingAssemblyLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6198.RollingRingAssemblyLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
