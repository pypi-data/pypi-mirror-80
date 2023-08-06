import math
import numpy as np
from scipy.interpolate import RegularGridInterpolator, NearestNDInterpolator,\
    LinearNDInterpolator


class vdf:
    """docstring
    """
    def __init__(self, v_max, resolution, grid_geom):
        """docstring
        """
        self.grid_cart = None
        self.grid_spher = None
        self.grid_cyl = None
        self.dvvv = None
        self.vdf_interp = np.zeros((resolution, resolution, resolution))
        self.grid_cart, self.grid_spher, self.grid_cyl,\
        self.dvvv = init_grid(v_max, resolution, grid_geom)
        self.grid_cart_t = self.grid_cart.copy()
        self.grid_spher_t = self.grid_spher.copy()
        self.nb_counts = np.zeros((resolution, resolution, resolution))

    def interpolate_cart_vdf(self, grid, vdf0, interpolate='near'):
        """docstring
        """
        if interpolate == 'near':
            method_str = 'nearest'
        elif interpolate == 'lin':
            method_str = 'linear'

        if interpolate in ['near', 'lin']:
            if vdf0.ndim == 2:
                grd = (grid[0, :, 0], grid[1, 0, :])
                interpFunc = RegularGridInterpolator(grd, vdf0,
                                                     bounds_error=False,
                                                     method=method_str,
                                                     fill_value=np.nan)
                d = interpFunc(self.grid_cart_t[[0, 2], :, :, 0].reshape(2, -1).T)
                d = d.reshape((self.vdf_interp.shape[0], self.vdf_interp.shape[0]))
                self.vdf_interp = d[:, :, None]
            elif vdf0.ndim == 3:
                grd = (grid[0, :, 0, 0], grid[1, 0, :, 0], grid[2, 0, 0, :])
                interpFunc = RegularGridInterpolator(grd, vdf0,
                                                     bounds_error=False,
                                                     method=method_str,
                                                     fill_value=np.nan)
                d = interpFunc(self.grid_cart_t.reshape(3, -1).T)
                ## (res,res,res)
                self.vdf_interp = d.T.reshape(self.vdf_interp.shape)

    def interpolate_spher_vdf(self, grid, vdf0, interpolate='near'):
        """docstring
        """
        speed = grid[0, :, 0, 0][::-1].copy()
        theta = grid[1, 0, :, 0].copy()
        phi = grid[2, 0, 0, :].copy()
        vdf0 = np.flip(vdf0, axis=0)

        if interpolate == 'near':
            interp_method = 'nearest'
        elif interpolate == 'lin':
            interp_method = 'linear'

        interpFunc = RegularGridInterpolator((speed, theta, phi),
                                             vdf0, bounds_error=False,
                                             method=interp_method,
                                             fill_value=np.nan)
        d = interpFunc(self.grid_spher_t.reshape(3, -1).T)
        d = d.T.reshape(self.vdf_interp.shape)
        d[np.isnan(d)] = 0.
        self.nb_counts += (~np.isnan(d))
        self.vdf_interp += d

    def transform_grid(self, R=None, v=None, s=None):
        """docstring
        """
        if R is not None:
            gc = self.grid_cart_t.copy()
            self.grid_cart_t = np.dot(R, gc.reshape(3, -1)).reshape(self.grid_cart.shape)

        if v is not None:
            gc = self.grid_cart.copy()
            self.grid_cart_t = gc - v[:, None, None, None]

        self.grid_spher_t = cart2spher(self.grid_cart_t)


def vdf_scaled(vdf):
    """0-to-1 scaling of a vdf. Must be given over a spherical grid.
    """
    ds = vdf - np.nanmin(vdf, axis=(1, 2))[:, None, None]
    ds /= np.nanmax(ds, axis=(1, 2))[:, None, None]
    return ds


