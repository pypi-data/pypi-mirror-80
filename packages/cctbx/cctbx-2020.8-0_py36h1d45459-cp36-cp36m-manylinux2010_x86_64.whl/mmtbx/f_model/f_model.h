#ifndef MMTBX_F_MODEL_H
#define MMTBX_F_MODEL_H

#include <mmtbx/error.h>
#include <cctbx/adptbx.h>
#include <cctbx/xray/targets.h>

namespace mmtbx { namespace f_model {
using namespace std;
namespace af=scitbx::af;
using scitbx::mat3;
using scitbx::sym_mat3;

const int max_n_shells = 10;

template <typename FloatType>
FloatType k_anisotropic_one_h(cctbx::miller::index<> const& h,
                        scitbx::sym_mat3<FloatType> u_star)
{
  return cctbx::adptbx::debye_waller_factor_u_star(
    h, u_star,
    /*exp_arg_limit*/ 40., /*truncate_exp_arg*/ true);
}

template <typename FloatType>
FloatType f_b_exp_one_h(FloatType const& ss, FloatType const& b)
{
  return cctbx::adptbx::debye_waller_factor_b_iso(
    /*stol_sq*/ ss, /*b_iso*/ b,
    /*exp_arg_limit*/ 40., /*truncate_exp_arg*/ true);
}

template <typename FloatType>
af::shared<FloatType> k_mask(
  af::const_ref<FloatType> const& ss,
  FloatType const& k_sol,
  FloatType const& b_sol)
{
  af::shared<FloatType> result(ss.size(), 0);
  for(std::size_t i=0; i < ss.size(); i++) {
    result[i] = k_sol * std::exp(-1.*b_sol*ss[i]);
  }
  return result;
}

template <typename FloatType>
af::shared<FloatType> k_anisotropic(
  af::const_ref<cctbx::miller::index<> > const& miller_indices,
  scitbx::sym_mat3<FloatType> const& u_star)
{
  af::shared<FloatType> result(miller_indices.size(), 1);
  for(std::size_t i=0; i < miller_indices.size(); i++) {
    result[i] = cctbx::adptbx::debye_waller_factor_u_star(
      miller_indices[i], u_star, /*exp_arg_limit*/ 40.,
      /*truncate_exp_arg*/ true);
  }
  return result;
}

template <typename FloatType>
af::shared<FloatType> k_anisotropic(
  af::const_ref<cctbx::miller::index<> > const& miller_indices,
  af::shared<FloatType> const& a,
  cctbx::uctbx::unit_cell const& unit_cell)
{
  af::shared<FloatType> result(miller_indices.size(), 1);
  af::double6 p = unit_cell.reciprocal_parameters();
  FloatType as=p[0], bs=p[1], cs=p[2];
  for(std::size_t i=0; i < miller_indices.size(); i++) {
    cctbx::miller::index<> const& miller_index = miller_indices[i];
    int h=miller_index[0], k=miller_index[1], l=miller_index[2];
    FloatType stol = unit_cell.stol_sq(miller_index);
    FloatType s = 0;
    if(stol != 0) s = 1./stol;
    result[i]=
      1 +
      h*h*as*as*s   * a[0]+
      h*h*as*as     * a[1]+
      k*k*bs*bs*s   * a[2]+
      k*k*bs*bs     * a[3]+
      l*l*cs*cs*s   * a[4]+
      l*l*cs*cs     * a[5]+
      2*k*l*bs*cs*s * a[6]+
      2*k*l*bs*cs   * a[7]+
      2*h*l*as*cs*s * a[8]+
      2*h*l*as*cs   * a[9]+
      2*h*k*as*bs*s * a[10]+
      2*h*k*as*bs   * a[11];
  }
  return result;
}

template <typename FloatType=double,
          typename ComplexType=std::complex<double> >
class core
{
  public:
    af::shared<ComplexType>                f_calc;
    af::shared<ComplexType>                f_part1;
    af::shared<ComplexType>                f_part2;
    scitbx::sym_mat3<FloatType>            u_star;
    af::shared<cctbx::miller::index<> >    hkl;
    cctbx::uctbx::unit_cell                uc;
    af::shared<FloatType>                  ss;
    af::shared<ComplexType>                f_model, f_bulk, f_mask_one;
    mat3<FloatType>                        a;
    af::shared<FloatType>                  k_isotropic;
    af::shared<FloatType>                  k_anisotropic;
    af::shared<FloatType>                  k_mask;
    af::shared<ComplexType>                f_model_no_aniso_scale;

    int n_shells() const
    {
      MMTBX_ASSERT(k_sols_.size()==shell_f_masks_.size());
      return k_sols_.size();
    }

    FloatType k_sol(unsigned short i) const
    {
      return k_sols_[i];
    }

    FloatType b_sol(unsigned short i) const
    {
      return b_sols_[i];
    }

    af::shared<FloatType> k_sols() const
    {
      return k_sols_;
    }

