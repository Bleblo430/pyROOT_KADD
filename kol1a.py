import ROOT as R
import numpy as np

def fun(x,p):
    X = x[0]
    C = p[0]
    return C * np.exp(-X) * np.sin(X)

f_unnorm = R.TF1("f_unnorm", fun, 1/10, 2, 1)
f_unnorm.SetParameter(0,1)

#normalizacja funkcji
const = 1/f_unnorm.Integral(1/10,2)

f = R.TF1("f", fun, 1/10, 2, 1)
f.SetParameter(0, const)

def dystrybuanta(x,p):
    return f.Integral(0,x[0])

d = R.TF1("d", dystrybuanta, 1/10, 2, 0)

#wartość oczekiwana
mean = f.Mean(1/10,2)
print("Wartość oczekiwana =", mean)
#wariancja
var = f.Variance(1/10,2)
print("Wariancja =", var)
#kwantyl 0.4
kwan = d.GetX(0.4)
print("Kwantyl 0.4 =", kwan)

#rysowanie dystrybuanty
c1 = R.TCanvas("c1", "Dystrybuanta", 800, 600)

d.Draw()
d.SetTitle("Dystrybuanta")

c1.Update()

input("Naciśnij Enter, aby zakończyć...")

