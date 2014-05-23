Component Based Objects
=======================

Component oriented design is a good head start for high level
data-oriented design. Components put your mind in the right frame for
not linking together concepts when they don’t need to be, and component
based objects can easily be processed by type, not by instance, which
leads to a smoother processing profile. Component based entity systems
are found in games development as a way to provide a data-driven
functionality system for entities, which can allow for designer control
over what would normally be the realm of a programmer. Not only are
component based entities better for rapid design changes, but they also
stymie the chances of the components getting bogged down into monolithic
objects as most game designers would demand more components with new
features over extending the scope of existing components. Most new
designs need iterating, and extending an existing component by code
doesn’t allow design to change back and forth, trying different things.

When people talk about how to create compound objects, sometimes they
talk about using components to make up an object. Though this is better
than a monolithic class, it is not component based approach, it merely
uses components to make the object more readable, and potentially more
reusable. Component based turns the idea of how you define an object on
its head. The normal approach to defining an object in object oriented
design is to name it, then fill out the details as and when they become
necessary. For example, your car object is defined as a Car, if not
extending Vehicle, then at least including some data about what physics
and meshes are needed, with construction arguments for wheels and body
shell model assets etc, possibly changing class dependent on whether
it’s an AI or player car. In component oriented design, component based
objects aren’t so rigidly defined, and don’t so much become defined
after they are named, as much as a definition is selected or compiled,
and then tagged with a name if necessary. For example, instancing a
physics component with four wheel physics, instancing a renderable for
each part (wheels, shell, suspension) adding an AI or player component
to control the inputs for the physics component, all adds up to
something which we can tag as a Car, or leave as is and it becomes
something implicit rather than explicit and immutable.

A component based object is nothing more than the sum of its parts. This
means that the definition of a component based object is also nothing
more than an inventory with some construction arguments. This object or
definition agnostic approach makes refactoring and redesigning a
completely trivial exercise.

[^1]: Gas Powered Games, Looking Glass Studios, Insomniac, Neversoft all
    used component based objects

[^2]: Gas Powered Games released a web article about their component
    based architecture back in 2004, read it at
    http://garage.gaspowered.com/?q=su\_301

[^3]: GPG:DG uses GO or Game-Objects, but we stick with the term entity
    because it has become the standard term.

[^4]: or is updated while the rendering is happening on another thread
