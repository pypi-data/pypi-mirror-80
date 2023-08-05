from __future__ import absolute_import, division, print_function

import os

import iotbx.phil
import libtbx.load_env
import libtbx.phil
import mmtbx.model

from cctbx import crystal
from libtbx.program_template import ProgramTemplate
from libtbx.utils import null_out, Sorry
from mmtbx.command_line.maps import run as make_map
from iotbx.data_manager import DataManager
from six.moves import zip

# -----------------------------------------------------------------------------
def test_data_manager():
  a = DataManager(['model'])

  a.add_model('a', 'b')
  a.add_model('c', 'd')
  assert a.get_model() == 'b'
  assert a.get_model('a') == 'b'
  assert a.get_model('c') == 'd'
  assert a.get_model_names() == ['a', 'c']

  assert a.has_models()
  assert a.has_models(exact_count=True, expected_n=2)
  assert not a.has_models(expected_n=3, raise_sorry=False)

  # exporting phil
  working_phil = a.export_phil_scope()
  assert len(working_phil.extract().data_manager.model) == 2

  # data tracking
  try:
    a.has_models(expected_n=3, raise_sorry=True)
  except Sorry:
    pass

  try:
    a.has_models(exact_count=True, raise_sorry=True)
  except Sorry:
    pass

  a.set_default_model('c')
  assert a.get_model() == 'd'

  assert a.get_model_names() == ['a', 'c'] or a.get_model_names() == ['c', 'a']

  a.remove_model('c')
  try:
    a.get_model()
  except Sorry:
    pass
  try:
    a.get_model('missing')
  except Sorry:
    pass
  try:
    a.set_default_model('missing')
  except Sorry:
    pass

  a = DataManager(datatypes=['sequence', 'phil'])
  assert a.get_sequence_names() == []
  assert not hasattr(a, 'get_model')

  # phil functions
  test_phil_str = '''
data_manager {
  phil_files = data_manager_test.eff
}
'''
  with open('data_manager_test.eff', 'w') as f:
    f.write(test_phil_str)

  # loading file with get function
  assert len(a.get_phil_names()) == 0
  p = a.get_phil('data_manager_test.eff')
  assert type(p) == libtbx.phil.scope
  assert 'data_manager_test.eff' in a.get_phil_names()

  # loading file with phil
  a = DataManager(datatypes=['phil'])
  test_phil = iotbx.phil.parse(test_phil_str)
  a.load_phil_scope(test_phil)

  assert 'data_manager_test.eff' in a.get_phil_names()
  assert a.get_default_phil_name() == 'data_manager_test.eff'

  os.remove('data_manager_test.eff')

  # writing
  a = DataManager(datatypes=['model', 'phil', 'sequence'])
  a.add_model('a','b')
  a.add_phil('c','d')
  a.add_sequence('e','f')

  a.write_model_file(a.get_model(), filename='a.dat', overwrite=True)
  a.write_phil_file(a.get_phil(), filename='c.dat', overwrite=True)
  a.write_sequence_file(a.get_sequence(), filename='e.dat', overwrite=True)

  with open('a.dat', 'r') as f:
    lines = f.readlines()
  assert lines[0] == 'b'

  os.remove('a.dat')
  os.remove('c.dat')
  os.remove('e.dat')

