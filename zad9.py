import ROOT as R
import array
import numpy as np
N = 20 #liczba binów
alpha = 0.05 #poziom istotoności

A = R.TTree("A","A")
A.ReadFile("dane-zad9a.txt", "A")


B = R.TTree("B","B")
B.ReadFile("dane-zad9b.txt", "B")

a = [entry.A for entry in A]
b = [entry.B for entry in B]

print(max(a), min(a))
print(max(b), min(b))

ha = R.TH1F("histA","histA",N,4,16)
hb = R.TH1F("histB","histB",N,4,16)

for entry in A:
    ha.Fill(entry.A)

for entry in B:
    hb.Fill(entry.B)


#test chi2 dla serii A i B
Na = sum(ha.GetBinContent(i) for i in range(1, N+1))
Nb = sum(hb.GetBinContent(i) for i in range(1, N+1))



X2 = 0
used_bins = 0
for i in range(1,N+1): #range iteruje do N-1 a w rooot biny numerowane są od 1 do N
    Ai = ha.GetBinContent(i)
    Bi = hb.GetBinContent(i)/Nb*Na

    

    X2 += ((Ai-Bi)**2)/(Ai+Bi)
    used_bins +=1

print(X2)
v = used_bins - 1 #liczba stopni swobody to ilosc uzytych binów-1

X2_crit = R.Math.chisquared_quantile_c(alpha, v)

if X2> X2_crit:
    print("próbki nie pochodzą z tego samego rozkładu")

else:
    print("próbki mogą pochodzić z tego samego rozkładu ")

#sprawdzenie czy wariancją A oraz B są takie same, test F Fishera

a_arr = array.array("d",a)
b_arr = array.array("d",b)

mean_a = R.TMath.Mean(len(a_arr), a_arr)
mean_b = R.TMath.Mean(len(b_arr), b_arr)

var_a = ha.GetStdDev()**2
var_b = hb.GetStdDev()**2

if var_a>=var_b:
    F = var_a/var_b
    v1 = len(a) - 1
    v2 = len(b) - 1
else:
    F = var_a/var_b
    v1 = len(b) - 1
    v2 = len(a) - 1

F_crit = R.Math.fdistribution_quantile_c(alpha/2, v1, v2)

if F>F_crit:
    print("wariancje są różne")
else: 
    print("brak podstaw by uznać że wariancje są różne")

#porównanie czy średnie A i B są takie same, test t student 

t = (mean_a - mean_b)/np.sqrt(var_a/Na + var_b/Nb) #statystyka testowa

print(t)

df = Na+Nb-2 #stopnie swobody dla testu t

t_crit = R.TMath.StudentQuantile(1 - alpha/2, df)

if abs(t)>t_crit:
    print("średnie są różne")
else:
    print("brak podstaw by uznać że średnie są różne")














c = R.TCanvas()
c.Divide(2)
c.cd(1)
ha.Draw()
c.cd(2)
hb.Draw()

c.Update()

input("cokolwiek: ")
