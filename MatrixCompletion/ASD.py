"""
Alternating Steepest Descent (ASD)
Taken from Low rank matrix completion by alternating steepest descent methods
Jared Tanner and Ke Wei
SIAM J. IMAGING SCIENCES (2014)

We have a matrix M with incomplete entries,
and want to estimate the full matrix

Solves the following relaxation of the problem:
minimize_{X,Y} \frac{1}{2} ||P_{\Omega}(Z^0) - P_\{Omega}(XY)||_F^2
Where \Omega represents the set of m observed entries of the matrix M
and P_{\Omega}() is an operator that represents the observed data. 

Inputs:
 M := Incomplete matrix, with NaN on the unknown matrix
 r := hypothesized rank of the matrix

Usage:
 Just call the function ASD(M)
"""

import numpy as np
from scipy import linalg

def ASD(M, r = None, reltol=1e-5, maxiter=5000):

    # Get shape and Omega
    m, n = M.shape
    if r == None:
        r = min(m, n, 5)

    Omega = ~np.isnan(M)
    relres = reltol * linalg.norm(M[Omega]) #set relative error

    # Initialize
    X = np.random.randn(m, r)
    Y = np.random.randn(r, n)
    itres = np.zeros((maxiter+1, 1)) 

    XY = np.dot(X, Y)
    diff_on_omega = M[Omega] - XY[Omega]
    res = linalg.norm(diff_on_omega)
    iter = 0
    itres[iter] = res

    while iter < maxiter and res >= relres:
        
        # Gradient for X
        diff_on_omega_matrix = np.zeros((m,n))
        diff_on_omega_matrix[Omega] = diff_on_omega
        grad_X = np.dot(diff_on_omega_matrix, np.transpose(Y))
        
        # Stepsize for X
        delta_XY = np.dot(grad_X, Y)
        tx = linalg.norm(grad_X,'fro')**2/linalg.norm(delta_XY)**2
    
        # Update X
        X = X + tx*grad_X;
        diff_on_omega = diff_on_omega-tx*delta_XY[Omega]
    
        # Gradient for Y
        diff_on_omega_matrix = np.zeros((m,n))
        diff_on_omega_matrix[Omega] = diff_on_omega
        Xt = np.transpose(X)
        grad_Y = np.dot(Xt, diff_on_omega_matrix)
    
        # Stepsize for Y
        delta_XY = np.dot(X, grad_Y)
        ty = linalg.norm(grad_Y,'fro')**2/linalg.norm(delta_XY)**2
    
        # Update Y
        Y = Y + ty*grad_Y
        diff_on_omega = diff_on_omega-ty*delta_XY[Omega]
        
        res = linalg.norm(diff_on_omega)
        iter = iter + 1
        itres[iter] = res

    M_out = np.dot(X, Y)

    out = [iter, itres[iter]/linalg.norm(M[Omega])]

    return M_out, out