# -----------------------------------------------------------------------------
def test_model_datatype():
  import mmtbx.monomer_library.server
  try:
    mon_lib_srv = mmtbx.monomer_library.server.server()
  except mmtbx.monomer_library.server.MonomerLibraryServerError:
    print("Can not initialize monomer_library, skipping test_model_datatype.")
    return

  # 1yjp
  model_str = '''
CRYST1   21.937    4.866   23.477  90.00 107.08  90.00 P 1 21 1      2
ORIGX1      1.000000  0.000000  0.000000        0.00000
ORIGX2      0.000000  1.000000  0.000000        0.00000
ORIGX3      0.000000  0.000000  1.000000        0.00000
SCALE1      0.045585  0.000000  0.014006        0.00000
SCALE2      0.000000  0.205508  0.000000        0.00000
SCALE3      0.000000  0.000000  0.044560        0.00000
ATOM      1  N   GLY A   1      -9.009   4.612   6.102  1.00 16.77           N
ATOM      2  CA  GLY A   1      -9.052   4.207   4.651  1.00 16.57           C
ATOM      3  C   GLY A   1      -8.015   3.140   4.419  1.00 16.16           C
ATOM      4  O   GLY A   1      -7.523   2.521   5.381  1.00 16.78           O
ATOM      5  N   ASN A   2      -7.656   2.923   3.155  1.00 15.02           N
ATOM      6  CA  ASN A   2      -6.522   2.038   2.831  1.00 14.10           C
ATOM      7  C   ASN A   2      -5.241   2.537   3.427  1.00 13.13           C
ATOM      8  O   ASN A   2      -4.978   3.742   3.426  1.00 11.91           O
ATOM      9  CB  ASN A   2      -6.346   1.881   1.341  1.00 15.38           C
ATOM     10  CG  ASN A   2      -7.584   1.342   0.692  1.00 14.08           C
ATOM     11  OD1 ASN A   2      -8.025   0.227   1.016  1.00 17.46           O
ATOM     12  ND2 ASN A   2      -8.204   2.155  -0.169  1.00 11.72           N
ATOM     13  N   ASN A   3      -4.438   1.590   3.905  1.00 12.26           N
ATOM     14  CA  ASN A   3      -3.193   1.904   4.589  1.00 11.74           C
ATOM     15  C   ASN A   3      -1.955   1.332   3.895  1.00 11.10           C
ATOM     16  O   ASN A   3      -1.872   0.119   3.648  1.00 10.42           O
ATOM     17  CB  ASN A   3      -3.259   1.378   6.042  1.00 12.15           C
ATOM     18  CG  ASN A   3      -2.006   1.739   6.861  1.00 12.82           C
ATOM     19  OD1 ASN A   3      -1.702   2.925   7.072  1.00 15.05           O
ATOM     20  ND2 ASN A   3      -1.271   0.715   7.306  1.00 13.48           N
ATOM     21  N   GLN A   4      -1.005   2.228   3.598  1.00 10.29           N
ATOM     22  CA  GLN A   4       0.384   1.888   3.199  1.00 10.53           C
ATOM     23  C   GLN A   4       1.435   2.606   4.088  1.00 10.24           C
ATOM     24  O   GLN A   4       1.547   3.843   4.115  1.00  8.86           O
ATOM     25  CB  GLN A   4       0.656   2.148   1.711  1.00  9.80           C
ATOM     26  CG  GLN A   4       1.944   1.458   1.213  1.00 10.25           C
ATOM     27  CD  GLN A   4       2.504   2.044  -0.089  1.00 12.43           C
ATOM     28  OE1 GLN A   4       2.744   3.268  -0.190  1.00 14.62           O
ATOM     29  NE2 GLN A   4       2.750   1.161  -1.091  1.00  9.05           N
ATOM     30  N   GLN A   5       2.154   1.821   4.871  1.00 10.38           N
ATOM     31  CA  GLN A   5       3.270   2.361   5.640  1.00 11.39           C
ATOM     32  C   GLN A   5       4.594   1.768   5.172  1.00 11.52           C
ATOM     33  O   GLN A   5       4.768   0.546   5.054  1.00 12.05           O
ATOM     34  CB  GLN A   5       3.056   2.183   7.147  1.00 11.96           C
ATOM     35  CG  GLN A   5       1.829   2.950   7.647  1.00 10.81           C
ATOM     36  CD  GLN A   5       1.344   2.414   8.954  1.00 13.10           C
ATOM     37  OE1 GLN A   5       0.774   1.325   9.002  1.00 10.65           O
ATOM     38  NE2 GLN A   5       1.549   3.187  10.039  1.00 12.30           N
ATOM     39  N   ASN A   6       5.514   2.664   4.856  1.00 11.99           N
ATOM     40  CA  ASN A   6       6.831   2.310   4.318  1.00 12.30           C
ATOM     41  C   ASN A   6       7.854   2.761   5.324  1.00 13.40           C
ATOM     42  O   ASN A   6       8.219   3.943   5.374  1.00 13.92           O
ATOM     43  CB  ASN A   6       7.065   3.016   2.993  1.00 12.13           C
ATOM     44  CG  ASN A   6       5.961   2.735   2.003  1.00 12.77           C
ATOM     45  OD1 ASN A   6       5.798   1.604   1.551  1.00 14.27           O
ATOM     46  ND2 ASN A   6       5.195   3.747   1.679  1.00 10.07           N
ATOM     47  N   TYR A   7       8.292   1.817   6.147  1.00 14.70           N
ATOM     48  CA  TYR A   7       9.159   2.144   7.299  1.00 15.18           C
ATOM     49  C   TYR A   7      10.603   2.331   6.885  1.00 15.91           C
ATOM     50  O   TYR A   7      11.041   1.811   5.855  1.00 15.76           O
ATOM     51  CB  TYR A   7       9.061   1.065   8.369  1.00 15.35           C
ATOM     52  CG  TYR A   7       7.665   0.929   8.902  1.00 14.45           C
ATOM     53  CD1 TYR A   7       6.771   0.021   8.327  1.00 15.68           C
ATOM     54  CD2 TYR A   7       7.210   1.756   9.920  1.00 14.80           C
ATOM     55  CE1 TYR A   7       5.480  -0.094   8.796  1.00 13.46           C
ATOM     56  CE2 TYR A   7       5.904   1.649  10.416  1.00 14.33           C
ATOM     57  CZ  TYR A   7       5.047   0.729   9.831  1.00 15.09           C
ATOM     58  OH  TYR A   7       3.766   0.589  10.291  1.00 14.39           O
ATOM     59  OXT TYR A   7      11.358   2.999   7.612  1.00 17.49           O
TER      60      TYR A   7
HETATM   61  O   HOH A   8      -6.471   5.227   7.124  1.00 22.62           O
HETATM   62  O   HOH A   9      10.431   1.858   3.216  1.00 19.71           O
HETATM   63  O   HOH A  10     -11.286   1.756  -1.468  1.00 17.08           O
HETATM   64  O   HOH A  11      11.808   4.179   9.970  1.00 23.99           O
HETATM   65  O   HOH A  12      13.605   1.327   9.198  1.00 26.17           O
HETATM   66  O   HOH A  13      -2.749   3.429  10.024  1.00 39.15           O
HETATM   67  O   HOH A  14      -1.500   0.682  10.967  1.00 43.49           O
MASTER      238    0    0    0    0    0    0    6   66    1    0    1
END
'''

  # test reading/writing PDB
  test_filename = 'test_model.pdb'
  test_output_filename = 'test_model_output.pdb'
  test_eff = 'model.eff'
  dm = DataManager(['model'])
  dm.process_model_str(test_filename, model_str)
  dm.write_model_file(model_str, filename=test_output_filename, overwrite=True)
  m = dm.get_model(test_output_filename)
  assert test_output_filename in dm.get_model_names()
  dm.write_model_file(m, overwrite=True)
  pdb_filename = 'cctbx_program.pdb'
  assert os.path.exists(pdb_filename)
  dm.process_model_file(pdb_filename)
  assert not dm.get_model(pdb_filename).input_model_format_cif()
  dm.write_model_file(m, test_filename, overwrite=True)

  # test reading PDB writing CIF
  test_filename = 'test_model.pdb'
  test_output_filename = 'test_model.cif'
  dm = DataManager(['model'])
  dm.process_model_str(test_filename, model_str)
  m = dm.get_model(test_filename)
  dm.write_model_file(m, filename=test_output_filename, format='cif',
      overwrite=True)
  m = dm.get_model(test_output_filename)
  assert test_output_filename in dm.get_model_names()
  dm.write_model_file(m, overwrite=True)
  cif_filename = 'cctbx_program.cif'
  assert os.path.exists(cif_filename)
  dm.process_model_file(cif_filename)
  assert dm.get_model(cif_filename).input_model_format_cif()

  # test type
  assert dm.get_model_type() == 'x_ray'
  dm.set_model_type(test_filename, 'neutron')
  assert dm.get_model_type() == 'neutron'
  phil_scope = dm.export_phil_scope()
  extract = phil_scope.extract()
  assert extract.data_manager.model[0].type == 'neutron'
  with open(test_eff, 'w') as f:
    f.write(phil_scope.as_str())
  new_phil_scope = iotbx.phil.parse(file_name=test_eff)
  new_dm = DataManager(['model'])
  new_dm.load_phil_scope(new_phil_scope)
  assert new_dm.get_model_type(test_filename) == 'neutron'
  new_dm = DataManager(['model'])
  try:
    new_dm.set_default_model_type('nonsense')
  except Sorry:
    pass
  new_dm.set_default_model_type('electron')
  new_dm.process_model_file(test_filename)
  assert new_dm.get_model_type() == 'electron'
  assert len(new_dm.get_model_names()) == 1
  assert len(new_dm.get_model_names(model_type='electron')) == 1
  assert len(new_dm.get_model_names(model_type='neutron')) == 0

  os.remove(test_eff)
  os.remove(test_filename)

  # test reading/writing CIF
  test_filename = 'test_model_datatype.cif'
  dm.write_model_file(dm.get_model().model_as_mmcif(),
                      filename=test_filename, overwrite=True)
  dm.process_model_file(test_filename)
  os.remove(test_filename)
  assert test_filename in dm.get_model_names()
  m = dm.get_model(test_filename)
  dm.write_model_file(m, overwrite=True)
  cif_filename = 'cctbx_program.cif'
  assert os.path.exists(cif_filename)
  dm.process_model_file(cif_filename)
  assert dm.get_model(cif_filename).input_model_format_cif()
  os.remove(pdb_filename)
  os.remove(cif_filename)

  # test pdb_interpretation
  extract = mmtbx.model.manager.get_default_pdb_interpretation_params()
  extract.pdb_interpretation.use_neutron_distances = True
  dm.update_pdb_interpretation_for_model(test_filename, extract)
  assert dm.get_model(test_filename).restraints_manager is None

