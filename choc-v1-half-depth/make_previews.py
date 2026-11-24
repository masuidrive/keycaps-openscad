#!/usr/bin/env python3
"""Create CAD-derived review images. Requires CadQuery, NumPy and Matplotlib."""
from pathlib import Path
import os
os.environ.setdefault("MPLCONFIGDIR", "/tmp/choc-mpl")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
import numpy as np
from build_keycap_reve import *

DIR = Path(__file__).resolve().parent
BG, INK, SUB, TEAL = "#f6f8fc", "#122139", "#425469", "#027c74"

def project(ax, s, camera, color):
    v, ids = s.tessellate(0.025, 0.08)
    pts = np.array([[p.x, p.y, p.z] for p in v])
    tri = pts[np.array(ids)]
    camera = np.array(camera, dtype=float)
    camera /= np.linalg.norm(camera)
    xhat = np.cross((0, 0, 1), camera)
    xhat /= np.linalg.norm(xhat)
    yhat = np.cross(camera, xhat)
    norm = np.cross(tri[:,1]-tri[:,0], tri[:,2]-tri[:,0])
    norm /= np.linalg.norm(norm, axis=1)[:,None]
    light = np.array((-0.6,-0.5,1.0 if camera[2]>0 else -1.0))
    light /= np.linalg.norm(light)
    polys = np.stack((tri @ xhat, tri @ yhat), axis=2)
    depths = tri @ camera
    active = np.where((norm @ camera) > 0.001)[0]
    shade = (0.61 + 0.36*np.maximum(0,norm @ light))
    colors = np.clip(np.asarray(color)[None,:]*shade[:,None] + 0.055, 0, 1)
    lo, hi = polys[active].min(axis=(0,1)), polys[active].max(axis=(0,1))
    polys -= (lo+hi)/2
    # Actual depth buffer; protects the top plate from through-projection of pegs.
    scale = 42
    extent = (-8.8, 8.8, -6.0, 6.0)
    width, height = int((extent[1]-extent[0])*scale), int((extent[3]-extent[2])*scale)
    zbuf = np.full((height,width), -np.inf)
    rgba = np.zeros((height,width,4), dtype=np.uint8)
    screen = (polys - (extent[0],extent[2]))*scale
    for j in active:
        a,b,c = screen[j]
        v,u = b-a,c-a
        den = v[0]*u[1]-v[1]*u[0]
        if abs(den)<1e-10:
            continue
        x0,y0 = np.maximum(0,np.floor(screen[j].min(axis=0)).astype(int))
        x1,y1 = np.minimum((width,height),np.ceil(screen[j].max(axis=0)).astype(int))
        if x1<=x0 or y1<=y0:
            continue
        x,y = np.meshgrid(np.arange(x0,x1)+.5-a[0],np.arange(y0,y1)+.5-a[1])
        l=(x*u[1]-y*u[0])/den
        m=(v[0]*y-v[1]*x)/den
        z=depths[j,0] + l*(depths[j,1]-depths[j,0]) + m*(depths[j,2]-depths[j,0])
        rect=zbuf[y0:y1,x0:x1]
        sel=(l>=-1e-8)&(m>=-1e-8)&(l+m<=1+1e-8)&(z>rect)
        rect[sel]=z[sel]
        rgba[y0:y1,x0:x1][sel]=[*np.round(colors[j]*255).astype(np.uint8),255]
    ax.imshow(rgba, origin="lower", extent=extent, interpolation="antialiased")
    ax.set(xlim=(-8.8,8.8), ylim=(-6,6), aspect="equal")
    ax.axis("off")

def dim(ax, x1, y1, x2, y2, label, dy=.16, rotation=0):
    ax.annotate("", xy=(x2,y2), xytext=(x1,y1),
                arrowprops=dict(arrowstyle="<->", color=TEAL, shrinkA=0, shrinkB=0, linewidth=1))
    ax.text((x1+x2)/2+(0.24 if rotation else 0),(y1+y2)/2+(0 if rotation else dy),label,
            ha="left" if rotation else "center",va="center" if rotation else "bottom",
            fontsize=9,color=TEAL,rotation=rotation,rotation_mode="anchor")

def rr(ax,w,d,r,fc="none",ec=INK,lw=1.45,ls="-"):
    ax.add_patch(FancyBboxPatch((-w/2,-d/2),w,d,boxstyle=f"round,pad=0,rounding_size={r}",
                                facecolor=fc,edgecolor=ec,linewidth=lw,linestyle=ls))

fig, axes = plt.subplots(2,3,figsize=(10.4,7),facecolor=BG)
fig.subplots_adjust(left=.05,right=.95,bottom=.08,top=.81,hspace=.43,wspace=.19)
fig.text(.06,.925,"Choc v1 / RevE",fontsize=27,fontweight="bold",color=INK)
fig.text(.06,.877,"Reconstructed prototypes  /  C0.8 upper outside edge only",fontsize=13,color=SUB)
for i,(variant,(w,d)) in enumerate(LEG_DIMS.items()):
    shape = model(variant)
    project(axes[0,i],shape,(-.8,-1.2,1.32),(.47,.64,.80))
    project(axes[1,i],shape,(.48,-1.25,-1.45),(.47,.64,.80))
    axes[0,i].set_title(f"{variant}  /  {w:.2f} × {d:.2f} mm pegs",pad=2,fontsize=10.5,fontweight="bold",color=INK)
    axes[1,i].set_title(f"Underside  /  {i+1} {'groove' if i==0 else 'grooves'}",pad=2,fontsize=10.5,color=SUB)
