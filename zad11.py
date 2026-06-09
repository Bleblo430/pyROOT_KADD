import ROOT as R
import numpy as np
import array

X = [-0.9, -0.7, -0.5, -0.3, -0.1, 0.1, 0.3, 0.5, 0.7, 0.9]
Y = [86, 50, 26, 24,20, 55, 113, 186, 339, 601]
Uy = [10, 14, 13, 9, 13, 12, 12, 13, 11, 14]
N = 5

def MNK(X,Y,Uy,N):
    if len(X) != len(Y):
        print("serie X i Y mają różnę długości ")
        return None
    else:
        A = R.TMatrixD(len(X), N+1)
        for i in range(len(X)):#iteracja po punktach
            for j in range(N+1):#iteracja po potęgach 
                A[i][j] = X[i]**j
        
        
        W =R.TMatrixD(len(X),len(X))
        for i in range(len(X)):
                w = 1/Uy[i]**2 #waga punktu z niepewności
                W[i][i] = w
        
        AT = R.TMatrixD(R.TMatrixD.kTransposed, A) #a transponowana

        WA = R.TMatrixD(W.GetNrows(), A.GetNcols()) 
        WA.Mult(W, A)   

        left = R.TMatrixD(AT.GetNrows(), WA.GetNcols())
        left.Mult(AT, WA)

        

        y = R.TMatrixD(len(Y), 1)

        for i in range(len(Y)):
            y[i][0] = Y[i]
        
        WY = R.TMatrixD(W.GetNrows(), y.GetNcols())
        WY.Mult(W, y)

        right = R.TMatrixD(AT.GetNrows(), WY.GetNcols())
        right.Mult(AT,WY)

        left_inv = R.TMatrixD(left)
        left_inv.Invert()
        a = R.TMatrixD(left_inv.GetNrows(), right.GetNcols())
        a.Mult(left_inv, right)
        
        coefs = []
        for i in range(a.GetNrows()):
            coefs.append(a[i][0])

        errors = []

        for i in range(left_inv.GetNrows()):
            errors.append(left_inv[i][i]**0.5)
        #lista współczynników gdzie coefs[n] odpowiada współczynnikowi przy n potędze wielomianu 

        eta = R.TMatrixD(A.GetNrows(), a.GetNcols())
        eta.Mult(A, a)

        eta_list = []
        for i in range(eta.GetNrows()):
            eta_list.append(eta[i][0])


        return coefs,errors,eta_list
    
coefs0,err0,_= MNK(X,Y,Uy,0)
coefs1,err1,_ = MNK(X,Y,Uy,1)
coefs2,err2,_ = MNK(X,Y,Uy,2)
coefs3,err3,_ = MNK(X,Y,Uy,3)
coefs4,err4,_ = MNK(X,Y,Uy,4)
coefs5,err5,_ = MNK(X,Y,Uy,5)
coefs6,err6,_ = MNK(X,Y,Uy,6)

poly0 = np.polynomial.Polynomial(coefs0)
poly1 = np.polynomial.Polynomial(coefs1)
poly2 = np.polynomial.Polynomial(coefs2)
poly3 = np.polynomial.Polynomial(coefs3)
poly4 = np.polynomial.Polynomial(coefs4)
poly5 = np.polynomial.Polynomial(coefs5)
poly6 = np.polynomial.Polynomial(coefs6)

def fun0(x,p):
    return poly0(x[0])
def fun1(x,p):
    return poly1(x[0])
def fun2(x,p):
    return poly2(x[0])
def fun3(x,p):
    return poly3(x[0])
def fun4(x,p):
    return poly4(x[0])
def fun5(x,p):
    return poly5(x[0])
def fun6(x,p):
    return poly6(x[0])
f0 = R.TF1("f0", fun0, min(X), max(X))
f1 = R.TF1("f1", fun1, min(X), max(X))
f2 = R.TF1("f2", fun2, min(X), max(X))
f3 = R.TF1("f3", fun3, min(X), max(X))
f4 = R.TF1("f4", fun4, min(X), max(X))
f5 = R.TF1("f5", fun5, min(X), max(X))
f6 = R.TF1("f6", fun6, min(X), max(X))


c1 = R.TCanvas()
n = len(X)
x = array.array("d", X)
y = array.array("d", Y)
ex = array.array("d", [0.0] * n)
ey = array.array("d", Uy)

g = R.TGraphErrors(n, x, y, ex, ey)
g.SetTitle(f"Dopasowany ręcznie wielomian zadanego stopnia")
g.Draw("AP")
f0.SetLineColor(R.kRed)
f1.SetLineColor(R.kBlue)
f2.SetLineColor(R.kGreen)
f3.SetLineColor(R.kMagenta)
f4.SetLineColor(R.kCyan)
f5.SetLineColor(R.kOrange)
f6.SetLineColor(R.kBlack)

f0.Draw("same")
f1.Draw("same")
f2.Draw("same")
f3.Draw("same")
f4.Draw("same")
f5.Draw("same")
f6.Draw("same")

legend = R.TLegend(0.65, 0.55, 0.9, 0.9)

legend.AddEntry(f0, "N=0", "l")
legend.AddEntry(f1, "N=1", "l")
legend.AddEntry(f2, "N=2", "l")
legend.AddEntry(f3, "N=3", "l")
legend.AddEntry(f4, "N=4", "l")
legend.AddEntry(f5, "N=5", "l")
legend.AddEntry(f6, "N=6", "l")
legend.Draw()


#automatyczne dobieranie wielomianu
def autoMNK(X,Y,Uy):
    running = True
    i = 0 
    Y_arr = np.array(Y)
    Uy_arr = np.array(Uy)
    while running:
        

        


        coefs, err, eta = MNK(X,Y,Uy,i)

        eta_arr = np.array(eta)

        chi2 = np.sum(((Y_arr - eta_arr) / Uy_arr)**2)
        ndf = len(X) - len(coefs)

        chi2_ndf = chi2 / ndf
        print(chi2_ndf)
        i +=1
        if chi2_ndf <0.01:
            running = False
    return coefs, i-1, chi2_ndf


coefs_auto, NN, chi2_ndf = autoMNK(X,Y,Uy)
poly_auto = np.polynomial.Polynomial(coefs_auto)
def fun_auto(x,p):
    return poly_auto(x[0])

f_auto = R.TF1("fauto", fun_auto, min(X), max(X))

c2 = R.TCanvas()
c2.cd()
n = len(X)
x = array.array("d", X)
y = array.array("d", Y)
ex = array.array("d", [0.0] * n)
ey = array.array("d", Uy)

g2 = R.TGraphErrors(n, x, y, ex, ey)
g2.SetTitle(f"Dopasowany automatycznie wielomian stopnia N = {NN} z chi2/ndf = {chi2_ndf}")
g2.Draw("AP")
f_auto.Draw("same")





c1.Update()
c2.Update()
input()










