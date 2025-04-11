# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.7
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score

# %%
sheet = pd.read_excel(
    "count.ods",
    sheet_name="Sheet1",
    header=int(0),
    usecols="A:D"
)
sheet

# %%
_filtered = sheet[sheet["year"]>2021]
_filtered["applied"]/_filtered["finished"]
_filtered = _filtered.assign(ratio= _filtered["finished"]/_filtered["applied"])

# %%
applicants = sheet[["year","applied"]].dropna()
ranks = sheet[["year","finished"]].dropna()

# %%
dataX = sheet["year"].to_list()
range1=np.linspace(dataX[0]-1,dataX[-1]+2,1000)

# %%
fncPoly = lambda x,b,c,d:b*x**2+c*x+d

fitApplicants = curve_fit(
    fncPoly,
    applicants["year"],
    applicants["applied"]
)[0]
fitRanks = curve_fit(
    fncPoly,
    ranks["year"],
    ranks["finished"]
)[0]

fncFitApplicants = lambda x:fncPoly(x,*fitApplicants)
fncFitRanks = lambda x:fncPoly(x,*fitRanks)

fitPolyX = range1
fitApplicantsY = list(map(fncFitApplicants,range1))
fitRanksY = list(map(fncFitRanks,range1))

r2_applicants = r2_score(
    applicants["applied"],
    list(map(fncFitApplicants,applicants["year"]))
)
r2_ranks = r2_score(
    ranks["finished"],
    list(map(fncFitRanks,ranks["year"]))
)

print(f"applicants: {fitApplicants[0]} * x**2 + {fitApplicants[1]} * x + {fitApplicants[2]} \n r^2: {r2_applicants}")
print(f"ranks: {fitRanks[0]} * x**2 + {fitRanks[1]} * x + {fitRanks[2]} \n r^2: {r2_ranks}")

# %%
fig,ax = plt.subplots(figsize=(8, 8),dpi=200)
plt.rcParams['font.family'] = "Roboto"
plt.rcParams['font.size'] = 10
# matplotlib.rcParams['text.antialiased'] = False
# matplotlib.rcParams["lines.antialiased"] = False
# matplotlib.rcParams["patch.antialiased"] = False

plt.plot(
    fitPolyX,
    fitApplicantsY,
    label=f"Quadratic fit Applicants $R^2=${r2_applicants:.5f}",
    linestyle="--",
    # linewidth=1,
    color="green",
)

plt.plot(
    fitPolyX,
    fitRanksY,
    label=f"Quadratic fit Ranks $R^2=${r2_ranks:.5f}",
    linestyle="--",
    # linewidth=1,
    color="red",
)

plt.scatter(
    applicants["year"],
    applicants["applied"],
    marker="x",
    color="blue",
    s=60.0,
    zorder=10)
for i,_ in enumerate(dataX):
    plt.annotate(
        applicants["applied"][i],
        (applicants["year"][i],applicants["applied"][i]-60)
    )

_derived = sheet[sheet["year"]<=2021]
plt.scatter(
    _derived["year"],
    _derived["finished"],
    marker="x",
    color="green",
    s=60.0,
    zorder=10)
plt.text(0.02,0.84,
    "Green points were derived from \napplicant and MOOC counts",
    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
    transform=ax.transAxes
    )


plt.scatter(
    _filtered["year"],
    _filtered["finished"],
    marker="x",
    color="blue",
    s=60.0,
    zorder=10)
for i,_ in enumerate(ranks["year"]):
    plt.annotate(
        int(ranks["finished"][i]),
        (ranks["year"][i],ranks["finished"][i]-60)
    )

plt.xlabel("year")
plt.ylabel("applicants")
plt.title("tud aerospace applicants and ranks")
# plt.yticks(np.arange(1200,3000,100))
ax.yaxis.set_major_locator(ticker.MultipleLocator(100))
plt.grid(linestyle='--')
plt.legend()
ax.xaxis.set_ticks(range(dataX[0]-1,dataX[-1]+2))
plt.xlim(dataX[0]-1,dataX[-1]+2)


labels = [item.get_text() for item in ax.get_xticklabels()]
for (key,value) in enumerate(labels):
    try:
        labels[key] = value + f"\n ratio:{_filtered[_filtered["year"]==int(value)]["ratio"].dropna().to_list()[0]:.2f}"
    except:
        pass

ax.set_xticklabels(labels)

# plt.xlim(2000,2030)
# plt.ylim(1250,3000)

pred = [
    [applicants["year"].iloc[-1]+1,fncFitApplicants(applicants["year"].iloc[-1]+1)],
    [ranks["year"].iloc[-1]+1,fncFitRanks(ranks["year"].iloc[-1]+1)]
]

plt.ylim(
    round(fncFitRanks(applicants["year"].iloc[0]-1)-100,-2),
    round(pred[0][1]+(pred[0][1] - ranks["finished"].iloc[0])*0.15,-2)
)

plt.scatter(
    pred[0][0],
    pred[0][1],
    marker="o",
    color="brown",
    s=60.0,
    zorder=10
)

plt.scatter(
    pred[1][0],
    pred[1][1],
    marker="o",
    color="brown",
    s=60.0,
    zorder=10
)

for i in pred:
    plt.annotate(
        int(i[1]),
        (i[0]+0.06,i[1]-60)
    )


plt.show()

# %%
fig.savefig("poly.png",bbox_inches='tight')
