import math
import struct
import matplotlib.pyplot as plt

#koordinate tacaka za testiranje programa
#Nis
#s1: 43.3211424
#i1: 21.89567149
#Kopaonik
#s2: 43.2683875545226  
#i2: 20.826308767077144


# funkcija za pronalazenje odgovarajuceg .hgt fajla na osnovu koordinati kao i za citanje nadmorske visinu tacke
def procitajVisinu(n, e):
    fajl = "N" + str(math.trunc(n)) + "E0" + str(math.trunc(e)) + ".hgt"
    i = n - math.trunc(n)
    j = e - math.trunc(e)
    vrsta = round(i * 1200)
    kolona = round(j * 1200)
    pozicija = (1201 * (1201 - vrsta - 1) + kolona) * 2
    f=open(fajl, "rb")
    f.seek(pozicija)
    buf = f.read(2)
    val = struct.unpack('>h', buf)
    if not val == -32768: #nevalidna vrednost 
       return val
    else:
       return None
#--------------------------------------------------------------------------------------------------------------------------------

#  funkcija za nalazenje distance izmedju dve tacka 
def haversine(gsirina1, gduzina1, gsirina2, gduzina2):
    gsirina1_rad = math.radians(gsirina1)
    gsirina2_rad = math.radians(gsirina2)
    gduzina1_rad = math.radians(gduzina1)
    gduzina2_rad = math.radians(gduzina2)
    delta_lat = gsirina2_rad - gsirina1_rad
    delta_lon = gduzina2_rad - gduzina1_rad
    a = math.sqrt((math.sin(delta_lat / 2)) ** 2 + math.cos(gsirina1_rad) * math.cos(gsirina2_rad) * (math.sin(delta_lon / 2)) ** 2) 
    #haverenise formula za rucunanje udaljenosti izmedju 2 tacke  na lopti 
    d = 2 * 6371000 * math.asin(a) #6371000 - poluprecnik zemlje
    return d
#--------------------------------------------------------------------------------------------------------------------------------




if __name__ == "__main__":

    # prva tacka
    severna1 = float(input("Unesite koordinate severne geografsku sirine prve tacke: "))
    istocna1 = float(input("Unesite koordinate istocne geografske duzine prve tacke: "))
    # druga tacka
    severna2 = float(input("Unesite koordinate severne geografske sirine druge tacke: "))
    istocna2 = float(input("Unesite koordinate istocne geografske duzine druge tacke: "))

    T1 = [severna1, istocna1]
    T2 = [severna2, istocna2]

    # najkraca udaljenost izmedju T1 i T2
    distanca = haversine(severna1, istocna1, severna2, istocna2)

    p = 200 # broj podeoka na grafiku ()

    intervalSirine = (T2[0] - T1[0]) / p  # interval za dobijanje geografske sirine tacaka izmedju T2 i T1
    intervalDuzine = (T2[1] - T1[1]) / p  # interval za dobijanje geografske duzine tacaka izmedju T2 i T1


    pocetnaSirina = T1[0]
    pocetnaDuzina = T1[1]

    listaGeoSirina = [pocetnaSirina]
    listaGeoDuzina = [pocetnaDuzina]

  #dobijanje tacka odgovarajuce geografske sirine i geografske duzine u odnosu na intervale

    for i in range(p):
        lat_step = pocetnaSirina + intervalSirine
        lon_step = pocetnaDuzina + intervalDuzine
        pocetnaDuzina = lon_step
        pocetnaSirina = lat_step
        listaGeoSirina.append(lat_step)
        listaGeoDuzina.append(lon_step)

    listaDuzina = []
    for j in range(len(listaGeoSirina)):
        lat_p = listaGeoSirina[j]
        lon_p = listaGeoDuzina[j]
        dp = haversine(pocetnaSirina, pocetnaDuzina, lat_p, lon_p) / 1000  # /1000 da bi bilo u km
        round(dp)
        listaDuzina.append(dp)

    listaDuzina.reverse()

    # citanje nadmorskih visina tacaka izmedju T1 i T2
    listaVisina = []
    for j in range(len(listaGeoSirina)):
        listaVisina.append(procitajVisinu(listaGeoSirina[j], listaGeoDuzina[j]))

   # listaVisina.reverse()

    x = listaDuzina  # udaljenost izmedju dve tacke crtamo na x osi
    y = listaVisina  # nadmorske visine tacaka crtamo na y osi

    

    plt.plot(x[0],y[0])
    #sluzi da predstavimo prvu tacku(u nasem slucaju Nis) cija nadmorska visina se nalazi na poziciji y[0] u listiVisina

    plt.plot(x[len(x)-1], y[len(y)-1])
    #sluzi da prikazemo krajnju lokaciju(tacka 2) koja od prve tacke ima udaljenost x(len(x)-1) km a njena nadmorska visina je posledjni element u y listi (y[len(y)-1]) metara

    plt.plot(x, y,"red")
    # iscrtavamo nadmorske visine tacaka koje se nalaze izmedju tacaka T1 i T2

    minimum = min(listaVisina)
    for i in range(len(listaGeoSirina)):
        plt.fill_between( x[i], minimum, y[i], color="pink", alpha=0.2, lw=3)
        

    plt.title("Profil terena", loc="center")
    plt.legend([T2, T1]) #u legendi stoje koordinate zadatih tacaka
    plt.xlabel("Udaljenost: " + str(round(distanca / 1000)) + "km (" + str(round(distanca)) + "m)")
    plt.ylabel("Nadmorksa visina (m)")

    plt.show()
