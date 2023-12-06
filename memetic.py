import random
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

# Parameter Memetic Algorithm
jumlah_populasi = 10
generasi = 100
prob_mutasi = 0.2
ukuran_tournament = 3

# Inisialisasi populasi
populasi = [random.sample(range(jumlah_semua_kota), jumlah_semua_kota) for _ in range(jumlah_populasi)]

# Fungsi evaluasi fitness
def hitung_fitness(rute):
    total_jarak = sum([jarak_matriks[rute[i]][rute[i + 1]] for i in range(len(rute) - 1)])
    return 1 / total_jarak  # Minimalkan jarak, maksimalkan fitness

# Algoritma Memetic
for gen in range(generasi):
    populasi = sorted(populasi, key=lambda x: hitung_fitness(x), reverse=True)  # Sorting berdasarkan fitness (descending)

    # Pembaruan lokal dengan hill climbing pada beberapa individu terbaik
    for i in range(2):
        individu_terbaik = populasi[i]
        for _ in range(5):  # Melakukan hill climbing sebanyak 5 iterasi
            titik1, titik2 = random.sample(range(jumlah_semua_kota), 2)
            individu_terbaik[titik1], individu_terbaik[titik2] = individu_terbaik[titik2], individu_terbaik[titik1]

    # Seleksi turnamen untuk memilih orang tua
    orangtua1 = max(random.sample(populasi, ukuran_tournament), key=lambda x: hitung_fitness(x))
    orangtua2 = max(random.sample(populasi, ukuran_tournament), key=lambda x: hitung_fitness(x))

    # Crossover menggunakan order crossover
    start = random.randint(0, jumlah_semua_kota - 1)
    end = random.randint(start + 1, jumlah_semua_kota)
    anak = [-1] * jumlah_semua_kota
    anak[start:end] = orangtua1[start:end]
    remaining = [item for item in orangtua2 if item not in anak]
    index = 0
    for i in range(jumlah_semua_kota):
        if anak[i] == -1:
            anak[i] = remaining[index]
            index += 1

    # Mutasi dengan swap mutation
    if random.random() < prob_mutasi:
        titik1, titik2 = random.sample(range(jumlah_semua_kota), 2)
        anak[titik1], anak[titik2] = anak[titik2], anak[titik1]

    # Evaluasi fitness anak
    fitness_anak = hitung_fitness(anak)
    if fitness_anak > hitung_fitness(populasi[-1]):
        populasi[-1] = anak

# Hasil terbaik setelah iterasi selesai
rute_terbaik = max(populasi, key=lambda x: hitung_fitness(x))
jarak_terpendek = 1 / hitung_fitness(rute_terbaik)

print("Rute Terpendek:", rute_terbaik)
print("Jarak Terpendek:", jarak_terpendek)