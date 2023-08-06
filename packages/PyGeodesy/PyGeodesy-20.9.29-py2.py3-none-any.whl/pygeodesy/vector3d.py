
# -*- coding: utf-8 -*-

u'''Generic 3-D vector base class L{Vector3d} and function L{sumOf}.

Pure Python implementation of vector-based functions by I{(C) Chris
Veness 2011-2015} published under the same MIT Licence**, see
U{Vector-based geodesy
<https://www.Movable-Type.co.UK/scripts/latlong-vectors.html>}.

@newfield example: Example, Examples
'''

from pygeodesy.basics import isscalar, joined_, len2, map1, property_doc_, \
                             property_RO, _xnumpy, _xkwds
from pygeodesy.errors import _AssertionError, CrossError, IntersectionError, \
                             _IsnotError, _TypeError, _ValueError
from pygeodesy.fmath import fdot, fsum, fsum_, hypot_, hypot2_
from pygeodesy.formy import n_xyz2latlon, n_xyz2philam, _radical2
from pygeodesy.interns import EPS, EPS1, NN, PI, PI2, _coincident_, _colinear_, \
                             _COMMA_, _COMMA_SPACE_, _datum_, _h_, _height_, \
                             _invalid_, _Missing, _name_, _near_concentric_, \
                             _no_intersection_, _PARENTH_, _point_, _scalar_, \
                             _too_distant_fmt_, _y_, _z_, _1_, _2_, _3_, \
                             _0_0, _0_5, _1_0
from pygeodesy.lazily import _ALL_DOCS, _ALL_LAZY
from pygeodesy.named import modulename, _NamedBase, _xnamed, _xother3, _xotherError
from pygeodesy.namedTuples import Vector3Tuple
from pygeodesy.streprs import strs
from pygeodesy.units import Radius, Radius_

from math import atan2, copysign, cos, sin, sqrt

__all__ = _ALL_LAZY.vector3d
__version__ = '20.09.28'


def _xyzn4(xyz, y, z, Error=_TypeError):  # imported by .ecef
    '''(INTERNAL) Get an C{(x, y, z, name)} 4-tuple.
    '''
    try:
        t = xyz.x, xyz.y, xyz.z
    except AttributeError:
        t = xyz, y, z
    try:
        x, y, z = map1(float, *t)
    except (TypeError, ValueError) as x:
        d = dict(zip(('xyz', _y_, _z_), t))
        raise Error(txt=str(x), **d)

    return x, y, z, getattr(xyz, _name_, NN)


def _xyzhdn6(xyz, y, z, height, datum, ll, Error=_TypeError):  # by .cartesianBase, .nvectorBase
    '''(INTERNAL) Get an C{(x, y, z, h, d, name)} 6-tuple.
    '''
    x, y, z, n = _xyzn4(xyz, y, z, Error=Error)

    h = height or getattr(xyz, _height_, None) \
               or getattr(xyz, _h_, None) \
               or getattr(ll,  _height_, None)

    d = datum or getattr(xyz, _datum_, None) \
              or getattr(ll,  _datum_, None)

    return x, y, z, h, d, n


class VectorError(_ValueError):
    '''L{Vector3d} or C{*Nvector} issue.
    '''
    pass


class Vector3d(_NamedBase):  # XXX or _NamedTuple or Vector3Tuple?
    '''Generic 3-D vector manipulation.

       In a geodesy context, these may be used to represent:
        - n-vector representing a normal to point on earth's surface
        - earth-centered, earth-fixed vector (= n-vector for spherical model)
        - great circle normal to vector
        - motion vector on earth's surface
        - etc.
    '''
    _crosserrors = True  # un/set by .errors.crosserrors

    _fromll = None  # original latlon
    _length = None  # cached length
    _numpy  = None  # module numpy iff imported by trilaterate3d2 below
    _united = None  # cached norm, unit (L{Vector3d})
    _xyz    = None  # cached xyz (L{Vector3Tuple})

    _x = 0  # X component
    _y = 0  # Y component
    _z = 0  # Z component

    def __init__(self, x, y, z, ll=None, name=NN):
        '''New 3-D L{Vector3d}.

           The vector may be normalised or use x/y/z values
           for height relative to the surface of the sphere
           or ellipsoid, distance from earth centre, etc.

           @arg x: X component of vector (C{scalar}).
           @arg y: Y component of vector (C{scalar}).
           @arg z: Z component of vector (C{scalar}).
           @kwarg ll: Optional latlon reference (C{LatLon}).
           @kwarg name: Optional name (C{str}).
        '''
        self._x = x
        self._y = y
        self._z = z
        if ll:
            self._fromll = ll
        if name:
            self.name = name

    def __add__(self, other):
        '''Add this to an other vector (L{Vector3d}).

           @return: Vectorial sum (L{Vector3d}).

           @raise TypeError: Incompatible B{C{other}} C{type}.
        '''
        return self.plus(other)
