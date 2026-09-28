# Galaxy Forge: 50 Weapons

Engine and constraints: `00_ENGINE_PROMPT.md`. Each entry is a spec, not code. Every weapon has an **archetype** (engine primitive), a **signature twist** (the one thing nothing else does), and a **VFX identity** (palette + shape language, deliberately non-overlapping).

Tiers set the DPS budget: C common ≈ 8, R rare ≈ 14, E epic ≈ 22, M mythic ≈ 30, U ultimate (burst, ≥ 45 s cooldown).
Scope vocabulary: `iron` (open sights, no zoom), `holo` (ring reticle, 1.5x), `dot` (red-dot, 2x), `scope4`, `scope8`, `thermal` (tinted overlay + mob heat-marker particles), `rangefinder` (distance readout), `lock` (lock-on reticle), `focus` (adjustable zoom dial).

## Batch prompt template

> Read `docs/weapons/00_ENGINE_PROMPT.md` and the engine already in `packs/GalaxyForge_BP/scripts/`. Implement these weapons from `docs/weapons/WEAPONS.md`: **[ids]**. For each: def in `tools/weapons/defs/<family>.py`, held model + emissive texture + icon, particles (via templates; add a template only if none fits), sound recipe, HUD glyphs, recipe, lang, weapon-specific twist code in `archetypes/custom/<id>.js`. Follow the definition of done. Do not touch other weapons' files. Run `python3 tools/creatures/build_all.py && python3 tools/build.py` and the Node tests. Append a 30-second in-game test to `docs/weapons/TESTING.md`. Report deviations.

**Batch order** (dependencies first): A = 01 09 17 (reference) → B = 02 03 04 10 12 13 → C = 05 06 11 14 16 → D = 18-22 → E = 23-26 → F = 27-32 → G = 33-38 → H = 39-45 → I = 07 08 15 → J = 46-50.

---

## Family 1: Plasma (blue/cyan/magenta, soft orbs, ring shockwaves)

**01 `pulse_carbine` — Pulse Carbine** · C · `bolt`
3-round burst, 60 blocks/s cyan bolts, 40-block range. Alt: single tap. Scope `dot`, cyan dot.
Twist: third bolt of every burst is a larger "kicker" (+50% dmg, ring impact).
VFX: elongated cyan teardrop bolt with a fading 6-tick comet trail; hex-shaped muzzle flash; small blue ring on impact. Model: compact carbine, glowing cyan coil strip along the top.

**02 `plasma_repeater` — Plasma Repeater** · R · `bolt` (auto)
Full-auto violet bolts, heat gauge. Scope `holo`, violet ring dot.
Twist: **perfect vent**. At overheat, a 2-second vent window shows a sliding marker on the action bar; releasing use in the green zone clears heat instantly plus a 3-second damage boost.
VFX: violet bolts with dancing static arcs; vent doors on the model open with steam jets when hot. Model: boxy, exposed radiator fins that glow orange→white with heat.

**03 `plasma_scattergun` — Sticky Scattergun** · R · `bolt`
8 slow (25 b/s) magenta globs in a spread; range 20. Alt: tighter spread. Scope `iron`.
Twist: globs **stick** to the first block or mob they touch and detonate 1.5 s later, chain-detonating other stuck globs within 3 blocks.
VFX: wobbling magenta blobs with drip trails; stuck globs pulse faster as fuse ends, then pop into a star-flash + ring. Model: fat double-barrel with a glowing pink canister.

**04 `splitter_rifle` — Splitter Rifle** · E · `bolt`
Single bolt; on hit or at 12 blocks, splits into 3 homing shards (homing radius 8).
Scope `dot`, green dot; dot color turns red when a split target is available.
Twist: shards inherit the parent's remaining pierce and can re-split once on a wall bounce.
VFX: teal core bolt fractures into a fan of thin lime needles with sine-curved paths. Model: rifle with a triangular prism emitter that visibly rotates.

