import ROOT as R
import numpy as np
from scipy.special import gamma

c = R.TCanvas("wykres chi-kwadrat", "wykres chi-kwadrat", 800, 600)
c.Divide(1,2)
#parametr stopni swobody
k = 5

def fun(x,p):
    X = x[0]
    P = p[0]
    return 1/(2**(P/2)*gamma(P/2))*X**(P/2-1)*np.exp(-X/2)

f = R.TF1("f", fun, 0, 20, 1)
f.SetParameter(0, k)

def dys(x,p):
    X = x[0]
    return f.Integral(0,X)
d = R.TF1("d", dys, 0, 20, 0)

c.cd(1)
f.Draw()
c.cd(2)
d.Draw()


c.Update()
input("woind")




