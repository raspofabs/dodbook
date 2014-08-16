Mementos
--------

Reducing detail introduces an old problme, though. Changing level of
detail in game logic systems, AI and such, brings with it the loss of
high detail history. In this case we need a way to store what is needed
to maintain a highly cohesive player experience. If a high detail
squadron in front of the player goes out of sight and another squadron
takes their place, we still want any damage done to the first group to
reappear when they come into sight again. Imagine if you had shot out
the glass on all the ships and when they came round again, it was all
back the way it was when they first arrived. A cosmetic effect, but one
that is jarring and makes it harder to suspend disbelief.

When a high detail entity drops to a lower level of detail, it should
store a memento, a small, well compressed nugget of data that contains
all the necessary information in order to rebuild the higher detail
entity from the lower detail one. When the squadron drops out of sight,
it stores a memento containing compressed information about the amount
of damage, where it was damaged, and rough positions of all the ships in
the squadron. When the squadron comes into view once more, it can read
this data and generate the high detail entities back in the state they
were before. Lossy compression is fine for most things, it doesn’t
matter precisely which windows, or how they were cracked, maybe just
that about $2/3$ of the windows were broken.

Another good example is in a city based free-roaming game. If AIs are
allowed to enter vehicles and get out of them, then there is a good
possibility that you can reduce processing time by removing the AIs from
world when they enter a vehicle. If they are a passenger, then they only
need enough information to rebuild them and nothing else. If they are
the driver, then you might want to create a new driver type based on
some attributes of the pedestrian before making the memento for when
they exit the vehicle.

If a vehicle reaches a certain distance away from the player, then you
can delete it. To keep performance high, you can change the priorities
of vehicles that have mementos so that they try to lose sight of the
player thus allowing for earlier removal from the game. Optimisations
like this are hard to coordinate in Object-oriented systems as internal
inspection of types isn’t encouraged.

