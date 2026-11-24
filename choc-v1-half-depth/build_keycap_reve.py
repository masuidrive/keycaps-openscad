#!/usr/bin/env python3
"""Parametric reconstruction (not the historical RevB CAD). Requires CadQuery 2.x."""
import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import struct

import cadquery as cq

W, D, H = 14.5, 8.0, 5.7
PLATE_T, SHOULDER_T, LEG_T = 2.0, 0.6, 3.1
PITCH, TIP_C, TOP_C = 5.7, 0.08, 0.8
LEG_DIMS = {"A": (1.10, 2.80), "B": (1.15, 2.85), "C": (1.20, 2.90)}
# Not preserved in the surviving spec: explicitly chosen reconstruction values.
CORNER_R = 1.2
SHOULDER_W, SHOULDER_D = 1.80, 3.80
# Long axis along X. C's three grooves have 1 mm gaps. The pocket
# on the right is also 1 mm from both the shoulder and the outer wall.
GROOVE_X = 5.75
GROOVE_W, GROOVE_D, GROOVE_Z = 2.0, 1.0, 0.8
GROOVE_Y = {"A": (0.0,), "B": (-1.0, 1.0), "C": (-2.0, 0.0, 2.0)}
STEM_X = (-PITCH / 2, PITCH / 2)
PLATE_Z = LEG_T + SHOULDER_T


def box(x, y, z, w, d, h):
    return cq.Workplane("XY").workplane(offset=z).center(x, y).box(
        w, d, h, centered=(True, True, False)
    )


def model(variant, chamfer=TOP_C, width=W):
    assert variant in LEG_DIMS
    w, d = LEG_DIMS[variant]
    plate = box(0, 0, PLATE_Z, width, D, PLATE_T).edges("|Z").fillet(CORNER_R)
    if chamfer:
        plate = plate.edges(">Z").chamfer(chamfer)
    for y in GROOVE_Y[variant]:
        # The pocket opens only toward the flat plate underside.
        cut = box(GROOVE_X, y, PLATE_Z - 0.1, GROOVE_W, GROOVE_D, GROOVE_Z + 0.1)
        plate = plate.cut(cut)
    for x in STEM_X:
        shoulder = box(x, 0, LEG_T, SHOULDER_W, SHOULDER_D, SHOULDER_T)
        peg = box(x, 0, 0, w, d, LEG_T).edges("<Z").chamfer(TIP_C)
        plate = plate.union(shoulder).union(peg)
    return plate.clean().val()


def near(x, y, tol=1e-6):
    assert abs(x - y) <= tol, (x, y)


def bounds(s):
    b = s.BoundingBox()
    return (b.xlen, b.ylen, b.zlen)


def section(s, z, thickness=0.002):
    return s.intersect(box(0, 0, z, 30.0, 30.0, thickness).val())


def check_shape(s, variant):
    assert s.isValid() and len(s.Solids()) == 1
    for got, want in zip(bounds(s), (W, D, H)):
        near(got, want)
    top = max(s.Faces(), key=lambda f: f.Center().z)
    near(top.Center().z, H)
    near(top.BoundingBox().xlen, W - 2 * TOP_C)
    near(top.BoundingBox().ylen, D - 2 * TOP_C)
    cap_wall = section(s, H - TOP_C - 0.005)
    near(cap_wall.BoundingBox().xlen, W)
    near(cap_wall.BoundingBox().ylen, D)
    # Arbitrary plane section halfway through the C0.4 where the 45° slope
    # should inset half the nominal chamfer on both sides.
    bevel = section(s, H - TOP_C / 2, thickness=0.0001)
    near(bevel.BoundingBox().xlen, W - TOP_C)
    near(bevel.BoundingBox().ylen, D - TOP_C)
    w, d = LEG_DIMS[variant]
    ns = sorted(section(s, 0.5).Solids(), key=lambda so: so.Center().x)
    assert len(ns) == 2
    near(ns[1].Center().x - ns[0].Center().x, PITCH)
    for leg in ns:
        near(leg.BoundingBox().xlen, w)
        near(leg.BoundingBox().ylen, d)
    ns = sorted(section(s, 0, thickness=0.0001).Solids(), key=lambda so: so.Center().x)
    assert len(ns) == 2
    for leg in ns:
        near(leg.BoundingBox().xlen, w - 2 * (TIP_C - 0.0001))
        near(leg.BoundingBox().ylen, d - 2 * (TIP_C - 0.0001))
    for x in STEM_X:
        shoulder = s.intersect(box(x, 0, LEG_T + 0.3, SHOULDER_W + 0.1, SHOULDER_D + 0.1, 0.002).val())
        near(shoulder.BoundingBox().xlen, SHOULDER_W)
        near(shoulder.BoundingBox().ylen, SHOULDER_D)
    # Verify count and volume of pockets against the same CAD with no pockets.
    unpocketed = box(0, 0, PLATE_Z, W, D, PLATE_T).edges("|Z").fillet(CORNER_R).val()
    roof = unpocketed.intersect(box(0, 0, PLATE_Z, 30, 30, 0.9).val())
    difference = roof.cut(s)
    assert len(difference.Solids()) == len(GROOVE_Y[variant])
    for cavity, y in zip(sorted(difference.Solids(), key=lambda v: v.Center().y), GROOVE_Y[variant]):
        for got, want in zip(bounds(cavity), (GROOVE_W, GROOVE_D, GROOVE_Z)):
            near(got, want)
        near(cavity.Center().y, y)
    # Compare solids as sets with the reconstructed baseline, not the unavailable RevB bytes.
    lower = box(0, 0, -1, 40, 40, H - TOP_C + 1).val()
    a, b = model(variant, 0).intersect(lower), s.intersect(lower)
    near(a.Volume(), b.Volume())
    near(a.cut(b).Volume(), 0)
    near(b.cut(a).Volume(), 0)
    check_predecessor(s, model(variant, width=15.5))

