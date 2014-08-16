Learning to count
-----------------

Sometimes we just want to save space, and to do that we need to
understand the data being compressed. The compiler cannot do it for us,
and we will always have a better idea of what the data is meant to be
like. The best example of the difference between trying to compress
anything and being able to specialise must be the special case lossy
compressors: JPEG, MPG, and the like. In these cases, and others where
the information is held inside the data, but not all the data is
required to rebuild the information, only an external agent that is
aware of what actually constitutes important data can provide the
information about what can be ignored. Lossy algorithms are based on
what can be expected (predictions which might require a transform into a
different way of viewing the data), and what is fundamental (some basic
structure that is known, but would not be picked up by a standard
compression technique). All lossy techniques rely on knowing the
difference between what is close enough and what is unacceptable
degradation. Lossy techniques rely on biological imperfections,
something which is still hard to build a general optimiser for.

Lossless compression relies on being able to count, and in one way, we
have invented counting algorithms in forms of Huffman or arithmetic
encoding. These algorithms count before they compress, to determine the
chance of any particular element being seen. Many lossless compressors
take an approach like this, or use history relative probability, such as
run-length-encoding where repeating a value is one of two high
probability choices available during encoding. Not being able to look at
the data beforehand and come up with a realistic, or even reasonable
estimate of probability of each possible encodable value will hamper any
form of compression that relies on probabilities.

Without understanding the cause of the data, these algorithmic
approaches can only go so far. If we know the reason why the data
exists, as in where it comes from or what it’s for, there are often
opportunities for even better compression. For example, compressing the
RGB in an image with alpha, knowing that the data is bitwise AND onto
destination data that has a known set of bits set, knowing the ranges of
many parts of a document and knowing biases for values given other
values in the same document.