**05 `plasma_lance` — Plasma Lance** · E · `charge` + `hitscan`
Hold 1.2 s to charge; releases a piercing beam (range 60, pierce 5). Half-charge fires a weaker beam.
Scope `scope4`, cyan dot with ring that tightens as charge builds.
Twist: three energy rings travel down the beam after it fires and each ring applies a separate shockwave hit at the first mob it reaches.
VFX: charge phase draws 20 motes spiraling into the tip; beam is a white core with cyan sheath; rings are expanding tori. Model: long lance barrel with three floating ring emitters that spin up.

**06 `sunfire_cannon` — Sunfire Cannon** · M · `bolt` (slow) + `field`
Slow (8 b/s) golden-white plasma sphere, radius 1.2, big AoE on impact (5 blocks). 2.5 s charge.
Scope `scope4`, orange ring dot that shows AoE radius on the ground.
Twist: leaves a "sun-scar" pool for 6 s that burns anything inside; melts sand/snow/ice within 3 blocks (gated by `mobGriefing`, cap 20 blocks).
VFX: pulsing sun orb with flare spikes and orbiting sparks; impact is a white-out flash + expanding golden ring + rising heat shimmer. Model: shoulder-fired cannon with a glowing golden core cage.

**07 `ion_disruptor` — Ion Disruptor** · R · `hitscan`
Blue-static pulse; low damage. Applies Slowness III + Weakness for 4 s to mobs; vs `gx` droids/mechs/tanks: **stun** (stops AI 3 s via `gx:stunned` property/event) plus heavy damage.
Scope `holo`, electric-blue dot.
Twist: stunned machines emit a visible spark halo and take +40% damage from all sources.
VFX: jagged blue-white forked beam, crackling spheres at impact. Model: pistol with a tesla-sphere in a glass housing that flickers.

**08 `twin_photon_smg` — Twin Photon SMG** · C · `bolt` (auto)
Two barrels alternate; 12 shots/s of small yellow photon darts, short range (25).
Scope `holo`, yellow dot.
Twist: alternating barrels (visible in the model animation), and muzzle flashes alternate sides; every 12th shot is a golden tracer that pings a hit-marker with a coin sound.
VFX: yellow-white stitched dart lines; tiny sparks. Model: stubby SMG with two side-by-side barrels and a yellow ammo counter strip.

## Family 2: Laser (thin, hard-edged, saturated; long beams, mirrors)

**09 `red_dot_marksman` — Red Dot Marksman** · C · `hitscan`
Semi-auto, range 80, headshot bonus (hit above 85% of target height ×1.8). Scope `dot` 3x, always-on red dot.
Twist: dot is visible to other players and mobs of the illager family notice it (aggro on looking at it). Tracer is a 1-tick hairline.
VFX: crisp red hairline with a short glowing afterimage; tiny red starburst on hit. Model: classic marksman rifle with a visible optic whose lens glows red.

**10 `prism_beam` — Prism Beam** · E · `beam`
Channeled beam (dps 14), range 30, heat-limited.
Scope `focus` (zoom 1-4x adjusted with sneak-tap), white dot.
Twist: **refraction**. Passing through glass/ice/tinted glass blocks, the beam splits into 3 spectrum beams (red/green/blue) that fan out and each deal damage; it also stops at opaque blocks.
VFX: white beam that becomes rainbow after glass; a floating prism model piece spins. Model: crystalline rifle with a hovering prism.

**11 `helios_sniper` — Helios Sniper** · E · `hitscan` + `charge`
Bolt-action, 8x scope, hold to hold breath (sneak-hold 1 s steadies a wobbling reticle). Range 150, pierce 3 mobs, 30 dmg.
Scope `scope8` + `rangefinder`, thin green dot with distance readout.
Twist: **time-stop moment**. A kill shot beyond 60 blocks slows nearby mobs for 2 s (a kill-cam beat) and gives a cinematic vignette flash.
VFX: green needle beam with a supersonic ring that travels 10 blocks behind the bullet; shell casing particle. Model: long bolt-action with a big lens and emissive green barrel shroud.

