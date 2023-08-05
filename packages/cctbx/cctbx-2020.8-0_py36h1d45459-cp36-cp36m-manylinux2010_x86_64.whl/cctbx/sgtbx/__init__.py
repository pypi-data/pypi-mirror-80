from __future__ import absolute_import, division, print_function
from cctbx import uctbx

import boost_adaptbx.boost.python as bp
from six.moves import range
from six.moves import zip
ext = bp.import_ext("cctbx_sgtbx_ext")
from cctbx_sgtbx_ext import *

import libtbx

rhombohedral_hermann_mauguin_symbols = [
  "R 3",
  "R -3",
  "R 3 2",
  "R 3 m",
  "R 3 c",
  "R -3 m",
  "R -3 c"]

class empty: pass

from cctbx.array_family import flex
from scitbx import matrix
from boost_adaptbx.boost import rational
import random
import sys

bp.inject(ext.space_group_symbol_iterator, bp.py3_make_iterator)

def vec3_rat_from_str(s):
  flds = s.split(",")
  assert len(flds) == 3
  result = []
  for fld in flds:
    slash_count = fld.count("/")
    assert slash_count < 2
    if (slash_count == 0):
      n, d = int(fld), 1
    else:
      n, d = [int(t) for t in fld.split("/")]
    result.append(rational.int(n, d))
  return result

@bp.inject_into(ext.space_group)
class _():

  def smx(self, with_inversion=False):
    if with_inversion: n = 2*self.n_smx()
    else: n = self.n_smx()
    for i_smx in range(n):
      yield self(i_smx)

  def ltr(self):
    for i in range(self.n_ltr()):
      yield self(i,0,0).t()

  def info(self):
    return space_group_info(group=self)

  def adp_constraints(self):
    return tensor_rank_2_constraints(space_group=self, reciprocal_space=True)

  def cartesian_adp_constraints(self, unit_cell):
    return tensor_rank_2_cartesian_constraints(unit_cell, self)


class any_generator_set(object):

  def __init__(self, space_group,
               z2c_r_den=cb_r_den, z2c_t_den=cb_t_den):
    self.space_group = space_group
    gen_set = ext.any_generator_set(space_group=space_group,
                                    z2p_r_den=cb_r_den,
                                    z2p_t_den=cb_t_den)
    gen_set.set_primitive()
    self.non_primitive_generators = gen_set.z_gen()
    self.primitive_generators = gen_set.p_gen()


