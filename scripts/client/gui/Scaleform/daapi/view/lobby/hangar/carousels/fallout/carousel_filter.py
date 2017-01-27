# Embedded file name: scripts/client/gui/Scaleform/daapi/view/lobby/hangar/carousels/fallout/carousel_filter.py
from account_helpers.AccountSettings import FALLOUT_CAROUSEL_FILTER_1, FALLOUT_CAROUSEL_FILTER_2
from gui.shared.utils.requesters import REQ_CRITERIA
from gui.Scaleform.daapi.view.lobby.hangar.carousels.basic.carousel_filter import CarouselFilter, BasicCriteriesGroup, EventCriteriesGroup

class FalloutCarouselFilter(CarouselFilter):

    def __init__(self):
        super(FalloutCarouselFilter, self).__init__()
        self._serverSections = (FALLOUT_CAROUSEL_FILTER_1, FALLOUT_CAROUSEL_FILTER_2)
        self._criteriesGroups = (EventCriteriesGroup(), FalloutBasicCriteriesGroup())


class FalloutBasicCriteriesGroup(BasicCriteriesGroup):

    def update(self, filters):
        super(FalloutBasicCriteriesGroup, self).update(filters)
        if filters['gameMode']:
            self._criteria |= REQ_CRITERIA.VEHICLE.FALLOUT.AVAILABLE