In Practice
===========

Data-oriented development is not rooted in theory, but practice. Because
of this, it’s hard to describe the methodology without some practical
examples. In this chapter I will document some experiences with the
data-oriented approach.

Data-manipulation
-----------------

### The Cube

In 22cans first experiment, there was call to handle a large amount of
traffic from a large number of clients, potentially completely
fragmented, and yet also completely syncronised. The plan was to develop
a service capable of handling a large number of incoming packets of
*update* data while also compiling it into compressed *output* data that
could be send to the client all with a minimal turnaround time.

The system was developed in C++11 on Linux, and followed the basic
tenets of data-oriented design from day one. The data was loaded, but
not given true context. Manipulations on the data were procedures that
operated on the data given other data. This was a massive time saver
when the servers needed a complete redesign. The speed of data
processing was sufficient to allow us to run all the services in
debug[^1].

When the server went live, it wasn’t the services that died, it was the
front end. Nginx is amazing, but under that amount of load on a single
server, with so many of the requests requiring a lock on an SQL db
backend, the machine reached it’s limit very quickly. For once, we think
PHP itself wasn’t to blame. We had to redesign all the services so they
could work in three different situations so as to allow the server to
become a distributed service. By not locking down data into contexts, it
was relatively easy to change the way the data was processed, to
reconfigure the single service that previously did all the data
consumption, collation, and serving, into three different services that
handled incoming data, merging the multiple instances, and serving the
data on the instances. In part this was due to a very procedural
approach, but it was also down to not linking together data that was
separate by binding into an object context. The lack of binding allows
for simpler recombination of procedures, simpler rewriting of
procedures, and simpler repurposing of procedures from related services.
This is something that object oriented approach makes harder because you
can be easily tempted to start adding base classes and inheriting to
gain common functionality or algorithms. As soon as you do that you
start tying things together by what they mean rather than what they are,
and then you lose the ability to reuse code.

### Rendering order

While working on the in-house engine at Broadsword, we came up with an
idea for how to reimplement the renderer that should have been much more
efficient, not just saving CPU cycles, but also allowing for platform
specific optimisations at run time by having the renderer analyse the
current set of renderables and organise the whole list of jobs by what
caused the least program changes, texture changes, constant changes and
primitive render calls. The system seemed too good to be true, and
though we tried to write the system, Broadsword never finished it. After
Broadsword dissolved, when I did finish it, I didn’t have access to a
console[^2], so I was only able to test out the performance on a PC. As
expected the new system was faster, but only marginally. With hindsight,
I now see that the engine was only marginally more efficient because the
tests were being run on a system that would only see marginal
improvements, but even the x86 architecture saw improvements, which can
be explained away as slightly better control flow and generally better
cache utilisation.

First let me explain the old system.

All renderables came from a scene graph. There could be multiple scene
graph renders per frame, which is how the 2D and 3D layers of the game
were composited, and each of them could use any viewport, but most of
them just used the fullscreen viewport as the engine hadn’t been used
for a split screen game, and thus the code was probably not working for
viewports anyway. Each scene graph render to viewport would walk the
scene[^3] collecting transforms, materials, colour tints, and meshes, to
render, at which point the node that contained the mesh would push a
render element onto the queue for rendering into that viewport. This
queueing up of elements to render seemed simple and elegant at the time.
It meant that programmers could quickly build up a scene and render it,
most of the time using helpers that loaded up the assets and generated
the right nodes for setting textures, transforms, shader constants, and
meshes. These rendering queues were then sorted before rendering. Sorted
by material only for solid textures, and sorted back to front for alpha
blended materials. This was the old days of fixed function pipelines and
only minimal shader support on our target platforms. Once the rendering
was done, all the calculated combinations were thrown away. This meant
that for everything that was rendered, there was definitely a complete
walk of the scene graph.

