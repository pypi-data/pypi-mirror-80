from time import time
from copy import copy
import numpy as np
import scipy.constants as ct
from numba import njit, prange
import matplotlib
# np.seterr(all='raise')
# matplotlib.use('Qt5agg')
import matplotlib.pyplot as plt
import scipy.interpolate as scint
import aptools.plasma_accel.general_equations as ge


def evolve_plasma_rk4(r, pr, q, xi, dxi, xi_d, n_d, sz_d, sr_d, a_0, w_0, tau, xi_c):
    Ar, Apr = dxi*equations_of_motion(xi, r, pr, q, xi_d, n_d, sz_d, sr_d, a_0, w_0, tau, xi_c)
    Br, Bpr = dxi*equations_of_motion(xi+dxi/2, r + Ar/2, pr + Apr/2, q, xi_d, n_d, sz_d, sr_d, a_0, w_0, tau, xi_c)
    Cr, Cpr = dxi*equations_of_motion(xi+dxi/2, r + Br/2, pr + Bpr/2, q, xi_d, n_d, sz_d, sr_d, a_0, w_0, tau, xi_c)
    Dr, Dpr = dxi*equations_of_motion(xi+dxi, r + Cr, pr + Cpr, q, xi_d, n_d, sz_d, sr_d, a_0, w_0, tau, xi_c)
    r += 1/6*(Ar + 2*Br + 2*Cr + Dr)
    pr += 1/6*(Apr + 2*Bpr + 2*Cpr + Dpr)

    
    idx_neg = np.where(r < 0)
    r[idx_neg] *= -1
    pr[idx_neg] *= -1

    return r, pr


def equations_of_motion(xi, r_p, pr_p, q_p, xi_d, n_d, sz_d, sr_d, a_0, w_0, tau, xi_c):
    r_p= r_p.copy()
    pr_p = pr_p.copy()
    idx_neg = np.where(r_p < 0)
    r_p[idx_neg] *= -1
    pr_p[idx_neg] *= -1
    
    nabla_a = laser_source(xi, r_p, a_0, w_0, tau, xi_c)
    b_theta_0_p = b_theta_0_driver(xi, r_p, xi_d, n_d, sz_d, sr_d)
    psi_p, dr_psi_p, dxi_psi_p = calculate_psi_and_derivatives_at_particles(r_p, pr_p, q_p)
    # psi_p_o, dr_psi_p_o, dxi_psi_p_o = calculate_psi_and_derivatives_at_particles_old(r_p, pr_p, q_p)
    # b_theta_bar_p = calculate_b_theta_bar_at_particles(r_p, pr_p, q_p, gamma_p, psi_p, dr_psi_p, dxi_psi_p, b_theta_0_p)
    a2 = laser_a2(xi, r_p, a_0, w_0, tau, xi_c)
    gamma_p = (1 + pr_p**2 + a2 + (1+psi_p)**2)/(2*(1+psi_p))
    b_theta_bar_p = calculate_plasma_fields_at_particles(r_p, pr_p, q_p, gamma_p, psi_p, dr_psi_p, dxi_psi_p, b_theta_0_p, nabla_a)
    dpr = gamma_p * dr_psi_p / (1 + psi_p) - b_theta_bar_p - b_theta_0_p - nabla_a / (2 * (1 + psi_p))
    dr = pr_p / (1 + psi_p)

    return np.vstack((dr, dpr))


# @njit()
def psi(r_part, q_part, r_vals):
    psi_vals = np.zeros_like(r_vals)
    for i in range(len(r_vals)):
        r_curr = r_vals[i]
        sum_i = np.where(r_part < r_curr)
        r_i = r_part[sum_i]
        q_i = q_part[sum_i]
        psi_vals[i] = np.sum(q_i * np.log(r_curr/r_i)) - r_curr**2/4
    psi_vals = psi_vals - np.sum(q_part * np.log(r_part[-1]/r_part)) + r_part[-1]**2/4
    return psi_vals


# @njit()
def dr_psi(r_part, q_part, r_vals):
    dr_psi_vals = np.zeros_like(r_vals)
    for i in range(len(r_vals)):
        r_curr = r_vals[i]
        sum_i = np.where(r_part < r_curr)
        q_i = q_part[sum_i]
        dr_psi_vals[i] = np.sum(q_i)/r_curr - r_curr/2
    return dr_psi_vals


# @njit()
def dxi_psi(r_part, pr_part, q_part, psi_part, r_vals):
    dxi_psi_vals = np.zeros_like(r_vals)
    for i in range(r_vals.shape[0]):
        r_curr = r_vals[i]
        idx = np.where(r_part < r_curr)
        r_i = r_part[idx]
        pr_i = pr_part[idx]
        q_i = q_part[idx]
        psi_i = psi_part[idx]
        dxi_psi_vals[i] = - np.sum((q_i * pr_i) / (r_i * (1+psi_i)))
    dxi_psi_vals += np.sum((q_part * pr_part) / (r_part * (1+psi_part)))
    return dxi_psi_vals


def calculate_fields_at_mesh(xi, r_vals, r_p, pr_p, q_p, xi_d, n_d, sz_d, sr_d, a_0, w_0, tau, xi_c):
    nabla_a = laser_source(xi, r_p, a_0, w_0, tau, xi_c)
    b_theta_0_p = b_theta_0_driver(xi, r_p, xi_d, n_d, sz_d, sr_d)
    psi_p, dr_psi_p, dxi_psi_p = calculate_psi_and_derivatives_at_particles(r_p, pr_p, q_p)
    a2 = laser_a2(xi, r_p, a_0, w_0, tau, xi_c)
    gamma_p = (1 + pr_p**2 + a2/2 + (1+psi_p)**2)/(2*(1+psi_p))
    psi_vals, dr_psi_vals, dxi_psi_vals = calculate_psi_and_derivatives_at_mesh(r_vals, r_p, pr_p, q_p)
    b_theta_bar_vals = calculate_plasma_fields_at_mesh(r_vals, r_p, pr_p, q_p, gamma_p, psi_p, dr_psi_p, dxi_psi_p, b_theta_0_p, nabla_a)
    b_theta_0_vals = b_theta_0_driver(xi, r_vals, xi_d, n_d, sz_d, sr_d)
    
    return psi_vals, dr_psi_vals, dxi_psi_vals, b_theta_bar_vals, b_theta_0_vals


