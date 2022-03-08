CASH_SIZE = 10 * 60  # seconds
ACCIDENT_TIME = 2 * 60  # seconds


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
        tt, ids = self.data[-1]
        min_time = {}
        for t, ids in self.data[::-1]:
            for id in ids:
                min_time[id] = t
        accident = False
        for id in ids:
            if id in self.blocked_ids:
                continue
            if tt - min_time[id] >= ACCIDENT_TIME:
                accident = True
                self.blocked_ids.add(id)
        return accident
