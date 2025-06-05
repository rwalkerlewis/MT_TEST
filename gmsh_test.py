import gmsh
import sys

# Initialize gmsh
gmsh.initialize()
gmsh.model.add("two_stacked_blocks")

# Geometry parameters
width = 10
height_block1 = 5
height_block2 = 3

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

# Top block (Block 2), sits above block 1
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

# Synchronize geometry before meshing
gmsh.model.geo.synchronize()

# Set mesh size (optional)
gmsh.model.mesh.setSize(gmsh.model.getEntities(0), 0.5)

# Generate 2D mesh
gmsh.model.mesh.generate(2)

# Write mesh to file
gmsh.write("two_blocks.msh")

# Launch GUI if desired
if '-nopopup' not in sys.argv:
    gmsh.fltk.run()

# Finalize
gmsh.finalize()

