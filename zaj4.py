import ROOT as R
import numpy as np
import ctypes as ct

def fun(x,p):
    X = x[0]
    Y = x[1]
    C = p[0]
    if (0<X<3) and (0<Y<4):
        return C*((-(0.5*X-1)**2)*((0.25*Y-1.5)**2)+3)
    else :
        return 0
    
f_unn = R.TF2("f_unn", fun, 0, 3, 0, 4, 1) # pamiętaj o ostatnim argumencie - liczbie parametrów
f_unn.SetParameter(0,1)

const = 1/f_unn.Integral(0,3,0,4)

f = R.TF2("f_unn", fun, 0, 3, 0, 4, 1)
f.SetParameter(0,const)

hist = R.TH2F("hist", "Losowanie z rozkladu 2D:",50, 0,3,50,0,4) # te wartości przed przedziałami to liczba binów w zakresie 



x = ct.c_double(0.0) #root działa na C/C++ i nie konwertuje liczb pythonowych na swoje wieć bezpiecznie używać Ctypes
y = ct.c_double(0.0) 

for i in range(1000000):
    f.GetRandom2(x,y)
    hist.Fill(x.value, y.value) #obiekty ctype to obiekty zwracające liczbe w pudełku a nie liczbe więc czeba sobie ją wyciągnąć
     
hist.Scale(1.0/hist.Integral("width"))

c1 = R.TCanvas()
c1.Divide(2)
c1.cd(1)
hist.Draw("SURF")


#dystrybuante należy zrobić recznie bo dla histogramu2D brakuje funkcji
#musimy zrobić sumę prawdopodobieństw od każdego punktu x,y zgromadzonego w binach
#po prawo i w dół od niego
dhist = hist.Clone("dystrybuanta_histogramu") #tworzymy kopie histogramu żeby w nim zapisywać dystrybuantee a nie nadpisywać orginał
dhist.SetTitle("Dystrybuanta empirycznego histogramu 2D")
nx = hist.GetNbinsX()
ny = hist.GetNbinsY()
for i in range(1,nx+1): #ROOT numeruje biny od 1 do n włącznie 
    for j in range(1,ny+1):
        s = 0 #suma prawdopdodobieństwa w binach po prawo i w dół
        for k in range(1,i+1): #od pierwszego bina do tego w którym się aktualnie znajdujemy
            for l in range(1,j+1):
                s += hist.GetBinContent(k,l)
        dhist.SetBinContent(i,j,s)

#normalizacja dystrybuanty
tot = hist.Integral()
dhist.Scale(1.0/tot)

c1.cd(2)
dhist.Draw("SURF")

#rozkłady brzegowe
hx = hist.ProjectionX()
hy = hist.ProjectionY()
#normalizacja, width uwzględnia szerokość binu, bez width było by poprawnie TYLKO jeśli bun ma szerokość 1
hx.Scale(1.0/hx.Integral(), "width")
hy.Scale(1.0/hy.Integral(), "width")

c2 = R.TCanvas()
c2.Divide(2)

c2.cd(1)
hx.Draw()
c2.cd(2)
hy.Draw()

#korelacja kowariancje średnie i odchylenia oraz errory

N = hist.GetEntries()

mean_x = hist.GetMean(1)
std_x = hist.GetStdDev(1)

err_std_x = hist.GetStdDevError(1)



err_mean_x = hist.GetMeanError(1) #tak też można
err_mean_x = std_x/np.sqrt(N)

mean_y = hist.GetMean(2)
std_y = hist.GetStdDev(2)

err_std_y = hist.GetStdDevError(2)

err_mean_y = hist.GetMeanError(2)
err_mean_y = std_y/np.sqrt(N)

print(f"wartość oczekiwana po osi x: {mean_x} +- {err_mean_x}")
print(f"odchylenie standardowe po osi x: {std_x} +- {err_std_x}")
print(f"wartość oczekiwana po osi y: {mean_y} +- {err_mean_y}")
print(f"odchylenie standardowe po osi y: {std_y} +- {err_std_y}")

cov = hist.GetCovariance()
corr = hist.GetCorrelationFactor()

print(f"kowariancja: {cov}")
print(f"korelacja: {corr}")


c1.Update()
c2.Update()
input("cokolwiek")