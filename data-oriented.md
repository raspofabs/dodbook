Data-Oriented Design
====================

Data-oriented design has been around for decades in one form or another,
but was only officially given a name by Noel Llopis in his September
2009 article of the same name. The idea that it is a programming
paradigm is seen as contentious as many believe that it can be used side
by side with another paradigm such as object-oriented programming,
procedural programming, or functional programming. In one respect they
are right, data-oriented design can function alongside the other
paradigms, but so can they. A Lisp programmer knows that functional
programming can coexist with object-oriented programming and a C
programmer is well aware that object-oriented programming can coexist
with procedural programming. We shall ignore these comments and claim
that data-oriented design is another important tool; a tool just as
capable of coexistence as the rest.

The time was right in 2009. The hardware was ripe for a change in how to
develop. Badly programmed potentially very fast computers, hindered by a
hardware ignorant programming paradigm made many engine programmers
weep. The times have changed, and many mobile and desktop solutions now
need the data-oriented design approach less, not because the machines
are better at mitigating ineffective programming, but the games being
designed are less demanding. As we move towards ubiquity for multi-core
machines, not just the desktops, but our phones too, and towards a world
of programming for massively parallel processing design as in the
compute cores on our graphics cards and in our consoles, the need for
data-oriented design will only grow. It will grow because abstractions
and serial thinking will be the bottleneck of your competitors, and
those that embrace the data-oriented approach will thrive.

It’s all about the data
-----------------------

Data is all we have. Data is what we need to transform in order to
create a user experience. Data is what we load when we open a document.
Data is the graphics on the screen and the pulses from the buttons on
your game pad and the cause of your speakers and headphones producing
waves in the air and the method by which you level up and how the bad
guy knew where you were to shoot at you and how long the dynamite took
to explode and how many rings you dropped when you fell on the spikes
and the current velocity of every particle in the beautiful scene that
ended the game, that was loaded off the disc and into your life. Any
application is nothing without its data. Photoshop without the images is
nothing. Word is nothing without the characters. Cubase is worthless
without the events. All the applications that have ever been written
have been written to output data based on some input data. The form of
that data can be extremely complex, or so simple it requires no
documentation at all, but all applications produce and need data.

Instructions are data too. Instructions take up memory, use up
bandwidth, and can be transformed, loaded, saved and constructed. It’s
natural for a developer to not think of instructions as being data[^1],
but there is very little differentiating them on older, less protective
hardware. Even though memory set aside for executables is protected from
harm and modification on most contemporary hardware, this relatively new
invention is still merely an invention. Instructions are still data, and
once more, they are what we transform too. We take instructions and turn
them into actions. The number, size, and frequency of them is something
that matters and that we have control over.

This forms the basis of the argument for a data-oriented approach to
development, but leaves out one major element. All this data and the
transforming of data, from strings, to images, to instructions, they all
have to run on something. Sometimes that thing is quite abstract, such
as a virtual machine running on unknown hardware. Sometimes that thing
is concrete, such as knowing which specific CPU and what speed and
memory capacity and bandwidth you have available. But in all cases, the
data is not just data, but data that exists on some hardware somewhere,
and it has to be transformed by some hardware. In essence, data-oriented
design is the practice of designing software by developing transforms
for well formed data where well formed is guided by the target hardware
and the transforms that will operate on it. Sometimes the data isn’t
well defined, and sometimes the hardware is equally evasive, but in most
cases a good background of hardware appreciation can help out almost
every software project.

If the ultimate result of an application is data, and all input can be
represented by data, and it is recognised that all data transforms are
not performed in a vacuum, then a software development methodology can
be founded on these principles, the principles of understanding the
data, and how to transform it given some knowledge of how a machine will
do what it needs to do with data of this quantity, frequency, and it’s
statistical qualities. Given this basis, we can build up a set of
founding statements about what makes a methodology data-oriented.

Data is not the problem domain
------------------------------

The first principle: Data is not the problem domain.

For some, it would seem that data-oriented design is the antithesis of
most other programming paradigms because data-oriented design is a
technique that does not readily allow the problem domain to enter into
the software so readily. It does not recognise the concept of an object
in any way, as data is consistently without meaning, whereas the
abstraction heavy paradigms try to pretend the computer and its data do
not exist at every turn, abstracting away the idea that there are bytes,
or CPU pipelines, or other hardware features.

