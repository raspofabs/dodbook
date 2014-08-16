Predictable instructions
------------------------

The biggest crime to commit in a deeply pipelined core is to tell it to
do loads of instructions, then once it’s almost done, change your mind
and start on something completely different. This heinous crime is all
too common, with control flow instructions doing just that when they’re
hard to predict, or impossible to predict in the case of entirely random
data, or where the data pattern is known, but the architecture doesn’t
support branch predictions.
