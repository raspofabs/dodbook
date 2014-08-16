Components imply entities
-------------------------

If we go back to our level file, we see that the room table is quite
explicit about itself. What we have is a simple list of rooms with all
the attributes that are connected to the room written out along the
columns. Although adding new features is simple enough, modification or
reusing any of these separately would prove tricky.

If we change the room table into multiple adjective tables, we can see
how it is possible to build it out of components without having a
literal core room. We will add tables for renderable, position, and exit

[h]Room Renderable\

<span>lllll</span> **<span>RoomID</span>&MeshID&TextureID\
r1&m1&t1\
r2&m2&t2\
r3&m3&t3\
**

\
Room Position\

<span>lllll</span> **<span>RoomID</span>&WorldPos\
r1&0,0\
r2&20,5\
r3&30,-5\
**

\
Exit Room\

<span>lllll</span> **<span>RoomID</span>\
r3\
**

\

With the new layout there is no core room. It is only implied through
the fact that it is being rendered, and that it has a position. In fact,
the last table has taken advantage of the fact that the room is now
implicit, and changed from a bool representing whether the room is an
exit room or not into a one column table. The entry in that table
implies the room is the exit room. This will give us an immediate memory
usage balance of one bool per room compared to one row per exit room.
Also, it becomes slightly easier to calculate if the player is in an
exit room, they simply check for that room’s existence in the ExitRoom
table and nothing more.

Another benefit of implicit entities is the non-intrusive linking of
existing entities. In our data file, there is no space for multiple
doors per room. With the pointer littering technique, having multiple
doors would require an array of doors, or maybe a linked list of doors,
but with the database style table of doors, we can add more rows
whenever a room needs a new door.

[h]Doors\

<span>ll</span> **<span>RoomID</span>&bf<span>RoomID</span>\
r1&r2\
r2&r3\
**

\
Locked Doors\

<span>lll</span> **<span>RoomID</span>&bf<span>RoomID</span>&Locked\
r2&r3&k1\
**

\

Notice that we have to make the primary key the combination of the two
rooms. If we had kept the single room ID as a primary key, then we could
only have one row per room. In this case we have allowed for only one
door per combination of rooms. We can guarantee in our game that a room
will only have one door that leads to another room; no double doors into
other rooms. Because of that, the locks also have to switch to a
compound key to reference locked doors. All this is good because it
means the system is extending, but by changing very little. If we
decided that we did need multiple doors from one room to another we
could extend it thus:

[h]Doors\

<span>lll</span> **<span>DoorID</span>&RoomID&RoomID\
d1&r1&r2\
d2&r2&r3\
**

\
Locked Doors\

<span>ll</span> **<span>DoorID</span>&Locked\
d2&k1\
**

\

There is one sticking point here, first normal form dictates that we
should build the table of Doors differently, where we have two columns
of doors, it requires that we have one, but multiple rows per door.

[h]Doors\

<span>ll</span> **<span>DoorID</span>&RoomID\
d1&r1\
d1&r2\
d2&r2\
d2&r3\
**

\
Locked Doors\

<span>ll</span> **<span>DoorID</span>&Locked\
d2&k1\
**

\

we can choose to use this or ignore it, but only because we know that
doors have two and only two rooms. A good reason to ignore it could be
that we assume the door opens into the first door. Thus these two room
IDs actually need to be given slightly different names, such as
*DoorInto*, and *DoorFrom*.

Sometimes, like with RoomPickups, the rows in a table can be thought of
as instances of objects. In RoomPickups, the rows represent an instance
of a PickupType in a particular Room. This is a many to many
relationship, and it can be useful in various places, even when the two
types are the same, such as in the RoomDoors table.

When most programmers begin building an entity system they start by
creating an entity type and an entity manager. The entity type contains
information on what components are connected to it, and this implies a
core entity that exists beyond what the components say about it. Adding
information about what components an entity has directly into the core
entity might help debugging for a little while, while the components are
all still centred about entities, but it becomes cumbersome when we
realise the potential of splitting and merging entities and have to move
away from using an explicit entity inspector. Entities as a replacement
for classes, have their place, and they can simplify the move from class
central thinking to a more data-oriented approach.

