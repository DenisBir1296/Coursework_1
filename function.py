import math
#import time
import numpy as np
from scipy.special import jn_zeros, jv



class mainFunction:
    def __init__(self):
        self.error = None

        self.R = None
        self.c = None
        self.k = None
        self.alp = None
        self.l = None
        self.T = None
        self.U0 = None

        self.ro = None
        self.t = None

        self.countOfPoints = None

        self.zeros = jn_zeros(0, 1000)

    def check(self):
        if (self.ro is None) | (self.t is None):
            self.update_arrays()
        return (self.error is not None) & (self.R is not None) & (self.c is not None) \
            & (self.k is not None) & (self.alp is not None) & (self.l is not None) & (self.U0 is not None)\
            & (self.countOfPoints is not None)


    def check_ro(self, ro):
        if self.R is not None:
            return (ro >= 0) & (ro <= self.R)
        return False

    def check_t(self, t):
        if self.T is not None:
            return (t >= 0) & (t <= self.T)
        return False

    def update_arrays(self):
        if (self.R is None) | (self.T is None) | (self.countOfPoints is None):
            return
        self.ro = np.linspace(0., self.R, self.countOfPoints)
        self.t = np.linspace(0., self.T, self.countOfPoints)
        return self

    def set_count_of_points(self, numb):
        self.countOfPoints = numb
        self.update_arrays()
        return self

    def set_error(self, er):
        self.error = er
        return self

    def set_value(self, R, c, k, alp, l, T, U0):
        self.R = R
        self.c = c
        self.k = k
        self.alp = alp
        self.l = l
        self.T = T
        self.U0 = U0
        self.update_arrays()
        return self

    def func(self, ro, t, error, R, c, k, alp, l):
        omega = 0.
        if t > 0:
            n = int(math.sqrt(
                pow(R / math.pi, 2) * c * (
                            math.log((8. * R * c) / (math.pi * k * t * error)) - (2. * alp * t) / (c * l)) / (
                        k * t)) + 1)
            for mu in self.zeros[:min(n, len(self.zeros))]:
                omega += jv(1, 4. * mu / R) * jv(0, ro * mu / R) * math.exp(
                    -(k * t * (pow(mu / R, 2) + (2 * alp) / (l * k)) / c)) / (mu * pow(jv(1, mu), 2))
            return self.U0 + omega * 16 / R
        else:
            return self.U0 + (2. if ro < 4. else 0.)

    def get_func_on_t(self, t):
        #beg = time.time()
        if not self.check():
            return None
        omega = np.empty(self.countOfPoints)
        for i in range(self.countOfPoints):
            omega[i] = self.func(self.ro[i], t, self.error, self.R, self.c, self.k, self.alp, self.l)
        #print('time = ', time.time() - beg)
        return omega

    def get_func_on_ro(self, ro):
        #beg = time.time()
        if not self.check():
            return None
        omega = np.empty(self.countOfPoints)
        for i in range(self.countOfPoints):
            omega[i] = self.func(ro, self.t[i], self.error, self.R, self.c, self.k, self.alp, self.l)
        #print('time = ', time.time() - beg)
        return omega

    def get_t(self):
        return self.t

    def get_ro(self):
        return self.ro






