## Quality meshing utility

This tool generates a two-dimensional quality mesh from the provided input geometries using the mesh generator 'Triangle'.

It does enforce quality constraints, but the resulting mesh will have no elevation data whatsoever.

## Parameters

### Triangulation constraints

These settings control the global generation settings.

**Break lines.** A line layer containing line segments to be preserved during triangulation.

<!-- **Dividing constraints.** Dividing constraints enforce a certain number of segments along a break line. This is important for the use of inner boundaries where the upper and lower interface must share the same number of segments. -->

> *Beta release note: Dividing constriants are not yet available as there may be some changes to the way the elements are segmentized.*

**Constrained points.** Extra points to enforce during triangulation. This ensures that there will be a mesh node in the output for every constrained point.

**Minimum angle constraint.** Global constraint for the minimum inner angle of any mesh element generated. Be careful when increasing this value as it may dramatically increase mesh count while generating a large number of tiny triangles.

**Maximum area constraint.** Global constraint for the maximum are of a given mesh element. Maximum area constraints defined through mesh regions will overrule this value.

<!-- **Extra arguments.** Additional command line flags to pass to 'Triangle'. Expert option. -->

### Regions

Regions allow the application of custom constraints on a per-region basis.

**Region marker layer.** A point layer containing the region point definitions. The following region attributes can be applied:

* **Holes.** A whole number field flagging a given region as a hole. After triangulaton, any elements within the hole will be deleted from the mesh.

* **MATID.** A whole number field designating the material ID to assign elements generated within the given region.

* **Maximum area.** A decimal number field designating the maximum area constraint to use for elements generated within the region. These constraints will overrule the global constraint.

### Mesh domain

This controls where the resulting mesh ends.

'Triangle' always generates the convex hull as part of its triangulation algorithm. It then carves away the outermost mesh elements to reach the desired shape.

<!-- This can be done in multiple ways: -->
This can currently only be done one way:

<!-- * **Keep convex hull.** The convex hull generated is kept; no mesh elements are deleted. -->

* **Shrink to segments.** Any mesh element that is not enclosed by break lines is deleted. This is the default behaviour.

    This may "eat" your entire mesh if your input break lines are not forming any closed polygons.

    > *Note: To get BASEmesh v1 behaviour, add your boundary polygon outline to the break lines layer and select this option.*

<!-- * **Use custom boundary.** Before triangulation, the input data is trimmed to the custom boundary polygon outline. This option is the most expensive in terms of computation. -->

### String definitions

Used to specify named cross sections within the resulting mesh.

The lines defining the string definitions will implicitly be merged into the inut break lines. You do not have to include them in your break lines layer.

**String definitions layer.** The layer containing the string definition lines. It is advisable to use single-segment lines spanning the entire mesh as the nodes must be assigned their respective line strings after meshing (each subsegment requires its own point-on-line check needed).

**String definitions ID field.** The string field containing the unique name of a given string definition.

**Include in 2DM node strings.** The string definitions will be written to node strings in the output 2DM file. This option is required for use with BASEMENT 3.

**Write to sidecar file.** The string definitions will be written to a separate text file. This option is required for use with BASEMENT 2.8.

### Settings

**Log level.** This controls how much of 'Triangle' output is forwarded to the log panel. Enabling any of the debug levels will cause significant overhead during triangulation and may dramatically increase processing time.

**Snapping tolerance.** Compensates for floating point errors and other issues with the input data. The default value, -6, translates to 1e-6 maximum snapping distance. Any vertices (i.e. points or break line segment endpoints) closer than this will be considered coincident.

### Output

**Keep triangle files.** All of the triangulation is carried out in a temporary directory and is deleted immediately after conversion is complete. If this setting is enabled, they will instead be copied into the same directory as the output 2DM file.
