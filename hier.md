Hierarchical Level-of-Detail and Implicit-state
===============================================

Consoles and graphics cards are not generally bottlenecked at the
polygon rendering stage in the pipeline. Usually they are fill rate
bound if there are large polygons on screen, or there is a lot of alpha
blending, and for the most part, graphics chips spend a lot of their
time reading textures. Because of this, the old way of doing level of
detail with multiple meshes with decreasing numbers of polygons is never
going to be as good as a technique that takes into account the actual
data required of the level of detail used in each renderable.
Hierarchical level of detail fixes the problem of high primitive count
and mistargetted art optimisations by grouping and merging many low
level of detail meshes into one low level of detail mesh, thus reducing
the time spent in the setup of render calls, and enforcing a better
perspective on the artist producing the lower resolution asset. In a
typical very large scale environment, a hierarchical level of detail
implementation can reduce the workload on a game engine by an order of
magnitude as the number of entities in the scene considered for
rendering drops significantly. Even though the number of polygons
rendered might be exactly the same, or maybe even more, the fact that
the engine usually only has to handle a static number of entities at
once increases stability and allows for more accurately targeted
optimisations of both art and code.

Existence from Null to Infinity
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

Mementos
--------

Reducing detail introduces an old problme, though. Changing level of
detail in game logic systems, AI and such, brings with it the loss of
high detail history. In this case we need a way to store what is needed
to maintain a highly cohesive player experience. If a high detail
squadron in front of the player goes out of sight and another squadron
takes their place, we still want any damage done to the first group to
reappear when they come into sight again. Imagine if you had shot out
the glass on all the ships and when they came round again, it was all
back the way it was when they first arrived. A cosmetic effect, but one
that is jarring and makes it harder to suspend disbelief.

When a high detail entity drops to a lower level of detail, it should
store a memento, a small, well compressed nugget of data that contains
all the necessary information in order to rebuild the higher detail
entity from the lower detail one. When the squadron drops out of sight,
it stores a memento containing compressed information about the amount
of damage, where it was damaged, and rough positions of all the ships in
the squadron. When the squadron comes into view once more, it can read
this data and generate the high detail entities back in the state they
were before. Lossy compression is fine for most things, it doesn’t
matter precisely which windows, or how they were cracked, maybe just
that about $2/3$ of the windows were broken.

Another good example is in a city based free-roaming game. If AIs are
allowed to enter vehicles and get out of them, then there is a good
possibility that you can reduce processing time by removing the AIs from
world when they enter a vehicle. If they are a passenger, then they only
need enough information to rebuild them and nothing else. If they are
the driver, then you might want to create a new driver type based on
some attributes of the pedestrian before making the memento for when
they exit the vehicle.

If a vehicle reaches a certain distance away from the player, then you
can delete it. To keep performance high, you can change the priorities
of vehicles that have mementos so that they try to lose sight of the
player thus allowing for earlier removal from the game. Optimisations
like this are hard to coordinate in Object-oriented systems as internal
inspection of types isn’t encouraged.

JIT Data Generation
-------------------

If a vehicle that has been created as part of the ambient population is
suddenly required to take on a more important role, such as the car
being involved in a fire fight. It is important to generate new entities
that don’t seem overly generic or unlikely given what the player knows
about the game so far. Generating data can be thought of as providing a
memento to read from just in time. JIT mementos are faked mementos that
provide a false sense of continuity by allowing pseudo random generators
or hash functions the opportunity to replace non-zero memory usage
mementos when the data is unlikely to change, or be needed for more than
a short while.

JIT mementos can also be the basis of a highly textured environment with
memento style sheets or style guides that can direct a feel bias for any
mementos generated in those virtual spaces. Imagine a city style guide
that specifies rules for occupants of cars, that businessmen might
share, but are less likely to, families have children in the back seats
with mum or dad driving, young adults tend to drive around in pairs.
These style guides help add believability to any generated data. Add in
local changes such as having types of car linked to their drivers,
convertibles driven by well dressed types or kids, low riders driven
almost exclusively by ghetto residents, imports driven by young adults.
In a space game, dirty hairy pilots of cargo ships, well turned out
officers commanding yachts, rough and ready mercenaries in everything
from a single seater to a dreadnought.

