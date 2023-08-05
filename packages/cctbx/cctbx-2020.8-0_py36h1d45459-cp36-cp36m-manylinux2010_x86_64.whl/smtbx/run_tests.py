from __future__ import absolute_import, division, print_function

from libtbx import test_utils
from libtbx.test_utils.pytest import discover
import libtbx.load_env

tst_list = [
    ["$D/absolute_structure/tests/tst_absolute_structure.py",
     "--fix_random_seeds"],
    "$D/ab_initio/tests/tst_ab_initio_ext.py",
    ["$D/ab_initio/tests/tst_charge_flipping.py", '--fix_seed', '--on=E',
     '"hall: P 1"', '"hall: P 3"', '"hall: -P 2ybc"' ],
    "$D/masks/tests/tst_masks.py",
    "$D/structure_factors/direct/tests/tst_standard_xray.py",
    ["$D/refinement/tests/tst_weighting_schemes.py",
     "--fix_random_seeds"],
    "$D/refinement/constraints/tests/tst_lbfgs.py",
    "$B/refinement/constraints/tests/tst_reparametrisation",
    "$B/refinement/constraints/tests/tst_geometrical_hydrogens",
    "$B/refinement/constraints/tests/tst_special_position",
    "$D/refinement/constraints/tests/tst_reparametrisation.py",
    ["$D/refinement/constraints/tests/tst_constrained_structure.py",
     '--normal_eqns_solving_method=naive'],
    ["$D/refinement/constraints/tests/tst_constrained_structure.py",
     '--normal_eqns_solving_method=levenberg-marquardt'],
    ["$D/refinement/restraints/tests/tst_restraints.py",
     '--verbose', '--scatterers=5', '--resolution=0.2'],
    "$D/regression/tst_commandline_refine.py",
    "$D/regression/tst_commandline_anomrefine.py",
] + discover()

# unstable test
tst_list_expected_unstable = [
  "$D/refinement/tests/tst_least_squares.py",
  ]

def run():
  build_dir = libtbx.env.under_build("smtbx")
  dist_dir = libtbx.env.dist_path("smtbx")
  test_utils.run_tests(build_dir, dist_dir, tst_list)

if __name__ == '__main__':
  run()
