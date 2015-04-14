#  Finite Difference Linear System Solving Module
#
#      created by: Jackson, Caleb, Justin
#      date:       14/13/2015

import numpy as np
import WaveFunction

# solves the system using the naive finite difference approach
def solve1(xs, ts, potential, psi_init, periodic_boundary_cond):
    matrix = build_matrix(xs, ts, potential, periodic_boundary_cond)
    return finite_difference1(xs, ts, psi_init, matrix, periodic_boundary_cond)

# solves the system using the unitary approach
def solve2(xs, ts, potential, psi_init, periodic_boundary_cond):
    left_matrix = build_matrix_left(xs, ts, potential, periodic_boundary_cond)
    right_matrix = build_matrix_right(xs, ts, potential, periodic_boundary_cond)
    return finite_difference2(xs, ts, psi_init, left_matrix, right_matrix, periodic_boundary_cond)

# builds the tridiagonal matrix for the naive finite difference approach
def build_matrix(xs, ts, potential, periodic_boundary_cond):
    num_x = xs.get_num_divisions()
    delta_x = xs.get_delta()
    delta_t = ts.get_delta()
    matrix = np.zeros((num_x, num_x), dtype=complex)

    if periodic_boundary_cond:
        # periodic boundary conditions
        matrix[0,0] = potential[0] + 1/delta_x**2 - 1j/delta_t
        matrix[0,1] = -1/(2*delta_x**2)
        matrix[0,-1] = -1/(2*delta_x**2)

        matrix[-1,-1] = potential[0] + 1/delta_x**2 - 1j/delta_t
        matrix[-1,-2] = -1/(2*delta_x**2)
        matrix[-1,0] = -1/(2*delta_x**2)
    else:
        # zero boundary conditions
        matrix[0,0] = 1.0
        matrix[-1,-1] = 1.0
    for n in xrange(1,num_x-1):
        for i in xrange(num_x):
            if i==n:
                matrix[n,i] = potential[i] + 1/delta_x**2 - 1j/delta_t
            elif abs(i-n) == 1:
                matrix[n,i] = -1/(2*delta_x**2)
    return matrix

# builds the tridiagonal matrix for the left side of the equation
def build_matrix_left(xs, ts, potential, periodic_boundary_cond):
    num_x = xs.get_num_divisions()
    delta_x = xs.get_delta()
    delta_t = ts.get_delta()
    matrix = np.zeros((num_x, num_x), dtype=complex)


    if periodic_boundary_cond:
        # periodic boundary conditions
        matrix[0,0] = 1 + 1j*delta_t/(2*delta_x**2) + 1j*delta_t*potential[0]/2
        matrix[0,1] = -1j*delta_t/(4*delta_x**2)
        matrix[0,-1] = -1j*delta_t/(4*delta_x**2)

        matrix[-1,-1] = 1 + 1j*delta_t/(2*delta_x**2) + 1j*delta_t*potential[0]/2
        matrix[-1,-2] = -1j*delta_t/(4*delta_x**2)
        matrix[-1,0] = -1j*delta_t/(4*delta_x**2)
    else:
        # zero boundary conditions
        matrix[0,0] = 1.0
        matrix[-1,-1] = 1.0

    for n in xrange(1,num_x-1):
        for i in xrange(num_x):
            if i==n:
                matrix[n,i] = 1 + 1j*delta_t/(2*delta_x**2) + 1j*delta_t*potential[i]/2
            elif abs(i-n) == 1:
                matrix[n,i] = -1j*delta_t/(4*delta_x**2)
    return matrix

# builds the tridiagonal matrix for the right side of the equation
def build_matrix_right(xs, ts, potential, periodic_boundary_cond):
    num_x = xs.get_num_divisions()
    delta_x = xs.get_delta()
    delta_t = ts.get_delta()
    matrix = np.zeros((num_x, num_x), dtype=complex)

    if periodic_boundary_cond:
        # periodic boundary conditions
        matrix[0,0] = 1 - 1j*delta_t/(2*delta_x**2) - 1j*delta_t*potential[0]/2
        matrix[0,1] = 1j*delta_t/(4*delta_x**2)
        matrix[0,-1] = 1j*delta_t/(4*delta_x**2)

        matrix[-1,-1] = 1 - 1j*delta_t/(2*delta_x**2) - 1j*delta_t*potential[0]/2
        matrix[-1,-2] = 1j*delta_t/(4*delta_x**2)
        matrix[-1,0] = 1j*delta_t/(4*delta_x**2)
    else:
        # zero boundary conditions
        matrix[0,0] = 1.0
        matrix[-1,-1] = 1.0

    for n in xrange(1,num_x-1):
        for i in xrange(num_x):
            if i==n:
                matrix[n,i] = 1 - 1j*delta_t/(2*delta_x**2) - 1j*delta_t*potential[i]/2
            elif abs(i-n) == 1:
                matrix[n,i] = 1j*delta_t/(4*delta_x**2)
    return matrix

# goes through the naive finite difference approach
def finite_difference1(xs, ts, psi_init, matrix, periodic_boundary_cond):
    num_x = xs.get_num_divisions()
    num_t = ts.get_num_divisions()
    delta_t = ts.get_delta()
    psi = np.zeros((num_t,num_x), dtype=complex)
    psi[0,:] = psi_init

    if not periodic_boundary_cond:
        psi[:,0] = 0
        psi[:,-1] = 0

    for n in xrange(num_t-1):
        psi[n+1,:] = np.linalg.solve(matrix, -1j*psi[n,:]/delta_t)
        if not periodic_boundary_cond:
            psi[n+1,0] = 0
            psi[n+1,-1] = 0
        psi[n+1,:] = WaveFunction.normalize(psi[n+1,:])
    return psi

# goes through the unitary finite difference method
def finite_difference2(xs, ts, psi_init, left_matrix, right_matrix, periodic_boundary_cond):
    num_x = xs.get_num_divisions()
    num_t = ts.get_num_divisions()
    delta_t = ts.get_delta()
    psi = np.zeros((num_t,num_x), dtype=complex)
    psi[0,:] = psi_init

    if not periodic_boundary_cond:
    # boundary conditions
        psi[:,0] = 0
        psi[:,-1] = 0

    for n in xrange(num_t-1):
        b = psi[n,:]
        psi[n+1,:] = np.linalg.solve(left_matrix,np.dot(right_matrix,b))
        if not periodic_boundary_cond: 
            psi[n+1,0] = 0
            psi[n+1,-1] = 0
    return psi
