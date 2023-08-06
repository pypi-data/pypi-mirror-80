from copy import copy
import numpy as np
import scipy.constants as ct
# np.seterr(all='raise')
import matplotlib.pyplot as plt


def A_i(q_i, r_i, psi_i):
    return q_i / (r_i * (1 + psi_i))


def B_i(q_i, r_i, gamma_i, p_ri, psi_i, dr_psi_i, dxi_psi_i, b_theta_0):
    return (- (q_i * gamma_i * dr_psi_i) / (r_i * (1+psi_i)**2)
            + (q_i * p_ri**2 * dr_psi_i) / (r_i * (1+psi_i)**3)
            + (q_i * p_ri * dxi_psi_i) / (r_i * (1+psi_i)**2)
            + (q_i * p_ri**2) / (r_i**2 * (1+psi_i)**2)
            + (q_i * b_theta_0) / (r_i * (1+psi_i)))


def C_i(q_i, r_i, gamma_i, p_ri, psi_i):
    return ((q_i * p_ri**2) / (r_i * (1+psi_i)**2)
            - (q_i / r_i) * (gamma_i / (1+psi_i)-1))


def a_i(r_i, a_im, b_im, psi_i, dr_psi_i, dxi_psi_i, b_theta_0, pr_i, q_i, gamma_i):
    A_i_val = A_i(q_i, r_i, psi_i)
    B_i_val = B_i(q_i, r_i, gamma_i, pr_i, psi_i, dr_psi_i, dxi_psi_i, b_theta_0)
    C_i_val = C_i(q_i, r_i, gamma_i, pr_i, psi_i)
    return (1 + A_i_val*r_i/2) * a_im + A_i_val/(2*r_i) * b_im + (2*B_i_val + A_i_val*C_i_val)/4


def b_i(r_i, a_im, b_im, psi_i, dr_psi_i, dxi_psi_i, b_theta_0, pr_i, q_i, gamma_i):
    A_i_val = A_i(q_i, r_i, psi_i)
    B_i_val = B_i(q_i, r_i, gamma_i, pr_i, psi_i, dr_psi_i, dxi_psi_i, b_theta_0)
    C_i_val = C_i(q_i, r_i, gamma_i, pr_i, psi_i)
    return (- A_i_val*r_i**3/2 * a_im + (1 - A_i_val*r_i/2) * b_im
            + r_i * (4*C_i_val - 2*B_i_val*r_i - A_i_val*C_i_val*r_i) / 4)


def b_theta_bar(a_i, b_i, r):
    return a_i * r - b_i / r


def b_theta_0_driver(xi, r, xi_d, n_d, sz_d, sr_d):
    return (- n_d * np.exp(-(xi-xi_d)**2/(2*sz_d**2)) * sr_d**2/r * (1 - np.exp(-r**2/(2*sr_d**2)))
            - 30.2 * np.exp(-(xi-6.5)**2/(2*0.3**2)) * 0.1**2/r * (1 - np.exp(-r**2/(2*0.1**2))))


def psi(r_part, q_part, r):
    return -delta_psi(r_part, q_part, r_part[-1]) + delta_psi(r_part, q_part, r)


def delta_psi(r_part, q_part, r):
    sum_i = np.where(r_part <= r)
    r_i = r_part[sum_i]
    q_i = q_part[sum_i]
    return np.sum(q_i * np.log(r/r_i)) - r**2/4


def dr_psi(r_part, q_part, r):
    sum_i = np.where(r_part <= r)
    q_i = q_part[sum_i]
    return np.sum(q_i)/r - r/2


def dxi_psi(r_part, pr_part, q_part, psi_part, r):
    return (dxi_delta_psi(r_part, pr_part, q_part, psi_part, r) -
            dxi_delta_psi(r_part, pr_part, q_part, psi_part, r_part[-1]))


def dxi_delta_psi(r_part, pr_part, q_part, psi_part, r):
    sum_i = np.where(r_part <= r)
    r_i = r_part[sum_i]
    p_ri = pr_part[sum_i]
    q_i = q_part[sum_i]
    psi_i = psi_part[sum_i]
    return -np.sum((q_i * p_ri) / (r_i * (1+psi_i)))


