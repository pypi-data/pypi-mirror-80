from __future__ import absolute_import, division, print_function
from cctbx.web.asu_gallery import jvx
from cctbx.web.asu_gallery import jv_index
from cctbx.web.asu_gallery import guide_to_notation
from cctbx.web.asu_gallery import web_links
from cctbx.sgtbx.direct_space_asu import reference_table
from cctbx.sgtbx.direct_space_asu import facet_analysis
from cctbx import sgtbx
from scitbx import matrix
from libtbx.option_parser import OptionParser
from six.moves import urllib
import math
import os
from six.moves import range

def select_color(inclusive_flag):
  if (inclusive_flag): return (0,255,0)
  return (255,0,0)

class orthogonalizer(object):

  def __init__(self, unit_cell):
    self.unit_cell = unit_cell

  def __call__(self, vertex):
    return self.unit_cell.orthogonalize([float(x) for x in vertex])

def unit_cell_geometry(ortho, xy_plane_only=False):
  g = jvx.geometry("unit_cell")
  points_int = jvx.pointSet()
  points_cart = g.points
  points_cart.hide_points()
  for i in (0,1):
    for j in (0,1):
      for k in (0,1):
        if (xy_plane_only and k != 0): continue
        v = (i,j,k)
        points_int.append(v)
        points_cart.append(ortho(v))
  lines = g.lines
  for i in range(0,len(points_int.points)-1):
    for j in range(i+1,len(points_int.points)):
      v1 = points_int.points[i].vertex
      v2 = points_int.points[j].vertex
      n = 0
      for k in range(3):
        if (v1[k] != v2[k]): n += 1
      if (n == 1):
        lines.append(jvx.line((i,j)))
  return g

def basis_vector_geometry(ortho, min_fractional):
  g = jvx.geometry("basis_vectors")
  g.points.hide_points()
  g.lines = jvx.lineSet(thickness=3)
  for i in range(3):
    v = [float(x) - 0.15 for x in min_fractional]
    if (i == 0):
      g.points.append(ortho(v))
    v[i] += 0.25
    g.points.append(ortho(v))
  for i in range(3):
    color=[0,0,0]
    color[i] = 255
    g.lines.append(jvx.line(vertices=(0,i+1), color=color))
  return g

def cartesian_polygon(ortho, polygon):
  result = []
  for vertex in polygon:
    result.append(ortho(vertex[0]))
  return result

def get_diagonal_extend(ortho, all_vertices):
  min_coor = list(ortho((2,2,2)))
  max_coor = list(ortho((-2,-2,-2)))
  for vertex in all_vertices.keys():
    vertex_cart = ortho(vertex)
    for i in range(3):
      min_coor[i] = min(min_coor[i], vertex_cart[i])
      max_coor[i] = max(max_coor[i], vertex_cart[i])
  return abs(matrix.col(max_coor) - matrix.col(min_coor))

def get_min_fractional(all_vertices):
  result = [0,0,0]
  for vertex in all_vertices.keys():
    for i in range(3):
      result[i] = min(result[i], vertex[i])
  return result

def get_edge_vectors(vertices):
  col = matrix.col
  n = len(vertices)
  result = []
  for i in range(n):
    j = (i+1) % n
    result.append(col(vertices[j]) - col(vertices[i]))
  return result

def shrink_polygon(vertices, shrink_length):
  n = len(vertices)
  edge_vectors = get_edge_vectors(vertices)
  normal_vector = edge_vectors[0].cross(edge_vectors[1])
  result = []
  for i in range(n):
    j = (i-1) % n
    ei = edge_vectors[i]
    ej = edge_vectors[j]
    phi = math.acos(-ei.dot(ej) / math.sqrt(ei.norm_sq() * ej.norm_sq()))
    assert 0 < phi < math.pi
    f = shrink_length / math.tan(phi/2)
    shift_para = ei * (f / abs(ei))
    shift_perp = normal_vector.cross(ei)
    l = abs(shift_perp)
    assert l > 0
    shift_perp *= shrink_length / l
    vertex_inside = matrix.col(vertices[i]) + shift_para + shift_perp
    result.append(vertex_inside.elems)
  return result

def shrink_edge(cart_a, cart_b, shrink_length):
  a = matrix.col(cart_a)
  b = matrix.col(cart_b)
  d = (b-a) * (shrink_length / abs(b-a))
  return ((a+d).elems, (b-d).elems)

def edge_geometry(ortho, all_edge_segments, shrink_length, xy_plane_only=False):
  g = jvx.geometry("edges")
  g.points.hide_points()
  g.lines = jvx.lineSet(thickness=3)
  for edge_segments in all_edge_segments:
    for i_segment in range(len(edge_segments)-1):
      v1, v2 = [edge_segments[i_segment+_].vertex for _ in [0,1]]
      if (xy_plane_only and (v1[2] != 0 or v2[2] != 0)):
        continue
      i = g.points.size()
      g.points.extend(shrink_edge(ortho(v1), ortho(v2), shrink_length))
      g.lines.append(jvx.line(
        (i,i+1),
        color=select_color(edge_segments[i_segment].edge_inclusive_flag)))
  return g

