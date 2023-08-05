from __future__ import absolute_import, division, print_function
from cctbx.array_family import flex # import dependency
from cctbx.eltbx import wavelengths, tiny_pse
from cctbx import adptbx
from six.moves import range

centric_implies_centrosymmetric_error_msg = """\
If the structure is centrosymmetric, the origin MUST lie on a center of
symmetry.
"""

both_iso_and_aniso_in_use_error_msg = """\
ShelX supports only the specification either of u_iso or of u_aniso,
each one excluding the other"""

def generator(xray_structure,
              data_are_intensities=True,
              title=None,
              wavelength=None,
              temperature=None,
              full_matrix_least_squares_cycles=None,
              conjugate_gradient_least_squares_cycles=None,
              overall_scale_factor=None,
              weighting_scheme_params=None,
              sort_scatterers=True,
              unit_cell_dims=None,
              unit_cell_esds=None
              ):
  space_group = xray_structure.space_group()
  assert not space_group.is_centric() or space_group.is_origin_centric(),\
         centric_implies_centrosymmetric_error_msg
  assert [full_matrix_least_squares_cycles,
          conjugate_gradient_least_squares_cycles].count(None) in (0, 1)
  if title is None:
    title = '????'
  if wavelength is None:
    wavelength = wavelengths.characteristic('Mo').as_angstrom()
  sgi = xray_structure.space_group_info()
  uc = xray_structure.unit_cell()

  yield 'TITL %s in %s\n' % (title, sgi.type().lookup_symbol())
  if unit_cell_dims is None:
    unit_cell_dims = uc.parameters()
  yield 'CELL %.5f %s\n' % (
    wavelength,
    ' '.join(('%.4f ',)*3 + ('%.3f',)*3) % unit_cell_dims)
  if unit_cell_esds:
    yield 'ZERR %i %f %f %f %f %f %f\n' % ((sgi.group().order_z(),) + unit_cell_esds)
  else:
    yield 'ZERR %i 0. 0. 0. 0. 0. 0.\n' % sgi.group().order_z()

  latt = 1 + 'PIRFABC'.find(sgi.group().conventional_centring_type_symbol())
  if not space_group.is_origin_centric(): latt = -latt
  yield 'LATT %i\n' % latt
  for i in range(space_group.n_smx()):
    rt_mx = space_group(0, 0, i)
    if rt_mx.is_unit_mx(): continue
    yield 'SYMM %s\n' % rt_mx
  yield '\n'

  uc_content = xray_structure.unit_cell_content()
  for e in uc_content:
    uc_content[e] = "%.1f" % uc_content[e]
  sfac = []
  unit = []
  prior = ('C', 'H')
  for e in prior:
    if e in uc_content:
      sfac.append(e)
      unit.append(uc_content[e])
  dsu = [ (tiny_pse.table(e).atomic_number(), e) for e in uc_content ]
  dsu.sort()
  sorted = [ item[-1] for item in dsu ]
  for e in sorted:
    if (e not in prior):
      sfac.append(e)
      unit.append(uc_content[e])
  yield 'SFAC %s\n' % ' '.join(sfac)
  for e in sfac:
    yield 'DISP %s 0 0 0\n' % e
  yield 'UNIT %s\n' % ' '.join(unit)
  sf_idx = dict([ (e, i + 1) for i, e in enumerate(sfac) ])
  yield '\n'

  if temperature:
    yield 'TEMP %.0f\n' % temperature

  if full_matrix_least_squares_cycles:
    yield 'L.S. %i\n' % full_matrix_least_squares_cycles

  if conjugate_gradient_least_squares_cycles:
    yield 'CGLS %i\n' % conjugate_gradient_least_squares_cycles

  yield '\n'

  if weighting_scheme_params is not None:
    if (isinstance(weighting_scheme_params, str)):
      yield 'WGHT %s\n' % weighting_scheme_params
    else:
      a, b = weighting_scheme_params
      if b is None:
        yield 'WGHT %.6f\n' % a
      else:
        yield 'WGHT %.6f %.6f\n' % (a, b)

  if overall_scale_factor is not None:
    yield 'FVAR %.8f\n' % overall_scale_factor

  fmt_tmpl = ('%-4s', '%2i') + ('%11.6f',)*3 + ('%11.5f',)
  fmt_iso = ' '.join(fmt_tmpl + ('%10.5f',))
  fmt_aniso = ' '.join(fmt_tmpl + ('%.5f',)*2 + ('=\n ',) + ('%.5f',)*4)
  if sort_scatterers:
    dsu = [ (tiny_pse.table(sc.scattering_type).atomic_number(), sc)
            for sc in xray_structure.scatterers() ]
    dsu.sort(reverse=True)
    scatterers = flex.xray_scatterer([ item[-1] for item in dsu ])
  else:
    scatterers = xray_structure.scatterers()
  atomname_set = set()
  for sc in scatterers:
    assert sc.fp == 0 # not implemented
    assert sc.fdp == 0 # not implemented
    assert sc.flags.use_u_iso() ^ sc.flags.use_u_aniso(),\
           both_iso_and_aniso_in_use_error_msg
    atomname = sc.label.strip()
    assert len(atomname) != 0
    assert len(atomname) <= 4
    if (atomname in atomname_set):
      raise RuntimeError('Duplicate atom name: "%s"' % atomname)
    atomname_set.add(atomname)
    params = (atomname, sf_idx[sc.scattering_type]) + sc.site
    occ = sc.weight()
    if not sc.flags.grad_occupancy(): occ += 10
    params += (occ, )
    if sc.flags.use_u_iso():
      yield fmt_iso % (params + (sc.u_iso,)) + "\n"
    else:
      u11, u22, u33, u12, u13, u23 = adptbx.u_star_as_u_cif(uc, sc.u_star)
      yield fmt_aniso % (params + (u11, u22, u33, u23, u13, u12)) + "\n"

  if data_are_intensities: hklf = 4
  else: hklf = 3
  yield 'HKLF %i\n' % hklf