#   __iadd__ = __add__
    __radd__ = __add__

    def __abs__(self):
        '''Return the norm of this vector.

           @return: Norm, unit length (C{float});
        '''
        return self.length

    def __cmp__(self, other):  # Python 2-
        '''Compare this and an other vector

           @arg other: The other vector (L{Vector3d}).

           @return: -1, 0 or +1 (C{int}).

           @raise TypeError: Incompatible B{C{other}} C{type}.
        '''
        self.others(other)
        return -1 if self.length < other.length else (
               +1 if self.length > other.length else 0)

    cmp = __cmp__

    def __div__(self, scalar):
        '''Divide this vector by a scalar.

           @arg scalar: The divisor (C{scalar}).

           @return: Quotient (L{Vector3d}).

           @raise TypeError: Non-scalar B{C{scalar}}.
        '''
        return self.dividedBy(scalar)
#   __itruediv__ = __div__
    __truediv__ = __div__

    def __eq__(self, other):
        '''Is this vector equal to an other vector?

           @arg other: The other vector (L{Vector3d}).

           @return: C{True} if equal, C{False} otherwise.

           @raise TypeError: Incompatible B{C{other}} C{type}.
        '''
        self.others(other)
        return self.isequalTo(other)

    def __ge__(self, other):
        '''Is this vector longer than or equal to an other vector?

           @arg other: The other vector (L{Vector3d}).

           @return: C{True} if so, C{False} otherwise.

           @raise TypeError: Incompatible B{C{other}} C{type}.
        '''
        self.others(other)
        return self.length >= other.length

    def __gt__(self, other):
        '''Is this vector longer than an other vector?

           @arg other: The other vector (L{Vector3d}).

           @return: C{True} if so, C{False} otherwise.

           @raise TypeError: Incompatible B{C{other}} C{type}.
        '''
        self.others(other)
        return self.length > other.length

    def __le__(self, other):  # Python 3+
        '''Is this vector shorter than or equal to an other vector?

           @arg other: The other vector (L{Vector3d}).

           @return: C{True} if so, C{False} otherwise.

           @raise TypeError: Incompatible B{C{other}} C{type}.
        '''
        self.others(other)
        return self.length <= other.length

    def __lt__(self, other):  # Python 3+
        '''Is this vector shorter than an other vector?

           @arg other: The other vector (L{Vector3d}).

           @return: C{True} if so, C{False} otherwise.

           @raise TypeError: Incompatible B{C{other}} C{type}.
        '''
        self.others(other)
        return self.length < other.length

    # Luciano Ramalho, "Fluent Python", page 397, O'Reilly 2016
    def __matmul__(self, other):  # PYCHOK Python 3.5+ ... c = a @ b
        '''Compute the cross product of this and an other vector.

           @arg other: The other vector (L{Vector3d}).

           @return: Cross product (L{Vector3d}).

           @raise TypeError: Incompatible B{C{other}} C{type}.
        '''
        return self.cross(other)
#   __imatmul__ = __matmul__

    def __mul__(self, scalar):
        '''Multiply this vector by a scalar

           @arg scalar: Factor (C{scalar}).

           @return: Product (L{Vector3d}).
        '''
        return self.times(scalar)
#   __imul__ = __mul__
#   __rmul__ = __mul__

    def __ne__(self, other):
        '''Is this vector not equal to an other vector?

           @arg other: The other vector (L{Vector3d}).

           @return: C{True} if so, C{False} otherwise.

           @raise TypeError: Incompatible B{C{other}} C{type}.
        '''
        self.others(other)
        return not self.isequalTo(other)

    def __neg__(self):
        '''Negate this vector.

           @return: Negative (L{Vector3d})
        '''
        return self.negate()

    def __pos__(self):
        '''Copy this vector.

           @return: Positive (L{Vector3d})
        '''
        return self.copy()

    # Luciano Ramalho, "Fluent Python", page 397, O'Reilly 2016
    def __rmatmul__(self, other):  # PYCHOK Python 3.5+ ... c = a @ b
        '''Compute the cross product of an other and this vector.

           @arg other: The other vector (L{Vector3d}).

           @return: Cross product (L{Vector3d}).

           @raise TypeError: Incompatible B{C{other}} C{type}.
        '''
        self.others(other)
        return other.cross(self)

    def __rsub__(self, other):
        '''Subtract this vector from an other vector.

           @arg other: The other vector (L{Vector3d}).

           @return: Difference (L{Vector3d}).

           @raise TypeError: Incompatible B{C{other}} C{type}.
        '''
        self.others(other)
        return other.minus(self)

    def __sub__(self, other):
        '''Subtract an other vector from this vector.

           @arg other: The other vector (L{Vector3d}).

           @return: Difference (L{Vector3d}).

           @raise TypeError: Incompatible B{C{other}} C{type}.
        '''
        return self.minus(other)
