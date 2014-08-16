Alternative Axes
----------------

As with all things, take away an assumption and you can find other uses
for a tool. Whenever you read about or work with a level of detail
system, you will be aware that the constraint on what level of detail is
shown has always been some distance function in space. It’s now time to
take that assumption, discard it, and analyse what is really happening.

First, we find that if we take away the assumption of distance, we can
infer the conditional as some kind of linear measure. This value
normally comes from a function that takes the camera position and finds
the relative distance to the entity under consideration. What we may
also realise when discarding the distance assumption is a more
fundamental understanding of that what we are trying to do. We are using
a runtime variable to control the presentation state of an entity. We
use runtime variables to control the state of many parts of our game
already, but in this case, there is a passive presentation response to
the variable, or axis being monitored. The presentation is usually some
graphical, or logical level of detail, but it could be something as
important to the entity as its own existence.

How long until a player forgets about something that might otherwise be
important? This information can help reduce memory usage as much as
distance. If you have ever played <span>*Grand Theft Auto IV*</span>,
you might have noticed that the cars can dissappear just by not looking
at them. As you turn around a few times you might notice that the cars
seem to be different each time you face their way. This is a stunning
use of temporal level of detail. Cars that have been bumped into or
driven and parked by the player remain where they were, because, in
essence, the player put them there. Because the player has interacted
with them, they are likely to remember that they are there. However,
ambient vehicles, whether they are police cruisers, or civilian
vehicles, are less important and don’t normally get to keep any special
status so can vanish when the player looks away.

In adition to time-since-seen, some elements may base their level of
detail on how far a player has progressed in the game, or how many of
something a player has, or how many times they have done it. For
example, a typical bartering animation might be cut shorter and shorter
as the game uses the axis of <span>*how many recent barters*</span> to
draw back the length of any non-interactive sections that could be
caused by the event. This can be done simply, and the player will be
thankful. It may even be possible to allow for multi-item transactions
after a certain number of transactions have happened. In effect, you
could set up gameplay elements, reactions to situations, triggers for
tutorials or extensions to gameplay options all through these abstracted
level of detail style axes.

This way of manipulating the present state of the game is safer from
transition errors. Errors that happen because going from one state to
another may have set something to true when transitioning one direction,
but not back to false when transitioning the other way. You can think of
the states as being implicit on the axis, not explicit, calculated
purely as a triggered event that manipulates state.

An example of where transition errors occur is in menu systems where
though all transitions should be reversible, sometimes you may find that
going down two levels of menu, but back only one level, takes you back
to where you started. For example, entering the options menu, then
entering an adjust volume slider, but backing out of the slider might
take you out of the options menu all together. These bugs are common in
UI code as there are large numbers of different layers of interaction.
Player input is often captured in obscure ways compared to gameplay
input response. A common problem with menus is one of ownership of the
input for a particular frame. For example, if a player hits both the
forward and backward button at the same time, a state machine UI might
choose to enter whichever transition response comes first. Another might
manage to accept the forward event, only to have the next menu accept
the back event, but worst of all might be the unlikely but seen in the
wild, menu transitioning to two different menus at the same time.
Sometimes the menu may transition due to external forces, and if there
is player input captured in a different thread of execution, the game
state can become disjoint and unresponsive. Consider a network game’s
lobby, where if everyone is ready to play, but the host of the game
disconnects while you are entering into the options screen prior to game
launch, in a traditional state machine like approach to menus, where
should the player return to once they exit the options screen? The lobby
would normally have dropped you back to a server search screen, but in
this case, the lobby has gone away to be replaced with nothing. This is
where having simple axes instead of state machines can prove to be
simpler to the point of being less buggy and more responsive.

