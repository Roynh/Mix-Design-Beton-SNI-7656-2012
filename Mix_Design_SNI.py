#SNI 7657-2012

#--INPUT DATA--#
# Mutu Rencana Masukkan 15-40 Mpa
mutu_rcn = 20

#Nilai Slump Masukkan "25-50","75-100","150-175",">175" 
slump_rcn = "75-100"

#(mm) Nilai Diameter Maksimum Agregat Kasar 
# Pilih 9.5, 12.5, 19, 25, 37.5, 50, 75, 150
dim_agr_maks = 37.5 

#(kg/m^3) Berat Kering Oven Agregat Kasar
berat_kering_oven = 983.5

#Berat Jenis Semen
bj_semen = 3.248

#Beton dgn Udara / Tanpa udara
#Masukkan True Jika beton dengan tambahan udara
#Masukkan False Jika beton tanpa tambahan udara
bool_udara = False


mods_agr_halus = 2.996 #Modulus Agregat Halus
ssd_halus = 1.81 #Berat Jenis (SSD) Agregat Halus
ssd_kasar = 2.564 #Berat Jenis (SSD) Agregat Kasar
abs_air_halus = 15.61 #(%) Penyerapan Air Agregat Halus
abs_agr_kasar = 0,6 #(%) Penyerapan Air Agregat Kasar

# Ubah jika beton dengan tambahan udara
#0 = Ringan
#1 = Sedang
#2 = Berat
jenis_beton = 0 
#--INPUT DATA--#


#MENCARI AIR PENCAMPUR
def airPencampur(slump, dim_agr) :
    slumps =  {"25-50":0,
            "75-100":1,
            "150-175":2,
            ">175":3}
    dim_agrs = [9.5,12.5,19,25,37.5,50,75,150]
    air_pencampur_tanpa_udara = [[207,199,190,179,166,154,130,113],
                             [228,216,205,193,181,169,145,124],
                             [243,228,216,202,190,178,160,0],
                             [0,0,0,0,0,0,0,0]]#kg/m^3
    air_pencampur_dengan_udara = [[181,175,268,160,150,142,122,107],
                              [202,193,184,165,165,157,133,119],
                              [216,205,197,174,174,166,154,0],
                              [0,0,0,0,0,0,0,0]]
    slump_key = slumps.get(str(slump))
    dim_agr_key = dim_agrs.index(dim_agr)
    airPencampurVal = 0
    if bool_udara == True :
        airPencampurVal = air_pencampur_dengan_udara[slump_key][dim_agr_key]
    elif bool_udara == False :
        airPencampurVal = air_pencampur_tanpa_udara[slump_key][dim_agr_key]
    
    return airPencampurVal

#MENCARI FAKTOR AIR SEMEN / RATION AIR SEMEN
def faktorFAS(mutu) : #semen portland 1
    kekuatan_beton = [40,35,30,25,20,15]
    FAS_nonUdara = [0.42,0.47,0.54,0.61,0.69,0.79]
    FAS_Udara = [0,0.39,0.45,0.52,0.60,0.70]
    mutuVal = 0
    if bool_udara == False :
        if mutu in kekuatan_beton :
            mutuIndex = kekuatan_beton.index(mutu)
            mutuVal = FAS_nonUdara[mutuIndex]
        else : 
            mutuVal = interpolasi_nonUdara(mutu)
    elif bool_udara == True :
        if mutu in kekuatan_beton :
            mutuIndex = kekuatan_beton.index(mutu)
            mutuVal = FAS_Udara[mutuIndex]
        else : 
            mutuVal = interpolasi_udara(mutu)
    
    return mutuVal

