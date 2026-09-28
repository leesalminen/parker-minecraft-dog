# Galaxy Forge — in-game test checklist

Generated from the roster by `tools/weapons/build_weapons.py`; regenerate with
`python3 tools/creatures/build_all.py`. Each entry is a 30-second check.

Before the first weapon: give yourself `gx:energy_cell` x64 and every weapon
(`/give @s gx:pulse_carbine` …), then in a flat world:

1. Sneak to aim — the scope overlay and laser dot appear, action bar shows the readout.
2. Fire — the weapon fires, bolts/beams/particles render, mobs take damage.
3. Hit your `galaxy:pup` and a tamed wolf — neither takes damage.
4. Empty the magazine, then press use — it reloads from an energy cell.

## Roster

### Acid Sprayer (`gx:acid_sprayer`) — common, cone
- Scope: open sights (no zoom); dot dot `#7cff3a`.
- 30s test: Hold use: 55-degree cone, 8 blocks, 8 dps.
- Twist: Every spray coats mobs in Corrode (Weakness + Poison-lite) and leaves a lingering acid puddle that corrodes anything walking into it.
- Ammo: cell, mag 10.

### Spore Launcher (`gx:spore_launcher`) — rare, lob
- Scope: red-dot (2x); dot dot `#d6ff3a`.
- 30s test: Press use: arc at 16 b/s, AoE 3; watch the glob lob and its landing ring.
- Twist: The pod bursts into a 5 s poison cloud and throws three homing spore darts that chase nearby mobs.
- Ammo: cell, mag 5.

### Nanite Swarm Rifle (`gx:nanite_swarm_rifle`) — epic, bolt
- Scope: lock-on reticle; dot dot `#c8d8e0`.
- 30s test: Hold use (one shot per press): 1x plume at 30 b/s, muzzle hive, impact gx:spark_burst.
- Twist: The nanite cloud flocks toward the nearest mob, re-seeks the next one after each kill, and dissolves after three targets.
- Ammo: cell, mag 20.

### Aurora Lance (`gx:aurora_lance`) — mythic, beam
- Scope: zoom dial; dot dot `#ffd45a`.
- 30s test: Hold use: channel 30 dps over 40 blocks; heat climbs, release to stop.
- Twist: Every second the beam cycles fire -> ice -> shock -> toxic, recolouring the beam and applying that element's status; fire into ice shatters and ice into shock arcs to nearby mobs.
- Ammo: heat; heat 100.

### Supernova Rifle (`gx:supernova_rifle`) — ultimate, charge
- Scope: 4x scope; dot dot_ring `#fff2c0`.
- 30s test: Hold 3.0s then release: 3 tiers, mode bolt.
- Twist: A 3 s overcharge fires a white slug that detonates as a supernova (radius 10, distance falloff, outward knockback, collapsing field) on a 60 s cooldown, with a white screen flash and 2 s of sound ducking.
- Ammo: cell, mag 1.

### Starforge Bow-Gun (`gx:starforge_bow`) — mythic, bolt
- Scope: 4x scope; dot dot `#ffd45a`.
- 30s test: Hold use (one shot per press): 1x star at 55 b/s, muzzle bow_limb, impact gx:crystal_burst.
- Twist: Arrows stick where they land as constellation nodes (8 s); 3 or more nodes draw luminous lines and form a star field dealing 10 dps to mobs inside, recycling the oldest past five.
- Ammo: cell, mag 6.

### Chrono Pistol (`gx:chrono_pistol`) — mythic, hitscan
- Scope: red-dot (2x); dot dot_cross `#4affd8`.
- 30s test: Press use: 12 dmg per shot at 40 blocks, 8-tick cadence. Watch the hex tracer and gear muzzle flash, then the gx:ring_wave impact.
- Twist: A hit tags the target for 3 s, recording its position every tick; sneak-fire rewinds it to where it stood, dealing damage proportional to the distance travelled (a failed teleport still lands the damage and the streak).
- Ammo: cell, mag 12.

