import gmsh
import sys

gmsh.initialize()
gmsh.model.add("two_stacked_blocks_quads")

# Geometry parameters
width = 10000
height_block1 = 9000
height_block2 = 1000
nx, ny1, ny2 = 100, 90, 10  # Mesh divisions (x, y for each block)

# Bottom block (Block 1)
p1 = gmsh.model.geo.addPoint(0, 0, 0)
p2 = gmsh.model.geo.addPoint(width, 0, 0)
p3 = gmsh.model.geo.addPoint(width, height_block1, 0)
p4 = gmsh.model.geo.addPoint(0, height_block1, 0)

l1 = gmsh.model.geo.addLine(p1, p2)
l2 = gmsh.model.geo.addLine(p2, p3)
l3 = gmsh.model.geo.addLine(p3, p4)
l4 = gmsh.model.geo.addLine(p4, p1)

loop1 = gmsh.model.geo.addCurveLoop([l1, l2, l3, l4])
surface1 = gmsh.model.geo.addPlaneSurface([loop1])

# Top block (Block 2)
p5 = gmsh.model.geo.addPoint(0, height_block1, 0)
p6 = gmsh.model.geo.addPoint(width, height_block1, 0)
p7 = gmsh.model.geo.addPoint(width, height_block1 + height_block2, 0)
p8 = gmsh.model.geo.addPoint(0, height_block1 + height_block2, 0)

l5 = gmsh.model.geo.addLine(p5, p6)
l6 = gmsh.model.geo.addLine(p6, p7)
l7 = gmsh.model.geo.addLine(p7, p8)
l8 = gmsh.model.geo.addLine(p8, p5)

loop2 = gmsh.model.geo.addCurveLoop([l5, l6, l7, l8])
surface2 = gmsh.model.geo.addPlaneSurface([loop2])

# Transfinite lines
for line in [l1, l5]:
    gmsh.model.geo.mesh.setTransfiniteCurve(line, nx + 1)
for line in [l3, l7]:
    gmsh.model.geo.mesh.setTransfiniteCurve(line, nx + 1)

gmsh.model.geo.mesh.setTransfiniteCurve(l2, ny1 + 1)
gmsh.model.geo.mesh.setTransfiniteCurve(l4, ny1 + 1)

gmsh.model.geo.mesh.setTransfiniteCurve(l6, ny2 + 1)
gmsh.model.geo.mesh.setTransfiniteCurve(l8, ny2 + 1)

# Transfinite surface and recombination for quads
gmsh.model.geo.mesh.setTransfiniteSurface(surface1)
gmsh.model.geo.mesh.setTransfiniteSurface(surface2)

gmsh.model.geo.mesh.setRecombine(2, surface1)
gmsh.model.geo.mesh.setRecombine(2, surface2)

gmsh.model.geo.synchronize()

# Physical groups (optional)
gmsh.model.addPhysicalGroup(2, [surface1], name="Block1")
gmsh.model.addPhysicalGroup(2, [surface2], name="Block2")

# Generate mesh
gmsh.model.mesh.generate(2)
gmsh.write("two_blocks_quads.msh")

# View in GUI
if "-nopopup" not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()

