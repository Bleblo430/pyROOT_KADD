import ROOT as R
import numpy as np
import matplotlib.pyplot as plt



def fun(x,p):
    X = x[0]
    return np.sin(np.cos(X))
f = R.TF1("f", fun, 0, np.pi/2, 0)
#funkcja pomocnicza dobrana analitycznie
def fun_pom(x,p):
    X = x[0]
    return np.cos(X)

f_pom = R.TF1("f_pom", fun_pom, 0, np.pi/2, 0)

val_norm = f.Integral(0,np.pi/2)
print("Wartość całki =", val_norm)

#jakaś dziwna implementacja metody prostokąta tylko zamiast prostokąta jest cosinus
N = 100000 #liczba próbek
hits = 0
for i in range(N):
    x = np.random.uniform(0,np.pi/2)
    y = np.random.uniform(0,f_pom.Eval(x))
    if y < f.Eval(x):
        hits += 1
    val_mc = hits/N * f_pom.Integral(0,np.pi/2)
    rel_error = (val_mc - val_norm)/val_norm
    err = abs(rel_error)
    if err < 0.01:
        print(f"Wartość całki (metoda Monte Carlo) = {val_mc}, błąd względny = {rel_error:.4f}, program zatrzymano po {i+1} próbkach")
        break



















c1 = R.TCanvas("c1", "Funkcja", 800, 600)

f.Draw()
f_pom.Draw("same")
c1.Update()
input("Naciśnij Enter, aby zakończyć...")

