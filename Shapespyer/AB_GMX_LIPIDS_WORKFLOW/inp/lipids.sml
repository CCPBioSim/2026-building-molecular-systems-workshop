# SMILES for the phospholipids used in the tutorial: DPPC, DOPC and POPC
#
# NOTE: no hydrogens nor stereo-descriptors are present in  SMILES below! By default, hydrogens are added automatically. 
# One can use '--dbcis C' oprion of 'smiles' tool to obtain cis-arrangments around double bonds involving C atoms.
# Otherwise (if the tool is used without this option), the hydrocarbon tails will be generated in all-trans configuration.
#
C40H80NO8P DPPCC CCCCCCCCCCCCCCCC(=O)OCC(COP([O-])(=O)OCC[N+](C)(C)C)OC(=O)CCCCCCCCCCCCCCC
C40H80NO8P DPPC [N+](C)(C)(C)CCOP([O-])(=O)OCC(COC(=O)CCCCCCCCCCCCCCC)OC(=O)CCCCCCCCCCCCCCC
#
C44H84NO8P DOPCC CCCCCCCCC=CCCCCCCCC(=O)OCC(COP([O-])(=O)OCC[N+](C)(C)C)OC(=O)CCCCCCCC=CCCCCCCCC
C44H84NO8P DOPC [N+](C)(C)(C)CCOP([O-])(=O)OCC(COC(=O)CCCCCCCC=CCCCCCCCC)OC(=O)CCCCCCCC=CCCCCCCCC
#
C42H82NO8P POPCC CCCCCCCCCCCCCCCC(=O)OCC(COP([O-])(=O)OCC[N+](C)(C)C)OC(=O)CCCCCCCC=CCCCCCCCC
C42H82NO8P POPC [N+](C)(C)(C)CCOP([O-])(=O)OCC(COC(=O)CCCCCCCCCCCCCCC)OC(=O)CCCCCCCC=CCCCCCCCC
#
# END OF SMILES
#
Box
1.0 1.0 1.0
