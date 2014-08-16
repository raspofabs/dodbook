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

