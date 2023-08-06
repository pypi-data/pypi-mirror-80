#define PY_SSIZE_T_CLEAN
#include <Python.h>

// A component of the BASEmesh pre-processing toolkit.
// Copyright (C) 2020  ETH Zürich
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <https://www.gnu.org/licenses/>.

//////////////////////////////////////////////////////////////////////////////
// C implementations of the "basemesh.algorithms.algorithms_py" submodule.
// -----------------------------------------------------------------------
// The functions exported by this extension are identical to the ones defined
// in Python, but should provide a considerable performance boost on supported
// platforms.
//////////////////////////////////////////////////////////////////////////////

// INTERNAL FUNCTIONS
// ------------------
// These are the functions that do all of the heavy lifting. They get called
// through the wrapper functions and may expect clean and error-free inputs.

// Calculate the dot prodcuct of two 2D vectors.
//
//! @param v1x          x coord. of the first vector
//! @param v1y          y coord. ...
//! @param v2x          x coord. of the second vector
//! @param v2y          y coord. ...
//
double DotProduct_2d(
    double v1x, double v1y, // First vector
    double v2x, double v2y) // Second vector
{
    return v1x * v2x + v1y * v2y;
}

// Calculate the 2D distance between two 2D points.
//
//! @param p1x          x coord. of the first point
//! @param p1y          y coord. ...
//! @param p2x          x coord. of the second point
//! @param p2y          y coord. ...
//! @return             Euclidean distance between the two points
//
double Dist_2d(
    double p1x, double p1y, // First point
    double p2x, double p2y) // Second point
{
    return sqrt(pow(p1x - p2x, 2) + pow(p1y - p2y, 2));
}

// Return the signed half plane distance of the 2D point the 2D line
//
// Return the signed distance from the point to the line. The sign is used to
// show which side of the line the point is on.
//
// If the line is pointing up/forward, then a positive distance is returned if
// the point lies to the right of the line, and a negative distance if the
// point lies to the left of the line.
//
// If normalise is true, the real distance is returned. Otherwise the final
// distance normalisation step is skipped, which can be used to boost
// performance when performing convex hull containment checks.
//
//! @param l1x          x coord. of the first vertex
//! @param l1y          y coord. ...
//! @param l2x          x coord. of the second vertex
//! @param l2y          y coord ...
//! @param ptx          x coord of the point to check
//! @param lty          y coord ...
//! @param normalise    Whether to return the correct distance (see above)
//! @return             The signed half plane distance of the point and line
//
double SignedHalfPlaneDistance(
    double l1x, double l1y, // First line vertex
    double l2x, double l2y, // Second line vertex
    double ptx, double pty, // Coordinates of the check point
    int normalise)          // Whether to return the real distance
{
    double length;
    // Right-hand normal vector of the input line
    double nvec_x = l2y - l1y, nvec_y = -l2x + l1x;
    // Line-relative position of the check point
    double rel_x = ptx - l1x, rel_y = pty - l1y;

    // To normalise the returned distance, the normal vector has to be
    // converted to a unit vector
    if (normalise)
    {
        length = Dist_2d(0.0, 0.0, nvec_x, nvec_y);
        nvec_x = nvec_x / length;
        nvec_y = nvec_y / length;
    }

    // Project the point onto the normal vector. If the proejction is negative,
    // the point lies on the "inside" of the edge.
    return DotProduct_2d(nvec_x, nvec_y, rel_x, rel_y);
}

// Interpolate the elevation of a 2D point using a 3D triangle
//
// Return the elevation of the point (ptx, pty) when projected onto the plane
// defined by the three triangle vertices.
// This uses Barycentric coordinates. The given point may lie on or outside
// of the triangle. The triangle may not be degenerate.
//
//! @param ptx         x ccord. of the point to interpolate
//! @param pty         y coord. ...
//! @param t1x         x coord. of the first vertex
//! @param t1y         y coord. ...
//! @param t2z         z coord. ...
//! @param t2x         x coord. of the second vertex
//! @param t2y         y coord. ...
//! @param t1z         z coord. ...
//! @param t3x         x coord. of the third vertex
//! @param t3y         y coord. ...
//! @param t3z         z coord. ...
//! @return            interpolated height of the point (ptx, pty)
//
double GetTriangleElevation(
    double ptx, double pty,             // Coordinates of the input point
    double t1x, double t1y, double t1z, // First triangle vertex
    double t2x, double t2y, double t2z, // Second triangle vertex
    double t3x, double t3y, double t3z) // Third triangle vertex
{
    double denom;
    double weight1, weight2, weight3; // Barycentric weights

    // Calculate Barycentric weights for each vertex
    denom = (t2y - t3y) * (t1x - t3x) + (t3x - t2x) * (t1y - t3y);
    weight1 = ((t2y - t3y) * (ptx - t3x) + (t3x - t2x) * (pty - t3y)) / denom;
    weight2 = ((t3y - t1y) * (ptx - t3x) + (t1x - t3x) * (pty - t3y)) / denom;
    weight3 = 1.0 - weight1 - weight2;

    // The interpolated value is not equal to the sum of all weights and their
    // associated vertex' elevation.
    return weight1 * t1z + weight2 * t2z + weight3 * t3z;
}

