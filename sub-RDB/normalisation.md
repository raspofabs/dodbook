Normalisation
-------------

First normal form requires that every row be distinct and rely on the
key. We haven’t got any keys yet, so first we must find out what these
are.

In any table, there is a set of columns that when compared to any other
row, are unique. Databases guarantee that this is possible by not
allowing complete duplicate rows to exist, there is always some
differentiation. Because of this rule, every table has a key because
every table can use all the columns at once as its primary key. For
example, in the mesh table, the combination of meshID and filename is
guaranteed to be unique. The same can be said for the textureID and
filename in the textures table. In fact, if you use all the columns of
the room table, you will find that it can be used to uniquely define
that room (obviously really, as if it had the same key, it would in fact
be literaly describing the same room, but twice).

Going back to the mesh table, because we can guarantee that each meshID
is unique in our system, we can reduce the key down to just one or the
other or meshID or filename. We’ll choose the meshID as it seems
sensible, but we could have chosen the filename[^2].

If we choose textureID, pickupID, and roomID as the primary keys for the
other tables, we can then look at continuing on to first normal form.

[h]Meshes\

<span>ll</span> **<span>MeshID</span>&MeshName\
m1&“filename”\
m2&“filename2”\
**

Textures\

<span>ll</span> **<span>TextureID</span>&TextureName\
t1&“texturefile”\
t2&“texturefile2”\
**

Pickups\

<span>lllll</span>
**<span>PickupID</span>&MeshID&TextureID&PickupType&ColourTint\
k1&m5&t5&KEY&Gold\
k2&m6&t6&POTION&(null)\
**

Rooms\

<span>lllllll</span>
**<span>RoomID</span>&MeshID&TextureID&WorldPos&Pickup1&Pickup2&...\
r1&m1&t1&0,0&k1&k2&...\
r2&m2&t2&20,5&(null)&(null)&...\
r3&m3&t3&30,-5&(null)&(null)&...\
**

  ...   Trapped   DoorTo   Locked   Start    Exit
  ----- --------- -------- -------- -------- -------
  ...   10hp      r2       (null)   (null)   false
  ...   (null)    r3       k1       22,7     false
  ...   (null)    (null)   (null)   (null)   true

### 1^st^ Normal Form

First normal form can be described as making sure the tables are not
sparse. We require that there be no null pointers and that there be no
arrays of data in each element of data. This can be performed as a
process of moving the repeats and all the optional content to other
tables. Anywhere there is a null, it implies optional content. Our first
fix is going to be the Pickups table, it has an optional ColourTint
element. We invent a new table PickupTint, and use the primary key of
the Pickup as the primary key of the new table.

[h]Pickups\

<span>llll</span> **<span>PickupID</span>&MeshID&TextureID&PickupType\
k1&m5&t5&KEY\
k2&m6&t6&POTION\
**

\
PickupTint\

<span>ll</span> **<span>PickupID</span>&**<span>ColourTint</span>\
k1&Gold\
****

two things become evident at this point, firstly that normalisation
appears to create more tables and less columns in each table, secondly
that there are only rows for things that matter. The latter is very
interesting as when using Object-oriented approaches, we assume that
objects can have attributes, so check that they are not NULL before
continuing, however, if we store data like this, then we know everything
is not NULL. Let’s move onto the Rooms table: make a new table for the
optional Pickups, Doors, Traps, and Start.

[h]Rooms\

<span>lllll</span> **<span>RoomID</span>&MeshID&TextureID&WorldPos&Exit\
r1&m1&t1&0,0&false\
r2&m2&t2&20,5&false\
r3&m3&t3&30,-5&true\
**

\
Room Pickup\

<span>lll</span> **<span>RoomID</span>&Pickup1&Pickup2\
r1&k1&k2\
**

\
Rooms Doors\

<span>lll</span> **<span>RoomID</span>&DoorTo&Locked\
r1&r2&(null)\
r2&r3&k1\
**

\
Rooms Traps\

<span>ll</span> **<span>RoomID</span>&Trapped\
r1&10hp\
**

\
Start Point\

<span>ll</span> **<span>RoomID</span>&Start\
r2&22,7\
**

We’re not done yet, the RoomDoors table has a null in it, so we add a
new table that looks the same as the existing RoomDoorTable, but remove
the row with a null. We can now remove the Locked column from the
RoomDoor table.

[h]Rooms Doors\

<span>ll</span> **<span>RoomID</span>&DoorTo\
r1&r2\
r2&r3\
**

\
Rooms Doors Locks\

<span>lll</span> **<span>RoomID</span>&DoorTo&Locked\
r2&r3&k1\
**

All done. But, first normal form also mentions no repeating groups of
columns, meaning that the PickupTable is invalid as it has a pickup1 and
pickup2 column. To get rid of these, we just need to move the data
around like this:

[h]Room Pickup\

<span>ll</span> **<span>RoomID</span>&**<span>Pickup</span>\
r1&k1\
r1&k2\
****

