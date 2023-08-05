from __future__ import absolute_import, division, print_function
from six.moves import range
import copy
from iotbx.detectors import ReadADSC
from scitbx.array_family import flex
import sys

class DetectorImageBase(object):
  def __init__(self,filename):
    self.filename=filename
    self.parameters=None
    self.linearintdata=None
    self.bin=1
    self.vendortype = "baseclass"
    self.beam_center_reference_frame = "instrument"#cf beam_center_convention.py
    self.beam_center_convention = None
    self.vendor_specific_null_value = 0

  def copy_common_attributes_from_parent_instance(self, parentobject):
    self.filename = copy.copy(parentobject.filename)
    self.bin = copy.copy(parentobject.bin)
    self.vendortype = copy.copy(parentobject.vendortype)
    self.beam_center_reference_frame = copy.copy(parentobject.beam_center_reference_frame)
    self.beam_center_convention = copy.copy(parentobject.beam_center_convention)
    self.header = copy.copy(parentobject.header)
    self.headerlines = copy.copy(parentobject.headerlines)

  def setBin(self,bin): #software binning.
                        # the only bin values supported are 1 & 2
    if self.bin!=1 or bin!=2: return
    if self.size1%bin!=0: return
    self.parameters['SIZE1']=self.parameters['SIZE1']//bin
    self.parameters['SIZE2']=self.parameters['SIZE2']//bin
    if 'CCD_IMAGE_SATURATION' in self.parameters:
      self.parameters['CCD_IMAGE_SATURATION']=self.parameters['CCD_IMAGE_SATURATION']*bin*bin
    self.parameters['PIXEL_SIZE']=self.parameters['PIXEL_SIZE']*bin
    self.bin = bin
    self.bin_safe_set_data(self.linearintdata)

  def set_beam_center_convention(self,beam_center_convention):
    from iotbx.detectors.beam_center_convention import convert_beam_instrument_to_imageblock
    convert_beam_instrument_to_imageblock(self,beam_center_convention)

  def fileLength(self):
    self.readHeader()
    return self.dataoffset()+self.size1*self.size2*self.integerdepth()
    # dataoffset() and integerdepth() must be defined in derived class
    # pure supposition:
    #  size1 corresponds to number of rows.  Columns are slow.
    #  size2 corresponds to number of columns.  Rows are fast.

  def getEndian(self):
    raise NotImplementedError # must be defined in derived class

  def endian_swap_required(self):
    data_is_big_endian = self.getEndian()
    import struct
    platform_is_big_endian = (
      struct.unpack('i',struct.pack('>i',3000))[0] == 3000
    )
    return data_is_big_endian != platform_is_big_endian

  def read(self):
    self.fileLength()
    self.bin_safe_set_data(
         ReadADSC(self.filename,self.dataoffset(),
         self.size1*self.bin,self.size2*self.bin,self.getEndian())
         )

  def bin_safe_set_data(self, new_data_array):
    #private interface for software binning 2 X 2.
    #  Any setting of linearintdata must be through this function
    #  self.bin==2: when data are read lazily, they must be binned
    #  new_data_array.bin2by2==True: the data have been binned
    if self.bin==2 and \
       new_data_array != None and\
       new_data_array.__dict__.get("bin2by2")!=True:
      from iotbx.detectors import Bin2_by_2
      self.linearintdata = Bin2_by_2(new_data_array)
      self.linearintdata.bin2by2 = True
    else:
      self.linearintdata = new_data_array

  def get_data_type(self):
    typehash = str(self.linearintdata.__class__)
    if typehash.find("int")>=0: return "int"
    elif typehash.find("double")>=0: return "double"

  def get_raw_data(self):
    return self.linearintdata

  def get_flex_image(self, binning=1, brightness=1.0, color_scheme=0):
    datatype = self.get_data_type()
    if datatype=="int":
      from iotbx.detectors import FlexImage
    elif datatype=="double":
      from iotbx.detectors import FlexImage_d as FlexImage
    return FlexImage(
      rawdata=self.linearintdata,
      binning=binning,
      vendortype=self.vendortype,
      brightness=brightness,
      saturation=int(getattr(self, "saturation", 65535)),
      color_scheme=color_scheme)

  data_types = dict( SIZE1=int, SIZE2=int, PIXEL_SIZE=float,
                     DISTANCE=float, TWOTHETA=float, OSC_RANGE=float,
                     OSC_START=float, PHI=float, WAVELENGTH=float,
                     BEAM_CENTER_X=float, BEAM_CENTER_Y=float,
                     CCD_IMAGE_SATURATION=int, DETECTOR_SN=str )

  def get_spotfinder(self,distl_params): #following heuristics_base.register_frames() example
    #application-specific adjustments to parameters
    #XXX this should probably be a deep copy of parameters.
    if distl_params.distl.res.inner!=None:
      distl_params.distl_lowres_limit = distl_params.distl.res.inner
    if distl_params.distl.res.outer!=None:
      distl_params.force_method2_resolution_limit = distl_params.distl.res.outer
      distl_params.distl_highres_limit = distl_params.distl.res.outer

    distl_params.distl_force_binning = False
    distl_params.distl_permit_binning = False
    distl_params.wedgelimit = 1
    distl_params.spotfinder_header_tests = False

    #unusual location for min spot area tests...
    from iotbx.detectors.context.config_detector import beam_center_convention_from_image_object
    beam_center_convention_from_image_object(self,distl_params)
    # end special min spot area treatment

    from spotfinder.applications.practical_heuristics import heuristics_base
    from spotfinder.diffraction.imagefiles import file_names
    class empty:pass
    E = empty()
    E.argv = ["Empty",self.filename]
    names = file_names(E)
    this_frame = names.frames()[0]
    process_dictionary = dict(twotheta = "%f"%self.twotheta,
       ybeam = "%f"%self.beamy,
       xbeam = "%f"%self.beamx,
       distance = "%f"%self.distance,
       wavelength = "%f"%self.wavelength,
       template = [item.template for item in names.FN if item.number==this_frame][0],
                              )
    Spotfinder = heuristics_base(process_dictionary,distl_params)
    Spotfinder.images[this_frame] = Spotfinder.oneImage(this_frame,
      Spotfinder.pd, self)
    Spotfinder.determine_maxcell(this_frame,Spotfinder.pd)
    Spotfinder.images[this_frame]['spotoutput']['relpath']=self.filename
    from spotfinder.applications.stats_distl import pretty_image_stats
    pretty_image_stats(Spotfinder,this_frame)
    return Spotfinder,this_frame

  def debug_write(self,fileout,mod_data=None):
    if "TWOTHETA" not in self.parameters:
      self.parameters["TWOTHETA"]=0.0
    from iotbx.detectors import ImageException
    try:
      endian = self.getEndian()
      if endian==1:
        self.parameters["BYTE_ORDER"]="big_endian"
      else:
        self.parameters["BYTE_ORDER"]="little_endian"
    except ImageException:
      endian = 0
      self.parameters["BYTE_ORDER"]="little_endian"

    if "DETECTOR_SN" in self.parameters:
      try:
        self.parameters["DETECTOR_SN"] = int(self.parameters["DETECTOR_SN"])
      except ValueError:
        self.parameters["DETECTOR_SN"] = 0
    else:
      self.parameters["DETECTOR_SN"] = 0

    #handle pilatus
    if self.parameters['SIZE1'] == 2527 and self.parameters['SIZE2'] == 2463:
      self.parameters['SIZE1'] = 2463
      self.parameters['SIZE2'] = 2527

    #handle eiger-1M
    if self.parameters['SIZE1'] == 1065 and self.parameters['SIZE2'] == 1030:
      self.parameters['SIZE1'] = 1030
      self.parameters['SIZE2'] = 1065

    #handle eiger-4M
    if self.parameters['SIZE1'] == 2167 and self.parameters['SIZE2'] == 2070:
      self.parameters['SIZE1'] = 2070
      self.parameters['SIZE2'] = 2167

    #handle eiger-9M
    if self.parameters['SIZE1'] == 3269 and self.parameters['SIZE2'] == 3110:
      self.parameters['SIZE1'] = 3110
      self.parameters['SIZE2'] = 3269

    #handle eiger-1M
    if self.parameters['SIZE1'] == 4371 and self.parameters['SIZE2'] == 4150:
      self.parameters['SIZE1'] = 4150
      self.parameters['SIZE2'] = 4371

    info = """{
HEADER_BYTES= 1024;
DIM=2;
BYTE_ORDER=%(BYTE_ORDER)s;
TYPE=unsigned_short;
SIZE1=%(SIZE1)4d;
SIZE2=%(SIZE2)4d;
PIXEL_SIZE=%(PIXEL_SIZE)8.6f;
TIME=0.000000;
DISTANCE=%(DISTANCE).2f;
TWOTHETA=%(TWOTHETA).2f;
PHI=%(OSC_START).3f;
OSC_START=%(OSC_START).3f;
OSC_RANGE=%(OSC_RANGE).3f;
WAVELENGTH=%(WAVELENGTH).6f;
BEAM_CENTER_X=%(BEAM_CENTER_X).2f;
BEAM_CENTER_Y=%(BEAM_CENTER_Y).2f;
CCD_IMAGE_SATURATION=65535;
DETECTOR_SN=%(DETECTOR_SN)d;
}\f"""%self.parameters
    with open(fileout, "w") as F:
      F.write(info)
      len_null=1024-len(info)
    with open(fileout, "ab") as F:
      F.write(b'\0'*len_null)

    from iotbx.detectors import WriteADSC
    if mod_data==None: mod_data=self.linearintdata
    if not mod_data.all_ge(0):
      from libtbx.utils import Sorry
      raise Sorry("Negative values not allowed when writing SMV")
    WriteADSC(fileout,mod_data,self.size1,self.size2,endian)

  def __getattr__(self, attr):
    # Returns the computed attribute value or raises an AttributeError
    # exception.  This method is only called when an attribute could
    # not be looked up in the usual places.
    if   attr=='size1' : return self.parameters['SIZE1']
    elif attr=='size2' : return self.parameters['SIZE2']
    elif attr=='npixels' : return self.parameters['SIZE1'] * self.parameters['SIZE2']
    elif attr=='saturation' : return self.parameters.get('CCD_IMAGE_SATURATION',65535)
    elif attr=='rawdata' : return self.linearintdata
    elif attr=='pixel_size' : return self.parameters['PIXEL_SIZE']
    elif attr=='osc_start' : return self.parameters.get('OSC_START',0.0)
    elif attr=='distance' : return self.parameters['DISTANCE']
    elif attr=='wavelength' : return self.parameters.get('WAVELENGTH',0.0)
    elif attr=='beamx' : return self.parameters['BEAM_CENTER_X']
    elif attr=='beamy' : return self.parameters['BEAM_CENTER_Y']
    elif attr=='deltaphi' : return self.parameters.get('OSC_RANGE',0.0)
    elif attr=='twotheta' : return self.parameters.get('TWOTHETA',0.0)
    elif attr=='serial_number' : return self.parameters['DETECTOR_SN']
    raise AttributeError

  def show_header(self, out=None):
    if (out is None):
      out = sys.stdout
    print("File:",self.filename, file=out)
    print("Number of pixels: slow=%d fast=%d"%(self.size1,self.size2), file=out)
    print("Pixel size: %f mm"%self.pixel_size, file=out)
    print("Saturation: %.0f"%self.saturation, file=out)
    print("Detector distance: %.2f mm"%self.distance, file=out)
    print("Detector 2theta swing: %.2f deg."%self.twotheta, file=out)
    print("Rotation start: %.2f deg."%self.osc_start, file=out)
    print("Rotation width: %.2f deg."%self.deltaphi, file=out)
    print("Beam center: x=%.2f mm  y=%.2f mm"%(self.beamx,self.beamy), file=out)
    print("Wavelength: %f Ang."%self.wavelength, file=out)

  # code developed for the image viewer. phil_parameters is a scope extract
  def initialize_viewer_properties(self,phil_parameters,verbose=True):

    self._invert_beam_center = False
    from iotbx.detectors.context.config_detector import \
      beam_center_convention_from_image_object
    bc = beam_center_convention_from_image_object(self,phil_parameters)
    if verbose:
      print("beam center convention: %d" % bc)
    # FIXME what about 2-4 & 6-7?
    if (bc == 0):
      self._invert_beam_center = True
      self._invert_y = True
    elif (bc == 1):
      self._invert_y = False
    elif (bc == 5):
      self._invert_y = True

    self.image_size_fast = self.size2 # width
    self.image_size_slow = self.size1 # height
    self.pixel_resolution = self.pixel_size

  def detector_coords_as_image_coords_float(self, x, y):
    """
    Convert absolute detector position (in mm) to floating-value image pixel coordinates.
    """
    dw = self.image_size_fast * self.pixel_resolution
    dh = self.image_size_slow * self.pixel_resolution
    x_frac = x / dw
    if (self._invert_y):
      y_frac = - ((y / dh) - 1.0)
    else :
      y_frac = y / dh
    return x_frac * self.image_size_fast, \
           y_frac * self.image_size_slow

  def detector_coords_as_image_coords(self, x, y):
    """
    Convert absolute detector position (in mm) to integer-value image pixel coordinates.
    """
    x_point,y_point = self.detector_coords_as_image_coords_float(x,y)
    return (int(x_point), int(y_point))

  def image_coords_as_detector_coords(self, x, y, readout=None):
    """
    Convert image pixel coordinates to absolute position on the detector
    (in mm).
    """
    dw = self.image_size_fast * self.pixel_resolution
    dh = self.image_size_slow * self.pixel_resolution
    x_frac = x / self.image_size_fast
    y_frac = y / self.image_size_slow
    x_detector = x_frac * dw
    if (self._invert_y):
      y_detector = (1.0 - y_frac) * dh
    else :
      y_detector = y_frac * dh
    return x_detector, y_detector

  def get_beam_center_mm(self):
    # FIXME Pilatus and ADSC images appear to have different conventions???
    if (self._invert_beam_center):
      center_x = self.beamy
      center_y = self.beamx
    else :
      center_x = self.beamx
      center_y = self.beamy
    return center_x, center_y

  def get_beam_center_pixels_fast_slow(self):
    center_x, center_y = self.get_beam_center_mm()
    return self.detector_coords_as_image_coords_float(center_x, center_y)

  def get_pixel_intensity(self,coords):
    try:
      return self.linearintdata[(int(coords[0]), int(coords[1]))]
    except IndexError:
      return None

  def get_tile_manager(self, phil):
    return tile_manager_base(
      phil,beam=(int(self.beamx/self.pixel_size),
                 int(self.beamy/self.pixel_size)),
           reference_image=self,
           size1=self.size1,
           size2=self.size2)


