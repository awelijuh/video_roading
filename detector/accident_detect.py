import logging    

CASH_SIZE = 10 * 60  # seconds
ACCIDENT_TIME = 2 * 60  # seconds
ACCIDENT_COUNT = 40  # count
logger = logging.getLogger('accident_detector')


class AccidentDetector:
    def __init__(self):
        self.data = []
        self.blocked_ids = set()

    def add_time(self, time, ids):
        self.data.append((time, ids))
        ind = 0
        while time - self.data[ind][0] > CASH_SIZE:
            ind += 1
        self.data = self.data[ind:]

    def is_accident(self):
        tt, last_ids = self.data[-1]
        min_time = {}
        ids_count = {}
        for t, ids in self.data[::-1]:
            for id in ids:
                min_time[id] = t
                if ids_count.get(id) is None:
                    ids_count[id] = 0
                ids_count[id] += 1
        accident = False
        accident_ids = []
        for id in last_ids:
            if id in self.blocked_ids:
                continue
            if tt - min_time[id] >= ACCIDENT_TIME and ids_count[id] > ACCIDENT_COUNT:
                accident = True
                self.blocked_ids.add(id)
                accident_ids.append(id)
        if accident:
            logger.info('accident detected!')
        return accident
