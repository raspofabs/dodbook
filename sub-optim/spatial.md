Spatial sets for collisions
---------------------------

In collision detection, there is often a broad-phase step which can
massively reduce the number of potential collisions we check against.
When ray casting, it’s often useful to find the potential intersection
via an octree, bsp, or other single query accelerator. When running path
finding, sometimes it’s useful to look up local nodes to help choose a
starting node for your journey.

All spatial data-stores accelerate queries by letting them do less. They
are based on some spatial criteria and return a reduced set that is
shorter and thus less expensive to transform into new data.

Existing libraries that support spatial partitioning have to try to work
with arbitrary structures, but because all our data is already organised
by table, writing adaptors for any possible table layout is simple.
Writing generic algorithms becomes very easy without any of the side
effects normally associated with writing code that is used in multiple
places. Using the table based approach, because of its intention
agnosticism (that is, the spatial system has no idea it’s being used on
data that doesn’t technically belong in space), we can use spatial
partitioning algorithms in unexpected places, such as assigning audio
channels by not only their distance from the listener, but also their
volume and importance. Making a 5 dimensional spatial partitioning
system, or an N dimensional one, would only have to be written once,
have unit tests written once, before it could be used and trusted to do
some very strange things. Spatially partitioning by the quest progress
for tasks to do seems a little overkill, but getting the set of all
nearby interesting entities by their location, threat, and reward, seems
like something an AI might consider useful.

