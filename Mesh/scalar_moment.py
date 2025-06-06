import numpy as np

def compute_scalar_moment(moment_tensor):
    """
    Compute the scalar seismic moment from a moment tensor.

    Parameters:
    -----------
    moment_tensor : ndarray of shape (3,3)
        Symmetric 3x3 moment tensor in Newton-meters (or dyne-cm)

    Returns:
    --------
    M0 : float
        Scalar seismic moment (same units as the input tensor)
    """
    if moment_tensor.shape != (3, 3):
        raise ValueError("Moment tensor must be a 3x3 array.")

    # Ensure the tensor is symmetric
    symmetric_tensor = 0.5 * (moment_tensor + moment_tensor.T)
    
    # Frobenius norm and scalar moment
    frob_norm = np.sqrt(np.sum(symmetric_tensor**2))
    M0 = frob_norm / np.sqrt(2)
    return M0

def compute_moment_magnitude(M0):
    """
    Compute the moment magnitude from scalar moment.

    Parameters:
    -----------
    M0 : float
        Scalar seismic moment in N·m

    Returns:
    --------
    Mw : float
        Moment magnitude
    """
    if M0 <= 0:
        raise ValueError("Scalar moment must be positive.")
    Mw = (2.0 / 3.0) * (np.log10(M0) - 9.1)  # 9.1 ≈ log10(10^9.1) ≈ 6.07
    return Mw

def moment_to_yield(M0_Nm, A=16.05, B=1.5):
    """
    Convert scalar seismic moment (N·m) to kiloton yield (kt) for an isotropic source.
    
    Parameters:
    -----------
    M0_Nm : float or array_like
        Scalar seismic moment in N·m.
    A : float
        Empirical constant for log10(M0 in dyne·cm) = A + B * log10(Y).
    B : float
        Empirical constant.
    
    Returns:
    --------
    yield_kt : float or ndarray
        Estimated kiloton yield.
    """
    # Convert moment from N·m to dyne·cm
    M0_dyne_cm = M0_Nm * 1e7
    log_M0 = np.log10(M0_dyne_cm)
    log_Y  = (log_M0 - A) / B
    return 10 ** log_Y




# Example usage:
val = 1e9
M = np.array([
    [1e12, 0,   0],
    [0, 1e12,   0],
    [0,   0, 1e12]
])  # units: N·m

# Compute scalar moment and magnitude
M0 = compute_scalar_moment(M)
Mw = compute_moment_magnitude(M0)
Y_kt = moment_to_yield(M0)

print(f"Scalar Moment (M0): {M0:.3e} N·m")
print(f"Moment Magnitude (Mw): {Mw:.2f}")
print(f"Estimated yield: {Y_kt:.2f} kilotons")
