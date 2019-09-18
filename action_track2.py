# simulator tilt track
# _________________________________________


#      0,1                0,0
# -1,0    1,0    :   1,0      1,1
#    0,-1                 0,1
# yes event tracking forward -->
# may be event tracking forward with stop -!?
# canceled event tracking forward and back --> < --
# yes after cancel <---->

import time
# import datetime
import random

# from key_event_dev import KeyboardString2FD as ks2
from key_event_dev import kinv as ks1
# import numpy
# import json
ADCvolt = 3  # voltage on the ADC volt
Differend = 0.03  # voltage difference at the ADC inputs
ADC_scale = 4096  # ADC 12 bit
Frequency = 10  # sampling rate in Hz
Threshold = 1000


class TiltMove:

    def __init__(self, vect, inv):
        self.inv = inv
        self.vect = vect
        self.x_0 = self.vect[0] * self.inv
        self.x_1 = self.vect[1] * self.inv
        self.x_2 = self.vect[2]
        self.adc_scl = ADC_scale
        self.frq = Frequency
        self.tf = 1/Threshold
        self.dfr = Differend / ADCvolt
        self.thr = int(Threshold)

    def to_end(self):
        return int(self.adc_scl - random.randrange(0, 500))  # random power

    def quest_point(self):
        return int(self.adc_scl - (random.randrange(0, 900, 100) + 100))

    def zoom_tilt(self):
        return int((self.adc_scl/self.frq))

    def tikl_mov(self, m, s):
        if s == 0:
            yield m, self.x_2
            m += self.zoom_tilt()
            time.sleep(self.tf)
        elif s != 0:
            yield m, self.x_2
            m -= self.zoom_tilt()
            time.sleep(self.tf)

    def sim_mov(self, m):
        if self.x_0 != 0:
            yield int(m * self.x_0 * self.dfr), 0
            time.sleep(self.tf)
        elif self.x_1 != 0:
            yield 0, m * int(self.x_1 * self.dfr)
            time.sleep(self.tf)


class TiklEvent(TiltMove):

    def __call__(self, ch):
        timer = time.time()
        while time.time() - timer < 1:
            for tkl in range(0, self.thr + ch, self.zoom_tilt()):
                for t2 in self.tikl_mov(tkl, 0):
                    yield t2
            for tkl2 in range(self.thr, 0, -self.zoom_tilt()):
                for t3 in self.tikl_mov(tkl2, 1):
                    yield t3


class YesEvent(TiltMove):

    def __call__(self, ch):
        for tilt_pow in range(0, self.to_end(), self.zoom_tilt()):
            if tilt_pow < self.thr - ch:
                for j9 in self.tikl_mov(tilt_pow, 0):
                    yield j9
            else:
                for j10 in self.sim_mov(tilt_pow):
                    yield j10
        yield self.x_0, self.x_1


# class YesEv2(TiltMove):
#
#     def __call__(self, ch):
#         for tilt_pow in range(0, self.to_end(), self.zoom_tilt()):
#             if tilt_pow < self.thr - ch:
#                 for j9 in self.tikl_mov(tilt_pow, 0):
#                     yield j9
#             else:
#                 for j10 in self.sim_mov(tilt_pow):
#                     yield j10
#         yield self.x_0, self.x_1, self.x_2


class NoEvent(TiltMove):

    def __call__(self, ch):
        for tilt_pow in range(0, self.to_end(), self.zoom_tilt()):
            if tilt_pow < self.thr - ch:
                for j9 in self.tikl_mov(tilt_pow, 0):
                    yield j9
            else:
                for j10 in self.sim_mov(tilt_pow):
                    yield j10
        for tilt_no in range(self.to_end(), 0, - self.zoom_tilt()):
            if tilt_no < self.thr - ch:
                for j11 in self.tikl_mov(tilt_no, 1):
                    yield j11
            else:
                for j11 in self.sim_mov(tilt_no):
                    yield j11
        yield 0, 0