class space_group_info(object):

  __safe_for_unpickling__ = True

  def __init__(self,
        symbol=None,
        table_id=None,
        group=None,
        number=None,
        space_group_t_den=None):
    assert [symbol, group, number].count(None) >= 2
    if (number is not None):
      symbol = str(number)
    if (symbol is None):
      assert table_id is None
      if (space_group_t_den is not None):
        assert space_group_t_den == group.t_den()
      self._group = group
    else:
      assert group is None
      if (table_id is None):
        symbols = space_group_symbols(symbol)
      else:
        if (isinstance(symbol, int)): symbol = str(symbol)
        symbols = space_group_symbols(symbol, table_id)
      if (space_group_t_den is None):
        self._group = space_group(
          space_group_symbols=symbols)
      else:
        self._group = space_group(
          space_group_symbols=symbols, t_den=space_group_t_den)
    if (self._group is not None):
      self._group.make_tidy()
    self._space_group_info_cache = empty()

  def _copy_constructor(self, other):
    self._group = other._group
    self._space_group_info_cache = other._space_group_info_cache

  def __getstate__(self):
    return (self._group,)

  def __setstate__(self, state):
    self._group = state[0]
    self._space_group_info_cache = empty()

  def group(self):
    return self._group

  def type(self, tidy_cb_op=True, r_den=None, t_den=None):
    cache = self._space_group_info_cache
    cache_type = getattr(cache, "_type", None)
    if (cache_type is None):
      f = self._group.t_den() // sg_t_den
      if (r_den is None): r_den = f * cb_r_den
      if (t_den is None): t_den = f * cb_t_den
    else:
      cache_type_params = cache._type_params
      if (r_den is None): r_den = cache_type_params[1]
      if (t_den is None): t_den = cache_type_params[2]
    type_params = (tidy_cb_op, r_den, t_den)
    if (cache_type is None or cache_type_params != type_params):
      cache._type_params = type_params
      cache._type = cache_type = space_group_type(*(self._group,)+type_params)
    return cache_type

  def any_generator_set(self):
    cache = self._space_group_info_cache
    try:
      return cache._generators
    except AttributeError:
      cache._generators = any_generator_set(self.group())
      return cache._generators

  def reciprocal_space_asu(self):
    cache = self._space_group_info_cache
    if (not hasattr(cache, "_reciprocal_space_asu")):
      cache._reciprocal_space_asu = reciprocal_space_asu(self.type())
    return cache._reciprocal_space_asu

  def direct_space_asu(self):
    from cctbx.sgtbx.direct_space_asu import reference_table
    cache = self._space_group_info_cache
    if (not hasattr(cache, "_direct_space_asu")):
      reference_asu = reference_table.get_asu(self.type().number())
      cache._direct_space_asu = reference_asu.change_basis(
        self.change_of_basis_op_to_reference_setting().inverse())
    return cache._direct_space_asu

  def brick(self):
    cache = self._space_group_info_cache
    if (not hasattr(cache, "_brick")):
      cache._brick = brick(self.type())
    return cache._brick

  def wyckoff_table(self):
    cache = self._space_group_info_cache
    if (not hasattr(cache, "_wyckoff_table")):
      cache._wyckoff_table = wyckoff_table(self.type())
    return cache._wyckoff_table

  def structure_seminvariants(self):
    cache = self._space_group_info_cache
    if (not hasattr(cache, "_structure_seminvariants")):
      cache._structure_seminvariants = structure_seminvariants(self._group)
    return cache._structure_seminvariants

  def reference_setting(self):
    cache = self._space_group_info_cache
    if (not hasattr(cache, "_reference_setting")):
      cache._reference_setting = space_group_info(symbol=self.type().number())
    return cache._reference_setting

  def change_of_basis_op_to_reference_setting(self):
    return self.type().cb_op()

  def is_reference_setting(self):
    return self.change_of_basis_op_to_reference_setting().is_identity_op()

  def as_reference_setting(self):
    return self.change_basis(self.change_of_basis_op_to_reference_setting())

  def change_basis(self, cb_op):
    if (isinstance(cb_op, str)):
      cb_op = change_of_basis_op(cb_op)
    return space_group_info(group=self.group().change_basis(cb_op))

  def change_of_basis_op_to_other_hand(self):
    return self.type().change_of_hand_op()

  def change_hand(self):
    return self.change_basis(self.change_of_basis_op_to_other_hand())

  def change_of_basis_op_to_primitive_setting(self):
    return self.group().z2p_op()

  def primitive_setting(self):
    return self.change_basis(self.change_of_basis_op_to_primitive_setting())

  def change_of_basis_op_to(self, other):
    """ The change of basis from self to other.
    This method strives to return a mere origin shift.
    """
    self_to_ref_op = self.change_of_basis_op_to_reference_setting()
    other_to_ref_op = other.change_of_basis_op_to_reference_setting()

    # early exit if other is not the same space group in a different setting
    self_as_reference = self.change_basis(self_to_ref_op)
    other_as_reference = other.change_basis(other_to_ref_op)
    if self_as_reference.group() != other_as_reference.group(): return None

    # the obvious answer: if it is a mere shift, return it
    obvious_result = other_to_ref_op.inverse()*self_to_ref_op
    if obvious_result.c().r().is_unit_mx(): return obvious_result

    # otherwise, let's try to find an origin shift by hand
    # see test case exercise_change_of_basis_between_arbitrary_space_groups
    # in regression/tst_sgtbx.py for the motivation for this code.
    self_z2p_op = self.change_of_basis_op_to_primitive_setting()
    other_z2p_op = other.change_of_basis_op_to_primitive_setting()
    primitive_self = self.change_basis(self_z2p_op)
    primitive_other = other.change_basis(other_z2p_op)
    if (   set([ op.r() for op in primitive_self.group() ])
        == set([ op.r() for op in primitive_other.group() ])):
      self_tr_info_for_r = dict([ (op.r(), translation_part_info(op))
                                  for op in primitive_self.group() ])
      origin_shift = matrix.mutable_zeros(3)
      for op in primitive_other.group():
        self_ti = self_tr_info_for_r[op.r()]
        other_ti = translation_part_info(op)
        if self_ti.intrinsic_part() != other_ti.intrinsic_part():
          origin_shift = None
          break
        delta = other_ti.origin_shift().minus(
             self_ti.origin_shift()).mod_positive()
        delta_num = delta.num()
        for i in range(3):
          if origin_shift[i] == 0:
            origin_shift[i] = 24//delta.den()*delta_num[i]
        if origin_shift.elems.count(0) == 0: break
      if origin_shift is not None:
        origin_shift = tr_vec(origin_shift, tr_den=24)
        if not origin_shift.is_zero():
          cb_op = change_of_basis_op(
            rt_mx(origin_shift)).new_denominators(24, 144)
          cb_op = other_z2p_op.inverse()*cb_op*self_z2p_op
          cb_op.mod_positive_in_place()
          tentative_other = self.change_basis(cb_op)
          if tentative_other.group() == other.group():
            return cb_op

    # no origin shift has been found, so return the obvious answer
    return obvious_result

  def reflection_intensity_equivalent_groups(self, anomalous_flag=True):
    result = []
    reference_group = self.reference_setting().group()
    reference_crystal_system = reference_group.crystal_system()
    reference_reflection_intensity_group = reference_group \
      .build_derived_reflection_intensity_group(anomalous_flag=anomalous_flag)
    reference_reflection_intensity_group.make_tidy()
    for space_group_symbols in space_group_symbol_iterator():
      if (space_group_symbols.crystal_system() != reference_crystal_system):
        continue
      other_sg = space_group(space_group_symbols)
      if (other_sg.build_derived_reflection_intensity_group(
            anomalous_flag=anomalous_flag)
          == reference_reflection_intensity_group):
        result.append(other_sg.change_basis(
          self.change_of_basis_op_to_reference_setting().inverse()))
    return result

  def __str__(self):
    cache = self._space_group_info_cache
    if (not hasattr(cache, "_lookup_symbol")):
      cache._lookup_symbol = self.type().lookup_symbol()
    return cache._lookup_symbol

  def __repr__(self):
    cache = self._space_group_info_cache
    if (not hasattr(cache, "_lookup_symbol")):
      cache._lookup_symbol = self.type().lookup_symbol()
    return 'sgtbx.space_group_info(symbol="%s")' % cache._lookup_symbol

  def symbol_and_number(self):
    return "%s (No. %d)" % (str(self), self.type().number())

  def show_summary(self, f=None, prefix="Space group: "):
    if (f is None): f = sys.stdout
    print("%s%s" % (prefix, self.symbol_and_number()), file=f)

  def number_of_continuous_allowed_origin_shifts(self):
    return self.structure_seminvariants() \
      .number_of_continuous_allowed_origin_shifts()

  def subtract_continuous_allowed_origin_shifts(self, translation_frac):
    cb_op = self.change_of_basis_op_to_reference_setting()
    return cb_op.c_inv() * self.reference_setting().structure_seminvariants() \
      .subtract_principal_continuous_shifts(
        translation=cb_op.c() * translation_frac)

  def is_allowed_origin_shift(self, shift, tolerance):
    """
    Determine whether the specified fractional coordinate shift is allowed
    under the space group rules.

    :param shift: tuple specifying fractional coordinate shift
    :param tolerance: tolerance for coordinate shifts outside the allowed
                      range
    :returns: Python boolean
    """
    from libtbx.math_utils import iround
    is_ltr = lambda v: max([ abs(x-iround(x)) for x in v ]) < tolerance
    z2p_op = self.group().z2p_op()
    primitive_self = self.change_basis(z2p_op)
    primitive_shift = z2p_op.c() * shift
    if is_ltr(primitive_shift):
      return True
    for s in primitive_self.any_generator_set().primitive_generators:
      w_m_i = s.r().minus_unit_mx()
      t = w_m_i * primitive_shift
      if not is_ltr(t):
        return False
    else:
      return True

  def any_compatible_unit_cell(self, volume=None, asu_volume=None):
    """
    Generate a unit cell of arbitrary dimensions (optionally filling the
    desired volume) with parameters compatible with the specified space
    group.

    :param volume: desired unit cell volume
    :param asu_volume: desired volume of the asymmetric unit
    :returns: uctbx.unit_cell object
    """
    assert [volume, asu_volume].count(None) == 1
    if (volume is None):
      volume = asu_volume * self.group().order_z()
    sg_number = self.type().number()
    if   (sg_number <   3):
      params = (1., 1.3, 1.7, 83, 109, 129)
    elif (sg_number <  16):
      params = (1., 1.3, 1.7, 90, 109, 90)
    elif (sg_number <  75):
      params = (1., 1.3, 1.7, 90, 90, 90)
    elif (sg_number < 143):
      params = (1., 1., 1.7, 90, 90, 90)
    elif (sg_number < 195):
      params = (1., 1., 1.7, 90, 90, 120)
    else:
      params = (1., 1., 1., 90, 90, 90)
    unit_cell = uctbx.unit_cell(params).change_basis(
      cb_op=self.change_of_basis_op_to_reference_setting().inverse())
    f = (volume / unit_cell.volume())**(1/3.)
    params = list(unit_cell.parameters())
    for i in range(3): params[i] *= f
    return uctbx.unit_cell(params)

  def any_compatible_crystal_symmetry(self, volume=None, asu_volume=None):
    from cctbx import crystal
    return crystal.symmetry(
      unit_cell=self.any_compatible_unit_cell(
        volume=volume, asu_volume=asu_volume),
      space_group_info=self)

  def cif_symmetry_code(self, rt_mx, full_code=False, sep="_"):
    """ The symmetry code for the given rt_mx in the given space group as
        required by the CIF:

        http://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Igeom_angle_site_symmetry_.html

        With the default full_code=False, if the translation term is zero,
        just the index of the symmetry operation is returned.
    """
    group = self._group
    cache = self._space_group_info_cache
    if not hasattr(cache, "_index_lookup_table"):
      lookup = {}
      for i, op in enumerate(group):
        lookup.setdefault(op.r(), {})
        lookup[op.r()][op.t().mod_positive()] = i
      cache._index_lookup_table = lookup
    rt_mx = rt_mx.new_denominators(group.r_den(), group.t_den())
    tr_vecs = cache._index_lookup_table[rt_mx.r()]
    t_mod_positive = rt_mx.t().mod_positive()
    idx = tr_vecs[t_mod_positive]
    t_diff = rt_mx.t().minus(group[idx].t())
    if not full_code and t_diff.is_zero():
      return "%i" %(idx+1)
    klm = tuple([int(i) + 5 for i in t_diff.as_double()])
    return "%i%s" %(idx+1, sep) + "%i%i%i" %(klm)

