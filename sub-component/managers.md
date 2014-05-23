Towards Managers
----------------

After splitting your classes up into components, you might find that
your classes look more awkward now they are accessing variables hidden
away in new structures. But it’s not your classes that should be looking
up variables, but instead transforms on the classes. A common operation
such as rendering requires the position and the model information, but
it also requires access to the renderer. Such global access is seen as a
common compromise during most game development, but here it can be seen
as the method by which we move away from a class centric approach to
transforming our data into render requests that affect the graphics
pipeline without referring to data unimportant to the renderer, and how
we don’t need a controller to fire a shot.

    class RenderManager {
        void Update() {
            foreach( {index,pos} in positionArray ) {
                if( index in renderArray ) {
                    ModelID mid = renderArray[ index ].playerModel;
                    gRenderer.AddModel( mid, pos );
                }
            }
        }
    }
    class PhysicsManager {
        void Update() {
            foreach( {index,pos} in positionArray ) {
                if( index in renderArray ) {
                    ModelID mid = renderArray[ index ].playerModel;
                    ApplyCollisionAndResponse( pos.position, pos.velocity
                }
            }
        }
    }
    class PlayerControl {
        void Update() {
            foreach( {index,control} in controlArray ) {
                if( control.controllable ) {
                    Pad pad = GetPad( control.controller );
                    if( pad.IsPressed( SHOOT ) ) {
                        if( index in inventoryArray ) {
                            if( inventoryArray[ index ].bulletCount > 0 ) {
                                if( index in animArray ) {
                                    animArray[ index ].currentAnimGoal = SHOOT_ONCE;
                                }
                            }
                        }
                    }
                }
            }
            foreach( {index,inv} in inventoryArray )  {
                if( inv.bulletCount > 0 ) {
                    if( index in animArray ) {
                        anim = animArray[ index ];
                        if( anim.currentAnim == SHOOT_ONCE ) {
                            anim.currentAnim = SHOT;
                            inventoryArray[index].bulletCount -= 1;
                            anim.playingSoundHandle = PlaySound( GUNFIRE );
                        }
                    }
                }
            }
        }
    }

What happens when we let more than just the player use these arrays?
Normally we’d have some separate logic for handling player fire until we
refactored the weapons to be generic weapons with NPCs using the same
code for weapons proably by having a new weapon class that can be
pointed to by the player or an NPC, but instead what we have here is a
way to split off the weapon firing code in such a way as to allow the
player and the NPC to share firing code without inventing a new class to
hold the firing. In fact, what we’ve done is split the firing up into
the different tasks that it really contains.

Tasks are good for parallel processing, and with component based objects
we open up the opportunity to make most of our previously class oriented
processes into more generic tasks that can be dished out to whatever CPU
or co-processor can handle them.
