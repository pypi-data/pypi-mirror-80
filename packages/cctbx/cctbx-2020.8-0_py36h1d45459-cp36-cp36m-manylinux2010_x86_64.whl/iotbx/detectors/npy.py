from __future__ import absolute_import, division, print_function
from six.moves import range
# -*- Mode: Python; c-basic-offset: 2; indent-tabs-mode: nil; tab-width: 8; -*-

from iotbx.detectors.detectorbase import DetectorImageBase, tile_manager_base
from scitbx.array_family          import flex
import six
from six.moves import cPickle as pickle

def image_dict_to_unicode(data):
  if not data or six.PY2: return data
  for key in list(data.keys()): # modifying dict so need list of keys up front or iterator breaks
    if isinstance(data[key], bytes):
      data[key] = data[key].decode()
    if isinstance(key, bytes):
      data[key.decode()] = data[key]
      del data[key]
  return data

class NpyImage(DetectorImageBase):
  def __init__(self, filename, source_data = None):
    DetectorImageBase.__init__(self, filename)
    self.vendortype = "npy_raw"
    self.source_data = image_dict_to_unicode(source_data)

  def readHeader(self, horizons_phil):
    version_control = horizons_phil.distl.detector_format_version

    if self.source_data == None:
      with open(self.filename, "rb") as fh:
        if six.PY3:
          cspad_data = image_dict_to_unicode(pickle.load(fh, encoding="bytes"))
        else:
          cspad_data = pickle.load(fh)
    else:
      cspad_data = self.source_data

    # XXX assert that cspad_data['image'].ndim is 2?

    self.parameters                         = {}

    if version_control == "CXI 3.1":
      import numpy
      self.parameters['SIZE1']                = cspad_data['image'].shape[0] # XXX order?
      self.parameters['SIZE2']                = cspad_data['image'].shape[1] # XXX order?
      self.parameters['PIXEL_SIZE']           = 110e-3 # XXX fiction
      self.parameters['BEAM_CENTER_X']        = 0.5 * self.parameters['SIZE1'] * self.parameters['PIXEL_SIZE']  # XXX order?
      self.parameters['BEAM_CENTER_Y']        = 0.5 * self.parameters['SIZE2'] * self.parameters['PIXEL_SIZE']  # XXX order?
      self.parameters['CCD_IMAGE_SATURATION'] = 2**14 - 1
      self.parameters['DISTANCE']             = 93   # XXX fiction
      self.parameters['OSC_START']            = 0    # XXX fiction
      self.parameters['OSC_RANGE']            = 0    # XXX fiction
      self.parameters['SATURATED_VALUE']      = 2**14 - 1
      self.parameters['TWOTHETA']             = 0    # XXX fiction
      # From Margaritondo & Rebernik Ribic (2011): the dimensionless
      # relativistic gamma-factor is derived from beam energy in MeV and
      # the electron rest mass, K is a dimensionless "undulator
      # parameter", and L is the macroscopic undulator period in
      # Aangstroem (XXX).  See also
      # http://ast.coe.berkeley.edu/srms/2007/Lec10.pdf.  XXX This
      # should really move into the pyana code, since the parameters are
      # SLAC-specific.
      gamma                         = cspad_data['beamEnrg'] / 0.510998910
      K                             = 3.5
      L                             = 3.0e8
      self.parameters['WAVELENGTH'] = L / (2 * gamma**2) * (1 + K**2 / 2)
      SI = cspad_data['image'].astype(numpy.int32)
      SI = flex.int(SI)
      self.bin_safe_set_data(SI)
    elif version_control in ["CXI 3.2","CXI 4.1","CXI 5.1","CXI 6.1","CXI 7.1","CXI 7.d","XPP 7.1","XPP 7.marccd",
                             "CXI 8.1","CXI 8.d","XPP 8.1","XPP 8.marccd","CXI 8.2","Sacla.MPCCD","CXI 9.1","XPP 9.1",
                             "CXI 10.1","CXI 10.2","CXI 11.1","CXI 11.2", "XPP 11.1","Sacla.MPCCD.8tile"]:
      self.parameters['ACTIVE_AREAS']         = cspad_data.get('ACTIVE_AREAS', None)
      self.parameters['BEAM_CENTER_X']        = cspad_data['BEAM_CENTER_X']
      self.parameters['BEAM_CENTER_Y']        = cspad_data['BEAM_CENTER_Y']
      self.parameters['CCD_IMAGE_SATURATION'] = cspad_data['CCD_IMAGE_SATURATION']
      self.parameters['DISTANCE']             = cspad_data['DISTANCE']
      self.parameters['OSC_RANGE']            = 0 # XXX fiction
      self.parameters['OSC_START']            = 0 # XXX fiction
      self.parameters['PIXEL_SIZE']           = cspad_data['PIXEL_SIZE']
      self.parameters['SATURATED_VALUE']      = cspad_data['SATURATED_VALUE']
      self.parameters['MIN_TRUSTED_VALUE']    = cspad_data.get('MIN_TRUSTED_VALUE', 0)
      self.parameters['SIZE1']                = cspad_data['SIZE1']
      self.parameters['SIZE2']                = cspad_data['SIZE2']
      self.parameters['TWOTHETA']             = 0 # XXX fiction
      self.parameters['WAVELENGTH']           = cspad_data['WAVELENGTH']
      self.bin_safe_set_data(cspad_data['DATA'])

      if (self.parameters['ACTIVE_AREAS'] is not None):
        horizons_phil.distl.detector_tiling = self.parameters['ACTIVE_AREAS']
    elif version_control is None:
      #approrpiate for detectors other than the CS-PAD diffraction detectors
      self.parameters['ACTIVE_AREAS']         = cspad_data.get('ACTIVE_AREAS', None)
      self.parameters['BEAM_CENTER_X']        = cspad_data.get('BEAM_CENTER_X',None)
      self.parameters['BEAM_CENTER_Y']        = cspad_data.get('BEAM_CENTER_Y',None)
      self.parameters['CCD_IMAGE_SATURATION'] = cspad_data['CCD_IMAGE_SATURATION']
      self.parameters['DISTANCE']             = cspad_data.get('DISTANCE',None)
      self.parameters['PIXEL_SIZE']           = cspad_data['PIXEL_SIZE']
      self.parameters['SATURATED_VALUE']      = cspad_data['SATURATED_VALUE']
      self.parameters['MIN_TRUSTED_VALUE']    = cspad_data.get('MIN_TRUSTED_VALUE', 0)
      self.parameters['SIZE1']                = cspad_data['SIZE1']
      self.parameters['SIZE2']                = cspad_data['SIZE2']
      self.parameters['WAVELENGTH']           = cspad_data['WAVELENGTH']
      if 'OSC_RANGE' in cspad_data and cspad_data['OSC_RANGE'] > 0:
        self.parameters['OSC_START']            = cspad_data.get('OSC_START',None)
        self.parameters['OSC_RANGE']            = cspad_data.get('OSC_RANGE',None)
      import math
      if  ( math.isnan(self.parameters["DISTANCE"]) ):
         self.parameters["DISTANCE"]=0.0
      self.bin_safe_set_data(cspad_data['DATA'])
      if (self.parameters['ACTIVE_AREAS'] is not None):
        horizons_phil.distl.detector_tiling = self.parameters['ACTIVE_AREAS']


    if version_control not in ["CXI 3.1", "CXI 3.2"]:
      if horizons_phil.distl.tile_translations==None and \
         horizons_phil.distl.detector_tiling is not None:
          horizons_phil.distl.tile_translations = [0]*(int(len(horizons_phil.distl.detector_tiling)/2))


  # This is nop, because all the data has been read by readHeader().
  # The header information and the data are all contained in the same
  # pickled object.
  def read(self):
    pass

  def translate_tiles(self, phil):
    if phil.distl.detector_tiling==None: return
    if phil.distl.tile_translations==None: return

    if len(phil.distl.detector_tiling) <= 16:
      # assume this is the 2x2 CS Pad for spectroscopy; do not use tile translations
      if phil.distl.detector_format_version in ["CXI 4.1"]:
        # For the Run 4 CXI detector, the first sensor is inactive and pegged high(16K).
        # For calculating display contrast it is better to eliminate the sensor.
        if self.size1 == 370: #there are two sensors; we should eliminate the first
          self.parameters['SIZE1'] = 185
          self.linearintdata = self.linearintdata[int(len(self.linearintdata)/2):]
          self.linearintdata.reshape(flex.grid(self.size1,self.size2))
        print("CXI 2x2 size",self.size1,self.size2, self.linearintdata.focus())
      return

    assert 2 * len(phil.distl.tile_translations) == len(phil.distl.detector_tiling)

    shifted_int_data_old = self.__getattr__('rawdata')
    # Use __class__ attribute to transparently transform either flex.int or flex.double
    shifted_int_data_new = shifted_int_data_old.__class__(
      flex.grid(shifted_int_data_old.focus()))

    manager = self.get_tile_manager(phil)

    for i,shift in enumerate(manager.effective_translations()):
      shift_slow = shift[0]
      shift_fast = shift[1]

      ur_slow = phil.distl.detector_tiling[4 * i + 0]
      ur_fast = phil.distl.detector_tiling[4 * i + 1]
      ll_slow = phil.distl.detector_tiling[4 * i + 2]
      ll_fast = phil.distl.detector_tiling[4 * i + 3]

      #print "Shifting tile at (%d, %d) by (%d, %d)" % (ur_slow, ur_fast, shift_slow, shift_fast)

      shifted_int_data_new.matrix_paste_block_in_place(
        block = shifted_int_data_old.matrix_copy_block(
          i_row=ur_slow,i_column=ur_fast,
          n_rows=ll_slow-ur_slow, n_columns=ll_fast-ur_fast),
        i_row = ur_slow + shift_slow,
        i_column = ur_fast + shift_fast
      )

    self.bin_safe_set_data(shifted_int_data_new)

  def correct_gain_in_place(self, filename, adu_scale, phil):
    stddev = NpyImage( filename )
    stddev.readHeader(phil)
    stddev.translate_tiles(phil)
    self.bin_safe_set_data( (adu_scale*self.linearintdata)/(1+stddev.linearintdata) )

  def correct_background_in_place(self, phil):

    """The 'in place' function actually changes the raw data in this image object"""
    active_areas = self.get_tile_manager(phil).effective_tiling_as_flex_int()
    B = active_areas

    assert len(active_areas)%4 == 0
    # apply an additional margin of 1 pixel, since we don't seem to be
    # registering the global peripheral margin.  XXX this should be changed later
    asics = [(B[i]+1,B[i+1]+1,B[i+2]-1,B[i+3]-1) for i in range(0,len(B),4)]

    for asic in asics:
      self.linearintdata.matrix_paste_block_in_place(
        block = self.correct_background_by_block(asic),
        i_row = asic[0],
        i_column = asic[1]
      )

    self.bin_safe_set_data(self.linearintdata)

  def correct_background_by_block(self, asic):
    """The 'by block' function doesn't changes the object data, it just returns the
       filtered data for a particular detector asic"""

    from iotbx.detectors.util.filters import background_correct_padded_block
    corrected_data = background_correct_padded_block(self.linearintdata, asic)
    return corrected_data

  def get_tile_manager(self, phil):
    return tile_manager(phil,beam=(int(self.beamx/self.pixel_size),
                                   int(self.beamy/self.pixel_size)),
                             size1=self.size1,
                             size2=self.size2)

  def debug_write(self,fileout,mod_data=None):
    try:
      if mod_data == None:
        mod_data = self.get_raw_data().iround()
    except AttributeError:
      pass

    DetectorImageBase.debug_write(self,fileout,mod_data)

  def getEndian(self):
    return 1   # big!  arbitrary