def reference_space_group_infos():
  for number in range(1,230+1):
    yield space_group_info(number=number)

@bp.inject_into(tr_vec)
class _():

  def as_rational(self):
    return matrix.col(rational.vector(self.num(), self.den()))

class le_page_1982_delta_details:

  def __init__(self, reduced_cell, rot_mx, deg=False):
    orth = matrix.sqr(reduced_cell.orthogonalization_matrix())
    frac = matrix.sqr(reduced_cell.fractionalization_matrix())
    r_info = rot_mx.info()
    self.type = r_info.type()
    self.u = rot_mx.info().ev()
    self.h = rot_mx.transpose().info().ev()
    self.t = orth * matrix.col(self.u)
    self.tau = matrix.row(self.h) * frac
    if (abs(self.type) == 1):
      self.delta = 0.0
    else:
      self.delta = self.t.accute_angle(self.tau, deg=deg)

@bp.inject_into(rot_mx)
class _():

  def as_rational(self):
    return matrix.sqr(rational.vector(self.num(), self.den()))

  def le_page_1982_delta_details(self, reduced_cell, deg=False):
    return le_page_1982_delta_details(
      reduced_cell=reduced_cell, rot_mx=self, deg=deg)

  def le_page_1982_delta(self, reduced_cell, deg=False):
    return self.le_page_1982_delta_details(
      reduced_cell=reduced_cell, deg=deg).delta

  def lebedev_2005_perturbation(self, reduced_cell):
    s = matrix.sym(sym_mat3=reduced_cell.metrical_matrix())
    m = self.as_rational().as_float()
    r = m.transpose() * s * m
    sirms = s.inverse() * (r-s)
    return ((sirms * sirms).trace() / 12)**0.5