**12 `mirror_pistol` — Ricochet Laser Pistol** · C · `hitscan`
Rapid semi-auto laser sidearm, range 30. Scope `iron`, orange dot.
Twist: **ricochet**. Beams bounce off polished blocks (iron, gold, quartz, polished stone, glass) up to 3 times, keeping 80% damage per bounce, drawing the full bounce path.
VFX: orange zig-zag beam paths with pin-point flashes at each bounce. Model: chunky retro-future pistol with a mirrored side plate.

**13 `gatling_laser` — Six-Barrel Gatling Laser** · E · `bolt`/`beam` hybrid (auto)
Spin-up 1 s; fire rate ramps from 4 to 24 shots/s; red-orange bolts. Slows the wielder (Slowness I) while spun up. Scope `holo`, red ring.
Twist: barrel-cluster rotation speed is the visible gauge; at max spin, shots become a continuous hairline beam; spin-down keeps firing for 0.5 s after releasing (momentum).
VFX: six alternating muzzle flashes in a rotating pattern, spent-heat shimmer. Model: six-barrel cluster with a rotating animation tied to spin.

**14 `tri_beam` — Focus Tri-Beam** · R · `beam`
Three parallel beams that converge at a focal distance set by scope zoom (dial with sneak-tap: 8/16/32 blocks).
Scope `focus`, three-dot triangle that merges into one when focused.
Twist: damage scales with how close the target is to the focal point (up to ×3 at focus, ×0.3 out of focus).
VFX: three thin violet beams knitting into one hot white core at the focal point, with a converging lens flare. Model: three-barrel array with a focus lens ring.

**15 `orbital_designator` — Orbital Designator** · U · `field`/`lob`
Hold the dot on a target for 2 s (lock ticks fill a reticle) → a beam from the sky slams down after 1.5 s (telegraph ring on the ground). 60 s cooldown.
Scope `rangefinder` + `lock`, red-to-white pulsing dot. Range 120.
Twist: pillar of light from above with a ground shockwave, 6-block radius, high damage (no block damage unless `mobGriefing`, cap 30 blocks).
VFX: descending ring array (concentric rings dropping down the pillar), white-out flash, dust column. Model: handheld laser designator with a fold-out antenna and a red beacon lamp.

**16 `cutter_beam` — Mining Cutter** · R · `beam` (utility)
Short-range (6) continuous beam that mines blocks slowly like a tool (respects tool-tier: diamond-level) and melts a glowing groove.
Scope `iron`, green dot marks the target block and shows a progress ring.
Twist: dig speed ramps the longer you hold the beam on the same block; ore blocks emit a bonus sparkle; mining count shown in action bar. Useful, not just combat.
VFX: thin green-white beam with sparks and glowing molten line on blocks. Model: chunky work-tool with an emissive green nozzle.

## Family 3: Fire (orange/yellow/blue flame; volume and drama)

**17 `dragon_breath_flamer` — Dragon-Breath Flamer** · R · `cone`
Continuous cone (range 9, 60° angle), ignites mobs (5 s), dps 12. Fuel gauge, 30 s of fire per cell. Scope `iron`, no dot.
Twist: heat ramps flame color orange → yellow → blue over 4 s of continuous fire, with damage ×1.5 at blue; fire briefly spreads flammable blocks only if `mobGriefing`.
VFX: layered flame billows with ember spray, heat distortion; the tank on the model's back glows with the fuel level. Model: two-hand flamethrower with a pilot flame at the nozzle.

**18 `fireball_launcher` — Fireball Launcher** · C · `lob`/`bolt`
Slow (14 b/s) fireball with slight gravity, AoE 3, ignites. Alt: triple spread.
Scope `dot`, orange dot with arc-drop pip to show gravity.
Twist: fireballs leave a burning trail for 1 s that ignites mobs walking through it; bounce once on impact with the floor.
VFX: big lumpy fireball with a smoke tail and rising embers; explosion is a fire-ring plus orange flash. Model: bulky launcher with a glowing furnace hatch.

