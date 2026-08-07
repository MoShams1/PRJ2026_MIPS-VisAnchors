import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
from pathlib import Path

from matplotlib.pyplot import xticks

data_folder = "data/Exp1"
all_files = Path(data_folder).glob("*.json")

all_data = []
for file in all_files:
    with file.open() as f:
        data = json.load(f)

    all_data.append(data)


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

plt.figure(figsize=(5, 4))
ax = plt.gca()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

dist_cnd_m = dist_cnd_mat.mean(axis=0)
dist_cnd_sem = dist_cnd_mat.std(axis=0, ddof=1) / np.sqrt(nsubj)
plt.bar(unique_cnds,
        dist_cnd_m,
        yerr=dist_cnd_sem,
        color="lightgray")
plt.xlabel("Conditions")
plt.ylabel("Replica distance (dva)")
plt.xticks(range(12))

for subj in dist_cnd_mat:
    plt.scatter(
        unique_cnds,
        subj,
        edgecolor="none",
        facecolor="black",
        alpha=.3,
        s=20
    )

plt.axhline(y=6, color='black', linestyle="--", linewidth=1)

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

for subj in subjects_nvis:
    plt.scatter(
        cnd_list,
        subj,
        edgecolor="none",
        facecolor="black",
        alpha=.3,
        s=20
    )

plt.axhline(y=6, color='black', linestyle="--", linewidth=1)
plt.savefig("fig1B.svg")

# ----------------------------------------------------------------------------
# replica distance - two-dot configurations

nsubj = len(all_data)
cnd_dict = {
    "Single": [1, 2, 3, 4],
    "Orthogonal": [6, 8],
    "Parallel": [5, 7],
    "Diagonal": [9, 10],
    "Full": [11]}

cnd_list = list(cnd_dict.keys())

subjects = []
for isubj in range(nsubj):

    subject = []
    for _, meta_cnd_array in cnd_dict.items():
        ind = np.isin(unique_cnds, meta_cnd_array)
        subject.append(dist_cnd_mat[isubj, ind].mean())

    subjects.append(subject)

subjects_2vis = np.array(subjects)

# ----------------------------------------------------------------------------
# panel C

plt.figure(figsize=(3.5, 4))
ax = plt.gca()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

subjects_2vis_m = subjects_2vis.mean(axis=0)
subjects_2vis_sem = subjects_2vis.std(axis=0, ddof=1) / np.sqrt(nsubj)
plt.bar(cnd_list[1:-1],
        subjects_2vis_m[1:-1],
        yerr=subjects_2vis_sem[1:-1],
        color='lightgray')
plt.xlabel("Extension type")
plt.ylabel("Replica distance (dva)")

for subj in subjects_2vis:
    plt.scatter(
        cnd_list[1:-1],
        subj[1:-1],
        edgecolor="none",
        facecolor="black",
        alpha=.3,
        s=20
    )

plt.axhline(y=6, color='black', linestyle="--", linewidth=1)
plt.axhline(y=float(subjects_2vis_m[0]), color='darkgray', linestyle="-",
            linewidth=1)
plt.axhline(y=float(subjects_2vis_m[-1]), color='darkgray', linestyle="-",
            linewidth=1)
plt.savefig("fig1C.svg")

# ----------------------------------------------------------------------------
# replica distance - eccentricity

nsubj = len(all_data)
cnd_dict = {
    "Close1": [1, 2],
    "Far1": [3, 4],
    "Close2": [5],
    "Far2": [7]
}

cnd_list = list(cnd_dict.keys())

subjects = []
for isubj in range(nsubj):

    subject = []
    for _, meta_cnd_array in cnd_dict.items():
        ind = np.isin(unique_cnds, meta_cnd_array)
        subject.append(dist_cnd_mat[isubj, ind].mean())

    subjects.append(subject)

subjects_ecc = np.array(subjects)

# ----------------------------------------------------------------------------
# panel D

plt.figure(figsize=(4, 4))
ax = plt.gca()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

subjects_ecc_m = subjects_ecc.mean(axis=0)
subjects_ecc_sem = subjects_ecc.std(axis=0, ddof=1) / np.sqrt(nsubj)
x = [1, 2, 3.5, 4.5]
plt.bar(x,
        subjects_ecc_m,
        yerr=subjects_ecc_sem,
        color='lightgray')
plt.xlabel("Eccentricity")
plt.ylabel("Replica distance (dva)")

for subj in subjects_ecc:
    plt.scatter(
        x,
        subj,
        edgecolor="none",
        facecolor="black",
        alpha=.3,
        s=20
    )
plt.xticks(x, cnd_list)

plt.axhline(y=6, color='black', linestyle="--", linewidth=1)
plt.savefig("fig1D.svg")

# ----------------------------------------------------------------------------
plt.show()
