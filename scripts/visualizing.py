import pandas as pd
import numpy as np
from sys import argv
import matplotlib.pyplot as plt
import seaborn as sns
from statannotations.Annotator import Annotator

# Importing the prediction tsv and metadata sheet
final = pd.read_csv(str(argv[1]), sep='\t')

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(10, 5),)

pairs=[(0, 8)]

sns.boxplot(ax=ax[0], data=final, x="Condition_Gy", y="mnpernuc")
sns.stripplot(ax=ax[0], data=final, x="Condition_Gy", y="mnpernuc", color='black')

ax[0].set_ylabel("MN/all Nuclei", fontsize=20)
ax[0].set_xlabel("IR Dose (Gy)", fontsize=20)
ax[0].tick_params(labelsize=15)

annotator = Annotator(ax[0], pairs, data=final, x="Condition_Gy", y="mnpernuc")
annotator.configure(test='t-test_ind',text_format='simple',)
annotator.apply_and_annotate()


sns.boxplot(ax=ax[1], data=final, x="Condition_Gy", y="perNucProdMns")
sns.stripplot(ax=ax[1], data=final, x="Condition_Gy", y="perNucProdMns", color='black')

ax[1].set_ylabel("Proportion of parent nuclei", fontsize=20)
ax[1].set_xlabel("IR Dose (Gy)", fontsize=20)
ax[1].tick_params(labelsize=15)

annotator = Annotator(ax[1], pairs, data=final, x="Condition_Gy", y="perNucProdMns")
annotator.configure(test='t-test_ind', text_format='simple',)
annotator.apply_and_annotate()
plt.tight_layout()
plt.savefig('./MicroNucMLProtocol/output/ComparingGy.pdf')
