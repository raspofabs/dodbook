Searching
=========

When looking for specific data, it’s very important to remember why
you’re doing it. If the search is not necessary, then that’s your
biggest possible saving. Finding if a row exists in a table will be slow
if approached naively. You can manually add searching helpers such as
binary trees, hash tables, or just keep your table sorted by using
ordered insertion whenever you add to the table. If you’re looking to do
the latter, this could slow things down, as ordered inserts aren’t
normally concurrent, and adding extra helpers is normally a manual task.
In this section we find ways to combat all these problems.

Indexes
-------

Database management systems have long held the concept of indexes. They
are traditionally automatically added when a database management system
notices that a particular query has been run a large number of times. We
can use this idea and implement a just-in-time indexing system in our
games to provide the same kinds of performance improvement. Every time
you want to find out if an element exists, or even just generate a
subset, like when you need to find all the entities in a certain range,
you will have to build it as a pocess to generate a row or table, but
the process that causes the row or table generation can be thought of as
an object that can transform itself dependent on the situation. Starting
out as a simple linear search query (if the data is not already sorted),
the process can find out that it’s being used quite often through
internal telemetry, and proably be able to discover that it’s generally
returns a simply tunable set of results, such as the first N items in a
sorted list, and can hook itself into the tables that it references.
Hooking into the insertion, modification, and deletion would allow the
query to update itself rather than run the full query again. This can be
a significant saving, but it can also be useful as it is optional. As
it’s optional, it can be garbage collected.

If we build generalised back ends to handle building queries into these
tables, they can provide multiple benefits. Not only can we provide
garbage collection of indexes that aren’t in use, but they can also make
the programs in some way self documenting and self profiling. If we
study the logs of what tables had pushed for building indexes for their
queries, then we can quickly see data hotspots and where there is room
for improvement. The holy grail here is self optimising code.

data-oriented Lookup
--------------------

The first step in any data-oriented approach to searching is to
understand the difference between the key, and the data that is
dependent on the key. Object-oriented solutions to searching often ask
the object whether or not it satisfies some criteria. Because the object
is asked a question, there is often a large amount of code called,
memory indirectly accessed, and cache-lines filled but hardly used. Even
in a non-Object-oriented approach, there is frequently still a lot of
cache abuse. Following is a listing for a simple binary search for a key
in a naive implementation of an animation container. This kind of data
access pattern is common in animation, hash lookups, and other spatial
searches.

~~~~ {caption="Binary" search="" for="" a="" given="" time="" value=""}
struct AnimKey {
    float time;
    float x,y,z;
};
struct Anim {
    int numKeys;
    AnimKey *keys;
    AnimKey *GetKeyAtTime( float t ) {
        int l = 0, h = numKeys-1;
        int m = (l+h) / 2;
        while( l < h ) {
            if( keys[m].time > t )
                h = m;
            else
                l = m;
            m = (l+h) / 2;
        }
        return keys[i];
    }
};
~~~~

We can improve on this very quickly by moving to a structure of arrays.
What follows is a quick rewrite that saves us a lot of memory access.

~~~~ {caption="Binary" search="" for="" a="" given="" time="" value=""}
struct AnimKey {
    float x,y,z;
};
struct Anim {
    int numKeys;
    float *keyTime;
    AnimKey *keys;
    AnimKey *GetKeyAtTime( float t ) {
        int l = 0, h = numKeys-1;
        int m = (l+h) / 2;
        while( l < h ) {
            if( keyTime[m] > t )
                h = m;
            else
                l = m;
            m = (l+h) / 2;
        }
        return keys[i];
    }
};
~~~~

Using the data-oriented SoA, we speed this up, but why is it faster? The
first impression most people get is that we’ve moved from a nice solid
16byte structure to a horrible or padded 12byte structure for the
animation keys. Sometimes it pays to think a bit further than what looks
right as first glance. Primarily, we are now finding the key by hunting
for a value in a list of values. Not looking for a whole struct by one
of its members in an array of structs. This is faster because the cache
will be filled with mostly pertinent data. There are ways to organise
the data better still, but any more optimisation requires a complexity
or space time trade off. A basic binary search will home in on the
correct data quite quickly, but each of the first steps will cause a new
cache-line to be read in. If you know how big your cache-line is, then
you can check all the values that have been loaded for free while you
wait for the next cache-line to load in. Once you have got near the
destination, most of the memory you need is in memory and all you’re
doing from then on is making sure you have found the right key. In a
good SoA engine, all this can be done behind the scenes with a well
optimised search algorithm usable all over the game code. It is worth
mentioning again, that every time you break out into larger data
structures, you deny your proven code the chance to be reused.

If the reason for a search is simpler, such as checking for existence,
then there are even faster alternatives. Bloom filters offer a constant
time lookup that even though it produces some false positives, can be
tweaked to generate a reasonable answer hit rate for very large sets. In
particular, if you are checking for which table an row exists in, then
bloom filters work very well, by providing data about which tables to
look in, usually only returning the correct table, but sometimes more
than one.

In relational databases, indexes are added to tables at runtime when
there are multiple queries that could benefit in their presence. For our
data-oriented approach, there will always be some way to speed up a
search but only by looking at the data. If the data is not already
sorted, then an index is a simple way to find the specific item we need.
If the data is already sorted, but needs even faster access, then a
search tree optimised for the cache-line size would help.

A binary search is one of the best search algorithms for using the
smallest number of instructions to find a key value. But if you want the
fastest algorithm, you must look at what takes time, and a lot of the
time, it’s not instructions. Loading a whole cache-line or information
and doing as much as you can with that would be a lot more helpful than
using the smallest number of instructions. Consider these two different
data layouts for a animation key finding system:

