## Elevation meshing utility

This tool triangulates the provided input geometries using the mesh generator 'Triangle'. The resulting mesh can be used as an elevation source for mesh interpolation.

> *Important: The resulting mesh will be generated without any mesh quality constraints applied and is not suitable for any kind of numeric simulation.*

## Parameters

### Triangulation constraints

These layers serve as the input constraints to the 'Triangle' mesh generator. They are required to contain 3D geometries as they are also used to interpolate the elevation data.

**Line segments.** A 3D line layer serving as the main constraint for triangulation. It is recommended to only use this layer whenever possible.

**Fixed points.** An auxiliary 3D point layer allowing for finer control of the interpolated elevation. Generally used to "pad out" the mesh in places where only following the break lines would result in artifacts.

### Mesh domain

This controls where the resulting mesh ends.

'Triangle' always generates the convex hull as part of its triangulation algorithm. It then carves away the outermost mesh elements to reach the desired shape.

This can be done in multiple ways:

* **Keep convex hull.** The convex hull generated is kept; no mesh elements are deleted. This is the default behaviour.

    Since the elevation mesh is only ever used for interpolation, the extra boundary triangles generally do not affect the resulting mesh.

    Use this option if your only elevation source are points.

* **Shrink to segments.** Any mesh element that is not enclosed by break lines is deleted.

    This allows for concave mesh domains, but may "eat" your entire mesh if your input line segments are not forming any closed polygons.

    > *Note: To get BASEmesh v1 behaviour, add your boundary polygon outline to the line segments layer and select this option.*

<!-- * **Use custom boundary.** Before triangulation, the input data is trimmed to the custom boundary polygon outline. This option is the most expensive in terms of computation. -->

### Settings

**Log level.** This controls how much of 'Triangle' output is forwarded to the log panel. Enabling any of the debug levels will cause significant overhead during triangulation and may dramatically increase processing time.

**Snapping tolerance.** Compensates for floating point errors and other issues with the input data. The default value, -6, translates to 1e-6 maximum snapping distance. Any vertices (i.e. points or line segment endpoints) closer than this will be considered coincident.

### Output

**Keep triangle files.** All of the triangulation is carried out in a temporary directory and is deleted immediately after conversion is complete. If this setting is enabled, they will instead be copied into the same directory as the output 2DM file.
