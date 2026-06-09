import ROOT as R
import array
import numpy as np

alpha = 0.05 #poziom istotoności
N = 20

A = R.TTree("A","A")
A.ReadFile("kol2zad3daneA.txt", "A")


B = R.TTree("B","B")
B.ReadFile("kol2zad3daneB.txt", "B")

a = [entry.A for entry in A]
b = [entry.B for entry in B]

print(max(a), min(a))
print(max(b), min(b))

ha = R.TH1F("histA","histA",N,0,5)
hb = R.TH1F("histB","histB",N,0,5)

for entry in A:
    ha.Fill(entry.A)

for entry in B:
    hb.Fill(entry.B)

a_arr = array.array("d",a)
b_arr = array.array("d",b)

mean_a = R.TMath.Mean(len(a_arr), a_arr)
mean_b = R.TMath.Mean(len(b_arr), b_arr)

Na = sum(ha.GetBinContent(i) for i in range(1, N+1))
Nb = sum(hb.GetBinContent(i) for i in range(1, N+1))

var_a = ha.GetStdDev()**2
var_b = hb.GetStdDev()**2

t = (mean_a - mean_b)/np.sqrt(var_a/Na + var_b/Nb) #statystyka testowa

print(t)

df = Na+Nb-2 #stopnie swobody dla testu t

t_crit = R.TMath.StudentQuantile(1 - alpha/2, df)

#H0: średnia1 = średnia 2
#H1: średnie są różne
if abs(t)>t_crit:
    print("średnie są różne")
else:
    print("brak podstaw by uznać że średnie są różne")