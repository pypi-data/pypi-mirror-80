#ifndef RSTBX_SIMPLE_INT_HPP
#define RSTBX_SIMPLE_INT_HPP
#include <scitbx/array_family/shared.h>
#include <scitbx/vec3.h>
#include <scitbx/vec2.h>
#include <map>
#include <numeric>
#include <annlib_adaptbx/ann_adaptor.h>
#include <spotfinder/core_toolbox/distl.h>
#include <cctbx/miller.h>
#include <scitbx/array_family/flex_types.h>
#include <rstbx/backplane.h>
#include <scitbx/error.h>

#define round(x) ((x)>=0?(int)((x)+0.5):(int)((x)-0.5))

namespace rstbx { namespace integration {

  template <typename NumType=int>
  class fast_less_than
  {
    public:
      //! This fast comparison function is implemented as operator().
      bool operator()(scitbx::vec2<NumType> const& h1,
                      scitbx::vec2<NumType> const& h2) const
      {
        for(std::size_t i=0;i<2;i++) {
          if (h1[i] < h2[i]) return true;
          if (h1[i] > h2[i]) return false;
        }
        return false;
      }
  };

  template <typename ArrType>
  void
  show_array( ArrType const& A ){
    af::flex_grid<> kg = A.accessor();
    for (int ii=kg.origin()[0];ii<kg.last()[0];++ii){
      for (int jj=kg.origin()[1];jj<kg.last()[1];++jj){
        int val = A[ kg(af::adapt(af::tiny<int, 2>(ii,jj))) ]?1:7;
            std::cout<<val;
      } std::cout<<std::endl;
    }
  }

  static int MIN_BACKGROUND_SZ = 6;//Bare minimimum for OK statistics and invertible matrix

  struct patch {
    /* typedef */
    typedef std::map<scitbx::vec2<int>, bool, fast_less_than<> > mask_t;

    /* member data */
    vector<double> peak;
    vector<int> peak_used;
    vector<double> background;
    vector<int> background_used;
    scitbx::vec2<int> origin, size;

    patch() { }
    ~patch() { }

    void set_origin(scitbx::vec2<int> const & _origin) {origin = _origin;}
    void set_size(scitbx::vec2<int> const & _size) {size = _size;}

    /* actually generate the profile */

    void generate_profile(mask_t const & peak_mask,
                          scitbx::af::shared<double> const & peak_values,
                          mask_t const & background_mask,
                          scitbx::af::shared<double> const & background_values)
    {
      int imin, imax, jmin, jmax, counter;

      /* check that this peak is worth printing e.g. has > 100 counts */

      if (std::accumulate(peak_values.begin(), peak_values.end(), 0.0) < 100.0) {
        return;
      }

      /* loop over mask to determine profile limits */

      imax = - 1000000;
      imin = + 1000000;
      jmax = - 1000000;
      jmin = + 1000000;

      for(mask_t::const_iterator k = peak_mask.begin();
          k != peak_mask.end(); ++ k) {
        int i = k->first[0];
        int j = k->first[1];
        if (i < imin) imin = i;
        if (i > imax) imax = i;
        if (j < jmin) jmin = j;
        if (j > jmax) jmax = j;
      }

      for(mask_t::const_iterator k = background_mask.begin();
          k != background_mask.end(); ++ k) {
        int i = k->first[0];
        int j = k->first[1];
        if (i < imin) imin = i;
        if (i > imax) imax = i;
        if (j < jmin) jmin = j;
        if (j > jmax) jmax = j;
      }

      origin[0] = imin;
      origin[1] = jmin;
      size[0] = imax - imin + 1;
      size[1] = jmax - jmin + 1;

      peak.resize(size[0] * size[1], 0);
      peak_used.resize(size[0] * size[1], 0);
      background.resize(size[0] * size[1], 0);
      background_used.resize(size[0] * size[1], 0);

      counter = 0;
      for(mask_t::const_iterator k = peak_mask.begin();
          k != peak_mask.end(); ++ k) {
        int i = k->first[0] - imin;
        int j = k->first[1] - jmin;
        peak[i * size[1] + j] = peak_values[counter];
        peak_used[i * size[1] + j] = 1;
        counter ++;
      }

      counter = 0;
      for(mask_t::const_iterator k = background_mask.begin();
          k != background_mask.end(); ++ k) {
        int i = k->first[0] - imin;
        int j = k->first[1] - jmin;
        background[i * size[1] + j] = background_values[counter];
        background_used[i * size[1] + j] = 1;
        counter ++;
      }

      /* now print this out to see if it works */

      printf("Peak %d %d origin %d %d\n", size[0], size[1], origin[0], origin[1]);

      for (int i = 0; i < size[0]; i ++) {
        for (int j = 0; j < size[1]; j ++) {
          if (peak_used[i * size[1] + j]) {
            printf(" %5.f", peak[i * size[1] + j]);
          } else {
            printf("     .");
          }
        }
        printf("\n");
      }

      printf("Background %d %d\n", size[0], size[1]);

      for (int i = 0; i < size[0]; i ++) {
        for (int j = 0; j < size[1]; j ++) {
          if (background_used[i * size[1] + j]) {
            printf(" %5.f", background[i * size[1] + j]);
          } else {
            printf("     .");
          }
        }
        printf("\n");
      }

    }
  };

