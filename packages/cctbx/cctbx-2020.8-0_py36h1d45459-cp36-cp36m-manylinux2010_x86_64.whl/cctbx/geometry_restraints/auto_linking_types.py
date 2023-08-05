from __future__ import absolute_import, division, print_function

bond_origin_ids = {}
angle_origin_ids = {}
torsion_origin_ids = {}
chiral_origin_ids = {}
plane_origin_ids = {}
parallelity_origin_ids = {}
origin_ids = [bond_origin_ids,
              angle_origin_ids,
              torsion_origin_ids,
              plane_origin_ids,
              chiral_origin_ids,
              parallelity_origin_ids,
              ]

class origins(list):
  def __init__(self, item, internals=None):
    self.internals = internals
    for i, l in enumerate(item):
      self.append(l)
      if i==3:
        self.header = l

  def __repr__(self):
    return list.__repr__(self) + ' is %s' % self.internals

starting_id = 0
for link_info in [
    ['covalent geometry', [0,1,2,3,4,5]],
    ['SS BOND', # short desc.
     # complete desc.
     'Disulphide bond for CYS-like sulphur atoms within 3A (default) using '
     'values determined from hi-res structures and published in CCN. '
     'Some bonds are automatically excluded based on distance from metals.',
     # citation
     'Comput. Cryst. Newsl. (2015), 6, 13-13.',
     # geo file header - bond, angle, dihedral (None will suppress output)
     ['Disulphide bridge']*3,
     # internals
     [0,1,2], # does not seem to be used much...
    ],
    ['hydrogen bonds',
     'hydrogen bonds added both for protein SS and NA basepairs',
     '',
     ['Bond-like', 'Secondary Structure restraints around h-bond'],
     [0,1],
    ],
    ['metal coordination',
     '',
     '',
     ['Metal coordination']*2,
     [0,1],
    ],
    ['edits',
     '',
     'www.phenix-online.org/documentation/reference/refinement.html#definition-of-custom-bonds-and-angles',
     ['User supplied']*4+[None, 'User supplied'],
     [0,1,2,3,5],
    ],
    # ['glycosidic',
    #  'Standard glycosidic CIF link blocks such as link_??? and ???',
    #  '',
    #  ['Standard Glycosidic']*5, # includes chirals!!!
    #  [0,1,2,3,4],
    # ],
    ['glycosidic custom',
     'Custom glycosidic links need to be generated when the atom names of '
     '''the carbohydrates don't conform to the standard.''',
     '',
     ['Custom Glycosidic']*5,
     [0,1,2,3,4],
    ],
    ['basepair stacking',
     'Enforces parallel between two bases in the sequence',
     'J. Appl. Cryst. 48, 1130-1141 (2015).',
     [None, None, None, None, None, 'Stacking parallelity'],
     [5],
    ],
    ['basepair parallelity',
     'Enforces parallel between two base pairs in paired bases',
     'J. Appl. Cryst. 48, 1130-1141 (2015).',
     [None, None, None, None, None, 'Basepair parallelity'],
     [5],
    ],
    ['basepair planarity',
     'Enforces planrity of two base pairs in paired bases',
     'J. Appl. Cryst. 48, 1130-1141 (2015).',
     [None, None, None, 'xxx', 'Basepair planarity'],
     [3],
    ],
    # ['trans peptide link',
    # 'Applying the standard TRANS peptide link to a non-standard peptide',
    # '',
    # ['Trans Peptide']*3+[None],
    # [0,1,2,4]
    # ]
    ['Misc. bond',
     'Bond created based on atom type and distance.',
     '',
     ['Misc.']*5,
     [0,1,2,3,4]
    ],
    ]:
  for oi in origin_ids:
    assert starting_id not in oi
    oi[starting_id] = origins(link_info[:-1], internals=link_info[-1])
  starting_id+=1

# only angles
for link_info in []:
  angle_origin_ids[starting_id] = origins(link_info, internals=[1])
  starting_id+=1

# only dihedrals
for link_info in [
    ['C-beta',
     'C-beta restraints are (only) dihedrals used by default',
     '',
     [None, None, 'C-Beta improper'],
     ],
    ['chi angles',
     'Torsion restraints on chi angles (side-chain rotamers)',
     '',
     [None, None, 'Side chain'],
     ],
  ]:
  torsion_origin_ids[starting_id] = origins(link_info, internals=[2])
  starting_id+=1

from cctbx.geometry_restraints.standard_cif_links import standard_cif_links
for scl in standard_cif_links:
  assert starting_id not in origin_ids[0]
  origin_ids[0][starting_id] = origins(scl, internals=[0,1,2,3,4,5])
  starting_id+=1

# for oi in origin_ids:
#   print '-'*80
#   for key, item in oi.items():
#     print key
#     print item

if __name__=="__main__":
  print('-'*80)
  print(bond_origin_ids)
  print('-'*80)
  print(angle_origin_ids)
  print('-'*80)
  print(torsion_origin_ids)
  print('-'*80)
  print(parallelity_origin_ids)
