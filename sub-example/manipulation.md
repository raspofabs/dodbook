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