**19 `meteor_rifle` — Meteor Caller Rifle** · E · `hitscan` + `field`
Fire a marker beam (range 90); after 1 s, 5 meteors fall in a spread over 3 s, each 4 AoE.
Scope `scope4` + `rangefinder`, orange dot with a 5-ring meteor-drop preview on the ground.
Twist: the rifle has 3 "meteor charges" that refill slowly (12 s); charges shown as three glowing chambers on the model and in the HUD.
VFX: streaking fireballs with long tails from above at angle, ember-scatter craters that glow for 3 s. Model: heavy rifle with a rotating three-chamber drum on top.

**20 `phoenix_repeater` — Phoenix Repeater** · M · `bolt` (returning)
Fires a burning phoenix-shaped projectile (range 35) that flies out, then **returns** to the shooter along a curved path, hitting on both legs.
Scope `dot`, orange-yellow dot.
Twist: catching the returning phoenix (must be within 2 blocks when it returns) heals 2 hearts and refunds the shot; missing it lets it burn out in a firework.
VFX: fiery bird silhouette made of particles with wing flap (2-frame shape swap), trailing feathers of flame; flight path swoops. Model: ornate gauntlet-rifle with a phoenix crest.

**21 `magma_mortar` — Magma Mortar** · E · `lob` + `field`
Arcing lava blobs (gravity high), AoE 4, leaves a magma pool for 5 s (fire damage, particles only; **no** lava blocks).
Scope `rangefinder`, orange arc-preview.
Twist: pools merge if blobs land within 3 blocks (radius grows, duration extends); mobs standing in a pool get "Molten" (−armor via Weakness).
VFX: viscous glowing red-orange blobs with dripping trails, bubbling pools with rising spark pops. Model: squat mortar tube with a glowing magma reservoir window.

**22 `inferno_revolver` — Inferno Revolver** · R · `hitscan`
6-shot revolver, 15 dmg each, ignites. Alt: **fan the hammer**: dump all remaining shots in 0.8 s with big spread.
Scope `iron`, thin orange dot.
Twist: reload is a spin animation with a quick-time "speedloader" bar; perfect timing gives the next cylinder an explosive round.
VFX: huge muzzle-flame with blue-white core, smoking cylinder vents after firing. Model: chunky revolver with visibly glowing chambers that dim as you fire.

## Family 4: Cryo (white/ice-blue; shards, mist, frost)

**23 `frost_lance` — Frost Lance** · R · `beam`
Short-medium beam (range 20, dps 9), applies stacking **Chill** (each 1 s of hit = +1 stack); at 5 stacks the target freezes solid (Slowness 255, 3 s).
Scope `dot`, ice-blue dot.
Twist: frozen mobs **shatter** if hit by any other damage source: large bonus damage plus an ice-burst AoE.
VFX: pale-blue beam with drifting snow motes, ice-crystal growth on mobs (spawned crystal particles at body level), shatter = glittering shard burst. Model: crystalline lance with a frost-fogged barrel.

**24 `glacier_shard_launcher` — Glacier Shard Launcher** · R · `bolt`
Fires large jagged ice shards (35 b/s, gravity low). Shards **stick** into blocks and mobs.
Scope `iron`.
Twist: after sticking, the shard grows into a 3-spike crystal cluster over 1.5 s (particles only) that slows anything within 3 blocks for 6 s.
VFX: crystal-like blue-white shard with a prismatic glint; growth is spikes of particle triangles rising with a chime. Model: rifle made of stacked ice crystals with an emissive cyan seam.

**25 `blizzard_cannon` — Blizzard Cannon** · E · `cone` (channeled)
Wide cone (range 12, 90°) of wind and snow: pushes mobs away (knockback), slows, dps 10.
Scope `iron`.
Twist: builds a "whiteout" on the wielder's screen edges (title glyph frost vignette, cosmetic) and creates a growing snowdrift of particles on the ground; the longer you fire, the more the cone widens.
VFX: swirling snow spiral, streaking ice pellets, heavy mist. Model: large barrel with a spinning turbine fan visible in the mouth.