The data-oriented design approach doesn’t build the real world problem
into the code. This could be seen as a failing of the data-oriented
approach by veteran object-oriented developers, as many examples of the
success of object-oriented design come from being able to bring the
human concepts to the machine, then in this middle ground, a solution
can be written in this language that is understandable by both human and
computer. The data-oriented approach gives up some of the human
readability by leaving the problem domain in the design document, but
stops the machine from having to handle human concepts at any level by
just that same action.

Let us consider first how the problem domain becomes part of the
software in programming paradigms that promote abstraction. In the case
of objects, we tie meanings to data by associating them with their
containing classes and their associated functions. In high level
abstraction, we separate actions and data by high level concepts, which
might not apply at the low level, thus reducing the likelihood that the
functions will be efficiently implemented.

When a class owns some data, it gives that data a context, and that
context can sometimes limit the ability to reuse the data. Adding
functions to a context can bring in further data, which quickly leads to
classes that contain many different pieces of data that are unrelated in
themselves, but need to be in the same class because an operation
required a context, but the operation also required additional data.
Normally this becomes hard to untangle as functions that operate over
the whole context drag in random pieces of data from all over the class
meaning that many data items cannot be removed as they would then be
inaccessible.

When we consider the data from the data-oriented design point of view,
data is mere facts that can be interpreted in whatever way necessary to
get the output data in the format it needs to be. We only care about
what transforms we do, and where the data ends up. In practice, when you
discard meanings from data, you also reduce the chance of tangling the
facts with their contexts, and thus you also reduce the likelihood of
mixing unrelated data just for the sake of an operation or two.

Data and Statistics
-------------------

The second principle: Data is type, frequency, quantity, shape and
probability.

The second statement is that data is not just the structure. A common
misconception about data-oriented design is that it’s all about cache
misses. Even if it was all about making sure you never missed the cache,
and it was all about structuring your classes so the hot and cold data
was split apart, it would be a generally useful addition to your toolkit
of thought, but data-oriented design is about all aspects of the data.
To write a book on how to avoid cache misses, you need more than just
some tips on how to organise your structures, you need a grounding in
what is really happening inside your computer when it is running your
program. Teaching that in a book is also impossible as it would only
apply to one generation of hardware, and one generation of programming
languages, however data oriented design is not rooted in one language
and one set of hardware. The schema of the data is still important, but
the actual values are as important, if not more so. It is not enough to
have some photographs of a cheetah to determine how fast it can run. You
need to see it in the wild.

The data-oriented design model is centred around data, live data, real
data, information data. Object-oriented design is centred around the
problem and its solution. Objects, not real things, but abstract
representations of things that make up the design of the solution to the
problem presented in the application design document. The objects only
manipulate the data needed to represent them without any consideration
for the hardware or the real world data patterns or quantities. This is
why object-oriented design allows you to quickly build up first versions
of applications, allowing you to put the first version of the design
document or problem definition directly into the code.

Data-oriented design takes a different approach to the problem, instead
of assuming that we know nothing about the hardware, it assumes we know
nothing about the problem. Anyone who has written a sizable piece of
software should recognise that the technical design for any project can
change so much that there is hardly anything recognisable from the first
draft in the final implementation. Data-oriented design avoids this
waste of resources by never assuming that the design needs to exist
anywhere other than in a document while it proceeds to provide a
solution to the current problem.

Data-Oriented Design takes it’s cues from the data that is seen or
expected. Instead of planning for all eventualities, or planning to make
things adaptable, it uses the most probable input to direct the choice
of algorithm. Instead of planning to be extendible, it plans to be
simple, and get the job done. Extendible can be added later, with the
safety net of unit tests to ensure that it remains working as it did
while it was simple.

Data changes
------------