The new system, which was born before we were aware of data-oriented
design, but was definitely born of looking at the data, was different in
that it no longer required walking the scene graph. We wanted to
maintain the same programmer friendly front edge API, so maintained the
facade of a scene graph walk, but instead of walking the graph, we only
added a new element to the rendering when the node was added, and only
removed it when it was removed from the scene graph. This meant we had a
lot of special code that looked for multiple elements registered in
multiple view port lists, but, other than that, a render merely looked
up into the particular node it cared about, gathered the latest data,
and processed it pulling when it required it rather than being pushed
things it didn’t even care about.

The new system benefited from being a simple list of pointers from which
to fetch data (the concept of a dirty transform was removed, all
transforms were considered to be dirty every frame), and the computation
was simplified for sorting as all the elements that were solid were
already sorted from the previous render, and all the alpha blended
elements were sorted because they belonged to the set of alpha blended
elements. This lack of options accounted for some saved time, but the
biggest saving probably came from the way the data was being gathered
per frame rather than being generated from a incoherent tree. A tree
that, to traverse, requried many pointer lookups into virtual tables as
all the nodes were base classed to a base node type and all update and
render calls were virtual causing many misses all the way through each
of the tree walks.

In the end the engine was completely abandoned as Broadsword dissolved,
but that was the first time we had taken an existing codebase and
(though inadvertantly) converted it to data-oriented.

### Keeping track of damage

During the development of the multiplayer code for Max Payne 3 there
came a point where it became more and more important that we kept track
of damage dealt to every player from every player. Sometimes this would
be because we want to estimate more accurately how much health a player
had. Sometimes this would be because we needed to know who saved who and
thus who got a teammate saved bonus, or who got the assist. We kept a
tight ship on Max Payne 3, we tried to keep the awards precise as far as
we could go, no overcompensating for potential lost packets, no faking
because we wanted a fair and competition grade experience where players
could make all the difference through skill, and not through luck. To do
this, we needed to have a system that kept track of all the bullets
fired, but not fail when we missed some, or they arrived out of order.
What we needed was a system that could be interrogated, but could
receive data about things that had happened back in time. It needed to
be able to heal itself in case of oddities, and last but not least, it
needed to be really quick so we can interrogate it many times per frame.

The solution was a simple list of things that happened and at what time.
Initially the data was organised as a list of structures with a sorted
list of pointers to the data for quick queries about events over time,
but after profiling the queries with and without the sorted list, the
benefits of the lack of maintaining a sorted list outweighed the
benefits of doing a one time sort on just the data needed to satisfy the
query. There were only two queries, which were not frequently called,
that benefitted from the sorted data, and when they were called they
didn’t need to be extremely fast as they were called as the result of
player death, which not only happened less often than once a frame, but
also regularly resulted in there being less to update as the player
cared a lot less about visibility checks and handling network
traffic[^4]. This simple design allowed for many different queries to
run over the core data, and allowed for anyone to add another new query
easily because there was no data-hiding getting in the way of any new
kind of access. Object-oriented approaches to this kind of data handling
often provide a gateway to the data but marshall it so that the queries
become heavyweight and consistently targetted for optimisation. With a
very simple data structure and open access to the data in any form, any
new query could be as easily optimised as any existing one.

Game entities
-------------

### Converting an object oriented player

While I was at Frontier Developments, I was working on a little space
game that ended up being a boat game in caverns[^5] and that was the
first time I intentionally changed a game from object-oriented to
component-oriented. The ships all had their rendering positions, their
health, speed, momentum, ammo recharge timers etc, and these were all
part of a base ship class that was extended to be a player class, and
inherited from a basic element that was extended to also include the
loot drops and the dangerous ice blocks. All this is pretty standard
practice, and from the number of codebases I have seen, it’s pretty
light on the scale of inheritance with which games normally end up.
Still, I had this new tool in my bag, the component-oriented approach
specifically existence based processing. I wanted to try it out, see if
it really did impact the profile of the game in any significant way. I
started with the health values. I made a new component for health, and
anyone that was at full health, or was dead, was not given an instance
of the component. The player ship and the enemy ships all had no health
values until they were shot and found wanting.

