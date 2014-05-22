Sorting
=======

For some subsystems, sorting is a highly important function. Sorting the
primitive render calls so that they render front to back for opaque
objects can have a massive impact on GPU performance, so it’s worth
doing. Sorting the primitive render calls so they render back to front
for alpha blended objects is usually a necessity. Sorting sound channels
by their amplitude over their sample position is a good indicator of
priority.

Whatever you need to sort for, make sure you need to sort first, as
usually, sorting is a highly memory intense business.

Do you need to?
---------------

There are some algorithms that seem to require sorted data, but don’t,
and some that require sorted data but don’t seem to. Be sure you know
whether you need to before you make any false moves.

One common use of sorting in games is in the render pass where some
engine programmers recommend having all your render calls sorted by a
high bit count key generated from a combination of depth, mesh,
material, shader, and other flags such as whether the call is alpha
blended. This then allows the renderer to adjust the sort at runtime to
get the most out of the bandwidth available. In the case of the
rendering list sort, you could run the whole list through a general
sorting algorithm, but in reality, there’s no reason to sort the alpha
blended objects with the opaque objects, so in many cases you can take a
first step of putting the list into two separate buckets, and save some
n for your O. Also, choose your sorting algorithm wisely. With opaque
objects, the most important part is usually sorting by textures then by
depth, but that can change with how much your fill rate is being trashed
by overwriting the same pixel multiple times. If your overdraw doesn’t
matter too much but your texture uploads do, then you probably want to
radix sort your calls. With alpha blended calls, you just have to sort
by depth, so choose an algorithm that handles that case best, usually a
quick sort or a merge sort bring about very low but guaranteed accurate
sorting.

Maintain by insertion sort or parallel merge sort
-------------------------------------------------

Depending on what you need the list sorted for, you could sort while
modifying. If the sort is for some AI function that cares about
priority, then you may as well insertion sort as the base heuristic
commonly has completely orthogonal inputs. If the inputs are related,
then a post insertion table wide sort might be in order, but there’s
little call for a full scale sort.

If you really do need a full sort, then use an algorithm that likes
being parallel. Merge sort and quick sort are somewhat serial in that
they end or start with a single thread doing all the work, but there are
variants that work well with multiple processing threads, and for small
data sets there are special sorting network techniques that can be
faster than better algorithms just because they fit the hardware so
well[^1].

Sorting for your platfom
------------------------

Always remembering that in data-oriented development you must look to
the data before deciding which way you’re going to write the code. What
does the data look like? For rendering, there is a large amount of data
with different axes for sorting. If your renderer is sorting by mesh and
material, to reduce vertex and texture uploads, then the data will show
that there are a number of render calls that share texture data, and a
number of render calls that share vertex data. Finding out which way to
sort first could be figured out by calculating the time it takes to
upload a texture, how long it takes to upload a mesh, how many extra
uploads are required for each, then calculating the total scene time,
but mostly, profiling is the only way to be sure. If you want to be able
to profile, or allow for runtime changes in case your game has such
varying asset profiles that there is no one solution to fit all, having
a flexible sorting criteria is extremely useful, and sometimes
necessary. Fortunately, it can be made just as quick as any inflexible
sorting technique, bar a small set up cost.

Radix sort is the fastest serial sort. If you can do it, radix sort is
very fast because it generates a list of starting points for data of
different values. This allows the sorter to drop their contents into
containers based on a translation table, a table that returns an offset
for a given data value. If you build a list from a known small value
space, then radix sort can operate very fast to give a coarse first
pass. The reason radix sort is serial, is that it has to modify the
table it is reading from in order to update the offsets for the next
element that will be put in the same bucket.

It is possible to make this last stage of the process parallel by having
each sorter ignore any values that it reads that are outside its working
set, meaning that each worker reads through the entire set of values
gathering for their bucket, but there is still a small chance of
non-linear performance due to having to write to nearby memory on
different threads. During the time the worker collects the elements for
its bucket, it could be generating the counts for the next radix in the
sequence, only requiring a summing before use in the next pass of the
data, mitigating the cost of iterating over the whole set with every
worker.

