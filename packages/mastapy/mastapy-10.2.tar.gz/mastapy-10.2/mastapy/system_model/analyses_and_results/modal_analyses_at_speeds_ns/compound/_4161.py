'''_4161.py

DatumCompoundModalAnalysesAtSpeeds
'''


from typing import List

from mastapy.system_model.part_model import _2013
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _4036
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns.compound import _4139
from mastapy._internal.python_net import python_net_import

_DATUM_COMPOUND_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS.Compound', 'DatumCompoundModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('DatumCompoundModalAnalysesAtSpeeds',)


class DatumCompoundModalAnalysesAtSpeeds(_4139.ComponentCompoundModalAnalysesAtSpeeds):
    '''DatumCompoundModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _DATUM_COMPOUND_MODAL_ANALYSES_AT_SPEEDS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'DatumCompoundModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2013.Datum':
        '''Datum: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2013.Datum)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4036.DatumModalAnalysesAtSpeeds]':
        '''List[DatumModalAnalysesAtSpeeds]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4036.DatumModalAnalysesAtSpeeds))
        return value

    @property
    def component_modal_analyses_at_speeds_load_cases(self) -> 'List[_4036.DatumModalAnalysesAtSpeeds]':
        '''List[DatumModalAnalysesAtSpeeds]: 'ComponentModalAnalysesAtSpeedsLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysesAtSpeedsLoadCases, constructor.new(_4036.DatumModalAnalysesAtSpeeds))
        return value