**26 `absolute_zero_sniper` — Absolute Zero Sniper** · M · `hitscan` + `field`
Slow bolt-action, 6x scope, 20 dmg. On hit spawns a **stasis bubble** (radius 3, 3 s): all mobs inside freeze in place (Slowness 255 + no AI) with time-frozen particles.
Scope `scope8` + `thermal`, pale-cyan dot.
Twist: the bubble shows the mob's "frozen moment" with a frosted geometry shell (particle outline); shattering it (hitting any mob inside) ends stasis early with a damage multiplier for each mob.
VFX: a translucent ice sphere with drifting snowflake orbits; a low-pitched gong on hit. Model: elegant long rifle with a frost-crystal scope housing.

## Family 5: Lightning (white/yellow/electric-blue; forks, arcs, thunder)

**27 `tesla_coil_gun` — Tesla Coil Gun** · R · `chain`
Fires an arc that jumps between up to 5 targets within 6 blocks (falloff 15%/jump). Range 20 to first target.
Scope `holo`, yellow-white dot; jumps preview as faint lines to targets in range while aimed.
Twist: the coil on top spins up and stores charge; 3 shots in 2 s adds +1 jump.
VFX: forked bright arcs with jitter, small orbiting ball lightning at each target, coil sparks on the model. Model: coil-topped rifle with a visible copper spiral that glows.

**28 `storm_caller` — Storm Caller** · E · `field`
Aim at a spot (range 80): 1 s telegraph ring, then 3 lightning strikes in the area (each 6 dmg + stun, no fire) over 2 s.
Scope `scope4` + `rangefinder`, yellow ring dot showing the strike zone.
Twist: strikes prefer mobs in the zone (auto-targeting inside the circle); wet mobs (in rain/water) take +50%.
VFX: white forked bolts from above with a bright afterimage; thunder-crack (layered vanilla thunder sound with pitch shift). Model: staff-like rifle with a storm-cloud orb on the tip that swirls.

**29 `railgun_mk2` — Railgun Mk II** · M · `charge` + `hitscan`
Charge 1.5 s (coil ring particles); fires a piercing slug through mobs and up to 3 blocks of non-obsidian material (range 100, dmg 35).
Scope `scope8` + `thermal`, white-blue dot.
Twist: passing through blocks leaves a glowing tunnel scar; the shockwave ring travels along the path and knocks back everything nearby.
VFX: bright blue-white line + shock disk rings, sonic-boom double crack, lightning sparks rolling off the barrel. Model: long dual-rail rifle with glowing rails and a coil array.

**30 `volt_whip` — Volt Whip** · R · `tether`
Lightning whip, range 10. **Primary**: crack (dmg 8, stun 1 s) and pull the mob toward you. **Alt**: attach to a block and pull yourself there (grapple; cooldown 3 s).
Scope `iron`, yellow dot at the anchor.
Twist: whip crackles in an S-curve animation across its length; wraps a mob with rings of arcs.
VFX: undulating electric line with node sparks, wrap-ring at the mob. Model: hilt with a glowing coil and a floating rope-line particle in hand.

**31 `thunder_shotgun` — Thunder Shotgun** · C · `cone`
Short-range (10) burst: 6 arcs fan out; each arc 5 dmg; stuns 0.5 s. Pump action (pump animation before next shot).
Scope `iron`.
Twist: point-blank kills produce a thunder-clap that pushes back mobs within 4 blocks.
VFX: multiple forking arcs from the muzzle, yellow lightning cloud, a ring at the end. Model: pump-action shotgun with copper coils along the barrel.

