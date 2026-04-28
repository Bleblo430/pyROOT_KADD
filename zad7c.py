import numpy as np
import ROOT as R
c = R.TCanvas("c", "histogram sumy", 800, 600)
#zakres
a = 0
b = 1

#liczba próbek
I = 1e6

N = 10
h = R.TH1F(f"h{N}", f"histogram {N}", 100,0,2*np.pi)
for i in range(int(I)):
    s = 0
    for j in range(N):
        s+=np.random.uniform(a,b)
    s = s%2*np.pi
    h.Fill(s)

h.Draw("HIST")
c.Update()
input("windo")