  struct simple_integration {
    /* member data */
    double pixel_size;
    scitbx::vec2<int> detector_size;
    typedef std::map<scitbx::vec2<int>, bool,fast_less_than<> > mask_t;
    typedef scitbx::af::shared<mask_t>         masks_t;
    masks_t ISmasks, BSmasks;
    scitbx::af::shared<scitbx::vec2<int> > detector_xy_draft;
    int FRAME;
    int BACKGROUND_FACTOR;
    const int MAXOVER; //number of nearest neighbors
    double nbr_cutoff_sq;
    int NEAR;
    scitbx::af::shared<scitbx::vec2<double> > corrections;
    scitbx::af::shared<double> integrated_data;
    scitbx::af::shared<double> integrated_sigma;
    scitbx::af::shared<cctbx::miller::index<> > integrated_miller;
    scitbx::af::shared<cctbx::miller::index<> > rejected_miller;
    scitbx::af::shared<std::string > rejected_reason;
    scitbx::af::shared<scitbx::vec2<double> > detector_xy;
    scitbx::af::shared<double> max_signal;
    scitbx::af::shared<bool> integrated_flag;

    simple_integration(): BACKGROUND_FACTOR(1),MAXOVER(6),NEAR(10),
      detector_saturation(std::numeric_limits<double>::max()),
      use_mask_pixel_val(false),mask_pixel_val(-2),check_tiles(false),
      guard_width_sq(11),detector_gain(0) {}

    /* accessors and mutators */
    void set_pixel_size(double const& pxsz) {pixel_size=pxsz;}

    void set_detector_size(int const& x, int const& y)
     {detector_size = scitbx::vec2<int>(x,y);}

    void set_frame(int const& f) {FRAME=f;}

    void set_background_factor(int const& f) {BACKGROUND_FACTOR=f;}

    void set_nbr_cutoff_sq(double const& b) {nbr_cutoff_sq=b;}

    void set_guard_width_sq(int const& b) {guard_width_sq=b;}

    void set_detector_gain(double const& b) {detector_gain=b;}

    double detector_saturation;
    void set_detector_saturation(double const& b) {detector_saturation = b;}

    bool use_mask_pixel_val;
    int mask_pixel_val;
    void set_mask_pixel_val(int const&val) {use_mask_pixel_val = true; mask_pixel_val = val;}

    void append_ISmask(scitbx::af::shared<int> mask){
      mask_t newmask;
      for (int i=0; i < mask.size(); i+=2){
        newmask[scitbx::vec2<int>(mask[i],mask[i+1])]=true;
      }
      ISmasks.push_back(newmask);
    }