    af::shared<FloatType> b_sols() const
    {
      return b_sols_;
    }

    af::shared<FloatType> k_mask_one() const
    {
      return k_mask;
    }

    af::shared<ComplexType> f_mask() const
    {
      MMTBX_ASSERT(shell_f_masks_.size()==1U);
      return shell_f_masks_[0];
    }

    af::shared<ComplexType>  shell_f_mask(unsigned short i) const
    {
      return shell_f_masks_[i];
    }

    af::shared<af::shared<ComplexType> > shell_f_masks() const
    {
      return shell_f_masks_;
    }

    core() {}

    core(af::shared<ComplexType>                const& f_calc_,
         af::shared< af::shared<ComplexType> >  const& f_masks,
         af::shared<FloatType>                  const& k_sols,
         af::shared<FloatType>                  const& b_sols,
         af::shared<ComplexType>                const& f_part1_,
         af::shared<ComplexType>                const& f_part2_,
         scitbx::sym_mat3<FloatType>            const& u_star_,
         af::shared<cctbx::miller::index<> >    const& hkl_,
         af::shared<FloatType>                  const& ss_
         )
    :
      f_calc(f_calc_),
      u_star(u_star_), hkl(hkl_), ss(ss_),
      k_anisotropic(hkl_.size(), af::init_functor_null<FloatType>()),
      f_bulk(hkl_.size(), af::init_functor_null<ComplexType>()),
      f_model(hkl_.size(), af::init_functor_null<ComplexType>()),
      f_part1(f_part1_), f_part2(f_part2_),
      f_model_no_aniso_scale(f_calc_.size(),af::init_functor_null<ComplexType>())
    {
      MMTBX_ASSERT(f_calc.size() == hkl.size());
      for(short j=0; j<f_masks.size(); ++j)
        MMTBX_ASSERT(f_calc.size() == f_masks[j].size());
      MMTBX_ASSERT(f_calc.size() == f_part1_.size());
      MMTBX_ASSERT(f_calc.size() == f_part2_.size());
      MMTBX_ASSERT(k_sols.size() == f_masks.size());
      MMTBX_ASSERT(k_sols.size() == b_sols.size());
      k_sols_ = k_sols;
      b_sols_ = b_sols;
      shell_f_masks_ = f_masks;
      MMTBX_ASSERT( this->n_shells() >= 1U );
      for(short j=0; j<shell_f_masks_.size(); ++j)
        MMTBX_ASSERT(f_calc.size() == this->shell_f_masks_[j].size());
      FloatType*   k_anisotropic_  = k_anisotropic.begin();
      FloatType*   ss__      = ss.begin();
      ComplexType* f_bulk_   = f_bulk.begin();
      ComplexType* f_model_  = f_model.begin();
      ComplexType* f_calc__  = f_calc.begin();
      ComplexType* f_part1__ = f_part1.begin();
      ComplexType* f_part2__ = f_part2.begin();
      ComplexType* f_model_no_aniso_scale_ = f_model_no_aniso_scale.begin();
      scitbx::af::shared<ComplexType*> f_masks__;
      for(short j=0; j<shell_f_masks_.size(); ++j)
        f_masks__.push_back(shell_f_masks_[j].begin());
      for(std::size_t i=0; i < hkl.size(); i++) {
        k_anisotropic_[i] = k_anisotropic_one_h(hkl[i], u_star);
        // TODO: optimize
        FloatType fbs = f_b_exp_one_h(ss__[i], b_sols_[0]);
        f_bulk_[i] = f_k_bexp_f_one_h(f_masks__[0][i], fbs, k_sols_[0]);
        for(short j=1; j<k_sols_.size(); ++j) {
          FloatType fbs = f_b_exp_one_h(ss__[i], b_sols_[j]);
          f_bulk_[i] +=f_k_bexp_f_one_h(f_masks__[j][i],fbs,k_sols_[j]);
        }
        ComplexType tmp = f_model_one_h(
          f_calc__[i], f_bulk_[i], f_part1_[i], f_part2__[i], 1.0);
        f_model_[i] = tmp*k_anisotropic_[i];
        f_model_no_aniso_scale_[i] = tmp;
      }
    }

