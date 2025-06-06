
"""Generate a tri or quad mesh with two vertically stacked blocks using Gmsh and PyLith utilities.
"""

import gmsh
from gmsh_utils import (BoundaryGroup, MaterialGroup, GenerateMesh)

class App(GenerateMesh):
    """
    Application used to generate the mesh using Gmsh.

    Domain is 100km by 150km.
    -50.0 km <= x <= 50.0 km
    -75.0 km <= y <= 75.0 km

    Blocks are stacked vertically.
    """
    DOMAIN_X = 15000
    DOMAIN_Y = 15000

    DX_FAULT = 100
    DX_BIAS = 1.0001

    def __init__(self):
        """Constructor."""
        self.cell_choices = {
            "default": "quad",
            "choices": ["tri", "quad"],
        }
        self.filename = "mesh_quad.msh"

    def create_geometry(self):
        """Create geometry with two stacked blocks (one above the other)."""
        lx = self.DOMAIN_X
        ly = self.DOMAIN_Y
        x1 = -0.5 * lx
        y1 = -0.5 * ly
        ly_half = 0.5 * ly

        # Bottom block
        p1 = gmsh.model.geo.add_point(x1, y1, 0.0)
        p2 = gmsh.model.geo.add_point(x1 + lx, y1, 0.0)
        p3 = gmsh.model.geo.add_point(x1 + lx, y1 + ly_half, 0.0)
        p4 = gmsh.model.geo.add_point(x1, y1 + ly_half, 0.0)

        # Top block
        p5 = gmsh.model.geo.add_point(x1, y1 + ly_half, 0.0)  # same as p4
        p6 = gmsh.model.geo.add_point(x1 + lx, y1 + ly_half, 0.0)  # same as p3
        p7 = gmsh.model.geo.add_point(x1 + lx, y1 + ly, 0.0)
        p8 = gmsh.model.geo.add_point(x1, y1 + ly, 0.0)

        # Bottom block lines
        c1 = gmsh.model.geo.add_line(p1, p2)
        c2 = gmsh.model.geo.add_line(p2, p3)
        c3 = gmsh.model.geo.add_line(p3, p4)
        c4 = gmsh.model.geo.add_line(p4, p1)

        # Top block lines
        c5 = gmsh.model.geo.add_line(p5, p6)
        c6 = gmsh.model.geo.add_line(p6, p7)
        c7 = gmsh.model.geo.add_line(p7, p8)
        c8 = gmsh.model.geo.add_line(p8, p5)

        # Surface definitions
        cl1 = gmsh.model.geo.add_curve_loop([c1, c2, c3, c4])
        self.s_bottom = gmsh.model.geo.add_plane_surface([cl1])

        cl2 = gmsh.model.geo.add_curve_loop([c5, c6, c7, c8])
        self.s_top = gmsh.model.geo.add_plane_surface([cl2])

        # Store for marking
        self.c_bottom = [c1, c2, c3, c4]
        self.c_top = [c5, c6, c7, c8]
        self.c_fault = c5  # shared horizontal interface

        gmsh.model.geo.synchronize()

    def mark(self):
        """Mark geometry for materials, boundary conditions, faults, etc."""
        materials = (
            MaterialGroup(tag=1, entities=[self.s_bottom]),
            MaterialGroup(tag=2, entities=[self.s_top]),
        )
        for material in materials:
            material.create_physical_group()

        face_groups = (
            BoundaryGroup(name="boundary_yneg", tag=12, dim=1, entities=[self.c_bottom[0]]),
            BoundaryGroup(name="boundary_ypos", tag=13, dim=1, entities=[self.c_top[2]]),
            BoundaryGroup(name="boundary_xneg", tag=10, dim=1, entities=[self.c_bottom[3], self.c_top[3]]),
            BoundaryGroup(name="boundary_xpos", tag=11, dim=1, entities=[self.c_bottom[1], self.c_top[1]]),
            BoundaryGroup(name="fault", tag=20, dim=1, entities=[self.c_fault]),
        )
        for group in face_groups:
            group.create_physical_group()

    def generate_mesh(self, cell):
        """Generate the mesh with bias from the fault."""
        gmsh.option.set_number("Mesh.MeshSizeFromPoints", 0)
        gmsh.option.set_number("Mesh.MeshSizeFromCurvature", 0)
        gmsh.option.set_number("Mesh.MeshSizeExtendFromBoundary", 0)

        field_distance = gmsh.model.mesh.field.add("Distance")
        gmsh.model.mesh.field.setNumbers(field_distance, "CurvesList", [self.c_fault])

        field_size = gmsh.model.mesh.field.add("MathEval")
        math_exp = GenerateMesh.get_math_progression(field_distance, min_dx=self.DX_FAULT, bias=self.DX_BIAS)
        gmsh.model.mesh.field.setString(field_size, "F", math_exp)

        gmsh.model.mesh.field.setAsBackgroundMesh(field_size)

        if cell == "quad":
            gmsh.option.setNumber("Mesh.Algorithm", 8)
            gmsh.model.mesh.generate(2)
            gmsh.model.mesh.recombine()
        else:
            gmsh.model.mesh.generate(2)

        gmsh.model.mesh.optimize("Laplace2D")


if __name__ == "__main__":
    App().main()