def init_grid(v_max, resolution, grid_geom):
    """Here we define the bin edges and centers, depending on the chosen
    coordinate system."""
    if grid_geom == 'cart':
        edgesX = np.linspace(-v_max, v_max, resolution + 1,
                             dtype=np.float32)
        centersX = (edgesX[:-1] + edgesX[1:]) * .5
        # 3 x res x res_phi x res/2
        grid_cart = np.mgrid[-v_max:v_max:resolution*1j,
                             -v_max:v_max:resolution*1j,
                             -v_max:v_max:resolution*1j]
        grid_cart = grid_cart.astype(np.float32)
        grid_spher = cart2spher(grid_cart)
        grid_cyl = cart2cyl(grid_cart)
        dv = centersX[1]-centersX[0]
        dvvv = np.ones((resolution, resolution, resolution)) * dv ** 3

    elif grid_geom == 'spher':
        edges_rho = np.linspace(0, v_max, resolution + 1, dtype=np.float32)
        edges_theta = np.linspace(0, np.pi, resolution + 1,
                                  dtype=np.float32)
        edges_phi = np.linspace(0, 2*np.pi, resolution + 1,
                                dtype=np.float32)
        centers_rho = (edges_rho[:-1] + edges_rho[1:]) * .5
        centers_theta = (edges_theta[:-1] + edges_theta[1:]) * .5
        centers_phi = (edges_phi[:-1] + edges_phi[1:]) * .5
        grid_spher = np.mgrid[centers_rho[0]:centers_rho[-1]:centers_rho.size*1j,
                              centers_theta[0]:centers_theta[-1]:centers_theta.size*1j,
                              centers_phi[0]:centers_phi[-1]:centers_phi.size*1j]
        grid_spher = grid_spher.astype(np.float32)
        grid_cart = spher2cart(grid_spher)
        grid_cyl = cart2cyl(grid_cart)
        d_rho = centers_rho[1]-centers_rho[0]
        d_theta = centers_theta[1]-centers_theta[0]
        d_phi = centers_phi[1]-centers_phi[0]
        dv = centers_rho[1]-centers_rho[0]
        dvvv = np.ones((resolution, resolution, resolution)) \
        * centers_rho[:, None, None] * d_rho * d_theta * d_phi

    elif grid_geom == 'cyl':
        edges_rho = np.linspace(0, v_max, resolution+1, dtype=np.float32)
        edges_phi = np.linspace(0, 2*np.pi, resolution+1, dtype=np.float32)
        edges_z = np.linspace(-v_max, v_max, resolution+1, dtype=np.float32)
        centers_rho = (edges_rho[:-1]+edges_rho[1:])*.5
        centers_phi = (edges_phi[:-1]+edges_phi[1:])*.5
        centers_z = (edges_z[:-1]+edges_z[1:])*.5
        grid_cyl = np.mgrid[centers_rho[0]:centers_rho[-1]:centers_rho.size*1j,
                            centers_phi[0]:centers_phi[-1]:centers_phi.size*1j,
                            centers_z[0]:centers_z[-1]:centers_z.size*1j]
        grid_cyl = grid_cyl.astype(np.float32)
        grid_cart = cyl2cart(grid_cyl)
        grid_spher = cart2spher(grid_cart)
        dRho = centers_rho[1]-centers_rho[0]
        dPhi = centers_phi[1]-centers_phi[0]
        dZ = centers_z[1]-centers_z[0]
        dvvv = np.ones((resolution, resolution, resolution)) \
        * centers_rho[:, None, None]*dRho*dPhi*dZ

    return grid_cart, grid_spher, grid_cyl, dvvv


def spher2cart(v_spher):
    """Coordinate system conversion
    """
    v_cart = np.zeros_like(v_spher)
    v_cart[0] = v_spher[0] * np.sin(v_spher[1]) * np.cos(v_spher[2])
    v_cart[1] = v_spher[0] * np.sin(v_spher[1]) * np.sin(v_spher[2])
    v_cart[2] = v_spher[0] * np.cos(v_spher[1])

    return v_cart


def cart2spher(v_cart):
    """Coordinate system conversion
    """
    v_spher = np.zeros_like(v_cart)
    v_spher[0] = np.sqrt(np.sum(v_cart ** 2, axis=0))
    v_spher[1] = np.arccos(v_cart[2] / v_spher[0])
    v_spher[2] = np.arctan2(v_cart[1], v_cart[0])
    itm = (v_spher[2] < 0.)
    v_spher[2][itm] += 2*np.pi

    return v_spher


def cyl2cart(v_cyl):
    """Coordinate system conversion
    """
    v_cart = np.zeros_like(v_cyl)
    v_cart[0] = v_cyl[0]*np.cos(v_cyl[1])
    v_cart[1] = v_cyl[0]*np.sin(v_cyl[1])
    v_cart[2] = v_cyl[2].copy()

    return v_cart


