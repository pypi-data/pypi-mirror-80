Added joining of protein and genome properties via join-protein-position-info command.

Protein properties now calculated via prepare-protein-files command (which
join-protein-position-info calls).  

The annotate-homology command is temporily broken by this change.

All calculations except clustering (which can't avoid it) will do operations in a per-genome
and per-homology-group basis so as to avoid in-memory joins which break as the 
number of input genomes rises.

