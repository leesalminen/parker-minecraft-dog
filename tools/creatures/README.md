# Creature spec format
Each `specs/<name>.py` exports `SPEC` (dict) or `SPECS` (list). `python3 tools/creatures/build_all.py [id...]` regenerates
everything into packs/GalaxyForge_{BP,RP}. `python3 tools/creatures/preview.py <module> out.png` renders a 4-view sheet.

```python
from lib import *
SPEC = {
  "id": "sabertooth",              # -> entity gx:sabertooth, files gx_sabertooth.*
  "name": "Glacier Sabertooth",
  "egg": ("#d9e6f2", "#3a5a7a"),
  "glow": False,                   # True if any texel uses glow(...)
  "scale": 1.0, "visible": [w, h, y_offset],   # visible bounds (blocks); must cover the whole model or it culls
  "bones": [ {"name": "body", "parent": None, "pivot": [x,y,z], "rotation": [rx,ry,rz]?,
              "cubes": [ {"o": [x,y,z], "s": [w,h,d]  (INT sizes), "skin": "fur", "inflate": 0.25?, "rot": [..]?, "pivot": [..]?} ]} ],
            # parents must be listed before children. Model faces -Z. 1 unit = 1/16 block. Ground is y=0.
            # NEVER use "mirror": every cube gets unique UVs; write both sides as separate cubes.
  "skins": { "fur": fn(p) -> colour|None, "default": fn },   # skin lookup: cube["skin"] -> bone name -> "default"
  "anims": { "walk": anim({...bones...}) },   # see lib helpers: quad_walk, biped_walk, hex_walk, sway, bob, flap, merge, anim
  "play":  [ ("walk", "query.modified_move_speed > 0.02"), "idle" ],   # entries: name or {name: molang}
  "behavior": {...},               # see lib.build_behavior
}
```
Painter `fn(p)`: p.face, p.x, p.y, p.fw, p.fh, p.w, p.h, p.d, p.p (model-space xyz of texel: use for continuous noise/stripes
across cubes), p.rng. Return `"#rrggbb"`, `(r,g,b)`, `glow(color)` for emissive, or None for transparent.
Helpers: rgb shade(c,f) mix(a,b,t) noise3(x,y,z,seed,scale) hash01.

Behavior keys: role (hostile|boss|neutral|passive|companion|mount), health, speed, damage, box [w,h] (blocks), knockback_resist,
family [..], fly, hover, climb, ranged(+range), ride {"seats": [[x,y,z]...] in blocks}, spawn {"biomes":[tags],"weight","herd":[a,b]},
loot [(item,min,max)], sound ("zombie"|"golem"|... or (name,[pitchlo,pitchhi])), xp, tame_items (companion), fire_immune, boss.