**32 `glaive_disc` — Arc Glaive Thrower** · E · `bolt` (returning, bouncing)
Throws a spinning disc of lightning (range 25). Bounces between up to 4 targets, then boomerangs back.
Scope `dot`, electric-blue dot.
Twist: catch to recharge; a mid-air disc can be **re-fired**: a second use makes it split into 3 discs temporarily.
VFX: a glowing ring with jittering edge arcs, a trail of ring afterimages; blades spin. Model: launcher with a rotating disc chamber.

## Family 6: Void & Gravity (purple/black/indigo; distortion, inversions)

**33 `gravity_well_launcher` — Gravity Well Launcher** · E · `lob` + `field`
Orb thrown (range 30); on impact spawns a **singularity** for 4 s, pulling mobs and items within 6 blocks, dps 5; ends with a collapse burst (AoE 5, knockback outward).
Scope `rangefinder`, violet dot.
Twist: pulled mobs orbit the center; cancels flying mobs' hover and pulls projectiles, including your own bolts (bend them into the well).
VFX: dark sphere with an accretion ring, particles spiraling in, brief lensing flash on collapse. Model: bulbous launcher with a swirling dark orb in a glass sphere.

**34 `void_beam` — Void Beam Rifle** · E · `beam`
Channeled purple-black beam (dps 16), range 25.
Scope `holo`, black dot with a violet halo.
Twist: hit targets accumulate **Void Marks** (visible rings). At 4 marks, they're pulled into a rift for 1 s and released with heavy damage.
VFX: dark beam with inverted-color ripples ("void" shimmer), mark rings around the target's head. Model: matte-black rifle with an emissive violet slit.

**35 `blink_rifle` — Blink Rifle** · R · `bolt` (teleport)
Fires a violet orb (range 40). **Primary**: teleports you to the impact point (safe-location check). **Alt**: swap positions with the mob hit.
Scope `dot`, purple dot marks the landing point.
Twist: 5-second cooldown; you get a brief after-image trail. Won't teleport into blocks or the void; safe-spot search within 2 blocks.
VFX: starburst at the origin and at the arrival, an afterimage streak between, dimensional slice lines. Model: sleek rifle with a floating ring that spins on fire.

**36 `umbra_smg` — Umbra SMG** · R · `bolt` (auto, silent)
Silent (no fire sound, only a faint hiss), dark bolts with no visible muzzle flash.
Scope `holo`, faint violet dot.
Twist: **Shadow Mark**. Hits mark a target; 5 marks on the same mob detonate them in a shadow burst (AoE 3, dmg 12).
VFX: near-invisible tracer, shadow tendrils curling from marked mobs, a burst of dark shards on detonation. Model: matte suppressed SMG with a subtle purple edge glow.

**37 `black_hole_cannon` — Black Hole Cannon** · U · `bolt` (slow) + `field`
5 s charge (screen darkens at the edges); fires a slow black hole (4 b/s) that swallows mobs, pulls them, dealing a burst of damage in the center. 60 s cooldown.
Scope `scope4`, violet dot.
Twist: swallows projectiles, and **pulls nearby loose items** toward it; collapses with a bright white flash and shockwave ring.
VFX: black sphere with a bright accretion ring tilted, gravitational lensing simulated with a shimmering distortion of particles, star streaks stretched toward the center. Model: massive shoulder cannon, exposed swirling emissive core.

**38 `repulsor_gauntlet` — Repulsor Gauntlet** · R · `cone` (shockwave)
Palm blast: short-range shockwave cone (range 8), heavy knockback, dmg 6. **Alt**: fire at the ground for a **rocket-jump** (launch yourself up).
Scope `holo` (palm targeting ring).
Twist: charge (hold) up to 1 s for larger cone and more force; ground-slam blast when fired downward while airborne pushes everything around you.
VFX: expanding translucent rings (repeated 3 in a row), floor dust ring, air-warp shimmer. Model: armored gauntlet with a glowing circular palm emitter.

## Family 7: Bio & Nano (acid green/toxic yellow/organic; splatter and swarm)

