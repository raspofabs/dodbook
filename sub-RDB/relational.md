How does relational data differ?
---------------------------

We now examine how it is possible to put game data into a relational form.
First we must give ourselves a level file to work with. We’re not going
to go into the details of the lowest level of how we utilise large data
primitives such as meshes, textures, sounds and such. For now, think of
assets as being the same kind of data as strings[^1].

We’re going to define a level file for a game where you hunt for keys to
unlock doors in order to get to the exit room. The level file will be a
list of different game objects that exist in the game, and the
relationships between the objects. First, we’ll assume that it contains
a list of rooms (some trapped, some not), with doors leading to other
rooms which can be locked. It will also contain a set of pickups, some
that let the player unlock doors, some that affect the player’s stats
(like health potions), and all the rooms have lovely textured meshes, as
do all the pickups. One of the rooms is marked as the exit, and one has
a player start point.

~~~~ {caption="A" setup="" script=""}
// create rooms, pickups, and other things.
m1 = mesh( "filename" )
m2 = mesh( "filename2" )
t1 = texture( "textureFile" )
t2 = texture( "textureFile2" )
k1 = pickup( TYPE_KEY, m5,t5, TintColourGold )
k2 = pickup( TYPE_POTION, m4,t4, null )
r1 = room( worldPos(0,0), m1, t1, hasPickup(k1)+hasTrap(true,10hp)+hasDoorTo(r2) )
r2 = room( worldPos(20,5), m2,t2, hasDoorTo(r3,lockedWith(k1)+isStart(worldPos(22,7) )
r3 = room( worldPos(30,-5), m3,t3, isExit() )
~~~~

[src:roomscript]

In the first step, you take all the data from the object creation
script, and fit it into rows in your table. To start with, we create a
table for each type of object, and a row for each instance of those
obejcts. We need to invent columns as necessary, and use NULL everywhere
that an instance doesn’t have that attribute/column.

[h]Meshes\

  MeshID   MeshName
  -------- -------------
  m1       “filename”
  m2       “filename2”

Textures\

  TextureID   TextureName
  ----------- ----------------
  t1          “texturefile”
  t2          “texturefile2”

Pickups\

  MeshID   TextureID   PickupType   ColourTint   PickupID
  -------- ----------- ------------ ------------ ----------
  m5       t5          KEY          Gold         k1
  m6       t6          POTION       (null)       k2

Rooms\

  RoomID   MeshID   TextureID   WorldPos   Pickup1   Pickup2   ...
  -------- -------- ----------- ---------- --------- --------- -----
  r1       m1       t1          0,0        k1        k2        ...
  r2       m2       t2          20,5       (null)    (null)    ...
  r3       m3       t3          30,-5      (null)    (null)    ...

  ...   Trapped   DoorTo   Locked   Start    Exit
  ----- --------- -------- -------- -------- -------
  ...   10hp      r2       (null)   (null)   false
  ...   (null)    r3       k1       22,7     false
  ...   (null)    (null)   (null)   (null)   true

[tab:initialtables]

Once we have taken the construction script and generated tables, we find
that these tables contain a lot of nulls. The nulls in the rows replace
the optional content of the objects. If an object instance doesn’t have
a certain attributes then we replace those features with nulls. When we
plug this into a database, it will handle it just fine, but storing all
the nulls seems unnecessary and looks like it’s wasting space. Present
day database technology has moved towards keeping nulls to the point
that a lot of large, sparse table databases have many more null entries
than they have data. They operate on these sparsely filled tables with
functional programming techniques. We, however should first see how it
worked in the past with relational databases. Back when SQL was first
invented there were three known stages of data normalisation (there
currently are six recognised numbered normal forms, plus BoyceCodd
(which is a stricter variant of third normal form), and Domain Key
(which, for the most part defines a normalisation which requires using
domain knowledge instead of storing data).

[^1]: There are existing APIs that present strings in various ways
    dependent on how they are used, for example the difference between
    human readable strings (usually UTF-8) and ascii strings for
    debugging. Adding sounds, textures, and meshes to this seems quite
    natural once you realise that all these things are resources for
    human consumption