Transitioning to the component based health took a while. Translating
any game from one programming paradigm to another is not a task to be
taken lightly, even when your game code is small and you’ve only spent
sixty hours developing the game so far. Once the game was back up
though, the profile spoke loud and clear of the benefits. I had
previously spent some time in health code every frame, this was because
the ships had health regenerators that ran and updated the health every
time they got an update poll. They needed to do an update because they
were updated, not because they needed to, and they didn’t have any way
to opt out before the componentisation, as the update to health was part
of the ship update. Now the health update only ran over the active
health instances, and removed itself once it reached max health rather
than bounce of the max health.

This relatively small change allowed me to massively increase the number
of small delicate ships in the game (ships that would beat the player
ship by overrunning it rather than being able to withstand the player’s
fire and get close in to do some damage), and also lead to another
optimisation: componentising the weapon recharge timer.

If the first change was a success, then the second was a major success.
Instead of keeping track of when a weapon was ready to fire again, the
time that it would be available was inserted into a sorted list of
recharge times. Only the head of the list was checked every global
update, meaning that a large number of weapons could be recharging at
once and none of them caused any data access until they were very nearly
or actually ready.

This immediate success lead me to believe the data-oriented design
movement was really important and needed to be spread around, and
probably caused my sudden hatred of object-oriented programming. From
that point on, all I could see was cache-misses and pointless update
checks.

### People don’t really exist.

> *A Mathematician, a Biologist and a Physicist are sitting in a street
> cafe watching people going in and coming out of the house on the other
> side of the street.*
>
> First they see two people going into the house. Time passes. After a
> while they notice three persons coming out of the house.
>
> The Physicist: “The measurement wasn’t accurate.”.\
> The Biologists conclusion: “They have reproduced”.\
> The Mathematician: “If now exactly 1 person enters the house then it
> will be empty again.”

The followers in the GODUS prototype are little objects when they are
running around, and though the code has changed quite a bit from the
initial lists of pointers to people structures, and has thus become
unweildy, there was one element that was a perfect example of
hierarchical level of detail in the game logic. The followers, once they
had started to build a building, dissappeared. They were no longer
required in any way, so they were reduced to a mere increment of the
number of people in a building. An object-oriented programmer disputed
this being a good way to go, “but what if the person has a special
weapon, or is a special character?”. Logic prevailed. If there was a
special weapon, then there would have been a count of those in the
house, or the weapon would have become owned by the house, and as for a
special character, the same kind of exception could be made, but in
reality, which is where we firmly plant ourselves when developing in the
data-oriented paradigm, these potential changes had not so far been
requested, and by the end of the development, they still hadn’t.

Another example from the GODUS prototype was the use of duck-typing.
Instead of adding a base class for people and houses, just to see if
they were meant to be under control of the local player, we used a
templated function to extract a boolean value. Duck typing doesn’t
require anything more than certain member functions or variables being
available. They don’t have to be in the same place, or come bundled into
a base class: they just have to be present.

When teaching data-oriented design, I find the biggest hurdle is
convincing programmers that data-oriented design is possible for some
areas of development. It’s very easy to accidentally assume that you
need to bundle things into objects, especially after years of training
and teaching object-oriented developlment. It won’t come naturally and
you will keep catching yourself building things as objects first then
making them more relational afterwards. It will take time to fully
remove the muscle memory of putting related things in the same class,
but worry not, I’m sure all data-oriented developers go through this
transition where they know they’re not coding data-oriented, but they
don’t quite know how to do it yet.

### Lazy evaluation molasses

The idea of lazy evaluation makes so much sense, and yet it’s precisely
that kind of sense that makes no sense for a computer. I remember there
was a dirty bit check before an update in some of the global update code
on Outsider, something I would have done a hundred times over before I
started to get a better feel for what the computer was doing, and found
one of the best lines-of-code to time-saved ratio fixes I ever found in
a triple A game. The dirty bit check was just before the code that
actually did the work of updating the instance. This meant that the CPU
had to preload the *fixup* code while it was checking the dirty bit, and
because the fixup code was virtual functions based, it meant that the
code was loading the virtual table value and the function was preloaded
all the while the dirty bit was about to say it wasn’t necessary to do
any of it. To make matters worse, the code was inside an if, implying to
most compilers that it would be the more likely taken branch[^6]. The
fix was simple. Build up a local array of objects to actually do an
update of, then do them all at once. Because the code to do the update
wasn’t preloaded, the whole update took a lot less time. You can have
your lazy evaluation, but don’t preload the evaluation if you don’t have
to.