def laser_source(xi, r, a_0, w_0, tau, xi_c):
    s_r = w_0 / np.sqrt(2)
    s_z = tau / (2*np.sqrt(2*np.log(2))) * np.sqrt(2)
    return a_0**2/2 * 4 * r / s_r**2 * (np.exp(-(r)**2/(s_r**2)) * np.exp(-(xi-xi_c)**2/(s_z**2)))


def laser_a2(xi, r, a_0, w_0, tau, xi_c):
    s_r = w_0 / np.sqrt(2)
    s_z = tau / (2*np.sqrt(2*np.log(2))) * np.sqrt(2)
    return a_0**2/2 * (np.exp(-(r)**2/(s_r**2)) * np.exp(-(xi-xi_c)**2/(s_z**2)))


def evolve_plasma_rk4(r, pr, gamma, q, xi, dxi, xi_d, n_d, sz_d, sr_d, a_0, w_0, tau, xi_c):
    Ar, Apr = dxi*equations_of_motion(xi, r, pr, gamma, q, xi_d, n_d, sz_d, sr_d, a_0, w_0, tau, xi_c)
    Br, Bpr = dxi*equations_of_motion(xi+dxi/2, r + Ar/2, pr + Apr/2, gamma, q, xi_d, n_d, sz_d, sr_d, a_0, w_0, tau, xi_c)
    Cr, Cpr = dxi*equations_of_motion(xi+dxi/2, r + Br/2, pr + Bpr/2, gamma, q, xi_d, n_d, sz_d, sr_d, a_0, w_0, tau, xi_c)
    Dr, Dpr = dxi*equations_of_motion(xi+dxi, r + Cr, pr + Cpr, gamma, q, xi_d, n_d, sz_d, sr_d, a_0, w_0, tau, xi_c)
    r += 1/6*(Ar + 2*Br + 2*Cr + Dr)
    pr += 1/6*(Apr + 2*Bpr + 2*Cpr + Dpr)
    psi_p = np.zeros_like(r)
    for i, r_i in enumerate(r):
        psi_p[i] = psi(r, q, r_i)
    a2 = laser_a2(xi, r, a_0, w_0, tau, xi_c)
    gamma = (1 + pr**2 + a2/2 + (1+psi_p)**2)/(2*(1+psi_p))
    return r, pr, gamma


def equations_of_motion(xi, r, pr, gamma, q, xi_d, n_d, sz_d, sr_d, a_0, w_0, tau, xi_c):
    idx_neg = np.where(r < 0)
    r[idx_neg] *= -1
    pr[idx_neg] *= -1
    psi_p, dr_psi_p, b_theta_bar_p, b_theta_0_p, nabla_a = calculate_fields_avg(xi, r, pr, gamma, q, xi_d, n_d, sz_d, sr_d, a_0, w_0, tau, xi_c)
    dpr = gamma * dr_psi_p / (1 + psi_p) - b_theta_bar_p - b_theta_0_p + nabla_a / (4 * (1 + psi_p))
    dr = pr / (1 + psi_p)
    return np.array([dr, dpr])


def calculate_fields(xi, r_part, pr_part, gamma_part, q_part, xi_d, n_d, sz_d, sr_d):
    b_driver = b_theta_0_driver(xi, r_part, xi_d, n_d, sz_d, sr_d)
    a_i_p = 0
    b_i_p = 0
    psi_p = np.zeros_like(r_part)
    dr_psi_p = np.zeros_like(r_part)
    dxi_psi_p = np.zeros_like(r_part)
    b_plasma_p = np.zeros_like(r_part)
    for i, r in enumerate(r_part):
        psi_p[i] = psi(r_part, q_part, r)
        dr_psi_p[i] = dr_psi(r_part, q_part, r)
        dxi_psi_p[i] = dxi_psi(r_part, pr_part, q_part, psi_p, r)
        # if i == len(r_part)-1:
        #     a_i_new = 0
        # else:
        a_i_new = a_i(r, a_i_p, b_i_p, psi_p[i], dr_psi_p[i], dxi_psi_p[i], b_driver[i], pr_part[i], q_part[i], gamma_part[i])
        b_i_new = b_i(r, a_i_p, b_i_p, psi_p[i], dr_psi_p[i], dxi_psi_p[i], b_driver[i], pr_part[i], q_part[i], gamma_part[i])
        a_i_p = a_i_new
        b_i_p = b_i_new
        b_plasma_p[i] = b_theta_bar(a_i_p, b_i_p, r)
    return psi_p, dr_psi_p, b_plasma_p, b_driver