Data-oriented design is current. Object-oriented design starts to show
its weaknesses when designs change. Object-oriented design suffers from
an inertia inherent in keeping the problem domain coupled with the
implementation. A data-oriented approach to design takes note of the
change in design by understanding the change in the data. The
data-oriented approach to design also allows for change to the code when
the source of data changes, unlike the encapsulated internal state
manipulations of the object-oriented approach. In general, data-oriented
design handles change better as pieces of data and transforms can be
more simply coupled and decoupled than objects can be mutated and
reused.

The reason this is so comes from the linking of intention and aspect
that comes with lumping data and functions in with concepts of objects
where the objects are the schema, the aspect, the use case, and the real
world or design counterpart to the code. If you link your data
manipulations to your data then you make it hard to unlink data related
by operation. If you link your operations by related data, then you make
it hard to unlink your operations when the data changes or splits. If
you keep your data in one place, write operations in another place, and
keep the aspects and roles of data intrinsic from how the operations and
transforms are applied to the data, then you will find that many
refactorings that would have been large and difficult in object oriented
code, become trivial. With this benefit comes a cost of keeping tabs on
what data is required for each operation, and the potential danger of
desynchronisation. This consideration can lead to keeping some cold code
in an object oriented style where objects are responsible for
maintaining internal consistency over efficiency and mutability.

A big misunderstanding for many new to the data-oriented design
paradigm, a concept brought over from abstraction based development, is
that we can design a static library or set of templates to provide
generic solutions to everything presented in this book as a
data-oriented solution. The awful truth is that data, though it can be
generic by type, is not generic in any real world sense. The values are
different, and often contain patterns that we can turn to our advantage.
How would it be possible to do compression if it were not for patterns?
Our runtime code can also benefit from this but it is overlooked as
being not object-oriented, or being too hard coded. It can be better to
hard code a transform than pretend it’s not hard coded by wrapping it in
a generic container and using the wrong algorithms on it. Using existing
templates like this provide a known benefit of a minor increase in
readability to those who already know of the library, and potentially
less bugs if the functionality was in some way generic. But, if the
functionality was not very well mapped to the existing generic solution,
writing it with a templated function and then extending would possibly
make the code harder to read by hiding the fact that the technique had
been changed subtly. Hard coding a new algorithm is frequently a better
choice as long as it has sufficient tests, and tests are easier to write
if you constrain yourself to the facts about the data, and only work
with simple data and not stateful objects.

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

What can provide a computational framework for such complex data?
-----------------------------------------------------------------

Games developers are notorious for thinking about games development from
either a low level all out performance perspective, or from a very high
level gameplay and interaction perspective. This may have come about
because of the widening gap between the amount of code that has to be
performant, and the amount of code to make the game complete.
Object-oriented techniques provide good coverage of the high level
aspect, and the assembler gurus have been hacking away at performance
for so long even their beards have beards. There has never been much of
a middle ground in games development, which is probably why the
structure and performance techniques employed by big-iron companies
never seemed useful. When games development was first flourishing in the
late 1990’s, academic or corporate software engineering practices were
seen as suspicious because wherever they were employed, there was a
dramatic drop in game performance, and whenever any prospective
employees came from those industries, they never managed to impress. As
games machines became more like standard micro-computers, and standard
micro-computers became more similar to the mainframes of old, the more
obvious it became that standard professional software engineering
practices could be useful. Now the scale of games has grown to match the
hardware, and with each successive generation, the number of man hours
to develop a game has grown exponentially, which is why project
management and software engineering practices have become de-facto at
the larger games companies. There was a time when games developers were
seen as cutting edge programmers, inventing new technology as the need
arises, but with the advent of less adventurous hardware (most notably
in the x86 based XBox, and it’s only mildly interesting successor),
there has been less call for ingenious coding practices, and more call
for a standardised process. This means that game development can be
tuned to ensure the release date will coincide with marketing dates.
There will always be an element of randomness in high profile games
development because there will always be an element of innovation that
virtually guarantees that you will not be able to predict how long the
project, or at least one part of the project, will take.

Part of the difficulty in adding new and innovative features to a game
is the data layout. If you need to change the data layout for a game, it
will need objects to be redesigned or extended in order to work within
the existing framework. If there is no new data, then a feature might
require that previously separate systems suddenly be able to talk to
each other quite intimately. This coupling can often cause system wide
confusion with additional temporal coupling and corner cases so obscure
they can only be found one time in a million. This sounds fine to some
developers, but if you’re expecting to sell five to fifty million copies
of your game, that’s five to fifty people who can take a video of your
game, post it on the internet, and call your company rubbish because
they hadn’t fixed an obvious bug.

