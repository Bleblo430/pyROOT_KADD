import ROOT as R
import numpy as np
import matplotlib.pyplot as plt

def fun(x,p):
    X = x[0]
    return np.exp(-(3*X + 1/(X*X))) * (np.sin(X*X))**2

# def fun(x,p):
#     X = x[0]
#     return np.exp(-X)

f = R.TF1("f", fun, 1, 3)

val_normal = f.Integral(1,3)

#losowanie punktów w prostokącie od a do b na osi x i od 0 do max(f) na osi y
a = 1
b = 3

max_f = f.GetMaximum(a,b)
relative_error = []
N = [10,25,50,75,100,150,200,250,300,400,500,750,1000,2000,3000,4000,5000,6000,7000,8000,9000,10000]

for n in N:
    num = 0
    #losowanie punktów w prostokącie od a do b na osi x i od 0 do max(f) na osi y
    a = 1
    b = 3
    for i in range(n):
        x = np.random.uniform(a,b)
        y = np.random.uniform(0,max_f)
        
        if y < f.Eval(x):
            num += 1
    val_classic_von_neumann = (b-a)*max_f*num/n
    err = (val_normal - val_classic_von_neumann)/val_normal
    relative_error.append(np.abs(err)) 
    
               
#losowanie z funkcją pomocniczą
ymax1 = f.GetMaximum(1,3)
xmax1 = f.GetMaximumX(1,3)


xmax2 = 3
ymax2 = f.Eval(xmax2)


a = ((ymax2 - ymax1)/(xmax2 - xmax1))
b = (ymax1 - ((ymax2 - ymax1)/(xmax2 - xmax1))*xmax1)

def funkcja_pomocnicza(x,p):
    X = x[0]
    return a*X + b+0.001

fun_pom = R.TF1("fun_pom", funkcja_pomocnicza, 1, 3)


def dystrybuanta_funkcji_pomocniczej(x,p):
    X = x[0]
    return 0.5*a*X**2 + b*X

dyst_fun_pom = R.TF1("dyst_fun_pom", dystrybuanta_funkcji_pomocniczej, 1, 3)

Smin = dyst_fun_pom.Eval(1)
Smax = dyst_fun_pom.Eval(3)


def dyst_inverse(x,p):
    Y = x[0]
    return dyst_fun_pom.GetX(Y,1,3)

dyst_inv = R.TF1("dyst_inv", dyst_inverse, Smin, Smax)

hit = R.TH1F("hit", "cos", 100, 0, 4)

k = 1000000
num = 0
for i in range(k):
    u1 = np.random.uniform(Smin,Smax)
    xi = dyst_inv.Eval(u1)
    hit.Fill(xi)
    u2 = np.random.uniform(0,1)
    if u2 < f.Eval(xi)/fun_pom.Eval(xi):
        num += 1
val_dyst_von_neumann = fun_pom.Integral(1,3)*num/k









print(f"Wartość całki metodą integral: {val_normal}")
print(f"Wartość całki metodą klasycznego von Neumanna: {val_classic_von_neumann}")
print(f"Wartość całki metodą z funkcją pomocniczą von Neumanna: {val_dyst_von_neumann}")

c1 = R.TCanvas("c", "Wykres funkcji", 800, 600)
f.SetTitle("Wykres funkcji")
f.GetXaxis().SetTitle("x")
f.GetYaxis().SetTitle("f(x)")
f.Draw()
fun_pom.SetLineColor(R.kBlue)
fun_pom.Draw("same")

c2  = R.TCanvas("c2", "test", 800, 600)
hit.Draw()


print("Błąd względny: ", relative_error)
plt.scatter(N, relative_error)
plt.title("Błąd względny w zależności od liczby punktów")
plt.xlabel("Liczba punktów")
plt.ylabel("Błąd względny")
plt.show()


c1.Update()
c2.Update()
input("cokolwiek")
