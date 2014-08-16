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

[^1]: Tony Albrecht proves this point in his article on sorting networks
    http://seven-degrees-of-freedom.blogspot.co.uk/2010/07/question-of-sorts.html

