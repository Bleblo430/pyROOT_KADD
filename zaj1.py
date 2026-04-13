import ROOT

#TCanvas 
#ROOT.TCanvas(name, title, width, height)
#name -nazwa obiektu dla użytku roota unikalna w programie

#fnckje
#ROOT.TF1(name, wzór, x_min, x_max)
#name - jak wcześniej
#wzór - wzór funkcji jako string w składni c++

#histogram
#ROOT.TH1F(name, title, liczba przedziałów, xmin, xmax)
#cmin,xmax - zakres wartości
# liczba przedziałów - liczba słupków histogramu zakres podzielony równo na tyle części


c = ROOT.TCanvas("zaj1_wykresy", "Wykresy z zajęć 1", 800, 600)
fun1 = ROOT.TF1("fun1", "sin(x)", 0., 10.)
fun2 = ROOT.TF1("fun2", "cos(x)", 0., 10.)

his1 = ROOT.TH1F("his1", "his1", 6,0.5,6.5)
for i in range(2):
    his1.Fill(1)
    
his1.Fill(2) #fill dodaje konkretną wartość dlo histogramu, zostaje ona automatycznie przypisana do słupka w zakresie

for i in range(5):
    his1.Fill(3)

for i in range(4):
    his1.Fill(4)

for i in range(10):
    his1.Fill(5)

for i in range(12):
    his1.Fill(6)

c.Divide(2,2)

c.cd(1)
fun1.Draw()

c.cd(2)
fun2.Draw()

c.cd(3)
fun1.Draw()
fun2.Draw("SAME") #rysuje na tym samym wykresie
fun2.SetLineColor(ROOT.kBlue) #ustawia kolor lini rysowanej DLA FUNKCJI nie dla canvy 

c.cd(4)
his1.Draw("HIST")


c.Update()
input("Ponieważ pyROOT zamyka okna po wykonaniu programu trzeba urzymywać coś żeby program nie zamknął wykresó po ułamkach sekund stąd ten input jest całkiem dobrym rozwiązaniem. po kliknięciu enter okna się zamkną")



