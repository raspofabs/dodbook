Existence from null to infinity
-------------------------------

Going back to our entities being implicit on their attributes, we can
utilise the theory of hierarchical level of detail to offer up some
optimisations for our code. If we have high level low fidelity coarse
grain game logic for distant or currently unimportant game entities, and
only drill down to highly tuned code when an entity becomes more
apparent to the player, then we can save a lot of cycles on things the
player is not interested in, or possibly even able to see.

Consider a game where you are defending a base from incoming attacks.
The attackers come in squadons of ships, you can see them all coming at
once, over a thousand ships in all and up to twenty at once in each
squadron. You have to shoot them down, or be inundated with gunfire and
bombs, taking out both you and the base you are defending.

Running full AI, with swarming for motion and avoidance for your slower
moving weapons might be too much if it was run on all thousand ships
every tick, but you don’t need to. The basic assumption made by most AI
programmers is that unless they are within attacking range, then they
don’t need to be running AI. This is true, and does offer an immediate
speed up compared to the naive approach. Hierarchical LOD provides
another way to think about this, through changing the number of entities
based on how they are perceived by the player. For want of a better
term, count-lodding is a name that describes what is happening behind
the scenes a little better, because sometimes there is no hierarchy and
yet there can still be a change in count between the levels of detail.

In the count-lodding version of the base defender game, there is a few
Wave entities that project a few Squadron blips on the radar. The
squadrons don’t exist as their own entities until they get close enough.
Once a wave’s squadron is within range, the Wave can decrease its
squadron count, and pop out a new Squadron entity. The Squadron entity
shows blips on the radar for each of its component ships. The ships
don’t exist, but they are implicit in the Squadron. The Wave continues
to pop Squadrons as they come into range, and once it’s internal count
has dropped to zero, it deletes itself as it now represents no entities.
As a Squadron comes into even closer range, it pops out its ships into
their own entities, and deletes itself. As the ships get closer, their
renderables are allowed to switch to higher resolution and their AI is
allowed to run at a higher intelligence setting.

When the ships are shot at, they switch to a taken damage type much like
the health system earlier. They are full health unless they take damage.
If an AI reacts to damage with fear, they may eject, adding another
entity to the world. If the wing of the plane is shot off, then that
also becomes a new entity in the world. Once a plane has crashed, it can
delete its entity and replace it with a smoking wreck entity that will
be much simpler to process than an aerodynamic simulation.

If the player can’t keep the ships at bay and their numbers increase in
size so much that any normal level of detailing can’t kick in, count
lodding can still help by returning ships to squadrons and flying them
around the base attacking as a group rather than as invididual ships.
The level of detail heuristic can be tuned so that the nearest and
front-most squadron are always the highest level of detail, and the ones
behind the player maintain a very simplistic representation.

This is game development smoke and mirrors as a basic game engine
element. In the past we have reduced the number of concurrent attacking
AI[^1], reduced the number of cars on screen by staggering the lineup
over the whole race track[^2], and we’ve literally combined people
together into one person instead of having loads of people on screen at
once[^3]. This kind of reduction of processing is commonplace. Now use
it everywhere appropriate, not just when a player is not looking.

[^1]: I beleive this was half-life

[^2]: Ridge Racer was one of the worst for this

[^3]: Populous did this
