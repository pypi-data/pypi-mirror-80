from __future__ import absolute_import, division, print_function
import sys
from six.moves import range

def head(f=None):
  if (f is None): f = sys.stdout
  print('''\
<?xml version="1.0" encoding="ISO-8859-1" standalone="yes"?>
<!DOCTYPE jvx-model SYSTEM "http://www.javaview.de/rsrc/jvx.dtd">
<jvx-model>
<geometries>''', file=f)

def tail(f=None):
  if (f is None): f = sys.stdout
  print('''\
</geometries>
</jvx-model>''', file=f)

def jvx_item_colors(f, indent, items):
  print(indent + '<colors>', file=f)
  for item in items:
    print(indent + '  <c>%d %d %d</c>' % item.color, file=f)
  print(indent + '</colors>', file=f)

class point(object):

  def __init__(self, vertex, color=(255,0,0)):
    self.vertex = tuple(vertex)
    self.color = tuple(color)

def make_point(vertex):
  return point(vertex)

class pointSet(object):

  def __init__(self, thickness=4):
    self.thickness = thickness
    self.points = []
    self.point_dict = {}
    self.show_points = "show"

  def size(self):
    return len(self.points)

  def append(self, point):
    if (not hasattr(point, "vertex")):
      point = make_point(point)
    if (not point.vertex in self.point_dict):
      self.point_dict[point.vertex] = len(self.points)
      self.points.append(point)

  def extend(self, points):
    for point in points:
      self.append(point)

  def index(self, point):
    if (hasattr(point, "vertex")):
      return self.point_dict[point.vertex]
    return self.point_dict[tuple(point)]

  def hide_points(self):
    self.show_points = "hide"
    return self

  def jvx(self, f=None):
    if (f is None): f = sys.stdout
    if (self.size() == 0): return
    print('<pointSet dim="3" point="%s" color="show">' % self.show_points, file=f)
    print('  <points>', file=f)
    for point in self.points:
      print('    <p>%g %g %g</p>' % point.vertex, file=f)
    jvx_item_colors(f, "    ", self.points)
    print('    <thickness>%g</thickness>' % self.thickness, file=f)
    print('  </points>', file=f)
    print('</pointSet>', file=f)

class line(object):

  def __init__(self, vertices, color=(0,0,0)):
    self.vertices = tuple(vertices)
    self.color = tuple(color)

class lineSet(object):

  def __init__(self, thickness=1):
    self.thickness = thickness
    self.lines = []

  def size(self):
    return len(self.lines)

  def append(self, line):
    self.lines.append(line)

  def jvx(self, f=None):
    if (f is None): f = sys.stdout
    print('<lineSet line="show" color="show">', file=f)
    print('  <lines>', file=f)
    for line in self.lines:
      print('    <l>', end=' ', file=f)
      for v in line.vertices: print(v, end=' ', file=f)
      print('</l>', file=f)
    jvx_item_colors(f, "    ", self.lines)
    print('    <thickness>%g</thickness>' % self.thickness, file=f)
    print('  </lines>', file=f)
    print('</lineSet>', file=f)

class face(object):

  def __init__(self, vertices, color=(255,0,255)):
    self.vertices = tuple(vertices)
    self.color = tuple(color)

class faceSet(object):

  def __init__(self, backface="hide"):
    self.backface = backface
    self.faces = []

  def size(self):
    return len(self.faces)

  def append(self, face):
    self.faces.append(face)

  def jvx(self, f=None):
    if (f is None): f = sys.stdout
    print('<faceSet face="show" edge="hide" backface="%s" color="show">' % \
        self.backface, file=f)
    print('  <faces>', file=f)
    for face in self.faces:
      print('    <f>', end=' ', file=f)
      for v in face.vertices: print(v, end=' ', file=f)
      print('</f>', file=f)
    jvx_item_colors(f, "    ", self.faces)
    print('  </faces>', file=f)
    print('</faceSet>', file=f)

class geometry(object):

  def __init__(self, name, backface="hide"):
    self.name = name
    self.points = pointSet()
    self.lines = lineSet()
    self.faces = faceSet(backface=backface)

  def jvx(self, f=None):
    if (f is None): f = sys.stdout
    print('<geometry name="%s">' % self.name, file=f)
    if (self.points.size() > 0): self.points.jvx(f)
    if (self.lines.size() > 0): self.lines.jvx(f)
    if (self.faces.size() > 0): self.faces.jvx(f)
    print('</geometry>', file=f)

def bracketed_link(text, html, f=None):
  if (f is None): f = sys.stdout
  if (html is not None):
    print('[<a href="%s">' % html, end=' ', file=f)
  print('%s' % text, file=f)
  if (html is not None):
    print('</a>]', end=' ', file=f)
  print(file=f)

def html_loader(jvx_file_name,
                title="JavaView",
                header=None,
                sub_header=None,
                index_html=None,
                prev_html=None,
                next_html=None,
                alternative_label=None,
                alternative_html=None,
                legend=None,
                f=None,
                jars_url=None):
  if (f is None): f = sys.stdout
  from cctbx.web.asu_gallery import html_head_title
  print(html_head_title(title=title), file=f)
  print('''\
<body>
''', file=f)
  if (header is not None):
    print('<h2>%s</h2>' % header, file=f)
  if (sub_header is not None):
    print('%s' % sub_header, file=f)
    print('<p>', file=f)
  print('''\
<APPLET alt="JavaView applet"
        archive="%(jars_url)s/javaview.jar,%(jars_url)s/jvx.jar"
        name="javaview"
        code="javaview.class"
        width="400"
        height="400">
  <PARAM NAME="Model" VALUE="%(jvx_file_name)s">
</APPLET>
<p>
''' % vars(), file=f)
  if (index_html is not None):
    bracketed_link("Index", index_html, f=f)
  if (prev_html is not None or next_html is not None):
    bracketed_link("Previous", prev_html, f=f)
    bracketed_link("Next", next_html, f=f)
  if (alternative_html is not None):
    bracketed_link(alternative_label, alternative_html, f=f)
  if (legend is not None):
    print('<p>', file=f)
    for line in legend:
      print(line, file=f)
  print('<hr>', file=f)
  print('''\
This visualisation is using
<a href="http://www.javaview.de">JavaView</a>.

</body>
</html>''', file=f)

def run():
  from cctbx import sgtbx
  head()
  g = geometry("domino")
  p = g.points
  for i in range(-1,2):
    for j in range(-1,2):
      for k in range(-1,2):
        if ((i,j,k) != (0,0,0)):
          p.append(point((i,j,k)))
  point_group = sgtbx.space_group_info("P 2 3").group()
  f = g.faces
  for s in point_group:
    f.append(face((p.index(s*(-1,-1,-1)),
                   p.index(s*(-1,0,-1)),
                   p.index(s*(0,0,-1)),
                   p.index(s*(0,-1,-1))), (255,0,0)))
    f.append(face((p.index(s*(0,-1,-1)),
                   p.index(s*(0,0,-1)),
                   p.index(s*(1,0,-1)),
                   p.index(s*(1,-1,-1))), (0,0,255)))
  g.jvx()
  tail()

if (__name__ == "__main__"):
  run()