### Good Boy Cannon (`gx:good_boy_cannon`) — mythic, bolt
- Scope: red-dot (2x); dot dot `#ffd7ea`.
- 30s test: Hold use (one shot per press): 1x paw at 50 b/s, muzzle paw_muzzle, impact gx:star_flash.
- Twist: Paw bolts heal a tamed galaxy:pup and grant Speed + Strength for 10 s; sneak-fire launches a bone starburst that teleport-dashes every tamed pup within 30 blocks to your side.
- Ammo: cell, mag 8.

### Frost Lance (`gx:frost_lance`) — rare, beam
- Scope: red-dot (2x); dot dot `#bfe6ff`.
- 30s test: Hold use: channel 14 dps over 20 blocks; heat climbs, release to stop.
- Twist: The beam stacks Chill once per second of contact; at five stacks the target freezes solid (Slowness 255 for 3 s) and shatters in a crystal burst.
- Ammo: heat; heat 100.

### Glacier Shard Launcher (`gx:glacier_shard_launcher`) — rare, bolt
- Scope: open sights (no zoom); dot dot `#9fe0ff`.
- 30s test: Hold use (one shot per press): 1x shard at 35 b/s, muzzle crystal, impact gx:crystal_burst.
- Twist: Shards stick into whatever they hit, then fuse into a 3-spike crystal cluster that slows every mob within 3 blocks for 6 s.
- Ammo: cell, mag 6.

### Blizzard Cannon (`gx:blizzard_cannon`) — epic, cone
- Scope: open sights (no zoom); dot dot `#dff4ff`.
- 30s test: Hold use: 90-degree cone, 12 blocks, 22 dps.
- Twist: The longer you channel, the wider the cone: a whiteout frosts the screen edges, a snowdrift piles up, and mobs are pushed further and further away.
- Ammo: heat; heat 100.

### Absolute Zero Sniper (`gx:absolute_zero_sniper`) — mythic, hitscan
- Scope: thermal tint; dot dot `#bfe6ff`.
- 30s test: Press use: 20 dmg per shot at 100 blocks, 14-tick cadence. Watch the star tracer and frost_scope muzzle flash, then the gx:shock_disc impact.
- Twist: A hit seals mobs in a stasis bubble; hitting any mob inside shatters it early for bonus damage scaled by how many mobs are trapped.
- Ammo: cell, mag 4.

### Dragon-Breath Flamer (`gx:dragon_breath_flamer`) — rare, cone
- Scope: open sights (no zoom); dot dot `#ff6a1a`.
- 30s test: Hold use: 60-degree cone, 9 blocks, 14 dps.
- Twist: Continuous fire ramps the flame orange to yellow to blue over 4 s, and at blue the cone deals x1.5 damage while the tank gauge drains.
- Ammo: heat; heat 100.

### Fireball Launcher (`gx:fireball_launcher`) — common, lob
- Scope: red-dot (2x); dot dot `#ff8a1a`.
- 30s test: Press use: arc at 14 b/s, AoE 3; watch the glob lob and its landing ring.
- Twist: Fireballs leave a 1 s burning trail that scorches anything crossing it and bounce once off the floor, while sneak-fire throws a triple spread.
- Ammo: cell, mag 8.

### Meteor Caller Rifle (`gx:meteor_rifle`) — epic, hitscan
- Scope: 4x scope; dot dot_ring `#ff5a12`.
- 30s test: Press use: 4 dmg per shot at 90 blocks, 40-tick cadence. Watch the shard tracer and drum muzzle flash, then the gx:debris_burst impact.
- Twist: Three meteor charges refill one every 12 s, and each shot paints a marker beam that 1 s later brings five meteors down over 3 s, each a 4-block crater.
- Ammo: heat.

### Phoenix Repeater (`gx:phoenix_repeater`) — mythic, bolt
- Scope: red-dot (2x); dot dot `#ffb02b`.
- 30s test: Hold use (one shot per press): 1x plume at 40 b/s, muzzle crest, impact gx:star_flash.
- Twist: The phoenix flies out 35 blocks then curves back to the shooter, and catching it within 2 blocks heals 2 hearts and refunds the shot.
- Ammo: cell, mag 8.