@njit()
def calculate_psi_and_derivatives_at_mesh(r_vals, r_part, pr_part, q_part):
    n_part = r_part.shape[0]
    n_points = r_vals.shape[0]

    psi_part = np.zeros(n_part)
    psi_vals = np.zeros(n_points)
    dr_psi_vals = np.zeros(n_points)
    dxi_psi_vals = np.zeros(n_points)

    sum_1_arr = np.zeros(n_part)
    sum_2_arr = np.zeros(n_part)
    sum_3_arr = np.zeros(n_part)

    sum_1 = 0.
    sum_2 = 0.
    sum_3 = 0.

    # Calculate sum_1, sum_2 and psi_part.
    idx = np.argsort(r_part)
    for i_sort in range(n_part):
        i = idx[i_sort]
        r_i = r_part[i]
        pr_i = pr_part[i]
        q_i = q_part[i]

        sum_1 += q_i
        sum_2 += q_i * np.log(r_i)
        sum_1_arr[i] = sum_1
        sum_2_arr[i] = sum_2
        psi_part[i] = sum_1*np.log(r_i) - sum_2 - r_i**2/4.
    r_N = r_part[-1]
    psi_part += - (sum_1*np.log(r_N) - sum_2 - r_N**2/4.)

    # Calculate sum_3.
    for i_sort in range(n_part):
        i = idx[i_sort]
        r_i = r_part[i]
        pr_i = pr_part[i]
        q_i = q_part[i]
        psi_i = psi_part[i]

        sum_3 += (q_i * pr_i) / (r_i * (1+psi_i))
        sum_3_arr[i] = sum_3

    # Calculate fields at r_vals
    i_comp = 0
    for i in range(n_points):
        r = r_vals[i]
        for i_sort in range(n_part):
            i_p = idx[i_sort]
            r_i = r_part[i_p]
            i_comp = i_sort
            if r_i >= r:
                i_comp -= 1
                break
        # calculate fields
        if i_comp == -1:
            psi_vals[i] = - r**2/4.
            dr_psi_vals[i] = - r/2.
            dxi_psi_vals[i] = 0.
        else:
            i_p = idx[i_comp]
            psi_vals[i] = sum_1_arr[i_p]*np.log(r) - sum_2_arr[i_p] - r**2/4.
            dr_psi_vals[i] = sum_1_arr[i_p] / r - r/2.
            dxi_psi_vals[i] = - sum_3_arr[i_p]
    psi_vals = psi_vals - (sum_1*np.log(r_N) - sum_2 - r_N**2/4.)
    dxi_psi_vals = dxi_psi_vals + sum_3

    return psi_vals, dr_psi_vals, dxi_psi_vals


@njit()
def calculate_psi_and_derivatives_at_particles(r_part, pr_part, q_part):
    n_part = r_part.shape[0]
    psi_vals = np.zeros(n_part)
    dr_psi_vals = np.zeros(n_part)
    dxi_psi_vals = np.zeros(n_part)

    sum_1 = 0.
    sum_2 = 0.
    sum_3 = 0.

    # Calculate psi and dr_psi.
    idx = np.argsort(r_part)
    for i_sort in range(n_part):
        i = idx[i_sort]
        r_i = r_part[i]
        pr_i = pr_part[i]
        q_i = q_part[i]

        sum_1_new = sum_1 + q_i
        sum_2_new = sum_2 + q_i * np.log(r_i)
        # psi_im1 = sum_1*np.log(r_i) - sum_2 - r_i**2/4.
        # psi_i = sum_1_new*np.log(r_i) - sum_2_new - r_i**2/4.

        psi_vals[i] = ((sum_1 + sum_1_new)*np.log(r_i) - (sum_2+sum_2_new))/2 - r_i**2/4.
        # psi_vals[i] = (psi_im1 + psi_i) / 2.
        dr_psi_vals[i] = (sum_1 + sum_1_new) / (2.*r_i) - r_i/2.

        sum_1 = sum_1_new
        sum_2 = sum_2_new
    r_N = r_part[-1]
    psi_vals = psi_vals - (sum_1*np.log(r_N) - sum_2 - r_N**2/4.)

    # Calculate dxi_psi.
    for i_sort in range(n_part):
        i = idx[i_sort]
        r_i = r_part[i]
        pr_i = pr_part[i]
        q_i = q_part[i]
        psi_i = psi_vals[i]

        sum_3_new = sum_3 + (q_i * pr_i) / (r_i * (1+psi_i))
        dxi_psi_vals[i] = -(sum_3 + sum_3_new) / 2.
        sum_3 = sum_3_new

    dxi_psi_vals = dxi_psi_vals + sum_3
    return psi_vals, dr_psi_vals, dxi_psi_vals