class tile_manager_base(object):

  def __init__(self, working_params, beam=None, size1=None, size2=None,
               reference_image=None):

    self.working_params = working_params
    self.beam = beam # direct beam position supplied as slow,fast pixels
    self.size1 = size1
    self.size2 = size2
    self.reference_image = reference_image

  def effective_tiling_as_flex_int(self, reapply_peripheral_margin=False,
                                   reference_image=None,
                                   encode_inactive_as_zeroes=False, **kwargs):
    """Some documentation goes here"""

    if reference_image is not None:
      self.reference_image = reference_image

    IT = self.effective_tiling_as_flex_int_impl(**kwargs)

    # Inactive margin around the edge of the sensor
    if reapply_peripheral_margin:
      try:    peripheral_margin = self.working_params.distl.peripheral_margin
      except Exception: peripheral_margin = 2
      for i in range(len(IT) // 4):
        IT[4 * i + 0] += peripheral_margin
        IT[4 * i + 1] += peripheral_margin
        IT[4 * i + 2] -= peripheral_margin
        IT[4 * i + 3] -= peripheral_margin

    if self.working_params.distl.tile_flags is not None and encode_inactive_as_zeroes is False:
      #sensors whose flags are set to zero are not analyzed by spotfinder
      #this returns an active list with fewer tiles
      expand_flags=[]
      for flag in self.working_params.distl.tile_flags :
        expand_flags=expand_flags + [flag]*4
      bool_flags = flex.bool( flex.int(expand_flags)==1 )
      return IT.select(bool_flags)

    if self.working_params.distl.tile_flags is not None and encode_inactive_as_zeroes is True:
      #sensors whose flags are set to zero are identified
      #this returns a same-length active list with some tiles set to 0,0,0,0
      expand_flags=[]
      for flag in self.working_params.distl.tile_flags :
        expand_flags=expand_flags + [flag]*4
      Zero_IT = flex.int()
      for idx in range(len(IT)):
        Zero_IT.append(expand_flags[idx]*IT[idx])
      return Zero_IT

    return IT

  def effective_tiling_as_flex_int_impl(self, **kwargs):
    assert self.reference_image is not None

    IT = flex.int()
    from iotbx.detectors import image_divider
    if self.reference_image.linearintdata is None:
      self.reference_image.readHeader()
      self.reference_image.read()
    null_value = self.reference_image.vendor_specific_null_value
    divider = image_divider(
      self.reference_image.linearintdata,
      null_value
      )

    for i in range(divider.module_count()):
      slow = divider.tile_slow_interval(i)
      fast = divider.tile_fast_interval(i)
      IT.append(slow.first)
      IT.append(fast.first)
      IT.append(slow.last+1)
      IT.append(fast.last+1)

    return IT