# -----------------------------------------------------------------------------
def test_model_and_restraint():

  # from 3tpj
  model_str = '''
CRYST1  104.428  128.690   76.662  90.00  90.00  90.00 C 2 2 21
ATOM   5877  O   URE A 403     -37.796 -38.296   5.693  1.00 15.43           O
ATOM   5878  C   URE A 403     -36.624 -38.509   5.800  1.00 20.53           C
ATOM   5879  N2  URE A 403     -36.191 -39.836   6.120  1.00 27.82           N
ATOM   5880  N1  URE A 403     -35.679 -37.450   5.644  1.00 21.36           N
ATOM   5881 HN11 URE A 403     -34.792 -37.617   5.732  1.00 25.63           H
ATOM   5882 HN12 URE A 403     -35.965 -36.613   5.445  1.00 25.63           H
ATOM   5883 HN21 URE A 403     -35.307 -40.015   6.211  1.00 33.38           H
ATOM   5884 HN22 URE A 403     -36.801 -40.499   6.221  1.00 33.38           H
'''

  restraint_str = '''
#
data_comp_list
loop_
_chem_comp.id
_chem_comp.three_letter_code
_chem_comp.name
_chem_comp.group
_chem_comp.number_atoms_all
_chem_comp.number_atoms_nh
_chem_comp.desc_level
URE URE Unknown                   ligand 8 4 .
#
data_comp_URE
#
loop_
_chem_comp_atom.comp_id
_chem_comp_atom.atom_id
_chem_comp_atom.type_symbol
_chem_comp_atom.type_energy
_chem_comp_atom.partial_charge
_chem_comp_atom.x
_chem_comp_atom.y
_chem_comp_atom.z
URE        C       C   C     .          0.4968   -0.0000   -0.0000
URE        O       O   O     .          1.7184   -0.0000   -0.0000
URE        N1      N   NH2   .         -0.2180   -0.0000    1.2381
URE        N2      N   NH2   .         -0.2180    0.0000   -1.2381
URE        HN11    H   HNH2  .          0.2355   -0.0000    2.0237
URE        HN12    H   HNH2  .         -1.1251    0.0000    1.2382
URE        HN21    H   HNH2  .          0.2355    0.0000   -2.0237
URE        HN22    H   HNH2  .         -1.1251   -0.0000   -1.2382
#
loop_
_chem_comp_bond.comp_id
_chem_comp_bond.atom_id_1
_chem_comp_bond.atom_id_2
_chem_comp_bond.type
_chem_comp_bond.value_dist
_chem_comp_bond.value_dist_esd
URE  C       O      double        1.222 0.020
URE  C       N1     single        1.430 0.020
URE  C       N2     single        1.430 0.020
URE  N1      HN11   single        0.907 0.020
URE  N1      HN12   single        0.907 0.020
URE  N2      HN21   single        0.907 0.020
URE  N2      HN22   single        0.907 0.020
#
loop_
_chem_comp_angle.comp_id
_chem_comp_angle.atom_id_1
_chem_comp_angle.atom_id_2
_chem_comp_angle.atom_id_3
_chem_comp_angle.value_angle
_chem_comp_angle.value_angle_esd
URE  N2      C       N1           120.00 3.000
URE  N2      C       O            120.00 3.000
URE  N1      C       O            120.00 3.000
URE  HN12    N1      HN11         120.00 3.000
URE  HN12    N1      C            120.00 3.000
URE  HN11    N1      C            120.00 3.000
URE  HN22    N2      HN21         120.00 3.000
URE  HN22    N2      C            120.00 3.000
URE  HN21    N2      C            120.00 3.000
#
loop_
_chem_comp_tor.comp_id
_chem_comp_tor.id
_chem_comp_tor.atom_id_1
_chem_comp_tor.atom_id_2
_chem_comp_tor.atom_id_3
_chem_comp_tor.atom_id_4
_chem_comp_tor.value_angle
_chem_comp_tor.value_angle_esd
_chem_comp_tor.period
URE CONST_01      HN11    N1      C       O              0.00   0.0 0
URE CONST_02      HN12    N1      C       O            180.00   0.0 0
URE CONST_03      HN21    N2      C       O             -0.00   0.0 0
URE CONST_04      HN22    N2      C       O            180.00   0.0 0
URE CONST_05      HN21    N2      C       N1           180.00   0.0 0
URE CONST_06      HN22    N2      C       N1            -0.00   0.0 0
URE CONST_07      HN11    N1      C       N2          -180.00   0.0 0
URE CONST_08      HN12    N1      C       N2            -0.00   0.0 0
#
loop_
_chem_comp_plane_atom.comp_id
_chem_comp_plane_atom.plane_id
_chem_comp_plane_atom.atom_id
_chem_comp_plane_atom.dist_esd
URE plan-1  C      0.020
URE plan-1  O      0.020
URE plan-1  N1     0.020
URE plan-1  N2     0.020
URE plan-1  HN11   0.020
URE plan-1  HN12   0.020
URE plan-1  HN21   0.020
URE plan-1  HN22   0.020
'''

  model_filename = 'ure.pdb'
  restraint_filename = 'ure.cif'

  dm = DataManager(['model', 'restraint'])
  dm.write_model_file(model_str, filename=model_filename, overwrite=True)
  dm.write_restraint_file(restraint_str, filename=restraint_filename,
                          overwrite=True)

  # fails because no restraints are loaded
  dm.process_model_file(model_filename)
  model = dm.get_model()
  try:
    model.get_restraints_manager()
  except Sorry:
    pass

  # automatically add restraints
  dm.process_restraint_file(restraint_filename)
  model = dm.get_model()
  model.get_restraints_manager()

  os.remove(model_filename)
  os.remove(restraint_filename)

