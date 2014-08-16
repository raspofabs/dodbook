Relational Databases
====================

E. F. Codd wrote a paper [^1] on how to move away from structured files as
a way of storing data. This paper was the basis of all modern relational
databases and provided a much needed language in which to think about how data
could be stored, and manipulated. Before the paper was published in 1970, all
databases were graph or network model of data. In games we tend to use these
too, where objects point to other objects. A graph or network, is a collection
of nodes and connections like objects and pointers to other objects, sometimes
the connections are one way just the same as when only one object holds a
pointer to the other in a relationship. Boyce and Codd set out to prove that
their relational approach to data storage, allowed a much higher degree of data
independence, and that through independence, we gain much in the forms of
simple redundancy checking, less data access per query, higher maintainability
through implicit relations instead of explicit links, and through common
language of manipulation, efficient idioms could be built and reused without
transforming the implementation significantly between data storage mechanisms.

In games and other highly dynamic software with evolutionary development
requirements, the power of using data that is freed from design details and
from implementation details is immense. The biggest hurdles we face in game
development are maintenance, redesign driven implementation modifications,
regression testing of these changes, and version resilience for the end user.
Savegames that work backwards and forwards across versions of the same game are
a powerful tool for testers, and for automated testing.

[^1] E.F.Codd - A Relational Model of Data for Large Shared Data Banks
     Communications of the ACM - Volume 13 / Number 6 / June, 19 - Pg 377-387