// Return whether a point lies within a convex polygon.
//
// Points on the edge of the polygon do not get any special treatment, they
// are at the mercy of floating point precision.
// The given polygon must use counter-clockwise vertex order.
//
//! @param ptx          x coord. of the point to check
//! @param pty          y coord. ...
//! @param poly_x       array of x coordinates
//! @param poly_y       array of y coordinates
//! @param n            number of vertices
//! @return             1 if the point lies within the polygon, otherwise 0
//
int PointInPolygonConvex(
    double ptx, double pty, // Coordinates of the input point
    double vtcs_x[],        // Array of X coordinates
    double vtcs_y[],        // Array of Y coordinates
    Py_ssize_t num)         // Number of elements in the arrays
{
    double vtx_ax, vtx_ay; // The first vertex of the current edge
    double vtx_bx, vtx_by; // The second vertex of the current edge

    for (Py_ssize_t i = 0; i < num; i++)
    {
        // Get the edge vertices
        vtx_ax = vtcs_x[i];
        vtx_ay = vtcs_y[i];
        if (i + 1 < num)
        {
            vtx_bx = vtcs_x[i + 1];
            vtx_by = vtcs_y[i + 1];
        }
        else
        {
            // The last edge ends at index 0 again, to close the loop
            vtx_bx = vtcs_x[0];
            vtx_by = vtcs_y[0];
        }

        // If the input point lies on the right half plane of any edge, it
        // must lie outside the polygon
        if (SignedHalfPlaneDistance(vtx_ax, vtx_ay, vtx_bx, vtx_by,
                                    ptx, pty, 0) > 0.0)
        {
            return 0;
        }
    }
    // If the point has passed every half plane sign check, it must lie within
    // the polygon
    return 1;
}

// WRAPPER FUNCTIONS
// -----------------
// These are the functions that get called by Python. They are responsible for
// converting arguments, error-checking and other housekeeping.

static PyObject *
HalfPlaneDistance_Wrapper(PyObject *self, PyObject *args)
{
    double hpd;

    // Python arguments
    double l1x, l1y, l2x, l2y; // The line to check against
    double ptx, pty;           // The point to check
    int normalise = 1;         // Whether to return the corrected distance

    // Parse arguments
    if (!PyArg_ParseTuple(args, "((dd)(dd))(dd)|p", &l1x, &l1y, &l2x, &l2y,
                          &ptx, &pty, &normalise))
    {
        return NULL;
    }

    // Perform the calculation
    hpd = SignedHalfPlaneDistance(l1x, l1y, l2x, l2y, ptx, pty, normalise);

    // Return as Python float
    return PyFloat_FromDouble(hpd);
}

//! @param: asd
static PyObject *
InterpolateTriangle_Wrapper(PyObject *self, PyObject *args)
{
    double height;

    // Python arguments
    double ptx, pty;      // The point to interpolate
    double t1x, t1y, t1z; // The first vertex of the triangle
    double t2x, t2y, t2z; // The first vertex of the triangle
    double t3x, t3y, t3z; // The first vertex of the triangle

    // Parse arguments
    if (!PyArg_ParseTuple(args, "(dd)((ddd)(ddd)(ddd))", &ptx, &pty,
                          &t1x, &t1y, &t1z,
                          &t2x, &t2y, &t2z,
                          &t3x, &t3y, &t3z))
    {
        return NULL;
    }

    // Perform the interpolation
    height = GetTriangleElevation(ptx, pty, t1x, t1y, t1z,
                                  t2x, t2y, t2z, t3x, t3y, t3z);

    // Return as Python float
    return PyFloat_FromDouble(height);
}

static PyObject *
PointInPolygonConvex_Wrapper(PyObject *self, PyObject *args)
{
    int is_contained;
    double *vtcs_x;
    double *vtcs_y;
    Py_ssize_t num;
    PyObject *vertex;

    // Python arguments
    double ptx, pty;   // The point to check
    PyObject *polygon; // The polygon to check against

    // Parse arguments
    if (!PyArg_ParseTuple(args, "(dd)O", &ptx, &pty, &polygon))
    {
        return NULL;
    }

    // Ensure the given type is a polygon
    if (!PyTuple_Check(polygon))
    {
        PyErr_SetString(PyExc_TypeError,
                        "polygon is expected a tuple of tuples");
        return NULL;
    }

    // Ensure the polygon has at least three vertices
    num = PyTuple_Size(polygon);
    if (num < 3)
    {
        PyErr_SetString(PyExc_ValueError,
                        "A valid polygon must have at least three vertices");
        return NULL;
    }

    // Convert polygon tuple to array
    vtcs_x = (double *)malloc(num * sizeof(double));
    vtcs_y = (double *)malloc(num * sizeof(double));
    for (Py_ssize_t i = 0; i < num; i++)
    {
        // Retrieve the current vertex
        vertex = PyTuple_GetItem(polygon, i);

        // Ensure the vertex is a tuple of at least two elements
        if (!PyTuple_Check(vertex))
        {
            PyErr_SetString(PyExc_TypeError,
                            "polygon is expected a tuple of tuples");
            return NULL;
        }
        if (PyTuple_Size(vertex) != 2)
        {
            PyErr_SetString(PyExc_TypeError,
                            "polygon is not 2d");
            return NULL;
        }

        vtcs_x[i] = PyFloat_AsDouble(PyTuple_GetItem(vertex, 0));
        vtcs_y[i] = PyFloat_AsDouble(PyTuple_GetItem(vertex, 1));
    }

    // Perform containment check
    is_contained = PointInPolygonConvex(ptx, pty, vtcs_x, vtcs_y, num);

    // Free the arrays
    free(vtcs_x);
    free(vtcs_y);

    // Return as Python bool
    return PyLong_FromLong(is_contained);
}

