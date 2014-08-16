Stream Processing
-----------------

Now we realise that all the game data and game runtime can be
implemented in a database oriented approach, there’s one more
interesting side effect: data as streams. Our persistent storage is a
database, our runtime data is in the same format as it was on disk, what
do we benefit from this? Databases can be thought of as collections of
rows, or collections of columns, but there is one more way to think
about the tables, they are sets. The set is the set of all possible
permutations of the attributes. For example, in the case of RoomPickups,
the table is defined as the set of all possible combinations of Rooms
and Pickups. If a room has a Pickup, then the bit is set for that
room,pickup combination. If you know that there are only N rooms and M
types of Pickup, then the set can be defined as a bit field as that is
N\*M bits long. For most applications, using a bitfield to represent a
table would be wasteful, as the set size quickly grows out of scope of
any hardware, but it can be interesting to note what this means from a
processing point of view. Processing a set, transforming it into another
set, can be thought of as traversing the set and producing the output
set, but the interesting attribute of a set is that it is unordered. An
unordered list can be trivially parallel processed. There are massive
benefits to be had by taking advantage of this trivialisation of
parallelism wherever possible, and we normally cannot get near this
because of the data layout of the object-oriented approaches.

Coming at this from another angle, graphics cards vendors have been
pushing in this direction for many years, and we now need to think in
this way for game logic too. We can process lots of data quickly as long
as we utilise about stream processing as much as possible and use random
access processing as little as possible. Stream processing in this case
means to process data without having variables that are external to the
current datum., thus ensuring the processes or transforms are trivially
parallelisable.

When you prepare a primitive render for a graphics card, you set up
constants such as the transform matrix, the texture binding, any
lighting values, or which shader you want to run. When you come to run
the shader, each vertex and pixel may have its own scratch pad of local
variables, but they never write to globals or refer to a global
scratchpad. Enforcing this, we can guarantee parallelism because the
order of operations are ensured to be irrelevant. If a shader was
allowed to write to globals, there would be locking, or it would become
an inherently serial operation. Neither of these are good for massive
core count devices like graphics cards, so that has been a self imposed
limit and an important factor in their design.

Doing all processing this way, without globals / global scratchpads,
gives you the rigidity of intention to highly parallelise your
processing and make it easier to think about the system, inspect it,
debug it, and extend it or interrupt it to hook in new features. If you
know the order doesn’t matter, it’s very easy to rerun any tests or
transforms that have caused bad state.

