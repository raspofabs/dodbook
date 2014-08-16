Inherently concurrent operations
--------------------------------

When working with tables of data, many operations are inherently
concurrent. Simple transforms that take one table and generate the next
step, such as those of physics systems or AI state / finite state
machines, are inherently concurrent. You could provide a core per row /
element and there would be no issues at all. Setting up the local bone
transforms from a skeletal animation data stream, ticking timers,
producing condition values for later use in condition tables. All these
are completely concurrent tasks. Anything that could be implemented as a
pixel or vertex shader is inherently concurrent, which is why parallel
processing languages such as shader models, do not cheaply allow for
random write to memory, and don’t allow accumulators across elements.

Seeing that these operations are inherently concurrent, we can start to
see that it’s possible to restructure our game from an end result
perspective. We can use the idea of a structured query to help us find
our critical path back to the game state. Many table transforms can be
split up into much smaller pieces, possibly thinking along the lines of
map reduce, bringing some previously serial operations into the
concurrent solution set.

Any N to N transform is perfectly concurrent. Any N to \<=N is perfectly
concurrent, but depending on how you handle output NULLs, you could end
up wasting memory. A reduce stage is necessary, but that could be
managed by a gathering task after the main task has finished, or at
least, after the first results have started coming in.

Any uncoupled transforms can be run concurrently. Ticking all the finite
state machines can happen at the same time as updating the phsyics
model, can happen at the same time as the graphics culling system
building the next frame’s render list. As long as all your different
game state transforms are independent from each other’s current output,
they can be dependent on each other’s original state and still maintain
concurrency.

For example, the physics system can update while the renderer and the AI
rely on the positions and velocities of the current frame. The AI can
update while the animation system can rely on the previous set of
states.

Multi stage transforms, such as physics engine broadphase, detection,
reaction and resolution, will traditionally be run in series while the
transforms inside each stage run concurrently. Standard solutions to
these stages require that all data be finished processing from each
previous stage, but if you can find some splitting planes for the
elements during the first stage, you can then remove temporal cohesion
from the processing because you can know what is necessary for the next
step and hand out jobs from finished subsets of each stage’s results.

Concurrent operation assumes that each core operating on the data is
free to access that data without interfering, but there is a way that
seemingly unconnected processes can end up getting in each other’s way.
Most systems have multiple layers of cache, and this is where the
accident can happen. False sharing is when data, though actually
unrelated, is connected by the physical layout of the hardware. For
example, the cachelines of a CPU might be 16 to 128 bytes long. If two
different CPUs try to write to neighbouring bytes, or words, at best the
cores will lock up as the memory is shunted around trying to keep memory
consistent, but worse, could end up losing data if the cache is not
coherent[^2]. To reduce the chance of this happening, processing of
small element tables should consider this and split any cooperation into
cacheline size jobs.

[^2]: cache coherency is the system by which changed data is propagated
    to other caches so that consistent state is achieved.