def vertex_geometry(ortho, all_vertices, xy_plane_only=False):
  g = jvx.geometry("vertices")
  for vertex,inclusive_flag in all_vertices.items():
    if (xy_plane_only and vertex[2] != 0):
      continue
    g.points.append(jvx.point(
      ortho(vertex), color=select_color(inclusive_flag)))
  return g

def asu_as_jvx(group_type_number, asu, colored_grid_points=None,
               http_server_name=None,
               html_subdir="asu_gallery",
               jars_url="http://%s/jv395/jars",
               explore_symmetry_url=
                 "http://%s/cctbx/cctbx_web.cgi" \
                +"?target_module=explore_symmetry&amp;sgsymbol="):
  if (http_server_name is None):
    http_server_name = web_links.default_http_server_name
  xy_plane_only = (group_type_number < 0)
  space_group_info = sgtbx.space_group(asu.hall_symbol).info()
  if (not xy_plane_only):
    assert space_group_info.type().number() == group_type_number
  list_of_polygons = facet_analysis.asu_polygons(asu)
  all_edge_segments = facet_analysis.get_all_edge_segments(
    asu, list_of_polygons)
  all_vertices = facet_analysis.get_all_vertices(all_edge_segments)
  unit_cell = space_group_info.any_compatible_unit_cell(volume=100)
  ortho = orthogonalizer(unit_cell)
  shrink_length = get_diagonal_extend(ortho, all_vertices) * 0.02
  geometries = []
  if (colored_grid_points is None):
    for polygons in list_of_polygons:
      for polygon,inclusive_flag in polygons:
        def exclude():
          for vertex in polygon:
            if (vertex[0][2] != 0):
              return True
          return False
        if (xy_plane_only and exclude()):
          continue
        vertices_cart = cartesian_polygon(ortho, polygon)
        vertices_inside_cart = shrink_polygon(vertices_cart, shrink_length)
        points_int = jvx.pointSet()
        g = jvx.geometry("facet", backface=["hide", "show"][int(xy_plane_only)])
        points_cart = g.points
        points_cart.hide_points()
        i = -1
        for vertex in polygon:
          i += 1
          points_int.append(vertex[0])
          points_cart.append(vertices_inside_cart[i])
        faces = g.faces
        point_indices = []
        for vertex in polygon:
          point_indices.append(points_int.index(vertex[0]))
        faces.append(jvx.face(point_indices, select_color(inclusive_flag)))
        geometries.append(g)
    geometries.append(edge_geometry(
      ortho, all_edge_segments, shrink_length, xy_plane_only=xy_plane_only))
    geometries.append(vertex_geometry(
      ortho, all_vertices, xy_plane_only=xy_plane_only))
  else:
    g = jvx.geometry("grid")
    for frac in colored_grid_points:
      if (xy_plane_only and frac.site[2] != 0): continue
      g.points.append(jvx.point(ortho(frac.site), color=frac.color))
    geometries.append(g)
  if (colored_grid_points is None):
    grid_label = ""
    alternative_html_infix = "_grid"
    alternative_label = "Grid view"
  else:
    grid_label = "_grid"
    alternative_html_infix = ""
    alternative_label = "Polygon view"
  if (xy_plane_only): fmt = "asu_%02d%s"
  else:               fmt = "asu_%03d%s"
  base_file_name = fmt % (abs(group_type_number), grid_label)
  jvx_file_name = os.path.join(html_subdir, base_file_name+".jvx")
  jvx_in_html = base_file_name+".jvx"
  html_file_name = os.path.join(html_subdir, base_file_name+".html")
  prev_html = None
  next_html = None
  if (xy_plane_only):
    fmt = "asu_%02d%s.html"
    last_group_type_number = 17
  else:
    fmt = "asu_%03d%s.html"
    last_group_type_number = 230
  if (abs(group_type_number) > 1):
    prev_html = fmt % (abs(group_type_number)-1, grid_label)
  else:
    prev_html = fmt % (last_group_type_number, grid_label)
  if (abs(group_type_number) < last_group_type_number):
    next_html = fmt % (abs(group_type_number)+1, grid_label)
  else:
    next_html = fmt % (1, grid_label)
  alternative_html = fmt % (abs(group_type_number), alternative_html_infix)
  if (colored_grid_points is None or len(colored_grid_points) > 0):
    f = open(jvx_file_name, "w")
    jvx.head(f)
    unit_cell_geometry(ortho, xy_plane_only=xy_plane_only).jvx(f)
    basis_vector_geometry(ortho, get_min_fractional(all_vertices)).jvx(f)
    for g in geometries:
      g.jvx(f)
    jvx.tail(f)
    f.close()
  legend = []
  l = legend.append
  l("Surface area: green = inside the asymmetric unit, red = outside")
  l("<br>")
  l("Basis vectors: a = red, b = green, c = blue")
  l("<p>")
  shape_vertices = facet_analysis.shape_vertices(asu)
  l("<table border=2 cellpadding=8>")
  l("<tr valign=top>")
  l("<td>")
  remaining = []
  for vertex in shape_vertices:
    if (xy_plane_only and vertex[2] != 0): continue
    remaining.append(vertex)
  remaining.sort()
  l("<pre>Number of vertices: %d" % len(remaining))
  if (xy_plane_only):
    j = -4
  else:
    j = -1
  for vertex in remaining:
    l("  "+str(vertex)[1:j])
  l("</pre>")
  l("</td>")
  l("<td>")
  remaining = []
  for cut in asu.cuts:
    if (xy_plane_only and cut.as_xyz() in ["z>=0", "z<1"]): continue
    remaining.append(cut)
  l("<pre>Number of faces: %d" % len(remaining))
  for cut in remaining:
    l("  "+cut.as_xyz())
  l("</pre>")
  l('<a href="guide_to_notation.html">[Guide to notation]</a>')
  l("</td>")
  l("<td>")
  l("<pre>Geometric notation:")
  for cut in remaining:
    l("  "+str(cut))
  l("</pre>")
  l('<a href="http://scripts.iucr.org/cgi-bin/paper?pz5088" target="external">'
    '[Acta Cryst. article]</a>')
  l("</td>")
  l("</tr>")
  l("</table>")
  if (not xy_plane_only):
    title = "ASU " + str(space_group_info)
    header = 'Space group: <a href="%s">%s</a> (No. %d)' % (
      explore_symmetry_url % http_server_name
        + urllib.parse.quote_plus(str(space_group_info)),
      str(space_group_info),
      group_type_number)
    sub_header = None
  else:
    from cctbx.sgtbx import plane_groups
    pg_symbol = plane_groups.hermann_mauguin_hall_table[
      -group_type_number-1][0].replace("_", " ")
    title = "ASU " + pg_symbol
    header = 'Plane group: %s (No. %d)' % (pg_symbol, -group_type_number)
    sub_header = 'Corresponding space group: <a href="%s">%s</a> (No. %d)' % (
      explore_symmetry_url % http_server_name
        + urllib.parse.quote_plus(str(space_group_info)),
      str(space_group_info),
      space_group_info.type().number())
  f = open(html_file_name, "w")
  jvx.html_loader(
    jvx_in_html,
    title=title,
    header=header,
    sub_header=sub_header,
    index_html="index.html",
    prev_html=prev_html,
    next_html=next_html,
    alternative_label=alternative_label,
    alternative_html=alternative_html,
    legend=legend,
    jars_url=jars_url%http_server_name,
    f=f)
  f.close()