### Component oriented design

While at Broadsword, I found an article about dungeon seige proclaiming
the benefit of components when developing a game. The GOs or Game
Objects that were used were components that could be stitched together
to create new compound objects.

Taking that as inspiration, I looked at all our different scene-graph
nodes, gameplay helper classes and functions we commonly used, and tried
to distill them into their elements. I started by just making components
such as *PlayerCharacter* and *AICharacter*, adding a *Prop* element
before realising where I was going wrong. The object oriented mindset
had told me to look at the compounds, not the elements, so I went back
to the drawing board and started dissecting the objects again. Component
oriented development works out best when you completely explode all your
compounds, then recombine when you find the combinations are consistent,
or when combining makes more sense to computation.

After I was done fully dissecting our basic game classes I had a long
list of separate, elements that by themselves did very little[^7]. At
this point, I added the bootstrap code to generate the scene. Some
components required other components at runtime, so I added a *requires*
trait to the components, much like \#include, except to make this work
for teardown, I also added a count so components went away much like
reference counted smart pointers folded away. The initial demo was a
simple animated character running around a 3D environment, colliding
with props via the collision Handler.

In the beginning, I had a container entity that maintained a list of
components. Once I had a first working version, I stepped back and
thought about the system. I started to see that the core entity wasn’t
really necessary. As long as any update components were updated, then
the game would tick on. As long as the entity’s components could find
their requirement components, then the game would work. I shifted to
having an implicit entity based on the UID I generate on entity
creation. This meant that all entities were really only the components
that were linked to that ID, as the ID didn’t index into an array of
entity objects, or point to an allocated entity, it was merely an ID off
which to hang all the components.

Adding features to a class at runtime was now possible. I could inject
an additional property into the existing entities because I had centred
the entities around a key, and not any kind of central class. The next
step from here was to add components via a scripting language so it
would be possible to develop new gameplay code while running the game.
Unfortunately this never happened, but some MMO engine developers have
done precisely this.

The success of this demo convinced me that components would play a major
role in our continuing game development, but alas, we only used the
engine for one more product and the time to bring the new component
based system up to speed for the size of the last project was estimated
to be counter productive. Mick West released an article about how when
he was at Neversoft, he did manage to convert the Tony Hawks code-base
to components[^8] which means it’s not impossible to migrate, it’s just
not easy. If we were to start component oriented... well that’s a
different story, normally told by Scott Bilas.

[^1]: anyone remembering developing on a PS2 will likely attest to the
    minimal benefit you get from optimisations when your main bottleneck
    is the VU and GS. The same was true here, we had a simple bottleneck
    of the size of the data and the operations to run on it.
    Optimisations had minimal impact on processing speed, but they did
    impact our ability to debug the service when it did crash.

[^2]: The target platforms of the engine included the Playstation 2 and
    the Nintendo Wii along with Win32.

[^3]: sometimes multiple cameras belonged to the same scene to the scene
    graph would be walked multiple times

[^4]: dead men don’t care about bullets and don’t really care that much
    about what other players are doing

[^5]: due to concerns that a 2D space game might be misinterpretted as
    the next elite I imagine

[^6]: profile guided optimisation might have saved a lot of time here,
    but the best solution is to give the profiler and optimiser a better
    chance by leaving them less to do

[^7]: Position, Velocity, PlayerInputMapper, VelocityFromInput,
    MeshRender, SkinnedMeshRender, MatrixPalette, AnimPlayer,
    AnimFromInput, and CollisionHandler

[^8]: http://cowboyprogramming.com/2007/01/05/evolve-your-heirachy/
