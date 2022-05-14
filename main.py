import numpy as np
import matplotlib.pyplot as plt

plt.style.use('seaborn')
plt.rcParams["figure.figsize"] = (14,7)

d = 0.001 #dijametar kapi
r = d/2  #poluprecnik kapi
zap = (4*np.pi/3)*r**3 #zapremina kapi
rov = 1000 #gustina vode
m = rov*zap #masa kapi

ni = 1.82e-5 #viskoznost vazduha Nsm/m**2
kv = 6*np.pi*r*ni #koeficijent otpora

g = 9.81

vt = m*g/kv #terminalna brzina
V0 = [0, -vt, -2*vt, vt] #pocetna brzina #v0 < 0 u pravcu zemlje ispaljeno, v0 > 0 u pravcu neba ispaljeno, v0 = 0 slobodan pad(po zadatku bas)

dt = 1e-3 #vremenski korak

y0 = 750 #visina sa koje pada kap

for i, v0 in enumerate(V0):
    #bez otpora - dok se ne postigne brzina malo veca od terminalne
    vyb = [v0]; yb = [y0]
    tb = [0]
    #O.K. metodom racunamo brzinu i polozaj dok ne postane malo veca od terminalne
    while -vyb[-1] < 1.1*vt:
        ayb = -g

        vyb.append(vyb[-1] + ayb*dt)
        yb.append(yb[-1] + vyb[-1]*dt)

        tb.append(tb[-1] + dt)



    #sa otporom - do dodira kapi kise sa Zemljom
    ayo = [-g - kv/m*v0]; vyo = [v0]
    yo = [y0]; to = [0]
    tvt = 0; vvt = vyo[-1]; nadjen = False
    #O.K. metodom racunamo brzinu i polozaj kada imamo silu otpora
    while yo[-1] > 0:
        ayo.append(-g - kv/m*vyo[-1])

        vyo.append(vyo[-1] + ayo[-1]*dt)
        yo.append(yo[-1] + vyo[-1]*dt)

        to.append(to[-1] + dt)

        # trenutak kada je v(t) za 0.1% manje od vt
        if nadjen == False and np.abs(-vyo[-1]-vt)/vt < 0.001: #racunamo relativnu gresku
            nadjen = True
            tvt = to[-1]; vvt = vyo[-1]


    tt = np.linspace(0, to[-1], 50)
    vt_niz = -vt*np.ones_like(tt)

    #plotovanje brzina
    plt.subplot(1, 3, 1)
    plt.xlabel('Vreme [s]')
    plt.ylabel('Brzina [m/s]')

    naslov = 'Brzina u funkciji vremena, v0 = ' + str(round(v0, 2))
    plt.title(naslov)

    if v0 == 0:
        plt.plot(tb, vyb, '--r', linewidth = 1.5, label = 'v bez otpora')

    plt.plot(to, vyo, 'b', label = 'v sa otporom')
    plt.scatter(tt, vt_niz, 5 * np.ones_like(tt), color = 'black', label = 'v terminalno')
    if nadjen == True:
        plt.plot(tvt, vvt, 'o', color = 'purple', label = '0.1% vt')
    plt.legend()

    #plotovanje ubrzanja
    plt.subplot(1, 3, 2)
    plt.xlabel('Vreme [s]')
    plt.ylabel('Ubrzanje [m/s**2]')

    naslov = 'Ubrzanje u funkciji vremena, v0 = ' + str(round(v0, 2))
    plt.title(naslov)

    plt.plot(to, -g*np.ones_like(to), '--r', linewidth = 1.5, label = 'a bez otpora')
    plt.plot(to, ayo, 'b', label = 'a sa otporom')
    plt.legend()

    #plotovanje polozaja tela u ekvidistantnim trenucima vremena
    plt.subplot(1, 3, 3)
    plt.ylabel('Visina [m]')

    naslov = 'Polozaj kapi u ekvidistantnim trenucima, v0 =' + str(round(v0, 2))
    plt.title(naslov)

    #uzimamo svaki hiljaditi polazaj kako bismo lakse videli na grafiku
    tmp = list(np.zeros_like(yo)) 
    plt.scatter(tmp[::1000], yo[::1000], 5*np.ones_like(yo[::1000]) , color = 'black', label='sa otporom')

    plt.show()