def calculate_fields_avg(xi, r_part, pr_part, gamma_part, q_part, xi_d, n_d, sz_d, sr_d, a_0, w_0, tau, xi_c):
    b_driver = b_theta_0_driver(xi, r_part, xi_d, n_d, sz_d, sr_d)
    nabla_a = laser_source(xi, r_part, a_0, w_0, tau, xi_c)
    # a_i_p = 0
    # b_i_p = 0
    psi_p = np.zeros_like(r_part)
    dr_psi_p = np.zeros_like(r_part)
    dxi_psi_p = np.zeros_like(r_part)
    # b_plasma_p = np.zeros_like(r_part)
    for i, r in enumerate(r_part):
        psi_p[i] = psi(r_part, q_part, r-0.001)
        dr_psi_p[i] = dr_psi(r_part, q_part, r-0.001)
        dxi_psi_p[i] = dxi_psi(r_part, pr_part, q_part, psi_p, r-0.001)
        # if i == len(r_part)-1:
        #     a_i_new = 0
        # else:
        # a_i_new = a_i(r-0.001, a_i_p, b_i_p, psi_p[i], dr_psi_p[i], dxi_psi_p[i], b_driver[i], pr_part[i], q_part[i], gamma_part[i])
        # b_i_new = b_i(r-0.001, a_i_p, b_i_p, psi_p[i], dr_psi_p[i], dxi_psi_p[i], b_driver[i], pr_part[i], q_part[i], gamma_part[i])
        # a_i_p = a_i_new
        # b_i_p = b_i_new
        # b_plasma_p[i] = b_theta_bar(a_i_p, b_i_p, r-0.001)
    # a_i_p = 0
    # b_i_p = 0
    psi_p2 = np.zeros_like(r_part)
    dr_psi_p2 = np.zeros_like(r_part)
    dxi_psi_p2 = np.zeros_like(r_part)
    # b_plasma_p2 = np.zeros_like(r_part)
    for i, r in enumerate(r_part):
        psi_p2[i] = psi(r_part, q_part, r+0.001)
        dr_psi_p2[i] = dr_psi(r_part, q_part, r+0.001)
        dxi_psi_p2[i] = dxi_psi(r_part, pr_part, q_part, psi_p2, r+0.001)
        # if i == len(r_part)-1:
        #     a_i_new = 0
        # else:
        # a_i_new = a_i(r+0.001, a_i_p, b_i_p, psi_p2[i], dr_psi_p2[i], dxi_psi_p2[i], b_driver[i], pr_part[i], q_part[i], gamma_part[i])
        # b_i_new = b_i(r+0.001, a_i_p, b_i_p, psi_p2[i], dr_psi_p2[i], dxi_psi_p2[i], b_driver[i], pr_part[i], q_part[i], gamma_part[i])
        # a_i_p = a_i_new
        # b_i_p = b_i_new
        # b_plasma_p2[i] = b_theta_bar(a_i_p, b_i_p, r+0.001)
    psi_p = (psi_p + psi_p2) / 2
    dr_psi_p = (dr_psi_p + dr_psi_p2) / 2
    dxi_psi_p = (dxi_psi_p + dxi_psi_p2) / 2
    # b_plasma_p = (b_plasma_p + b_plasma_p2) / 2
    
    a_i_p = 0
    b_i_p = 0
    b_plasma_p = np.zeros_like(r_part)
    for i, r in enumerate(r_part):
        a_i_new = a_i(r, a_i_p, b_i_p, psi_p[i], dr_psi_p[i], dxi_psi_p[i], b_driver[i], pr_part[i], q_part[i], gamma_part[i])
        b_i_new = b_i(r, a_i_p, b_i_p, psi_p[i], dr_psi_p[i], dxi_psi_p[i], b_driver[i], pr_part[i], q_part[i], gamma_part[i])
        ai = (a_i_p + a_i_new)/2
        bi = (b_i_p + b_i_new)/2
        b_plasma_p[i] = b_theta_bar(ai, bi, r)
    return psi_p, dr_psi_p, b_plasma_p, b_driver, nabla_a


