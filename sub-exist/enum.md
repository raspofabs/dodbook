Don’t use enums {#sec:exist-enum}
---------------

Enumerations are used to define sets of states. We could have had a
state variable for the regenerating entity, one that had infullhealth,
ishurt, isdead as its three states. We could have had a team index
variable for the avoidance entity enumerating all the available teams.
Instead we used tables to provide all the information we needed. Any
enum can be emulated with a variety of tables. All you need is one table
per enumerable value. Setting the enumeration is an insert into a table.

When using tables to replace enums, some things become more difficult:
finding out the value of an enum in an entity is difficult as it
requires checking all the tables that represent that state for the
entity. However, this is mostly disallowed and unnecessary, as the main
reason for getting the value is either to do an operation based on the
state, or to find out if an entity is in the right state to be
considered for an operation.

If the enum is a state or type enum previously handled by a switch or
virtual call, then we don’t need to look up the value, instead we change
the way we think about the problem. The solution is to run transforms
taking the content of each of the switch cases or virtual methods as the
operation to apply to the appropriate table, the table corresponding to
the original enumeration value.

If the enum is instead used to determine whether or not an entity can be
operated upon, then you can operate on all the entities in the
appropriate table. Transforming the whole table or the join of that
table with some other condition. If you’re thinking about the case where
you have an entity as the result of a query and need to know if it is in
a certain state before deciding commit some change, consider that the
table you need access to could have been one of the initial mappings,
meaning that no entity would be found that didn’t match the enum
replacing table in the way you needed it to.

