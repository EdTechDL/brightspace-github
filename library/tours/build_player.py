#!/usr/bin/env python3
"""Inline a tour JSON file into the player template so the result opens offline by double-click.

Usage: python3 build_player.py <tour.json> <out.html>
"""
import json, sys, pathlib

here = pathlib.Path(__file__).parent
tour_path = pathlib.Path(sys.argv[1])
out_path = pathlib.Path(sys.argv[2])
tour = json.loads(tour_path.read_text(encoding="utf-8"))
# sanity checks: every step's screen exists and every extends resolves
screens = tour["screens"]
for sid, s in screens.items():
    if "extends" in s and s["extends"] not in screens:
        sys.exit(f"screen {sid} extends unknown screen {s['extends']}")
for st in tour["steps"]:
    if st["screen"] not in screens:
        sys.exit(f"step {st['id']} uses unknown screen {st['screen']}")
    if st.get("next") and st["next"] not in screens:
        sys.exit(f"step {st['id']} points to unknown next screen {st['next']}")
html = (here / "player-template.html").read_text(encoding="utf-8")
payload = json.dumps(tour, ensure_ascii=False).replace("</script", "<\\/script")
html = html.replace("/*__TOUR_JSON__*/ null", payload, 1)
out_path.write_text(html, encoding="utf-8")
print(f"built {out_path} with {len(tour['steps'])} steps and {len(screens)} screens")
