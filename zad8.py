import ROOT as R

X = R.TTree("X","X")
X.ReadFile("dane-zad8.txt","X")

x = [entry.X for entry in X]



print(max(x))

hist = R.TH1I("hist","hist",8,-0.5,7.5) #ustawienie binów dla zakresu 0 do N na od -0.5 do N+0.5 i lczby binów N=1 powoduje że środki binów są w wartościach całkowitych

for entry in X:
    hist.Fill(entry.X)

poisson = R.TF1("poisson", "[1] * TMath::Poisson(x, [0])",0,7)

#parametry startowe
#parametr 0 to lambda 1 to stala normalizująca 
mean = hist.GetMean()
const = hist.Integral()
poisson.SetParameter(0,mean)
poisson.SetParameter(1,const)

poisson_chi2 = R.TF1("poisson_chi2", "[1]*TMath::Poisson(x,[0])", 0, 7)
poisson_mle  = R.TF1("poisson_mle",  "[1]*TMath::Poisson(x,[0])", 0, 7)

poisson_chi2.SetParameter(0,mean)
poisson_chi2.SetParameter(1,const)

poisson_mle.SetParameter(0,mean)
poisson_mle.SetParameter(1,const)

mle = hist.Fit(poisson_mle, "LS") #parametr L to loglikehood Parametr S zapisuje wynik fitu by uzyc go jako zmiennej
chi2 = hist.Fit(poisson_chi2, "RS+") #parametr R to chi kwadrat parametr + powoduje że poprzednie dopasowanie nie zostaje nadpisane

########################
#statystyka testowa

#liczba stopni sowobody
v_chi2 = poisson_chi2.GetNDF()
v_mle = poisson_mle.GetNDF()

T_chi2=0
for i in range(1, hist.GetNbinsX()+1): #histogramy root maja dodatkowe biny, bin 0 underflow i bin N+1 bin overflow ponieważ range iteruje od do N-1 musimy celować i tak w bin overflow
    n_obs = hist.GetBinContent(i)
    x = poisson_chi2.Eval(i-1)
    T_chi2+= ((n_obs-x)**2)/x

T_mle=0
for i in range(1, hist.GetNbinsX()+1): #histogramy root maja dodatkowe biny, bin 0 underflow i bin N+1 bin overflow ponieważ range iteruje od do N-1 musimy celować i tak w bin overflow
    n_obs = hist.GetBinContent(i)
    x = poisson_mle.Eval(i-1)
    T_mle+= ((n_obs-x)**2)/x

def chi2test(T,NDF,alpha):
    T_kryt = R.TMath.ChisquareQuantile(1 - alpha, NDF)
    if T<T_kryt:
        print("brak podstaw do odrzucenia hipotezy o rozkładzie poissona")
    elif T>T_kryt:
        print("hipoteza rozkładu poissona odrzucona")

alpha = 0.05

print(T_chi2)
print(T_mle)

chi2test(T_chi2,v_chi2,alpha)
chi2test(T_mle,v_mle,alpha)



for i in range(1, hist.GetNbinsX()+1):
    print(hist.GetBinContent(i),poisson_mle.Eval(i-1))





c = R.TCanvas()
c.Divide(2)

c.cd(1)
hist.Draw()
mle.Draw("SAME")

c.cd(2)
hist.Draw()
chi2.Draw("SAME")







c.Update()
input("iqws")