    core(af::shared<ComplexType> const& f_calc_,
         af::shared<ComplexType> const& f_mask_one_,
         af::shared<FloatType>   const& k_isotropic_,
         af::shared<FloatType>   const& k_anisotropic_,
         af::shared<FloatType>   const& k_mask_,
         af::shared<ComplexType> const& f_part1_,
         af::shared<ComplexType> const& f_part2_)
    :
      f_calc(f_calc_),
      f_mask_one(f_mask_one_),
      k_mask(k_mask_),
      k_isotropic(k_isotropic_),
      f_part1(f_part1_),
      f_part2(f_part2_),
      k_anisotropic(k_anisotropic_),
      f_model(f_calc_.size(), af::init_functor_null<ComplexType>()),
      f_model_no_aniso_scale(f_calc_.size(),af::init_functor_null<ComplexType>())
    {
      MMTBX_ASSERT(f_calc.size() == f_mask_one.size());
      MMTBX_ASSERT(f_calc.size() == k_mask.size());
      MMTBX_ASSERT(f_calc.size() == k_isotropic.size());
      MMTBX_ASSERT(f_calc.size() == k_anisotropic.size());
      ComplexType* f_model_  = f_model.begin();
      ComplexType* f_calc__  = f_calc.begin();
      ComplexType* f_mask_one__  = f_mask_one.begin();
      FloatType* k_isotropic__ = k_isotropic.begin();
      FloatType* k_anisotropic__ = k_anisotropic.begin();
      FloatType* k_mask__ = k_mask.begin();
      ComplexType* f_part1__ = f_part1.begin();
      ComplexType* f_part2__ = f_part2.begin();
      ComplexType* f_model_no_aniso_scale_ = f_model_no_aniso_scale.begin();
      for(std::size_t i=0; i < f_calc.size(); i++) {
        ComplexType fmnas = k_isotropic__[i]*(
          f_calc__[i] + k_mask__[i]*f_mask_one__[i]+f_part1_[i]+f_part2__[i]);
        f_model_no_aniso_scale_[i] = fmnas;
        f_model_[i] = k_anisotropic[i]*fmnas;
      }
    };

    protected:
       ComplexType f_k_bexp_f_one_h(ComplexType const& f_h,
                                    FloatType   const& f_bexp_h,
                                    FloatType   const& k)
       {
         return k * f_bexp_h * f_h;
       }
       ComplexType f_model_one_h(ComplexType const& f_calc_h,
                                 ComplexType const& f_bulk_h,
                                 ComplexType const& f_part1_h,
                                 ComplexType const& f_part2_h,
                                 FloatType   const& k_anisotropic_h)
       {
         return k_anisotropic_h * (f_calc_h + f_bulk_h + f_part1_h + f_part2_h);
       }
       scitbx::af::shared<af::shared<ComplexType> > shell_f_masks_;
       scitbx::af::shared<FloatType> k_sols_;
       scitbx::af::shared<FloatType> b_sols_;
};

template <typename FloatType=double,
          typename ComplexType=std::complex<double> >
class data
{
  public:
    af::shared<ComplexType> f_calc;
    af::shared<ComplexType> f_bulk;
    af::shared<ComplexType> f_part1;
    af::shared<ComplexType> f_part2;
    af::shared<ComplexType> f_model;
    af::shared<FloatType>   k_isotropic_exp;
    af::shared<FloatType>   k_isotropic;
    af::shared<FloatType>   k_anisotropic;
    af::shared<ComplexType> f_model_no_aniso_scale;

    data() {}

    data(af::shared<ComplexType> const& f_calc_,
         af::shared<ComplexType> const& f_bulk_,
         af::shared<FloatType>   const& k_isotropic_exp_,
         af::shared<FloatType>   const& k_isotropic_,
         af::shared<FloatType>   const& k_anisotropic_,
         af::shared<ComplexType> const& f_part1_,
         af::shared<ComplexType> const& f_part2_)
    :
      f_calc(f_calc_),
      f_bulk(f_bulk_),
      k_isotropic_exp(k_isotropic_exp_),
      k_isotropic(k_isotropic_),
      f_part1(f_part1_),
      f_part2(f_part2_),
      k_anisotropic(k_anisotropic_),
      f_model(f_calc_.size(), af::init_functor_null<ComplexType>()),
      f_model_no_aniso_scale(f_calc_.size(),af::init_functor_null<ComplexType>())
    {
      MMTBX_ASSERT(f_calc.size() == f_bulk.size());
      MMTBX_ASSERT(f_calc.size() == k_isotropic.size());
      MMTBX_ASSERT(f_calc.size() == k_anisotropic.size());
      ComplexType* f_model_  = f_model.begin();
      ComplexType* f_calc__  = f_calc.begin();
      ComplexType* f_bulk__  = f_bulk.begin();
      FloatType* k_isotropic_exp__   = k_isotropic_exp.begin();
      FloatType* k_isotropic__   = k_isotropic.begin();
      FloatType* k_anisotropic__ = k_anisotropic.begin();
      ComplexType* f_part1__ = f_part1.begin();
      ComplexType* f_part2__ = f_part2.begin();
      ComplexType* f_model_no_aniso_scale_ = f_model_no_aniso_scale.begin();
      for(std::size_t i=0; i < f_calc.size(); i++) {
        ComplexType fmnas = k_isotropic_exp__[i] * k_isotropic__[i]*(
          f_calc__[i] + f_bulk__[i]+f_part1_[i]+f_part2__[i]);
        f_model_no_aniso_scale_[i] = fmnas;
        f_model_[i] = k_anisotropic[i]*fmnas;
      }
    };
};

}} // namespace mmtbx::f_model

#endif // MMTBX_F_MODEL_H