fig.text(.06,.048,"CAD projections  •  14.5 × 8 × 5.7 mm envelope  •  Physical fit not verified",fontsize=9,color=SUB)
fig.savefig(DIR/"RevE_CAD_Preview.png",dpi=160,facecolor=BG)
plt.close(fig)

fig, axes=plt.subplots(2,2,figsize=(11,8),facecolor=BG)
fig.subplots_adjust(left=.07,right=.94,bottom=.08,top=.83,hspace=.52,wspace=.18)
fig.text(.07,.936,"Choc v1 / RevE dimensions",fontsize=24,fontweight="bold",color=INK)
fig.text(.07,.89,"All dimensions in mm  /  Prototype reconstruction",fontsize=12,color=SUB)
ax=axes[0,0]; rr(ax,W,D,CORNER_R,"#e0ebf5");rr(ax,W-2*TOP_C,D-2*TOP_C,CORNER_R-TOP_C,"#f0f6fa",TEAL)
dim(ax,-W/2,5,W/2,5,"14.5"); dim(ax,9,-D/2,9,D/2,"8",0.2,90)
ax.annotate("C0.8 × 45°",xy=(5.7,-3.65),xytext=(3,-5.5),color=TEAL,fontsize=9,arrowprops={"arrowstyle":"->","color":TEAL})
ax.set(xlim=(-9.3,10.2),ylim=(-6.1,5.9)); ax.set_title("Top",fontweight="bold",color=INK)
ax=axes[0,1];rr(ax,W,D,CORNER_R,"#e0ebf5")
for x in STEM_X:
    ax.add_patch(Rectangle((x-SHOULDER_W/2,-SHOULDER_D/2),SHOULDER_W,SHOULDER_D,fc="#c6d9eb",ec=SUB,lw=1))
    w,d=LEG_DIMS["C"]
    ax.add_patch(Rectangle((x-w/2,-d/2),w,d,fc="#647a92",ec=SUB,lw=1))
for y in GROOVE_Y["C"]:
    ax.add_patch(Rectangle((GROOVE_X-GROOVE_W/2,y-GROOVE_D/2),GROOVE_W,GROOVE_D,fc=BG,ec=TEAL,lw=1))
dim(ax,STEM_X[0],-2.8,STEM_X[1],-2.8,"5.7 pitch")
ax.annotate("2 × 1 × 0.8\n1 clear gap",xy=(GROOVE_X,1.9),xytext=(2.1,5.1),color=TEAL,fontsize=9,arrowprops={"arrowstyle":"->","color":TEAL})
ax.set(xlim=(-9.3,10.2),ylim=(-5.6,6.2)); ax.set_title("Underside — C shown",fontweight="bold",color=INK)
ax=axes[1,0]
outline=[(-W/2,PLATE_Z),(W/2,PLATE_Z),(W/2,H-TOP_C),(W/2-TOP_C,H),(-W/2+TOP_C,H),(-W/2,H-TOP_C)]
ax.fill(*zip(*outline),facecolor="#e0ebf5",edgecolor=INK)
for x in STEM_X:
    ax.add_patch(Rectangle((x-SHOULDER_W/2,LEG_T),SHOULDER_W,SHOULDER_T,fc="#c6d9eb",ec=INK,lw=1))
    w,_=LEG_DIMS["C"]
    pts=[(x-w/2,LEG_T),(x+w/2,LEG_T),(x+w/2,TIP_C),(x+w/2-TIP_C,0),(x-w/2+TIP_C,0),(x-w/2,TIP_C)]
    ax.fill(*zip(*pts),facecolor="#647a92",edgecolor=INK,lw=1)
dim(ax,9.2,0,9.2,H,"5.7  total",.13,90)
ax.text(-7.7,-1.0,"2 plate  +  0.6 shoulder  +  3.1 peg",fontsize=9,color=SUB)
ax.text(-7.7,-1.63,"0.08 peg-tip chamfer, separate from C0.8",fontsize=9,color=SUB)
ax.set(xlim=(-9.3,10.4),ylim=(-2.0,6.3)); ax.set_title("Front",fontweight="bold",color=INK)
ax=axes[1,1]
ax.text(.02,.91,"FIT VARIANTS",transform=ax.transAxes,color=TEAL,fontsize=11,fontweight="bold")
for i,(variant,(w,d)) in enumerate(LEG_DIMS.items()):
    ax.text(.02,.78-i*.17,f"{variant}      {w:.2f} × {d:.2f}    /    {i+1} {'groove' if i==0 else 'grooves'}",transform=ax.transAxes,color=INK,fontsize=12)
ax.text(.02,.13,"Reconstructed: corner R1.2, shoulder\npad footprint 1.80 × 3.80 and groove placement.",transform=ax.transAxes,color=SUB,fontsize=9.5)
for ax in axes.ravel()[:3]: ax.set_aspect("equal")
for ax in axes.ravel(): ax.axis("off")
fig.savefig(DIR/"RevE_Dimensional_Drawing.png",dpi=175,facecolor=BG)
fig.savefig(DIR/"RevE_Dimensional_Drawing.svg",facecolor=BG)
