# BASEmesh

BASEmesh is a mesh generation and preprocessing toolkit for the numerical simulation package [BASEMENT](https://basement.ethz.ch/).

It serves as a standalone Python module, as well as a plugin for [QGIS](https://www.qgis.org/) version 3.10 and up. This document covers the QGIS Plugin use-case, see the [API documentation](docs/README.md) for information on the standalone Python interface.

> **Note:** It is recommended to use the latest version of QGIS with BASEmesh as there have been several useful additions to the 3D view since 3.10 LTR.

## Beta Release Info

BASEmesh 2 is still in development. No parts of its API should be considered final and may be subject to change.

For information on current progress and ETAs, check the repository [issues](https://git.ee.ethz.ch/basemesh/basemesh-v2/issues).

## Features

* Triangulation of 3D geometries into 2.5D meshes
* 2D quality mesh generation using Jonathan Shewchuk's [Triangle](https://www.cs.cmu.edu/~quake/triangle.html)
* Mesh interpolation from mesh or raster sources

## Installation

### Standalone Installation

Use the following command to install BASEmesh via pip:

**Windows**

```sh
C:\Users\<user>\Documents> python -m pip install --upgrade pip basemesh
```

**Linux**

```sh
user@device:~$ python3 -m pip install --upgrade pip basemesh
```

### Plugin Installation

1. Start QGIS
2. Load the QGIS plugin manager by choosing *Manage and Install Plugins…* in the *Plugins* category of the QGIS toolbar
3. Select *Settings* from the left panel
4. Click on *Add…* and provide a descriptive name, e.g. 'BASEmesh Plugin Repository'
5. Specify the repository address: <https://people.ee.ethz.ch/~basement/qgis_plugins/qgis_plugins.xml>
6. Press OK to confirm; a new entry has been added to the list of plugin repositories (make sure the *Status* reports as *connected* before continuing)
7. Select *All* from the left panel of the plugin manager and search for 'BASEmesh'
8. Choose the BASEmesh plugin (if several are available, choose the one with the highest version number) and press *Install Plugin*
9. Close the plugin manager. A new toolbar should have appeared and a *BASEmesh* entry added to the *Plugins* category of the QGIS toolbar

## Getting Started

The BASEmesh workflow consists of three steps:

1. Elevation mesh generation (optional if you have raster elevation data)
2. Quality mesh generation
3. Mesh interpolation

The following sections will cover the basics of how to use each tool. Note that this is purely a first introduction into the process and will skip a lot of the nuances regarding model setup and mesh generation. You can find additional information in the utilities' *'Help'* tab.

Visit the [repository Wiki](https://git.ee.ethz.ch/basemesh/basemesh-v2/-/wikis/home) for detailed guides and examples.

If you are a seasoned user of BASEmesh v1.4.5, check out the [Migration guide](https://git.ee.ethz.ch/basemesh/basemesh-v2/-/wikis/Migration-guide) for details on how to convert your existing projects for this version of BASEmesh.

### Elevation Mesh Generation

Elevation meshes are generated to represent the elevation geometry of your model. They provide an alternative to raster DEM data and allow the interpolation of a 2D quality mesh onto an elevated geometry.

#### 3D Input Geometry

To generate an elevation mesh, you require input geometry in the form of 3D vector layers. These will generally take the form of 3D polylines or points.

If your input geometry is not 3D, you can use the *'Convert Legacy Layer (…)'* algorithms in the QGIS Processing Toolbox to add elevation information via layer attributes.

#### Mesh Domain

By default, the elevation meshing utility will use the *'Keep convex hull'* mesh domain setting. This means that the outer edge of the generated mesh will equal the convex hull of your input data.

This allows the generation of a mesh from point data only, but it will also "eat" any concavities, which is generally not an issue when using a single elevation data source.

If you do require concavities, make sure you have a closed line string where you would like your mesh to end, then choose the *'Shrink to segments'* mesh domain setting. This will delete any geometries that are not contained within the outermost closed line string found. Note that this can "eat" your entire mesh if the outside line string is missing or has any gaps.

#### Snapping Tolerance

If you know your input data is not perfect (which is highly likely with real-world GIS data), you can use the *'Snapping Tolerance'* setting to define a fuzz range at which geometry will be snapped to each other. The value set in the GUI is the exponent; a value of `-2` means that any points within `0.01` units will be considered coincident.

### Quality Mesh Generation

The quality mesh defines the actual computational grid used for the simulation. It will always be flat, i.e. not contain any elevation information whatsoever.

#### 2D Input Geometry

Quality meshing is entirely two-dimensional, any elevation information in the input data will be discarded if provided.

Make sure that your break lines enclose the outside perimeter of your mesh.

#### Mesh Regions

Any segment-bounded region in the mesh can be assigned a Material ID and element size constraint. This is done via a region marker point layer with the appropriate fields:

| Field        | Description                                                                   | Type    |
|--------------|-------------------------------------------------------------------------------|---------|
| Hole marker  | Any region with a hole marker will be carved out of the resulting mesh        | Integer |
| Material ID  | Used to defines area-specific parameters such as friction or soil composition | Integer |
| Maximum area | The maximum area of any mesh element in this region                           | Real    |

#### String Definitions

String definitions are node strings used to keep track of specific cross sections in the mesh, either to serve as a boundary condition or as an output.

They are defined by named line string features in their own layer and will be automatically merged into the mesh break lines upon meshing.  After the meshing is complete, these line strings are then used to retrieve the mesh nodes that were generated along these break lines.

You can include string definitions in the generate 2DM file (this is the required format for BASEMENT 3) or write them to a separate text file (for BASEMENT 2.8). You can also check both options if you wish to compare results from both versions.

### Mesh Interpolation

The mesh interpolation utility takes an existing, flat quality mesh and drapes it over an elevation source.

This can either be a previously generated mesh layer, or a DEM raster layer and band.

#### Basic Mode

In this mode, only a single elevation source may be selected. If the quality mesh extends beyond the provided elevation source, meshing will fail.

#### Advanced Mode

This mode has two panels,  with the available elevation sources to the right and an empty list to the left.

You can select any number of elevation sources from the right panel and drag them into the left in any order. Only elevation sources in the left panel will be used for interpolation, with the higher-ranked sources taking priority.

For and point in the quality mesh that must be interpolated, the first elevation source is queried first. If it can produce a value, this value will be used right away, just as in Basic mode.

If an elevation source cannot produce a value, the elevation source below it will be queried instead, until one manages to produce a value, or the entire list is exhausted.

This allows for multi-source interpolation, e.g. an elevation mesh for the river itself, a fine-grid DEM for its immediate surroundings and a coarser DEM for floodplains further away.

#### Output Formats

BASEMENT 2.8 only uses node elevation data, whereas BASEMENT 3 only uses element face elevation for its simulation.

The *'Output mesh format'* drop down list may be used to select either or both elevation sources.

Note that due to the node and element elevation being independent, the *'BASEMENT 2 and 3 (node and element elevation)'* setting will have roughly twice the execution time as either setting on its own.

The mesh generated by the interpolation utility is now ready for use in BASEMENT, no additional exporting steps are necessary.
