import numpy as np
import cv2


class camera:
    def __init__(self, K, R=None, t=None, distortion=None, imshape=None):
        self.K = K
        self.R = R
        self.t = t
        self.distortion = distortion
        self.imshape = imshape
        if R is None:
            self.R = np.eye(3, dtype=K.dtype)
        if t is None:
            self.t = np.zeros((3,), K.dtype)
        if distortion is None:
            self.distortion = np.array(tuple(), K.dtype)
        if imshape is None:
            self.imshape = np.array((0, 0), int)

    @property
    def position(self):
        """position of the camera in *world space*."""
        return - self.R.T.dot(self.t)

    @property
    def P(self):
        """Projection matrix, (3, 4) array."""
        return self.K.dot(np.c_[self.R, self.t])

    @property
    def focal_vector(self):
        """Focal vector, (2,) view into array self.K."""
        return np.diag(self.K)[:2]

    @property
    def principal_point(self):
        """Principal point, (2,) view into array self.K."""
        return self.K[:2, -1]

    def relative_to(self, other):
        R = self.R.dot(other.R.T)
        t = R.dot(other.position - self.position)
        return R, t

    def __repr__(self):
        def arr2str(s, A):
            return s + np.array2string(A, precision=2, separator=',',
                                       suppress_small=True,
                                       prefix=s.strip('\n'))
        return (arr2str("camera{   K: ", self.K) + ",\n" +
                arr2str("          R: ", self.R) + ",\n" +
                arr2str("          t: ", self.t) + ",\n" +
                arr2str("    imshape: ", self.imshape) + ",\n" +
                arr2str(" distortion: ", self.distortion) + "}")