def check_predecessor(s, revd):
    # Encloses the whole underside interface including the groove pockets,
    # but not the deliberately shortened exterior rim.
    interface = box(0, 0, -0.1, 13.5, 7.0, 4.7).val()
    a, b = revd.intersect(interface), s.intersect(interface)
    near(a.cut(b).Volume(), 0)
    near(b.cut(a).Volume(), 0)
    near(s.cut(revd).Volume(), 0)
    assert revd.Volume() > s.Volume()
    near(s.BoundingBox().xmin, -W / 2)
    near(s.BoundingBox().xmax, W / 2)
    return round(revd.Volume() - s.Volume(), 6)


def stl_report(p, shape):
    data = p.read_bytes()
    n, = struct.unpack_from("<I", data, 80)
    assert len(data) == 84 + 50 * n and n > 0
    # STL's independently copied float32 coordinates can differ by a few ULPs.
    # Compare with a 1e-4 mm weld and also prove nondegenerate facet orientation.
    edges = Counter()
    verts = set()
    vol = 0.0
    xyz = []
    for i in range(n):
        a = struct.unpack_from("<12fH", data, 84 + 50 * i)
        t = [a[j:j+3] for j in (3, 6, 9)]
        x, y, z = t
        u = [b - a for a, b in zip(x, y)]
        v = [b - a for a, b in zip(x, z)]
        cr = [u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0]]
        assert sum(k*k for k in cr) > 1e-20
        assert sum(k*l for k, l in zip(cr, a[:3])) > 0
        vol += sum(k*l for k, l in zip(cr, x)) / 6.0
        xyz.extend(t)
        ts = [tuple(round(k * 1e4) for k in v) for v in t]
        assert len(set(ts)) == 3
        verts.update(ts)
        for ei in range(3):
            edges[ts[ei], ts[(ei+1) % 3]] += 1
    adj = {}
    for (a, b), count in edges.items():
        assert count == 1 and edges[b, a] == 1
        adj.setdefault(a, set()).add(b)
    todo = [next(iter(verts))]
    seen = set()
    while todo:
        cur = todo.pop()
        if cur not in seen:
            seen.add(cur)
            todo.extend(adj[cur] - seen)
    assert seen == verts
    for values, desired in zip(zip(*xyz), (W, D, H)):
        near(max(values) - min(values), desired, 0.0003)
    assert vol > 0 and abs(vol - shape.Volume()) < 0.2
    return {"triangles": n, "welded_vertices": len(verts), "closed": True,
            "edge_manifold": True, "single_component": True, "outward_winding": True,
            "volume_mm3": round(vol, 6)}


def write(out, predecessor=None):
    out.mkdir(parents=True, exist_ok=True)
    report = {}
    for key, dims in LEG_DIMS.items():
        s = model(key)
        check_shape(s, key)
        stem = f"ChocV1_14p5x8_RevE_{key}"
        stl, step = (out / f"{stem}.{fmt}" for fmt in ("stl", "step"))
        s.exportStl(str(stl), tolerance=0.004, angularTolerance=0.05, relative=False)
        cq.exporters.export(s, str(step))
        imported = cq.importers.importStep(str(step)).val()
        check_shape(imported, key)
        near(imported.Volume(), s.Volume(), 0.0001)
        prior = predecessor / f"ChocV1_15p5x8_RevD_{key}.step" if predecessor else None
        removed = None
        if prior:
            removed = check_predecessor(imported, cq.importers.importStep(str(prior)).val())
        report[key] = {
            "bounds_mm": [round(v, 6) for v in bounds(imported)],
            "flat_top_bounds_mm": [W - 2 * TOP_C, D - 2 * TOP_C],
            "top_outer_chamfer_mm": TOP_C, "peg_tip_chamfer_mm": TIP_C,
            "peg_xy_mm": list(dims), "peg_pitch_mm": PITCH,
            "plate_mm": PLATE_T, "shoulder_mm": SHOULDER_T, "peg_mm": LEG_T,
            "grooves": len(GROOVE_Y[key]), "groove_dimensions_mm": [GROOVE_W, GROOVE_D, GROOVE_Z],
            "step_solid": "valid single solid after round-trip",
            "upper_chamfer_only_vs_reconstructed_baseline": True,
            "unchanged_functional_underside_vs_revd": True,
            "revd_step_reference_sha256": sha256(prior.read_bytes()).hexdigest() if prior else None,
            "revd_actual_step_removal_mm3": removed,
            "front_side_groove_outer_margin_mm": round(W / 2 - (GROOVE_X + GROOVE_W / 2), 6),
            "step_volume_mm3": round(imported.Volume(), 6),
            "stl": stl_report(stl, s),
            "sha256": {p.name: sha256(p.read_bytes()).hexdigest() for p in (stl, step)},
        }
    (out / "qa.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output", type=Path, default=Path(__file__).resolve().parent)
    p.add_argument("--revd-cad", type=Path, help="Verify against exact exported RevD STEP files.")
    args = p.parse_args()
    write(args.output, args.revd_cad)
