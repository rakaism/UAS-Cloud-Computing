import numpy as np

# Fungsi untuk menghitung jarak antar dua kota
def hitung_jarak(kota1, kota2):
    return ((kota1[0] - kota2[0]) ** 2 + (kota1[1] - kota2[1]) ** 2) ** 0.5

# Inisialisasi kota dan matriks jarak
kota = [(2, 5),
        (8, 3),
        (6, 9),
        (4, 7),
        (10, 2),
        (12, 6),
        (3, 10), 
        (9, 8), 
        (5, 4), 
        (11, 1), 
        (7, 12), 
        (1, 9), 
        (10, 5),
        (4, 3), 
        (8, 11), 
        (6, 1), 
        (3, 7), 
        (9, 4), 
        (12, 10), 
        (2, 2)]
jumlah_semua_kota = len(kota)
jarak_matriks = np.zeros((jumlah_semua_kota, jumlah_semua_kota))

for i in range(jumlah_semua_kota):
    for j in range(jumlah_semua_kota):
        jarak_matriks[i][j] = hitung_jarak(kota[i], kota[j])

# Parameter ACO
jumlah_semut = 5
alpha = 1.0  # Pengaruh pheromone
beta = 2.0   # Pengaruh jarak
rho = 0.5    # Tingkat penguapan pheromone
Q = 1.0      # Pheromone yang dilepaskan semut

# Inisialisasi pheromone
pheromone = np.ones((jumlah_semua_kota, jumlah_semua_kota)) / jumlah_semua_kota

# Algoritma Ant Colony Optimization
generasi = 100
for gen in range(generasi):
    lintasan_semua_semut = []
    for semut in range(jumlah_semut):
        posisi_semut = np.random.randint(0, jumlah_semua_kota)
        lintasan_semut = [posisi_semut]

        while len(lintasan_semut) < jumlah_semua_kota:
            probabilitas_transisi = np.zeros(jumlah_semua_kota)
            kunjungan = set(lintasan_semut)

            for kota_berikutnya in range(jumlah_semua_kota):
                if kota_berikutnya not in kunjungan:
                    probabilitas_transisi[kota_berikutnya] = (pheromone[posisi_semut][kota_berikutnya] ** alpha) * \
                                                               ((1.0 / jarak_matriks[posisi_semut][kota_berikutnya]) ** beta)

            probabilitas_transisi /= probabilitas_transisi.sum()
            posisi_semut = np.random.choice(range(jumlah_semua_kota), p=probabilitas_transisi)
            lintasan_semut.append(posisi_semut)

        lintasan_semua_semut.append(lintasan_semut)

    # Pembaruan pheromone
    delta_pheromone = np.zeros((jumlah_semua_kota, jumlah_semua_kota))
    for lintasan_semut in lintasan_semua_semut:
        for i in range(len(lintasan_semut) - 1):
            delta_pheromone[lintasan_semut[i]][lintasan_semut[i + 1]] += Q / jarak_matriks[lintasan_semut[i]][lintasan_semut[i + 1]]

    pheromone = (1.0 - rho) * pheromone + delta_pheromone

# Hasil terbaik setelah iterasi selesai
jarak_terpendek = float('inf')
rute_terpendek = None
for lintasan_semut in lintasan_semua_semut:
    total_jarak = sum([jarak_matriks[lintasan_semut[i]][lintasan_semut[i + 1]] for i in range(len(lintasan_semut) - 1)])
    if total_jarak < jarak_terpendek:
        jarak_terpendek = total_jarak
        rute_terpendek = lintasan_semut

print("Rute Terpendek:", rute_terpendek)
print("Jarak Terpendek:", jarak_terpendek)