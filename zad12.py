import ROOT as R


alpha = 0.05 #poziom istotnosci

#odczyt danych
A = R.TTree("A","A")
A.ReadFile("dane-zad12.txt", "A")

a = [entry.A for entry in A]



print(max(a))
print(min(a))

#zakres
m = 1.6
n = 2.1

#histogram
hist = R.TH1F("histA","histA",20,m,n)

for entry in A:
    hist.Fill(entry.A)

#funkcja gausa

#model gauss + prosta
model = R.TF1("model", "gaus(0)+pol1(3)",m,n)
#parametry
# 0 -> amplituda Gaussa
# 1 -> średnia
# 2 -> sigma
# 3 -> wyraz wolny prostej
# 4 -> współczynnik kierunkowy
model.SetParameters(hist.GetMaximum(), 1.865, 0.02, 100, 0)
fit_result = hist.Fit(model, "RS")









chi2 = model.GetChisquare()
ndf = model.GetNDF()
p_value = model.GetProb()


print("chi2 =", chi2)
print("ndf =", ndf)
print("p-value =", p_value)

# H0 - model wystarczająco dobrze opisuje dane
# H1 - model nie opisuje danych

if p_value < alpha:
    print("Odrzucamy H0: model nie opisuje danych.")
else:
    print("Nie odrzucamy H0: model opisuje dane wystarczająco dobrze.")


#przedziały ufności

#płutno na przedziały ufności 10%
graph_intervals1 = R.TGraphErrors()
#dodawanie przedziału na jakim poziom ufności ma być liczony inaczej będzie puste płutno
for i in range(hist.GetNbinsX()):
    x = hist.GetBinCenter(i + 1)
    graph_intervals1.SetPoint(i, x, 0)
#dodawanie poziomu ufności
R.TVirtualFitter.GetFitter().GetConfidenceIntervals(graph_intervals1, 0.90)
graph_intervals1.SetFillColorAlpha(R.kBlue, 0.25)


#dla ufności 1%
graph_intervals2 = R.TGraphErrors()
#dodawanie przedziału na jakim poziom ufności ma być liczony
for i in range(hist.GetNbinsX()):
    x = hist.GetBinCenter(i + 1)
    graph_intervals2.SetPoint(i, x, 0)
#dodawanie poziomu funości
R.TVirtualFitter.GetFitter().GetConfidenceIntervals(graph_intervals2, 0.99)
graph_intervals2.SetFillColorAlpha(R.kGreen, 0.25)

#macierze korelacji i kowariancji
cov = fit_result.GetCovarianceMatrix()
cor = fit_result.GetCorrelationMatrix()

print("Macierz kowariancji:")
cov.Print()

print("Macierz korelacji:")
cor.Print()


#rysowanie
c1 = R.TCanvas()
hist.Draw()
graph_intervals1.Draw("3 same")
#graph_intervals2.Draw("3 same")
model.Draw("same")

c2 = R.TCanvas()
hist.Draw()
#graph_intervals1.Draw("3 same")
graph_intervals2.Draw("3 same")
model.Draw("same")






input()