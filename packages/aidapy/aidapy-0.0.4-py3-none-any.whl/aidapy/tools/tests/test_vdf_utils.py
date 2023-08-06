"""
Unit tests for mms_vdf methods.
"""
import numpy as np
import pytest
import aidapy.tools.vdf_utils as vdfu


def test_interpolate_cart_vdf():
    """Unit test on vdfu.vdf.interpolate_cart_vdf method."""
    reso=4
    vdf_obj = vdfu.vdf(v_max=1., resolution=reso, grid_geom='spher')
    gird_cart_data = np.mgrid[-2:2:6j, -2:2:6j, -2:2:6j]
    vdf0 = np.ones((6, 6, 6))
    vdf_obj.interpolate_cart_vdf(gird_cart_data, vdf0, interpolate='near')
    assert vdf_obj.vdf_interp.shape == (reso, reso, reso)
    assert(np.all(vdf_obj.vdf_interp==1.))
    vdf_obj.interpolate_cart_vdf(gird_cart_data, vdf0, interpolate='lin')
    assert vdf_obj.vdf_interp.shape == (reso, reso, reso)
    assert(np.allclose(vdf_obj.vdf_interp, np.ones_like(vdf_obj.vdf_interp)))


def test_interpolate_spher_vdf():
    """Unit test on vdfu.vdf.interpolate_spher_vdf method."""
    reso=4
    vdf_obj = vdfu.vdf(v_max=1., resolution=reso, grid_geom='spher')
    grid_spher_data = np.mgrid[2:0:6j, 0:np.pi:6j, 0:2*np.pi:6j]
    vdf0 = np.ones((6, 6, 6))
    vdf_obj.interpolate_spher_vdf(grid_spher_data, vdf0, interpolate='near')
    assert vdf_obj.vdf_interp.shape == (reso, reso, reso)
    assert(np.allclose(vdf_obj.vdf_interp, np.ones_like(vdf_obj.vdf_interp)))
    vdf_obj.interpolate_spher_vdf(grid_spher_data, vdf0, interpolate='lin')
    assert vdf_obj.vdf_interp.shape == (reso, reso, reso)
    assert(np.allclose(vdf_obj.vdf_interp, np.ones_like(vdf_obj.vdf_interp)*2))


def test_transform_grid():
    """Unit test on vdfu.vdf.transform_grid() method."""
    reso=4
    vdf_obj = vdfu.vdf(v_max=1., resolution=reso, grid_geom='cart')
    vdf_obj.transform_grid(R=None, v=np.array([1., 0., 0.]))
    assert(np.allclose(vdf_obj.grid_cart_t+np.array([1., 0., 0.])[:,None,None,None], vdf_obj.grid_cart))
    vdf_obj = vdfu.vdf(v_max=1., resolution=reso, grid_geom='cart')
    vdf_obj.transform_grid(R=np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]]), v=None)
    assert(np.allclose(vdf_obj.grid_cart_t[2], vdf_obj.grid_cart[2]))


def test_vdf_scaled():
    """Unit test for vdf_scaled method."""
    vdf0 = (np.random.random((4, 4, 4))-.5)*7.
    vdf_sca = vdfu.vdf_scaled(vdf0)
    assert(np.all(np.amin(vdf_sca, axis=(1, 2))==0.))
    assert(np.all(np.amax(vdf_sca, axis=(1, 2))==1.))


