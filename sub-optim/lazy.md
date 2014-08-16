Lazy Evaluation for the masses
------------------------------

When optimising Objectoriented code, it’s quite common to find local
caches of calculations done hidden in mutable member variables. One
trick found in most updating hierarchies is the dirty bit, the flag that
says whether the child or parent members of a tree imply that this
object needs updating. When traversing the hierarchy, this dirty bit
causes branching based on data that has only just loaded, usually
meaning there is no chance to guess the outcome and thus in most cases,
causes a pipeline flush and an instruction lookup.

If your calculation is expensive, then you might not want to go the
route that renderer engines now use. In render engines, it’s cheaper to
do every scene matrix concatenation every frame than it is only doing
the ones necessary and figuring out if they are.

For example, in the /emph<span>GCAP 2009 - Pitfalls of Object Oriented
Programming presentation by Tony Albrecht</span> in the early slides he
declares that checking a dirty flag is less useful than not checking it
as if it does fail (the case where the object is not dirty) the
calculation that would have taken 12 cycles is dwarfed by the cost of a
branch misprediction (23-24 cycles).

If your calculation is expensive, you don’t want to bog down the game
with a large number of checks to see if the value needs updating. This
is the point at which existence-based-processing comes into its own
again as existence the dirty table implies that it needs updating, and
as a dirty element is updated it can be pushing new dirty elements onto
the end of the table, even prefetching if it can improve bandwidth.

