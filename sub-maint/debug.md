Debugging
---------

The prime causes of bugs are the unexpected side effects of a transform,
or an unexpected corner case where a conditional didn’t return the
correct value. In object-oriented programming, this can manifest in many
ways, from an exception caused by de-referencing a null, to ignoring the
interactions of the player because the game logic hadn’t noticed it was
meant to be interactive.

### Lifetimes

One of the most common causes of the null dereference is when an
object’s lifetime is handled by a separate object to the one
manipulating it. For example, if you are playing a game where the
badguys can die, you have to be careful to update all the objects that
are using them whenever the badguy gets deleted, otherwise you can end
up dereferencing invalid memory which can lead to dereferencing null
pointers because the class has destructed. data-oriented development
tends towards this being impossible as the existence of an entity in a
table implies its processability, and if you leave part of an entity
around in a table, you haven’t deleted the entity fully. This is a
different kind of bug, but it’s not a crash bug, and it’s easier to find
and kill as it’s just making sure that when an entity is destroyed, all
the tables it can be part of also destroy their elements too.

### Avoiding pointers

When looking for data-oriented solutions to programming problems, we
often find that pointers aren’t required, and often make the solution
harder to scale. Using pointers where null values are possible implies
that each pointer doesn’t only have the value of the object being
pointed at, but also implies a boolean value for whether or not that
instance exists. Removing this unnecessary extra feature can remove
bugs, save time, and reduce complexity.

### Bad State

Sometimes a bug is more to do with a game not being in the right state.
Debugging then becomes a case of finding out how the game got into its
current, broken state.

When you encapsulate your state, you hide internal changes. This quickly
leads to adding lots of debugging logs. Instead of hiding, data-oriented
suggests keeping data in simple forms, and potentially leaving it around
longer than required can lead to highly simplified transform inspection.
If you have a transform that appears to work, but for one odd case it
doesn’t, the simplicity of adding an assert and not deleting the input
data reducing the amount of guesswork and toil required to generate the
bug fix. If you keep most of your transforms as one-way, that is to say
they take from one source, and produce or update another, but even if
you run the code multiple times it will still produce the same results
as it would the first time. The transform is idempotent. This useful
property allows you to find a bug, then rewind and trace through without
having to attempt to rebuild the initial state.

One way of keeping your code idempotent is to write your transforms in a
single assignment style. If you operate with multiple transforms but all
leading to predicated join points, you can guarantee yourself some
timings, and you can look back at what caused the final state to turn
out like it did without even rewinding. If your conditions are condition
tables, just leave the inputs around until validity checks have been
completed then you have the ability to go into any live system and check
how it arrived at that state. This alone should reduce any investigation
time to a minimum.