@bp.inject_into(rot_mx_info)
class _():

  def basis_of_invariant(self):
    from cctbx.math_module import basis_of_mirror_plane_with_normal
    if not hasattr(self, '_basis_of_invariant'):
      if self.type() == 1:
        basis = ((1,0,0), (0,1,0), (0,0,1))
      elif self.type() == -2:
        basis = basis_of_mirror_plane_with_normal(self.ev())
      elif self.type() < 0:
        basis = ()
      else:
        basis = (self.ev(), )
      self._basis_of_invariant = basis
    return self._basis_of_invariant

  def __str__(self):
    result = "% i" % self.type()
    if self.sense() == -1: result += "^%i" % self.sense()
    result += " |(%i, %i, %i)" % self.ev()
    return result

@bp.inject_into(translation_part_info)
class _():

  def __str__(self):
    result = "+(%s) @(%s) t_l=(%s)" % (self.intrinsic_part().mod_positive(),
                                       self.origin_shift().mod_positive(),
                                       self.location_part().mod_positive())
    return result


@bp.inject_into(ext.rt_mx)
class _():

  def __getinitargs__(self):
    return (flex.int(self.as_int_array() + (self.r().den(), self.t().den())),)

  def as_rational(self):
    return matrix.rt((self.r().as_rational(), self.t().as_rational()))

  def as_4x4_rational(self):
    r = self.r().as_rational().elems
    t = self.t().as_rational().elems
    zero = rational.int(0)
    one = rational.int(1)
    return matrix.rec((
      r[0], r[1], r[2], t[0],
      r[3], r[4], r[5], t[1],
      r[6], r[7], r[8], t[2],
      zero, zero, zero,  one), (4, 4))

  def show_geometrical_elements(self, out=None):
    if out is None: out = sys.stdout
    r_info = self.r().info()
    t_info = translation_part_info(self)
    print("%s %s" % (r_info, t_info), file=out)