#   __isub__ = __sub__

    def _update(self, updated, *attrs):
        '''(INTERNAL) Zap cached attributes if updated.
        '''
        if updated:
            _NamedBase._update(self, updated, '_length',  # '_fromll'
                                   '_united', '_xyz', *attrs)

    def angleTo(self, other, vSign=None, wrap=False):
        '''Compute the angle between this and an other vector.

           @arg other: The other vector (L{Vector3d}).
           @kwarg vSign: Optional vector, if supplied (and out of the
                         plane of this and the other), angle is signed
                         positive if this->other is clockwise looking
                         along vSign or negative in opposite direction,
                         otherwise angle is unsigned.
           @kwarg warp: Wrap/unroll the angle to +/-PI (c{bool}).

           @return: Angle (C{radians}).

           @raise TypeError: If B{C{other}} or B{C{vSign}} not a L{Vector3d}.
        '''
        x = self.cross(other)
        s = x.length
        if s < EPS:
            return _0_0
        # use vSign as reference to get sign of s
        if vSign and x.dot(vSign) < 0:
            s = -s

        a = atan2(s, self.dot(other))
        if wrap and abs(a) > PI:
            a -= copysign(PI2, a)
        return a

    def cross(self, other, raiser=None):
        '''Compute the cross product of this and an other vector.

           @arg other: The other vector (L{Vector3d}).
           @kwarg raiser: Optional, L{CrossError} label if raised (C{str}).

           @return: Cross product (L{Vector3d}).

           @raise CrossError: Zero or near-zero cross product and both
                              B{C{raiser}} and L{crosserrors} set.

           @raise TypeError: Incompatible B{C{other}} C{type}.
        '''
        self.others(other)

        x = self.y * other.z - self.z * other.y
        y = self.z * other.x - self.x * other.z
        z = self.x * other.y - self.y * other.x

        if raiser and self.crosserrors and max(map1(abs, x, y, z)) < EPS:
            t = _coincident_ if self.isequalTo(other) else _colinear_
            r = getattr(other, '_fromll', None) or other
            raise CrossError(raiser, r, txt=t)

        return self.classof(x, y, z)

    @property_doc_('''raise or ignore L{CrossError} exceptions (C{bool}).''')
    def crosserrors(self):
        '''Get L{CrossError} exceptions (C{bool}).
        '''
        return self._crosserrors

    @crosserrors.setter  # PYCHOK setter!
    def crosserrors(self, raiser):
        '''Raise L{CrossError} exceptions (C{bool}).
        '''
        self._crosserrors = bool(raiser)

    def dividedBy(self, factor):
        '''Divide this vector by a scalar.

           @arg factor: The divisor (C{scalar}).

           @return: New, scaled vector (L{Vector3d}).

           @raise TypeError: Non-scalar B{C{factor}}.

           @raise VectorError: Invalid or zero B{C{factor}}.
        '''
        if not isscalar(factor):
            raise _IsnotError(_scalar_, factor=factor)
        try:
            return self.times(_1_0 / factor)
        except (ValueError, ZeroDivisionError) as x:
            raise VectorError(factor=factor, txt=str(x))

    def dot(self, other):
        '''Compute the dot (scalar) product of this and an other vector.

           @arg other: The other vector (L{Vector3d}).

           @return: Dot product (C{float}).

           @raise TypeError: Incompatible B{C{other}} C{type}.
        '''
        self.others(other)

        return fdot(self.xyz, *other.xyz)

    def equals(self, other, units=False):  # PYCHOK no cover
        '''DEPRECATED, use method C{isequalTo}.
        '''
        return self.isequalTo(other, units=units)

    def isequalTo(self, other, units=False, eps=EPS):
        '''Check if this and an other vector are equal or equivalent.

           @arg other: The other vector (L{Vector3d}).
           @kwarg units: Optionally, compare the normalized, unit
                         version of both vectors.
           @kwarg eps: Tolerance for equality (C{scalar}).

           @return: C{True} if vectors are identical, C{False} otherwise.

           @raise TypeError: Incompatible B{C{other}} C{type}.

           @example:

           >>> v1 = Vector3d(52.205, 0.119)
           >>> v2 = Vector3d(52.205, 0.119)
           >>> e = v1.isequalTo(v2)  # True
        '''
        self.others(other)

        if units:
            d = self.unit().minus(other.unit())
        else:
            d = self.minus(other)
        return max(map(abs, d.xyz)) < eps

    @property_RO
    def length(self):
        '''Get the length (norm, magnitude) of this vector (C{float}).
        '''
        if self._length is None:
            self._length = hypot_(self.x, self.y, self.z)
        return self._length

    @property_RO
    def length2(self):
        '''Get the length I{squared} of this vector (C{float}).
        '''
        return hypot2_(self.x, self.y, self.z)

    def minus(self, other):
        '''Subtract an other vector from this vector.

           @arg other: The other vector (L{Vector3d}).

           @return: New vector difference (L{Vector3d}).

           @raise TypeError: Incompatible B{C{other}} C{type}.
        '''
        self.others(other)

        return self.classof(self.x - other.x,
                            self.y - other.y,
                            self.z - other.z)

    def nearestOn(self, other1, other2, within=True):
        '''Locate the point between two points closest to this point.

           @arg other1: Start point (L{Vector3d}).
           @arg other2: End point (L{Vector3d}).
           @kwarg within: If C{True} return the closest point between
                          the given points, otherwise the closest
                          point on the extended line through both
                          points (C{bool}).

           @return: Closest point (L{Vector3d}).

           @raise TypeError: If B{C{other1}} or B{C{other2}} is not L{Vector3d}.

           @see: Method L{sphericalTrigonometry.LatLon.nearestOn3} and
                 U{3-D Point-Line distance<https://MathWorld.Wolfram.com/
                 Point-LineDistance3-Dimensional.html>}.
        '''
        return _nearestOn(self, self.others(other1=other1),
                                self.others(other2=other2), within=within)

    def negate(self):
        '''Return this vector in opposite direction.

           @return: New, opposite vector (L{Vector3d}).
        '''
        return self.classof(-self.x, -self.y, -self.z)

    @property_RO
    def _N_vector(self):
        '''(INTERNAL) Get the (C{nvectorBase._N_vector_})
        '''
        from pygeodesy.nvectorBase import _N_vector_
        return _N_vector_(*(self._xyz or self.xyz))

    def others(self, *other, **name_other_up):
        '''Refined class comparison.

           @arg other: The other vector (L{Vector3d}).
           @kwarg name_other_up: Overriding C{name=other} and C{up=1}
                                 keyword arguments.

           @return: The B{C{other}} if compatible.

           @raise TypeError: Incompatible B{C{other}} C{type}.
        '''
        other, name, up = _xother3(self, other, **name_other_up)
        if not isinstance(other, Vector3d):
            _NamedBase.others(self, other, name=name, up=up + 1)
        return other

    def parse(self, str3d, sep=_COMMA_, name=NN):
        '''Parse an C{"x, y, z"} string to a similar L{Vector3d} instance.

           @arg str3d: X, y and z string (C{str}), see function L{parse3d}.
           @kwarg sep: Optional separator (C{str}).
           @kwarg name: Optional instance name (C{str}), overriding this name.

           @return: The similar instance (L{Vector3d}).

           @raise VectorError: Invalid B{C{str3d}}.
        '''
        return parse3d(str3d, sep=sep, Vector=self.classof,
                              name=name or self.name)

    def plus(self, other):
        '''Add this vector and an other vector.

           @arg other: The other vector (L{Vector3d}).

           @return: Vectorial sum (L{Vector3d}).

           @raise TypeError: Incompatible B{C{other}} C{type}.
        '''
        self.others(other)

        return self.classof(self.x + other.x,
                            self.y + other.y,
                            self.z + other.z)

    sum = plus  # alternate name

    def rotate(self, axis, theta):
        '''Rotate this vector around an axis by a specified angle.

           See U{Rotation matrix from axis and angle
           <https://WikiPedia.org/wiki/Rotation_matrix#Rotation_matrix_from_axis_and_angle>}
           and U{Quaternion-derived rotation matrix
           <https://WikiPedia.org/wiki/Quaternions_and_spatial_rotation#Quaternion-derived_rotation_matrix>}.

           @arg axis: The axis being rotated around (L{Vector3d}).
           @arg theta: The angle of rotation (C{radians}).

           @return: New, rotated vector (L{Vector3d}).

           @JSname: I{rotateAround}.
        '''
        a = self.others(axis=axis).unit()  # axis being rotated around

        c = cos(theta)
        b = a.times(1 - c)
        s = a.times(sin(theta))

        p = self.unit().xyz  # point being rotated

        # multiply p by a quaternion-derived rotation matrix
        return self.classof(fdot(p, a.x * b.x + c,   a.x * b.y - s.z, a.x * b.z + s.y),
                            fdot(p, a.y * b.x + s.z, a.y * b.y + c,   a.y * b.z - s.x),
                            fdot(p, a.z * b.x - s.y, a.z * b.y + s.x, a.z * b.z + c))

    def rotateAround(self, axis, theta):  # PYCHOK no cover
        '''DEPRECATED, use method C{rotate}.
        '''
        return self.rotate(axis, theta)

    def times(self, factor):
        '''Multiply this vector by a scalar.

           @arg factor: Scale factor (C{scalar}).

           @return: New, scaled vector (L{Vector3d}).

           @raise TypeError: Non-scalar B{C{factor}}.
        '''
        if not isscalar(factor):
            raise _IsnotError(_scalar_, factor=factor)
        return self.classof(self.x * factor,
                            self.y * factor,
                            self.z * factor)

    def to2ab(self):  # PYCHOK no cover
        '''DEPRECATED, use property C{Nvector.philam}.

           @return: A L{PhiLam2Tuple}C{(phi, lam)}.
        '''
        return n_xyz2philam(self.x, self.y, self.z)

    def to2ll(self):  # PYCHOK no cover
        '''DEPRECATED, use property C{Nvector.latlon}.

           @return: A L{LatLon2Tuple}C{(lat, lon)}.
        '''
        return n_xyz2latlon(self.x, self.y, self.z)

    def to3xyz(self):  # PYCHOK no cover
        '''DEPRECATED, use property C{xyz}.

           @return: A L{Vector3Tuple}C{(x, y, z)}.
        '''
        return self.xyz

    def toStr(self, prec=5, fmt=_PARENTH_, sep=_COMMA_SPACE_):  # PYCHOK expected
        '''Return a string representation of this vector.

           @kwarg prec: Optional number of decimal places (C{int}).
           @kwarg fmt: Optional, enclosing format to use (C{str}).
           @kwarg sep: Optional separator between components (C{str}).

           @return: Vector as "(x, y, z)" (C{str}).
        '''
        t = sep.join(strs(self.xyz, prec=prec))
        if fmt:
            t = fmt % (t,)
        return t

    def unit(self, ll=None):
        '''Normalize this vector to unit length.

           @kwarg ll: Optional, original location (C{LatLon}).

           @return: Normalized vector (L{Vector3d}).
        '''
        if self._united is None:
            n = self.length
            if n > EPS and abs(n - 1) > EPS:
                u = self._xnamed(self.dividedBy(n))
                u._length = 1
            else:
                u = self.copy()
            u._fromll = ll or self._fromll
            self._united = u._united = u
        return self._united

    @property_RO
    def x(self):
        '''Get the X component (C{float}).
        '''
        return self._x

    @property_RO
    def xyz(self):
        '''Get the X, Y and Z components (L{Vector3Tuple}C{(x, y, z)}).
        '''
        if self._xyz is None:
            self._xyz = Vector3Tuple(self.x, self.y, self.z)
        return self._xnamed(self._xyz)

    @property_RO
    def y(self):
        '''Get the Y component (C{float}).
        '''
        return self._y

    @property_RO
    def z(self):
        '''Get the Z component (C{float}).
        '''
        return self._z