def run(http_server_name=None, html_subdir="asu_gallery"):
  parser = OptionParser(usage="usage: python jv_asu.py [options] [numbers...]")
  parser.add_option("-s", "--server",
    action="store",
    type="string",
    help="network name of http server",
    metavar="NAME")
  parser.add_option("-p", "--plane_group",
    action="store_true")
  options, args = parser.parse_args()
  if (options.server is not None):
    http_server_name = options.server
  if (not os.path.isdir(html_subdir)):
    os.makedirs(html_subdir)
  jv_index.write_html(open("%s/index.html" % html_subdir, "w"))
  guide_to_notation.write_html(
    open("%s/guide_to_notation.html" % html_subdir, "w"))
  if (len(args) == 0):
    if (options.plane_group):
      args = ["1-17"]
    else:
      args = ["1-230"]
  for arg in args:
    numbers = [int(n) for n in arg.split('-')]
    assert len(numbers) in (1,2)
    if (len(numbers) == 1): numbers *= 2
    for group_type_number in range(numbers[0], numbers[1]+1):
      if (options.plane_group):
        print("Plane group number:", group_type_number)
        from cctbx.sgtbx.direct_space_asu import plane_group_reference_table
        asu = plane_group_reference_table.get_asu(group_type_number)
        group_type_number *= -1
      else:
        print("Space group number:", group_type_number)
        asu = reference_table.get_asu(group_type_number)
      for colored_grid_points in [None, []]:
        asu_as_jvx(
          group_type_number=group_type_number,
          asu=asu,
          colored_grid_points=colored_grid_points,
          http_server_name=http_server_name,
          html_subdir=html_subdir)

if (__name__ == "__main__"):
  run()