### Magma Mortar (`gx:magma_mortar`) — epic, lob
- Scope: distance readout; dot dot `#ff4a10`.
- 30s test: Press use: arc at 12 b/s, AoE 4; watch the glob lob and its landing ring.
- Twist: Blobs landing within 3 blocks of an existing pool grow it (+1 radius, +4 s) instead of stacking a second one, and mobs in a pool get Molten.
- Ammo: cell, mag 6.

### Inferno Revolver (`gx:inferno_revolver`) — rare, hitscan
- Scope: open sights (no zoom); dot dot `#ff5a20`.
- 30s test: Press use: 15 dmg per shot at 32 blocks, 20-tick cadence. Watch the dart tracer and cylinder muzzle flash, then the gx:spark_burst impact.
- Twist: Sneak-fire fans the hammer to empty the cylinder in 0.8 s with wide spread, and a speedloader press in the green window loads an explosive round.
- Ammo: cell, mag 6.

### Red Dot Marksman (`gx:red_dot_marksman`) — common, hitscan
- Scope: red-dot (2x); dot dot `#ff2a2a`.
- 30s test: Press use: 8 dmg per shot at 80 blocks, 20-tick cadence. Watch the dart tracer and point muzzle flash, then the gx:star_flash impact.
- Twist: The crimson dot is always on and visible to everyone, so aiming is a tell; a hit on the top 15% of a target deals x1.8.
- Ammo: cell, mag 8.

### Prism Beam (`gx:prism_beam`) — epic, beam
- Scope: zoom dial; dot dot `#ffffff`.
- 30s test: Hold use: channel 14 dps over 30 blocks; heat climbs, release to stop.
- Twist: The beam stops at opaque blocks, but through glass, ice or tinted glass it refracts into three red/green/blue spectrum beams that fan out and each deal damage.
- Ammo: heat; heat 100.

### Helios Sniper (`gx:helios_sniper`) — epic, charge
- Scope: 8x scope; dot dot `#5aff6a`.
- 30s test: Hold 1.2s then release: 2 tiers, mode hitscan.
- Twist: Sneak-hold one second steadies the reticle (hold breath); a kill shot beyond 60 blocks is a kill-cam beat that slows nearby mobs for 2 s.
- Ammo: cell, mag 5.

### Ricochet Laser Pistol (`gx:mirror_pistol`) — common, hitscan
- Scope: open sights (no zoom); dot dot `#ff8a2a`.
- 30s test: Press use: 4 dmg per shot at 30 blocks, 10-tick cadence. Watch the hex tracer and plate muzzle flash, then the gx:star_flash impact.
- Twist: Beams bounce off polished blocks (iron, gold, quartz, polished stone, glass) up to 3 times, drawing the full zig-zag path.
- Ammo: cell, mag 12.

### Six-Barrel Gatling Laser (`gx:gatling_laser`) — epic, bolt
- Scope: ring reticle (1.5x); dot dot_ring `#ff5a2a`.
- 30s test: Hold use (auto): 1x disc at 70 b/s, muzzle cluster, impact gx:spark_burst.
- Twist: Barrel spin is the gauge: 4 to 24 shots/s over one second, the wielder slowed while spun up, and releasing keeps the barrels firing for 0.5 s.
- Ammo: cell, mag 60.

### Focus Tri-Beam (`gx:tri_beam`) — rare, beam
- Scope: zoom dial; dot dot_cross `#c08aff`.
- 30s test: Hold use: channel 14 dps over 40 blocks; heat climbs, release to stop.
- Twist: Three beams converge at a focal distance dialled with sneak-tap (8/16/32 blocks); damage is x3 at focus and falls to x0.3 out of focus.
- Ammo: heat; heat 100.

### Orbital Designator (`gx:orbital_designator`) — ultimate, lob
- Scope: distance readout; dot dot_ring `#ff3a3a`.
- 30s test: Press use: arc at 14 b/s, AoE 6; watch the star lob and its landing ring.
- Twist: Hold the dot on a spot for 2 s to lock; 1.5 s later a pillar of light slams down with a 6-block ground shockwave (60 s cooldown).
- Ammo: cell, mag 1.

