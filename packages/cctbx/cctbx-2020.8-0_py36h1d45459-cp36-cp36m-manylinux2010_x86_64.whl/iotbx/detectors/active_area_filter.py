from __future__ import absolute_import, division, print_function
from six.moves import range
from scitbx.array_family import flex

class active_area_filter:
  NEAR = 2
  def __init__(self,IT):
    from scitbx import matrix
    self.IT = IT
    from annlib_ext import AnnAdaptor

    reference = flex.double()

    for i in range(len(IT)//4):
      UL = matrix.col((float(IT[4*i]),float(IT[4*i+1])))
      LR = matrix.col((float(IT[4*i+2]),float(IT[4*i+3])))
      center = (UL+LR)/2.
      reference.append(center[0])
      reference.append(center[1])
    self.adapt = AnnAdaptor(data=reference,dim=2,k=self.NEAR)
  def __call__(self,predictions,hkllist,pxlsz):
    if len(self.IT) == 4:
      # We have only one tile, AnnAdaptor chokes in this case but then there is
      # only one choice of nearest neighbour anyway!
      nearest_neighbours = flex.int(len(predictions)*self.NEAR, 0)
    else:
      query = flex.double()
      for pred in predictions:
        query.append(pred[0]/pxlsz)
        query.append(pred[1]/pxlsz)
      self.adapt.query(query)
      assert len(self.adapt.nn)==len(predictions)*self.NEAR
      nearest_neighbours = self.adapt.nn
    selection = flex.bool()
    self.tile_id = flex.int()
    for p in range(len(predictions)):
      is_in_active_area = False
      for n in range(self.NEAR):
        itile = nearest_neighbours[p*self.NEAR+n]
        if self.IT[4*itile]<predictions[p][0]/pxlsz<self.IT[4*itile+2] and\
           self.IT[4*itile+1]<predictions[p][1]/pxlsz<self.IT[4*itile+3]:
          is_in_active_area = True;break
      if is_in_active_area:
        self.tile_id.append(itile)
      selection.append(is_in_active_area)
    assert selection.count(True) == len(self.tile_id)
    return predictions.select(selection),hkllist.select(selection)
