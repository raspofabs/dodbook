There is no Entity
------------------

What happens when we completely remove the player class? If we consider
that an entity may be not only represented by it’s collection of
components, but also might only be it’s current configuration of
components, then there is the possibility of removing the core class of
Player. Removing this class can mean we no longer think of the player as
being the centre of the game, but also the class no longer existing
means that any code is no longer tied to itself.

    struct Orientation { Vec pos, up, forward, right; };
    SparseArray<Orientation> orientationArray;
    SparseArray<Vec> velocityArray;
    SparseArray<float> healthArray;
    SparseArray<int> xpArray, usedPowerupsArray, controllerID, bulletCount;
    struct Attributes { int SPEED, JUMP, STRENGTH, DODGE; };
    SparseArray<Attributes> attributeArray;
    SparseArray<bool> godmodeArray, controllable, isVisible;
    SparseArray<AnimID> currentAnim, animGoal;
    SparseArray<SoundHandle> playingSound;
    SparseArray<AssetID> modelArray;
    SparseArray<LocomotionType> locoModelArray;
    SparseArray<Array<ItemType> > inventoryArray;

    void RenderUpdate() {
        foreach( {index,assetID} in modelArray ) {
            if( index in isVisible ) {
                gRenderer.AddModel( assetID, orientationArray[ index ] );
            }
        }
    }
    void PhysicsUpdate {
        foreach( {index,vel} in velocityArray ) {
            if( index in modelArray ) {
                ApplyCollisionAndResponse( orientationArray[index], vel, modelArray[ index ] );
            }
        }
    }
    void ControlUpdate() {
        foreach( {index,control} in controllerID ) {
            if( controllable[ index ] ) {
                Pad pad = GetPad( control.controller );
                if( pad.IsPressed( SHOOT ) ) {
                    if( inventoryArray[ index ].bulletCount > 0 ) {
                        animArray[ index ].currentAnimGoal = SHOOT_ONCE;
                    }
                }
            }
        }
    }
    void UpdateAnims() {
        foreach( {index, anim} in currentAnim ) {
            if( anim == SHOOT_ONCE ) {
                anim = SHOT;
                inventoryArray[index].bulletCount -= 1;
                playingSound = PlaySound( GUNFIRE );
            }
        }
    }
    int NewPlayer( int padID, Vec startPoint ) {
        int ID = newID();
        controllerID[ ID ] padID;
        GetAsset( "PlayerModel", ID ); // adds a request to put the player model into modelArray[ID]
        orientationArray[ ID ] = Orientation(startPoint);
        velocityArray[ ID ] = VecZero();
        return ID;
    }

Moving away from a player class means that many other classes can be
invented without adding much code. Allowing script to generate new
classes by composition increases the power of script to dramatically
increase the apparent complexity of the game without adding more code.
What is also of major benefit is that all the different entities in the
game now run the same code at the same time. everyone’s physics is
updated before they are rendered[^4] and everyone’s controls (whether
they be player or AI) are updated before they are animated. Having the
managers control when the code is executed is a large part of the leap
towards fully parallelisable code.