### Mining Cutter (`gx:cutter_beam`) — rare, beam
- Scope: open sights (no zoom); dot dot `#5aff8a`.
- 30s test: Hold use: channel 14 dps over 6 blocks; heat climbs, release to stop.
- Twist: Dig speed ramps the longer the beam stays on one block; ore blocks sparkle, and the action bar counts the blocks mined (mobGriefing-gated).
- Ammo: heat; heat 100.

### Tesla Coil Gun (`gx:tesla_coil_gun`) — rare, chain
- Scope: ring reticle (1.5x); dot dot `#ffe95a`.
- 30s test: Press use: arc jumps 4 targets within 6 blocks, 0.85 falloff per jump.
- Twist: The copper coil spins up as you fire: three shots inside 2 s add a sixth jump to every arc until the charge lapses.
- Ammo: cell, mag 12.

### Storm Caller (`gx:storm_caller`) — epic, lob
- Scope: 4x scope; dot dot_ring `#ffe04a`.
- 30s test: Press use: arc at 40 b/s, AoE 0; watch the star lob and its landing ring.
- Twist: Strikes auto-target the nearest mob inside the circle instead of the bare ground, and mobs standing in water take +50%.
- Ammo: cell, mag 4.

### Railgun Mk II (`gx:railgun_mk2`) — mythic, charge
- Scope: thermal tint; dot dot `#bfe4ff`.
- 30s test: Hold 1.5s then release: 3 tiers, mode hitscan.
- Twist: The slug pierces five mobs and cuts a glowing glass tunnel through soft rock, while its shockwave ring knocks everything near the path away.
- Ammo: cell, mag 4; heat 100.

### Volt Whip (`gx:volt_whip`) — rare, tether
- Scope: open sights (no zoom); dot dot `#ffd23a`.
- 30s test: Press use: attaches within 10 blocks and pulls; sneak + use to grapple.
- Twist: The whip crackles in an S-curve and wraps the reeled mob in rings of arcs; sneak-use anchors it to a block and pulls you across the gap.
- Ammo: cell, mag 10.

### Thunder Shotgun (`gx:thunder_shotgun`) — common, cone
- Scope: open sights (no zoom); dot dot `#ffcf2b`.
- 30s test: Hold use: 55-degree cone, 10 blocks, 8 dps.
- Twist: Each blast shoves its target 1.2 back and cracks a static arc, so a point-blank pump clears the space around you.
- Ammo: cell, mag 6.

### Arc Glaive Thrower (`gx:glaive_disc`) — epic, bolt
- Scope: red-dot (2x); dot dot `#6ab8ff`.
- 30s test: Hold use (one shot per press): 1x disc at 45 b/s, muzzle rotor, impact gx:debris_burst.
- Twist: The disc bounces through four targets, then reverses and boomerangs home after 25 blocks; re-pressing mid-air splits it into three.
- Ammo: cell, mag 5.

### M9 Service Pistol (`gx:m9_pistol`) — rare, hitscan
- Scope: open sights (no zoom); dot dot `#ff2a1a`.
- 30s test: Press use: 4 dmg per shot at 50 blocks, 5-tick cadence. Watch the 9mm tracer and compact muzzle flash, then the gx:debris_burst impact.
- Twist: Light recoil and fast follow-ups; headshots deal 1.5x.
- Ammo: mag, mag 15.

### .44 Magnum Revolver (`gx:magnum_44`) — epic, hitscan
- Scope: open sights (no zoom); dot dot `#ff2a1a`.
- 30s test: Press use: 14 dmg per shot at 60 blocks, 14-tick cadence. Watch the 44mag tracer and revolver_gap muzzle flash, then the gx:debris_burst impact.
- Twist: Heavy kick and knockback; headshots deal double.
- Ammo: mag, mag 6.

### MP5 Submachine Gun (`gx:mp5_smg`) — epic, hitscan
- Scope: open sights (no zoom); dot dot `#ff2a1a`.
- 30s test: Press use: 2.5 dmg per shot at 45 blocks, 2-tick cadence. Watch the 9mm_para tracer and tri_lug muzzle flash, then the gx:debris_burst impact.
- Twist: 600 rpm with very little climb; best hip-fire in the family.
- Ammo: mag, mag 30.

