#ifndef SMTBX_REFINEMENT_CONSTRAINTS_GEOMETRICAL_HYDROGENS_H
#define SMTBX_REFINEMENT_CONSTRAINTS_GEOMETRICAL_HYDROGENS_H

#include <smtbx/refinement/constraints/reparametrisation.h>
#include <scitbx/constants.h>
#include <scitbx/math/orthonormal_basis.h>
#include <cmath>


namespace smtbx { namespace refinement { namespace constraints {

namespace constants {
  using namespace scitbx::constants;
  static double const cos_tetrahedral_angle = -1./3.;
  static double const tetrahedral_angle = std::acos(cos_tetrahedral_angle);
  static double const sin_tetrahedral_angle
    = std::sqrt(1. - cos_tetrahedral_angle*cos_tetrahedral_angle);
  static double const half_sqrt_3 = std::sqrt(3.)/2;
}


/// Base class for geometrical hydrogen
template <int n_hydrogens>
class geometrical_hydrogen_sites : public asu_parameter
{
public:
  geometrical_hydrogen_sites(scatterer_type *h)
  : hydrogen(h)
  {}

  geometrical_hydrogen_sites(scatterer_type *h0, scatterer_type *h1)
  : hydrogen(h0, h1)
  {}

  geometrical_hydrogen_sites(af::tiny<scatterer_type *, n_hydrogens> h)
  : hydrogen(h)
  {}

  virtual af::ref<double> components() {
    return af::ref<double>(x_h[0].begin(), 3*x_h.size());
  }

  virtual scatterer_sequence_type scatterers() const {
    return hydrogen.const_ref();
  }

  virtual index_range
  component_indices_for(scatterer_type const *scatterer) const;

  virtual void
  write_component_annotations_for(scatterer_type const *scatterer,
                                  std::ostream &output) const;

  virtual void store(uctbx::unit_cell const &unit_cell) const {
    for (int i=0; i<hydrogen.size(); ++i) {
      hydrogen[i]->site = unit_cell.fractionalize(x_h[i]);
    }
  }

protected:
  af::tiny<scatterer_type *, n_hydrogens> hydrogen;
  af::tiny<cart_t, n_hydrogens> x_h;
};


/// Model of Y-XHn with tetrahedral angles
/**
  X is referred to as the "pivot" and Y as the "pivot neighbour".

  All angles Hi-X-Hj and Hi-X-Y are tetrahedral.
  All distances X-Hi are equal. That unique distance may be a variable
  parameter if stretching is allowed.
  The Hydrogen sites ride on the pivot site.
*/
template <int n_hydrogens, bool staggered>
class terminal_tetrahedral_xhn_sites
  : public geometrical_hydrogen_sites<n_hydrogens>
{
public:
  /// Construct Hydrogens freely rotating about the bond X-Y
  /** e_zero_azimuth is the vector such that the plane (e_zero_azimuth, XY)
      defines azimuth = 0. Thus it shall be such that it can never become nearly
      colinear to the bond between the pivot and its neighbour.
   */
  terminal_tetrahedral_xhn_sites(site_parameter *pivot,
                                 site_parameter *pivot_neighbour,
                                 independent_scalar_parameter *azimuth,
                                 independent_scalar_parameter *length,
                                 cart_t const &e_zero_azimuth,
                                 af::tiny<asu_parameter::scatterer_type *,
                                          n_hydrogens> const &hydrogen)
    : parameter(4),
      geometrical_hydrogen_sites<n_hydrogens>(hydrogen),
      e_zero_azimuth(e_zero_azimuth)
  {
    SMTBX_ASSERT(!staggered);
    this->set_arguments(pivot, pivot_neighbour, azimuth, length);
  }

  /// Construct Hydrogens staggered on the specified site
  /** stagger shall be a neighbour of the pivot neighbour onto which to
      stagger the Hydrogen's.
   */
  terminal_tetrahedral_xhn_sites(site_parameter *pivot,
                                 site_parameter *pivot_neighbour,
                                 site_parameter *stagger,
                                 independent_scalar_parameter *length,
                                 af::tiny<asu_parameter::scatterer_type *,
                                          n_hydrogens> const &hydrogen)
  : parameter(4),
    geometrical_hydrogen_sites<n_hydrogens>(hydrogen)
  {
    SMTBX_ASSERT(staggered);
    this->set_arguments(pivot, pivot_neighbour, stagger, length);
  }

  virtual void linearise(uctbx::unit_cell const &unit_cell,
                         sparse_matrix_type *jacobian_transpose);

private:
  cart_t e_zero_azimuth;
};

/* Angle helper object */
class angle_parameter : public scalar_parameter {
public:
  angle_parameter(
    site_parameter *left,
    site_parameter *center,
    site_parameter *right,
    double value_)
  : parameter(3)
  {
    set_arguments(left, center, right);
    value = value_;
  }