**39 `acid_sprayer` — Acid Sprayer** · C · `cone`
Short-range green spray (range 8), applies **Corrode** (Weakness + Poison-lite 4 s, stacking 3×).
Scope `iron`.
Twist: puddles remain on the ground for 4 s (particles only) that apply Corrode to any mob entering them; corroded mobs' armor value visibly drips.
VFX: viscous lime spray with bubbling droplets, sizzling puddles with rising vapor. Model: bulbous tank sprayer with a glowing acid vial.

**40 `spore_launcher` — Spore Launcher** · R · `lob`
Fires a pulsing spore pod (range 25) that bursts into a poison cloud for 5 s (radius 3), and spawns 3 homing spore darts that chase nearby mobs.
Scope `dot`, yellow-green dot.
Twist: mobs killed inside the cloud spawn a small mushroom-puff (particles + XP bonus).
VFX: soft glowing spore clouds with drifting motes, tiny fungal blooms (particle) on impact. Model: organic launcher with a bioluminescent mushroom pod on top.

**41 `nanite_swarm_rifle` — Nanite Swarm Rifle** · E · `bolt` (swarm)
Fires a cloud of ~20 tiny particles (single logical projectile) that fly with flocking motion, homing on the nearest target (range 30) and dealing tick damage while attached.
Scope `lock`, silver dot; lock ticks over the target.
Twist: after killing a target, the swarm re-seeks another within 8 blocks (up to 3 targets) before dissolving.
VFX: silver-teal glinting motes forming a shifting shape, sparkle trail, a metallic hiss sound. Model: sleek white-and-teal rifle with a honeycomb magazine.

## Family 8: Sonic, Missile, Drone (kinetic/support)

**42 `sonic_cannon` — Sonic Cannon** · R · `cone`
Charge-and-release wave (range 15, 45° cone): dmg 10, stun 1.5 s, knockback. Shatters glass in the cone (gated by `mobGriefing`, cap 12).
Scope `iron`.
Twist: the wave is drawn as concentric expanding arcs that ripple and refract through the terrain; hits arrive delayed by distance (visible wave speed), so you can lead targets.
VFX: white-teal arc bands that stretch and fade, ground ripples. Model: horn-shaped cannon with a vibrating emitter plate.

**43 `seeker_rack` — Seeker Missile Rack** · E · `lob`/`bolt` (homing)
Hold aim on mobs to lock up to 4 (lock time 0.6 s each); release to fire 4 homing missiles, 8 dmg each, AoE 2. Range 60.
Scope `lock` + `rangefinder`, red brackets on locked targets.
Twist: missiles arc up then dive; hitting a wall triggers a proximity detonation instead of a dud.
VFX: white smoke trails with orange nozzle glow, tiny fins visible as a particle cross, a bright pop with a smoke ring. Model: shoulder-mounted 4-tube rack with hinged covers that pop open.

**44 `drone_launcher` — Combat Drone Launcher** · E · `deploy`
Launches a hovering drone that orbits you for 20 s and shoots small lasers at hostile mobs within 12 blocks (dps 6). Max 2 active.
Scope `holo`, blue dot: aim the dot at a mob to **order the drone to focus** it.
Twist: the drone returns and docks when the timer ends (and a cell is refunded if it survived); it can be shot down by mobs.
VFX: small emissive quad-rotor with a rotating blade animation, a blue targeting line to its target. Model: handheld launcher with a folded drone visible in the tube. New entity `gx:combat_drone`.

**45 `sentinel_kit` — Sentinel Turret Kit** · E · `deploy`
Places a 1-block auto-turret (health 20, dps 8, range 16, 30 s life). Max 2 active. Never targets pups, tamed mobs, or players.
Scope `iron`, green dot for placement preview (a hologram ghost outline).
Twist: turrets that share line-of-sight sync fire for a bonus; the hologram placement preview shows their range circle.
VFX: unfolding tripod animation, a green scanning cone particle, sparks as it fires. Model: chunky briefcase-style kit that opens. New entity `gx:sentinel_turret`.

