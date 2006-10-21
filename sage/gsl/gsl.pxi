include "math.pxi"
cdef enum:
  GSL_SUCCESS = 0

#ctypedef int size_t
include "gsl_mode.pxi"
include "gsl_math.pxi"
include "gsl_complex.pxi"
include "gsl_poly.pxi"
include "gsl_sf_result.pxi"
include "gsl_airy.pxi"
include "gsl_bessel.pxi"
include "gsl_clausen.pxi"
include "gsl_coulomb.pxi"
include "gsl_coupling.pxi"
include "gsl_dawson.pxi"
include "gsl_debye.pxi"
include "gsl_dilog.pxi"
include "gsl_elementary.pxi"
include "gsl_ellint.pxi"
include "gsl_elljac.pxi"
include "gsl_erf.pxi"
include "gsl_exp.pxi"
include "gsl_expint.pxi"
include "gsl_fermi_dirac.pxi"
include "gsl_gamma.pxi"
include "gsl_gegenbauer.pxi"
include "gsl_hyperg.pxi"
include "gsl_laguerre.pxi"
include "gsl_lambert.pxi"
include "gsl_legendre.pxi"
include "gsl_log.pxi"
include "gsl_pow_int.pxi"
include "gsl_psi.pxi"
include "gsl_synchrotron.pxi"
include "gsl_transport.pxi"
include "gsl_trig.pxi"
include "gsl_zeta.pxi"

include "gsl_block.pxi"
include "gsl_vector.pxi"
include "gsl_vector_complex.pxi"
include "gsl_matrix.pxi"
include "gsl_matrix_complex.pxi"

include "gsl_permutation.pxi"
include "gsl_combination.pxi"
include "gsl_sort.pxi"

include "gsl_blas.pxi"
include "gsl_linalg.pxi"
include "gsl_eigen.pxi"
include "gsl_fft.pxi"
include "gsl_integration.pxi"
include "gsl_rng.pxi"
include "gsl_qrng.pxi"
include "gsl_random.pxi"
include "gsl_statistics.pxi"
include "gsl_histogram.pxi"
include "gsl_ntuple.pxi"
include "gsl_monte.pxi"
include "gsl_odeiv.pxi"
include "gsl_interp.pxi"
include "gsl_diff.pxi"
include "gsl_chebyshev.pxi"
include "gsl_sum.pxi"
include "gsl_roots.pxi"
include "gsl_min.pxi"
include "gsl_fit.pxi"
include "gsl_errno.pxi"