class tile_manager(tile_manager_base):

  def effective_translations(self):

    # if there are quadrant translations, do some extra work to apply them
    if self.working_params.distl.quad_translations != None:
      from scitbx.matrix import col
      beam = col(self.beam)
      for itile in range(len(self.working_params.distl.detector_tiling) // 4):
        tile_center = (
          col(self.working_params.distl.detector_tiling[4*itile:4*itile+2]) +
          col(self.working_params.distl.detector_tiling[4*itile+2:4*itile+4]))/2
        delta = tile_center-beam
        iquad = [(True,True),(True,False),(False,True),(False,False)
                ].index((delta[0]<0, delta[1]<0)) # UL,UR,LL,LR
        yield (self.working_params.distl.tile_translations[2 * itile + 0] +
               self.working_params.distl.quad_translations[2 * iquad + 0],
               self.working_params.distl.tile_translations[2 * itile + 1] +
               self.working_params.distl.quad_translations[2 * iquad + 1])
      return

    for i in range(len(self.working_params.distl.tile_translations) // 2):
       yield (self.working_params.distl.tile_translations[2 * i + 0],
              self.working_params.distl.tile_translations[2 * i + 1])

  def effective_tiling_as_flex_int_impl(self, **kwargs):
    import copy
    IT = flex.int(copy.copy(self.working_params.distl.detector_tiling))

    assert len(IT)%4==0 # only meaningful for groups of 4
    for itl in range(0,len(IT),4): # validate upper-left/ lower-right ordering
      assert IT[itl] < IT[itl+2]; assert IT[itl+1] < IT[itl+3]

    if self.working_params.distl.tile_translations!=None and \
      2*len(self.working_params.distl.tile_translations) == len(IT):
      #assume that the tile translations have already been applied at the time
      #the file is read; now they need to be applied to the spotfinder tile boundaries

      #check if beam position has been supplied
      self.beam = kwargs.get("beam",self.beam)

      for i,shift in enumerate(self.effective_translations()):
        shift_slow = shift[0]
        shift_fast = shift[1]
        IT[4 * i + 0] += shift_slow
        IT[4 * i + 1] += shift_fast
        IT[4 * i + 2] += shift_slow
        IT[4 * i + 3] += shift_fast
    return IT

#if __name__=='__main__':
#  import sys
#  i = sys.argv[1]
#  a = SaturnImage(i)
#  a.readHeader()
#  a.read()