### Thompson M1928 (`gx:thompson_m1928`) — mythic, hitscan
- Scope: open sights (no zoom); dot dot `#ff2a1a`.
- 30s test: Press use: 3 dmg per shot at 40 blocks, 2-tick cadence. Watch the 45acp tracer and cutts muzzle flash, then the gx:debris_burst impact.
- Twist: Big drum, heavy hitter, wide spray: get close.
- Ammo: mag, mag 50.

### M4A1 Carbine (`gx:m4a1_carbine`) — mythic, hitscan
- Scope: ring reticle (1.5x); dot dot `#ff2a1a`.
- 30s test: Press use: 4 dmg per shot at 80 blocks, 3-tick cadence. Watch the 556 tracer and birdcage muzzle flash, then the gx:debris_burst impact.
- Twist: Sneak to aim through the holo sight (1.5x zoom, tighter spread).
- Ammo: mag, mag 30.

### AK-47 (`gx:ak47`) — mythic, hitscan
- Scope: open sights (no zoom); dot dot `#ff2a1a`.
- 30s test: Press use: 5 dmg per shot at 70 blocks, 3-tick cadence. Watch the 762x39 tracer and slant_brake muzzle flash, then the gx:debris_burst impact.
- Twist: More punch and more climb than the M4; aim to tighten it up.
- Ammo: mag, mag 30.

### SCAR-H Battle Rifle (`gx:scar_h`) — mythic, hitscan
- Scope: red-dot (2x); dot dot `#ff2a1a`.
- 30s test: Press use: 7 dmg per shot at 90 blocks, 4-tick cadence. Watch the 762nato tracer and scar_hider muzzle flash, then the gx:debris_burst impact.
- Twist: Full-power rounds punch through one mob into the next.
- Ammo: mag, mag 20.

### M16A4 Burst Rifle (`gx:m16a4`) — mythic, hitscan
- Scope: 4x scope; dot dot `#ff2a1a`.
- 30s test: Press use: 5 dmg per shot at 100 blocks, 10-tick cadence. Watch the 556_m855 tracer and a2_hider muzzle flash, then the gx:debris_burst impact.
- Twist: Each pull fires a tight three-round burst; the ACOG zooms when you sneak.
- Ammo: mag, mag 30.

### M14 EBR (`gx:m14_ebr`) — mythic, hitscan
- Scope: 4x scope; dot dot `#ff2a1a`.
- 30s test: Press use: 9 dmg per shot at 140 blocks, 6-tick cadence. Watch the 762_match tracer and dmr_brake muzzle flash, then the gx:debris_burst impact.
- Twist: Pinpoint semi-auto at long range; headshots deal 1.75x.
- Ammo: mag, mag 20.

### M24 Sniper Rifle (`gx:m24_sws`) — epic, hitscan
- Scope: 8x scope; dot dot `#ff2a1a`.
- 30s test: Press use: 28 dmg per shot at 220 blocks, 30-tick cadence. Watch the 308_win tracer and sniper_crown muzzle flash, then the gx:debris_burst impact.
- Twist: Sneak for the zoomed scope; the bolt cycles between shots. Headshots deal double.
- Ammo: mag, mag 5.

### Barrett M82 .50 Cal (`gx:barrett_m82`) — mythic, hitscan
- Scope: 8x scope; dot dot `#ff2a1a`.
- 30s test: Press use: 36 dmg per shot at 260 blocks, 20-tick cadence. Watch the 50bmg tracer and double_brake muzzle flash, then the gx:debris_burst impact.
- Twist: Pierces four targets and throws them back. Massive kick.
- Ammo: mag, mag 10.

### Mosin-Nagant (`gx:mosin_nagant`) — rare, hitscan
- Scope: 4x scope; dot dot `#ff2a1a`.
- 30s test: Press use: 21 dmg per shot at 180 blocks, 26-tick cadence. Watch the 762x54r tracer and hooded_post muzzle flash, then the gx:debris_burst impact.
- Twist: Old-school bolt gun: slow, precise, double damage on headshots.
- Ammo: mag, mag 5.