  virtual void linearise(uctbx::unit_cell const &unit_cell,
                         sparse_matrix_type *jacobian_transpose);
};

/// Model of X-CH2-Y
/**
  C is referred to as the "pivot" and X and Y as pivot's neighbour 1 and 2.

  All angles Hi-C-X and Hi-C-Y are equal.
  The angle H-C-H is refinable (flapping).
  if the H-C-H angle is refinable or fixed to a certain angle - an instance of
  the independent_scalar_parameter must be passed, otherwise to make the H-C-H
  angle to behave as in shelxl an instance of the angle_parameter should be
  provided.
*/
class secondary_xh2_sites
  : public geometrical_hydrogen_sites<2>
{
public:
  secondary_xh2_sites(site_parameter *pivot,
                      site_parameter *pivot_neighbour_0,
                      site_parameter *pivot_neighbour_1,
                      independent_scalar_parameter *length,
                      scalar_parameter *h_c_h,
                      scatterer_type *hydrogen_0,
                      scatterer_type *hydrogen_1)
  : parameter(5),
    geometrical_hydrogen_sites<2>(hydrogen_0, hydrogen_1)
  {
    set_arguments(pivot, pivot_neighbour_0, pivot_neighbour_1, length, h_c_h);
  }

  virtual void linearise(uctbx::unit_cell const &unit_cell,
                         sparse_matrix_type *jacobian_transpose);
};


/// Model of tertiary CH
/** All angles Hi-C-X are equal.
 */
class tertiary_xh_site
  : public geometrical_hydrogen_sites<1>
{
public:
  tertiary_xh_site(site_parameter *pivot,
                   site_parameter *pivot_neighbour_0,
                   site_parameter *pivot_neighbour_1,
                   site_parameter *pivot_neighbour_2,
                   independent_scalar_parameter *length,
                   scatterer_type *hydrogen)
  : parameter(5),
    geometrical_hydrogen_sites<1>(hydrogen)
  {
    set_arguments(pivot,
                  pivot_neighbour_0, pivot_neighbour_1, pivot_neighbour_2,
                  length);
  }

  virtual void linearise(uctbx::unit_cell const &unit_cell,
                         sparse_matrix_type *jacobian_transpose);
};


/// Model of aromatic C-H or amide N-H
/** Denoting C or N as X and the two neighbours of X as Y and Z,
    Z-X-Y is bisected by X-H.
*/
class secondary_planar_xh_site:
  public geometrical_hydrogen_sites<1>
{
public:
  secondary_planar_xh_site(site_parameter *pivot,
                           site_parameter *pivot_neighbour_0,
                           site_parameter *pivot_neighbour_1,
                           independent_scalar_parameter *length,
                           scatterer_type *hydrogen)
  : parameter(4),
    geometrical_hydrogen_sites<1>(hydrogen)
  {
    set_arguments(pivot, pivot_neighbour_0, pivot_neighbour_1, length);
  }

  virtual void linearise(uctbx::unit_cell const &unit_cell,
                         sparse_matrix_type *jacobian_transpose);
};


/// Model of terminal Z-Y=XH2 (ethylenic CH2 or amide NH2)
/**
    X is referred to as the "pivot" whereas Y is the pivot's neighbour
    and Z is the pivot's neighbour's substituent.

    The two hydrogen atoms are in the plane ZYX,
    and XY bissects the 120-degree angle H1-X-H2.
*/
class terminal_planar_xh2_sites
  : public geometrical_hydrogen_sites<2>
{
public:
  terminal_planar_xh2_sites(site_parameter *pivot,
                            site_parameter *pivot_neighbour,
                            site_parameter *pivot_neighbour_substituent,
                            independent_scalar_parameter *length,
                            scatterer_type *hydrogen_0,
                            scatterer_type *hydrogen_1)
  : parameter(4),
    geometrical_hydrogen_sites<2>(hydrogen_0, hydrogen_1)
  {
    set_arguments(pivot, pivot_neighbour, pivot_neighbour_substituent, length);
  }

  virtual void linearise(uctbx::unit_cell const &unit_cell,
                         sparse_matrix_type *jacobian_transpose);
};


/// Model of acetylenic X-CH
/**
    X-C-H is linear
*/
class terminal_linear_ch_site
  : public geometrical_hydrogen_sites<1>
{
public:
  terminal_linear_ch_site(site_parameter *pivot,
                          site_parameter *pivot_neighbour,
                          independent_scalar_parameter *length,
                          scatterer_type *hydrogen)
  : parameter(3),
    geometrical_hydrogen_sites<1>(hydrogen)
  {
    set_arguments(pivot, pivot_neighbour, length);
  }

  virtual void linearise(uctbx::unit_cell const &unit_cell,
                         sparse_matrix_type *jacobian_transpose);
};

/// Model of polyhedral B/C(4,5)-H
/**
    ()-H is a negative sum of unit vectors from the pivot to the neighbours,
    normalised to the given/refined length
*/
class polyhedral_bh_site
  : public geometrical_hydrogen_sites<1>
{
public:
  polyhedral_bh_site(site_parameter *pivot,
                     af::shared<site_parameter *> const& neighbours,
                     independent_scalar_parameter *length,
                     scatterer_type *hydrogen)
  : parameter(neighbours.size()+2),
    geometrical_hydrogen_sites<1>(hydrogen)
  {
    set_argument(0, pivot);
    set_argument(1, length);
    for (size_t i=0; i<neighbours.size(); i++)
      set_argument(i+2, neighbours[i]);
  }

  virtual void linearise(uctbx::unit_cell const &unit_cell,
                         sparse_matrix_type *jacobian_transpose);
};

}}}

#endif // GUARD