# -----------------------------------------------------------------------------
def test_sequence_datatype():

  # 1sar.fa
  seq_filename = 'test_seq.fa'
  seq_str = '''>1SAR A
DVSGTVCLSALPPEATDTLNLIASDGPFPYSQDGVVFQNRESVLPTQSYGYYHEYTVITPGARTRGTRRIICGEATQEDY
YTGDHYATFSLIDQTC
'''

  with open(seq_filename, 'w') as f:
    f.write(seq_str)

  dm = DataManager(['sequence'])
  dm.process_sequence_file(seq_filename)
  assert seq_filename in dm.get_sequence_names()

  seq = dm.get_sequence()
  new_str = dm.get_sequence_as_string(seq_filename)
  for a, b in zip(new_str, seq_str):
    assert a == b

  os.remove(seq_filename)

# -----------------------------------------------------------------------------
def test_miller_array_datatype():

  data_dir = os.path.dirname(os.path.abspath(__file__))
  data_mtz = os.path.join(data_dir, 'data',
                          'insulin_unmerged_cutted_from_ccp4.mtz')

  dm = DataManager(['miller_array', 'phil'])
  dm.process_miller_array_file(data_mtz)

  # test labels
  labels = ['M_ISYM', 'BATCH', 'I,SIGI,merged', 'IPR,SIGIPR,merged',
            'FRACTIONCALC', 'XDET', 'YDET', 'ROT', 'WIDTH', 'LP', 'MPART',
            'FLAG', 'BGPKRATIOS']
  for label in dm.get_miller_array_labels():
    assert label in labels

  assert len(dm.get_miller_arrays()) == len(dm.get_miller_array_labels())

  # test access by label
  label = dm.get_miller_array_labels()[3]
  new_label = dm.get_miller_arrays(labels=[label])[0].info().label_string()
  assert label == new_label

  # test custom PHIL
  dm.write_phil_file(dm.export_phil_scope().as_str(),
                     filename='test.phil', overwrite=True)
  loaded_phil = iotbx.phil.parse(file_name='test.phil')
  new_dm = DataManager(['miller_array', 'phil'])
  new_dm.load_phil_scope(loaded_phil)
  assert data_mtz == new_dm.get_default_miller_array_name()
  for label in new_dm.get_miller_array_labels():
    assert label in labels

  os.remove('test.phil')

  # test type
  assert dm.get_miller_array_type() == 'x_ray'
  label = labels[3]
  dm.set_miller_array_type(data_mtz, label, 'electron')
  assert dm.get_miller_array_type(label=label) == 'electron'
  dm.write_phil_file(dm.export_phil_scope().as_str(),
                     filename='test_phil', overwrite=True)
  loaded_phil = iotbx.phil.parse(file_name='test_phil')
  new_dm.load_phil_scope(loaded_phil)
  assert new_dm.get_miller_array_type(label=label) == 'electron'
  new_dm = DataManager(['miller_array'])
  try:
    new_dm.set_default_miller_array_type('q')
  except Sorry:
    pass
  new_dm.set_default_miller_array_type('neutron')
  new_dm.process_miller_array_file(data_mtz)
  assert new_dm.get_miller_array_type(label=label) == 'neutron'

  os.remove('test_phil')

  # test writing file
  arrays = dm.get_miller_arrays()
  dataset = arrays[2].as_mtz_dataset(column_root_label='label1')
  dataset.add_miller_array(miller_array=arrays[3], column_root_label='label2')
  mtz_object = dataset.mtz_object()
  dm.write_miller_array_file(mtz_object, filename='test.mtz', overwrite=True)
  dm.process_miller_array_file('test.mtz')
  new_labels = dm.get_miller_array_labels('test.mtz')
  assert 'label1,SIGlabel1' in new_labels
  assert 'label2,SIGlabel2' in new_labels

  os.remove('test.mtz')

  # test file server
  fs1 = dm.get_reflection_file_server()
  fs2 = dm.get_reflection_file_server([data_mtz, data_mtz])
  assert 2*len(fs1.miller_arrays) == len(fs2.miller_arrays)
  cs = crystal.symmetry(
    unit_cell=dm.get_miller_arrays()[0].crystal_symmetry().unit_cell(),
    space_group_symbol='P1')
  fs = dm.get_reflection_file_server(crystal_symmetry=cs)
  assert fs.crystal_symmetry.is_similar_symmetry(cs)
  assert not fs.crystal_symmetry.is_similar_symmetry(
    dm.get_miller_arrays()[0].crystal_symmetry())
  fs = dm.get_reflection_file_server(labels=['I,SIGI,merged'])
  assert len(fs.get_miller_arrays(None)) == 1
  miller_array = fs.get_amplitudes(None, None, True, None, None)
  assert miller_array.info().label_string() == 'I,as_amplitude_array,merged'

  for label in dm.get_miller_array_labels():
    dm.set_miller_array_type(label=label, array_type='electron')
  fs = dm.get_reflection_file_server(array_type='x_ray')
  assert len(fs.get_miller_arrays(None)) == 0
  fs = dm.get_reflection_file_server(array_type='electron')
  assert len(fs.get_miller_arrays(None)) == 13
  fs = dm.get_reflection_file_server(filenames=[data_mtz],
    labels=[['I,SIGI,merged', 'IPR,SIGIPR,merged']], array_type='neutron')
  assert len(fs.get_miller_arrays(None)) == 0
  for label in ['I,SIGI,merged', 'IPR,SIGIPR,merged']:
    dm.set_miller_array_type(label=label, array_type='x_ray')
  fs = dm.get_reflection_file_server(filenames=[data_mtz],
    labels=[['I,SIGI,merged', 'IPR,SIGIPR,merged']], array_type='x_ray')
  assert len(fs.get_miller_arrays(data_mtz)) == 2
  fs = dm.get_reflection_file_server(filenames=[data_mtz], array_type='x_ray')
  assert len(fs.get_miller_arrays(data_mtz)) == 2
  fs = dm.get_reflection_file_server(filenames=[data_mtz], array_type='electron')
  assert len(fs.get_miller_arrays(data_mtz)) == 11

  # test subset of labels
  label_subset = labels[3:8]
  dm = DataManager(['miller_array', 'phil'])
  dm.process_miller_array_file(data_mtz)
  dm._miller_array_labels[data_mtz] = label_subset
  dm.set_miller_array_type(label=label_subset[2], array_type='electron')
  assert dm.get_miller_array_type(label=label_subset[2]) == 'electron'
  dm.write_phil_file(dm.export_phil_scope().as_str(), filename='test.phil',
                     overwrite=True)
  loaded_phil = iotbx.phil.parse(file_name='test.phil')
  new_dm = DataManager(['miller_array', 'phil'])
  new_dm.load_phil_scope(loaded_phil)
  assert new_dm.get_miller_array_type(label=label_subset[2]) == 'electron'
  fs = new_dm.get_reflection_file_server(array_type='x_ray')
  assert len(fs.get_miller_arrays(None)) == 4
  fs = new_dm.get_reflection_file_server(array_type='electron')
  assert len(fs.get_miller_arrays(None)) == 1
  os.remove('test.phil')

  label_subset = list()
  dm = DataManager(['miller_array', 'phil'])
  dm.process_miller_array_file(data_mtz)
  dm._miller_array_labels[data_mtz] = label_subset
  dm.write_phil_file(dm.export_phil_scope().as_str(), filename='test.phil',
                     overwrite=True)
  loaded_phil = iotbx.phil.parse(file_name='test.phil')
  new_dm = DataManager(['miller_array', 'phil'])
  new_dm.load_phil_scope(loaded_phil)
  fs = new_dm.get_reflection_file_server(array_type='x_ray')
  assert len(fs.get_miller_arrays(None)) == 13
  fs = new_dm.get_reflection_file_server(array_type='electron')
  assert len(fs.get_miller_arrays(None)) == 0
  os.remove('test.phil')

