Optimisations and Implementations
=================================

When optimising software, you have to know what is causing the software
to run slower than you need it to run. We find in most cases, data
movement is what really costs us the most. In the GPU, we find it
labelled under fill rate, and when on CPU, we call it cache-misses. Data
movement is where most of the energy goes when processing data, not in
calculating solutions to functions, or from running an algorithm on the
data, but actually the fulfillment of the request for the data in the
first place. As this is most definitely true about our current
architectures, we find that implicit or calculable information is much
more useful than cached values or explicit state data.

If we start our game development by organising our data in normalised
tables, we have many opportunities for optimisation. Starting with such
a problem agnostic layout, we can pick and choose from tools we’ve
created for other tasks, at worst elevating the solution to a template
or a strategy, before applying it to both the old and new use cases.


