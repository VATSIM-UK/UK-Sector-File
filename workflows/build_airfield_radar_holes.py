#!/usr/bin/env python3
"""
Generate Misc Other/Airfield_Radar_Holes.txt
-------------------------------------------
Creates radar HOLE definitions for all UK aerodromes (EG**)
based on public CC0 data from OurAirports.

- Each HOLE inhibits Primary, Secondary, and Mode C up to (elevation + 10 ft)
- Rectangular polygons are derived from runway endpoints (inflated slightly)
- Falls back to a small square if no runway data is present
"""

import csv, io, math, os, re, sys, urllib.request
from pathlib import Path
from typing import Dict, List, Tuple, Optional

ROOT = Path(__file__).resolve().parents[1]
AIRPORTS_DIR = ROOT / "Airports"
OUTFILE = ROOT / "Misc Other" / "Airfield_Radar_Holes.txt"

OURAIRPORTS_AIRPORTS = "https://ourairports.com/airports.csv"
OURAIRPORTS_RUNWAYS  = "https://ourairports.com/runways.csv"

# Parameters
RECT_INFLATE_M = float(os.getenv("RECT_INFLATE_M", 400.0))
FALLBACK_HALF_SIDE_M = float(os.getenv("FALLBACK_HALF_SIDE_M", 1250.0))

def list_repo_icaos() -> List[str]:
    return sorted(
        d.name.upper()
        for d in AIRPORTS_DIR.iterdir()
        if d.is_dir() and re.fullmatch(r"EG[A-Z0-9]{2}", d.name.upper())
    )

def fetch_csv(url: str) -> List[Dict[str, str]]:
    with urllib.request.urlopen(url, timeout=60) as r:
        data = r.read().decode("utf-8", errors="replace")
    return list(csv.DictReader(io.StringIO(data)))

def dlat_dlon(lat_deg: float, dx_m: float, dy_m: float) -> Tuple[float, float]:
    R = 6371008.8
    lat_r = math.radians(lat_deg)
    dlat = dy_m / R
    dlon = dx_m / (R * math.cos(lat_r))
    return math.degrees(dlat), math.degrees(dlon)

def hem(val: float, latlon: str) -> str:
    if latlon == "lat":  return ("N" if val >= 0 else "S") + f"{abs(val):.6f}"
    else:                return ("E" if val >= 0 else "W") + f"{abs(val):.6f}"

def square(lat: float, lon: float, half_side_m: float) -> List[Tuple[float,float]]:
    dlat, _ = dlat_dlon(lat, 0, half_side_m)
    _, dlon = dlat_dlon(lat, half_side_m, 0)
    return [(lat-dlat, lon-dlon), (lat-dlat, lon+dlon),
            (lat+dlat, lon+dlon), (lat+dlat, lon-dlon)]

def convex_hull(points: List[Tuple[float,float]]) -> List[Tuple[float,float]]:
    pts = sorted(set(points))
    if len(pts) <= 1: return pts
    def cross(o,a,b): return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])
    lower, upper = [], []
    for p in pts:
        while len(lower)>=2 and cross(lower[-2],lower[-1],p)<=0: lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper)>=2 and cross(upper[-2],upper[-1],p)<=0: upper.pop()
        upper.append(p)
    return lower[:-1]+upper[:-1]

def min_area_rect(points: List[Tuple[float,float]], inflate_m: float) -> List[Tuple[float,float]]:
    import math
    hull = convex_hull(points)
    if len(hull) < 3: return []
    lat0 = sum(p[0] for p in hull)/len(hull)
    lon0 = sum(p[1] for p in hull)/len(hull)
    R = 6371008.8; cos0 = math.cos(math.radians(lat0))
    XY=[((math.radians(lo-lon0)*R*cos0),(math.radians(la-lat0)*R)) for la,lo in hull]
    best=None
    for i in range(len(XY)):
        j=(i+1)%len(XY)
        dx,dy=XY[j][0]-XY[i][0],XY[j][1]-XY[i][1]
        ang=math.atan2(dy,dx)
        rot=[(x*math.cos(-ang)-y*math.sin(-ang),x*math.sin(-ang)+y*math.cos(-ang)) for x,y in XY]
        xs,ys=[p[0] for p in rot],[p[1] for p in rot]
        minx,maxx,miny,maxy=min(xs),max(xs),min(ys),max(ys)
        area=(maxx-minx)*(maxy-miny)
        if best is None or area<best[0]:
            best=(area,ang,minx,maxx,miny,maxy)
    _,ang,minx,maxx,miny,maxy=best
    minx-=inflate_m; maxx+=inflate_m; miny-=inflate_m; maxy+=inflate_m
    rect=[(minx,miny),(maxx,miny),(maxx,maxy),(minx,maxy)]
    def inv_rot(pt): c,s=math.cos(ang),math.sin(ang); return (pt[0]*c+pt[1]*s,-pt[0]*s+pt[1]*c)
    corners=[]
    for x,y in rect:
        xr,yr=inv_rot((x,y))
        lo=lon0+math.degrees(xr/(R*cos0)); la=lat0+math.degrees(yr/R)
        corners.append((la,lo))
    return corners

def main():
    repo_icaos=list_repo_icaos()
    if not repo_icaos:
        print("No EG** directories found."); sys.exit(0)

    airports=fetch_csv(OURAIRPORTS_AIRPORTS)
    runways=fetch_csv(OURAIRPORTS_RUNWAYS)
    core={r["ident"].upper():r for r in airports if r.get("ident")}
    OUTFILE.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTFILE,"w",encoding="utf-8",newline="\n") as fh:
        fh.write("; ------------------------------------------------------------------------------\n")
        fh.write("; AIRFIELD RADAR HOLES\n")
        fh.write("; ------------------------------------------------------------------------------\n")
        fh.write("; Generated automatically by workflows/build_airfield_radar_holes.py\n")
        fh.write("; Data source: OurAirports (CC0)\n")
        fh.write("; Each HOLE blocks Primary, Secondary, and Mode C up to (elevation + 10 ft).\n")
        fh.write("; Rectangles are derived from runway endpoints and expanded slightly.\n")
        fh.write("; Comments are ignored by the ESE compiler.\n")
        fh.write("; ------------------------------------------------------------------------------\n\n")

        count=0
        for icao in repo_icaos:
            a=core.get(icao)
            if not a or not a.get("latitude_deg") or not a.get("elevation_ft"): continue
            lat=float(a["latitude_deg"]); lon=float(a["longitude_deg"])
            elev=float(a["elevation_ft"]) + 10.0
            # collect runway endpoints
            pts=[]
            for r in runways:
                if (r.get("airport_ident") or "").upper()!=icao: continue
                for lk in ["le_latitude_deg","he_latitude_deg"]:
                    try: pts.append((float(r[lk]),float(r[lk.replace('latitude','longitude')])))
                    except: pass
            if len(pts)>=2:
                rect=min_area_rect(pts,RECT_INFLATE_M)
            else:
                rect=square(lat,lon,FALLBACK_HALF_SIDE_M)
            if not rect: continue
            fh.write(f"; {icao} — top {int(elev)} ft (ARP {lat:.6f}, {lon:.6f})\n")
            fh.write(f"HOLE:{int(elev)}:{int(elev)}:{int(elev)}\n")
            for la,lo in rect+[rect[0]]:
                fh.write(f"COORD:{hem(la,'lat')}:{hem(lo,'lon')}\n")
            fh.write("\n")
            count+=1
        print(f"Wrote {count} HOLEs to {OUTFILE}")

if __name__=="__main__":
    main()
