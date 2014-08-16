Branching without branching
---------------------------

Due to the restrictions imposed on their use, condition tables have the
opportunity to be realised in branch free or heavily optimised code.
Depending on the number of rows in the decision table, it might be
possible to optimise the query by output, but normally the query can be
optimised by input. We will see more of this choice of rows vs columns
in chapter <span>ref:example</span>.

The first thing we do is generate a truth value from the conditions and
the query array. Remember the query array is made up of isTrue, isFalse,
and null values. We need to generate, from an array of booleans, a
single boolean result. Logically, we can produce this by xoring the
inputs with the isFalse elements, and then oring in the null entries.
Once we have this final array, we only need to check that all elements
are true to find the entire query to be true.

If we allow for our pre-processor to produce bitmasks of input values,
then we can produce a pair of bit masks that generate the kind of result
we need. First, we prepare the ignore mask, this mask contains a high
bit wherever we don’t care about the input value. Naturally, all null
fields can be converted to 1s, and so can any bits higher than the
maximum query entry. The second mask is the falsity masks, and is true
if the query array tri-state is isFalse. These masks are now the xor and
ignore masks.

    unsigned int xorMask = 0;
    unsigned int ignoreMask = 0;
    for( int i = 0; i < tableColumns; ++i ) {
        if( column[i].condition == isFalse )
            xorMask |= BIT( i );
        if( column[i].condition == null )
            ignoreMask |= BIT(i);
    }
    for( int i = tableColumns; i < MAX_BITS; ++i ) {
        ignoreMask |= BIT(i);
    }

Next, prepare the input as a list of boolean values. If we have well
formed data, we can assume that we have already built our inputs as bit
fields, but if our data is still object oriented, or at least still
arrays of structures, then we will probably do this step inline with
reading each structure from the array of structures.

    foreach( row in table ) {
        unsigned int values = 0;
        for( int i = 0; i < tableColumns; ++i ) {
            if( row[i] )
                values |= BIT( i );
        }
    }

Once you have your inputs transformed into the array of bit fields, you
can run them through the condition table. If they are an array of
structures, then it’s likely that caching the inputs into a separate
table isn’t going to make things faster, so this decision pass can be
run on the bit field directly. In this snippet we run one bit field
through one set of condition masks.

    unsigned int conditionsMet = ( value ^ xorMask ) | ignoreMask;
    unsigned int unmet = ~conditionsMet;
    if( !unmet ) {
        addToTable( t );
    }

The code first <span>*XORs*</span> the values so the false values become
true for all the cases where we want the value to be false. Then we
<span>*OR*</span> with the ignore so that any entries we don’t care
about become true and don’t falsely break the condition. Once we have
this final value, we can be certain that it will be all ones in case of
a match, and will have some zeros if it is a miss. An <span>if</span>
using the binary-not of the final value will suffice to prove the system
works, but we can do better.

Using the <span>*conditionsMet*</span> value, we can generate a final
mask onto an arbitrary value.

    unsigned int czero = ( cvalue + 1 ); // one more than all the ones is zero.
    unsigned int cmask = ~(czero | -czero) >> 31; // only zero returns -1 from this.
    ID valueIn = valueOut & cmask; // if true, return the key, else return zero.

Now, we can use this value in many ways. We can use it on the primary
key, and add this key to the output table, and providing a list table
that can be reduced by ignoring nulls, we have, in effect, a dead
bucket. If we use it on the increment counter, then we can just add an
entry to the end of the output table, but not increase the size of the
output table. Either way, we can assume this is a branchless
implementation of an entry being added to a table. If this was an event,
then a multi-variable condition check is now branchlessly putting out an
event. If you let these loops unroll, then depending on your platform,
you are going to process a lot more data than a branching model will.