Big iron developers had these same concerns back in the 1970’s. Their
software had to be built to high standards because their programs would
frequently be working on data that was concerned with real money
transactions. They needed to write business logic that operated on the
data, but most important of all, they had to make sure the data was
updated through a provably careful set of operations in order to
maintain its integrity. Database technology grew from the need to
process stored data, to do complex analysis on it, to store and update
it, and be able to guarantee that it was valid at all times. To do this,
the ACID test was used to ensured atomicity, consistency, isolation, and
durability. Atomicity was the test to ensure that all transactions would
either complete, or do nothing. It could be very bad for a database to
update only one account in a financial transaction. There could be money
lost, or created if a transaction was not atomic. Consistency was added
to ensure that all the resultant state changes that should happen during
a transaction do happen, that is, all triggers that should fire, do,
even if the triggers cause triggers, with no limit. This would be highly
important if an account should be blocked after it has triggered a form
of fraud detection. If a trigger has not fired, then the company using
the database could risk being liable for even more than if they had
stopped the account when they first detected fraud. Isolation is
concerned with ensuring that all transactions that occur cannot cause
any other transactions to differ in behaviour. Normally this means that
if two transactions appear to work on the same data, they have to queue
up and not try to operate at the same time. Although this is generally
good, it does cause concurrency problems. Finally, durability. This was
the second most important element of the four, as it has always been
important to ensure that once a transaction has completed, it remains
so. In database terminology, durability meant that the transaction would
be guaranteed to have been stored in such a way that it would survive
server crashes or power outages. This was important for networked
computers where it would be important to know what transactions had
definitely happened when a server crashed or a connection dropped.

Modern network games also have to worry about highly important data like
this, especially with non-free downloadable content, and even more so
with consumable downloadable content. To provide much of the
functionality required of the database ACID test, games developers have
gone back to looking at how databases were designed to cope with these
strict requirements and found reference to staged commits, idempotent
functions, techniques for concurrent development and a vast literature
base on how to design tables for a database.

Databases provide a way to store highly complex data in a structured way
while providing a simple to learn language for transforming and
generating reports based on that data. The language, SQL, invented in
the 1970’s by Donald D. Chamberlin and Raymond F. Boyce at IBM, provides
a method by which it is possible to store computable data while also
maintaining data relationships. But, games don’t have simple computable
data, they have classes and objects. Database technology doesn’t work
for the Object-oriented approach that games developers use.

The data in games can be highly complex, it doesn’t neatly fit into
database rows. Not all objects can fit into rows of columns. Try to find
the right table columns to describe a level file. Try to find the right
columns to describe a car in a racing game, do you have a column for
each wheel? Do you have a column for each collision primitive, or just a
column for the collision mesh?

The obvious answer is that game data just doesn’t fit into the database
way of thinking. However, that’s only because we’ve not normalised the
data. We’ll stick with a level file for a while as we find out how years
old techniques can provide a very useful insight into what game data is
really doing. There are some types of data where it doesn’t make sense
to move into databases, such as the raw assets (sounds, textures, vertex
buffers etc.) but these can be seen as primitives, much like the
integers, floating point numbers, strings and boolean values we shall be
working with.

What we shall discover is that everything we did was already in a
database, but it wasn’t obvious to us because of how we store our data.
The structure of our data is a trade-off against performance,
readability, maintenance, future proofing, extendibility and reuse. The
most flexible database in common use is the file-system. It has one
table with two columns. A primary key of the file path, and a string for
the data. This simplest database system is the perfect fit for a
completely future proof system. The more complex the tables get, the
less future proof, and the less maintainable, but the higher the
performance and readability. For example, a file has no documentation of
its own, but the schema of a database could be all that is required to
understand a sufficiently well designed database. That’s how games don’t
even appear to have databases. They are so complex for the sake of
performance that they have forgotten that they are merely a data
transform.

[^1]: unless they are a Lisp programmer