JIT mementos are a good way to keep variety up, and style guides bias
that so it comes without the impression that everyone is different so
everyone is the same. When these biases are played out without being
striclty adhered to, you can build a more textured environment. If your
environment is heavily populated with a completely different people all
the time, there is nothing to hold onto, not patterns to recognise. When
there are no patterns, the mind tends to see noise, or mark it as samey.
Even the most varied virtual worlds look bland when there is too much
content all in the same place.

Alternative Axes
----------------

As with all things, take away an assumption and you can find other uses
for a tool. Whenever you read about or work with a level of detail
system, you will be aware that the constraint on what level of detail is
shown has always been some distance function in space. It’s now time to
take that assumption, discard it, and analyse what is really happening.

First, we find that if we take away the assumption of distance, we can
infer the conditional as some kind of linear measure. This value
normally comes from a function that takes the camera position and finds
the relative distance to the entity under consideration. What we may
also realise when discarding the distance assumption is a more
fundamental understanding of that what we are trying to do. We are using
a runtime variable to control the presentation state of an entity. We
use runtime variables to control the state of many parts of our game
already, but in this case, there is a passive presentation response to
the variable, or axis being monitored. The presentation is usually some
graphical, or logical level of detail, but it could be something as
important to the entity as its own existence.

How long until a player forgets about something that might otherwise be
important? This information can help reduce memory usage as much as
distance. If you have ever played <span>*Grand Theft Auto IV*</span>,
you might have noticed that the cars can dissappear just by not looking
at them. As you turn around a few times you might notice that the cars
seem to be different each time you face their way. This is a stunning
use of temporal level of detail. Cars that have been bumped into or
driven and parked by the player remain where they were, because, in
essence, the player put them there. Because the player has interacted
with them, they are likely to remember that they are there. However,
ambient vehicles, whether they are police cruisers, or civilian
vehicles, are less important and don’t normally get to keep any special
status so can vanish when the player looks away.

In adition to time-since-seen, some elements may base their level of
detail on how far a player has progressed in the game, or how many of
something a player has, or how many times they have done it. For
example, a typical bartering animation might be cut shorter and shorter
as the game uses the axis of <span>*how many recent barters*</span> to
draw back the length of any non-interactive sections that could be
caused by the event. This can be done simply, and the player will be
thankful. It may even be possible to allow for multi-item transactions
after a certain number of transactions have happened. In effect, you
could set up gameplay elements, reactions to situations, triggers for
tutorials or extensions to gameplay options all through these abstracted
level of detail style axes.

This way of manipulating the present state of the game is safer from
transition errors. Errors that happen because going from one state to
another may have set something to true when transitioning one direction,
but not back to false when transitioning the other way. You can think of
the states as being implicit on the axis, not explicit, calculated
purely as a triggered event that manipulates state.

An example of where transition errors occur is in menu systems where
though all transitions should be reversible, sometimes you may find that
going down two levels of menu, but back only one level, takes you back
to where you started. For example, entering the options menu, then
entering an adjust volume slider, but backing out of the slider might
take you out of the options menu all together. These bugs are common in
UI code as there are large numbers of different layers of interaction.
Player input is often captured in obscure ways compared to gameplay
input response. A common problem with menus is one of ownership of the
input for a particular frame. For example, if a player hits both the
forward and backward button at the same time, a state machine UI might
choose to enter whichever transition response comes first. Another might
manage to accept the forward event, only to have the next menu accept
the back event, but worst of all might be the unlikely but seen in the
wild, menu transitioning to two different menus at the same time.
Sometimes the menu may transition due to external forces, and if there
is player input captured in a different thread of execution, the game
state can become disjoint and unresponsive. Consider a network game’s
lobby, where if everyone is ready to play, but the host of the game
disconnects while you are entering into the options screen prior to game
launch, in a traditional state machine like approach to menus, where
should the player return to once they exit the options screen? The lobby
would normally have dropped you back to a server search screen, but in
this case, the lobby has gone away to be replaced with nothing. This is
where having simple axes instead of state machines can prove to be
simpler to the point of being less buggy and more responsive.

[^1]: I beleive this was half-life

[^2]: Ridge Racer was one of the worst for this

[^3]: Populous did this
