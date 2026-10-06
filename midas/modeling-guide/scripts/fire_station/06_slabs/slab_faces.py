# -*- coding: utf-8 -*-
# Slab panels = closed faces of the analytical beam graph of one level.
import json, math
from collections import defaultdict
SC=__import__("os").environ.get("MG_WORKDIR", ".")   # working data folder (JSON / PNG in and out)

def faces(elems):
    """elems: list of dict(a,b,id). Returns list of faces: dict(poly=[pts], edges=[elem ids]) (outer face removed)."""
    adj=defaultdict(list); eid={}
    for e in elems:
        a,b=tuple(e["a"]),tuple(e["b"]); adj[a].append(b); adj[b].append(a); eid[(a,b)]=eid[(b,a)]=e["id"]
    ang=lambda p,q:math.atan2(q[1]-p[1],q[0]-p[0])
    for p in adj: adj[p].sort(key=lambda q:ang(p,q))
    used=set(); out=[]
    for a in adj:
        for b in adj[a]:
            if (a,b) in used: continue
            poly=[]; edges=[]; u,v=a,b
            while (u,v) not in used:
                used.add((u,v)); poly.append(u); edges.append(eid[(u,v)])
                nb=adj[v]; i=nb.index(u); w=nb[(i-1)%len(nb)]      # next edge: most clockwise turn -> face on the left
                u,v=v,w
            out.append(dict(poly=poly,edges=edges))
    area=lambda P:sum(P[i][0]*P[(i+1)%len(P)][1]-P[(i+1)%len(P)][0]*P[i][1] for i in range(len(P)))/2
    for f in out: f["area"]=area(f["poly"])/1e6
    return [f for f in out if f["area"]>1e-6]                        # CCW faces only (outer face is CW)

def simplify(P):
    """drop collinear vertices -> true corners"""
    Q=[]
    n=len(P)
    for i in range(n):
        a,b,c=P[i-1],P[i],P[(i+1)%n]
        if abs((b[0]-a[0])*(c[1]-b[1])-(b[1]-a[1])*(c[0]-b[0]))>1e-3*math.dist(a,b)*math.dist(b,c): Q.append(b)
    return Q