@njit()
def calculate_plasma_fields_at_particles(r_p, pr_p, q_p, gamma_p, psi_p, dr_psi_p, dxi_psi_p, b_driver, nabla_a):
    """
    New calculation of plasma fields.

    Write a_i and b_i as linear system of a_0:

    a_i = K_i * a_0 + O_i
    b_i = U_i * a_0 + P_i


    Where:

    K_i = (1 + A_i*r_i/2) * K_im1  +  A_i/(2*r_i)     * U_im1
    U_i = (-A_i*r_i**3/2) * K_im1  +  (1 - A_i*r_i/2) * U_im1

    O_i = (1 + A_i*r_i/2) * O_im1  +  A_i/(2*r_i)     * P_im1  +  (2*Bi + Ai*Ci)/4
    P_i = (-A_i*r_i**3/2) * O_im1  +  (1 - A_i*r_i/2) * P_im1  +  r_i*(4*Ci - 2*Bi*r_i - Ai*Ci*r_i)/4

    With initial conditions:

    K_0 = 1
    U_0 = 0

    O_0 = 0
    P_0 = 0

    Then a_0 can be determined by imposing a_N = 0:

    a_N = K_N * a_0 + O_N = 0 <=> a_0 = - O_N / K_N

    """
    n_part = r_p.shape[0]

    # Preallocate arrays
    K = np.zeros(n_part)
    U = np.zeros(n_part)
    O = np.zeros(n_part)
    P = np.zeros(n_part)

    # Establish initial conditions (K_0 = 1, U_0 = 0, O_0 = 0, P_0 = 0)
    K_im1 = 1.
    U_im1 = 0.
    O_im1 = 0.
    P_im1 = 0.

    # Iterate over particles
    idx = np.argsort(r_p)
    for i_sort in range(n_part):
        i = idx[i_sort]
        r_i = r_p[i]
        pr_i = pr_p[i]
        q_i = q_p[i]
        gamma_i = gamma_p[i]
        psi_i = psi_p[i]
        dr_psi_i = dr_psi_p[i]
        dxi_psi_i = dxi_psi_p[i]
        b_theta_0 = b_driver[i]
        nabla_a_i = nabla_a[i]

        a = 1. + psi_i
        a2 = a*a
        a3 = a2*a
        b = 1. / (r_i * a)
        c = 1. / (r_i * a2)
        pr_i2 = pr_i * pr_i

        A_i = q_i * b
        B_i = q_i * (- (gamma_i * dr_psi_i) * c
                     + (pr_i2 * dr_psi_i) / (r_i * a3)
                     + (pr_i * dxi_psi_i) * c
                     + pr_i2 / (r_i*r_i * a2)
                     + b_theta_0 * b
                     + nabla_a_i * c / 2.)
        C_i = q_i * (pr_i2 * c - (gamma_i/a - 1.)/ r_i)
        
        l_i = (1. + A_i*r_i/2.)
        m_i = A_i/(2.*r_i)
        n_i = (-A_i*r_i**3/2.)
        o_i = (1. - A_i*r_i/2.)

        K_i = l_i*K_im1 + m_i*U_im1
        U_i = n_i*K_im1 + o_i*U_im1
        O_i = l_i*O_im1 + m_i*P_im1 + (2.*B_i + A_i*C_i)/4.
        P_i = n_i*O_im1 + o_i*P_im1 + r_i*(4.*C_i - 2.*B_i*r_i - A_i*C_i*r_i)/4.

        K[i] = K_i
        U[i] = U_i
        O[i] = O_i
        P[i] = P_i

        K_im1 = K_i
        U_im1 = U_i
        O_im1 = O_i
        P_im1 = P_i

    a_0 = - O_im1 / K_im1

    a_i = K * a_0 + O
    b_i = U * a_0 + P

    # b_theta_bar = a_i * r_p + b_i / r_p

    a_im1 = a_0
    b_im1 = 0.
    a_i_avg = np.zeros(n_part)
    b_i_avg = np.zeros(n_part)
    for i_sort in range(n_part):
        i = idx[i_sort]
        a_i_avg[i] = (a_i[i] + a_im1) / 2.
        b_i_avg[i] = (b_i[i] + b_im1) / 2.
        a_im1 = a_i[i]
        b_im1 = b_i[i]

    b_theta_bar = a_i_avg * r_p + b_i_avg / r_p
    return b_theta_bar        


@njit()
def calculate_plasma_fields_at_mesh(r_vals, r_p, pr_p, q_p, gamma_p, psi_p, dr_psi_p, dxi_psi_p, b_driver, nabla_a):
    n_part = r_p.shape[0]
    n_points = r_vals.shape[0]

    # Preallocate arrays
    b_theta_mesh = np.zeros(n_points)
    K = np.zeros(n_part)
    U = np.zeros(n_part)
    O = np.zeros(n_part)
    P = np.zeros(n_part)

    # Establish initial conditions (K_0 = 1, U_0 = 0, O_0 = 0, P_0 = 0)
    K_im1 = 1.
    U_im1 = 0.
    O_im1 = 0.
    P_im1 = 0.

    # Iterate over particles
    idx = np.argsort(r_p)
    for i_sort in range(n_part):
        i = idx[i_sort]
        r_i = r_p[i]
        pr_i = pr_p[i]
        q_i = q_p[i]
        gamma_i = gamma_p[i]
        psi_i = psi_p[i]
        dr_psi_i = dr_psi_p[i]
        dxi_psi_i = dxi_psi_p[i]
        b_theta_0 = b_driver[i]
        nabla_a_i = nabla_a[i]

        a = 1. + psi_i
        a2 = a*a
        a3 = a2*a
        b = 1. / (r_i * a)
        c = 1. / (r_i * a2)
        pr_i2 = pr_i * pr_i

        A_i = q_i * b
        B_i = q_i * (- (gamma_i * dr_psi_i) * c
                     + (pr_i2 * dr_psi_i) / (r_i * a3)
                     + (pr_i * dxi_psi_i) * c
                     + pr_i2 / (r_i*r_i * a2)
                     + b_theta_0 * b
                     + nabla_a_i * c / 2.)
        C_i = q_i * (pr_i2 * c - (gamma_i/a - 1.)/ r_i)
        
        l_i = (1. + A_i*r_i/2.)
        m_i = A_i/(2.*r_i)
        n_i = (-A_i*r_i**3/2.)
        o_i = (1. - A_i*r_i/2.)

        K_i = l_i*K_im1 + m_i*U_im1
        U_i = n_i*K_im1 + o_i*U_im1
        O_i = l_i*O_im1 + m_i*P_im1 + (2.*B_i + A_i*C_i)/4.
        P_i = n_i*O_im1 + o_i*P_im1 + r_i*(4.*C_i - 2.*B_i*r_i - A_i*C_i*r_i)/4.

        K[i] = K_i
        U[i] = U_i
        O[i] = O_i
        P[i] = P_i

        K_im1 = K_i
        U_im1 = U_i
        O_im1 = O_i
        P_im1 = P_i

    a_0 = - O_im1 / K_im1

    a_i = K * a_0 + O
    b_i = U * a_0 + P


    # Calculate fields at r_vals
    i_comp = 0
    for i in range(n_points):
        r = r_vals[i]
        for i_sort in range(n_part):
            i_p = idx[i_sort]
            r_i = r_p[i_p]
            i_comp = i_sort
            if r_i >= r:
                i_comp -= 1
                break
        # calculate fields
        if i_comp == -1:
            b_theta_mesh[i] = a_0 * r
        else:
            i_p = idx[i_comp]
            b_theta_mesh[i] = a_i[i_p] * r + b_i[i_p] / r

    return b_theta_mesh

