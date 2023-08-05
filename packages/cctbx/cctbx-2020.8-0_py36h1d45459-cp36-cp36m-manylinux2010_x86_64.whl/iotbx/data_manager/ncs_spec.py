from __future__ import absolute_import, division, print_function
'''
'''

from iotbx.data_manager import DataManagerBase
from libtbx import Auto
import os

# =============================================================================
class NcsSpecDataManager(DataManagerBase):

  datatype = 'ncs_spec'

  # ---------------------------------------------------------------------------
  # Ncs spec
  def add_ncs_spec(self, filename, data):
    return self._add(NcsSpecDataManager.datatype, filename, data)

  def set_default_ncs_spec(self, filename):
    return self._set_default(NcsSpecDataManager.datatype, filename)

  def get_ncs_spec(self, filename=None):
    return self._get(NcsSpecDataManager.datatype, filename)

  def get_ncs_spec_names(self):
    return self._get_names(NcsSpecDataManager.datatype)

  def get_default_ncs_spec_name(self):
    return self._get_default_name(NcsSpecDataManager.datatype)

  def remove_ncs_spec(self, filename):
    return self._remove(NcsSpecDataManager.datatype, filename)

  def has_ncs_specs(self, expected_n=1, exact_count=False, raise_sorry=False):
    return self._has_data(NcsSpecDataManager.datatype, expected_n=expected_n,
                          exact_count=exact_count, raise_sorry=raise_sorry)

  def process_ncs_spec_file(self, filename):
    return self._process_file(NcsSpecDataManager.datatype, filename)

  def get_default_output_ncs_spec_filename(self):
    filename = self.get_default_output_filename()
    if not filename.endswith('.ncs_spec'):
      filename += '.ncs_spec'
    return filename

  def write_ncs_spec_file(self, ncs_object, filename=Auto, overwrite=Auto):

   # default options
    if (filename is Auto):
      filename = self.get_default_output_ncs_spec_filename()

    if (overwrite is Auto):
      overwrite = self._overwrite

    # check arguments
    if (os.path.isfile(filename) and (not overwrite)):
      raise Sorry('%s already exists and overwrite is set to %s.' %
                  (filename, overwrite))

    ncs_str = ncs_object.as_ncs_spec_string()
    try:
      self._write_text(NcsSpecDataManager.datatype, ncs_str,
                     filename=filename, overwrite=overwrite)
    except IOError as err:
      raise Sorry('There was an error with writing %s.\n%s' %
                  (filename, err))

    self._output_files.append(filename)
    self._output_types.append(NcsSpecDataManager.datatype)



# =============================================================================
# end