@bp.inject_into(ext.search_symmetry_flags)
class _():

  def show_summary(self, f=None):
    if (f is None): f = sys.stdout
    print("use_space_group_symmetry:", self.use_space_group_symmetry(), file=f)
    print("use_space_group_ltr:", self.use_space_group_ltr(), file=f)
    print("use_normalizer_k2l:", self.use_normalizer_k2l(), file=f)
    print("use_normalizer_l2n:", self.use_normalizer_l2n(), file=f)
    print("use_seminvariants:", self.use_seminvariants(), file=f)

class special_op_simplified_term(libtbx.slots_getstate_setstate):

  __slots__ = ["i_vars", "multipliers", "constant"]

  def __init__(O, i_vars, multipliers, constant):
    assert len(i_vars) == len(multipliers)
    assert multipliers.count(0) == 0
    O.i_vars = i_vars
    O.multipliers = multipliers
    O.constant = constant

  def is_identity(O):
    if (len(O.multipliers) != 1): return False
    if (O.multipliers[0] != 1): return False
    if (O.constant != 0): return False
    return True

  def __str__(O):
    s = ""
    for i,m in zip(O.i_vars, O.multipliers):
      if (m < 0):
        s += "-"
        m = -m
      elif (len(s) != 0):
        s += "+"
      if (m != 1):
        s += str(m) + "*"
      s += "xyz"[i]
    c = O.constant
    if (c != 0 or len(s) == 0):
      if (c < 0):
        s += "-"
        c = -c
      elif (len(s) != 0):
        s += "+"
      s += str(c)
    return s

