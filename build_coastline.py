"""Rebuild the coastline data: the US copy embedded in index.html, and the worldwide tiles in coast/.

Source: @geo-maps/earth-coastlines-100m (OpenStreetMap coastline, about 100 m accuracy, ODbL).

    npm pack @geo-maps/earth-coastlines-100m
    tar xzf geo-maps-earth-coastlines-100m-*.tgz
    python build_coastline.py package/map.geo.json us_coast.txt          # US copy
    python build_coastline.py package/map.geo.json --tiles coast         # worldwide tiles

For the US copy, replace the contents of <script type="text/plain" id="coastData"> in index.html
with the contents of us_coast.txt. For the tiles, replace the coast/ folder and update the
COAST_TILES list in index.html with the printed tile names.

Tiles are 30° x 30°, named like n30w120.txt (south-west corner). Each segment is stored in
the tile that holds its first point, so no segment is stored twice.

Format: one coastline run per line, Google encoded-polyline (lat, lon) at 1e-4 degree
precision. The land polygons in the source are clockwise, so land is always on the
right-hand side of each segment; the page relies on that to tell land from sea.
"""
import json
import math
import sys

# Lower 48 (with some margin into Canada and Mexico), Alaska, Aleutians west of 180, Hawaii, Puerto Rico and USVI.
BOXES = [
    (23.5, 50.5, -126.0, -65.5),
    (50.5, 72.0, -180.0, -129.0),
    (50.5, 56.0, 170.0, 180.0),
    (18.0, 23.0, -161.0, -154.0),
    (17.4, 18.9, -68.2, -64.2),
]
TOLERANCE_M = 25  # Douglas-Peucker simplification


def in_boxes(p):
    lon, lat = p
    return any(a <= lat <= b and c <= lon <= e for a, b, c, e in BOXES)


def simplify(pts, tol):
    if len(pts) < 3:
        return pts
    lat0 = math.radians(pts[0][1])
    kx, ky = 111320 * math.cos(lat0), 110540
    P = [(x * kx, y * ky) for x, y in pts]
    keep = [False] * len(P)
    keep[0] = keep[-1] = True
    stack = [(0, len(P) - 1)]
    while stack:
        i, j = stack.pop()
        ax, ay = P[i]
        bx, by = P[j]
        dx, dy = bx - ax, by - ay
        L = math.hypot(dx, dy)
        best, bi = -1, -1
        for k in range(i + 1, j):
            px, py = P[k]
            d = abs(dy * (px - ax) - dx * (py - ay)) / L if L > 1e-6 else math.hypot(px - ax, py - ay)
            if d > best:
                best, bi = d, k
        if best > tol:
            keep[bi] = True
            stack += [(i, bi), (bi, j)]
    return [p for p, k in zip(pts, keep) if k]


def enc(v):
    v = ~(v << 1) if v < 0 else (v << 1)
    out = []
    while v >= 0x20:
        out.append(chr((0x20 | (v & 0x1F)) + 63))
        v >>= 5
    out.append(chr(v + 63))
    return "".join(out)


def main(src, dst):
    geo = json.load(open(src))
    polys = geo["geometries"][0]["coordinates"]
    runs = []
    for poly in polys:
        for ring in poly:
            cur = []
            for p in ring:
                if in_boxes(p):
                    cur.append(p)
                else:
                    if len(cur) > 1:
                        runs.append(cur)
                    cur = []
            if len(cur) > 1:
                runs.append(cur)
    lines, npts = [], 0
    for r in runs:
        q = [(round(lat * 1e4), round(lon * 1e4)) for lon, lat in simplify(r, TOLERANCE_M)]
        q = [q[0]] + [p for a, p in zip(q, q[1:]) if p != a]
        if len(q) < 2:
            continue
        s, plat, plon = [], 0, 0
        for la, lo in q:
            s.append(enc(la - plat) + enc(lo - plon))
            plat, plon = la, lo
        lines.append("".join(s))
        npts += len(q)
    open(dst, "w").write("\n".join(lines))
    print(f"{len(lines)} runs, {npts} points written to {dst}")


TILE = 30


def tile_key(lat, lon):
    return (math.floor(lat / TILE) * TILE, math.floor(lon / TILE) * TILE)


def tile_name(la, lo):
    return f"{'n' if la >= 0 else 's'}{abs(la):02d}{'e' if lo >= 0 else 'w'}{abs(lo):03d}"


def build_tiles(src, out_dir):
    import collections
    import os
    geo = json.load(open(src))
    polys = geo["geometries"][0]["coordinates"]
    tiles = collections.defaultdict(list)
    for poly in polys:
        for ring in poly:
            q = [(round(lat * 1e4), round(lon * 1e4)) for lon, lat in simplify(ring, TOLERANCE_M)]
            q = [q[0]] + [p for a, p in zip(q, q[1:]) if p != a]
            if len(q) < 2:
                continue
            cur, ck = [q[0]], tile_key(q[0][0] / 1e4, q[0][1] / 1e4)
            for a, b in zip(q, q[1:]):
                k = tile_key(a[0] / 1e4, a[1] / 1e4)
                if k != ck:
                    if len(cur) > 1:
                        tiles[ck].append(cur)
                    cur, ck = [a], k
                cur.append(b)
            if len(cur) > 1:
                tiles[ck].append(cur)
    os.makedirs(out_dir, exist_ok=True)
    names = []
    for (la, lo), runs in sorted(tiles.items()):
        lines = []
        for r in runs:
            s, plat, plon = [], 0, 0
            for a, b in r:
                s.append(enc(a - plat) + enc(b - plon))
                plat, plon = a, b
            lines.append("".join(s))
        name = tile_name(la, lo)
        open(os.path.join(out_dir, name + ".txt"), "w").write("\n".join(lines))
        names.append(name)
    print(f"{len(names)} tiles written to {out_dir}/")
    print("COAST_TILES:", ",".join(f'"{n}"' for n in names))


if __name__ == "__main__":
    if len(sys.argv) > 3 and sys.argv[2] == "--tiles":
        build_tiles(sys.argv[1], sys.argv[3])
    else:
        main(sys.argv[1], sys.argv[2])
