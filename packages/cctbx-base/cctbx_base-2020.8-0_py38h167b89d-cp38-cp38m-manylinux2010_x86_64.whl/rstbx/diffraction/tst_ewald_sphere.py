from __future__ import absolute_import, division, print_function
#!/usr/bin/env python
import math

from cctbx.uctbx import unit_cell
from scitbx import matrix
from rstbx.diffraction import rotation_angles, reflection_prediction
from rstbx.bpcx import sensor
from libtbx.test_utils import approx_equal
from six.moves import range

# This script (provided by Graeme Winter) will take the quartz structure and
# simulate a rotation around the 0 0 1 reflection and  1 0 1 reflection.
# If there is a problem then scatter will not be of 1/lambda length. test
# structure will be quartz 5.01, 5.01, 5.47, 90, 90, 120.

def rotation_scattering(reflections, UB_mat, rotation_vector,
                        wavelength, resolution,
                        assert_non_integer_index = False):
    '''Perform some kind of calculation...'''

    ra = rotation_angles(resolution, UB_mat, wavelength, rotation_vector)
    beam_vector = matrix.col([0, 0, 1 / wavelength])

    for hkl in reflections:
        if ra(hkl):
            omegas = ra.get_intersection_angles()
            if assert_non_integer_index:
                assert ra.H[0] != int(ra.H[0]) or \
                       ra.H[1] != int(ra.H[1]) or \
                       ra.H[2] != int(ra.H[2])

            for omegaidx in [0,1]:

                rot_mat = rotation_vector.axis_and_angle_as_r3_rotation_matrix(
                    omegas[omegaidx])
                assert(
                    -0.0001 < math.fabs(rot_mat.determinant() - 1.0) < 0.0001)

                H1 = (rot_mat * UB_mat)*hkl
                H1 =  H1 + beam_vector
                len_H1 = math.sqrt((H1[0] * H1[0]) +
                                   (H1[1] * H1[1]) +
                                   (H1[2] * H1[2]))

                if math.fabs(len_H1 - 1.0 / wavelength) > 0.0001:
                    raise RuntimeError('length error for %d %d %d' % hkl)

def scattering_prediction(reflections, UB_mat, rotation_vector,
                          wavelength, resolution,
                          assert_non_integer_index = False):
    '''Test the reflection_prediction class.'''

    ra = rotation_angles(resolution, UB_mat, wavelength, rotation_vector)
    beam_vector = matrix.col([0, 0, 1 / wavelength])

    detector_size = 100
    detector_distance = 100

    s =  sensor(matrix.col((- 0.5 * detector_size,
                            - 0.5 * detector_size,
                            detector_distance)),
                matrix.col((1, 0, 0)),
                matrix.col((0, 1, 0)),
                (0, detector_size), (0, detector_size))
    rp = reflection_prediction(rotation_vector, beam_vector, UB_mat, s)

    for hkl in reflections:
        if ra(hkl):
            omegas = ra.get_intersection_angles()
            if assert_non_integer_index:
                assert ra.H[0] != int(ra.H[0]) or \
                       ra.H[1] != int(ra.H[1]) or \
                       ra.H[2] != int(ra.H[2])

            for omegaidx in [0,1]:

                rot_mat = rotation_vector.axis_and_angle_as_r3_rotation_matrix(
                    omegas[omegaidx])

                assert(math.fabs(rot_mat.determinant() - 1.0) < 0.0001)

                H1 = (rot_mat * UB_mat)*hkl
                H1 =  H1 + beam_vector
                len_H1 = math.sqrt((H1[0] * H1[0]) +
                                   (H1[1] * H1[1]) +
                                   (H1[2] * H1[2]))

                if math.fabs(len_H1 - 1.0 / wavelength) > 0.0001:
                    raise RuntimeError('length error for %d %d %d' % hkl)

                if rp(hkl, omegas[omegaidx]):
                    x, y = rp.get_prediction()
                    assert(0 < x < detector_size)
                    assert(0 < y < detector_size)

if __name__ == '__main__':

    wavelength = 1.2
    resolution = 1.5

    uc = unit_cell([5.01, 5.01, 5.47, 90.0, 90.0, 120.0])

    bmat = matrix.sqr(uc.orthogonalization_matrix()).inverse().transpose()

    #----------------------------
    # prove that the matrix bmat is consistent with the ewald_sphere class
    # requirements:
    #               / A*x B*x C*x \
    #  Matrix A* =  | A*y B*y C*y |
    #               \ A*z B*z C*z /

    uc_reciprocal = uc.reciprocal()
    astar,bstar,cstar,alphastar,betastar,gammastar = uc_reciprocal.parameters()
    astar_vec = matrix.col([bmat[0],bmat[3],bmat[6]])
    bstar_vec = matrix.col([bmat[1],bmat[4],bmat[7]])
    cstar_vec = matrix.col([bmat[2],bmat[5],bmat[8]])

    assert approx_equal(astar, math.sqrt(astar_vec.dot(astar_vec)))
    assert approx_equal(bstar, math.sqrt(bstar_vec.dot(bstar_vec)))
    assert approx_equal(cstar, math.sqrt(cstar_vec.dot(cstar_vec)))
    assert approx_equal(bstar*cstar*math.cos(math.pi*alphastar/180),
                        bstar_vec.dot(cstar_vec))
    assert approx_equal(cstar*astar*math.cos(math.pi*betastar/180),
                        cstar_vec.dot(astar_vec))
    assert approx_equal(astar*bstar*math.cos(math.pi*gammastar/180),
                        astar_vec.dot(bstar_vec))

    # proof complete, bmat == A*
    #----------------------------

    first_rotation_vector = matrix.col([1, 0, 0])
    second_rotation_vector = matrix.col([1, 0, 1])

    maxh, maxk, maxl = uc.max_miller_indices(resolution)

    indices = []
    for h in range(-maxh, maxh + 1):
        for k in range(-maxk, maxk + 1):
            for l in range(-maxl, maxl + 1):
                indices.append((h, k, l))

    rotation_scattering(indices, bmat, first_rotation_vector,
                        wavelength, resolution)

    rotation_scattering(indices, bmat, second_rotation_vector,
                        wavelength, resolution)

    # Now repeat the entire excercise for some non-integer Miller indices

    float_indices = []
    for h in range(-maxh, maxh + 1):
        for k in range(-maxk, maxk + 1):
            for l in range(-maxl, maxl + 1):
                float_indices.append((h+0.2, k+0.2, l+0.2))

    rotation_scattering(float_indices, bmat, first_rotation_vector,
                        wavelength, resolution,
                        assert_non_integer_index = True)

    rotation_scattering(float_indices, bmat, second_rotation_vector,
                        wavelength, resolution,
                        assert_non_integer_index = True)


    scattering_prediction(indices, bmat, second_rotation_vector,
                          wavelength, resolution)
    print("OK")
