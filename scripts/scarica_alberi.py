"""Scarica il censimento degli alberi del Comune di Trento dal WMS pubblico del webGIS.

Il WFS del progetto "020_Verde" non espone layer: si interroga il layer `Alberi` con
GetFeatureInfo (WITH_GEOMETRY=true) a tasselli di 1,6 km e si uniscono i risultati,
eliminando i duplicati per `ogc_fid`.
Output: data/alberi_trento.geojson (coordinate WGS84)

Uso: python3 scripts/scarica_alberi.py
Fonte: Comune di Trento – https://gis.comune.trento.it/mobile/tn/?verde
(licenza da verificare con infogis@comune.trento.it)
"""

import json
import math
import time
import urllib.parse
import urllib.request
from pathlib import Path

WMS_URL = "https://gis.comune.trento.it/ows/mobile-l2l/qdjango/22/"
LAYER = "Alberi"
TILE = 1600  # metri
# Estensione del Comune di Trento in EPSG:25832 (UTM 32N), con margine
X_MIN, X_MAX = 654000, 674000
Y_MIN, Y_MAX = 5092000, 5112000
PAUSA = 0.5  # secondi tra le richieste, per non sovraccaricare il server

OUT = Path(__file__).resolve().parent.parent / "data" / "alberi_trento.geojson"


def utm32_to_wgs84(x, y):
    """Conversione UTM zona 32N (ETRS89 ≈ WGS84) -> lon, lat in gradi."""
    a, f, k0 = 6378137.0, 1 / 298.257223563, 0.9996
    e2 = f * (2 - f)
    ep2 = e2 / (1 - e2)
    x -= 500000.0
    m = y / k0
    mu = m / (a * (1 - e2 / 4 - 3 * e2**2 / 64 - 5 * e2**3 / 256))
    e1 = (1 - math.sqrt(1 - e2)) / (1 + math.sqrt(1 - e2))
    phi1 = (mu + (3 * e1 / 2 - 27 * e1**3 / 32) * math.sin(2 * mu)
            + (21 * e1**2 / 16 - 55 * e1**4 / 32) * math.sin(4 * mu)
            + (151 * e1**3 / 96) * math.sin(6 * mu))
    n1 = a / math.sqrt(1 - e2 * math.sin(phi1) ** 2)
    t1 = math.tan(phi1) ** 2
    c1 = ep2 * math.cos(phi1) ** 2
    r1 = a * (1 - e2) / (1 - e2 * math.sin(phi1) ** 2) ** 1.5
    d = x / (n1 * k0)
    lat = phi1 - (n1 * math.tan(phi1) / r1) * (
        d**2 / 2 - (5 + 3 * t1 + 10 * c1 - 4 * c1**2 - 9 * ep2) * d**4 / 24
        + (61 + 90 * t1 + 298 * c1 + 45 * t1**2 - 252 * ep2 - 3 * c1**2) * d**6 / 720)
    lon = (d - (1 + 2 * t1 + c1) * d**3 / 6
           + (5 - 2 * c1 + 28 * t1 - 3 * c1**2 + 8 * ep2 + 24 * t1**2) * d**5 / 120) / math.cos(phi1)
    return round(9 + math.degrees(lon), 7), round(math.degrees(lat), 7)


def interroga_tassello(x0, y0):
    half = TILE // 2
    params = {
        "SERVICE": "WMS",
        "VERSION": "1.3.0",
        "REQUEST": "GetFeatureInfo",
        "LAYERS": LAYER,
        "QUERY_LAYERS": LAYER,
        "CRS": "EPSG:25832",
        "BBOX": f"{x0},{y0},{x0 + TILE},{y0 + TILE}",
        "WIDTH": TILE,
        "HEIGHT": TILE,
        "I": half,
        "J": half,
        "FEATURE_COUNT": 100000,
        "INFO_FORMAT": "application/json",
        "FI_POINT_TOLERANCE": int(half * 1.45),  # raggio che copre anche gli angoli del tassello
        "WITH_GEOMETRY": "true",
    }
    url = WMS_URL + "?" + urllib.parse.urlencode(params)
    for tentativo in range(3):
        try:
            with urllib.request.urlopen(url, timeout=180) as r:
                return json.load(r).get("features", [])
        except Exception as e:
            print(f"  errore ({e}), riprovo...")
            time.sleep(3 * (tentativo + 1))
    return []


def main():
    alberi = {}
    xs = range(X_MIN, X_MAX, TILE)
    ys = range(Y_MIN, Y_MAX, TILE)
    totale = len(xs) * len(ys)
    n = 0
    for x0 in xs:
        for y0 in ys:
            n += 1
            feats = interroga_tassello(x0, y0)
            for f in feats:
                p = f["properties"]
                if not f.get("geometry"):
                    continue
                x, y = f["geometry"]["coordinates"][:2]
                p["x_utm32"], p["y_utm32"] = x, y
                alberi[p["ogc_fid"]] = {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": list(utm32_to_wgs84(x, y))},
                    "properties": p,
                }
            print(f"[{n}/{totale}] tassello {x0},{y0}: {len(feats)} alberi (totale unici {len(alberi)})")
            time.sleep(PAUSA)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"type": "FeatureCollection", "features": list(alberi.values())}, ensure_ascii=False))
    print(f"Salvati {len(alberi)} alberi in {OUT}")


if __name__ == "__main__":
    main()