class special_op_simplified(libtbx.slots_getstate_setstate):

  __slots__ = ["terms"]

  def __init__(O, terms):
    O.terms = terms

  def __str__(O):
    return ",".join([str(term) for term in O.terms])

  def shelx_fvar_encoding(self, fvars, site, p_tolerance=1e-5):
    from iotbx.shelx import fvar_encoding
    return fvar_encoding.site_constraints_special_op_simplified(
      O=self, fvars=fvars, site=site, p_tolerance=p_tolerance)

def special_op_simplifier(special_op):
  rt = special_op.as_rational()
  r = rt.r
  t = rt.t
  rows = [r[:3], r[3:6], r[6:]]
  terms = [None, None, None]
  r0 = rational.int(0)
  r1 = rational.int(1)
  n_done = 0
  for i_row,row in enumerate(rows):
    if (row == (0,0,0)):
      terms[i_row] = special_op_simplified_term([], [], t[i_row])
      n_done += 1
  if (n_done == 3):
    return special_op_simplified(terms=terms)
  if (n_done == 0):
    m, v = [], []
    for i in range(3):
      m.append([r[i+0], r[i+3]])
      v.append(r[i+6])
    from scitbx.matrix import row_echelon
    free_vars = row_echelon.form_rational(m, v)
    if (len(free_vars) == 0):
      sol = row_echelon.back_substitution_rational(m, v, free_vars, [None]*2)
      if (sol is not None and sol.count(0) == 0):
        for i_row in [0,1]:
          terms[i_row] = special_op_simplified_term([i_row], [r1], r0)
        terms[2] = special_op_simplified_term(
          [0,1], sol, t[2] - sol[0]*t[0] - sol[1]*t[1])
        return special_op_simplified(terms=terms)
  for i_row in range(3):
    if (terms[i_row] is not None): continue
    terms[i_row] = special_op_simplified_term([i_row], [r1], r0)
    for j_row in range(i_row+1,3):
      if (terms[j_row] is not None): continue
      m = matrix.linearly_dependent_pair_scaling_factor(
        vector_1=rows[i_row], vector_2=rows[j_row])
      if (m is None): continue
      assert m != 0
      terms[j_row] = special_op_simplified_term(
        [i_row], [m], t[j_row] - m*t[i_row])
  return special_op_simplified(terms=terms)

@bp.inject_into(ext.site_symmetry_ops)
class _():

  def __getinitargs__(self):
    return (self.multiplicity(), self.special_op(), self.matrices())

  def special_op_simplified(self):
    return special_op_simplifier(special_op=self.special_op())

  def shelx_fvar_encoding(self, fvars, site, p_tolerance=1e-5):
    from iotbx.shelx import fvar_encoding
    return fvar_encoding.site_constraints_site_symmetry_ops(
      O=self, fvars=fvars, site=site, p_tolerance=p_tolerance)