def test_init_grid():
    """Unit test on vdfu.init_grid method."""
    reso = 4
    grid_cart, grid_spher, grid_cyl, \
    dvvv = vdfu.init_grid(v_max=1., resolution=reso,
                          grid_geom='cart')
    assert grid_cart.shape == (3, reso, reso, reso)
    assert grid_spher.shape == (3, reso, reso, reso)
    assert grid_cyl.shape == (3, reso, reso, reso)
    assert dvvv.shape == (reso, reso, reso)
    # Testing that the grid values are strictly increasing.
    assert np.all(grid_cart[0][1:] > grid_cart[0][:-1])
    assert np.all(grid_cart[1][:, 1:] > grid_cart[1][:, :-1])
    assert np.all(grid_cart[2][:, :, 1:] > grid_cart[2][:, :, :-1])
    # Testing that grid_cart and grid_spher are one and the same grid.
    assert np.allclose(grid_spher, vdfu.cart2spher(grid_cart))
    assert np.allclose(grid_cyl, vdfu.cart2cyl(grid_cart))

    grid_cart, grid_spher, grid_cyl, \
    dvvv = vdfu.init_grid(v_max=1., resolution=reso,
                          grid_geom='spher')
    assert grid_cart.shape == (3, reso, reso, reso)
    assert grid_spher.shape == (3, reso, reso, reso)
    assert grid_cyl.shape == (3, reso, reso, reso)
    assert dvvv.shape == (reso, reso, reso)
    # Testing that the grid values are strictly increasing.
    assert np.all(grid_spher[0][1:] > grid_spher[0][:-1])
    assert np.all(grid_spher[1][:, 1:] > grid_spher[1][:, :-1])
    assert np.all(grid_spher[2][:, :, 1:] > grid_spher[2][:, :, :-1])
    # Testing that grid_cart and grid_spher are one and the same grid.
    assert np.allclose(grid_spher, vdfu.cart2spher(grid_cart))
    assert np.allclose(grid_cyl, vdfu.cart2cyl(grid_cart))

    grid_cart, grid_spher, grid_cyl, \
    dvvv = vdfu.init_grid(v_max=1., resolution=reso,
                          grid_geom='cyl')
    assert grid_cart.shape == (3, reso, reso, reso)
    assert grid_spher.shape == (3, reso, reso, reso)
    assert grid_cyl.shape == (3, reso, reso, reso)
    assert dvvv.shape == (reso, reso, reso)
    # Testing that the grid values are strictly increasing.
    assert np.all(grid_cyl[0][1:] > grid_cyl[0][:-1])
    assert np.all(grid_cyl[1][:, 1:] > grid_cyl[1][:, :-1])
    assert np.all(grid_cyl[2][:, :, 1:] > grid_cyl[2][:, :, :-1])
    # Testing that grid_cart and grid_spher are one and the same grid.
    assert np.allclose(grid_spher, vdfu.cart2spher(grid_cart))
    assert np.allclose(grid_cyl, vdfu.cart2cyl(grid_cart))


def test_R_2vect():
    """Unit test on vdfu.R_2vect method."""
    vec_a = np.array([1, 0, 0])
    vec_b = np.array([0, 1, 0])
    R = vdfu.R_2vect(vec_a, vec_b)
    # Right shape.
    assert R.shape == (3, 3)
    # Rotation around z-axis.
    assert R[2, 2] == 1.


def test_spher2cart():
    """Unit test on vdfu.spher2cart method."""
    reso = 5
    grid_spher_dummy = np.ones((3, reso, reso, reso))
    grid_cart = vdfu.spher2cart(grid_spher_dummy)
    assert grid_cart.shape == (3, reso, reso, reso)
    assert np.allclose(grid_spher_dummy, vdfu.cart2spher(grid_cart))


def test_cart2spher():
    """Unit test on vdfu.cart2spher method."""
    reso = 5
    grid_cart_dummy = np.ones((3, reso, reso, reso))
    grid_spher = vdfu.cart2spher(grid_cart_dummy)
    assert grid_spher.shape == (3, reso, reso, reso)
    assert np.allclose(grid_cart_dummy, vdfu.spher2cart(grid_spher))


def test_cyl2cart():
    """Unit test on vdfu.cyl2cart method."""
    reso = 5
    grid_cart_dummy = np.ones((3, reso, reso, reso))
    grid_cyl = vdfu.cart2cyl(grid_cart_dummy)
    assert grid_cyl.shape == (3, reso, reso, reso)
    assert np.allclose(grid_cart_dummy, vdfu.cyl2cart(grid_cyl))


def test_cart2cyl():
    """Unit test on vdfu.cart2cyl method."""
    reso = 5
    grid_cyl_dummy = np.ones((3, reso, reso, reso))
    grid_cart = vdfu.cyl2cart(grid_cyl_dummy)
    assert grid_cart.shape == (3, reso, reso, reso)
    assert np.allclose(grid_cyl_dummy, vdfu.cart2cyl(grid_cart))