def calculate_fields_new(xi, r_part, pr_part, gamma_part, q_part, xi_d, n_d, sz_d, sr_d):
    b_driver = b_theta_0_driver(xi, r_part, xi_d, n_d, sz_d, sr_d)
    a_i_p = 0
    b_i_p = 0
    psi_p = np.zeros_like(r_part)
    dr_psi_p = np.zeros_like(r_part)
    dxi_psi_p = np.zeros_like(r_part)
    b_plasma_p = np.zeros_like(r_part)
    a_i_arr = np.zeros_like(r_part)
    b_i_arr = np.zeros_like(r_part)
    for i, r in enumerate(r_part):
        psi_p[i] = psi(r_part, q_part, r)
        dr_psi_p[i] = dr_psi(r_part, q_part, r)
        dxi_psi_p[i] = dxi_psi(r_part, pr_part, q_part, psi_p, r)
        # if i == len(r_part)-1:
        #     a_i_new = 0
        # else:
    for i, r in enumerate(r_part):
        b_i_arr[i] = b_i(r, a_i_p, b_i_p, psi_p[i], dr_psi_p[i], dxi_psi_p[i], b_driver[i], pr_part[i], q_part[i], gamma_part[i])
        a_i_p = b_i_arr[i]
    a_i_new = a_i(r, a_i_p, b_i_p, psi_p[i], dr_psi_p[i], dxi_psi_p[i], b_driver[i], pr_part[i], q_part[i], gamma_part[i])
    a_i_p = a_i_new
    b_i_p = b_i_new
    b_plasma_p[i] = b_theta_bar(a_i_p, b_i_p, r)
    return psi_p, dr_psi_p, b_plasma_p, b_driver


# def calculate_fields_mesh(xi, r_part, pr_part, gamma_part, q_part, xi_d, n_d, sz_d, sr_d, r_bound, nr):
#     r_mesh = np.linspace(0, r_max, nr)
#     b_driver = b_theta_0_driver(xi, r_mesh, xi_d, n_d, sz_d, sr_d)
#     a_i_m = 0
#     b_i_m = 0
#     psi_m = np.zeros_like(r_mesh)
#     dr_psi_m = np.zeros_like(r_mesh)
#     dxi_psi_m = np.zeros_like(r_mesh)
#     b_plasma_m = np.zeros_like(r_mesh)
#     for i, r in enumerate(r_mesh):
#         psi_m[i] = psi(r_part, q_part, r)
#         dr_psi_m[i] = dr_psi(r_part, q_part, r)
#         dxi_psi_m[i] = dxi_psi(r_part, pr_part, q_part, psi_p, r)
#         if i == len(r_part)-1:
#             a_i_new = 0
#         else:
#             a_i_new = a_i(r, a_i_m, b_i_m, psi_m[i], dr_psi_m[i], dxi_psi_m[i], b_driver[i], pr_part[i], q_part[i], gamma_part[i])
#         b_i_new = b_i(r, a_i_p, b_i_p, psi_p[i], dr_psi_p[i], dxi_psi_p[i], b_driver[i], pr_part[i], q_part[i], gamma_part[i])
#         a_i_p = a_i_new
#         b_i_p = b_i_new
#         b_plasma_p[i] = b_theta_bar(a_i_p, b_i_p, r)
#     return psi_p, dr_psi_p, b_plasma_p, b_driver


