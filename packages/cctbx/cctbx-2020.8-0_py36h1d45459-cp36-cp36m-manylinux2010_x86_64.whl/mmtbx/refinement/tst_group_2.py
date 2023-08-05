from __future__ import absolute_import, division, print_function
import iotbx.pdb
import mmtbx.refinement.group
import mmtbx.f_model
from cctbx import miller

pdb_answer_str = """\n
CRYST1   21.937    4.866   23.477  90.00 107.08  90.00 P 1 21 1      2
ATOM      1  N   GLY A   1      -9.009   4.612   6.102  1.00 15.00           N
ATOM      2  CA  GLY A   1      -9.052   4.207   4.651  1.00 15.00           C
ATOM      3  C   GLY A   1      -8.015   3.140   4.419  1.00 15.00           C
ATOM      4  O   GLY A   1      -7.523   2.521   5.381  1.00 15.00           O
ATOM      5  N   ASN A   2      -7.656   2.923   3.155  1.00 15.00           N
ATOM      6  CA  ASN A   2      -6.522   2.038   2.831  1.00 15.00           C
ATOM      7  C   ASN A   2      -5.241   2.537   3.427  1.00 15.00           C
ATOM      8  O   ASN A   2      -4.978   3.742   3.426  1.00 15.00           O
ATOM      9  CB  ASN A   2      -6.346   1.881   1.341  1.00 15.00           C
ATOM     10  CG  ASN A   2      -7.584   1.342   0.692  1.00 15.00           C
ATOM     11  OD1 ASN A   2      -8.025   0.227   1.016  1.00 15.00           O
ATOM     12  ND2 ASN A   2      -8.204   2.155  -0.169  1.00 15.00           N
ATOM     13  N   ASN A   3      -4.438   1.590   3.905  1.00 15.00           N
ATOM     14  CA  ASN A   3      -3.193   1.904   4.589  1.00 15.00           C
ATOM     15  C   ASN A   3      -1.955   1.332   3.895  1.00 15.00           C
ATOM     16  O   ASN A   3      -1.872   0.119   3.648  1.00 15.00           O
ATOM     17  CB  ASN A   3      -3.259   1.378   6.042  1.00 15.00           C
ATOM     18  CG  ASN A   3      -2.006   1.739   6.861  1.00 15.00           C
ATOM     19  OD1 ASN A   3      -1.702   2.925   7.072  1.00 15.00           O
ATOM     20  ND2 ASN A   3      -1.271   0.715   7.306  1.00 15.00           N
ATOM     21  N   GLN A   4      -1.005   2.228   3.598  1.00 15.00           N
ATOM     22  CA  GLN A   4       0.384   1.888   3.199  1.00 15.00           C
ATOM     23  C   GLN A   4       1.435   2.606   4.088  1.00 15.00           C
ATOM     24  O   GLN A   4       1.547   3.843   4.115  1.00 15.00           O
ATOM     25  CB  GLN A   4       0.656   2.148   1.711  1.00 15.00           C
ATOM     26  CG  GLN A   4       1.944   1.458   1.213  1.00 15.00           C
ATOM     27  CD  GLN A   4       2.504   2.044  -0.089  1.00 15.00           C
ATOM     28  OE1 GLN A   4       2.744   3.268  -0.190  1.00 15.00           O
ATOM     29  NE2 GLN A   4       2.750   1.161  -1.091  1.00 15.00           N
ATOM     30  N   GLN A   5       2.154   1.821   4.871  1.00 15.00           N
ATOM     31  CA  GLN A   5       3.270   2.361   5.640  1.00 15.00           C
ATOM     32  C   GLN A   5       4.594   1.768   5.172  1.00 15.00           C
ATOM     33  O   GLN A   5       4.768   0.546   5.054  1.00 15.00           O
ATOM     34  CB  GLN A   5       3.056   2.183   7.147  1.00 15.00           C
ATOM     35  CG  GLN A   5       1.829   2.950   7.647  1.00 15.00           C
ATOM     36  CD  GLN A   5       1.344   2.414   8.954  1.00 15.00           C
ATOM     37  OE1 GLN A   5       0.774   1.325   9.002  1.00 15.00           O
ATOM     38  NE2 GLN A   5       1.549   3.187  10.039  1.00 15.00           N
ATOM     39  N   ASN A   6       5.514   2.664   4.856  1.00 15.00           N
ATOM     40  CA  ASN A   6       6.831   2.310   4.318  1.00 15.00           C
ATOM     41  C   ASN A   6       7.854   2.761   5.324  1.00 15.00           C
ATOM     42  O   ASN A   6       8.219   3.943   5.374  1.00 15.00           O
ATOM     43  CB  ASN A   6       7.065   3.016   2.993  1.00 15.00           C
ATOM     44  CG  ASN A   6       5.961   2.735   2.003  1.00 15.00           C
ATOM     45  OD1 ASN A   6       5.798   1.604   1.551  1.00 15.00           O
ATOM     46  ND2 ASN A   6       5.195   3.747   1.679  1.00 15.00           N
ATOM     47  N   TYR A   7       8.292   1.817   6.147  1.00 15.00           N
ATOM     48  CA  TYR A   7       9.159   2.144   7.299  1.00 15.00           C
ATOM     49  C   TYR A   7      10.603   2.331   6.885  1.00 15.00           C
ATOM     50  O   TYR A   7      11.041   1.811   5.855  1.00 15.00           O
ATOM     51  CB  TYR A   7       9.061   1.065   8.369  1.00 15.00           C
ATOM     52  CG  TYR A   7       7.665   0.929   8.902  1.00 15.00           C
ATOM     53  CD1 TYR A   7       6.771   0.021   8.327  1.00 15.00           C
ATOM     54  CD2 TYR A   7       7.210   1.756   9.920  1.00 15.00           C
ATOM     55  CE1 TYR A   7       5.480  -0.094   8.796  1.00 15.00           C
ATOM     56  CE2 TYR A   7       5.904   1.649  10.416  1.00 15.00           C
ATOM     57  CZ  TYR A   7       5.047   0.729   9.831  1.00 15.00           C
ATOM     58  OH  TYR A   7       3.766   0.589  10.291  1.00 15.00           O
ATOM     59  OXT TYR A   7      11.358   2.999   7.612  1.00 15.00           O
END
"""