# @njit()
def b_theta_0_driver(xi, r, xi_d, n_d, sz_d, sr_d):
    if xi > 10:
        return 0. * r
    else:
        # exp_term = np.where( r < 100*sr_d**2, np.exp(-r**2/(2*sr_d**2)), 0)
        exponent = np.where( r**2 < 10*sr_d**2, -r**2/(2*sr_d**2), -10*sr_d**2/(2*sr_d**2))
        b_d = (- n_d * np.exp(-(xi-xi_d)**2/(2*sz_d**2)) * sr_d**2/r * (1 - np.exp(exponent)))
                # - 0*25.2 * np.exp(-(xi-6.5)**2/(2*0.3**2)) * 0.1**2/r * (1 - np.exp(-r**2/(2*0.1**2))))
        # b_d = np.where( (r > 1) , 0, b_d)
        return b_d


def b_theta_0_driver_dist(xi, r, r_max, xi_min, xi_max, n_r, n_xi, n_p):
    from wake_t.utilities.bunch_generation import get_gaussian_bunch_from_size
    s_d = ge.plasma_skin_depth(n_p/1e6)
    bunch = get_gaussian_bunch_from_size(1e-6, 1e-6, 1e-6, 1e-6, 100, 0.1, 30, 0, 10, 1e4)
    r_part = np.sqrt(bunch.x**2 + bunch.y**2) / s_d
    x_edges = np.linspace(xi_min, xi_max, n_xi)
    y_edges = np.linspace(0, r_max, n_r)
    bins = [x_edges, y_edges]
    dr = y_edges[1]-y_edges[0]
    dxi = x_edges[1]-x_edges[0]
    bunch_hist, *_ = np.histogram2d(bunch.xi / s_d, r_part, bins=bins, weights=bunch.q/ct.e/(2*np.pi*dr*dxi*s_d**3*n_p))#*r_part))
    r_b = y_edges[1:] - dr/2
    xi_b = x_edges[1:] - dxi/2
    bunch_rint = np.cumsum(bunch_hist, axis=1)/r_b * dr
    f = scint.interp2d(r_b, xi_b, -bunch_rint)
    return f(r, xi, assume_sorted=True)
    # plt.imshow(bunch_rint)
    # plt.show()

# @njit()
def laser_source(xi, r, a_0, w_0, tau, xi_c):
    if a_0 == 0:
        return np.zeros_like(r)
    else:
        s_r = w_0 / np.sqrt(2)
        s_z = tau / (2*np.sqrt(2*np.log(2))) * np.sqrt(2)
        return - a_0**2 * r / s_r**2 * (np.exp(-(r)**2/(s_r**2)) * np.exp(-(xi-xi_c)**2/(s_z**2)))
    # return np.zeros_like(r)


# @njit()
def laser_a2(xi, r, a_0, w_0, tau, xi_c):
    if a_0 == 0:
        return np.zeros_like(r)
    else:
        s_r = w_0 / np.sqrt(2)
        s_z = tau / (2*np.sqrt(2*np.log(2))) * np.sqrt(2)
        return a_0**2/2 * (np.exp(-(r)**2/(s_r**2)) * np.exp(-(xi-xi_c)**2/(s_z**2)))
    # return np.zeros_like(r)


def calculate_wakefield(laser_params, beam_params, r_max, xi_max, n_part, nr, dxi):
    # Laser and beam parameters
    a_0, w_0, tau, xi_c = laser_params
    n_d, sr_d, sz_d, xi_d = beam_params

    # Initialize plasma particles
    dr = r_max / n_part
    r_part = np.linspace(dr, r_max, n_part)
    # dr = r_part[1] - r_part[0]
    pr_part = np.zeros_like(r_part)
    gamma_part = np.ones_like(r_part)
    q_part = dr*r_part

    # iteration steps
    steps = int(xi_max / dxi)

    # Initialize particle and field arrays
    r_all = copy(r_part)
    q_all = copy(q_part)
    xi_all = np.zeros(n_part)
    psi_mesh = np.zeros((nr+1, steps))
    dr_psi_mesh = np.zeros((nr+1, steps))
    dxi_psi_mesh = np.zeros((nr+1, steps))
    b_theta_bar_mesh = np.zeros((nr+1, steps))
    b_theta_0_mesh = np.zeros((nr+1, steps))
    r_mesh = np.linspace(0, r_max, nr+1)

    # Main loop
    t0 = time()
    for step in np.arange(steps):
        print(step)
        xi = dxi*(step+1)
        # plt.plot(np.ones_like(r_part)*xi, r_part, '.', ms=0.5)
        r_part, pr_part = evolve_plasma_rk4(r_part, pr_part, q_part, xi, dxi, xi_d, n_d, sz_d, sr_d, a_0, w_0, tau, xi_c)
        if step == 0:
            t_comp = time() - t0
        idx_keep = np.where(r_part<=r_max+0.1)
        r_part = r_part[idx_keep]
        pr_part = pr_part[idx_keep]
        gamma_part = gamma_part[idx_keep]
        q_part = q_part[idx_keep]
        
        r_all = np.append(r_all, r_part)
        q_all = np.append(q_all, q_part)
        xi_all = np.append(xi_all, np.ones(len(r_part))*xi)
        psi_mesh[:,step], dr_psi_mesh[:,step], dxi_psi_mesh[:,step], b_theta_bar_mesh[:,step], b_theta_0_mesh[:,step] = calculate_fields_at_mesh(xi, r_mesh, r_part, pr_part, q_part, xi_d, n_d, sz_d, sr_d, a_0, w_0, tau, xi_c)
    dr = r_max / nr
    dr_psi_mesh, dxi_psi_mesh = np.gradient(psi_mesh, dr, dxi)
    e_r_mesh = b_theta_bar_mesh +  b_theta_0_mesh - dr_psi_mesh
    n_p = np.gradient(np.vstack(r_mesh) * e_r_mesh, dr, axis=0, edge_order=2)/np.vstack(r_mesh) - np.gradient(dxi_psi_mesh, dxi, axis=1) - 1
    k_r_mesh = np.gradient(dr_psi_mesh, dr, axis=0, edge_order=2)
    t_tot = time() - t0
    print(t_comp)
    print(t_tot - t_comp)
    print(t_tot)

    return n_p, dr_psi_mesh, dxi_psi_mesh, k_r_mesh, psi_mesh