def interpolasi_nonUdara(mutu) :
    kekuatan_beton = [40,35,30,25,20,15]
    FAS_nonUdara = [0.42,0.47,0.54,0.61,0.69,0.79]
    angka_kecil = max(filter(lambda x: x < mutu, kekuatan_beton), default=None)
    angka_besar = min(filter(lambda x: x > mutu, kekuatan_beton), default=None)
    FAS_besar = FAS_nonUdara[kekuatan_beton.index(angka_besar)]
    FAS_kecil = FAS_nonUdara[kekuatan_beton.index(angka_kecil)]
    hasil_interpolasi = FAS_kecil + ((mutu-angka_kecil)/(angka_besar-angka_kecil)) * (FAS_besar-FAS_kecil)
    #print(angka_kecil)
    #print(FAS_kecil)
    #print(angka_besar)
    return hasil_interpolasi

def interpolasi_udara(mutu) :
    kekuatan_beton = [40,35,30,25,20,15]
    FAS_Udara = [0,0.39,0.45,0.52,0.60,0.70]
    angka_kecil = max(filter(lambda x: x < mutu, kekuatan_beton), default=None)
    angka_besar = min(filter(lambda x: x > mutu, kekuatan_beton), default=None)
    FAS_besar = FAS_Udara[kekuatan_beton.index(angka_besar)]
    FAS_kecil = FAS_Udara[kekuatan_beton.index(angka_kecil)]
    hasil_interpolasi = FAS_kecil + ((mutu-angka_kecil)/(angka_besar-angka_kecil)) * (FAS_besar-FAS_kecil)
    #print(angka_kecil)
    #print(FAS_kecil)
    #print(angka_besar)
    return hasil_interpolasi

#Mencari Volume Agregat Kasar
def volume_agrKasar(dim_agr, mods_halus, bk_oven) :
    dim_agrs = [9.5,12.5,19,25,37.5,50,75,150]
    mods_keys = [2.4,2.6,2.8,3]
    vol_agrs = [[0.5,0.59,0.66,0.71,0.75,0.78,0.82,0.87],
                [0.48,0.57,0.64,0.69,0.73,0.76,0.8,0.85],
                [0.46,0.66,0.62,0.67,0.71,0.74,0.78,0.83],
                [0.44,0.53,0.60,0.65,0.69,0.72,0.76,0.81]]
    actual_vol = 0
    if mods_halus in mods_keys :
        dim_key = dim_agrs.index(dim_agr)
        mods_key = mods_keys.index(mods_halus)
        vol_ratio = vol_agrs[mods_key][dim_key]
        actual_vol = bk_oven * vol_ratio
    else :
        dim_index = dim_agrs.index(dim_agr)
        vol_ratio = interpolasi_agr(dim_index, mods_halus)
        actual_vol = bk_oven * vol_ratio
    return actual_vol

def interpolasi_agr(dim_index, agr) :
    mods_keys = [2.4,2.6,2.8,3]
    vol_agrs = [[0.5,0.59,0.66,0.71,0.75,0.78,0.82,0.87],
                [0.48,0.57,0.64,0.69,0.73,0.76,0.8,0.85],
                [0.46,0.66,0.62,0.67,0.71,0.74,0.78,0.83],
                [0.44,0.53,0.60,0.65,0.69,0.72,0.76,0.81]]
    mods_kecil = max(filter(lambda x: x < agr, mods_keys), default=None)
    mods_besar = min(filter(lambda x: x > agr, mods_keys), default=None)
    vol_now_kecil = vol_agrs[mods_keys.index(mods_kecil)]
    vol_now_besar = vol_agrs[mods_keys.index(mods_besar)]
    vol_kecil = vol_now_kecil[dim_index]
    vol_besar = vol_now_besar[dim_index]
    hasil_interpolasi = vol_kecil + ((agr-mods_kecil)/(mods_besar-mods_kecil)) * (vol_besar-vol_kecil)
    #print(mods_kecil)
    #print(mods_besar)
    #print(vol_kecil)
    #print(vol_besar)
    #print(agr)
    #print(hasil_interpolasi)
    return hasil_interpolasi