def intersections2(center1, radius1, center2, radius2, sphere=True,  # MCCABE 14
                                                       Vector=None, **Vector_kwds):
    '''Compute the intersection of two spheres or circles, each defined
       by a center point and a radius.

       @arg center1: Center of the first sphere or circle (L{Vector3d},
                     C{Vector3Tuple} or C{Vector4Tuple}).
       @arg radius1: Radius of the first sphere or circle (same units as
                     the B{C{center1}} coordinates).
       @arg center2: Center of the second sphere or circle (L{Vector3d},
                     C{Vector3Tuple} or C{Vector4Tuple}).
       @arg radius2: Radius of the second sphere or circle (same units as
                     the B{C{center1}} and B{C{center2}} coordinates).
       @kwarg sphere: If C{True} compute the center and radius of the
                      intersection of two spheres.  If C{False}, ignore the
                      C{z}-component and compute the intersection of two
                      circles (C{bool}).
       @kwarg Vector: Class to return intersections (L{Vector3d} or
                      C{Vector3Tuple}) or C{None} for L{Vector3d}.
       @kwarg Vector_kwds: Optional, additional B{C{Vector}} keyword arguments,
                           ignored if B{C{Vector=None}}.

       @return: 2-Tuple of the C{center} and C{radius} of the intersection of
                the spheres if B{C{sphere}} is C{True}.  The C{radius} is C{0.0}
                for abutting spheres.  Otherwise, a 2-tuple of the intersection
                points of two circles.  For abutting circles, both intersection
                points are the same B{C{Vector}} instance.

       @raise IntersectionError: Concentric, invalid or non-intersecting spheres
                                 or circles.

       @raise UnitError: Invalid B{C{radius1}} or B{C{radius2}}.

       @see: U{Sphere-Sphere<https://MathWorld.Wolfram.com/Sphere-
             SphereIntersection.html>} and U{circle-circle
             <https://MathWorld.Wolfram.com/Circle-CircleIntersection.html>}
             intersections.
    '''
    try:
        return _intersects2(center1, Radius_(radius1=radius1),
                            center2, Radius_(radius2=radius2),
                            sphere=sphere, Vector=Vector, **Vector_kwds)
    except (TypeError, ValueError) as x:
        raise IntersectionError(center1=center1, radius1=radius1,
                                center2=center2, radius2=radius2, txt=str(x))