# -----------------------------------------------------------------------------
def test_real_map_datatype():

  data_dir = os.path.dirname(os.path.abspath(__file__))
  data_ccp4 = os.path.join(data_dir, 'data',
                          'non_zero_origin_map.ccp4')

  dm = DataManager(['real_map', 'phil'])
  dm.process_real_map_file(data_ccp4)
  assert dm.has_real_maps()

  # test custom PHIL
  dm.write_phil_file(dm.export_phil_scope().as_str(),
                     filename='test.phil', overwrite=True)
  loaded_phil = iotbx.phil.parse(file_name='test.phil')
  new_dm = DataManager(['real_map', 'phil'])
  new_dm.load_phil_scope(loaded_phil)
  assert data_ccp4 == new_dm.get_default_real_map_name()
  os.remove('test.phil')

  # test writing and reading file
  mm = dm.get_real_map()
  mm.shift_origin()
  dm.write_real_map_file(mm, filename='test.ccp4', overwrite=True)
  dm.process_real_map_file('test.ccp4')
  new_mm = dm.get_real_map('test.ccp4')
  assert not new_mm.is_similar(mm)
  new_mm.shift_origin()
  assert new_mm.is_similar(mm)

  os.remove('test.ccp4')

# -----------------------------------------------------------------------------
def test_map_mixins():
  regression_dir = libtbx.env.find_in_repositories(
    relative_path='phenix_regression/maps')
  if not regression_dir:
    print('Skipping test, phenix_regression missing')
    return

  dm = DataManager(['real_map'])
  assert not hasattr(dm, 'has_real_maps_or_map_coefficients')
  assert hasattr(dm, 'has_real_maps')
  assert not hasattr(dm, 'has_map_coefficients')

  dm = DataManager(['map_coefficients'])
  assert not hasattr(dm, 'has_real_maps_or_map_coefficients')
  assert not hasattr(dm, 'has_real_maps')
  assert hasattr(dm, 'has_map_coefficients')

  dm = DataManager()
  assert hasattr(dm, 'has_real_maps_or_map_coefficients')
  assert hasattr(dm, 'has_real_maps')
  assert hasattr(dm, 'has_map_coefficients')

  cwd = os.getcwd()
  model_file = os.path.join(regression_dir, 'test_maps4.pdb')
  mtz_file = os.path.join(regression_dir, 'test_maps4.mtz')
  make_map([model_file, mtz_file, 'output.directory={cwd}'.format(cwd=cwd),
            'output.prefix=tmm'],
    use_output_directory=False, log=null_out())
  real_map_file = 'tmm_2mFo-DFc_map.ccp4'
  map_coefficients_file = 'tmm_map_coeffs.mtz'

  assert not dm.has_real_maps_or_map_coefficients(expected_n=1, exact_count=True)
  dm.process_real_map_file(real_map_file)
  assert dm.has_real_maps(expected_n=1, exact_count=True)
  assert dm.has_real_maps_or_map_coefficients(expected_n=1, exact_count=True)
  dm.process_map_coefficients_file(map_coefficients_file)
  assert dm.has_map_coefficients(expected_n=1, exact_count=True)
  assert not dm.has_real_maps_or_map_coefficients(expected_n=1, exact_count=True)
  assert dm.has_real_maps_or_map_coefficients(expected_n=1, exact_count=False)
  assert dm.has_real_maps_or_map_coefficients(expected_n=2, exact_count=True)

  os.remove(real_map_file)
  os.remove(map_coefficients_file)

