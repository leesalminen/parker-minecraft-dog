# Galaxy vehicles: car, plane, helicopter

| Entity | Spawn egg | Seats | Native driving component |
|---|---|---|---|
| `gx:car` Galaxy Cruiser Car | yes (auto) | 4 | `minecraft:input_ground_controlled` |
| `gx:plane` Sky Pup Plane | yes | 2 (tandem) | `minecraft:input_air_controlled` |
| `gx:helicopter` Galaxy Rescue Copter | yes | 2 (side by side) | `minecraft:input_air_controlled` |

Sources: `tools/creatures/specs/vehicles_{car,plane,helicopter}.py` (models, textures, animations, base entity),
`vehicles_common.py` (shared painters), `tools/creatures/extras/vehicles_patch.py` (post-processes the generated
entity JSON: strips mob AI, adds damage immunity), `packs/GalaxyForge_BP/scripts/vehicles.js` (runtime behaviour,
imported once from `main.js`). Rebuild with `python3 tools/creatures/build_all.py car plane helicopter`.

All three are immune to fall, wall-crash, contact, suffocation, drowning, fire, lava and explosion damage, never
attack, never wander and never look at players. Only direct attacks can hurt them (60 hp), so they can still be
removed.

## Controls (kid version)

- **Car:** look to steer, hold W to drive. The jump key does nothing (no horse hop). Hills, steps and mounds are
  handled automatically.
- **Plane:** hold W for speed, look where you want to go. Look up a bit on the ground to roll and take off. Once
  airborne it keeps a slow cruise even with no key held, so it can't stall. Nose up climbs, nose down dives, level
  holds altitude. Landing is soft; nothing damages you.
- **Helicopter:** W flies forward, look to turn (head look is free; `tickHeli` swings the airframe toward the pilot yaw). Hovers on its own. Look steeply up (past 30 degrees) to climb,
  steeply down (past 45 degrees) to descend; the jump key also climbs when the API reports it. It slows to a gentle
  touch-down within 2 blocks of the ground. Rotors spin fast while someone is aboard.
- Empty planes and helicopters settle to the ground on their own.

## The car and hills (the hard part)

### What Bedrock gives us

Bedrock has no step-height component that works for a ridden non-horse entity (`variable_max_auto_step` is not used
here because an unknown or unsupported component would stop the whole entity loading and it cannot be tested
offline). The vanilla answer is the horse jump, which is exactly the "hopping" we want to avoid. Manifest API is
`@minecraft/server` 1.11.0: `applyImpulse`, `clearVelocity`, `getVelocity`, `teleport`, `isOnGround`,
`getBlock`, `getBlockFromRay`, no `setVelocity`. So the only way to move an entity vertically without a visible pop
is impulses that shape its vertical velocity; teleporting up by small amounts is kept only as a stuck safety net.

### Approach (`tickCar` in vehicles.js)

Native movement (W, mouse yaw) is untouched. Each tick, for a car with a rider only:

1. **Heading**: velocity direction, or the nose direction when nearly stopped.
2. **Scan terrain ahead**: columns at 1-block spacing to the sides near the car and at 0.5-block spacing ahead up to 10
   blocks. For each column a downward scan finds the highest surface that has 2 free blocks above it (so tree
   canopies and cave roofs are ignored) and is no more than 3 blocks above the car (taller means wall: ignored).
   Bottom slabs count as half a block. Columns are cached for 25 ticks.
3. **Ramp target**: `target = max over samples of (surface - slope * max(0, distance - halfWidth - lead))`. This is a
   virtual ramp with slope 0.4 (about 22 degrees) that reaches full height `halfWidth + lead` (about 2 blocks) before
   the nose touches the step. Height under the car itself (`distance 0`) must always be met.
4. **Vertical velocity control**: if the car is below the target, command a climb speed
   `min(ramp feed-forward + 0.5 * error, braking curve sqrt(2 * slew * error), 0.35)`, with the change per tick
   limited to 0.06 (jerk limit), applied as an impulse that also cancels that tick's gravity. At the crest the climb
   speed eases out instead of stopping, so there is no hop off the top.
5. **Down**: when the ground falls away the car sinks at most 0.16 blocks/tick instead of free-falling.
6. **Momentum**: while the script carries the car in the air, small horizontal impulses stop it losing speed
   (ground-controlled entities have weak air control).