def _intersects2(center1, r1, center2, r2, sphere=True, too_d=None,  # in .ellipsoidalBase._intersections2
                                           Vector=None, **Vector_kwds):
    # (INTERNAL) Intersect two spheres or circles, see L{intersections2}
    # above, separated to allow callers to embellish any exceptions

    def _Vector(x, y, z):
        n = intersections2.__name__
        if Vector is None:
            v = Vector3d(x, y, z, name=n)
        else:
            kwds = _xkwds(Vector_kwds, name=n)
            v = Vector(x, y, z, **kwds)
        return v

    def _xVector(c1, u, x, y):
        xy1 = x, y, _1_0  # transform to original space
        return _Vector(fdot(xy1, u.x, -u.y, c1.x),
                       fdot(xy1, u.y,  u.x, c1.y), _0_0)

    c1 = _vother(sphere, center1=center1)
    c2 = _vother(sphere, center2=center2)

    if r1 < r2:  # r1, r2 == R, r
        c1, c2 = c2, c1
        r1, r2 = r2, r1

    m = c2.minus(c1)
    d = m.length
    if d < max(r2 - r1, EPS):
        raise ValueError(_near_concentric_)

    o = fsum_(-d, r1, r2)  # overlap == -(d - (r1 + r2))
    # compute intersections with c1 at (0, 0) and c2 at (d, 0), like
    # <https://MathWorld.Wolfram.com/Circle-CircleIntersection.html>
    if o > EPS:  # overlapping, r1, r2 == R, r
        x = _radical2(d, r1, r2).xline
        y = _1_0 - (x / r1)**2
        if y > EPS:
            y = r1 * sqrt(y)  # y == a / 2
        elif y < 0:
            raise ValueError(_invalid_)
        else:  # abutting
            y = _0_0
    elif o < 0:
        t = d if too_d is None else too_d
        raise ValueError(_too_distant_fmt_ % (t,))
    else:  # abutting
        x, y = r1, _0_0

    u = m.unit()
    if sphere:  # sphere radius and center
        c = c1 if x < EPS  else (
            c2 if x > EPS1 else c1.plus(u.times(x)))
        t = _Vector(c.x, c.y, c.z), Radius(y)

    elif y > 0:  # intersecting circles
        t = _xVector(c1, u, x, y), _xVector(c1, u, x, -y)
    else:  # abutting circles
        t = _xVector(c1, u, x, 0)
        t = t, t
    return t