# -----------------------------------------------------------------------------
def test_default_filenames():
  datatypes = ['model', 'ncs_spec', 'phil', 'real_map', 'restraint', 'sequence']
  extensions = ['cif', 'ncs_spec', 'eff', 'mrc', 'cif', 'seq']
  dm = DataManager(datatypes)
  for datatype, extension in zip(datatypes, extensions):
    filename = getattr(dm, 'get_default_output_{datatype}_filename'.
                       format(datatype=datatype))()
    assert filename == 'cctbx_program.' + extension

  filename = dm.get_default_output_model_filename(extension='.abc')
  assert filename == 'cctbx_program.abc'

  class TestProgram(ProgramTemplate):
    master_phil_str = """
output {
  serial = 0
    .type = int
}
"""
  master_phil = iotbx.phil.parse(TestProgram.master_phil_str)
  required_output_phil = iotbx.phil.parse(ProgramTemplate.output_phil_str)
  master_phil.adopt_scope(required_output_phil)
  working_phil = iotbx.phil.parse(ProgramTemplate.master_phil_str)
  params = master_phil.fetch(working_phil).extract()
  p = ProgramTemplate(dm, params, master_phil)
  assert dm.get_default_output_filename() == 'cctbx_program_000'
  dm.set_overwrite(True)
  dm.write_model_file('abc')    # cctbx_program_000.cif
  dm.write_phil_file('123')     # cctbx_program_000.eff
  dm.write_phil_file('456')     # cctbx_program_001.eff
  dm.write_model_file('def')    # cctbx_program_001.cif
  assert dm.get_default_output_filename() == 'cctbx_program_001'
  dm.write_sequence_file('ghi') # cctbx_program_001.seq
  dm.write_sequence_file('hkl') # cctbx_program_002.seq
  assert dm.get_default_output_filename() == 'cctbx_program_002'
  assert os.path.isfile('cctbx_program_000.cif')
  assert os.path.isfile('cctbx_program_001.cif')
  assert os.path.isfile('cctbx_program_000.eff')
  assert os.path.isfile('cctbx_program_001.eff')
  assert os.path.isfile('cctbx_program_001.seq')
  assert os.path.isfile('cctbx_program_002.seq')
  os.remove('cctbx_program_000.cif')
  os.remove('cctbx_program_001.cif')
  os.remove('cctbx_program_000.eff')
  os.remove('cctbx_program_001.eff')
  os.remove('cctbx_program_001.seq')
  os.remove('cctbx_program_002.seq')

  # test output.filename, output.file_name
  assert p.get_default_output_filename() == 'cctbx_program_002'
  assert p.get_default_output_filename(filename='abc') == 'abc'
  working_phil_str = 'output.filename=def'
  working_phil = iotbx.phil.parse(working_phil_str)
  params = master_phil.fetch(working_phil).extract()
  p = ProgramTemplate(dm, params, master_phil)
  assert params.output.filename == params.output.file_name == 'def'
  assert p.get_default_output_filename() == 'def'
  assert dm.get_default_output_filename() == 'def'
  working_phil_str = 'output.file_name=ghi'
  working_phil = iotbx.phil.parse(working_phil_str)
  params = master_phil.fetch(working_phil).extract()
  p = ProgramTemplate(dm, params, master_phil)
  assert params.output.filename == params.output.file_name == 'ghi'
  assert p.get_default_output_filename() == 'ghi'
  assert dm.get_default_output_filename() == 'ghi'

# -----------------------------------------------------------------------------
if __name__ == '__main__':

  test_data_manager()
  test_model_datatype()
  test_sequence_datatype()
  test_miller_array_datatype()
  test_real_map_datatype()
  test_map_mixins()
  test_default_filenames()

  if libtbx.env.find_in_repositories(relative_path='chem_data') is not None:
    test_model_and_restraint()
  else:
    print('Skip test_model_and_restraint, chem_data not available')
  print("OK")