    scitbx::af::shared<int> get_bsmask(int const& i){
      scitbx::af::shared<int> return_value;
      for (mask_t::const_iterator k=BSmasks[i].begin();
                               k != BSmasks[i].end(); ++k){
        return_value.push_back(k->first[0]);
        return_value.push_back(k->first[1]);
      }
      return return_value;
    }

    scitbx::af::shared<int>
    get_ISmask(int const& i){
      scitbx::af::shared<int> return_value;
      for (mask_t::const_iterator k=ISmasks[i].begin();
                               k != ISmasks[i].end(); ++k){
        return_value.push_back(k->first[0]);
        return_value.push_back(k->first[1]);
      }
      return return_value;
    }
    scitbx::af::shared<bool> get_integrated_flag(){return integrated_flag;}
    scitbx::af::shared<double> get_integrated_data(){return integrated_data;}
    scitbx::af::shared<double> get_integrated_sigma(){return integrated_sigma;}
    scitbx::af::shared<cctbx::miller::index<> > get_integrated_miller(){
      return integrated_miller;}
    scitbx::af::shared<cctbx::miller::index<> > get_rejected_miller(){
      return rejected_miller;}
    scitbx::af::shared<std::string > get_rejected_reason(){
      return rejected_reason;}
    scitbx::af::shared<scitbx::vec2<double> > get_detector_xy(){
      return detector_xy;}
    scitbx::af::shared<double> get_max_signal(){
      return max_signal;}

    /* algorithms */
    void
    positional_correction_mapping(
      scitbx::af::shared<scitbx::vec3<double> > predicted,
      scitbx::af::shared<scitbx::vec2<double> > correction_vectors,
      annlib_adaptbx::AnnAdaptor const& PS_adapt,
      annlib_adaptbx::AnnAdaptor const& IS_adapt,
      scitbx::af::shared<spotfinder::distltbx::w_spot> spots
      ){
      ISmasks.clear();
      corrections.clear();
      for (int i=0; i<predicted.size(); ++i){
        // calculate the positional correction for this prediction
        // ....average over the 10 nearest positional corrections
        scitbx::vec2<double>correction(0.0,0.0);
        for (int n=0; n<NEAR; ++n){ // loop over near indexed pairs
          correction += correction_vectors[PS_adapt.nn[i*NEAR+n]];
        }
        correction/=(double)NEAR;
        mask_t I_S_mask;

        scitbx::vec3<double> pred = predicted[i]/pixel_size;
        for (int n=0; n<NEAR; ++n){ // loop over near spotfinder spots
          int spot_match = IS_adapt.nn[i*NEAR+n];
          spotfinder::distltbx::w_spot spot = spots[spot_match];
          for (int p=0; p<spot.bodypixels.size(); ++p){
            double deltaX = spot.bodypixels[p].x - spot.ctr_mass_x();
            double deltaY = spot.bodypixels[p].y - spot.ctr_mass_y();
            I_S_mask[scitbx::vec2<int>(
                round(pred[0] + deltaX + correction[0]),
                round(pred[1] + deltaY + correction[1])
              )] = true;
          }
        }
        ISmasks.push_back(I_S_mask);
        corrections.push_back(correction);
      }
    }

    void
    null_correction_mapping(
      scitbx::af::shared<scitbx::vec3<double> > predicted,
      scitbx::af::shared<scitbx::vec2<double> > correction_vectors,
      annlib_adaptbx::AnnAdaptor const& IS_adapt,
      scitbx::af::shared<spotfinder::distltbx::w_spot> spots
      ){
      ISmasks.clear();
      corrections.clear();
      for (int i=0; i<predicted.size(); ++i){
        // do not make a positional correction
        scitbx::vec2<double>correction(0.0,0.0);

        mask_t I_S_mask;

        scitbx::vec3<double> pred = predicted[i]/pixel_size;
        for (int n=0; n<NEAR; ++n){ // loop over near spotfinder spots
          int spot_match = IS_adapt.nn[i*NEAR+n];
          spotfinder::distltbx::w_spot spot = spots[spot_match];
          for (int p=0; p<spot.bodypixels.size(); ++p){
            double deltaX = spot.bodypixels[p].x - spot.ctr_mass_x();
            double deltaY = spot.bodypixels[p].y - spot.ctr_mass_y();
            I_S_mask[scitbx::vec2<int>(
                round(pred[0] + deltaX + correction[0]),
                round(pred[1] + deltaY + correction[1])
              )] = true;
          }
        }
        ISmasks.push_back(I_S_mask);
        corrections.push_back(correction);
      }
    }