Notice that now we don’t have a unique primary key. This is an error in
databases as they just have to have something to index with, something
to identify a row against any other row. We are allowed to combine keys,
and for this case we used the all column trivial key. Now, let’s look at
the final set of tables in 1NF:

[h]Rooms\

<span>lllll</span> **<span>RoomID</span>&MeshID&TextureID&WorldPos&Exit\
r1&m1&t1&0,0&false\
r2&m2&t2&20,5&false\
r3&m3&t3&30,-5&true\
**

\
Room Pickup\

<span>ll</span> **<span>RoomID</span>&**<span>Pickup</span>\
r1&k1\
r1&k2\
****

\
Rooms Doors\

<span>ll</span> **<span>RoomID</span>&DoorTo\
r1&r2\
r2&r3\
**

\
Rooms Doors Locks\

<span>lll</span> **<span>RoomID</span>&DoorTo&Locked\
r2&r3&k1\
**

\
Rooms Traps\

<span>ll</span> **<span>RoomID</span>&Trapped\
r1&10hp\
**

\
Start Point\

<span>ll</span> **<span>RoomID</span>&Start\
r2&22,7\
**

The data, in this format takes much less space in larger projects as the
number of NULL entries would have only increased with increased
complexity of the level file. Also, by laying out the data this way, we
can add new features without having to revisit the original objects. For
example, if we wanted to add monsters, normally we would not only have
to add a new object for the monsters, but also add them to the room
objects. In this format, all we need to do is add a new table:

[h]Monster\

<span>llll</span> **<span>MonsterID</span>&Attack&HitPoints&StartRoom\
M1&2&5&r1\
M2&2&5&r3\
**

And now we have information about the monster and what room it starts in
without touching any of the original level data.

### Reflections

What we see here as we normalise our data is a tendency to add
information when it becomes necessary, but at a cost of the keys that
associate the data with the entity. Looking at many third party engines
and APIs, you can see parallels with the results of these
normalisations. It’s unlikely that the people involved in the design and
evolution of these engines took their data and applied database
normalisation techniques, but sometimes the separations between object
and componets of objects can be obvious enough that you don’t need a
formal technique in order to realise some positive structural changes.

In some games the entity object is not just an object that can be
anything, but is instead a specific subset of the types of entity
involved in the game. For example, in one game there might be an object
type for the player character, and one for each major type of enemy
character, and another for vehicles. This object oriented approach puts
a line, invisilbe to the player, but intrusive to the developer, between
classes of object and instances. It is intrusive because every time a
class definition is used instead of a differing data, the amount of code
required to utilise that specific entity type in a given circumstance
increases. In many codebases there is the concept of the player, and the
player has different attributes to other entities, such as lacking AI
controls, or having player controls, or having regenerating health, or
having ammo. All these different traits can be inferred from data
decisions, but sometimes they are made literal through code in classes.
When these differences are put in code, interfacing between different
classes becomes a game of adapting, a known design pattern that should
be seen as a symptom of mixed levels of specialisation in a set of
classes. When developing a game, this ususally manifests as time spent
writing out templated code that can operate on multiple classes rather
than refactoring the classes involved into more discrete components.
This could be considered wasted time as the likelyhood of other
operations needing to operate on all the objects is greater than zero,
and the effort to refactor into components is usually no greater than
the effort to create a working templated operation.

### Domain Key / Knowledge

Whereas first normal form is almost a mechanical process, 2nd Normal
form and beyond become a little more investigative. It is required that
the person doing the normalisation understand the data in order to
determine whether parts of the data are dependent on the key and whether
or not they would be better suited in a new table, or written out as a
form of procedural result due to domain knowledge.

Domain key normal form is normally thought of as the last normal form,
but for developing efficient data structures, it’s one of the things
that is best studied early and often. The term domain knowledge is
preferrable when writing code as it makes more immediate sense and
encourages use outside of keys and tables. Domain knowledge is the idea
that data depends on other data, given information about the domain in
which it resides. Domain knowledge can be as simple as knowing the
collowquialism for something, such as knowing that a certain number of
degrees Celsius or Fahrenheit is hot, or whether some SI unit relates to
a man-made concept such as 100m/s being rather quick. These procedural
solutions are present in some operating systems or applications: the
progress dialogue that may say “about a minute” rather than an
innaccurate and erratic seconds countdown. Hoever, domain knowledge
isn’t just about human interpretation of data. For example things such
as boiling point, the speed of sound, of light, speed limits and average
speed of traffic on a given road network, psychoacoustic properties, the
boiling point of water, and how long it takes a human to react to any
given visual input. All these facts may be useful in some way, but can
only be put into an application if the programmer adds it specifically
as procedural domain knowledge or as an attribute of a specific
instance.

