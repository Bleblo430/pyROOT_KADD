import numpy as np
import ROOT as R
c = R.TCanvas("c", "histogram sumy", 800, 600)
#zakres
a = 0
b = 1

#liczba próbek
I = 1e4

N = 2
while N<10:
    h = R.TH1F(f"h{N}", f"histogram {N}", 100,0,N)
    for i in range(int(I)):
        s = 0
        for j in range(N):
            s+=np.random.uniform(a,b)
        h.Fill(s)
    h.Fit("gaus", "Q")
    fit = h.GetFunction("gaus")
    val = fit.GetChisquare()/fit.GetNDF()
    if val < 1.3:
        print(f"Znaleziono N={N} z chi2/ndf={val}")
        break
    print(f"iteracja N={N} z chi2/ndf={val}")
   
    N+=1


h.Draw("HIST")
fit.Draw("same")
c.Update()

input("windo")


