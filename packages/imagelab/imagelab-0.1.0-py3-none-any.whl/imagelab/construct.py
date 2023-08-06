import numpy as np
import plyfile
import warnings
from imagelab import utilities


def fit_planes(points, mask=None):
    barycenters = points.mean(axis=-2, keepdims=True)
    baryvectors = (points - barycenters)
    if mask is not None:
        baryvectors[np.logical_not(mask)] *= 0
    M = (baryvectors[..., None, :] * baryvectors[..., None]).sum(axis=-3)
    eig_values = np.full((len(baryvectors), 3), np.nan)
    eig_vectors = np.full((len(baryvectors), 3, 3), np.nan)
    v = ~np.isnan(M).any(axis=-1).any(axis=-1)
    eig_values[v], eig_vectors[v] = np.linalg.eigh(M[v])
    i = tuple(np.arange(0, eig_values.shape[i], dtype=int)
              for i in range(0, len(eig_values.shape) - 1))
    _indices = np.zeros(len(eig_vectors), int)
    _indices[v] = np.nanargmin(np.abs(eig_values[v]), axis=-1)
    indices = (*i, slice(None), _indices)
    return eig_vectors[indices]


def normalize(v):
    return v / np.linalg.norm(v, axis=-1, keepdims=True)


def planefit_normals(camera, points3D, pixels):
    imshape = tuple(camera.imshape[:2])
    xyz = np.full(imshape + (3,), np.nan, points3D.dtype)
    xyz_pixels = tuple(utilities.rint(pixels).T)
    xyz[xyz_pixels] = points3D
    mask = np.zeros(imshape + (3, 3), bool)
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            mask_pixels = tuple(utilities.rint(pixels + np.array([[i, j]])).T)
            mask[(*mask_pixels, i, j)] = 1
    mask = mask.reshape(imshape + (9,))

    p3D = np.stack([xyz[mask[:, :, i]] for i in range(9)], axis=-2)
    nmask = np.stack([mask[mask[:, :, i]][:, 4] for i in range(9)], axis=-1)

    n = normalize(fit_planes(p3D, nmask))

    nan_count = np.isnan(n).sum()
    if nan_count > 0:
        print('Warning: from_SVD() produced {} nans'.format(nan_count))

    c = normalize(camera.position - xyz[mask[:, :, 4]])
    deviation = (n * c).sum(axis=1)
    n *= np.sign(deviation)[:, None]
    return n, np.abs(deviation)


class pointcloud(object):
    """pointcloud encapsulates positions, normals, and colors.

    The class can read and write Standford .ply files"""

    def __init__(self, positions=None, colors=None, normals=None):
        super(pointcloud, self).__init__()
        self.positions = positions
        self.colors = colors
        self.normals = normals

    def writePLY(self, filename, ascii=False):
        dtype = []
        N = -1
        if self.positions is not None:
            N = len(self.positions)
            dtype += [('x', 'f4'), ('y', 'f4'), ('z', 'f4')]
        if self.colors is not None:
            N = len(self.colors) if N == -1 else N
            dtype += [('red', 'u1'), ('green', 'u1'), ('blue', 'u1')]
        if self.normals is not None:
            N = len(self.normals) if N == -1 else N
            dtype += [('nx', 'f4'), ('ny', 'f4'), ('nz', 'f4')]

        error_msg = "Lengths of positions, colors, and normals must match."
        if self.positions is not None and N != len(self.positions):
            raise RuntimeError(error_msg)
        if self.colors is not None and N != len(self.colors):
            raise RuntimeError(error_msg)
        if self.normals is not None and N != len(self.normals):
            raise RuntimeError(error_msg)

        vertex = np.zeros((N,), dtype=dtype)

        if self.positions is not None:
            vertex['x'] = self.positions[:, 0].astype('f4')
            vertex['y'] = self.positions[:, 1].astype('f4')
            vertex['z'] = self.positions[:, 2].astype('f4')

        if self.colors is not None:
            self.colors = np.array(self.colors)
            if self.colors.shape == (N,) or self.colors.shape == (N, 1):
                vertex['red'] = self.colors.squeeze().astype('u1')
                vertex['green'] = self.colors.squeeze().astype('u1')
                vertex['blue'] = self.colors.squeeze().astype('u1')
            elif self.colors.shape == (N, 3):
                vertex['red'] = self.colors[:, 0].astype('u1')
                vertex['green'] = self.colors[:, 1].astype('u1')
                vertex['blue'] = self.colors[:, 2].astype('u1')

        if self.normals is not None:
            vertex['nx'] = self.normals[:, 0].astype('f4')
            vertex['ny'] = self.normals[:, 1].astype('f4')
            vertex['nz'] = self.normals[:, 2].astype('f4')

        vertex = plyfile.PlyElement.describe(vertex, 'vertex')

        ext = filename.split('.')[-1]
        if ext != "ply" and ext != "PLY":
            filename = filename + '.ply'
        plyfile.PlyData([vertex], text=ascii).write(filename)
        return self

    def readPLY(self, filename):
        self.__init__()

        vertex = plyfile.PlyData.read(filename)['vertex']

        with warnings.catch_warnings():
            # numpy does not like to .view() into structured array
            warnings.simplefilter("ignore")

            if all([p in vertex.data.dtype.names for p in ('x', 'y', 'z')]):
                position_data = vertex.data[['x', 'y', 'z']]
                N = len(position_data.dtype.names)
                self.positions = position_data.view((position_data.dtype[0],
                                                     N))

            colored = all([p in vertex.data.dtype.names
                           for p in ('red', 'green', 'blue')])
            if colored:
                color_data = vertex.data[['red', 'green', 'blue']]
                N = len(color_data.dtype.names)
                self.colors = color_data.view((color_data.dtype[0], N))

            if all([p in vertex.data.dtype.names for p in ('nx', 'ny', 'nz')]):
                normal_data = vertex.data[['nx', 'ny', 'nz']]
                N = len(normal_data.dtype.names)
                self.normals = normal_data.view((normal_data.dtype[0], N))
        return self