7. **Safety net**: pressed against a step with no speed and no rise for 6 ticks, teleport up 0.2 blocks per tick.

A Node harness with a stub world and a toy physics loop (auto-step 0.6, gravity 0.08, 0.98 drag) was used to tune
this. Results for a car driving at 0.4 blocks/tick: 1-block step, 2-block step, 3-block mound, 1-block bump, 4-stair
staircase all crossed with max rise 0.17 to 0.24 blocks per tick, one direction reversal on mounds (up then down),
no stall. 4-block wall correctly stops it. Without the script the same car stops at each step.

### Limits

- **Untested in Minecraft.** The physics numbers (gravity 0.08, air control, how ridden `input_ground_controlled`
  entities respond in the air) are assumptions. All tunables are in `CFG` at the top of `vehicles.js`; if the car
  feels floaty raise `slew`, if it lags behind slopes raise `lead` or lower `slope`.
- The ramp is planned from block columns, not exact collision shapes. Stairs are treated as full blocks (car rides a
  little high over them), fences and walls are treated as full-height solids, non-solid plants use a name list only
  when `Block.isSolid` is unavailable.
- Rises above 3 blocks are walls. Very fast driving (over about 0.5 blocks/tick) outruns the ramp; the safety net and
  vanilla step then take over and may pop.
- Cost is about 30 to 60 `getBlock` calls per ridden car per tick, before the cache. Only ridden cars are processed.
- Multiplayer: nothing is client-authoritative. A laggy connection shows the car with the usual entity interpolation,
  which smooths the climb but can add latency to it.

## Aircraft (`tickPlane`, `tickHeli`)

Both are `hover` entities with `input_air_controlled`, so W moves them along the look direction. The script then:

- **Plane:** swings velocity toward the look direction (banking turns), adds a minimum cruise thrust when airborne,
  maps pitch to climb rate (level holds altitude), sinks softly if it ever drops below stall speed, caps descent near
  the ground (flare), and does a ground roll plus rotation when the pilot looks up. The plane learns whether the
  engine applies gravity to it (`holdVy`) instead of assuming.
- **Helicopter:** takes over vertical speed (hover by default, climb / descend by look angle), adds horizontal drag so it
  stops when W is released, and lands slowly.

Limits: whether W moves a ridden `hover` entity in full 3D is the main unverified assumption. If W only moves it
horizontally, the plane still takes off (look up on the ground) and cruises; the helicopter still climbs and
descends by look angle. The pilot is the first rider only.

## v1.8: starfighters, rocket, space suit, troopers

| Entity | Notes |
|---|---|
| `gx:x_wing` X-Wing Starfighter | 1 seat, S-foils spread when boarded, 4 wingtip cannons (red bolts) |
| `gx:tie_fighter` Twin-Ion Fighter | 1 seat inside an open spoke-frame pod (wide view), 2 chin cannons (green bolts) |
| `gx:rocket` Galaxy Rocket | 2 seats, 360-degree glass cabin; jump = full thrust, look steeply down = descend, ceiling y=316 |

- Fighters use the plane flight model with `CFG.fighter` (fast, VTOL lift-off: look up on the ground). Fire with
  **hold JUMP, or click/punch**. Bolts are the weapon engine's script projectiles (`tickGuns` in `vehicles.js`; bolt.js
  draws a streak when `def.vfx.streak`). Muzzle offsets are in `SHIPS`; if they don't line up with the barrels after a
  model change, edit them there.
- Space = overworld y >= 240 (`scripts/space.js`). Without all four `gx:space_*` pieces: 2 damage/second and a warning.
  Suited: slow falling, jump boost, night vision, resistance. Suit is craftable from iron ingots (+ glass for the helmet).
- Troopers: `stormtrooper`, `sandtrooper`, `scout_trooper` (hostile, shoot red bolts, also hunt clones);
  `clone_trooper`, `clone_commander`, `clone_heavy` (tame with cooked beef / bread / porkchop; shoot monsters and
  imperials, defend their owner). Bolts are `gx:blaster_bolt_{red,blue}` (`extras/troopers_patch.py`).
- Untested in-game: seat/eye heights (`ride.seats` y), bolt model axis, and jump-as-fire. Tunables: `SHIPS`, `CFG`.