If your data is not simple enough to radix sort, you might be better off
using a merge sort or a quick sort, but there are other sorts that work
very well if you know the length of your sortable buffer at compile
time, such as sorting networks. Through merge-sort is not itself a
concurrent algorithm, the many early merges can be run in parallel, only
the final merge is serial, and with a quick pre-parse of the
to-be-merged data, you can finalise with two threads rather than one by
starting from both ends (you need to make sure that the mergers don’t
run out of data). Though quick sort is not a concurrent algorithm each
of the sub stages can be run in parallel. These algorithms are
inherently serial, but can be turned into partially parallelisable
algorithms with O(log n) latency.

When your n is small enough, a traditionally good technique is to write
an in place bubble sort. The algorithm is so simple, it is hard to write
wrong, and because of the small number of swaps required, the time taken
to set up a better sort could be better spent elsewhere. Another
argument for rewriting such trivial code is that inline implementations
can be small enough for the whole of the data and the algorithm to fit
in cache[^2]. As the negative impact of the inefficiency of the bubble
sort is negligible over such a small n, it is hardly ever frowned upon
to do this.

If you’ve been developing data-oriented, you’ll have a transform that
takes a table of n and produces the sorted version of it. The algorithm
doesn’t have to be great to be better than bubble sort, but notice that
it doesn’t cost any time to use a better algorithm as the data is
usually in the right shape already. Data-oriented development naturally
leads us to reuse good algorithms.

Sorting networks work by implementing the sort in a static manner. They
have input data and run swap if necessary functions on pairs of values
of that input data before outputting the final. The simplest sorting
network is two inputs.

$$\xymatrix{
    A \ar[r] & \ar[r] \ar[dr] & \ar[r] & A' \\
    B \ar[r] & \ar[r] \ar[ur] & \ar[r] & B' }$$

If the values entering are in order, the sorting crossover does nothing.
If the values are out of order, then the sorting cross over causes the
values to swap. This can be implemented as branchless writes:

    a' <= MAX(a,b)
    b' <= MIN(a,b)

This is fast on any hardware. The MAX and MIN functions will need
different implementations for each platform and data type, but in
general, branch free code executes faster than code that includes
branches.

Introducing more elements:

$$\xymatrix{
    A \ar[r]   & \ar[r] \ar[ddr] & \ar[rrr] &                 &        & \ar[r] \ar[dr] & \ar[rrr] &                &        & A' \\
    B \ar[rrr] &                 &          & \ar[ddr] \ar[r] & \ar[r] & \ar[r] \ar[ur] & \ar[r]   & \ar[r] \ar[dr] & \ar[r] & B' \\
    C \ar[r]   & \ar[r] \ar[uur] & \ar[rrr] &                 &        & \ar[r] \ar[dr] & \ar[r]   & \ar[r] \ar[ur] & \ar[r] & C' \\
    D \ar[rrr] &                 &          & \ar[uur] \ar[r] & \ar[r] & \ar[r] \ar[ur] & \ar[rrr] &                &        & D' }$$

What you notice here is that the critical path is not long (just three
stages in total), and as these are all branch free functions, the
performance is regular over all data permutations. With such a regular
performance profile, we can use the sort in ways where the variability
of sorting time length gets in the way, such as just-in-time sorting for
sub sections of rendering. If we had radix sorted our renderables, we
can network sort any final required ordering as we can guarantee a
consistent timing.

Sorting networks are somewhat like predication, the branch free way of
handling conditional calculations. Because sorting networks use a min /
max function, rather than a conditional swap, they gain the same
benefits when it comes to the actual sorting of individual elements.
Given that sorting networks can be faster than radix sort for certain
implementations, it goes without saying that for some types of
calculation, predication, even long chains of it, will be faster than
code that branches to save processing time. Just such an example exists
in the Pitfalls of Object Oriented Design presentation, concluding that
lazy evaluation costs more than the job it tried to avoid. I have no
hard evidence for it yet, but I believe a lot of AI code could benefit
the same, in that it would be wise to gather information even when you
are not sure you need it, as gathering it might be quicker than deciding
not to. For example, seeing if someone is in your field of vision, and
is close enough, might be small enough that it can be done for all AI
rather than just the ones that require it, or those that require it
occasionally.

[^1]: Tony Albrecht proves this point in his article on sorting networks
    http://seven-degrees-of-freedom.blogspot.co.uk/2010/07/question-of-sorts.html

[^2]: It might be wise to have some templated inline sort functions in
    your own utility header so you can utilise the benefits of
    miniaturistion, but don’t drop in a bloated std::sort