pdb_poor_adp_str = """\n
CRYST1   21.937    4.866   23.477  90.00 107.08  90.00 P 1 21 1      2
ATOM      1  N   GLY A   1      -9.009   4.612   6.102  1.00  0.01           N
ATOM      2  CA  GLY A   1      -9.052   4.207   4.651  1.00  0.01           C
ATOM      3  C   GLY A   1      -8.015   3.140   4.419  1.00  0.01           C
ATOM      4  O   GLY A   1      -7.523   2.521   5.381  1.00  0.01           O
ATOM      5  N   ASN A   2      -7.656   2.923   3.155  1.00495.00           N
ATOM      6  CA  ASN A   2      -6.522   2.038   2.831  1.00495.00           C
ATOM      7  C   ASN A   2      -5.241   2.537   3.427  1.00495.00           C
ATOM      8  O   ASN A   2      -4.978   3.742   3.426  1.00495.00           O
ATOM      9  CB  ASN A   2      -6.346   1.881   1.341  1.00495.00           C
ATOM     10  CG  ASN A   2      -7.584   1.342   0.692  1.00495.00           C
ATOM     11  OD1 ASN A   2      -8.025   0.227   1.016  1.00495.00           O
ATOM     12  ND2 ASN A   2      -8.204   2.155  -0.169  1.00495.00           N
ATOM     13  N   ASN A   3      -4.438   1.590   3.905  1.00  2.00           N
ATOM     14  CA  ASN A   3      -3.193   1.904   4.589  1.00  2.00           C
ATOM     15  C   ASN A   3      -1.955   1.332   3.895  1.00  2.00           C
ATOM     16  O   ASN A   3      -1.872   0.119   3.648  1.00  2.00           O
ATOM     17  CB  ASN A   3      -3.259   1.378   6.042  1.00  2.00           C
ATOM     18  CG  ASN A   3      -2.006   1.739   6.861  1.00  2.00           C
ATOM     19  OD1 ASN A   3      -1.702   2.925   7.072  1.00  2.00           O
ATOM     20  ND2 ASN A   3      -1.271   0.715   7.306  1.00  2.00           N
ATOM     21  N   GLN A   4      -1.005   2.228   3.598  1.00385.00           N
ATOM     22  CA  GLN A   4       0.384   1.888   3.199  1.00385.00           C
ATOM     23  C   GLN A   4       1.435   2.606   4.088  1.00385.00           C
ATOM     24  O   GLN A   4       1.547   3.843   4.115  1.00385.00           O
ATOM     25  CB  GLN A   4       0.656   2.148   1.711  1.00385.00           C
ATOM     26  CG  GLN A   4       1.944   1.458   1.213  1.00385.00           C
ATOM     27  CD  GLN A   4       2.504   2.044  -0.089  1.00385.00           C
ATOM     28  OE1 GLN A   4       2.744   3.268  -0.190  1.00385.00           O
ATOM     29  NE2 GLN A   4       2.750   1.161  -1.091  1.00385.00           N
ATOM     30  N   GLN A   5       2.154   1.821   4.871  1.00  0.03           N
ATOM     31  CA  GLN A   5       3.270   2.361   5.640  1.00  0.03           C
ATOM     32  C   GLN A   5       4.594   1.768   5.172  1.00  0.03           C
ATOM     33  O   GLN A   5       4.768   0.546   5.054  1.00  0.03           O
ATOM     34  CB  GLN A   5       3.056   2.183   7.147  1.00  0.03           C
ATOM     35  CG  GLN A   5       1.829   2.950   7.647  1.00  0.03           C
ATOM     36  CD  GLN A   5       1.344   2.414   8.954  1.00  0.03           C
ATOM     37  OE1 GLN A   5       0.774   1.325   9.002  1.00  0.03           O
ATOM     38  NE2 GLN A   5       1.549   3.187  10.039  1.00  0.03           N
ATOM     39  N   ASN A   6       5.514   2.664   4.856  1.00290.00           N
ATOM     40  CA  ASN A   6       6.831   2.310   4.318  1.00290.00           C
ATOM     41  C   ASN A   6       7.854   2.761   5.324  1.00290.00           C
ATOM     42  O   ASN A   6       8.219   3.943   5.374  1.00290.00           O
ATOM     43  CB  ASN A   6       7.065   3.016   2.993  1.00290.00           C
ATOM     44  CG  ASN A   6       5.961   2.735   2.003  1.00290.00           C
ATOM     45  OD1 ASN A   6       5.798   1.604   1.551  1.00290.00           O
ATOM     46  ND2 ASN A   6       5.195   3.747   1.679  1.00290.00           N
ATOM     47  N   TYR A   7       8.292   1.817   6.147  1.00  0.00           N
ATOM     48  CA  TYR A   7       9.159   2.144   7.299  1.00  0.00           C
ATOM     49  C   TYR A   7      10.603   2.331   6.885  1.00  0.00           C
ATOM     50  O   TYR A   7      11.041   1.811   5.855  1.00  0.00           O
ATOM     51  CB  TYR A   7       9.061   1.065   8.369  1.00  0.00           C
ATOM     52  CG  TYR A   7       7.665   0.929   8.902  1.00  0.00           C
ATOM     53  CD1 TYR A   7       6.771   0.021   8.327  1.00  0.00           C
ATOM     54  CD2 TYR A   7       7.210   1.756   9.920  1.00  0.00           C
ATOM     55  CE1 TYR A   7       5.480  -0.094   8.796  1.00  0.00           C
ATOM     56  CE2 TYR A   7       5.904   1.649  10.416  1.00  0.00           C
ATOM     57  CZ  TYR A   7       5.047   0.729   9.831  1.00  0.00           C
ATOM     58  OH  TYR A   7       3.766   0.589  10.291  1.00  0.00           O
ATOM     59  OXT TYR A   7      11.358   2.999   7.612  1.00  0.00           O
END
"""


