import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from sympy.functions.special.delta_functions import Heaviside


delta_l = 1


def A(rb):
    return 1 + (1/4 + beta(rb)/2 + rb/8*dbeta_drb(rb)) * rb**2
    

def B(rb):
    return 1/2 + 3/4*beta(rb) + 3/4*rb*dbeta_drb(rb) + rb**2/8*dbeta2_drb2(rb)


def C(rb):
    return 1/4 * (1 + 1/(1 + beta(rb)/4*rb**2)**2)


def beta(rb):
    delta = 0.1*rb + delta_l
    return (1 + delta/rb)**2 * np.log((1+delta/rb)**2) / ((1 + delta/rb)**2 - 1) - 1


def dbeta_drb(rb):
    delta = 0.1*rb + delta_l
    return 2*(delta + rb) * (delta * (delta+2*rb) - rb**2 * np.log((1+delta/rb)**2)) / (delta * rb * (delta + 2*rb)**2)


def dbeta2_drb2(rb):
    delta = 0.1*rb + delta_l
    return 2 * (delta * (np.log((1+delta/rb)**2)-4)-8*rb) / (delta + 2*rb)**3 + 2/rb**2


def electron_beam_source_old(rb, xi, N, beam_center, sz_b):
    return 4*N/((2*np.pi)**(3/2)*sz_b)*np.exp(-(xi-beam_center)**2/(2*sz_b**2))/rb**2


def electron_beam_source(xi, N, beam_center, sz_b):
    return N/((2*np.pi)**(3/2)*sz_b)*np.exp(-(xi-beam_center)**2/(2*sz_b**2))


def uniform_electrons_source(xi, beam_center):
    return (1-Heaviside(xi/beam_center-1))


def blowout_radius_ur(y, xi, beam_center, sz_b, N):
    rb, drb = y
    dy_dxi = [drb, (4*electron_beam_source(xi, N, beam_center, sz_b)/rb**2 + uniform_electrons_source(xi, b_center) - 2*drb**2 - 1)/rb]
    return dy_dxi


def blowout_radius(y, xi, beam_center, sz_b, N):
    rb, drb = y
    dy_dxi = [drb, (electron_beam_source(xi, N, beam_center, sz_b)/rb + uniform_electrons_source(xi, b_center)*rb/2 - B(rb)*rb*drb**2 -C(rb)*rb)/A(rb)]
    return dy_dxi

sr_beam = 0.1
sz_beam = np.sqrt(2)
N_beam = 10
b_center = 5


min_z = 0
max_z = 20
tspan = np.arange(min_z, max_z, sz_beam/1000)
# plt.plot(tspan, electron_beam_source(tspan, N_beam, b_center, sz_beam))
# plt.show()
# sol = odeint(blowout_radius_ur, [0.05, 0], tspan, args=(b_center, sz_beam, N_beam))
sol = odeint(blowout_radius, [0.05, 0], tspan, args=(b_center, sz_beam, N_beam))


"""Plotting"""
plt.plot(tspan, sol[:, 0])
plt.plot(tspan, -sol[:, 0])
plt.show()

