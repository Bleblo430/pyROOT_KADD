import ROOT as R

c1 = R.TCanvas()

f1 = R.TF1("poisson1", "TMath::Poisson(x, 0.1)",0,60)
f2 = R.TF1("poisson2", "TMath::Poisson(x, 0.5)",0,60)
f3 = R.TF1("poisson3", "TMath::Poisson(x, 1)",0,60)
f4 = R.TF1("poisson4", "TMath::Poisson(x, 2)",0,60)
f5 = R.TF1("poisson5", "TMath::Poisson(x, 3)",0,60)
conv1 = R.TF1Convolution(f1,f2,True)
conv1.SetRange(0,60)
conv1.SetNofPointsFFT(1000)

f0 = R.TF1("fdata", conv1, 0, 60, conv1.GetNpar())

f0.Draw()



input()


