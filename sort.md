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

