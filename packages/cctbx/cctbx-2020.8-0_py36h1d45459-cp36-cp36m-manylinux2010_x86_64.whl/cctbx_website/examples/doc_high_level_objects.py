from __future__ import absolute_import, division, print_function
from iotbx.map_model_manager import map_model_manager      # load in the map_model_manager
mmm=map_model_manager()     # get an initialized instance of the map_model_manager
mmm.generate_map()     # get a model from a small library model and calculate a map for it
mmm.write_map("map.mrc")     # write out a map in ccp4/mrc format
mmm.write_model("model.pdb")     # write out a model in PDB format
