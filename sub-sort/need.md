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

