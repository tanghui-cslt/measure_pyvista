import pyvista as pv

cube = pv.Cube()
def callback(point):
    """Create a cube and a label at the click point."""
    mesh = pv.Cube(center=point, x_length=0.05, y_length=0.05, z_length=0.05)
    pl.add_mesh(mesh, style='wireframe', color='b')
    pl.add_point_labels(point, [f"{point[0]:.2f}, {point[1]:.2f}, {point[2]:.2f}"])


pl = pv.Plotter()
pl.add_mesh(cube, show_edges=True)
pl.enable_surface_picking(callback=callback, left_clicking=True, show_point=False)
pl.show()