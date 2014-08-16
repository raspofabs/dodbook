Game entities
-------------

### Converting an object oriented player

While I was at Frontier Developments, I was working on a little space
game that ended up being a boat game in caverns[^5] and that was the
first time I intentionally changed a game from object-oriented to
component-oriented. The ships all had their rendering positions, their
health, speed, momentum, ammo recharge timers etc, and these were all
part of a base ship class that was extended to be a player class, and
inherited from a basic element that was extended to also include the
loot drops and the dangerous ice blocks. All this is pretty standard
practice, and from the number of codebases I have seen, it’s pretty
light on the scale of inheritance with which games normally end up.
Still, I had this new tool in my bag, the component-oriented approach
specifically existence based processing. I wanted to try it out, see if
it really did impact the profile of the game in any significant way. I
started with the health values. I made a new component for health, and
anyone that was at full health, or was dead, was not given an instance
of the component. The player ship and the enemy ships all had no health
values until they were shot and found wanting.

Transitioning to the component based health took a while. Translating
any game from one programming paradigm to another is not a task to be
taken lightly, even when your game code is small and you’ve only spent
sixty hours developing the game so far. Once the game was back up
though, the profile spoke loud and clear of the benefits. I had
previously spent some time in health code every frame, this was because
the ships had health regenerators that ran and updated the health every
time they got an update poll. They needed to do an update because they
were updated, not because they needed to, and they didn’t have any way
to opt out before the componentisation, as the update to health was part
of the ship update. Now the health update only ran over the active
health instances, and removed itself once it reached max health rather
than bounce off the max health.

This relatively small change allowed me to massively increase the number
of small delicate ships in the game (ships that would beat the player
ship by overrunning it rather than being able to withstand the player’s
fire and get close in to do some damage), and also lead to another
optimisation: componentising the weapon recharge timer.

If the first change was a success, then the second was a major success.
Instead of keeping track of when a weapon was ready to fire again, the
time that it would be available was inserted into a sorted list of
recharge times. Only the head of the list was checked every global
update, meaning that a large number of weapons could be recharging at
once and none of them caused any data access until they were very nearly
or actually ready.

This immediate success lead me to believe the data-oriented design
movement was really important and needed to be spread around, and
probably caused my sudden hatred of object-oriented programming. From
that point on, all I could see was cache-misses and pointless update
checks.

### People don’t really exist.

> *A Mathematician, a Biologist and a Physicist are sitting in a street
> cafe watching people going in and coming out of the house on the other
> side of the street.*
>
> First they see two people going into the house. Time passes. After a
> while they notice three people coming out of the house.
>
> The Physicist: “The measurement wasn’t accurate.”.\
> The Biologists conclusion: “They have reproduced”.\
> The Mathematician: “If now exactly 1 person enters the house then it
> will be empty again.”

The followers in the GODUS prototype are little objects when they are
running around, and though the code has changed quite a bit from the
initial lists of pointers to people structures, and has thus become
unweildy, there was one element that was a perfect example of
hierarchical level of detail in the game logic. The followers, once they
had started to build a building, dissappeared. They were no longer
required in any way, so they were reduced to a mere increment of the
number of people in a building. An object-oriented programmer disputed
this being a good way to go, “but what if the person has a special
weapon, or is a special character?”. Logic prevailed. If there was a
special weapon, then there would have been a count of those in the
house, or the weapon would have become owned by the house, and as for a
special character, the same kind of exception could be made, but in
reality, which is where we firmly plant ourselves when developing in the
data-oriented paradigm, these potential changes had not so far been
requested, and by the end of the development, they still hadn’t.

Another example from the GODUS prototype was the use of duck-typing.
Instead of adding a base class for people and houses, just to see if
they were meant to be under control of the local player, we used a
templated function to extract a boolean value. Duck typing doesn’t
require anything more than certain member functions or variables being
available. They don’t have to be in the same place, or come bundled into
a base class: they just have to be present.

When teaching data-oriented design, I find the biggest hurdle is
convincing programmers that data-oriented design is possible for some
areas of development. It’s very easy to accidentally assume that you
need to bundle things into objects, especially after years of training
and teaching object-oriented developlment. It won’t come naturally and
you will keep catching yourself building things as objects first then
making them more relational afterwards. It will take time to fully
remove the muscle memory of putting related things in the same class,
but worry not, I’m sure all data-oriented developers go through this
transition where they know they’re not coding data-oriented, but they
don’t quite know how to do it yet.

