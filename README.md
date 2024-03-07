# BridgeRNADesigner
A command line interface for designing Bridge RNAs for Bridge Editing.

## Installation
```bash
tar -zxvf BridgeRNADesigner.tar.gz
cd BridgeRNADesigner/
pip install .
```

## Usage
Command to design a Bridge RNA for a given target and donor sequence.
```bash
brna-design --target ATCGGGCCTACGCA --donor ACAGTATCTTGTAT
```

Example output:
```bash
# STOCKHOLM 1.0
BridgeRNA_tgt_ATCGGGCCTACGCA_dnr_ACAGTATCTTGTAT     AGTGCAGAGAAAATCGGCCAGTTTTCTCTGCCTGCAGTCCGCATGCCGTATCGGGCCTTGGGTTCTAACCTGTTGCGTAGATTTATGCAGCGGACTGCCTTTCTCCCAAAGTGATAAACCGGACAGTATCATGGACCGGTTTTCCCGGTAATCCGTATTTACAAGGCTGGTTTCACT
#=GC bRNA_template                                  AGTGCAGAGAAAATCGGCCAGTTTTCTCTGCCTGCAGTCCGCATGCCGTNNNNNNNNNTGGGTTCTAACCTGTNNNNNNNNNTTATGCAGCGGACTGCCTTTCTCCCAAAGTGATAAACCGGNNNNNNNNATGGACCGGTTTTCCCGGTAATCCGTNNTTNNNNNNNTGGTTTCACT
#=GC guides                                         .................................................LLLLLLLCC...............RRRRRCCHH........................................lllllllc..........................rr..rrrcchh..........
#=GC SS                                             ((.(((((((((((......)))))))))))))(((((((((.(((.............<(((.<>.)))>...............))))))))))))...........((((...<(((..........<.(((((((.....)))))...))....>.........)))>.))))
//
```