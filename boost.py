import time

class BoostManager:
    def __init__(self):
        self.available_boosts = 0
        self.last_gain_time = time.time()
        self.active = False
        self.boost_start = 0

    def update(self):
        if time.time() - self.last_gain_time >= 60:
            self.available_boosts += 1
            self.last_gain_time = time.time()

        if self.active and time.time() - self.boost_start >= 5:
            self.active = False

    def activate(self):
        if self.available_boosts > 0:
            self.available_boosts -= 1
            self.active = True
            self.boost_start = time.time()