## Family 9: Cosmic & Mythic (the showpieces: layered palettes, biggest VFX budget)

**46 `aurora_lance` — Aurora Lance** · M · `beam`
Rainbow beam (range 40); every second, it cycles element: fire (ignite) → ice (slow) → shock (stun) → toxic (poison).
Scope `focus`, dot color follows the current element.
Twist: switching element visibly recolors the model's aurora ribbons and the beam; combos: fire→ice hits shatter, ice→shock hits arc to nearby targets.
VFX: undulating curtain-like beam with ribbon shimmer, floating aurora particles above the wielder while aiming. Model: sleek lance with three emissive ribbon inlays.

**47 `supernova_rifle` — Supernova Rifle** · U · `charge` + `field`
3 s overcharge. Fires a white slug that detonates at range (or on impact) as a **supernova**: white-out, expanding double ring, radius 10, heavy damage; 60 s cooldown.
Scope `scope4`, white-gold dot with a big blast radius preview ring on the ground.
Twist: a brief **screen flash** and 2 s of sound ducking for the wielder; damage falls off with distance from the center and knocks back everything outward.
VFX: a star with lens spikes, an outward nebula ring of orange/magenta/blue, remaining sparkle dust for 3 s. Model: ornate rifle with a floating star core in an open lattice.

**48 `starforge_bow` — Starforge Bow-Gun** · M · `bolt` (nodes)
Fires star-tipped arrows that stick where they land, becoming **constellation nodes** (lifetime 8 s).
Scope `scope4`, gold dot.
Twist: when 3+ nodes exist, lines connect them and a triangle field forms between them dealing damage to mobs inside (dps 10); nodes beyond 5 recycle the oldest. Diagrams visible in the sky-glow.
VFX: gold star-glint arrow trails, luminous lines between nodes with a twinkling field fill. Model: recurve bow-rifle with a starlit limb and floating orbs.

**49 `chrono_pistol` — Chrono Pistol** · M · `hitscan`
Shot tags a target (range 40) and records its position each tick for 3 s. **Alt-fire**: rewind the target to where it was 3 s ago (a visible trail plays back), dealing damage proportional to distance traveled.
Scope `dot`, teal-gold dot with an hourglass reticle that empties as the tag expires.
Twist: rewinding replays the recorded path as a visible streak while the mob is teleported back (safe-location check; skip if the spot is now inside a block). If teleporting mobs proves unreliable on stable APIs, deal the damage and play the streak only, and note it in `DEVIATIONS.md`.
VFX: teal-gold clock-face ring appears around tagged mobs, a rewind streak of afterimages, tick-tock sound. Model: brass pocket-watch pistol with a visible spinning gear cluster.

**50 `good_boy_cannon` — Good Boy Cannon** · M · `bolt` + `field`
Fires glowing **paw-print star** bolts (range 40). Hostile mobs take damage (dps budget M). **Tamed `galaxy:pup`** hit by a bolt is healed, gets Speed + Strength for 10 s, and does a happy tail-wag/jump.
Scope `dot`, pink dot; aiming at your pup shows a heart marker.
Twist: hold sneak + fire to launch a **bone-shaped starburst** that calls every tamed pup within 30 blocks to your position (they teleport-dash with a stardust trail).
VFX: pink-gold paw stamps that leave trailing stardust, heart particles on heals, bark sound (vanilla wolf pitch-shifted) on fire. Model: chunky blaster with a paw-shaped muzzle and a glowing bone ornament. This one is Parker's dog's weapon; make it the best-looking of all 50.

---

## Roster check (engine uses this to verify uniqueness)
Palettes are non-overlapping per family, but same-family weapons must differ in **shape language**: bolt (teardrop, dart, glob, needle, disc, orb), beam (hairline, sheath, triple, prism, ribbon), cone (billow, spray, wave, snow). The engine's `build_weapons.py` should fail if two weapons share the same `(palette, projectile_shape, muzzle_shape)` tuple.