### Remington 870 (`gx:remington_870`) — mythic, hitscan
- Scope: open sights (no zoom); dot dot `#ff2a1a`.
- 30s test: Press use: 3 dmg per shot at 28 blocks, 16-tick cadence. Watch the 12ga_buck tracer and bead muzzle flash, then the gx:debris_burst impact.
- Twist: Devastating up close, falls off fast past 14 blocks. Knocks mobs back.
- Ammo: mag, mag 6.

### AA-12 Auto Shotgun (`gx:aa12`) — mythic, hitscan
- Scope: open sights (no zoom); dot dot `#ff2a1a`.
- 30s test: Press use: 1.5 dmg per shot at 24 blocks, 6-tick cadence. Watch the 12ga_auto tracer and aa12_muzzle muzzle flash, then the gx:debris_burst impact.
- Twist: Hold the trigger and it keeps spraying buckshot.
- Ammo: mag, mag 20.

### M249 SAW (`gx:m249_saw`) — mythic, hitscan
- Scope: open sights (no zoom); dot dot `#ff2a1a`.
- 30s test: Press use: 3 dmg per shot at 90 blocks, 2-tick cadence. Watch the 556_linked tracer and saw_hider muzzle flash, then the gx:debris_burst impact.
- Twist: Sustained fire with every fourth round a tracer; sneak to steady it.
- Ammo: mag, mag 200.

### M134 Minigun (`gx:m134_minigun`) — mythic, hitscan
- Scope: open sights (no zoom); dot dot `#ff2a1a`.
- 30s test: Press use: 1.5 dmg per shot at 80 blocks, 1-tick cadence. Watch the 762_belt tracer and rotary muzzle flash, then the gx:debris_burst impact.
- Twist: Barrels spin up for 0.7 s before the first round, then it never stops.
- Ammo: mag, mag 1500.

### M20 Super Bazooka (`gx:m20_bazooka`) — rare, bolt
- Scope: open sights (no zoom); dot dot `#ff2a1a`.
- 30s test: Hold use (one shot per press): 1x rocket_he at 42 b/s, muzzle bazooka_bell, impact gx:ring_wave.
- Twist: Rockets fly flat, trail smoke, and explode on contact (craters need mobGriefing).
- Ammo: mag, mag 1.

### FGM-148 Javelin (`gx:fgm148_javelin`) — rare, bolt
- Scope: thermal tint; dot dot `#ff2a1a`.
- 30s test: Hold use (one shot per press): 1x missile_heat at 30 b/s, muzzle soft_launch, impact gx:ring_wave.
- Twist: Fire-and-forget: the missile homes onto mobs up to 28 blocks from it.
- Ammo: mag, mag 1.

### M79 Grenade Launcher (`gx:m79_launcher`) — epic, lob
- Scope: open sights (no zoom); dot dot `#ff2a1a`.
- 30s test: Press use: arc at 26 b/s, AoE 3.5; watch the 40mm_he lob and its landing ring.
- Twist: Aim above the target: grenades arc and burst on impact.
- Ammo: mag, mag 1.

### Carl Gustaf Recoilless Cannon (`gx:carl_gustaf`) — rare, bolt
- Scope: 4x scope; dot dot `#ff2a1a`.
- 30s test: Hold use (one shot per press): 1x 84mm_heat at 55 b/s, muzzle venturi, impact gx:ring_wave.
- Twist: Back-blast smoke, a 5-block blast radius, and a 3-block crater.
- Ammo: mag, mag 1.

### Foam Popper (`gx:foam_popper`) — toy, bolt
- Scope: open sights (no zoom); dot dot `#ff7a1a`.
- 30s test: Hold use (one shot per press): 1x dart at 26 b/s, muzzle pop, impact gx:star_flash.
- Twist: Foam darts arc like the real thing and stay stuck to walls for a few seconds.
- Ammo: cell, mag 6.

### Foam Longshot (`gx:foam_longshot`) — toy, bolt
- Scope: 4x scope; dot dot_cross `#2f6fd6`.
- 30s test: Hold use (one shot per press): 1x needle at 42 b/s, muzzle crack, impact gx:star_flash.
- Twist: Sneak for the 4x scope; the heavier dart shoves mobs a couple of blocks back.
- Ammo: cell, mag 10.