@bp.inject_into(ext.site_symmetry_table)
class _():

  def __getinitargs__(self):
    return (self.indices(), self.table(), self.special_position_indices())

  def apply_symmetry_sites(self, unit_cell, sites_cart):
    sites_frac = unit_cell.fractionalize(sites_cart=sites_cart)
    for i_seq in self.special_position_indices():
      sites_frac[i_seq] = self.get(i_seq=i_seq).special_op() \
                        * sites_frac[i_seq]
    return unit_cell.orthogonalize(sites_frac=sites_frac)

  def show_special_position_shifts(self,
        special_position_settings,
        site_labels,
        sites_frac_original=None,
        sites_cart_original=None,
        sites_frac_exact=None,
        sites_cart_exact=None,
        out=None,
        prefix=""):
    assert [sites_frac_original, sites_cart_original].count(None) == 1
    assert [sites_frac_exact, sites_cart_exact].count(None) == 1
    if (out is None): out = sys.stdout
    print(prefix + "Number of sites at special positions:", \
      self.special_position_indices().size(), file=out)
    if (self.special_position_indices().size() > 0):
      label_len = 5
      for i_seq in self.special_position_indices():
        label_len = max(label_len, len(site_labels[i_seq]))
      label_fmt = "%%-%ds"%label_len
      print(prefix \
        + "  Minimum distance between symmetrically equivalent sites: %.4g" % (
        special_position_settings.min_distance_sym_equiv()), file=out)
      print(prefix + "  " + label_fmt%"Label" \
        + "   Mult   Shift    Fractional coordinates", file=out)
      uc = special_position_settings.unit_cell()
      if (sites_frac_original is None):
        sites_frac_original = uc.fractionalize(sites_cart=sites_cart_original)
      if (sites_frac_exact is None):
        sites_frac_exact = uc.fractionalize(sites_cart=sites_cart_exact)
      for i_seq in self.special_position_indices():
        so = sites_frac_original[i_seq]
        se = sites_frac_exact[i_seq]
        special_ops = self.get(i_seq=i_seq)
        print(prefix + "  " + label_fmt%site_labels[i_seq] \
          + "  %4d  %7.3f (%8.4f %8.4f %8.4f) original" % (
          (special_ops.multiplicity(), uc.distance(so, se)) + so), file=out)
        print(prefix + label_fmt%"" \
          + "   site sym %-6s"%special_position_settings.site_symmetry(se) \
              .point_group_type() \
          + "(%8.4f %8.4f %8.4f) exact"%se, file=out)
        s = str(special_ops.special_op())
        print(prefix + label_fmt%"" + " "*(18+max(0,(26-len(s))//2)), s, file=out)

  def discard_symmetry(self):
    assert len(self.table())>0
    site_sym = self.table()[0]
    assert site_sym.is_point_group_1()
    return site_symmetry_table(
      indices=flex.size_t(self.indices().size(), 0),
      table=[site_symmetry_ops(1, site_sym.special_op(), site_sym.matrices())],
      special_position_indices=flex.size_t())

  def symmetry_equivalent_pair_interactions(self, i_seq, j_seq, rt_mx_ji):
    return symmetry_equivalent_pair_interactions(
      site_symmetry_ops_i=self.get(i_seq),
      site_symmetry_ops_j=self.get(j_seq),
      i_seq_eq_j_seq=(i_seq == j_seq),
      rt_mx_ji=rt_mx_ji)

  def pack_coordinates(self, sites_frac):
    assert sites_frac.size() == self.indices().size()
    result = flex.double()
    for i_seq,x in enumerate(sites_frac):
      if (self.is_special_position(i_seq)):
        x = self.get(i_seq).site_constraints().independent_params(x)
      for _ in x: result.append(_)
    return result

  def unpack_coordinates(self, packed_coordinates):
    result = flex.vec3_double()
    ix = 0
    jx = 0
    for i_tab in self.indices():
      if (i_tab == 0):
        jx = ix + 3
        x = list(packed_coordinates[ix:jx])
      else:
        sc = self.table()[i_tab].site_constraints()
        jx = ix + sc.n_independent_params()
        x = sc.all_params(list(packed_coordinates[ix:jx]))
      ix = jx
      result.append(x)
    assert jx == packed_coordinates.size()
    return result

  def pack_gradients(self, g_frac):
    assert g_frac.size() == self.indices().size()
    result = flex.double()
    for i_seq,g in enumerate(g_frac):
      if (self.is_special_position(i_seq)):
        g = self.get(i_seq).site_constraints().independent_gradients(g)
      for _ in g: result.append(_)
    return result

@bp.inject_into(wyckoff_position)
class _():

  def special_op_simplified(self):
    return special_op_simplifier(special_op=self.special_op())

@bp.inject_into(wyckoff_table)
class _():

  def random_site_symmetry(self,
        special_position_settings,
        i_position,
        unit_shift_range=(-5,6),
        tolerance=1.e-8):
    position = self.position(i_position)
    run_away_counter = 0
    while 1:
      run_away_counter += 1
      assert run_away_counter < 1000
      site = position.special_op() * [random.random() for i in range(3)]
      if (unit_shift_range is not None):
        site = [x + random.randrange(*unit_shift_range) for x in site]
      site_symmetry = special_position_settings.site_symmetry(site)
      if (site_symmetry.distance_moved() < tolerance):
        assert site_symmetry.multiplicity() == position.multiplicity()
        return site_symmetry

@bp.inject_into(structure_seminvariants)
class _():

  def __str__(self):
    result = []
    for vm in self.vectors_and_moduli():
      result.append((vm.m,) + vm.v)
    return '\n'.join([ "%i: (%i, %i, %i)" % item for item in result ])

  def number_of_continuous_allowed_origin_shifts(self):
    return self.select(False).size()

class symmetry_equivalent_pair_interactions(libtbx.slots_getstate_setstate):

  __slots__ = ["site_symmetry_ops_j", "registry"]

  def __init__(O,
        site_symmetry_ops_i,
        site_symmetry_ops_j,
        i_seq_eq_j_seq,
        rt_mx_ji):
    O.site_symmetry_ops_j = site_symmetry_ops_j
    O.registry = {}
    ssm_i =   site_symmetry_ops_i.matrices()
    ssm_j = O.site_symmetry_ops_j.matrices()
    if (not i_seq_eq_j_seq and len(ssm_i) == 1 and len(ssm_j) == 1):
      # just for fast handling of common case
      rt_mx_ji = rt_mx_ji.cancel()
      O.registry[rt_mx_ji] = rt_mx_ji
      return
    sso_j = O.site_symmetry_ops_j.special_op()
    def add(mi, rt_mx_ji):
      rt_mx_ji_eq = mi.multiply(rt_mx_ji)
      rs = rt_mx_ji_eq.multiply(sso_j)
      if (rs not in O.registry):
        best = rt_mx_ji_eq
        for mj in ssm_j:
          best = min(best, rt_mx_ji_eq.multiply(mj))
        O.registry[rs] = best
    for mi in ssm_i:
      add(mi, rt_mx_ji)
    if (i_seq_eq_j_seq):
      rt_mx_ji_inv = rt_mx_ji.inverse()
      for mi in ssm_i:
        add(mi, rt_mx_ji_inv)

  def get(O):
    result = list(O.registry.values())
    result.sort()
    return result

  def is_equivalent(O, rt_mx_ji):
    sso_j = O.site_symmetry_ops_j.special_op()
    rs = rt_mx_ji.multiply(sso_j)
    return rs in O.registry

def compare_cb_op_as_hkl(a, b):
  # Deprecated. Do not use.
  if (len(a) < len(b)): return -1
  if (len(a) > len(b)): return  1
  from libtbx.math_utils import cmp
  return cmp(a, b)
