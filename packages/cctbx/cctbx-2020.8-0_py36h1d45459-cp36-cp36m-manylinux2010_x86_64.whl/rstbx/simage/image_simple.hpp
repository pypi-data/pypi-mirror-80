#ifndef RSTBX_SIMAGE_IMAGE_SIMPLE_HPP
#define RSTBX_SIMAGE_IMAGE_SIMPLE_HPP

#include <rstbx/import_scitbx_af.hpp>
#include <cctbx/miller.h>
#include <cctbx/uctbx.h>
#include <scitbx/mat3.h>
#include <scitbx/vec2.h>
#include <scitbx/array_family/versa.h>
#include <tbxx/error_utils.hpp>

namespace rstbx { namespace simage {

  struct image_simple
  {
    bool apply_proximity_filter;
    bool apply_detector_clipping;
    bool apply_proximity_factor;
    bool store_miller_index_i_seqs;
    bool store_spots;
    bool store_signals;
    bool set_pixels;
    af::shared<std::size_t> miller_index_i_seqs;
    af::shared<scitbx::vec3<double> > spots;
    af::shared<double> signals;
    af::versa<int, af::flex_grid<> > pixels;

    image_simple(
      bool apply_proximity_filter_,
      bool apply_detector_clipping_,
      bool apply_proximity_factor_,
      bool store_miller_index_i_seqs_,
      bool store_spots_,
      bool store_signals_,
      bool set_pixels_)
    :
      apply_proximity_filter(apply_proximity_filter_),
      apply_detector_clipping(apply_detector_clipping_),
      apply_proximity_factor(apply_proximity_factor_),
      store_miller_index_i_seqs(store_miller_index_i_seqs_),
      store_spots(store_spots_),
      store_signals(store_signals_),
      set_pixels(set_pixels_)
    {}

    image_simple&
    compute(
      cctbx::uctbx::unit_cell const& unit_cell,
      af::const_ref<cctbx::miller::index<> > const& miller_indices,
      af::const_ref<double> const& spot_intensity_factors,
      scitbx::mat3<double> const& crystal_rotation_matrix,
      double ewald_radius,
      double ewald_proximity,
      int signal_max,
      double detector_distance,
      scitbx::vec2<double> detector_size,
      scitbx::vec2<int> detector_pixels,
      unsigned point_spread,
      double gaussian_falloff_scale)
    {
      if (spot_intensity_factors.size() != 0) {
        TBXX_ASSERT(spot_intensity_factors.size() == miller_indices.size());
        TBXX_ASSERT(spot_intensity_factors.all_ge(0));
        TBXX_ASSERT(spot_intensity_factors.all_le(1));
      }
      TBXX_ASSERT(ewald_proximity > 0);
      TBXX_ASSERT(ewald_radius > 0);
      TBXX_ASSERT(detector_size.const_ref().all_gt(0));
      TBXX_ASSERT(detector_pixels.const_ref().all_gt(0));
      TBXX_ASSERT(point_spread > 0);
      TBXX_ASSERT(gaussian_falloff_scale >= 0);
      int dpx = detector_pixels[0];
      int dpy = detector_pixels[1];
      if (set_pixels) {
        pixels.resize(af::flex_grid<>(dpx, dpy), 0);
      }
      int* pixels_beg = pixels.begin();
      double dsx = detector_size[0];
      double dsy = detector_size[1];
      unsigned point_spread_half = point_spread / 2;
      bool point_spread_is_even_value = (point_spread % 2 == 0);
      double circle_radius_sq = point_spread * std::max(dsx/dpx, dsy/dpy) / 2;
      circle_radius_sq *= circle_radius_sq;
      TBXX_ASSERT(circle_radius_sq != 0);
      typedef scitbx::vec3<double> v3d;
      for(std::size_t ih=0;ih<miller_indices.size();ih++) {
        // compare with ewald_proximity() code in explore_completeness.py
        v3d rv = unit_cell.reciprocal_space_vector(miller_indices[ih]);
        v3d rvre = crystal_rotation_matrix * rv;
        rvre[2] += ewald_radius; // direct beam anti-parallel (0,0,1)
        double rvre_len = rvre.length();
        double rvre_proximity = std::abs(1 - rvre_len / ewald_radius);
        if (!apply_proximity_filter || rvre_proximity < ewald_proximity) {
          if (rvre[2] <= 0) {
            TBXX_ASSERT(apply_proximity_filter);
          }
          else {
            // http://en.wikipedia.org/wiki/Line-plane_intersection
            double d = -detector_distance / rvre[2];
            double dx = rvre[0] * d;
            double dy = rvre[1] * d;
            bool off_detector = (
                 std::abs(dx) > dsx/2
              || std::abs(dy) > dsy/2);
            if (off_detector && apply_detector_clipping) {
              continue;
            }
            double pxf = (dx/dsx + 0.5) * dpx;
            double pyf = (dy/dsy + 0.5) * dpy;
            if (store_miller_index_i_seqs) {
              miller_index_i_seqs.push_back(ih);
            }
            if (store_spots) {
              spots.push_back(scitbx::vec3<double>(pxf, pyf, 0));
              if (!store_signals && !set_pixels) continue;
            }
            double proximity_factor = 1;
            if (apply_proximity_factor) {
              proximity_factor -= scitbx::fn::pow2(
                rvre_proximity / ewald_proximity);
              if (proximity_factor < 0) proximity_factor = 0;
            }
            double signal_at_center =
                signal_max
              * (spot_intensity_factors.size() == 0 ? 1 :
                 spot_intensity_factors[ih])
              * proximity_factor;
            if (store_signals) {
              signals.push_back(signal_at_center);
            }
            if (off_detector || !set_pixels || proximity_factor == 0) continue;
            int signal = static_cast<int>(signal_at_center + 0.5);
            double gauss_arg_term = -gaussian_falloff_scale
                                  / circle_radius_sq;
            using scitbx::math::ifloor;
            int pxi = ifloor(pxf);
            int pyi = ifloor(pyf);
            int pxb = pxi - point_spread_half;
            int pyb = pyi - point_spread_half;
            if (point_spread_is_even_value) {
              if (pxf - pxi > 0.5) pxb++;
              if (pyf - pyi > 0.5) pyb++;
            }
            for(int i=0;i<=point_spread;i++) {
              int pi = pxb + i;
              if (pi < 0 || pi >= dpx) continue;
              int pi0 = pi * dpy;
              for(int j=0;j<=point_spread;j++) {
                int pj = pyb + j;
                if (pj < 0 || pj >= dpy) continue;
                if (point_spread > 2) {
                  double pcx = ((pi + 0.5) / dpx - 0.5) * dsx - dx;
                  double pcy = ((pj + 0.5) / dpy - 0.5) * dsy - dy;
                  double pc_sq = pcx*pcx + pcy*pcy;
                  if (pc_sq > circle_radius_sq) continue;
                  if (gaussian_falloff_scale != 0) {
                    double falloff_factor = std::exp(pc_sq * gauss_arg_term);
                    signal = static_cast<int>(
                      signal_at_center * falloff_factor + 0.5);
                  }
                }
                pixels_beg[pi0+pj] = signal;
              }
            }
          }
        }
      }
      return *this;
    }
  };

}} // namespace rstbx::simage

#endif // GUARD