class MayBeNo(TiltMove):

    def variant(self):
        if self.x_0 != 0:
            wrt = ks1[self.x_2]
            return wrt
        elif self.x_1 != 0:
            wrt2 = ks1[self.x_2]
            return wrt2

    def __call__(self, ch):
        to_half = self.to_end()//2
        to_rand = int(((to_half - 10) * random.random()) + to_half)
        # contr = [i4 * -1 for i4 in self.vect]
        for tilt_mb in range(0, to_rand, self.zoom_tilt()):
            if tilt_mb < self.thr - ch:
                for j12 in self.tikl_mov(tilt_mb, 0):
                    yield j12
            else:
                for j13 in self.sim_mov(tilt_mb):
                    yield j13
        timer = time.time()
        while time.time() - timer < 3:
            if self.x_0 != 0:
                yield int(to_rand * self.x_0 * self.dfr), 0
                time.sleep(1)
                yield int(-to_rand * self.x_0 * self.dfr), 0
            elif self.x_1 != 0:
                yield 0, int(to_rand * self.x_1 * self.dfr)
                time.sleep(1)
                yield 0, int(-to_rand * self.x_1 * self.dfr)

        may_be = input(f"input {self.variant()[0]} or {self.variant()[1]}")
        with open("box_tlt", "w") as bt:
            if may_be == self.variant()[0]:
                yield self.x_0, self.x_1, self.x_2
                bt.write(str(1))
            elif may_be == self.variant()[1]:
                yield -self.x_0, -self.x_1, self.x_2
                bt.write(str(-1))
            else:
                yield 0, 0


class MayBeYes(TiltMove):

    def __call__(self, ch):
        for tilt_pow in range(0, self.to_end(), self.zoom_tilt()):
            if tilt_pow < self.thr - ch:
                for j14 in self.tikl_mov(tilt_pow, 0):
                    yield j14
            else:
                for j15 in self.sim_mov(tilt_pow):
                    yield j15

        for tilt_no in range(self.to_end(), 0, - self.zoom_tilt()):
            if tilt_no < self.thr - ch:
                for j16 in self.tikl_mov(tilt_no, 1):
                    yield j16
            else:
                for j17 in self.sim_mov(tilt_no):
                    yield j17

        for tilt_pow in range(0, -self.to_end(), -self.zoom_tilt()):
            if tilt_pow > -self.thr + ch:
                for j14 in self.tikl_mov(tilt_pow, 1):
                    yield j14
            else:
                for j15 in self.sim_mov(tilt_pow):
                    yield j15

        yield -self.x_0, - self.x_1


class Stuck(TiltMove):

    def fl_loop(self, ch):
        for tilt_pow in range(0, self.to_end(), self.zoom_tilt()):
            if tilt_pow < self.thr - ch:
                for j14 in self.tikl_mov(tilt_pow, 0):
                    yield j14
            else:
                for j15 in self.sim_mov(tilt_pow):
                    yield j15

        for tilt_no in range(self.to_end(), 0, - self.zoom_tilt()):
            if tilt_no < self.thr - ch:
                for j16 in self.tikl_mov(tilt_no, 1):
                    yield j16
            else:
                for j17 in self.sim_mov(tilt_no):
                    yield j17

        for tilt_pow in range(0, -self.to_end(), -self.zoom_tilt()):
            if tilt_pow > -self.thr + ch:
                for j18 in self.tikl_mov(tilt_pow, 1):
                    yield j18
            else:
                for j19 in self.sim_mov(tilt_pow):
                    yield j19

        for tilt_no2 in range(-self.to_end(), 0, self.zoom_tilt()):
            if tilt_no2 > -self.thr + ch:
                for j20 in self.tikl_mov(tilt_no2, 1):
                    yield j20
            else:
                for j21 in self.sim_mov(tilt_no2):
                    yield j21

    def __call__(self, t):
        timer = time.time()
        while time.time() - timer < t:
            for j17 in self.fl_loop(10):
                yield j17
            time.sleep(0.3)
        yield 0, 0, self.x_2


class Twist(TiltMove):
    pass


if __name__ == "__main__":
    # yev = YesEvent([1, 0, 9], 1)
    # yev2 = yev.yes_ev(2)
    # for i01 in yev2:
    #     print(i01)
    # mby = MayBeYes([1, 0, 12], 1)
    # mb3 = mby.may_be_ya(Dwn)
    # for i10 in mb3:
    #     print(i10)
    # st1 = Stuck([1, 0, 8], 1)
    # st2 = st1.stuck(1)
    # for i16 in st2:
    #     print(i16)
    # tm2 = TiklEvent([1, 0, 10], 1)
    # tm3 = tm2.tkl_ev()
    # for i11 in tm3:
    #     print(i11)
    # y2 = YesEv2([1, 0, 12], 1)
    # for i4 in y2(10):
    #     print(i4)
    mbn2 = MayBeNo([1, 0, 12], 1)
    for i5 in mbn2(10):
        print(i5)

    pass
