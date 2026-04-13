import ROOT
import numpy as np


wzor_funkcji = "[0]*(-exp(-3*pow(x,2))+exp(-0.5*pow(x,2)))"
fun1_unnorm = ROOT.TF1("fun1_unnorm", wzor_funkcji, 0., 3.)
fun1_unnorm.SetParameter(0, 1.) # domyślna wartość parametru w kontekście roota to 0 dlatego do normalizacji tymczasowo trzeba ustawić wartość parametru na 1
const = 1./fun1_unnorm.Integral(0.,3.)

#funkcja unormowana
fun1 = ROOT.TF1("fununkcja_unormowana", wzor_funkcji, 0., 3.)
fun1.SetParameter(0, const)

#canva
c1 = ROOT.TCanvas("c1", "Funkcje", 800, 600)
c1.Divide(1,2)
#funkcja rysowanie
c1.cd(1)
fun1.SetTitle("Unormowana funkcja gestosci prawdopodobienstwa")
fun1.GetXaxis().SetTitle("x")
fun1.GetYaxis().SetTitle("f(x)")
fun1.Draw()

#dystrybuanta 
def dystrybuanta(x,p):
    return fun1.Integral(0,x[0])

fun_dyst = ROOT.TF1("funkcja_dystrybuanty", dystrybuanta, 0., 3., 0)

c1.cd(2)
fun_dyst.SetTitle("Dystrybuanta")
fun_dyst.GetXaxis().SetTitle("x")
fun_dyst.GetYaxis().SetTitle("Zgromadzone prawdopodobieńśtwo")
fun_dyst.Draw()

#wartości
#wartość modalna
max = fun1.GetMaximumX()
print("Maksimum funkcji/ wartość modalna =", max)

#wartość oczekiwana
mean = fun1.Mean(0,3)
print("Wartość oczekiwana =", mean)

#Kwantyle
kwan1 = fun_dyst.GetX(0.25)
kwan2 = fun_dyst.GetX(0.5)
kwan3 = fun_dyst.GetX(0.75)
print(f"kwantyl 25% = {kwan1}, kwantyl 50% = {kwan2}, kwantyl 75% = {kwan3}")


#wariancja
var = fun1.Variance(0,3)
print("Wariancja =", var)

od_stan = np.sqrt(var)
print("Odchylenie standardowe =", od_stan)








c1.Update()

input("do trzymania okna")
