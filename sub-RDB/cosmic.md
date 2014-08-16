Cosmic Hierarchies
------------------

Whatever you call them, be it Cosmic Base Class, Root of all Evil,
Gotcha \#97, or CObject, having a base class that everything derives
from has pretty much been a universal failure point in large C++
projects. The language does not naturally support introspection or duck
typing, so it has difficultly utilising CObjects effectively. If we have
a database driven approach, the idea of a cosmic base class might make a
subtle entrance right at the beginning by appearing as the entity to
which all other components are adjectives about, thus not letting
anything be anything other than an entity. Although component–based
engines can often be found sporting an EntityID as their owner, not all
require owners. Not all have only one owner. When you normalise
databases, you find that you have a collection of different entity
types. In our level file example we saw how the objects we started with
turned into a MeshID, TextureID, RoomID, and a PickupID. We even saw the
emergence through necessity of a DoorID. If we pile all these Ids into a
central EntityID, the system should work fine, but it’s not a necessary
step. A lot of entity systems do take this approach, but as is the case
with most movements, the first swing away swings too far. The balance is
to be found in practical examples of data normalisation provided by the
database industry.