def nearestOn(point, point1, point2, within=True,
                                     Vector=None, **Vector_kwds):
    '''Locate the point between two points closest to this point.

       @arg point1: Start point (L{Vector3d}, C{Vector3Tuple} or
                                 C{Vector4Tuple}).
       @arg point2: End point (L{Vector3d}, C{Vector3Tuple} or
                               C{Vector4Tuple}).
       @kwarg within: If C{True} return the closest point between
                      both given points, otherwise the closest
                      point on the extended line through both
                      points (C{bool}).
       @kwarg Vector: Class to return closest point (L{Vector3d} or
                      C{Vector3Tuple}) or C{None} for L{Vector3d}.
       @kwarg Vector_kwds: Optional, additional B{C{Vector}} keyword
                           arguments, ignored if B{C{Vector=None}}.

       @return: Closest point (L{Vector3d} or C{Vector}).

       @raise TypeError: Invalid B{C{point}}, B{C{point1}} or B{C{point2}}.

       @see: Methods L{sphericalTrigonometry.LatLon.nearestOn3} and
             L{sphericalTrigonometry.LatLon.nearestOn3}
             U{3-D Point-Line distance<https://MathWorld.Wolfram.com/
             Point-LineDistance3-Dimensional.html>}.
    '''
    def _v3d(p, _i_):
        if not isinstance(p, Vector3d):
            try:
                p = Vector3d(p.x, p.y, p.z)
            except (AttributeError, TypeError, ValueError) as x:
                raise _TypeError(_point_ + _i_, p, txt=str(x))
        return p

    p = _nearestOn(_v3d(point, NN), _v3d(point1, _1_),
                                    _v3d(point2, _2_), within)
    if Vector is not None:
        p = Vector(p.x, p.y, p.z, **Vector_kwds)
    return p


def _nearestOn(p0, p1, p2, within=True):
    # (INTERNAL) Get closest point, see L{nearestOn} above,
    # separated to allow callers to embellish any exceptions

    p21 = p2.minus(p1)
    d2 = p21.length**2
    if d2 < EPS:  # coincident
        p = p1  # ... or p2
    else:
        t = p0.minus(p1).dot(p21) / d2
        p = p1 if (within and t < EPS)  else (
            p2 if (within and t > EPS1) else
            p1.plus(p21.times(t)))
    return p