### Lazy evaluation molasses

The idea of lazy evaluation makes so much sense, and yet it’s precisely
that kind of sense that makes no sense for a computer. I remember there
was a dirty bit check before an update in some of the global update code
on Outsider, something I would have done a hundred times over before I
started to get a better feel for what the computer was doing, and found
one of the best lines-of-code to time-saved ratio fixes I ever found in
a triple A game. The dirty bit check was just before the code that
actually did the work of updating the instance. This meant that the CPU
had to preload the *fixup* code while it was checking the dirty bit, and
because the fixup code was virtual functions based, it meant that the
code was loading the virtual table value and the function was preloaded
all the while the dirty bit was about to say it wasn’t necessary to do
any of it. To make matters worse, the code was inside an if, implying to
most compilers that it would be the more likely taken branch[^6]. The
fix was simple. Build up a local array of objects to actually do an
update of, then do them all at once. Because the code to do the update
wasn’t preloaded, the whole update took a lot less time. You can have
your lazy evaluation, but don’t preload the evaluation if you don’t have
to.

### Component oriented design

While at Broadsword, I found an article about dungeon seige proclaiming
the benefit of components when developing a game. The GOs or Game
Objects that were used were components that could be stitched together
to create new compound objects.

Taking that as inspiration, I looked at all our different scene-graph
nodes, gameplay helper classes and functions we commonly used, and tried
to distill them into their elements. I started by just making components
such as *PlayerCharacter* and *AICharacter*, adding a *Prop* element
before realising where I was going wrong. The object oriented mindset
had told me to look at the compounds, not the elements, so I went back
to the drawing board and started dissecting the objects again. Component
oriented development works out best when you completely explode all your
compounds, then recombine when you find the combinations are consistent,
or when combining makes more sense to computation.

After I was done fully dissecting our basic game classes I had a long
list of separate, elements that by themselves did very little[^7]. At
this point, I added the bootstrap code to generate the scene. Some
components required other components at runtime, so I added a *requires*
trait to the components, much like \#include, except to make this work
for teardown, I also added a count so components went away much like
reference counted smart pointers folded away. The initial demo was a
simple animated character running around a 3D environment, colliding
with props via the collision Handler.

In the beginning, I had a container entity that maintained a list of
components. Once I had a first working version, I stepped back and
thought about the system. I started to see that the core entity wasn’t
really necessary. As long as any update components were updated, then
the game would tick on. As long as the entity’s components could find
their requirement components, then the game would work. I shifted to
having an implicit entity based on the UID I generate on entity
creation. This meant that all entities were really only the components
that were linked to that ID, as the ID didn’t index into an array of
entity objects, or point to an allocated entity, it was merely an ID off
which to hang all the components.

Adding features to a class at runtime was now possible. I could inject
an additional property into the existing entities because I had centred
the entities around a key, and not any kind of central class. The next
step from here was to add components via a scripting language so it
would be possible to develop new gameplay code while running the game.
Unfortunately this never happened, but some MMO engine developers have
done precisely this.

The success of this demo convinced me that components would play a major
role in our continuing game development, but alas, we only used the
engine for one more product and the time to bring the new component
based system up to speed for the size of the last project was estimated
to be counter productive. Mick West released an article about how when
he was at Neversoft, he did manage to convert the Tony Hawks code-base
to components[^8] which means it’s not impossible to migrate, it’s just
not easy. If we were to start component oriented... well that’s a
different story, normally told by Scott Bilas.

[^5]: due to concerns that a 2D space game might be misinterpretted as
    the next elite I imagine

[^6]: profile guided optimisation might have saved a lot of time here,
    but the best solution is to give the profiler and optimiser a better
    chance by leaving them less to do

[^7]: Position, Velocity, PlayerInputMapper, VelocityFromInput,
    MeshRender, SkinnedMeshRender, MatrixPalette, AnimPlayer,
    AnimFromInput, and CollisionHandler

[^8]: http://cowboyprogramming.com/2007/01/05/evolve-your-heirachy/
