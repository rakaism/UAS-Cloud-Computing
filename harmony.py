import numpy as np

# Fungsi untuk menghitung jarak antar dua kota
def hitung_jarak(kota1, kota2):
    return ((kota1[0] - kota2[0]) ** 2 + (kota1[1] - kota2[1]) ** 2) ** 0.5

# Inisialisasi kota
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

# Parameter Harmony Search
jumlah_harmony = 10
iterasi_max = 100
bandwidth = 0.5
harmony_memory_rate = 0.7

# Inisialisasi harmony memory
harmony_memory = [np.random.permutation(jumlah_semua_kota) for _ in range(jumlah_harmony)]

# Fungsi evaluasi
def evaluate(solution, kota):
    total_jarak = sum([hitung_jarak(kota[solution[i]], kota[solution[i + 1]]) for i in range(len(solution) - 1)])
    return total_jarak

# Harmony Search
for iterasi in range(iterasi_max):
    # Improvisasi
    new_solution = np.random.permutation(jumlah_semua_kota)
    for i in range(jumlah_semua_kota):
        if np.random.rand() < bandwidth:
            new_solution[i] = np.random.choice(jumlah_semua_kota)

    # Evaluasi
    cost_new_solution = evaluate(new_solution, kota)

    # Update harmony memory
    worst_index = np.argmax([evaluate(sol, kota) for sol in harmony_memory])
    if cost_new_solution < evaluate(harmony_memory[worst_index], kota):
        harmony_memory[worst_index] = new_solution

    # Adjust bandwidth
    bandwidth *= harmony_memory_rate

# Hasil terbaik setelah iterasi selesai
solusi_terbaik = min(harmony_memory, key=lambda x: evaluate(x, kota))
jarak_terpendek = evaluate(solusi_terbaik, kota)

print("Solusi Terbaik:", solusi_terbaik)
print("Jarak Terpendek:", jarak_terpendek)
