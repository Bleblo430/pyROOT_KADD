import ROOT as R
import numpy as np

def fun(x,p):
    X = x[0]
    Y = x[1]
    C = p[0]
    if (0<X<np.pi and 0<Y<np.pi and 0<X*Y<np.pi):
        return C*np.sin(X*Y)
    else:
        return 0
    
fun1_unnorm = R.TF2("fun1_unnorm", fun, 0., np.pi, 0., np.pi, 1)
fun1_unnorm.SetParameter(0, 1)

const = 1/fun1_unnorm.Integral(0.,np.pi,0.,np.pi)

fun1 = R.TF2("fun1", fun, 0., np.pi, 0., np.pi, 1)
fun1.SetParameter(0, const)

c1 = R.TCanvas("c1", "Funkcja", 800, 600)
c1.Divide(1,2)
c1.cd(1)
fun1.SetTitle("Unormowana funkcja gestosci prawdopodobienstwa")
fun1.GetXaxis().SetTitle("x")
fun1.GetYaxis().SetTitle("y")
fun1.Draw("SURF") #dobre do rysowania funkcji TF2


def dystrybuanta(x,p):
    return fun1.Integral(0,x[0],0,x[1])

fun_dyst = R.TF2("fun_dyst", dystrybuanta, 0., np.pi, 0., np.pi, 0)

g1 = R.TGraph2D()
i=0
for x in np.linspace(0, np.pi, 100):
    for y in np.linspace(0,np.pi,100):
        z = fun_dyst.Eval(x,y)
        
        g1.SetPoint(i,x,y,z)
        i+=1
        
c1.cd(2)
g1.Draw("SURF")

c2 = R.TCanvas("c2", "Wartości Brzegowe", 800, 600)
c2.Divide(1,2)
c2.cd(1)

g2 = R.TGraph()
g3 = R.TGraph()


i = 0
idx = np.linspace(0, np.pi, 100)
for i in range(len(idx)):
    x = idx[i]
    dx = np.pi/100
    y = fun1.Integral(x,x+dx,0,np.pi)/dx
    g2.SetPoint(i,x,y)        
    i+=1

g2.Draw("AL")        
        
i = 0
idx = np.linspace(0, np.pi, 100)
for i in range(len(idx)):
    x = idx[i]
    dx = np.pi/100
    y = fun1.Integral(0,np.pi,x, x+dx)/dx
    g3.SetPoint(i,x,y)        
    i+=1

c2.cd(2)
g3.Draw("AL")


        
    

c1.Update()
c2.Update()
input("wfew")


        
