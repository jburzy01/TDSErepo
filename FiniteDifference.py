import numpy as np
import WaveFunction

def solve1(xs, ts, potential, psi_init, periodic_boundary_cond):
    matrix = build_matrix(xs, ts, potential, periodic_boundary_cond)
    return finite_difference1(xs, ts, psi_init, matrix, periodic_boundary_cond)

def solve2(xs, ts, potential, psi_init, periodic_boundary_cond):
    left_matrix = build_matrix_left(xs, ts, potential, periodic_boundary_cond)
    right_matrix = build_matrix_right(xs, ts, potential, periodic_boundary_cond)
    return finite_difference2(xs, ts, psi_init, left_matrix, right_matrix, periodic_boundary_cond)

def build_matrix(xs, ts, potential, periodic_boundary_cond):
    num_x = xs.get_num_divisions()
    delta_x = xs.get_delta()
    delta_t = ts.get_delta()
    matrix = np.zeros((num_x, num_x), dtype=complex)

    # zero boundary conditions
#    matrix[0,0] = 1.0
#    matrix[-1,-1] = 1.0

    # periodic boundary conditions
    matrix[0,0] = potential[0] + 2/delta_x**2 - 1j/delta_t
    matrix[0,1] = -1/delta_x**2
    matrix[0,-1] = -1/delta_x**2

    matrix[-1,-1] = potential[0] + 2/delta_x**2 - 1j/delta_t
    matrix[-1,-2] = -1/delta_x**2
    matrix[-1,0] = -1/delta_x**2
    for n in xrange(1,num_x-1):
        for i in xrange(num_x):
            if i==n:
                matrix[n,i] = potential[i] + 2/delta_x**2 - 1j/delta_t
            elif abs(i-n) == 1:
                matrix[n,i] = -1/delta_x**2
    return matrix

def build_matrix_left(xs, ts, potential, periodic_boundary_cond):
    num_x = xs.get_num_divisions()
    delta_x = xs.get_delta()
    delta_t = ts.get_delta()
    matrix = np.zeros((num_x, num_x), dtype=complex)

    # zero boundary conditions
#    matrix[0,0] = 1.0
#    matrix[-1,-1] = 1.0

    # periodic boundary conditions
    matrix[0,0] = 1 + 1j*delta_t/delta_x**2 + 1j*delta_t*potential[0]/2
    matrix[0,1] = -1j*delta_t/(2*delta_x**2)
    matrix[0,-1] = -1j*delta_t/(2*delta_x**2)

    matrix[-1,-1] = 1 + 1j*delta_t/delta_x**2 + 1j*delta_t*potential[0]/2
    matrix[-1,-2] = -1j*delta_t/(2*delta_x**2)
    matrix[-1,0] = -1j*delta_t/(2*delta_x**2)

    for n in xrange(1,num_x-1):
        for i in xrange(num_x):
            if i==n:
                matrix[n,i] = 1 + 1j*delta_t/delta_x**2 + 1j*delta_t*potential[i]/2
            elif abs(i-n) == 1:
                matrix[n,i] = -1j*delta_t/(2*delta_x**2)
    return matrix

def build_matrix_right(xs, ts, potential, periodic_boundary_cond):
    num_x = xs.get_num_divisions()
    delta_x = xs.get_delta()
    delta_t = ts.get_delta()
    matrix = np.zeros((num_x, num_x), dtype=complex)

    # zero boundary conditions
#    matrix[0,0] = 1.0
#    matrix[-1,-1] = 1.0

    # periodic boundary conditions

    matrix[0,0] = 1 - 1j*delta_t/delta_x**2 - 1j*delta_t*potential[0]/2
    matrix[0,1] = 1j*delta_t/(2*delta_x**2)
    matrix[0,-1] = 1j*delta_t/(2*delta_x**2)

    matrix[-1,-1] = 1 - 1j*delta_t/delta_x**2 - 1j*delta_t*potential[0]/2
    matrix[-1,-2] = 1j*delta_t/(2*delta_x**2)
    matrix[-1,0] = 1j*delta_t/(2*delta_x**2)

    for n in xrange(1,num_x-1):
        for i in xrange(num_x):
            if i==n:
                matrix[n,i] = 1 - 1j*delta_t/delta_x**2 - 1j*delta_t*potential[i]/2
            elif abs(i-n) == 1:
                matrix[n,i] = 1j*delta_t/(2*delta_x**2)
    return matrix

def finite_difference1(xs, ts, psi_init, matrix, periodic_boundary_cond):
    num_x = xs.get_num_divisions()
    num_t = ts.get_num_divisions()
    delta_t = ts.get_delta()
    psi = np.zeros((num_t,num_x), dtype=complex)
    psi[0,:] = psi_init

    # boundary conditions
    psi[:,0] = 0
    psi[:,-1] = 0
    for n in xrange(num_t-1):
        psi[n+1,:] = np.linalg.solve(matrix, -1j*psi[n,:]/delta_t)
        psi[n+1,0] = 0
        psi[n+1,-1] = 0
        psi[n+1,:] = WaveFunction.normalize(psi[n+1,:])
    return psi

def finite_difference2(xs, ts, psi_init, left_matrix, right_matrix, periodic_boundary_cond):
    num_x = xs.get_num_divisions()
    num_t = ts.get_num_divisions()
    delta_t = ts.get_delta()
    psi = np.zeros((num_t,num_x), dtype=complex)
    psi[0,:] = psi_init
    # boundary conditions
#    psi[:,0] = 0
#    psi[:,-1] = 0
    for n in xrange(num_t-1):
        b = psi[n,:]
        psi[n+1,:] = np.linalg.solve(left_matrix,np.dot(right_matrix,b))
#        psi[n+1,0] = 0
#        psi[n+1,-1] = 0
#        psi[n+1,-1] = psi[n+1,0]
        psi[n+1,:] = WaveFunction.normalize(psi[n+1,:])
    return psi
