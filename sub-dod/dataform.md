How is data formed?
-------------------

The games we write have a lot of data, in a lot of different formats. We
have textures in multiple formats for multiple platforms. There are
animations, usually optimised for different skeletons or types of
playback. There are sounds, lights, and scripts. Don’t forget meshes,
they now consist of multiple buffers of attributes. Only a very small
proportion of meshes are old fixed function type with vertices
containing positions, UVs, and normals. The data in games development is
hard to box, and getting harder to pin down as more ideas that were
previously considered impossible have now become commonplace. This is
why we spend a lot of time working on editors and tool chains, so we can
take the free form output from designers and artists and find a way to
put it into our engines. Without our tool-chains, editors, viewers, and
tweaking tools, there would be no way we could produce a game with the
time we have. The Object-oriented approach provides a good way to wrap
our heads around all these different formats of data. It gives a
centralised view of where each type of data belongs, and classifies it
by what can be done to it. This makes it very easy to add and use data
quickly, but implementing all these different wrapper objects takes
time. Adding new functionality to these objects can sometimes require
large refactorings as occasionally objects are classified in such a way
that they don’t allow for new features to exist. For example, in many
old engines, there was no way to upload a texture that didn’t use a 32
bit or less pixel stride. With the advent of floating point textures all
that code required a minor refactoring. In the past it was not possible
to read a texture from the vertex shader, so when texture based skinning
came along, many engine programmers had to refactor their render update.
They had to allow for a vertex shader texture upload because it might be
necessary when uploading transforms for rendering a skinned mesh. In
many engines, mesh data is optimised for rendering, but when you have to
do mesh ray casting to see where bullets have hit, or for doing IK, or
physics, then you need multiple representations of an entity, at which
point the object oriented approach starts to look cobbled together as
there are less objects that represent real things, and more objects used
as containers so programmers can think in larger building blocks. These
blocks hinder though, as they become the only blocks used in thought,
and stop potential mental connections from happening. We went from 2D
sprites, to 3D meshes following the format of the hardware provider, to
custom data streams and compute units turning the streams into rendered
triangles. Wave data, to banks, to envelope controlled grain tables and
slews of layered sounds. Tile maps, to portals and rooms, to streamed,
multiple level of detail chunks of world, to hybrid mesh palette, props,
and unique stitching assets. From flip-book, to euler angle sequences,
to quaternions and slerped anims, to animation trees and behaviour
mapping.

All these types of data are pretty common if you’ve worked in games at
all, and many engines do provide a abstraction to these more fundamental
types. When a new type of data becomes heavily used, it is promoted into
the engine as a core type. We normally consider the trade off of new
types being handled as special cases until they become ubiquitous, to be
one of usability vs performance. We don’t want to provide free access to
the lesser understood elements of game development. People who are not,
or can not, invest time in finding out how best to use new features,
should be discouraged from using them. The Object-Oriented games
development way to do that is to not provide objects that represent
them, and instead only offer the features to people who know how to
utilise the more advanced tools.

Apart from the objects representing digital assets, there are also
objects for internal game logic. For every game there are objects that
only exist to further the gameplay. Collectable card games have a lot of
textures, but they also have a lot objects for rules, card stats, player
decks, match records, even objects to represent the current state of
play. All of these objects are completely custom designed for one game.
There may be sequels, but even they could well use quite different game
logic, and therefore require different data, which would imply different
methods on the now guaranteed different objects.

Game data is complex. Any first layout of the data is inspired by the
game’s design. However, once the development is underway, it needs to
keep up with however the game evolves. Object-oriented techniques offer
a quick way to implement a given design. Object-oriented development is
quick at implementing each design in turn, but it doesn’t offer a way to
migrate from one data schema to the next. There are hacks, such as those
used in version based asset handlers, but normally, games developers
change the tool-chain and the engine at the same time, do a full
re-export of all the assets, and commit to the next version all in one
go. This can be quite a painful experience if it has to happen over
multiple sites at the same time, or if you have a lot of assets, or if
you are trying to provide engine support for more than one title, and
only one wants to change to the new revision.

There has not yet been a successful effort to build a generic game asset
solution. This is because all games differ in so many subtle ways that
if you did provide a generic solution, it wouldn’t be a game solution,
just a new language. There is no solution to be found in trying to
provide all the possible types of object that a game can use. But, there
is a solution if we go back to thinking about a game as merely running a
set of computations on some data.
