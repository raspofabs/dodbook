Single Instruction Multiple Data
--------------------------------

There are no current generation consoles that don’t have SIMD of some
sort. All hardware now has some kind of vector unit, and to some extent,
as long as you work within your boundaries, even hardware that doesn’t
have SIMD instructions, such as embedded micro controllers, can operate
on multiple data. The idea behind SIMD is simple: issue one command, and
manipulate multiple pieces of data in the same way at the same time. The
most commonly referenced implementation of this is the vector units
inherent in all current generation hardware. The AlitVec instructions on
PPC and the SPU instruction set contain many instructions that operate
on multiple pieces of data at the same time, sometimes doing asymetric
operations such as rotating, splatting, or reconfiguring the vectors. On
older machines or simple machines, the explicit instructions may not
exist, but in the world of bitwise logic, we’ve always had some SIMD
instructions hanging around as all the bitwise ops run over multiple
elements in a bit field of whatever native word length. Consider some of
the winners of the quickest bit counting routines. My favourite is the
purely SIMD style bit counter given here:

    uint32_t CountBits( uint32_t in ) {
        v = v - ((v >> 1) & 0x55555555);                    // reuse input as temporary
        v = (v & 0x33333333) + ((v >> 2) & 0x33333333);     // temp
        c = ((v + (v >> 4) & 0xF0F0F0F) * 0x1010101) >> 24; // count
        return c;
    }

So, look to your types, and see if you can add a bit of SIMD to your
development without even breaking out the vector instrinsics.