def test_fields():
    # laser driver
    a_0 = 3
    w_0 = 2
    tau = 2
    xi_c = 3

    # beam driver
    xi_d = 3
    n_d = 0
    sr_d = 0.1
    sz_d = 1

    # plasma particles
    r_max = 10
    r_p = np.linspace(0, 4, 800)[1:]
    dr = r_p[1] - r_p[0]
    pr_p = np.zeros_like(r_p)
    gamma_p = np.ones_like(r_p)
    q_p = dr*r_p

    # calculate potential
    t0 = time()
    b_driver_p = b_theta_0_driver(0, r_p, xi_d, n_d, sz_d, sr_d)
    for i in range(100):
        # psi_i = psi(r_p, q_p, r_p)
        # dr_psi_i = dr_psi(r_p, q_p, r_p)
        psi_p, dr_psi_p, dxi_psi_p = calculate_psi_and_derivatives_at_particles(r_p, pr_p, q_p)
        b_theta_bar = calculate_b_theta_bar_at_particles(r_p, pr_p, q_p, gamma_p, psi_p, dr_psi_p, dxi_psi_p, b_driver_p)
    print(time() - t0)
    plt.plot(r_p, psi_p)
    plt.plot(r_p, dr_psi_p)
    plt.plot(r_p, dxi_psi_p)
    plt.plot(r_p, b_theta_bar)
    plt.show()


def test_rk():
    # laser driver
    a_0 = 0
    w_0 = 2
    tau = 2
    xi_c = 3

    # beam driver
    xi_d = 3.4
    n_d = 3.78
    sr_d = 0.4
    sz_d = 1

    # plasma particles
    r_max = 4.1
    r_part = np.linspace(0, 4, 400)[1:]
    dr = r_part[1] - r_part[0]
    pr_part = np.zeros_like(r_part)
    gamma_part = np.ones_like(r_part)
    q_part = dr*r_part
    p_idx = np.arange(len(r_part))

    # steps
    dxi = 0.05
    steps = 200


    i_track = 30
    r_track = np.zeros(steps)

    n_part = len(r_part)

    r_all = copy(r_part)
    q_all = copy(q_part)
    xi_all = np.zeros(n_part)

    psi_mesh = np.zeros((400, steps))
    dr_psi_mesh = np.zeros((400, steps))
    dxi_psi_mesh = np.zeros((400, steps))
    b_theta_bar_mesh = np.zeros((400, steps))
    b_theta_0_mesh = np.zeros((400, steps))

    psi_mesh_o = np.zeros((400, steps))
    dr_psi_mesh_o = np.zeros((400, steps))
    dxi_psi_mesh_o = np.zeros((400, steps))

    a2_mesh = np.zeros((400, steps))
    
    t0 = time()
    for step in np.arange(steps):
        print(step)
        xi = dxi*(step+1)
        # plt.plot(np.ones_like(r_part)*xi, r_part, '.', ms=0.5)
        r_part, pr_part = evolve_plasma_rk4(r_part, pr_part, q_part, xi, dxi, xi_d, n_d, sz_d, sr_d, a_0, w_0, tau, xi_c)
        if step == 0:
            t_comp = time() - t0
        idx_keep = np.where(r_part<=r_max)
        r_part = r_part[idx_keep]
        pr_part = pr_part[idx_keep]
        gamma_part = gamma_part[idx_keep]
        q_part = q_part[idx_keep]
        # r_part, idx = np.unique(r_part, return_index=True)
        # pr_part = pr_part[idx]
        # gamma_part = gamma_part[idx]
        # p_idx = p_idx[idx]
        # q_part = q_part[idx]
        r_all = np.append(r_all, r_part)
        q_all = np.append(q_all, q_part)
        xi_all = np.append(xi_all, np.ones(len(r_part))*xi)
        # for i, r in enumerate(np.linspace(0, 4, 200)):
        # psi_mesh_o[:,step] = psi(r_part, q_part, np.linspace(0, 4, 400))
        # psi_mesh[:,step], dr_psi_mesh[:,step], dxi_psi_mesh[:,step] = calculate_psi_and_derivatives_at_mesh(np.linspace(0, 4, 400), r_part, pr_part, q_part)
        # dr_psi_mesh_o[:,step] = dr_psi(r_part, q_part, np.linspace(0.01, 4, 400))
        a2_mesh[:,step] = laser_a2(xi, np.linspace(0, 4, 400), a_0, w_0, tau, xi_c)
        # psi_part, *_ = calculate_psi_and_derivatives_at_particles(r_part, pr_part, q_part)
        # dxi_psi_mesh_o[:,step] = dxi_psi(r_part, pr_part, q_part, psi_part, np.linspace(0, 4, 400))
        # r_track[step] = r_part[np.where(p_idx==i_track)]
        psi_mesh[:,step], dr_psi_mesh[:,step], dxi_psi_mesh[:,step], b_theta_bar_mesh[:,step], b_theta_0_mesh[:,step] = calculate_fields_at_mesh(xi, np.linspace(0.01, 4, 400), r_part, pr_part, q_part, xi_d, n_d, sz_d, sr_d, a_0, w_0, tau, xi_c)
    # plt.ylim((0, 2))
    # plt.plot(r_track)
    # plt.plot(xi_all, r_all, '.', ms=0.5)
    # plt.hist2d(xi_all, r_all, 100, weights=q_all/r_all)
    t_tot = time() - t0
    print(t_comp)
    print(t_tot - t_comp)
    print(t_tot)
    dr = 4 / 400
    dr_psi_mesh, dxi_psi_mesh = np.gradient(psi_mesh, dr, dxi)
    e_r_mesh = b_theta_bar_mesh +  b_theta_0_mesh - dr_psi_mesh
    n_p = np.gradient(np.vstack(np.linspace(0.01, 4, 400) ) * e_r_mesh, dr, axis=0)/np.vstack(np.linspace(0.01, 4, 400) ) - np.gradient(dxi_psi_mesh, dxi, axis=1)

    # n_p = (1 + a2_mesh/2 + (1+psi_mesh)**2)/(2*(1+psi_mesh)**2)
    plt.subplot(221)
    # plt.imshow(psi_mesh, aspect='auto')
    plt.plot(xi_all, r_all, '.', ms=0.5)
    plt.subplot(222)
    plt.imshow(np.gradient(psi_mesh, dxi)[1], aspect='auto', cmap='RdBu')
    # plt.imshow(dxi_psi_mesh_o, aspect='auto', cmap='RdBu')
    # plt.imshow(dr_psi_mesh, aspect='auto', cmap='RdBu')
    plt.subplot(223)
    # plt.plot(np.gradient(psi_mesh, dxi)[1][0])
    # plt.plot(dxi_psi_mesh[0])
    plt.plot(dr_psi_mesh[:,50])
    plt.plot(np.gradient(psi_mesh)[0][:,50]*100)
    # plt.plot(n_p[:,50])
    # plt.plot(np.gradient(psi_mesh)[0][:,50])
    plt.subplot(224)
    plt.imshow(n_p, aspect='auto', vmax=1, vmin=-1)
    # plt.imshow(np.gradient(psi_mesh, dxi)[1], aspect='auto', cmap='RdBu', vmax=2, vmin=-2)
    # plt.imshow(dxi_psi_mesh, aspect='auto', cmap='RdBu', vmax=2, vmin=-2)
    # plt.imshow(b_theta_bar_mesh)
    plt.show()