def cart2cyl(v_cart):
    """Coordinate system conversion
    """
    v_cyl = np.zeros_like(v_cart)
    v_cyl[0] = np.sqrt(v_cart[0]**2+v_cart[1]**2)
    v_cyl[1] = np.arctan2(v_cart[1], v_cart[0])
    v_cyl[2] = v_cart[2].copy()
    itm = (v_cyl[1] < 0.)
    v_cyl[1][itm] += 2*np.pi

    return v_cyl


def R_2vect(vector_orig, vector_fin):
    """
    Taken from:
    https://github.com/Wallacoloo/printipi/blob/master/util/rotation_matrix.py
    Calculate the rotation matrix required to rotate from one vector to another.
    For the rotation of one vector to another, there are an infinit series of
    rotation matrices possible.  Due to axially symmetry, the rotation axis
    can be any vector lying in the symmetry plane between the two vectors.
    Hence the axis-angle convention will be used to construct the matrix
    with the rotation axis defined as the cross product of the two vectors.
    The rotation angle is the arccosine of the dot product of the two unit vectors.
    Given a unit vector parallel to the rotation axis, w = [x, y, z] and the rotation angle a,
    the rotation matrix R is::
              |  1 + (1-cos(a))*(x*x-1)   -z*sin(a)+(1-cos(a))*x*y   y*sin(a)+(1-cos(a))*x*z |
        R  =  |  z*sin(a)+(1-cos(a))*x*y   1 + (1-cos(a))*(y*y-1)   -x*sin(a)+(1-cos(a))*y*z |
              | -y*sin(a)+(1-cos(a))*x*z   x*sin(a)+(1-cos(a))*y*z   1 + (1-cos(a))*(z*z-1)  |


    Parameters
    ----------
    R
        The 3x3 rotation matrix to update.
    vector_orig
        The unrotated vector defined in the reference frame.
    vector_fin
        The rotated vector defined in the reference frame.
    """

    # Convert the vectors to unit vectors.
    vector_orig = vector_orig / np.linalg.norm(vector_orig)
    vector_fin = vector_fin / np.linalg.norm(vector_fin)

    # The rotation axis (normalised).
    axis = np.cross(vector_orig, vector_fin)
    axis_len = np.linalg.norm(axis)
    if axis_len != 0.0:
        axis = axis / axis_len

    # Alias the axis coordinates.
    x = axis[0]
    y = axis[1]
    z = axis[2]

    # The rotation angle.
    angle = math.acos(np.dot(vector_orig, vector_fin))

    # Trig functions (only need to do this maths once!).
    ca = np.cos(angle)
    sa = np.sin(angle)

    # Calculate the rotation matrix elements.
    Rot_mat = np.zeros((3, 3))
    Rot_mat[0, 0] = 1.0 + (1.0 - ca)*(x**2 - 1.0)
    Rot_mat[0, 1] = -z*sa + (1.0 - ca)*x*y
    Rot_mat[0, 2] = y*sa + (1.0 - ca)*x*z
    Rot_mat[1, 0] = z*sa+(1.0 - ca)*x*y
    Rot_mat[1, 1] = 1.0 + (1.0 - ca)*(y**2 - 1.0)
    Rot_mat[1, 2] = -x*sa+(1.0 - ca)*y*z
    Rot_mat[2, 0] = -y*sa+(1.0 - ca)*x*z
    Rot_mat[2, 1] = x*sa+(1.0 - ca)*y*z
    Rot_mat[2, 2] = 1.0 + (1.0 - ca)*(z**2 - 1.0)

    return Rot_mat


def Rx(a, theta):
    """ Rotation around the x-axis of angle theta.
    """
    R = np.array([[1, 0,              0            ],
                  [0, np.cos(theta), -np.sin(theta)],
                  [0, np.sin(theta),  np.cos(theta)]])
    return np.dot(R, a)

def Ry(a, phi):
    """ Rotation around the y-axis of angle phi.
    """
    R = np.array([[np.cos(phi),  0, np.sin(phi) ],
			      [ 0,           1, 0           ],
			      [-np.sin(phi), 0, np.cos(phi)]])
    return np.dot(R, a)

def Rz(a, psi):
    """ Rotation around the z-axis of angle psi.
    """
    R = np.array([[np.cos(psi), -np.sin(psi), 0],
			      [np.sin(psi),  np.cos(psi), 0],
			      [0,            0,           1]])
    return np.dot(R, a)
