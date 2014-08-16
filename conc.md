Concurrency
===========

Any book on games development practices for contemporary and future
hardware must cover the issues of concurrency. There will come a time
when we have more cores in our computers than we have pixels on screen,
and when that happens, it would be best if we were already coding for
it, coding in a style that allows for maximal throughput with the
smallest latency. Thinking about how to solve problems for five, ten or
even one hundred cores isn’t going to keep you safe. You must think
about how your algorithms would work when you have an infinite number of
cores. Can you make your algorithms work for N cores?

Writing concurrent software has been seen as a hard task in the past
because most people think they understand threading and can’t get their
heads around all the different corner cases that are introduced when you
share the same memory as another thread. Fixing these with mutexs and
critical sections can become a minefield of badly written code that
works only 99% of the time. For any real concurrent development we have
to start thinking about our code transforming data. Every time you get a
deadlock or a race condition in threaded code, it’s because there’s some
ownership issue. If you code from a data transform point of view, then
there are some simple ground rules that provide very stable tools for
developing truly concurrent software.

