import numpy as np
from scipy import ndimage
from scipy.fftpack import fft
from imagelab.utilities import ndtake, fint
from imagelab import io  # for debugging purposes.


def decode(data, DFT_channels=1):
    data = np.squeeze(data, axis=-1)  # assume grayscale and squeese axis
    shifting_axis = -3  # always assume lists of images
    dft = fft(data, axis=shifting_axis)

    N = data.shape[shifting_axis]  # N data points
    sdft = 4 * dft / N
    M = fint(N / 2)  # Nyquist frequency

    sdft_ch = sdft[ndtake(DFT_channels, shifting_axis)]
    phase = np.mod(-np.angle(sdft_ch), 2 * np.pi)
    signal = np.absolute(sdft_ch)
    sdft = sdft[ndtake(slice(1, M), shifting_axis)]  # keep until Nyquist
    noise = np.absolute(sdft).sum(axis=shifting_axis)
    noise = noise - signal  # noise is all minus the *individual* signals
    return phase, signal, noise


def unwrap_phase_with_cue(phase, cue, wave_count):
    phase_cue = np.mod(cue - phase, 2 * np.pi)
    phase_cue = np.round(((phase_cue * wave_count) - phase) / (2 * np.pi))
    return (phase + (2 * np.pi * phase_cue)) / wave_count


def stdmask(phase, dphase, signal_noise_list):
    """ Standard masking function to use on the phase shift.

        If you wish to change how it works or some parameters, then copy this
        funtion and replace the relevant sections."""
    mask = np.ones_like(phase, dtype=bool)
    # Threshold on phase
    mask &= np.logical_and(phase >= 0.0, phase <= 2 * np.pi)
    for signal, noise in signal_noise_list:
        # Threshold on signal trust region
        mask &= np.logical_and(0.1 < signal, signal < 0.9)
        # Threshold on signal to noise ratio
        mask &= signal > 4 * noise
    # Threshold on gradient and curvature of phase.
    # TODO: Tune the tolarances for gradients and curvature.
    dph = np.linalg.norm(dphase, axis=-1)
    ddph = np.stack(np.gradient(dph, axis=(-2, -1)), axis=-1)
    ddph = np.linalg.norm(ddph, axis=-1)
    mask &= np.logical_and(1e-8 < dph, dph < 1e-2)
    mask &= ddph < 1e-2
    # Remove borders
    mask[..., [0, -1]] = 0
    mask[..., [0, -1], :] = 0
    # Remove mask-pixels with masked neighbors
    weights = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]], dtype=int)
    weights = np.broadcast_to(weights, mask.shape[:-2] + weights.shape)
    neighbors = ndimage.convolve(mask.astype(int), weights, mode='constant')
    mask = np.logical_and(mask, neighbors > 1)
    return mask


def decode_with_cue(primary, cue, wave_count, DFT_channels=1, maskfn=stdmask):
    primary_phase, primary_signal, primary_noise = decode(primary)
    cue_phase, cue_signal, cue_noise = decode(cue)
    phase = unwrap_phase_with_cue(primary_phase, cue_phase, wave_count)
    dphase = np.stack(np.gradient(phase, axis=(-2, -1)), axis=-1)
    signal_noise_list = [[primary_signal, primary_noise],
                         [cue_signal, cue_noise]]
    mask = maskfn(phase, dphase, signal_noise_list)
    return phase, dphase, mask


def stereo_correspondances(L_enc, R_enc, L_mask, R_mask, keep_unsure=False):
    if L_mask.sum() == 0 or R_mask.sum() == 0:
        return np.empty((2, 0))
    # To conserve computation size, we only consider a nonzero encoding patch.
    L_nz_rows, L_nz_cols = L_mask.nonzero()
    R_nz_rows, R_nz_cols = R_mask.nonzero()

    # Notice that rows are shared between L and R.
    rows = slice(min(L_nz_rows.min(), R_nz_rows.min()),
                 max(L_nz_rows.max(), R_nz_rows.max()) + 1)
    L_cols = slice(L_nz_cols.min(), L_nz_cols.max() + 1)
    R_cols = slice(R_nz_cols.min(), R_nz_cols.max() + 1)

    L_mask, R_mask = L_mask[rows, L_cols], R_mask[rows, R_cols]
    L_enc, R_enc = L_enc[rows, L_cols], R_enc[rows, R_cols]

    # both the left and right side of a match must exist
    match = np.logical_and(L_mask[..., None], R_mask[..., None, :-1])
    match &= R_mask[..., None, 1:]

    # Value in left should lie between to neighbouring values in right
    match[L_enc[..., :, None] < R_enc[..., None, :-1]] = 0
    match[L_enc[..., :, None] >= R_enc[..., None, 1:]] = 0

    if not keep_unsure:
        match[match.sum(axis=-1) > 1] = 0

    if match.sum() == 0:
        return np.empty((2, 0))

    if np.any(match.sum(axis=-1) > 1):
        print('wrong match', (match.sum(axis=-1) > 1).sum())
        errors = (match.sum(axis=-1) > 1)
        for e in errors.nonzero()[0]:
            print('i', e, 'phase', L_enc[..., e])
            _e = match[e].nonzero()[0]
            _a, _b = np.min(_e), np.max(_e) + 1
            print('a,b', _a, _b)
            print('left', R_enc[..., :-1][..., _a:_b])
            print('right', R_enc[..., 1:][..., _a:_b])

    r, cL, cR = tuple(match.nonzero())
    step = R_enc[(r, cR + 1)] - R_enc[(r, cR)]
    cRfrac = (L_enc[(r, cL)] - R_enc[(r, cR)]) / step

    r += rows.start
    cL += L_cols.start
    cR = cR + R_cols.start + cRfrac
    return np.array([[r, cL], [r, cR]]).swapaxes(1, 2)


def stereo_triangulate_linearization(left_cam, right_cam):
    dtype = left_cam.P.dtype
    P0 = left_cam.P
    P1 = right_cam.P
    e = np.eye(4, dtype=dtype)
    C = np.empty((4, 3, 3, 3), dtype)
    for i in np.ndindex((4, 3, 3, 3)):
        tmp = np.stack((P0[i[1]], P0[i[2]], P1[i[3]], e[i[0]]), axis=0)
        C[i] = np.linalg.det(tmp.T)
    C = C[..., None, None]
    yx = np.mgrid[0:left_cam.imshape[0], 0:left_cam.imshape[1]].astype(dtype)
    y, x = yx[None, 0, :, :], yx[None, 1, :, :]
    offset = C[:, 0, 1, 0] - C[:, 2, 1, 0] * x - C[:, 0, 2, 0] * y
    factor = -C[:, 0, 1, 2] + C[:, 2, 1, 2] * x + C[:, 0, 2, 2] * y
    return offset, factor


def stereo_triangulate(left, right, left_cam, right_cam):
    offset, factor = stereo_triangulate_linearization(left_cam, right_cam)
    idx = (slice(None), *(left + 0.5).astype(int).T)
    xyzw = offset[idx] + factor[idx] * right[None, ..., 1]
    return xyzw.T[..., :3] / xyzw.T[..., 3, None]