def parse3d(str3d, sep=_COMMA_, name=NN, Vector=Vector3d, **Vector_kwds):
    '''Parse an C{"x, y, z"} string.

       @arg str3d: X, y and z values (C{str}).
       @kwarg sep: Optional separator (C{str}).
       @kwarg name: Optional instance name (C{str}).
       @kwarg Vector: Optional class (L{Vector3d}).
       @kwarg Vector_kwds: Optional B{C{Vector}} keyword arguments,
                           ignored if B{C{Vector=None}}.

       @return: New B{C{Vector}} or if B{C{Vector}} is C{None},
                a L{Vector3Tuple}C{(x, y, z)}.

       @raise VectorError: Invalid B{C{str3d}}.
    '''
    try:
        v = [float(v.strip()) for v in str3d.split(sep)]
        if len(v) != 3:
            raise ValueError
    except (TypeError, ValueError) as x:
        raise VectorError(str3d=str3d, txt=str(x))

    r = Vector3Tuple(*v) if Vector is None else \
              Vector(*v, **Vector_kwds)
    return _xnamed(r, name, force=True)


def sumOf(vectors, Vector=Vector3d, **Vector_kwds):
    '''Compute the vectorial sum of several vectors.

       @arg vectors: Vectors to be added (L{Vector3d}[]).
       @kwarg Vector: Optional class for the vectorial sum (L{Vector3d}).
       @kwarg Vector_kwds: Optional B{C{Vector}} keyword arguments,
                           ignored if B{C{Vector=None}}.

       @return: Vectorial sum as B{C{Vector}} or if B{C{Vector}} is
                C{None}, a L{Vector3Tuple}C{(x, y, z)}.

       @raise VectorError: No B{C{vectors}}.
    '''
    n, vectors = len2(vectors)
    if n < 1:
        raise VectorError(vectors=n, txt=_Missing)

    r = Vector3Tuple(fsum(v.x for v in vectors),
                     fsum(v.y for v in vectors),
                     fsum(v.z for v in vectors))
    if Vector is not None:
        r = Vector(r.x, r.y, r.z, **Vector_kwds)  # PYCHOK x, y, z
    return r


