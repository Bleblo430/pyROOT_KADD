import ROOT as R
import array

N = 20
alpha = 0.05

A = R.TTree("A","A")
A.ReadFile("dane-zad10a.txt", "A")


B = R.TTree("B","B")
B.ReadFile("dane-zad10b.txt", "B")



a = [entry.A for entry in A]
b = [entry.B for entry in B]

print(max(a), min(a))
print(max(b), min(b))

ha = R.TH1F("histA","histA",N,0,20)
hb = R.TH1F("histB","histB",N,0,20)

for entry in A:
    ha.Fill(entry.A)

for entry in B:
    hb.Fill(entry.B)

a_arr = array.array("d",a)
b_arr = array.array("d",b)

mean_a = R.TMath.Mean(len(a_arr), a_arr)
mean_b = R.TMath.Mean(len(b_arr), b_arr)

var_a = ha.GetStdDev()**2
var_b = hb.GetStdDev()**2

#test jednostronny na wariancje 

#H0 - var a = var b
#H1 - var a > var b 
if var_a>=var_b:
    F = var_a/var_b
    v1 = len(a) - 1
    v2 = len(b) - 1
else:
    F = var_b/var_a
    v1 = len(b) - 1
    v2 = len(a) - 1

F_crit = R.Math.fdistribution_quantile_c(alpha, v1, v2)

if F>F_crit:
    print("wynik testu jednostronnego: wariancje są różne")
else: 
    print("wynik testu jednostronnego: brak podstaw by uznać że wariancje są różne")

#test obustronny
#H0 - var a = var b
#H1 - var a != var b 

if var_a >= var_b:
    F = var_a / var_b
    v1 = len(a) - 1   # stopnie swobody licznika
    v2 = len(b) - 1   # stopnie swobody mianownika
else:
    F = var_b / var_a
    v1 = len(b) - 1
    v2 = len(a) - 1

# test DWUSTRONNY więc alpha/2
F_crit = R.Math.fdistribution_quantile_c(alpha/2, v1, v2)



