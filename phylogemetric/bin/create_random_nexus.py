"""
Generate random data for performance benchmark.
"""

from random import choice
import argparse

N_SEQUENCES = 50
SEQ_LEN    = 10000
CHARACTERS = list("0000000001")

HEADER = """#NEXUS
Begin data;
Dimensions ntax={} nchar={};
Format datatype=dna missing=? gap=-;
Matrix
"""

FOOTER = """;
End;
"""

def create_nex(nseq, seqlen, chars):
    nex = HEADER.format(nseq, seqlen)
    for i in range(nseq):
        seq = ""
        name = "species{:03d}".format(i)
        for j in range(seqlen):
            seq += choice(chars)
        nex += "{:<11s}\t{}\n".format(name, seq)
    nex += FOOTER
    return nex


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create random Nexus file for benchmarking.')
    parser.add_argument('nseq', type=int, default=N_SEQUENCES,
                   help='number of randomly generated sequences')
    parser.add_argument('seqlen', type=int, default=SEQ_LEN,
                   help='length of randomly generated sequences')
    parser.add_argument('chars', type=str, default=CHARACTERS,
                   help='characters to generate random species from')

    args = parser.parse_args()
    nex = create_nex(args.nseq, args.seqlen, args.chars)
    print(nex)
