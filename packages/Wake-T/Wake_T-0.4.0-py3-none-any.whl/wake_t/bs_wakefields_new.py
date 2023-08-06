import numpy as np
import matplotlib.pyplot as plt


def psi(r_part, q_part, r):
    return delta_psi(r_part, q_part, r) - np.sum(q_part * np.log(r_part[-1]/r_part)) + r_part[-1]**2/4


def delta_psi(r_part, q_part, r):
    if r != 0:
        sum_i = np.where(r_part < r)
        r_i = r_part[sum_i]
        q_i = q_part[sum_i]
        return np.sum(q_i * np.log(r/r_i)) - r**2/4
    else:
        return 0.


def dr_psi(r_part, q_part, r):
    if r != 0:
        sum_i = np.where(r_part < r)
        q_i = q_part[sum_i]
        return np.sum(q_i)/r - r/2
    else:
        return 0.


def dxi_psi(r_part, pr_part, q_part, psi_part, r):
    return (dxi_delta_psi(r_part, pr_part, q_part, psi_part, r) -
            np.sum((q_part * pr_part) / (r_part * (1+psi_part))))


def dxi_delta_psi(r_part, pr_part, q_part, psi_part, r):
    if r != 0:
        sum_i = np.where(r_part < r)
        r_i = r_part[sum_i]
        p_ri = pr_part[sum_i]
        q_i = q_part[sum_i]
        psi_i = psi_part[sum_i]
        return -np.sum((q_i * p_ri) / (r_i * (1+psi_i)))
    else:
        return 0.


def b_theta_bar(a_i, b_i, r):
    return a_i * r - b_i / r


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

# def b_theta_bar(r, r_part, pr_part, q_part, gamma_part, psi_part, dr_psi_part, dxi_psi_part, b_theta_part):
#     flt = np.where(r_part < r)
#     r_below = r_part[flt]
#     pr_below = pr_part[flt]
#     q_below = q_part[flt]
#     gamma_below = gamma_part[flt]
#     psi_below = psi_part[flt]
#     dr_psi_below = dr_psi_part[flt]
#     dxi_psi_below = dxi_psi_part[flt]
#     b_theta_below = b_theta_part[flt]

#     ai = a_i(r_below, pr_below, q_below, gamma_below, psi_below, dr_psi_below, dxi_psi_below, b_theta_below)
#     bi = b_i(r_below, pr_below, q_below, gamma_below, psi_below, dr_psi_below, dxi_psi_below, b_theta_below)
#     return ai * r - bi / r


# def a_i(r_part, pr_part, q_part, gamma_part, psi_part, dr_psi_part, dxi_psi_part, b_theta_part):
#     if len(r_part) <= 1:
#         return 0.
#     else:
#         r_i = r_part[0]
#         pr_i = pr_part[0]
#         q_i = q_part[0]
#         gamma_i = gamma_part[0]
#         psi_i = psi_part[0]
#         dr_psi_i = dr_psi_part[0]
#         dxi_psi_i = dxi_psi_part[0]
#         b_theta_i = b_theta_part[0]

#         A_i_val = A_i(q_i, r_i, psi_i)
#         B_i_val = B_i(q_i, r_i, gamma_i, pr_i, psi_i, dr_psi_i, dxi_psi_i, b_theta_i)
#         C_i_val = C_i(q_i, r_i, gamma_i, pr_i, psi_i)

#         a_im = a_i(r_part[1:], pr_part[1:], q_part[1:], gamma_part[1:], psi_part[1:], dr_psi_part[1:], dxi_psi_part[1:], b_theta_part[1:])
#         b_im = b_i(r_part[1:], pr_part[1:], q_part[1:], gamma_part[1:], psi_part[1:], dr_psi_part[1:], dxi_psi_part[1:], b_theta_part[1:])

#         return (1 + A_i_val*r_i/2) * a_im + A_i_val/(2*r_i) * b_im + (2*B_i_val + A_i_val*C_i_val)/4

# # def a_i(r_i, psi_i, dr_psi_i, dxi_psi_i, b_theta_0, pr_i, q_i, gamma_i):
# #     A_i_val = A_i(q_i, r_i, psi_i)
# #     B_i_val = B_i(q_i, r_i, gamma_i, pr_i, psi_i, dr_psi_i, dxi_psi_i, b_theta_0)
# #     C_i_val = C_i(q_i, r_i, gamma_i, pr_i, psi_i)

# #     return (1 + A_i_val*r_i/2) * a_im + A_i_val/(2*r_i) * b_im + (2*B_i_val + A_i_val*C_i_val)/4