~~~~ {caption="Anim" key="" formats=""}
struct Anim {
    float keys[num];
    VALUE_TYPE values[num];
};

struct KeyClump { float startTimes[32]; } // 128 bytes
keyClump root;
keyClump subs[32];
// implicit first element that has the same value as root.startTimes[n],
// but last element is the same as root.startTimes[n+1]
VALUE_TYPE Values[32*32];
~~~~

A binary search is quick, but if you know you are going to be doing
completely random access of your data, but your data is of a certain
size, you can make even more optimisations. In the key clumps version,
the search loads the root (which has the times of every 32^nd^ key,)
then after finding which subroot to load loads that subroot. Once these
two pieces of data are memory, there is enough information to generate a
lookup index for the two values stored in <span>*Values*</span>, and the
sub key interval interpolation value.

~~~~ {caption="Finding" in="" the="" clump=""}
VALUE_TYPE GetAtT( t ) 
    int rootIndex = binaryFind( t, root );
    KeyClump &theSub = subs[rootIndex];
    int subIndex = binaryFind( t, theSub );
    int keyIndex = rootIndex * 32 + subIndex;
    float *keyTimes = &theSub;
    const float t1 = keyTimes[subIndex];
    const float t2 = keyTimes[subIndex+1];
    float blend = (t-t1) / ( t2-t1 );
    return Interp( Values[keyIndex], Values[keyIndex+1], blend );
}
~~~~

But most data isn’t this simple to optimise. A lot of the time, we have
to work with spatial data, but because we use objects, it’s hard to
strap on an efficient spatial reference container after the fact. It’s
virtually impossible to add one at runtime to an externally defined
class of objects.

Adding spatial partitioning when your data is in a simple data format
like rows allows us to generate spatial containers or lookup systems
that will be easy to maintain and optimise for each particular
situation. Because of the inherent reusability in data-oriented
transforms, we can write some very highly optimised routines for the
high level programmers.

Finding lowest or highest is a sorting problem
----------------------------------------------

In some circumstances you don’t even really need to search. If the
reason for searching is to find something within a range, such as
finding the closest food, or shelter, or cover, then the problem isn’t
really one of searching, but one of sorting. In the first few runs of a
query, the search might literally do a real search to find the results,
but if it’s run often enough, there is no reason not to promote the
query to a runtime updating sorted subset of some other tables’ data. If
you need the nearest three elements, then you keep a sorted list of the
nearest three elements, and when an element has an update, insertion or
deletion, you can update the sorted three with that information. For
insertions or modifications that bring elements that are not in the set
closer, you can check that the element is closer and pop the lowest
before adding the new element to the sorted best. If there is a
deletion, or a modification that makes one in the sorted set a contender
for elimination, a quick check of the rest of the elements to find a new
best set might be necessary. If you keep a larger than necessary set of
best values, however, then you might find that this never happens.

~~~~ {caption="keeping" more="" than="" you="" need=""}
Array<int> bigArray;
Array<int> bestValue;
const int LIMIT = 3;

void AddValue( int newValue ) {
    bigArray.push( newValue );
    bestValue.sortedinsert( newValue );
    if( bestValue.size() > LIMIT )
        bestValue.erase(bestValue.begin());
}
void RemoveValue( int deletedValue ) {
    bigArray.remove( deletedValue );
    bestValue.remove( deletedValue );
}
int GetBestValue() {
    if( bestValue.size() ) {
        return bestValue.top();
    } else {
        int best = bigArray.findbest();
        bestvalue.push( best );
        return best;
    }
}
~~~~

The trick is to find, at runtime, the best value to use that covers the
solution requirement. The only way to do that is to check the data at
runtime. For this, either keep logs, or run the tests with dynamic
resizing based on feedback from the table’s query optimiser.

Finding random is a hash/tree issue
-----------------------------------

For some tables, the values change very often. For a tree representation
to be high performance, it’s best not to have a high number of
modifications as each one could trigger the need for a rebalance. Of
course, if you do all your modifications in one stage of processing,
then rebalance, and then all your reads in another, then you’re probably
going to be okay still using a tree. If you have many different queries
on some data, you can end up with multiple different indexes. How
frequently the entries are changed should influence how you store your
index data. Keeping a tree around for each query could become expensive,
but would be cheaper than a hash table in most implementations. Hash
tables become cheaper where there are many modifications interspersed
with lookups, trees are cheaper where the data is mostly static, or at
least hangs around for a while. When the data becomes constant, a
perfect hash can trump a tree. Trees can be quickly made from data,
faster than hash tables which need you to run a hash function per entry
being inserted. Hash tables can be quickly updated and can take up only
marginally more space than trees if implemented with care. Perfect hash
tables use precalculated hash functions to generate an index, and don’t
require any space other than is used to store the constants and the
array of pointers or offsets into the original table. If you have the
time, then you might find a perfect hash that returns the actual
indexes. I’m not sure we have that long though.

For example, if we need to find the position of someone given their
gamertag, the players won’t be sorted by gamertag normally, so we need a
gamertag to player lookup. This data is mostly constant during game so
would be better suited to a tree or perfect hash if we could generate
one fast enough. Generally, people leave games and join them, so a tree
is probably as static a container as is sensible to use. Given the
number of players isn’t likely to go over a ten thousand at any point, a
trie based off the gamertag hash value should provide very quick lookup.

A hash can be more useful when the table is more chaotic, for example,
messages have senders and recipients. If we need to do something with
all the messages from or to one sender or recipient, then at least one
of those is not going to be the normal sorted order of the table.
Because the table is in constant flux, keeping a tree is virtually
useless, also the hash table variant can handle multiple entries with
the same key a lot easier than a tree implementation as it can use the
standard linked list of entries in a hash bucket to collect all the
messages with a certain sender/recipient.
