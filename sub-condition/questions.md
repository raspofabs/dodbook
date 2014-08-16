Building Questions
------------------

Condition tables are similar to Decision tables, except they have some
restrictions that allow for easier optimisation. All the input columns
in a condition table query are boolean. If you are familiar with
decision tables, this might seem like a limiting constraint, however if
you need to check that $X
< 20$, then you can do that before it enters the query. Also, unlike
decision tables, each row in a condition table doesn’t have a function
to call, but instead a table reference to output to if there is a match
on the conditions. These simple constraints allow for
existence-based-processing of the result tables, thus reducing the
instruction cache misses of the more traditional database oriented
decision table approach, and also allows the driving of event tables so
that conditions can trigger events on subscribed entities.

For each component involved in the condition table operation, you
generate the boolean values into the condition table input. Generating
each boolean value from the data in this fashion can utilise the
struct-of-arrays format much better, as the predicate can run as a tiny
kernel over the streaming data. In a traditional array-of-structs
format, this technique wouldn’t improve performance or increase
cache-line utilisation, so unless you’re testing your code on well
oriented data, this whole preprocessing step might be worse than
pointless. If your data is organised by concept, such as in an object
oriented class, then you might end up loading in the same data multiple
times to prepare the input table. As each kernel may be accessing only a
few bytes of a structure at a time, this will waste memory bandwidth.

Once the condition input is prepared, we then prepare the transform. The
transform consists of a set of query arrays and an output. The output
will be multiple tables, each query array can point to any of the output
tables, which means that an entry can end up in more than one table, and
can be put into a table more than one time based on how the output table
is organised. Sometimes, an entity will want to only act on the first
matching decision point (this would be a way to implement behaviour
trees), sometimes a component will want to include multiple matches
(this would be a way to implement scoring points).

The condition table is made up of rows, each row has a query array that
consists of one or more tri-state columns with possible values of {
isTrue, isFalse, null }. To match with an input, all query array columns
must match. In effect, an <span>*and*</span> over all the element
queries. The null entry will always return true. With this, it is
possible to build up any query you would normally do on your data.