    scitbx::af::shared<int > tiling_boundaries_m, tile_locations_m;
    bool check_tiles;

    scitbx::af::shared<scitbx::vec2<double> >
    safe_background(scitbx::af::flex_int const& rawdata,
      scitbx::af::shared<scitbx::vec3<double> > predicted,
      annlib_adaptbx::AnnAdaptor const& OS_adapt,
      scitbx::af::shared<int > flex_sorted,
      scitbx::af::shared<int > tiling_boundaries,
      scitbx::af::shared<int > tile_locations
      ){
        tiling_boundaries_m = tiling_boundaries;
        tile_locations_m = tile_locations;
        check_tiles = true;
        return safe_background(rawdata,predicted,OS_adapt,flex_sorted);
    }

    int guard_width_sq;
    double detector_gain;
    scitbx::af::shared<scitbx::vec2<double> >
    safe_background(scitbx::af::flex_int const& rawdata,
      scitbx::af::shared<scitbx::vec3<double> > predicted,
      annlib_adaptbx::AnnAdaptor const& OS_adapt,
      scitbx::af::shared<int > flex_sorted
      ){

      /* Set up some needed data structures based on flex_sorted,
         which is a generic sorted list of points (XY) close in distance
         to a central point */
      scitbx::af::shared<scitbx::vec2<int> >increments_xy;
      scitbx::af::shared<int >increments_d_sq;
      int min_x=0, min_y=0, max_x=0, max_y=0;
      for (int isort=0; isort<flex_sorted.size(); isort+=2){
        scitbx::vec2<int> increment(flex_sorted[isort],
                                    flex_sorted[isort+1]);
        if (flex_sorted[isort]<min_x) min_x = flex_sorted[isort];
        if (flex_sorted[isort+1]<min_y) min_y = flex_sorted[isort+1];
        if (flex_sorted[isort]>max_x) max_x = flex_sorted[isort];
        if (flex_sorted[isort+1]>max_y) max_y = flex_sorted[isort+1];
        increments_xy.push_back(increment);
        increments_d_sq.push_back( increment[0]*increment[0] +
                                   increment[1]*increment[1] );
      }
      int i_guard_width_limit = 0;
      for (int isort=0; isort<increments_xy.size(); ++isort){
        if (increments_xy[isort].length_sq() >= guard_width_sq){
          i_guard_width_limit = isort;
          break;
        }
      }

      int guard_padding = 1+int(std::sqrt((double)guard_width_sq));
      //set up a mask array to show the spot along with potential neighbors
      af::flex_grid<>::index_type origin(af::adapt(af::tiny<int, 2>(min_x-guard_padding,
                                                                    min_y-guard_padding)));
      af::flex_grid<>::index_type last(af::adapt(af::tiny<int, 2>(max_x+guard_padding,
                                                                  max_y+guard_padding)));
      // add padding to avoid seg fault when doing the convolution of spot with guard
      af::flex_grid<> g(origin, last, false);
      af::flex_bool spot_grid(g); // increment - and + addresses centered at zero.

      for (int i=0; i<predicted.size(); ++i){
        scitbx::vec3<double> pred = predicted[i];
        double predX = pred[0]/pixel_size;
        double predY = pred[1]/pixel_size;
        scitbx::vec2<double>correction = corrections[i];
        mask_t const& I_S_mask = ISmasks[i];
        // now consider the background
        mask_t altB_S_mask;
        scitbx::vec2<int> spot_position(
          round(predX + correction[0]),
          round(predY + correction[1]) );
        detector_xy_draft.push_back(spot_position); // integer grid position of predicted spot, with spotfinder empirical correction

        //insert a test to make sure spot is within FRAME
        if (spot_position[0] > FRAME && spot_position[1] > FRAME &&
            spot_position[0] < detector_size[0] - FRAME &&
            spot_position[1] < detector_size[1] - FRAME){

          mask_t spot_keys = I_S_mask;
          int base_spot_size = spot_keys.size();
          base_spot_size = std::max(base_spot_size,MIN_BACKGROUND_SZ);

          //Guard against spot mask pixels off the active area
          if (check_tiles || use_mask_pixel_val){
               int itile = tile_locations_m[i];
               bool pixels_are_active = true;
               for (mask_t::const_iterator k=spot_keys.begin();
                    k != spot_keys.end(); ++k){
                 if (check_tiles &&
                     ((k->first)[0] < tiling_boundaries_m[4*itile] ||
                      (k->first)[0] >= tiling_boundaries_m[4*itile+2] ||
                      (k->first)[1] < tiling_boundaries_m[4*itile+1] ||
                      (k->first)[1] >= tiling_boundaries_m[4*itile+3])) {
                   pixels_are_active = false;
                   break;
                 }
                 if (use_mask_pixel_val) {
                   int ivalue(rawdata(k->first[0],k->first[1]));
                   if (ivalue == mask_pixel_val) {
                   pixels_are_active = false;
                   break;
                   }
                 }
               }
               if (!pixels_are_active) {BSmasks.push_back(altB_S_mask);continue;}
          }

          //Look for potential overlaps
          for (int n=0; n<MAXOVER; ++n){
            double distance = OS_adapt.distances[i*MAXOVER+n];
            if (distance < nbr_cutoff_sq){
              mask_t const& other_mask = ISmasks[ OS_adapt.nn[i*MAXOVER+n] ];
              for (mask_t::const_iterator k=other_mask.begin();
                k != other_mask.end(); ++k){
                spot_keys[k->first]=true;
              }
            }
          } //Now spot keys has addresses of both self pixels and neighboring spot pixels

          int kmin_x=0, kmin_y=0, kmax_x=0, kmax_y=0;
          //insert here to actually make the compound mask
          for (mask_t::const_iterator mt = spot_keys.begin(); mt!=spot_keys.end(); ++mt){
                  int thisx = (mt->first - spot_position)[0];
                  int thisy = (mt->first - spot_position)[1];

                  if (thisx<kmin_x) kmin_x = thisx;
                  if (thisy<kmin_y) kmin_y = thisy;
                  if (thisx>kmax_x) kmax_x = thisx;
                  if (thisy>kmax_y) kmax_y = thisy;
          }

          af::flex_grid<>::index_type korigin(
                  af::adapt(af::tiny<int, 2>(kmin_x,kmin_y)));
          af::flex_grid<>::index_type klast(af::adapt(af::tiny<int, 2>(kmax_x,kmax_y)));
          af::flex_grid<> kg(korigin, klast, false);
          af::flex_bool kspot_grid(kg);

          for (mask_t::const_iterator mt = spot_keys.begin(); mt!=spot_keys.end(); ++mt){
            kspot_grid[
              kg(af::adapt(mt->first - spot_position)) ]=true;
          }

          //show_array<af::flex_bool>(kspot_grid);
          //kspot_grid is a mask with the focus spot + all local, potentially overlapping spots

          //Now construct the guard mask
          af::flex_bool guard_mask = spot_grid.deep_copy();
          //show_array<af::flex_bool>(guard_mask);
          for (int ii=std::max(kg.origin()[0],g.origin()[0]);
                   ii<std::min(kg.last()[0],g.last()[0]);++ii){
            for (int jj=std::max(kg.origin()[1],g.origin()[1]);
                     jj<std::min(kg.last()[1],g.last()[1]);++jj){
              guard_mask[ g(af::adapt(af::tiny<int, 2>(ii,jj))) ]|=
              kspot_grid[kg(af::adapt(af::tiny<int, 2>(ii,jj))) ];
            }
          }
          //show_array<af::flex_bool>(guard_mask);

          //Now iterate over increments to find background pixels.
          int alt_bs = 0;
          for (int isort=0; isort<increments_xy.size(); ++isort){
            if (guard_mask[g(af::adapt(increments_xy[isort]))]==true){continue;}
            // pixels in the spot mask have been eliminated, now eliminate guard pixels
            bool in_guard_zone=false;
            for (int iguard=1; iguard<i_guard_width_limit; ++iguard){
              // Put assertion in for debug: SCITBX_ASSERT(guard_mask.size()>g(af::adapt(increments_xy[isort] + increments_xy[iguard])));
              if (guard_mask[g(
                  af::adapt(increments_xy[isort] + increments_xy[iguard]))]==true){
                   in_guard_zone=true;}
            }
            if (in_guard_zone){continue;}
            scitbx::vec2<int>candidate_bkgd=spot_position+increments_xy[isort];

            //Guard against background pixels off the active area
            if (check_tiles || use_mask_pixel_val) {
               int itile = tile_locations_m[i];
               if (check_tiles &&
                   (candidate_bkgd[0] < tiling_boundaries_m[4*itile] ||
                    candidate_bkgd[0] >= tiling_boundaries_m[4*itile+2] ||
                    candidate_bkgd[1] < tiling_boundaries_m[4*itile+1] ||
                    candidate_bkgd[1] >= tiling_boundaries_m[4*itile+3]))
                  {continue;}
               if (use_mask_pixel_val) {
                  int ivalue(rawdata(candidate_bkgd[0],candidate_bkgd[1]));
                  if (ivalue == mask_pixel_val)
                    {continue;}
               }
            }
            altB_S_mask[candidate_bkgd] = true;
            alt_bs+=1;
            if (alt_bs == BACKGROUND_FACTOR * base_spot_size){break;}
          }
          /* Diagnostics only
          af::flex_bool b_mask = spot_grid.deep_copy();
          for (mask_t::const_iterator key=altB_S_mask.begin();
               key != altB_S_mask.end(); ++key){
              b_mask[ g(af::adapt(key->first - spot_position)) ]=true;
          }
          printf("Background:\n");
          show_array<af::flex_bool>(b_mask);
          */
        }

        /*  insist that the background mask pixel count meets/exceeds that of
            the spot mask, otherwise flag the spot to be skipped: */
        if (  //makes better Figures for grant proposal with factor of two; add this as a phil parameter.
          altB_S_mask.size() >= BACKGROUND_FACTOR * std::max(I_S_mask.size(),(std::size_t)MIN_BACKGROUND_SZ)
        ) {
          BSmasks.push_back(altB_S_mask);
        } else {
          BSmasks.push_back(mask_t());
        }

      }
      scitbx::af::shared<scitbx::vec2<double> > return_detector_xy_draft;
      for (int i=0; i<detector_xy_draft.size(); ++i){
        return_detector_xy_draft.push_back(
          scitbx::vec2<double>(
            detector_xy_draft[i][0],detector_xy_draft[i][1]));
      }
      return return_detector_xy_draft;
    }