def trilaterate3d2(center1, radius1, center2, radius2, center3, radius3,
                                     eps=EPS, Vector=None, **Vector_kwds):
    '''Trilaterate three spheres each given as an 3d center and radius.

       @arg center1: Center of the 1st sphere (L{Vector3d}, C{Vector3Tuple}
                     or C{Vector4Tuple}).
       @arg radius1: Radius of this sphere (same C{units} as C{x}, C{y}
                     and C{z}).
       @arg center2: Center of the 2nd sphere (L{Vector3d}, C{Vector3Tuple}
                     or C{Vector4Tuple}).
       @arg radius2: Radius of this sphere (same C{units} as C{x}, C{y}
                     and C{z}).
       @arg center3: Center of the 3rd sphere (L{Vector3d}, C{Vector3Tuple}
                     or C{Vector4Tuple}).
       @arg radius3: Radius of the 3rd sphere (same C{units} as C{x}, C{y}
                     and C{z}).
       @kwarg eps: Tolerance (C{float}).
       @kwarg Vector: Class to return intersections (L{Vector3d} or
                      C{Vector3Tuple}) or C{None} for L{Vector3d}.
       @kwarg Vector_kwds: Optional, additional B{C{Vector}} keyword arguments,
                           ignored if B{C{Vector=None}}.

       @return: A 2-tuple C{(tri1, tri2)} with both trilaterated points
                (B{C{Vector}}).  Both C{tri1} and C{tri2} are the same
                instance if all three spheres abut or intersect in a
                single point.

       @raise ImportError: Package C{numpy} not found, not installed or
                           not at least version 1.15.

       @raise IntersectionError: No intersection, near concentric,
                                 trilateration failed.

       @raise TypeError: Invalid B{C{center1}}, B{C{center2}} or B{C{center3}}.

       @raise ValueError: Invalid B{C{radius1}}, B{C{radius2}} or B{C{radius3}}.

       @note: Package U{numpy<https://pypi.org/project/numpy>} is required,
              version 1.15 or later.

       @see: Norrdine, A. U{I{An Algebraic Solution to the Multilateration
             Problem}<https://www.ResearchGate.net/publication/
             275027725_An_Algebraic_Solution_to_the_Multilateration_Problem>}
             and U{implementation<https://www.ResearchGate.net/publication/
             288825016_Trilateration_Matlab_Code>}.
    '''
    def _txt(c1, r1, _1, c2, r2, _2):
        # check for too distant and concentric spheres
        d = c1.minus(c2).length
        if d > (r1 + r2):
            t = _too_distant_fmt_ % (d,)
        elif d < abs(r1 - r2):
            t = _near_concentric_
        else:
            return NN
        return 'center' + joined_(_1, 'and', _2, t)

    def _vN(t01, x, z):
        # compute x, y and z and return as Vector
        x, y, z = (float(x + t01 * z) for x, z in zip(x, z))
        n = trilaterate3d2.__name__
        if Vector is None:
            v = Vector3d(x, y, z, name=n)
        else:
            kwds = _xkwds(Vector_kwds, name=n)
            v = Vector(x, y, z, **kwds)
        return v

    np = Vector3d._numpy
    if np is None:  # get numpy, once
        Vector3d._numpy = np = _xnumpy(trilaterate3d2, 1, 12)

    c1 = _vother(True, center1=center1)
    c2 = _vother(True, center2=center2)
    c3 = _vother(True, center3=center3)

    A = []  # 3 x 4
    b = []
    for c, d in ((c1, Radius_(radius1=radius1, low=eps)),
                 (c2, Radius_(radius2=radius2, low=eps)),
                 (c3, Radius_(radius3=radius3, low=eps))):
        A.append((_1_0, -2 * c.x, -2 * c.y, -2 * c.z))
        b.append(d**2 - c.length2)

    X = np.dot(np.linalg.pinv(A), b)  # Moore-Penrose pseudo-inverse
    Z, _ = _null_space2(np, A, eps)
    if np.shape(Z) != (4, 1):
        t = None  # near concentric
    else:
        x = X[1:]
        z = Z[1:]
        # quadratic polynominal, ordered (^0, ^1, ^2)
        p = (fdot(X, -_1_0, *x),
             fdot(Z, -_0_5, *x) * 2,
             fdot(Z,  _0_0, *z))
        t = tuple(r for r in np.polynomial.polynomial.polyroots(p)
                          if not np.iscomplex(r))  # too distant

    if not t:  # near concentric, too distant, no intersection, etc.
        t = _txt(c1, radius1, _1_, c2, radius2, _2_) or \
            _txt(c1, radius1, _1_, c3, radius3, _3_) or \
            _txt(c2, radius2, _2_, c3, radius3, _3_) or _no_intersection_
        raise IntersectionError(center1=center2, radius1=radius1,
                                center2=center2, radius2=radius2,
                                center3=center3, radius3=radius3,
                                txt=t)
    elif len(t) < 2:  # one intersection
        t = t[0], t[0]

    v = _vN(t[0], x, z)
    if abs(t[0] - t[1]) < eps:  # abutting
        t = v, v
    else:
        t = v, _vN(t[1], x, z)
    return t


def _null_space2(numpy, A, eps):
    # return the nullspace and rank of matrix A
    # @see: <https://SciPy-Cookbook.ReadTheDocs.io/items/RankNullspace.html>,
    # <https://NumPy.org/doc/stable/reference/generated/numpy.linalg.svd.html>,
    # <https://StackOverflow.com/questions/19820921>,
    # <https://StackOverflow.com/questions/2992947> and
    # <https://StackOverflow.com/questions/5889142>
    A = numpy.array(A)
    m = max(numpy.shape(A))
    if m != 4:  # for this usage
        raise _AssertionError(shape=m, txt=modulename(_null_space2, True))
    # if needed, square A, pad with zeros
    A = numpy.resize(A, m * m).reshape(m, m)
#   try:  # no numpy.linalg.null_space <https://docs.SciPy.org/doc/>
#       return scipy.linalg.null_space(A)  # XXX no spipy.linalg?
#   except AttributeError:
#       pass
    _, s, v = numpy.linalg.svd(A)
    t = max(eps, eps * s[0])  # tol, s[0] is largest singular
    r = numpy.sum(s > t)  # rank
    n = numpy.transpose(v[r:])  # nullspace
    # double check residual to be near-zero
    e = float(numpy.max(numpy.abs(numpy.dot(A, n))))
    if e > t:
        raise _AssertionError(eps=e, txt=modulename(_null_space2, True))
    # del A, s, vh  # release numpy
    return n, r


def _vother(sphere, **name_v):
    # check B{C{center#}} vector instance, return Vector3d
    name, v = name_v.popitem()
    try:  # isinstance(v, (Vector3, Vector3Tuple, Vector4Tuple))
        return Vector3d(v.x, v.y, v.z if sphere else _0_0)
    except AttributeError:  # no _x_ or _y_ attr
        pass
    raise _xotherError(Vector3d(0, 0, 0), v, name=name, up=2)


__all__ += _ALL_DOCS(intersections2, sumOf)

# **) MIT License
#
# Copyright (C) 2016-2020 -- mrJean1 at Gmail -- All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