Domain knowledge is useful because it allows us to lose some otherwise
unnecessarily stored data. It is a compiler’s job to analyse the
produced output of code (the abstract syntax tree) to then provide
itself with data upon which it can infer and use domain knowledge about
what operations can be omitted, reordered, or transformed to produce
faster or cheaper assembly. Profile guided optimisation is another way
of using domain knowledge, the domain being the runtime, the knowledge
being the statistics of instructino coverage and order of calling. PGO
is used to tune the location of instructions and hint branch predictors
so that they produce even better performance based on a real world use
case.

### All Normal Forms

First normal form: remove repeating columns and nulls by adding new
tables for optional values or one to may relationships. That is, ensure
that any potentially null columns in your table are moved to their own
table and use the primary table’s key as their primary key. Move any
repeating columns (such as item1, item2, item3) to a separate single
table (item) and again use the original table’s primary key as the
primary key for this new table.

Second, Third, and BC (Boyce-Codd) normal form: split tables such that
changes to values only affect the minimum amount of tables. Make sure
that columns rely on only the table key, and also all of the table key.
Look at all the columns and be sure that each one relies on all of the
key and not on any other column.

Fourth normal form: ensure that your tables columns are truly dependent
on each other. An example might be keeping a table of potential colours
and sizes of clothing, with an entry for each colour and size
combination. Most clothes come in a set of sizes, and a set of colours,
and don’t restrict certain colours based on size so there would be no
omissions from a matrix of all the known sizes and all the known
colours, instead the table should be two tables, both with the garment
as primary key, with size or colour as the data. This holds for
specifications, but doesn’t hold for the case where an item needs to be
checked for whether or not it is in stock. Not all sizes and colour
combinations may be in stock, so an “in-stock” cache table would be
right to have all three columns.

Fifth normal form: if the values in multiple columns are related by
possibility, then remove the columns out into the separate tables of
possible combinations. For example, an Ork can use simple weapons or
orcish weapons, a human can use simple weapons or human weapons, if we
say that Human Arthur is using a stick, then the stick doesn’t need the
column specifying that it is an simple weapon, but equally, if we say
the Ork KruelGut is using a sword, we don’t need a column specifying
that he is using an orcish sword, as he cannot use a human sword and
that is the only other form of sword available. In this case then we
have a table that tells us what each entity is using for a weapon (we
know what race each entity is in another table), and we have a table for
what weapon types are available per race, and the weapon table can still
have both weapontype and actual weapon. The benefit of this is that the
entities only need to maintain a lower range “weapon” and not also the
weapontype as the weapontype can be inferred from the weapontypes
available for the race. This reduction in memory useage may come at a
cost of performance, or may increase performance depending on how the
data is accessed.

Sixth normal form: This is an uncommon normal form because it is one
that is normally only important for keeping track of changing states and
can cause an explosion in the number of tables. However, it can be
useful in reducing memory usage when tracking rapidly changing
independent columns of an otherwise fully normalised table. For example,
if a character is otherwise fully normalised, but they need to keep
track of how much money, XP, and spell points they have over time, it
might be better to split out the money, XP, and spell points columns
into character/time/value tables that can be separately updated without
causing a whole new character record to be written purely for the sake
of time stamping.

Domain/Key normal form: using domain knowledge remove columns or parts
of column data because it depends on some other colum through some
intrinsic quality of the domain in which the table resides. Information
provided by the data may already be available in other data. For eaxmple
the colloquialism of old-man is dependent on having data on the gender
column and age colum, and can be inferred. Thus it doesn’t need to be in
a column and instead can live as a process. Equally, foreshadowing
existence based processing here, a dead ork has zero health and a unhurt
ork has zero damage. If we maintain a table for partially damaged orks
health values then we don’t need storage space undamaged ork health.
This minor saving can add up to large savings when operating on multiple
entities with multiple stats that can vary from a known default.

### Sum up

At this point we can see it is perfectly reasonable to store any highly
complex data structures in a database format, even game data with its
high interconnectedness and rapid design changing criteria. What is
still of concern is the less logical and more binary forms of data such
as material data, mesh data, audio clips and runtime integration with
scripting systems and control flow.

Platform specific resources such as audio, texture, vertex or video
formats are opaque to most developers, and moving towards a table
oriented approach isn’t going to change that. In databases, it’s common
to find column types of boolean, number, and string, and when building a
database that can handle all the natural atomic elements of our engine,
it’s reasonable to assume that we can add new column types for these
platform or engine intrinsics. The textureID and meshID column used in
room examples could be smart pointers to resources. Creating new meshes
and textures may be as simple as inserting a new row with the asset URL
and keeping track of whether or not an entry has arrived in the
fulfilled streaming request table or the URL to assetID table that could
be populated by a behind the scenes task scheduler.

As for integration with scripting systems and using tables for logic and
control flow, chapters on finite state machines, existence based
processing, condition tables and hierarchical level of detail show how
tables don’t complicate, but instead provide opportunity to do more with
fewer resources as results flow without constraint normally associated
with object or entity linked data structures.

[^2]: in fact, the filename is the primary key of the filedata on the
    storage media, filesystems are simple key-value databases with very
    large complex/large values