def test():
    # driver properties
    xi_d = 3
    n_d = 0
    sr_d = 1
    sz_d = 1

    # plasma particles
    r_part = np.linspace(0, 5, 1000)[1:]
    dr = r_part[1] - r_part[0]
    pr_part = np.zeros_like(r_part)
    gamma_part = np.ones_like(r_part)
    q_part = dr*r_part
    # values of psi and its derivatives at the particle location
    psi_p = np.zeros_like(r_part)
    dr_psi_p = np.zeros_like(r_part)
    dxi_psi_p = np.zeros_like(r_part)
    b_plasma_p = np.zeros_like(r_part)

    # r_mesh = np.linspace(0, 5, 100)[1:]
    # psi_0 = np.zeros_like(r_mesh)
    # dr_psi_0 = np.zeros_like(r_mesh)
    # dxi_psi_0 = np.zeros_like(r_mesh)
    steps = np.arange(1)
    for step in steps:
        b_driver = b_theta_0_driver(0, r_part, xi_d, n_d, sz_d, sr_d)
        a_i_p = 0
        b_i_p = 0
        for i, r in enumerate(r_part):
            psi_p[i] = psi(r_part, q_part, r)
            dr_psi_p[i] = dr_psi(r_part, q_part, r)
            dxi_psi_p[i] = dxi_psi(r_part, pr_part, q_part, psi_p, r)
            if i == len(r_part)-1:
                a_i_new = 0
            else:
                a_i_new = a_i(r, a_i_p, b_i_p, psi_p[i], dr_psi_p[i], dxi_psi_p[i], b_driver[i], pr_part[i], q_part[i], gamma_part[i])
            b_i_new = b_i(r, a_i_p, b_i_p, psi_p[i], dr_psi_p[i], dxi_psi_p[i], b_driver[i], pr_part[i], q_part[i], gamma_part[i])
            a_i_p = a_i_new
            b_i_p = b_i_new
            b_plasma_p[i] = b_theta_bar(a_i_p, b_i_p, r)
            # print(a_i_p,b_i_p)
    # plt.plot(b_plasma_p)
    plt.plot(psi_p)
    plt.plot(dr_psi_p)
    plt.plot(dxi_psi_p)
    plt.plot(np.gradient(psi_p, dr))
    plt.show()


def test_driver_field():
    xi_d = 3
    n_d = 10
    sr_d = 1
    sz_d = 1
    xi = np.linspace(0, 10, 100)
    r = np.linspace(0, 5, 50)
    xi, r = np.meshgrid(xi, r)
    b_d = b_theta_0_driver(xi, r, xi_d, n_d, sz_d, sr_d)
    plt.imshow(b_d)
    plt.show()


def test_rk():
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
    r_part = np.linspace(0, 9, 900)[1:]
    dr = r_part[1] - r_part[0]
    pr_part = np.zeros_like(r_part)
    gamma_part = np.ones_like(r_part)
    q_part = dr*r_part
    p_idx = np.arange(len(r_part))

    # steps
    dxi = 0.1
    steps = 80
    

    i_track = 30
    r_track = np.zeros(steps)

    n_part = len(r_part)

    r_all = copy(r_part)
    q_all = copy(q_part)
    xi_all = np.zeros(n_part)
    
    for step in np.arange(steps):
        xi = dxi*(step+1)
        # plt.plot(np.ones_like(r_part)*xi, r_part, '.', ms=0.5)
        r_part, pr_part, gamma_part = evolve_plasma_rk4(r_part, pr_part, gamma_part, q_part, xi, dxi, xi_d, n_d, sz_d, sr_d, a_0, w_0, tau, xi_c)
        idx_keep = np.where(r_part<=r_max)
        r_part = r_part[idx_keep]
        pr_part = pr_part[idx_keep]
        gamma_part = gamma_part[idx_keep]
        r_part, idx = np.unique(r_part, return_index=True)
        pr_part = pr_part[idx]
        gamma_part = gamma_part[idx]
        p_idx = p_idx[idx]
        q_part = q_part[idx]
        r_all = np.append(r_all, r_part)
        q_all = np.append(q_all, q_part)
        xi_all = np.append(xi_all, np.ones(len(r_part))*xi)
        # r_track[step] = r_part[np.where(p_idx==i_track)]
    # plt.ylim((0, 2))
    # plt.plot(r_track)
    plt.plot(xi_all, r_all, '.', ms=0.5)
    # plt.hist2d(xi_all, r_all, 50, weights=q_all/r_all)
    plt.show()



# test()
# test_driver_field()
test_rk()



