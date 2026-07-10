import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
from pathlib import Path

data_folder = "data/Exp1"
all_files = Path(data_folder).glob("*.json")

all_data = []
for file in all_files:
    with file.open() as f:
        data = json.load(f)

    all_data.append(data)

# todo: make a function to "clean" plots
# todo: modify the first plot
# todo: make plot for the two-dot conditions
# todo: make plot for the eccentricity

# ----------------------------------------------------------------------------
# replica distance - all conditions
# ----------------------------------------------------------------------------

nsubj = len(all_data)
unique_cnds = []
subjects = []
for isubj in range(nsubj):
    df = pd.DataFrame(all_data[isubj])
    unique_cnds = sorted(df["visanchor_cnd"].unique())
    subject = []
    for i, cnd in enumerate(unique_cnds):
        ind = df["visanchor_cnd"] == cnd
        subject.append(df.loc[ind, "replica_dist"].abs().mean())
    subjects.append(subject)
dist_cnd_mat = np.array(subjects)

# ----------------------------------------------------------------------------
# panel A

plt.figure()
ax = plt.gca()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

dist_cnd_m = dist_cnd_mat.mean(axis=0)
dist_cnd_sem = dist_cnd_mat.std(axis=0, ddof=1) / np.sqrt(nsubj)
plt.bar(unique_cnds, dist_cnd_m, yerr=dist_cnd_sem)
plt.xlabel("Conditions")
plt.ylabel("Replica distance (dva)")

for row in dist_cnd_mat:
    plt.scatter(
        unique_cnds,
        row,
        color="black"
    )
plt.savefig("fig1A.svg")

# ----------------------------------------------------------------------------
# replica distance - number of visual anchors

nsubj = len(all_data)
cnd_dict = {
    "1": [1, 2, 3, 4],
    "2": [5, 6, 7, 8, 9, 10],
    "4": [11]}

cnd_list = list(cnd_dict.keys())

subjects = []
for isubj in range(nsubj):

    subject = []
    for _, meta_cnd_array in cnd_dict.items():
        ind = np.isin(unique_cnds, meta_cnd_array)
        subject.append(dist_cnd_mat[isubj, ind].mean())

    subjects.append(subject)

subjects_nvis = np.array(subjects)

# ----------------------------------------------------------------------------
# panel B

plt.figure(figsize=(3.5, 4))
ax = plt.gca()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

subjects_nvis_m = subjects_nvis.mean(axis=0)
subjects_nvis_sem = subjects_nvis.std(axis=0, ddof=1) / np.sqrt(nsubj)
plt.bar(cnd_list,
        subjects_nvis_m,
        yerr=subjects_nvis_sem,
        color='lightgray')
plt.xlabel("Number of visual markers")
plt.ylabel("Replica distance (dva)")

for row in subjects_nvis:
    plt.scatter(
        cnd_list,
        row,
        edgecolor="none",
        facecolor="black",
        alpha=.3,
        s=20
    )

plt.axhline(y=6, color='black', linestyle="--", linewidth=1)
plt.savefig("fig1B.svg")

# ----------------------------------------------------------------------------
plt.show()