### Foam Storm (`gx:foam_storm`) — toy, bolt
- Scope: ring reticle (1.5x); dot dot_ring `#ffd23a`.
- 30s test: Hold use (one shot per press): 6x droplet at 24 b/s, muzzle volley, impact gx:star_flash.
- Twist: Six darts per pull in a loose spread: hard to miss, and each one bonks.
- Ammo: cell, mag 5.

### Pulse Carbine (`gx:pulse_carbine`) — common, bolt
- Scope: red-dot (2x); dot dot `#22e0ff`.
- 30s test: Hold use (one shot per press): 1x teardrop at 60 b/s, muzzle hex, impact gx:ring_wave.
- Twist: Third bolt of every burst is a larger kicker (+50% damage, ring impact).
- Ammo: cell, mag 24.

### Plasma Repeater (`gx:plasma_repeater`) — rare, bolt
- Scope: ring reticle (1.5x); dot dot_ring `#b06aff`.
- 30s test: Hold use (auto): 1x dart at 55 b/s, muzzle star, impact gx:spark_burst.
- Twist: Perfect vent: at overheat a 2s sliding marker appears; releasing in the green zone clears heat instantly and grants a 3s damage boost.
- Ammo: heat; heat 100.

### Sticky Scattergun (`gx:plasma_scattergun`) — rare, bolt
- Scope: open sights (no zoom); dot dot `#ff5ad8`.
- 30s test: Hold use (one shot per press): 8x glob at 25 b/s, muzzle flared, impact gx:star_flash.
- Twist: Globs stick to the first block or mob they touch and detonate 1.5s later, chain-detonating other stuck globs within 3 blocks.
- Ammo: cell, mag 8.

### Splitter Rifle (`gx:splitter_rifle`) — epic, bolt
- Scope: red-dot (2x); dot dot `#3aff9a`.
- 30s test: Hold use (one shot per press): 1x needle at 45 b/s, muzzle prism, impact gx:debris_burst.
- Twist: Shards inherit the parent's remaining pierce and can re-split once on a wall bounce.
- Ammo: cell, mag 12.

### Plasma Lance (`gx:plasma_lance`) — epic, charge
- Scope: 4x scope; dot dot_ring `#22e0ff`.
- 30s test: Hold 1.2s then release: 2 tiers, mode hitscan.
- Twist: Three energy rings travel down the beam and each applies a separate shockwave hit at the first mob it reaches.
- Ammo: cell, mag 6.

### Sunfire Cannon (`gx:sunfire_cannon`) — mythic, bolt
- Scope: 4x scope; dot dot_ring `#ffb02b`.
- 30s test: Hold use (one shot per press): 1x soft_orb at 8 b/s, muzzle cage, impact gx:ring_wave.
- Twist: Leaves a sun-scar pool for 6s that burns anything inside and melts sand/snow/ice within 3 blocks (gated by mobGriefing, cap 20 blocks).
- Ammo: cell, mag 4.

### Ion Disruptor (`gx:ion_disruptor`) — rare, hitscan
- Scope: ring reticle (1.5x); dot dot_cross `#5ab4ff`.
- 30s test: Press use: 5 dmg per shot at 40 blocks, 10-tick cadence. Watch the spark tracer and coil muzzle flash, then the gx:static_arc impact.
- Twist: Stunned machines emit a spark halo and take +40% damage from all sources.
- Ammo: cell, mag 18.

### Twin Photon SMG (`gx:twin_photon_smg`) — common, bolt
- Scope: ring reticle (1.5x); dot dot `#ffe95a`.
- 30s test: Hold use (auto): 1x disc at 50 b/s, muzzle twin, impact gx:spark_burst.
- Twist: Alternating barrels: muzzle flashes alternate sides, and every 12th shot is a golden tracer that pings a hit marker with a coin sound.
- Ammo: cell, mag 36.

### Sonic Cannon (`gx:sonic_cannon`) — rare, cone
- Scope: open sights (no zoom); dot dot `#6fe0d0`.
- 30s test: Hold use: 45-degree cone, 15 blocks, 10 dps.
- Twist: Charge and release: concentric arcs ripple out, stun mobs 1.5 s and shove them back, and shatter glass in the cone (mobGriefing, cap 12).
- Ammo: heat.

