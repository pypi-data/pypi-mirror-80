#ifndef SMTBX_REFINEMENT_CONSTRAINTS_U_EQ_DEPENDENT_U_ISO_H
#define SMTBX_REFINEMENT_CONSTRAINTS_U_EQ_DEPENDENT_U_ISO_H

#include <smtbx/refinement/constraints/reparametrisation.h>

namespace smtbx { namespace refinement { namespace constraints {

/** u_iso parameter that is proportional to the equivalent u_iso
    of some u_star parameter.

    The latter is the average of the diagonal elements of the associated u_cart.
    C.f. adptbx::u_star_as_u_iso
 */
class u_iso_proportional_to_pivot_u_eq : public asu_u_iso_parameter
{
public:
  u_iso_proportional_to_pivot_u_eq(u_star_parameter *pivot_u,
                                   double multiplier,
                                   scatterer_type *scatterer)
  : parameter(1),
    single_asu_scatterer_parameter(scatterer),
    multiplier(multiplier)
  {
    this->set_arguments(pivot_u);
  }

  u_star_parameter *pivot_u() const {
    return dynamic_cast<u_star_parameter *>(this->argument(0));
  }

  virtual void linearise(uctbx::unit_cell const &unit_cell,
                         sparse_matrix_type *jacobian_transpose);

  double multiplier;
};


}}}

#endif // GUARD
