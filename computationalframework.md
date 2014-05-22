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