#Perkiraan Awal Berat Beton
def perk_awalBBeton(dim_agr) :
    dim_agrs = [9.5,12.5,19,25,37.5,50,75,150]
    berat_nonUdara = [2280,2310,2345,2380,2410,2445,2490,2530]
    berat_dgnudara = [2200,2230,2275,2290,2350,2345,2405,2435]
    dim_agr_key = dim_agrs.index(dim_agr)
    perk_value = 0
    if bool_udara == False :
        perk_value = berat_nonUdara[dim_agr_key]
    elif bool_udara == True :
        perk_value = berat_dgnudara[dim_agr_key]
    
    return perk_value

#PERKIRAAN AGREGAT HALUS
def perk_agrHalus(air,semen,beratbeton,beratAgrOven) :
    agrHalusVal = beratbeton -  (air + semen + beratAgrOven)
    return agrHalusVal

#Banyaknya Udara Dalam Beton
def persenUdara(dim_agr,jenis_beton) :
    dim_agrs = [9.5,12.5,19,25,37.5,50,75,150]
    noUdara = [3,2.5,2,1.5,1,0.5,0.3,0.2]
    dgnUdara = [[4.5,4,3.5,3,2.5,2,1.5,1],
                [6,5.5,5,4.5,4.5,4,3.5,3],
                [7.5,7,6,6,5.5,5,4.5,4]]
    persUdaraVal = 0
    dimIndex = dim_agrs.index(dim_agr)
    if bool_udara == False :
        persUdaraVal = noUdara[dimIndex]
    elif bool_udara == True :
        persUdaraVal = dgnUdara[jenis_beton][dimIndex]

    return persUdaraVal

def main() :
    air_pencampur = airPencampur(slump_rcn,dim_agr_maks)
    FAS = faktorFAS(mutu_rcn)
    vol_agr_kasar = volume_agrKasar(dim_agr_maks,mods_agr_halus,berat_kering_oven)
    perkiraan_BBeton = perk_awalBBeton(dim_agr_maks)
    semen = air_pencampur/FAS
    vol_berat_halus = perk_agrHalus(air_pencampur,semen,perkiraan_BBeton,vol_agr_kasar)

    persen_udara = persenUdara(dim_agr_maks, jenis_beton)
    #Berat Absolut
    airAbs = air_pencampur/1000
    semenAbs = semen/(bj_semen*1000)
    agrKasarAbs = vol_agr_kasar/(ssd_kasar*1000)
    volUdara = persen_udara/100
    totalSelainHalus = abs(airAbs+semenAbs+agrKasarAbs+volUdara)
    volAgrHalusAbs = 1 - totalSelainHalus
    agrHalus = volAgrHalusAbs * ssd_halus*1000

    print(f"Banyaknya air pencampur             : {air_pencampur} Kg/m^3 \n")
    print(f"Rasio Air Semen                     : {FAS} \n")
    print(f"Banyaknya Kadar Semen               : {semen} Kg/m^3 \n")
    print(f"Volume Agregat Kasar Kering Oven    : {agrKasarAbs} m^3 \n")
    print(f"Berat Kering Agregat Kasar          : {vol_agr_kasar} Kg \n")
    print(f"Berat Perkiraan                     : {perkiraan_BBeton} Kg \n")
    print(f"Berat Agregat Halus                 : {vol_berat_halus} Kg \n")
    print(f"Volume Air                          : {airAbs} m^3 \n")
    print(f"Volume Padat Semen                  : {semenAbs} m^3 \n")
    print(f"Volume Absolut Agregat Kasar        : {agrKasarAbs} m^3 \n")
    print(f"Volume Udara Terperangkap           : {persen_udara} m^3 \n")
    print(f"Jumlah Volume Padat Selain agregat Halus    : {totalSelainHalus} m^3 \n")
    print(f"Volume Agregat halus Yang Dibutuhkan        : {volAgrHalusAbs} m^3 \n")
    print(f"Berat Agregat Halus Kering Yang Dibutuhkan  : {agrHalus} Kg \n")

main()
