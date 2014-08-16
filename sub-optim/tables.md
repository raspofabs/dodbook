Tables
------

To keep things simple, advice from multiple sources indicates that
keeping your data as vectors has a lot of positive benefits. There are
reasons to not use STL, including extended compile and link times, as
well as issues with memory allocations. Whether you use std::vector, or
roll your own dynamicly sized array, it is a good starting place for any
future optimisations. Most of the processing you will do will be
transforming one array into another, or modifying a table in place. In
both these cases, a simple array will suffice for most tasks.

For the benefit of your cache, structs of arrays can be more cache
friendly if the data is not related. It’s important to remember that
this is only true when the data is not meant to be accessed all at once,
as one advocate of the data-oriented design movement assumed that
structures of arrays were intrinsically cache friendly, then put the
x,y, and z coordinates in separate arrays of floats. The reason that
this is not cache friendly should be relatively easy to spot. If you
need to access the x,y, or z of an element in an array, then you more
than likely need to access the other two axes as well. This means that
for every element he would have been loading three cache-lines of float
data, not one. This is why it is important to think about where the data
is coming from, how it is related, and how it will be used.
Data-oriented design is not just a set of simple rules to convert from
one style to another.

If you use dynamic arrays, and you need to delete elements from them,
and these tables refer to each other through some IDs, then you may need
a way to splice the tables together in order to process them. If the
tables are sorted by the same value, then it can be written out as a
simple merge operation, such as in Listing [lst:joinmerge].

    Table<Type1> t1Table;
    Table<Type2> t2Table;
    Table<Type3> t3Table;

    ProcessJoin( Func functionToCall ) {
        TableIterator A = t1Table.begin();
        TableIterator B = t2Table.begin();
        TableIterator C = t3Table.begin();
        while( !A.finished && !B.finished && !C.finished ) {
            if( A == B && B == C ) {
                functionToCall( A, B, C );
                ++A; ++B; ++C;
            } else {
                if( A < B || A < C ) ++A;
                if( B < A || B < C ) ++B;
                if( C < A || C < B ) ++C;
            }
        }
    }

This works as long as the == operator knows about the table types and
can find the specific column to check against, and as long as the tables
are sorted based on this same column. But what about the case where the
tables are zipped together without being the sorted by the same columns?
For example, if you have a lot of entities that refer to a modelID, and
you have a lot of mesh-texture combinations that refer to the same
modelID, then you will likely need to zip together the matching rows for
the orientation of the entity, the modelID in the entity render data,
and the mesh and texture combinations in the models. The simplest way to
program a solution to this is to loop through each table in turn looking
for matches such as in Listing [lst:joinloop].

    Table<Orientation> oTable;
    Table<EntityRenderable> erTable;
    Table<MeshAndTexture> modelAssets;

    ProcessJoin( Func functionToCall ) {
        TableIterator A = oTable.begin();
        while( !A.finished() ) {
            TableIterator B = erTable.begin();
            while( !B.finished() ) {
                TableIterator C = modelAssets.begin();
                while( !C.finished() ) {
                    if( A == B && B == C ) {
                        functionToCall( A, B, C );
                    }
                 ++C;
                }
            ++B;
            }
        ++A;
        }
    }

Another thing you have to learn about when working with data that is
joined on different columns is the use of join strategies. In databases,
a join strategy is used to reduce the total number of operations when
querying across multiple tables. When joining tables on a column (or key
made up of multiple columns), you have a number of choices about how you
approach the problem. In our trivial coded attempt you can see we simply
iterate over the whole table for each table involved in the join, which
ends up being O($nmo$) or O($n^3$) for rougly same size tables. This is
no good for large tables, but for small ones it’s fine. You have to know
your data to decide whether your tables are big[^1] or not. If your
tables are too big to use such a trivial join, then you will need an
alternative strategy.

You can join by iteration, or you can join by lookup[^2], or you can
even join once and keep a join cache around.

The first thing could do is use the ability to have tables sorted in
multiple ways at the same time. Though this seems impossible, it’s
perfectly feasible to add auxilary data that will allow for traversal of
a table in a different order. We do this the same way databases allow
for any number of indexes into a table. Each index is created and kept
up to date as the table is modified. In our case, we implement each
index the way we need to. Maybe some tables are written to in bursts,
and an insertion sort would be slow, it might be better to sort on first
read. In other cases, the sorting might be better done on write, as the
writes are infrequent, or always interleaved with reads.

Concatenation trees provide a quick way to traverse a list. Conc-trees
usually are only minimally slower than a linear array due to the nature
of the structure. A conc-tree is a high level structure that points to a
low level structure, and many elements can pass through a process before
the next leaf needs to be loaded. The code for a conc-tree doesn’t
remain in memory all the time like other list handling code, as the list
offloads to an array iteration whenever it is able. This alone means
that sparse conc-trees end up spending little time in their own code,
and offer the benefit of not having to rebuild when an element goes
missing from the middle of the array.

In addition to using concatenation trees to provide a standard iterator
for a constantly modified data store, it can also be used as a way of
storing multiple views into data. For example, perhaps there is a set of
tables that are all the same data, and they all need to be processed,
but they are stored as different tables for some reason, such as what
team they are on. Using the same conc-tree code, they can be iterated as
a full collection with any code that accepts a conc-tree instead of an
array iterator.

Modifying a class can be difficult, especially at runtime when you can’t
affect the offsets in running code without at least stopping the process
and updating the executable. Adding new elements to a class can be very
useful, and in languages that allow it, such as Ruby and Python, and
even Javascript, it can be used as a substitute for virtual functions
and compositing. In other languages we can add new functions, new data,
and use them at runtime. In C++, we cannot change existing classes,
unless they are defined by some other mechanism than the compile time
structure syntax. We can add elements if we define a class by its
schema, a data driven representation of the elements in the class. The
benefit of this is that schema can include more, or less, than normal
given a new context. For example, in the case of some merging where the
merging happens on two different axes, there could be two different
schema representing the same class. The indexes would be different. One
schema could include both indexes, with which it would build up an
combination table that included the first two tables merged, by the
first index, but maintaining the same ordering so that when merging the
merged table with the third table to be merged, the second index can be
used to maintain efficient combination.

    A, B, C
    B has index(AB), and index(BC)
    merge A,B (by index(AB))
    AB, C
    merge AB, C (by index(BC))
    ABC


[^1]: dependent on the target hardware, how many rows and columns, and
    whether you want the process to run without trashing too much cache

[^2]: often a lookup join is called a join by hash, but as we know our
    data, we can use better row search algorithms than a hash when they
    are available

