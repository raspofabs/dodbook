Bit twiddling decision tables
-----------------------------

Dependent on the language and hardware, bit twiddling can give significant
gains. Some languages implement them poorly, and some hardware can have strange
limitations. Measure instead of assuming these techniques are faster on your
target platform.

Condition tables normally operate as arrays of condition flag bit
fields. The flags are the collected results of conditions on the data.
But, if the bit fields are organised by decision rather than by row,
then you can call in only the necessary conditions into different
decision transforms.

If the bits are organised by condition, then you can run a short
transform on the whole collection of condition bits to create a new,
simpler list of whether or nots. For example, you may have conditions
for decisions that you can map to an alphabet of a-m, but only need some
for making a decision. Imagine you need to be sure that a,d,f,g are all
false, but e,j,k need to all be true. Given this logic, you can build a
new condition, let’s say q, that equals $( a \wedge
d \wedge f \wedge g ) \wedge \neg( e \vee j \vee k )$ which can then be
used immediately as a job list.

Organising the bits this way could be easier to parallelize as a
transform that produces a condition stream would be in contention with
other processes if they shared memory[^3]. The benefit to row based
conditions comes when the conditions change infrequently, and the number
of things looking at the conditions to make decisions is small enough
that they all fit in a single platform specific type, such as a 32bit or
64bit unsigned int. In that case, there would be no benefit in reducing
the original contention when generating the condition bits, and because
the number of views, or contexts about the conditions is low, then there
is little to no benefit from splitting the processing so much.

If you have an entity that needs to reload when their ammo drops to
zero, and they need to consider reloading their weapon if there is a
lull in the action, then, even though both those conditions are based on
ammo, the decision transforms are not based on the same condition. If
the condition table has been generated as arrays of condition bitfields
with each bit representing one row’s state with respect to that
condition, then you can halve the bandwidth to the check for
definite-reload transform, and halve the bandwidth for the
reload-consideration check. There will be one stream of bits for the
condition of ammo equal to zero, and another stream for ammo less than
max. There’s no reason to read both, so we don’t.

What we have here is another case of deciding whether to go with
structures of arrays, or sticking with an array of structures. If we
access the data from a few different contexts, then a structure of
arrays trumps it. If we only have one context for using the conditions,
then the array of structures, or in this case, array of masks, wins out.
But remember to profile as any advice is only advice and only measuring
can really provide proof, or evidence that assumptions are wrong.

[^3]: This would be from false sharing, or even real sharing in the case
    of different bits in the same byte