def test_si_units():
    n_p_0 = 1e17
    s_d = ge.plasma_skin_depth(n_p_0)
    E_0 = ge.plasma_cold_non_relativisct_wave_breaking_field(n_p_0)

    # laser driver
    a_0 = 2.2
    w_0 = 24.e-6
    tau = 27e-15 * ct.c
    xi_c = 0

    # electron beam
    Q = 50e-12
    sr_d = 1e-6
    sz_d = 10e-6
    I_p = Q / (np.sqrt(2*np.pi)*sz_d/ct.c)#0e3 # A
    xi_d = xi_c + 40e-6

    r_max = 3 * s_d
    xi_max = 8 * s_d
    nr = 400
    dxi = 0.05 * s_d
    n_part = 1000

    # Convert to plasma units
    w_0 /= s_d
    tau /= s_d
    xi_c /= s_d
    n_d = I_p / (2*np.pi*ct.c*ct.e*sr_d**2*n_p_0*1e6)
    sr_d /= s_d
    sz_d /= s_d
    xi_d /= s_d
    dxi /= s_d
    xi_max /= s_d
    r_max /= s_d

    laser_params = [a_0, w_0, tau, xi_c]
    beam_params = [n_d, sr_d, sz_d, xi_d]

    n_p, dr_psi_mesh, dxi_psi_mesh = calculate_wakefield(laser_params, beam_params, r_max, xi_max, n_part, nr, dxi)

    plt.subplot(221)
    plt.imshow(n_p, aspect='auto', vmax=0, vmin=-3)
    plt.subplot(222)
    plt.imshow(dxi_psi_mesh, aspect='auto', cmap='RdBu')
    plt.subplot(223)
    plt.imshow(dr_psi_mesh, aspect='auto', cmap='RdBu')
    plt.subplot(224)
    plt.plot(dxi_psi_mesh[0]*E_0)
    plt.show()


def p_lens_p4():
    n_p_0 = 1e17
    s_d = ge.plasma_skin_depth(n_p_0)
    E_0 = ge.plasma_cold_non_relativisct_wave_breaking_field(n_p_0)
    w_p = ge.plasma_frequency(n_p_0)

    # laser driver
    a_0 = 0
    w_0 = 24.e-6
    tau = 27e-15 * ct.c
    xi_c = s_d

    # electron beam
    Q = 50e-12
    sr_d = 100e-6
    sz_d = 1e-6
    I_p = Q / (np.sqrt(2*np.pi)*sz_d/ct.c)#0e3 # A
    xi_d = 10e-6

    r_max = 400e-6
    xi_max = 100e-6
    nr = 400
    dxi = 0.01 * s_d
    n_part = 2000

    # Convert to plasma units
    w_0 /= s_d
    tau /= s_d
    xi_c /= s_d
    n_d = I_p / (2*np.pi*ct.c*ct.e*sr_d**2*n_p_0*1e6)
    sr_d /= s_d
    sz_d /= s_d
    xi_d /= s_d
    dxi /= s_d
    xi_max /= s_d
    r_max /= s_d

    laser_params = [a_0, w_0, tau, xi_c]
    beam_params = [n_d, sr_d, sz_d, xi_d]

    n_p, dr_psi_mesh, dxi_psi_mesh, k_r_mesh, psi_mesh = calculate_wakefield(laser_params, beam_params, r_max, xi_max, n_part, nr, dxi)

    plt.subplot(221)
    # plt.imshow(n_p, aspect='auto')
    plt.imshow(psi_mesh, aspect='auto')
    plt.subplot(222)
    plt.imshow(dxi_psi_mesh, aspect='auto', cmap='RdBu')
    plt.subplot(223)
    plt.imshow(k_r_mesh*w_p**2*ct.m_e/ct.e/ct.c, aspect='auto', cmap='RdBu')
    # plt.plot(k_r_mesh[3]*w_p**2*ct.m_e/ct.e/ct.c)
    plt.subplot(224)
    plt.imshow(dr_psi_mesh, aspect='auto', cmap='RdBu')
    # plt.plot(dxi_psi_mesh[0]*E_0)
    plt.show()


def test_bunch_distribution():
    n_p_0 = 1e23

    Q = 10e-12
    sr_d = 1e-6
    sz_d = 30e-15*ct.c
    I_p = Q / (np.sqrt(2*np.pi)*sz_d/ct.c)# A

    # Convert to plasma units
    s_d = ge.plasma_skin_depth(n_p_0/1e6)
    n_d = I_p / (2*np.pi*ct.c*ct.e*sr_d**2*n_p_0)
    sr_d /= s_d
    sz_d /= s_d

    xi = 0
    r = np.linspace(0.0001, 4, 300)
    analytic = b_theta_0_driver(xi, r, 0, n_d, sz_d, sr_d)
    distrib = b_theta_0_driver_dist(0, r, 4, -4, 4, 300, 100, n_p_0)
    plt.plot(analytic)
    plt.plot(distrib)
    plt.show()