    void
    integration_proper_fast(scitbx::af::flex_int const& rawdata,
      scitbx::af::shared<scitbx::vec3<double> > predicted,
      scitbx::af::shared<cctbx::miller::index<> > hkllist,
      scitbx::af::shared<scitbx::vec2<double> > detector_xy_draft
      ){

      if (detector_gain<=0.) {
        throw scitbx::error("Unphysical gain; must be set with phil: integration.detector_gain="); }
      integrated_data.clear();
      integrated_sigma.clear();
      integrated_miller.clear();
      rejected_miller.clear();
      rejected_reason.clear();
      detector_xy.clear();
      integrated_flag = scitbx::af::shared<bool>(predicted.size());

      for (int i=0; i<predicted.size(); ++i){
        af::shared<double> signal;
        af::shared<double> bkgrnd;
        bool sig_bkg_is_overload = false;
        if (BSmasks[i].size()==0){
          rejected_miller.push_back(hkllist[i]);
          rejected_reason.push_back("out-of-boundary spot");
          continue;}

        for (mask_t::const_iterator k=ISmasks[i].begin();
                                    k != ISmasks[i].end(); ++k){
          double dvalue(rawdata(k->first[0],k->first[1]));
          if (dvalue >= detector_saturation) {sig_bkg_is_overload=true;}
          signal.push_back(dvalue);
        }
        rstbx::corrected_backplane BP(0,0);
        for (mask_t::const_iterator k=BSmasks[i].begin();
                                    k != BSmasks[i].end(); ++k){
          int ivalue(rawdata(k->first[0],k->first[1]));
          if (ivalue >= detector_saturation) {sig_bkg_is_overload=true;}
          bkgrnd.push_back(double(ivalue));
          BP.accumulate(k->first[0],k->first[1],ivalue);
        }
        if (sig_bkg_is_overload) {
          rejected_miller.push_back(hkllist[i]);
          rejected_reason.push_back("do not integrate if signal/background pixels are overloaded");
          continue;}
        try{
          BP.finish();
        } catch (rstbx::backplane_zero_determinant) {
          rejected_miller.push_back(hkllist[i]);
          rejected_reason.push_back("not possible to fit backplane, skip this spot");
          continue;
        }

        /*
        patch p;
        p.generate_profile(ISmasks[i], signal, BSmasks[i], bkgrnd);
        */

        af::shared<double> corr_signal;
        af::shared<double> corr_bkgrnd;

        for (mask_t::const_iterator k=ISmasks[i].begin();
                                    k != ISmasks[i].end(); ++k){
          corr_signal.push_back(double(rawdata(k->first[0],k->first[1])) -
                           BP.localmean(k->first[0],k->first[1]));
        }
        for (mask_t::const_iterator k=BSmasks[i].begin();
                                    k != BSmasks[i].end(); ++k){
          corr_bkgrnd.push_back(double(rawdata(k->first[0],k->first[1])) -
                           BP.localmean(k->first[0],k->first[1]));
        }

        double summation_intensity=0.0;
        double uncorrected_signal=0.0;
        for (int k=0; k<corr_signal.size(); ++k){
          summation_intensity += corr_signal[k];
          uncorrected_signal += signal[k];
        }
        int mcount = signal.size();
        int ncount = bkgrnd.size();
        double sum_background = 0.0;
        for (int k=0; k<bkgrnd.size(); ++k){
          sum_background += bkgrnd[k];
        }

        // Use gain == 1
        // variance formula from Andrew Leslie, Int Tables article
        double variance = uncorrected_signal +
          sum_background*mcount*mcount/double(ncount*ncount);
        variance *= detector_gain;
        if (variance<=0.) {
          rejected_miller.push_back(hkllist[i]);
          rejected_reason.push_back("a spot measured on an inactive area");
          continue;}
        double sigma = std::sqrt(variance);

        integrated_flag[i]=true;
        integrated_data.push_back(summation_intensity);
        integrated_sigma.push_back(sigma);
        integrated_miller.push_back(hkllist[i]);
        detector_xy.push_back(detector_xy_draft[i]);
        double max_ismask = *(std::max_element(signal.begin(), signal.end()));
        double max_bsmask = *(std::max_element(bkgrnd.begin(), bkgrnd.end()));
        max_signal.push_back( std::max(max_ismask, max_bsmask) );
      }
    }
  };

}} // namespace rstbx::simage

#endif// RSTBX_SIMPLE_INT_HPP
