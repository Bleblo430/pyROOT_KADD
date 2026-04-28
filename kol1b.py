import ROOT as R
import numpy as np
import ctypes as ct


def fun(x,p):
    X = x[0]
    Y = x[1]
    C = p[0]
    return C * np.exp((-1/8)*(X**2) - (1/50)*(Y**2))

fun_unn = R.TF2("fun_unn", fun, 0, 1, 0, 1, 1)
fun_unn.SetParameter(0,1)
#normalizacja funkcji
const = 1/fun_unn.Integral(0,1,0,1)

f = R.TF2("f", fun, 0, 1, 0, 1, 1)
f.SetParameter(0, const)

X = []
Y = []
x = ct.c_double(0.0)  
y = ct.c_double(0.0)
for i in range(1000):
    f.GetRandom2(x,y)
    X.append(x.value)
    Y.append(y.value)

X = np.array(X)
Y = np.array(Y)


hx = R.TH1F("hx","hx",200,0,1)
hy = R.TH1F("hy","hy",200,0,1)

for entry in X:
    hx.Fill(entry)
for entry in Y:
    hy.Fill(entry)

hxvsy = R.TH2F("hxvsy","hxvsy",200,0,1,200,0,1)

for d1,d2 in zip(X,Y):
    hxvsy.Fill(d1,d2)

U = 2*X + 4*Y
V = 5*X - 7*Y
W = -9*X + 10*Y

hu = R.TH1F("hu","hu",200,-20,20)
hv = R.TH1F("hv","hv",200,-20,20)
hw = R.TH1F("hw","hw",200,-20,20)

for entry in U:
    hu.Fill(entry)
for entry in V:
    hv.Fill(entry)
for entry in W:
    hw.Fill(entry)


#macierz kowariancji X Y
stdx = hx.GetStdDev()
stdy = hy.GetStdDev()

cov = hxvsy.GetCovariance()

C = R.TMatrixD(2,2)
C[0][0] = stdx**2
C[0][1] = cov
C[1][0] = cov
C[1][1] = stdy**2

#macierz transformacji
T = R.TMatrixD(3,2)
T[0][0] = 2
T[0][1] = 4
T[1][0] = 5
T[1][1] = -7
T[2][0] = -9
T[2][1] = 10

#macierz kowariancji U V W
Tt = R.TMatrixD(2,3)
Tt.Transpose(T)
step1 = R.TMatrixD(3,2)
step1.Mult(T,C)
cym = R.TMatrixD(3,3)

#macierz kowariancji U V W to cym z równania C' = T * C * T^T
cym.Mult(step1,Tt)


#odchylenie standardowe U V W
stdu = hu.GetStdDev()
stdv = hv.GetStdDev()
stdw = hw.GetStdDev()


#macierz kowariancji XY
C.Print()
#macierz transformacji
T.Print()
#macierz kowariancji UVW
cym.Print()
#odchylenia standardowe U V W
print(f"odchylenie standardowe U = {stdu}, V = {stdv}, W = {stdw}")

input("Naciśnij Enter, aby zakończyć...")


    