// MODULE SETUP
// ------------
// The following items take care of the module setup, such as defining
// docstrings and hooking the Python names up to their wrapper functions.

PyDoc_STRVAR(
    HalfPlaneDistance_Doc,
    "Return the signed half plane distance for this point and line.\n"
    "\n"
    "The span of the vector defined by the given line bisects the 2D\n"
    "plane. If the given point lies on the span of the vector, `0.0`\n"
    "is returned.\n"
    "A positive distance means that the point lies to the right of an\n"
    "observer looking along the vector, a negative distance is returned\n"
    "for points to their left.\n"
    "\n"
    "By default, the returned distance is normalised, i.e. it equals the\n"
    "actual Euclidean distance between the two points. This behaviour\n"
    "can be disabled using the `normalise` kwarg, which will result in\n"
    "slightly improved performance.\n"
    "You can also manually calculate the Euclidean distance by dividing\n"
    "the return value by the length of the input line.\n"
    "\n"
    "Arguments:\n"
    "    line {Line2D} -- The vector splitting the plane\n"
    "    point {Point2D} -- The point to test\n"
    "\n"
    "Keyword arguments:\n"
    "    normalise {bool} -- Whether to normalize the return distance\n"
    "        {default: {True}}\n"
    "\n"
    "Returns:\n"
    "    float -- The signed distance from the span of the vecor\n");

PyDoc_STRVAR(
    InterpolateTriangle_Doc,
    "Interpolate a point using the given triangle.\n"
    "\n"
    "Interpolate the height at a given point using Barycentric\n"
    "coordinates.\n"
    "\n"
    "Arguments:\n"
    "    point {Point2D} -- Target point as a tuple of two floats\n"
    "    triangle {Triangle3D} -- Triangle to use for interpolation, a\n"
    "        tuple of three tuples of three floats each\n"
    "\n"
    "Returns:\n"
    "    float -- The interpolated height of the point\n");

PyDoc_STRVAR(
    PointInPolygonConvex_Doc,
    "Return whether the given point lies within the given polygon.\n"
    "\n"
    "Note that this algorithm does not check whether the given polygon\n"
    "is actually convex. It also does not check for self-intersections\n"
    "or whether the vertices are ordered in counter-clockwise order.\n"
    "\n"
    "Arguments:\n"
    "    point {Point2D} -- The point to check\n"
    "    polygon {Polygon2D} -- Any number of vertices forming a convex\n"
    "        polygon. At least three vertices are required.\n"
    "\n"
    "Raises:\n"
    "    ValueError: Raised if the given polygon tuple has fewer than\n"
    "        three vertices\n"
    "\n"
    "Returns:\n"
    "    bool -- Whether the point lies within the given polygon\n");

// Module symbol table
//
// This attaches the wrapper functions to their respective Python names and
// docstrings.
static PyMethodDef
    AlgorithmsCMethods[] = {
        // Python method name, C function, Argument parser, Python docstring
        {"half_plane_distance", HalfPlaneDistance_Wrapper,
         METH_VARARGS, HalfPlaneDistance_Doc},
        {"interpolate_triangle", InterpolateTriangle_Wrapper,
         METH_VARARGS, InterpolateTriangle_Doc},
        {"point_in_polygon_convex", PointInPolygonConvex_Wrapper,
         METH_VARARGS, PointInPolygonConvex_Doc},
        {NULL, NULL, 0, NULL} // Sentinel value
};

// Module definition
//
// This encapsulates the information needed by Python to create a new module.
static struct PyModuleDef
    AlgorithmsCModule = {
        PyModuleDef_HEAD_INIT,
        "algorithms_c",                                          // Name
        "Shared algorithms which could be reused or optimised.", // Docstring
        -1,
        AlgorithmsCMethods};

// Module initialiser
//
// This will be called by the Python executable when setting up the module.
PyMODINIT_FUNC
PyInit_algorithms_c(void)
{
    return PyModule_Create(&AlgorithmsCModule);
}