def run(refine, target, residues_per_window = 1, d_min=2):
  """
  Makes sure this actually work:
  'real-space' ADP refinement by converting the map into 'Fobs' and
  then actually doing usual reciprocal-space refinement. Surprisingly this
  converges to R=0 exactly regardless the resolution. ML does not work perhaps
  becase starting point is too far.
  """
  pdb_inp_poor = iotbx.pdb.input(source_info=None, lines=pdb_poor_adp_str)
  pdb_inp_poor.write_pdb_file(file_name="poor.pdb")
  ph = pdb_inp_poor.construct_hierarchy()
  ph.atoms().reset_i_seq()
  xrs_poor = pdb_inp_poor.xray_structure_simple()
  xrs_answer = iotbx.pdb.input(source_info=None,
    lines=pdb_answer_str).xray_structure_simple()
  ####
  f_obs = xrs_answer.structure_factors(d_min=d_min,algorithm="direct").f_calc()
  mtz_dataset = f_obs.as_mtz_dataset(column_root_label="F-calc")
  fc = abs(f_obs)
  fft_map = f_obs.fft_map(resolution_factor=0.25)
  fft_map.apply_volume_scaling()
  map_data = fft_map.real_map_unpadded()
  complete_set = miller.build_set(
    crystal_symmetry = xrs_answer.crystal_symmetry(),
    anomalous_flag   = False,
    d_min            = d_min)
  f_obs = complete_set.structure_factors_from_map(
    map            = map_data,
    use_scale      = True,
    anomalous_flag = False,
    use_sg         = True)
  f_obs = abs(f_obs)
  ###
  mtz_dataset.add_miller_array(
    miller_array=f_obs,
    column_root_label="F-obs")
  mtz_dataset.add_miller_array(
    miller_array=f_obs.generate_r_free_flags(),
    column_root_label="R-free-flags")
  mtz_object = mtz_dataset.mtz_object()
  mtz_object.write(file_name = "data.mtz")
  ###
  sfp=mmtbx.f_model.sf_and_grads_accuracy_master_params.extract()
  sfp.algorithm="direct"
  fmodel = mmtbx.f_model.manager(
    sf_and_grads_accuracy_params = sfp,
    xray_structure               = xrs_poor,
    f_obs                        = f_obs)
  fmodel.show()
  fmodel.update(target_name=target)
  print("Initial r_work=%6.4f r_free=%6.4f"%(fmodel.r_work(), fmodel.r_free()))
  selections = ph.chunk_selections(residues_per_chunk=residues_per_window)
  rr = mmtbx.refinement.group.manager(
    fmodel                      = fmodel,
    selections                  = selections,
    max_number_of_iterations    = 50,
    number_of_macro_cycles      = 25,
    convergence_test            = True,
    run_finite_differences_test = False,
    refine_adp                  = True,
    use_restraints              = True)
  print("After refinement r_work=%6.4f r_free=%6.4f"%(
    fmodel.r_work(), fmodel.r_free()))
  ph.adopt_xray_structure(fmodel.xray_structure)
  ph.write_pdb_file(file_name="reciprocal_space_refined_group_adp.pdb",
    crystal_symmetry = f_obs.crystal_symmetry())
  r_work = fmodel.r_work()*100
  assert r_work < 0.1, [r_work, target]

if (__name__ == "__main__"):
  run(refine="refine_adp", target="ls_wunit_k1")