# test_fields()
# test_rk()
test_si_units()
# p_lens_p4()
# test_bunch_distribution()



# @njit()
# def calculate_psi_and_derivatives_at_particles_bkp(r_part, pr_part, q_part):
#     n_part = r_part.shape[0]
#     psi_vals = np.zeros_like(r_part)
#     dr_psi_vals = np.zeros_like(r_part)
#     dxi_psi_vals = np.zeros_like(r_part)

#     sum_1 = 0.
#     sum_2 = 0.
#     sum_3 = 0.

#     # Iterate over particles
#     idx = np.argsort(r_part)
#     for i_sort in range(n_part):
#         i = idx[i_sort]
#         r_i = r_part[i]
#         pr_i = pr_part[i]
#         q_i = q_part[i]

#         # sum_1 += q_i
#         # sum_2 += q_i * np.log(r_i)
#         # psi_i = sum_1*np.log(r_i) - sum_2 - r_i**2/4
#         # sum_3 += (q_i * pr_i) / (r_i * (1+psi_i))

#         # sum_1_new = sum_1 + q_i
#         # sum_2_new = sum_2 + q_i * np.log(r_i)
#         # psi_im1 = sum_1*np.log(r_i) - sum_2 - r_i**2/4.
#         # psi_i = sum_1_new*np.log(r_i) - sum_2_new - r_i**2/4.
#         # sum_3_new = sum_3 + (q_i * pr_i) / (r_i * (1+psi_i))

#         # psi_vals[i] = (psi_im1 + psi_i) / 2.
#         # dr_psi_vals[i] = (sum_1 + sum_1_new) / (2.*r_i) - r_i/2.
#         # dxi_psi_vals[i] = -(sum_3 + sum_3_new) / 2.

#         sum_1_new = sum_1 + q_i
#         sum_2_new = sum_2 + q_i * np.log(r_i)
#         psi_i = sum_1_new*np.log(r_i) - sum_2_new - r_i**2/4.
        

#         psi_vals[i] = psi_i
#         dr_psi_vals[i] = sum_1_new / r_i - r_i/2.

#         sum_1 = sum_1_new
#         sum_2 = sum_2_new
#     r_N = r_part[-1]
#     psi_vals = psi_vals - (sum_1*np.log(r_N) - sum_2 - r_N**2/4.) # -np.sum(q_part * np.log(r_part[-1]/r_part)) + r_part[-1]**2/4

#     idx = np.argsort(r_part)
#     for i_sort in range(n_part):
#         i = idx[i_sort]
#         r_i = r_part[i]
#         pr_i = pr_part[i]
#         q_i = q_part[i]
#         psi_i = psi_vals[i]

#         sum_3_new = sum_3 + (q_i * pr_i) / (r_i * (1+psi_i))
#         dxi_psi_vals[i] = - sum_3_new
#         sum_3 = sum_3_new

#     dxi_psi_vals = dxi_psi_vals + sum_3
#     return psi_vals, dr_psi_vals, dxi_psi_vals


# @njit()
# def calculate_psi_and_derivatives_at_particles_old(r_part, pr_part, q_part):
#     psi_vals = np.zeros_like(r_part)
#     psi_vals_2 = np.zeros_like(r_part)
#     dr_psi_vals = np.zeros_like(r_part)
#     dxi_psi_vals = np.zeros_like(r_part)
#     for i in prange(r_part.shape[0]):
#         r_curr = r_part[i]
#         idx = np.where(r_part < r_curr)
#         idx_p1 = np.where(r_part <= r_curr)
#         r_i = r_part[idx]
#         pr_i = pr_part[idx]
#         q_i = q_part[idx]
#         r_ip1 = r_part[idx_p1]
#         pr_ip1 = pr_part[idx_p1]
#         q_ip1 = q_part[idx_p1]

#         psi_i = np.sum(q_i * np.log(r_curr/r_i)) - r_curr**2/4
#         psi_ip1 = np.sum(q_ip1 * np.log(r_curr/r_ip1)) - r_curr**2/4
#         psi_vals[i] = (psi_i + psi_ip1) / 2
#         psi_vals_2[i] = psi_ip1
#         dr_psi_vals[i] = (np.sum(q_i)/r_curr + np.sum(q_ip1)/r_curr)/2 - r_curr/2
#         dxi_psi_vals[i] = - (np.sum((q_i * pr_i) / (r_i * (1+psi_i))) + np.sum((q_ip1 * pr_ip1) / (r_ip1 * (1+psi_ip1))))/2
#     psi_vals += -np.sum(q_part * np.log(r_part[-1]/r_part)) + r_part[-1]**2/4
#     dxi_psi_vals += np.sum((q_part * pr_part) / (r_part * (1+psi_vals_2)))
#     return psi_vals, dr_psi_vals, dxi_psi_vals


# @njit()
# def calculate_b_theta_bar_at_particles(r_p, pr_p, q_p, gamma_p, psi_p, dr_psi_p, dxi_psi_p, b_driver):
#     ai_p = 0
#     bi_p = 0
#     b_theta_bar = np.zeros_like(r_p)
#     ai_arr = np.zeros_like(r_p)
#     bi_arr = np.zeros_like(r_p)
#     test = np.zeros_like(r_p)
#     idx = np.argsort(r_p)

#     for i_sort in prange(r_p.shape[0]):
#         i = idx[i_sort]
#         r_i = r_p[i]
#         pr_i = pr_p[i]
#         q_i = q_p[i]
#         gamma_i = gamma_p[i]
#         psi_i = psi_p[i]
#         dr_psi_i = dr_psi_p[i]
#         dxi_psi_i = dxi_psi_p[i]
#         b_driver_i = b_driver[i]

#         Ai = A_i(q_i, r_i, psi_i)
#         Bi = B_i(q_i, r_i, gamma_i, pr_i, psi_i, dr_psi_i, dxi_psi_i, b_driver_i)
#         Ci = C_i(q_i, r_i, gamma_i, pr_i, psi_i)

