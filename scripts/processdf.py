import pandas as pd
import numpy as np
from sys import argv
import json
import ast
from collections import Counter

# Importing the prediction tsv and metadata sheet
pred = pd.read_csv(str(argv[1]), sep='\t')
meta = pd.read_csv(str(argv[2]), sep=',')

# Merging the two using the "image" column
pred = pd.merge(pred, meta, on="image", how="inner")

# Required processing which extracts MN/all nuclei
if type(pred.nuclei.loc[0]) == str:
    pred['nuclei'] = pred['nuclei'].apply(ast.literal_eval)
    pred['micronuclei'] = pred['micronuclei'].apply(ast.literal_eval)
        
pred['totalnuc'] = [len(x['coord']) for x in pred['nuclei']]
pred['totalmn'] = [len(x['coord']) for x in pred['micronuclei']]
pred['mnpernuc'] = np.where( pred['totalnuc'] > 0, pred['totalmn'] / pred['totalnuc'], np.nan )

# The following steps are optional. Extract the indexed "parent" nucleus, identified in close proximity to the segmented MN. 
# Users who wish to skip these steps, may comment (#) these lines of code out.
pred['parentcounter'] = None

for idx, row in pred.iterrows():
    if row.totalnuc>0:
        pred.loc[idx, 'uniqueNucprod'] = (len(set(row.micronuclei['parent'])))
        pred.at[idx, 'parentcounter'] = dict(Counter(row.micronuclei['parent']))
        pred.loc[idx, 'MEANparentcountperMN'] = np.mean(list(Counter(row.micronuclei['parent']).values()))
        pred.loc[idx, 'MEANmnarea'] = np.mean(row.micronuclei['area'])

        grab= []
        for i in row.micronuclei['bbox']:
            w = i[2] - i[0]
            h = i[3] - i[1]
            if (w>h) & (h!=0):
                grab.append(w/h)
            elif (w<=h) & (w!=0):
                grab.append(h/w)
        pred.loc[idx, 'MEANmnshape'] = np.mean(grab)

        grab2 = []
        for j in range(len(row.micronuclei['parent'])):
            parentindex = row.micronuclei['parent'][j]
            grab2.append(row.micronuclei['area'][j]/row.nuclei['area'][parentindex])
        pred.loc[idx, 'relativeArea'] = np.mean(grab2)
        pred['perNucProdMns'] = (pred['uniqueNucprod']/pred['totalnuc'])    

# [Not optional] Saving the final processed dataframe
pred.to_csv('./MicroNucMLProtocol/output/ProcessedExample.tsv', sep='\t', index=False)
