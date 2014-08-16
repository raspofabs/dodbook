Condition Tables
================

Condition tables are a data-oriented approach to Decision tables.
Decision tables are a method by which you can generate flow control with
a table, mapping a vector of predicates to a set of outcomes or
destinations. In decision tables, each row has a predicate – a logical
statement, such as isTrue, isFalse, null, or some boolean returning
function on the data present in the column, such as $>0$ for numbers, or
<span>contains( “win” )</span> for strings. Decision tables aren’t
entirely like standard flow control statements, as they can lead to
multiple outcomes. We will see that a condition table query can also end
up being true for multiple outcomes, or even have no matching rows.

