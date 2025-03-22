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
dataX=list(sheet.year.iloc)
dataY=list(sheet.applied.iloc)

# %%
range1=np.linspace(dataX[0]-1,dataX[-1]+2,1000)

# %%
fncPoly = lambda x,b,c,d:b*x**2+c*x+d
fitPoly = curve_fit(
    fncPoly,
    dataX,
    dataY
)[0]
fncFitPoly = lambda x:fncPoly(x,*fitPoly)
fitPolyX = range1
fitPolyY = list(map(fncFitPoly,range1))

r2_poly = r2_score(
    dataY,
    list(map(fncFitPoly,dataX))
)

print(fitPoly)
print(f"{fitPoly[0]} * x**2 + {fitPoly[1]} * x + {fitPoly[2]} ")
print(r2_poly)

# %%
fncGrowth = lambda x,a,b:a*b**(x-dataX[2])
fitGrowth = curve_fit(
    fncGrowth,
    dataX,
    dataY,
    p0=[1,1.14],
    maxfev=10000
)[0]
fncFitGrowth = lambda x:fncGrowth(x,*fitGrowth)
fitGrowthX = range1
fitGrowthY = list(map(
    fncFitGrowth,
    range1
))

r2_growth=r2_score(
    dataY,
    list(map(fncFitGrowth,dataX))
)

print(fitGrowth)
print(r2_growth)

# %%
fig,ax = plt.subplots(figsize=(8, 8),dpi=200)
matplotlib.rcParams['font.family'] = "Roboto"
matplotlib.rcParams['font.size'] = 10
# matplotlib.rcParams['text.antialiased'] = False
# matplotlib.rcParams["lines.antialiased"] = False
# matplotlib.rcParams["patch.antialiased"] = False

plt.plot(
    fitPolyX,
    fitPolyY,
    label=f"Quadratic fit $R^2=${r2_poly:.5f}",
    linestyle="--",
    # linewidth=1,
    color="red",
)
plt.plot(
    fitGrowthX,
    fitGrowthY,
    label=f"Growth fit $R^2=${r2_growth:.5f}",
    linestyle="--",
    # linewidth=1,
    color="green",
)

plt.scatter(
    dataX,
    dataY,
    marker="x",
    color="blue",
    s=60.0,
    zorder=10)
for i,_ in enumerate(dataX):
    plt.annotate(
        dataY[i],
        (dataX[i],dataY[i]-60)
    )

plt.bar(
    2025,
    fncFitPoly(dataX[-1]+1)-fncFitGrowth(dataX[-1]+1),
    bottom=fncFitGrowth(dataX[-1]+1),
    width=0.1,
    color="grey",
    zorder=10
)
plt.annotate(
    int(np.round(fncFitPoly(dataX[-1]+1))),
    (dataX[-1]+1.1,fncFitPoly(dataX[-1]+1))
)
plt.annotate(
    int(np.round(fncFitGrowth(dataX[-1]+1))),
    (dataX[-1]+1.1,fncFitGrowth(dataX[-1]+1))
)
plt.annotate(
    "(projection)",
    (dataX[-1]+1,fncFitPoly(dataX[-1]+1)+(fncFitPoly(dataX[-1]+1)-fncFitPoly(dataX[-1]))*0.7),
    ha="center"
)
plt.xlabel("year")
plt.ylabel("applicants")
plt.title("tud aerospace applicants")
# plt.yticks(np.arange(1200,3000,100))
ax.yaxis.set_major_locator(ticker.MultipleLocator(100))
plt.grid(linestyle='--')
plt.legend()
plt.xlim(dataX[0]-1,dataX[-1]+2)
# plt.xlim(2000,2030)
# plt.ylim(1250,3000)
plt.show()

# %%
fig.savefig("applicants.png")
