A data-oriented Lookup
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