#         ai_new = (1 + Ai*r_i/2) * ai_p + Ai/(2*r_i) * bi_p + (2*Bi + Ai*Ci)/4
#         bi_new = (- Ai*r_i**3/2 * ai_p + (1 - Ai*r_i/2) * bi_p
#                   + r_i * (4*Ci - 2*Bi*r_i - Ai*Ci*r_i) / 4)
#         ai = (ai_p + ai_new)/2
#         bi = (bi_p + bi_new)/2
#         # print(bi_p)
#         # ai = ai_new
#         # bi = bi_new
#         ai_p = ai_new
#         bi_p = bi_new
#         ai_arr[i] = ai_new
#         bi_arr[i] = bi_new
#         if i == 0:
#             test[i] = Ci
#         else:
#             test[i] = test[i-i] + Ci
#         b_theta_bar[i] = ai * r_i + bi / r_i

#     return 0.*b_theta_bar


# @njit()
# def calculate_b_theta_bar_at_particles_bkp(r_p, pr_p, q_p, gamma_p, psi_p, dr_psi_p, dxi_psi_p, b_driver):
#     ai_p = 0
#     bi_p = 0
#     b_theta_bar = np.zeros_like(r_p)

#     idx = np.argsort(r_p)

#     for i_sort in prange(r_p.shape[0]):
#         i = idx[i_sort]
#         r_i = r_p[i]
#         pr_i = pr_p[i]
#         q_i = q_p[i]
#         gamma_i = gamma_p[i]
#         psi_i = psi_p[i]
#         dr_psi_i = dr_psi_p[i]
#         dxi_psi_i = dxi_psi_p[i]
#         b_driver_i = b_driver[i]

#         Ai = A_i(q_i, r_i, psi_i)
#         Bi = B_i(q_i, r_i, gamma_i, pr_i, psi_i, dr_psi_i, dxi_psi_i, b_driver_i)
#         Ci = C_i(q_i, r_i, gamma_i, pr_i, psi_i)

#         ai_new = (1 + Ai*r_i/2) * ai_p + Ai/(2*r_i) * bi_p + (2*Bi + Ai*Ci)/4
#         bi_new = (- Ai*r_i**3/2 * ai_p + (1 - Ai*r_i/2) * bi_p
#                   + r_i * (4*Ci - 2*Bi*r_i - Ai*Ci*r_i) / 4)
#         # ai = (ai_p + ai_new)/2
#         # bi = (bi_p + bi_new)/2
#         ai = ai_p
#         bi = bi_p
#         # ai_p = ai_new
#         # bi_p = bi_new

#         b_theta_bar[i] = ai * r_i - bi / r_i

#     return b_theta_bar


# @njit()
# def calculate_b_theta_bar_at_mesh(r, r_p, pr_p, q_p, gamma_p, psi_p, dr_psi_p, dxi_psi_p, b_driver):
#     # r must be sorted
#     ai_p = 0
#     bi_p = 0
#     b_theta_bar = np.zeros_like(r)

#     idx = np.argsort(r_p)

#     for i_sort in prange(r_p.shape[0]):
#         i = idx[i_sort]
#         r_i = r_p[i]
#         pr_i = pr_p[i]
#         q_i = q_p[i]
#         gamma_i = gamma_p[i]
#         psi_i = psi_p[i]
#         dr_psi_i = dr_psi_p[i]
#         dxi_psi_i = dxi_psi_p[i]
#         b_driver_i = b_driver[i]

#         Ai = A_i(q_i, r_i, psi_i)
#         Bi = B_i(q_i, r_i, gamma_i, pr_i, psi_i, dr_psi_i, dxi_psi_i, b_driver_i)
#         Ci = C_i(q_i, r_i, gamma_i, pr_i, psi_i)

#         ai_new = (1 + Ai*r_i/2) * ai_p + Ai/(2*r_i) * bi_p + (2*Bi + Ai*Ci)/4
#         bi_new = (- Ai*r_i**3/2 * ai_p + (1 - Ai*r_i/2) * bi_p
#                   + r_i * (4*Ci - 2*Bi*r_i - Ai*Ci*r_i) / 4)
#         ai = (ai_p + ai_new)/2
#         bi = (bi_p + bi_new)/2

#         b_theta_bar[i] = ai * r_i - bi / r_i
#     return b_theta_bar


# @njit()
# def A_i(q_i, r_i, psi_i):
#     return q_i / (r_i * (1 + psi_i))


# @njit()
# def B_i(q_i, r_i, gamma_i, p_ri, psi_i, dr_psi_i, dxi_psi_i, b_theta_0):
#     return q_i * (- (gamma_i * dr_psi_i) / (r_i * (1+psi_i)**2)
#                   + (p_ri**2 * dr_psi_i) / (r_i * (1+psi_i)**3)
#                   + (p_ri * dxi_psi_i) / (r_i * (1+psi_i)**2)
#                   + (p_ri**2) / (r_i**2 * (1+psi_i)**2)
#                   + (b_theta_0) / (r_i * (1+psi_i)))


# @njit()
# def C_i(q_i, r_i, gamma_i, p_ri, psi_i):
#     return ((q_i * p_ri**2) / (r_i * (1+psi_i)**2)
#             - (q_i / r_i) * (gamma_i / (1+psi_i)-1))


# @njit()
# def A_i_old(q_i, r_i, psi_i):
#     return q_i / (r_i * (1 + psi_i))


# @njit()
# def B_i_old(q_i, r_i, gamma_i, p_ri, psi_i, dr_psi_i, dxi_psi_i, b_theta_0):
#     return (- (q_i * gamma_i * dr_psi_i) / (r_i * (1+psi_i)**2)
#             + (q_i * p_ri**2 * dr_psi_i) / (r_i * (1+psi_i)**3)
#             + (q_i * p_ri * dxi_psi_i) / (r_i * (1+psi_i)**2)
#             + (q_i * p_ri**2) / (r_i**2 * (1+psi_i)**2)
#             + (q_i * b_theta_0) / (r_i * (1+psi_i)))


# @njit()
# def C_i_old(q_i, r_i, gamma_i, p_ri, psi_i):
#     return ((q_i * p_ri**2) / (r_i * (1+psi_i)**2)
#             - (q_i / r_i) * (gamma_i / (1+psi_i)-1))
