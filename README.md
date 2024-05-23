Bridge RNA Designer
===================

A command line and web interface for designing Bridge RNAs for Bridge Editing.

# CLI

## Installation

```bash
pip install -e .
```

## Usage

Command to design a Bridge RNA for a given target and donor sequence.
```bash
brna-design --target ATCGGGCCTACGCA --donor ACAGTATCTTGTAT
```

Example output:

```console
# STOCKHOLM 1.0
BridgeRNA_tgt_ATCGGGCCTACGCA_dnr_ACAGTATCTTGTAT     AGTGCAGAGAAAATCGGCCAGTTTTCTCTGCCTGCAGTCCGCATGCCGTATCGGGCCTTGGGTTCTAACCTGTTGCGTAGATTTATGCAGCGGACTGCCTTTCTCCCAAAGTGATAAACCGGACAGTATCATGGACCGGTTTTCCCGGTAATCCGTATTTACAAGGCTGGTTTCACT
#=GC bRNA_template                                  AGTGCAGAGAAAATCGGCCAGTTTTCTCTGCCTGCAGTCCGCATGCCGTNNNNNNNNNTGGGTTCTAACCTGTNNNNNNNNNTTATGCAGCGGACTGCCTTTCTCCCAAAGTGATAAACCGGNNNNNNNNATGGACCGGTTTTCCCGGTAATCCGTNNTTNNNNNNNTGGTTTCACT
#=GC guides                                         .................................................LLLLLLLCC...............RRRRRCCHH........................................lllllllc..........................rr..rrrcchh..........
#=GC SS                                             ((.(((((((((((......)))))))))))))(((((((((.(((.............<(((.<>.)))>...............))))))))))))...........((((...<(((..........<.(((((((.....)))))...))....>.........)))>.))))
//
```


# Webtool

[Published app](bridge.hsulab.arcinstitute.org)

### Run locally

```bash
streamlit run app.py --server.address=0.0.0.0
```
