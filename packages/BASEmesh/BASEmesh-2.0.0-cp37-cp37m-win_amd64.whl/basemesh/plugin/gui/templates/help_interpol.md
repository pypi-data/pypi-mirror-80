## Interpolation utility

This tool interpolates the elevation of an existing mesh.

## Parameters

**Mesh layer to interpolate.** This is the mesh that will be interpolated to a new elevation. Any existing elevation information is ignored. The input layer will not be altered.

### Elevation source (basic mode)

In basic mode, only a single elevation source may be selected. This may either be an existing mesh layer (generally an elevation mesh), or a band of a raster layer.

### Elevation source (advanced mode)

In advanced mode, any valid elevation sources are added to the **Available elevation sources** list. Drag-and-drop any number of elevation sources into the **Selected elevation sources** list to include them in the interpolation.

Reorder the elevation sources as needed; the top elevation sources will take priority over the lower ones.

### Implementation details

Multi-source interpolation works hierarchically. When a given elevation source is queried for the elevation for a given point, it either returns a valid elevation (e.g. for points within the elevation mesh), or raises an error (e.g. for point outside the elevation mesh).

If an error is detected, the interpolator falls through to the next elevation source. If it too fails, it falls through again, etc. until either a valid elevation was returned or the list of elevation sources is exhausted.

### Output format

The interpolation is always performed on a regular 2D mesh (i.e. one with vertex elevation, as is used by BASEMENT 2.8).

Depending on the format specified, it is then converted to a BASEMENT 3 mesh (i.e. one using centoid elevation data) in a separate step.

You can use the **Output mesh format** drop-down to select the format(s) to save. If both formats are written, a "v2-8" or "v3" suffix is added accordingly.