# def b_i(r_part, pr_part, q_part, gamma_part, psi_part, dr_psi_part, dxi_psi_part, b_theta_part):
#     if len(r_part) <= 1:
#         return 0.
#     else:
#         r_i = r_part[0]
#         pr_i = pr_part[0]
#         q_i = q_part[0]
#         gamma_i = gamma_part[0]
#         psi_i = psi_part[0]
#         dr_psi_i = dr_psi_part[0]
#         dxi_psi_i = dxi_psi_part[0]
#         b_theta_i = b_theta_part[0]

#         A_i_val = A_i(q_i, r_i, psi_i)
#         B_i_val = B_i(q_i, r_i, gamma_i, pr_i, psi_i, dr_psi_i, dxi_psi_i, b_theta_i)
#         C_i_val = C_i(q_i, r_i, gamma_i, pr_i, psi_i)

#         a_im = a_i(r_part[1:], pr_part[1:], q_part[1:], gamma_part[1:], psi_part[1:], dr_psi_part[1:], dxi_psi_part[1:], b_theta_part[1:])
#         b_im = b_i(r_part[1:], pr_part[1:], q_part[1:], gamma_part[1:], psi_part[1:], dr_psi_part[1:], dxi_psi_part[1:], b_theta_part[1:])
#         return (- A_i_val*r_i**3/2 * a_im + (1 - A_i_val*r_i/2) * b_im
#             + r_i * (4*C_i_val - 2*B_i_val*r_i - A_i_val*C_i_val*r_i) / 4)


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


def b_theta_0_driver(xi, r, xi_d, n_d, sz_d, sr_d):
    return (- n_d * np.exp(-(xi-xi_d)**2/(2*sz_d**2)) * sr_d**2/r * (1 - np.exp(-r**2/(2*sr_d**2)))
            - 0 * np.exp(-(xi-6.5)**2/(2*0.3**2)) * 0.1**2/r * (1 - np.exp(-r**2/(2*0.1**2))))


def test_psi():
    r_max = 2
    nr = 200
    dr = r_max / nr
    r_mesh = np.linspace(dr, r_max, nr)
    psi_m = np.zeros_like(r_mesh)
    dr_psi_m = np.zeros_like(r_mesh)
    dxi_psi_m = np.zeros_like(r_mesh)
    b_theta_m = np.zeros_like(r_mesh)

    
    # plasma particles
    ppm = 4
    r_max_part = 1
    n_part = ppm * nr * r_max_part / r_max
    dr_p = r_max_part / n_part
    r_part = np.linspace(dr_p, r_max_part, int(n_part))
    pr_part = np.zeros_like(r_part)
    gamma_part = np.ones_like(r_part)
    q_part = dr_p*r_part

    r_part += 0.5 - r_part/2

    # loop
    for i, r in enumerate(r_mesh):
        psi_m[i] = psi(r_part, q_part, r)
        dr_psi_m[i] = dr_psi(r_part, q_part, r)
    psi_p = np.interp(r_part, r_mesh, psi_m)
    dr_psi_p = np.interp(r_part, r_mesh, dr_psi_m)
    for i, r in enumerate(r_mesh):
        dxi_psi_m[i] = dxi_psi(r_part, pr_part, q_part, psi_p, r)
    dxi_psi_p = np.interp(r_part, r_mesh, dxi_psi_m)
    p_index = np.arange(len(r_part))
    for i, r in enumerate(r_mesh):
        ai = 0
        bi = 0
        idx_below = p_index[np.where(r_part < r)]
        for idx in idx_below:
            ai = a_i(r_part[idx], ai, bi, psi_p[idx], dr_psi_p[idx], dxi_psi_p[idx], 0., pr_part[idx], q_part[idx], gamma_part[idx])
            bi = b_i(r_part[idx], ai, bi, psi_p[idx], dr_psi_p[idx], dxi_psi_p[idx], 0., pr_part[idx], q_part[idx], gamma_part[idx])
        # b_theta_bar(r, r_part, pr_part, q_part, gamma_part, psi_p, dr_psi_p, dxi_psi_p, np.zeros_like(r_part))
        b_theta_m[i] = b_theta_bar(ai, bi, r)

    # plt.plot(r_mesh, psi_m)
    # plt.plot(r_mesh, dr_psi_m)
    # plt.plot(r_mesh, np.gradient(psi_m, dr))
    # plt.plot(r_mesh, dxi_psi_m)
    plt.hist(r_part, 100, range=[0, 1])
    plt.plot(r_mesh, b_theta_m)
    plt.show()


test_psi()
