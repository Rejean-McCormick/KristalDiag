NEUTRAL_REQUIRED=['N00','N01','N02','N03','N04','N06']
V7_BASE=NEUTRAL_REQUIRED + ['K00','K01','K02','K03','K04','K12','K13']
V9_READER=NEUTRAL_REQUIRED + ['K00','K01','K15','K16','K17','K22','K23']
PROFILES={
 'V7-Reader': V7_BASE,
 'V7-Mesh': NEUTRAL_REQUIRED + ['K00','K01','K02','K03','K04','K05','K06','K10','K12','K13'],
 'V7-Projection': NEUTRAL_REQUIRED + ['K00','K01','K02','K03','K04','K05','K06','K07','K08','K09','K10','K12','K13'],
 'V7-Kristall': NEUTRAL_REQUIRED + ['K00','K01','K02','K03','K04','K05','K06','K07','K08','K09','K10','K11','K12','K13'],
 'V9-State-Reader': V9_READER,
 'V9-Builder': V9_READER + ['K18'],
 'V9-Materializer': V9_READER + ['K19'],
 'V9-Publisher': V9_READER + ['K21'],
 'V9-Full': V9_READER + ['K18','K19','K20','K21','K24'],
}
ORDER=['V7-Reader','V7-Mesh','V7-Projection','V7-Kristall','V9-State-Reader','V9-Builder','V9-Materializer','V9-Publisher','V9-Full']
