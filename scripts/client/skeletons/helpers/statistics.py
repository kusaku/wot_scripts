# Embedded file name: scripts/client/skeletons/helpers/statistics.py


class IStatisticsCollector(object):

    def init(self):
        raise NotImplementedError

    def fini(self):
        raise NotImplementedError

    def start(self):
        raise NotImplementedError

    def stop(self):
        raise NotImplementedError

    def reset(self):
        raise NotImplementedError

    @property
    def update(self):
        raise NotImplementedError

    def getStatistics(self, andStop = True):
        raise NotImplementedError

    def noteHangarLoadingState(self, state, initialState = False, showSummaryNow = False):
        raise NotImplementedError