import time

import autogalaxy as ag

# Although we could test_autoarray the deflection angles without using an image (e.ag.mp. by just making a grid), we have chosen to
# set this test_autoarray up using an image and mask. This gives run-time numbers that can be easily related to an actual galaxy
# analysis

shape_2d = (301, 301)
pixel_scales = 0.05
sub_size = 4
radius = 4.0

print("sub grid size = " + str(sub_size))
print("circular mask radius = " + str(radius) + "\n")


mask = ag.Mask2D.circular(
    shape_2d=shape_2d, pixel_scales=pixel_scales, sub_size=sub_size, radius=radius
)

grid = ag.Grid.from_mask(mask=mask)

print("Number of points = " + str(grid.sub_shape_1d) + "\n")

### EllipticalIsothermal ###

mass_profile = ag.mp.EllipticalIsothermal(
    centre=(0.0, 0.0), elliptical_comps=(0.111111, 0.0), einstein_radius=1.0
)

image_plane_grid = ag.Grid.uniform(shape_2d=(500, 500), pixel_scales=0.02)

deflections = mass_profile.deflections_from_grid(grid=image_plane_grid)

deflections_y = ag.Array.manual_mask(
    array=deflections.in_1d[:, 0], mask=image_plane_grid.mask
)
deflections_x = ag.Array.manual_mask(
    array=deflections.in_1d[:, 1], mask=image_plane_grid.mask
)

input_deflections = ag.mp.InputDeflections(
    deflections_y=deflections_y,
    deflections_x=deflections_x,
    image_plane_grid=image_plane_grid,
    preload_grid=grid,
)

### Proifle ###

start = time.time()
input_deflections.deflections_from_grid(grid=grid)
diff = time.time() - start
print("InputDeflections time = {}".format(diff))
