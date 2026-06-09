import ROOT as R

c1 = R.TCanvas()
alpha = 0.01

A = R.TTree("A","A")
A.ReadFile("kol2zad2dane.txt", "A")

a = [entry.A for entry in A]


print(max(a), min(a))


ha = R.TH1F("histA","histA",20,2,20)
for entry in A:
    ha.Fill(entry.A)

f = R.TF1("landau","landau",2,20)
f.SetParameters(1,1,1)

ha.Fit(f)

chi2 = f.GetChisquare()
NDF = f.GetNDF()

print(f"wartość chi2 = {chi2}")
print(f"liczba stopni swobody = {NDF}")

T_kryt = R.TMath.ChisquareQuantile(1 - alpha, NDF)

print(T_kryt)

#H0 statystyka jest opisana danym rozkładem
#h1 statystyka nie jest odpisana danym rozkładem

if chi2<T_kryt:
        print("brak podstaw do odrzucenia hipotezy o rozkładzie lanbau")
elif chi2>T_kryt:
        print("hipoteza rozkładu lanbau odrzucona")

ha.Draw()

c1.Update()
input()