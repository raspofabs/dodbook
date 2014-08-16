Game Development Patterns
-------------------------

The Game/Session/Level/Entity hierarchy still applies, and can be
gathered accurately as part of the data flow analysis done during the
early stages of design iteration. If you use tables for most of your
data, then you will find that each layer has a set of tables.

Tick or update scheduling is normally necessary in order to maintain
data scheduling, but as the data flow is paramount in data-oriented
development, there is no need for a dedicated scheduler. In fact, the
sequences of transforms replace the scheduler normally found in games by
having a cascade of dependencies play out in the instance of a new frame
being rendered. A frame buffer swap is an event that begins a new
sequence of processes. In some games this could be the gathering of
controller updates followed by physics and logic updates, finally
culminating in an update of the renderable scene.

Double and Triple Buffering, which is normally the only way of getting
near a good framerate, by processing multiple stages over multiple
frames, may not need to happen so much as it does with object-oriented
code as data-oriented code is much more parallelisable, so doesn’t have
the long critical path between input and rendering output. Removing
multiple serial points can drastically reduce your overall gameplay
feedback latency.