### Seeker Missile Rack (`gx:seeker_rack`) — epic, lob
- Scope: lock-on reticle; dot dot_cross `#ff5a4a`.
- 30s test: Press use: arc at 20 b/s, AoE 2; watch the dart lob and its landing ring.
- Twist: Hold aim to bank a lock every 0.6 s (up to four), then release to ripple-fire that many missiles that arc up, dive, and detonate on a wall instead of dudding.
- Ammo: cell, mag 4.

### Combat Drone Launcher (`gx:drone_launcher`) — epic, deploy
- Scope: ring reticle (1.5x); dot dot `#5ab4ff`.
- 30s test: Press use: spawns gx:combat_drone, cap 2, 20s, 6 dps at 12 blocks.
- Twist: The drone orbits you for 20 s, shoots hostiles within 12 blocks (max two up), docks at the end of its timer and refunds a cell if it survived; the aim dot orders it to focus a mob.
- Ammo: cell, mag 2.

### Sentinel Turret Kit (`gx:sentinel_kit`) — epic, deploy
- Scope: open sights (no zoom); dot dot `#6aff9a`.
- 30s test: Press use: spawns gx:sentinel_turret, cap 2, 30s, 8 dps at 16 blocks.
- Twist: A turret that shares its 16-block line of sight with another of yours deals +25% damage while both stand; never targets pups, tamed mobs or players.
- Ammo: cell, mag 2.

### Gravity Well Launcher (`gx:gravity_well_launcher`) — epic, lob
- Scope: distance readout; dot dot_ring `#9a5aff`.
- 30s test: Press use: arc at 14 b/s, AoE 4.5; watch the soft_orb lob and its landing ring.
- Twist: The singularity drags mobs into orbit, grounds flying mobs and bends your own in-flight bolts into the well; when it collapses it bursts outward.
- Ammo: cell, mag 3.

### Void Beam Rifle (`gx:void_beam`) — epic, beam
- Scope: ring reticle (1.5x); dot dot `#100a1e`.
- 30s test: Hold use: channel 16 dps over 25 blocks; heat climbs, release to stop.
- Twist: Hits stack Void Marks on a target; the fourth mark tears a rift that pulls it upward and releases it with heavy damage.
- Ammo: heat; heat 100.

### Blink Rifle (`gx:blink_rifle`) — rare, bolt
- Scope: red-dot (2x); dot dot `#9a5aff`.
- 30s test: Hold use (one shot per press): 1x soft_orb at 55 b/s, muzzle ring_gate, impact gx:star_flash.
- Twist: Impact teleports you to the landing point (safe-spot search, 5 s cooldown); aiming swaps you with the mob you hit.
- Ammo: cell, mag 6.

### Umbra SMG (`gx:umbra_smg`) — rare, bolt
- Scope: ring reticle (1.5x); dot dot `#4a2a7a`.
- 30s test: Hold use (auto): 1x dart at 50 b/s, muzzle suppressor, impact gx:debris_burst.
- Twist: Silent dark bolts leave Shadow Marks; the fifth mark on one mob detonates it in a 3-block shadow burst.
- Ammo: cell, mag 30.

### Black Hole Cannon (`gx:black_hole_cannon`) — ultimate, bolt
- Scope: 4x scope; dot dot_ring `#b06aff`.
- 30s test: Hold use (one shot per press): 1x soft_orb at 4 b/s, muzzle maw, impact gx:star_flash.
- Twist: The slow hole swallows other projectiles and pulls loose items in; when it collapses it flashes white and rings outward (60 s cooldown).
- Ammo: cell, mag 1.

### Repulsor Gauntlet (`gx:repulsor_gauntlet`) — rare, cone
- Scope: ring reticle (1.5x); dot dot_ring `#8a5aff`.
- 30s test: Hold use: 55-degree cone, 8 blocks, 6 dps.
- Twist: Hold to charge a wider, harder blast; firing at the ground while airborne launches you upward on a repulsor burst.
- Ammo: heat; heat 100.

