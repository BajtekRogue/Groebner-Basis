from .monomial import Monomial

# Constant
CONST = Monomial({})

# Degree 1 K[x, y, z]
x = Monomial({'x': 1})
y = Monomial({'y': 1})
z = Monomial({'z': 1})

# Degree 2 K[x, y, z]
x2 = Monomial({'x': 2})
y2 = Monomial({'y': 2})
z2 = Monomial({'z': 2})
xy = Monomial({'x': 1, 'y': 1})
xz = Monomial({'x': 1, 'z': 1})
yz = Monomial({'y': 1, 'z': 1})

# Degree 3 K[x, y, z]
x3 = Monomial({'x': 3})
y3 = Monomial({'y': 3})
z3 = Monomial({'z': 3})
x2y = Monomial({'x': 2, 'y': 1})
x2z = Monomial({'x': 2, 'z': 1})
xy2 = Monomial({'x': 1, 'y': 2})
y2z = Monomial({'y': 2, 'z': 1})
xz2 = Monomial({'x': 1, 'z': 2})
yz2 = Monomial({'y': 1, 'z': 2})
xyz = Monomial({'x': 1, 'y': 1, 'z': 1})

# Degree 4 K[x, y, z]
x4 = Monomial({'x': 4})
y4 = Monomial({'y': 4})
z4 = Monomial({'z': 4})
x3y = Monomial({'x': 3, 'y': 1})
x3z = Monomial({'x': 3, 'z': 1})
xy3 = Monomial({'x': 1, 'y': 3})
y3z = Monomial({'y': 3, 'z': 1})
xz3 = Monomial({'x': 1, 'z': 3})
yz3 = Monomial({'y': 1, 'z': 3})
x2y2 = Monomial({'x': 2, 'y': 2})
x2z2 = Monomial({'x': 2, 'z': 2})
y2z2 = Monomial({'y': 2, 'z': 2})
x2yz = Monomial({'x': 2, 'y': 1, 'z': 1})
xy2z = Monomial({'x': 1, 'y': 2, 'z': 1})
xyz2 = Monomial({'x': 1, 'y': 1, 'z': 2})

# Degree 1 K[t, u, v]
t = Monomial({'t': 1})
u = Monomial({'u': 1})
v = Monomial({'v': 1})

# Degree 2 K[t, u, v]
t2 = Monomial({'t': 2})
u2 = Monomial({'u': 2})
v2 = Monomial({'v': 2})
tu = Monomial({'t': 1, 'u': 1})
tv = Monomial({'t': 1, 'v': 1})
uv = Monomial({'u': 1, 'v': 1})

# Degree 3 K[t, u, v]
t3 = Monomial({'t': 3})
u3 = Monomial({'u': 3})
v3 = Monomial({'v': 3})
t2u = Monomial({'t': 2, 'u': 1})
t2v = Monomial({'t': 2, 'v': 1})
tu2 = Monomial({'t': 1, 'u': 2})
u2v = Monomial({'u': 2, 'v': 1})
tv2 = Monomial({'t': 1, 'v': 2})
uv2 = Monomial({'u': 1, 'v': 2})
tuv = Monomial({'t': 1, 'u': 1, 'v': 1})

# Degree 4 K[t, u, v]
t4 = Monomial({'t': 4})
u4 = Monomial({'u': 4})
v4 = Monomial({'v': 4})
t3u = Monomial({'t': 3, 'u': 1})
t3v = Monomial({'t': 3, 'v': 1})
tu3 = Monomial({'t': 1, 'u': 3})
u3v = Monomial({'u': 3, 'v': 1})
tv3 = Monomial({'t': 1, 'v': 3})
uv3 = Monomial({'u': 1, 'v': 3})
t2u2 = Monomial({'t': 2, 'u': 2})
t2v2 = Monomial({'t': 2, 'v': 2})
u2v2 = Monomial({'u': 2, 'v': 2})
t2uv = Monomial({'t': 2, 'u': 1, 'v': 1})
tu2v = Monomial({'t': 1, 'u': 2, 'v': 1})
tuv2 = Monomial({'t': 1, 'u': 1, 'v': 2})


# Degree 1 K[a, b, c]
a = Monomial({'a': 1})
b = Monomial({'b': 1})
c = Monomial({'c': 1})

# Degree 2 K[a, b, c]
a2 = Monomial({'a': 2})
b2 = Monomial({'b': 2})
c2 = Monomial({'c': 2})
ab = Monomial({'a': 1, 'b': 1})
ac = Monomial({'a': 1, 'c': 1})
bc = Monomial({'b': 1, 'c': 1})

# Degree 3 K[a, b, c]
a3 = Monomial({'a': 3})
b3 = Monomial({'b': 3})
c3 = Monomial({'c': 3})
a2b = Monomial({'a': 2, 'b': 1})
a2c = Monomial({'a': 2, 'c': 1})
ab2 = Monomial({'a': 1, 'b': 2})
b2c = Monomial({'b': 2, 'c': 1})
ac2 = Monomial({'a': 1, 'c': 2})
bc2 = Monomial({'b': 1, 'c': 2})
abc = Monomial({'a': 1, 'b': 1, 'c': 1})

# Degree 4 K[a, b, c]
a4 = Monomial({'a': 4})
b4 = Monomial({'b': 4})
c4 = Monomial({'c': 4})
a3b = Monomial({'a': 3, 'b': 1})
a3c = Monomial({'a': 3, 'c': 1})
ab3 = Monomial({'a': 1, 'b': 3})
b3c = Monomial({'b': 3, 'c': 1})
ac3 = Monomial({'a': 1, 'c': 3})
bc3 = Monomial({'b': 1, 'c': 3})
a2b2 = Monomial({'a': 2, 'b': 2})
a2c2 = Monomial({'a': 2, 'c': 2})
b2c2 = Monomial({'b': 2, 'c': 2})
a2bc = Monomial({'a': 2, 'b': 1, 'c': 1})
ab2c = Monomial({'a': 1, 'b': 2, 'c': 1})
abc2 = Monomial({'a': 1, 'b': 1, 'c': 2})


