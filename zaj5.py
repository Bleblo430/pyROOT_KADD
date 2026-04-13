import ROOT as R
import numpy as np


X1 = R.TTree("X1","X1")
X1.ReadFile("X1.txt","X1")

X2 = R.TTree("X2","X2")
X2.ReadFile("X2.txt","X2")

X3 = R.TTree("X3","X3")
X3.ReadFile("X3.txt","X3") #od tąd do góy wczytanie danych

x1 = [entry.X1 for entry in X1] #zczytywanie danych przez ROOT daje obiekty typu root 
x2 = [entry.X2 for entry in X2] #żeby dostać obiekty do wykonywania normalnych operacji trzeba przerobić je na tablice ew na obiekty np.array
x3 = [entry.X3 for entry in X3]

#muszą być znumpyowane żeby działały operacje mnożenie dodawanie itd
x1 = np.array(x1)
x2 = np.array(x2)
x3 = np.array(x3)


#histogramy do odczytu wartości std, mean
histx1 = R.TH1F("histx1","histx1",200,0,20)
histx2 = R.TH1F("histx2","histx2",200,0,20)
histx3 = R.TH1F("histx3","histx3",200,0,20)

#wypełnianie histogramów
for entry in X1:
    histx1.Fill(entry.X1)
for entry in X2:
    histx2.Fill(entry.X2)
for entry in X3:
    histx3.Fill(entry.X3)

meanx1 = histx1.GetMean()
stdx1 = histx1.GetStdDev()

meanx2 = histx2.GetMean()
stdx2 = histx2.GetStdDev()

meanx3 = histx3.GetMean()
stdx3 = histx3.GetStdDev()

print(f"średnia dla X1 = {meanx1}, odchylenie standardowe (error) = {stdx1}")
print(f"średnia dla X2 = {meanx2}, odchylenie standardowe (error) = {stdx2}")
print(f"średnia dla X3 = {meanx3}, odchylenie standardowe (error) = {stdx3}")

#związki/histogramy 2D

hx1vsx2 = R.TH2F("x1vsx2","x1vsx2",200,0,20,200,0,20)
hx1vsx3 = R.TH2F("x1vsx3","x1vsx3",200,0,20,200,0,20)
hx2vsx3 = R.TH2F("x2vsx3","x2vsx3",200,0,20,200,0,20)

for d1,d2 in zip(X1,X2):
    hx1vsx2.Fill(d1.X1,d2.X2)
    
for d1,d3 in zip(X1,X3):
    hx1vsx3.Fill(d1.X1,d3.X3)

for d2,d3 in zip(X2,X3):
    hx2vsx3.Fill(d2.X2,d3.X3)    
    
    
    
#rysowanie histogramów
from IPython.display import display

c1 = R.TCanvas()

c1.Divide(3)
c1.cd(1)
hx1vsx2.Draw("COLZ")
c1.cd(2)
hx1vsx3.Draw("COLZ")
c1.cd(3)
hx2vsx3.Draw("COLZ")

#macierz kowariancji dla X

cov12 = hx1vsx2.GetCovariance()
cov13 = hx1vsx3.GetCovariance()
cov23 = hx2vsx3.GetCovariance()

var1 = stdx1**2
var2 = stdx2**2
var3 = stdx3**2

Cx = R.TMatrixD(3,3)
Cx[0][0] = var1
Cx[0][1] = cov12
Cx[0][2] = cov13
Cx[1][0] = cov12
Cx[1][1] = var2
Cx[1][2] = cov23
Cx[2][0] = cov13
Cx[2][1] = cov23
Cx[2][2] = var3



#zabawa Y
y1 = 3 + 1.5* x1 + 4*x2
y2 = 2*x1 + 5*x2 + x3
#macierfz współczynników z zadania
T = R.TMatrixD(2,3)
T[0][0] = 1.5
T[0][1] = 4
T[0][2] = 0
T[1][0] = 2
T[1][1] = 5
T[1][2] = 1

T_transposed = R.TMatrixD(3,2)
T_transposed.Transpose(T)

Cymstep1 = R.TMatrixD(2,3)
Cymstep1.Mult(T, Cx)

Cym = R.TMatrixD(2,2)
Cym.Mult(Cymstep1, T_transposed)



histy1 = R.TH1F("histy1","histy1",200,0,20)
histy2 = R.TH1F("histy2","histy2",200,0,20)
for entry in y1:
    histy1.Fill(entry)
for entry in y2:
    histy2.Fill(entry)

meany1 = histy1.GetMean()
stdy1 = histy1.GetStdDev()

meany2 = histy2.GetMean()
stdy2 = histy2.GetStdDev()

print(f"średnia dla Y1 = {meany1}, odchylenie standardowe (error) = {stdy1}")
print(f"średnia dla Y2 = {meany2}, odchylenie standardowe (error) = {stdy2}")

#macierz kowariancji Y
#deklaracja histogramów Y
hy1vsy2 = R.TH2F("y1vsy2","y1vsy2",200,0,20,200,0,20)
for d1,d2 in zip(y1,y2):
    hy1vsy2.Fill(d1,d2)
    
cov12 = hy1vsy2.GetCovariance()

var1 = stdy1**2
var2 = stdy2**2

Cy = R.TMatrixD(2,2)
Cy[0][0] = var1
Cy[0][1] = cov12
Cy[1][0] = cov12
Cy[1][1] = var2



#korelacja Y1 Y2
#przez histogram wywala zle
corr = hy1vsy2.GetCorrelationFactor() 

#jadąc przez macierz Cym
corr2 = Cym[0][1]/np.sqrt((Cym[0][0]*Cym[1][1]))
print("korelacja y1 vs y2 = ", corr2)
Cx.Print()
Cy.Print()

c1.Update()

input("cokolwiek")