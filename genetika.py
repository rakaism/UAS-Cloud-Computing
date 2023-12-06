import random

# Fungsi untuk menghitung jarak antar dua kota
def hitung_jarak(kota1, kota2):
    # Gunakan formulasi jarak Euclidean sebagai contoh
    return ((kota1[0] - kota2[0]) ** 2 + (kota1[1] - kota2[1]) ** 2) ** 0.5

# Fungsi untuk menghitung total jarak suatu rute
def hitung_total_jarak(rute, kota):
    total_jarak = 0
    for i in range(len(rute) - 1):
        total_jarak += hitung_jarak(kota[rute[i]], kota[rute[i+1]])
    return total_jarak

# Inisialisasi kota dan populasi awal
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
populasi_size = 10
populasi = [random.sample(range(len(kota)), len(kota)) for _ in range(populasi_size)]

# Fungsi seleksi menggunakan turnamen
def seleksi(populasi, kota):
    return min(populasi, key=lambda x: hitung_total_jarak(x, kota))

# Fungsi crossover menggunakan metode order crossover
def crossover(parent1, parent2):
    start = random.randint(0, len(parent1) - 1)
    end = random.randint(start + 1, len(parent1))
    child = [-1] * len(parent1)
    child[start:end] = parent1[start:end]
    remaining = [item for item in parent2 if item not in child]
    index = 0
    for i in range(len(child)):
        if child[i] == -1:
            child[i] = remaining[index]
            index += 1
    return child

# Fungsi mutasi menggunakan swap mutation
def mutasi(rute):
    idx1, idx2 = random.sample(range(len(rute)), 2)
    rute[idx1], rute[idx2] = rute[idx2], rute[idx1]
    return rute

# Algoritma Genetika
generasi = 1000
for gen in range(generasi):
    populasi = sorted(populasi, key=lambda x: hitung_total_jarak(x, kota))
    elitisme = 2
    terpilih = populasi[:elitisme]
    orangtua = [crossover(populasi[i], populasi[i+1]) for i in range(len(populasi) - elitisme)]
    anak_mutasi = [mutasi(child) for child in orangtua]
    populasi = terpilih + anak_mutasi

# Hasil terbaik setelah iterasi selesai
rute_terbaik = seleksi(populasi, kota)
jarak_terpendek = hitung_total_jarak(rute_terbaik, kota)

print("Rute Terbaik:", rute_terbaik)
print("Jarak Terpendek:", jarak_terpendek)