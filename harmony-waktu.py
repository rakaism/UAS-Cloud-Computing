import random

# ... (Definisi pekerjaan, perangkat mobile, dan fungsi-fungsi lainnya)
# Informasi pekerjaan
jobs = {
    1: {"Ukuran": 30, "Eksekusi": 40000},
    2: {"Ukuran": 100, "Eksekusi": 500000},
    3: {"Ukuran": 10000, "Eksekusi": 40000},
    4: {"Ukuran": 50, "Eksekusi": 200000},
    5: {"Ukuran": 500, "Eksekusi": 1000000},
    6: {"Ukuran": 200, "Eksekusi": 600000},
    7: {"Ukuran": 1000, "Eksekusi": 300000},
    8: {"Ukuran": 150, "Eksekusi": 700000},
    9: {"Ukuran": 1000, "Eksekusi": 200000},
    10: {"Ukuran": 2000, "Eksekusi": 900000},
}

# Informasi perangkat mobile
devices = {
    i: {"CPU": random.uniform(1.0, 2.0), "Battery": random.uniform(3.0, 6.0), "TransferRate": random.uniform(10, 50)}
    for i in range(1, 51)
}

# Informasi transfer energi
transfer_energy = {"Fog": 0.01, "Cloud": 0.01}

# Fungsi untuk menghitung waktu
def calculate_time(job, device):
    job_size = jobs[job]["Ukuran"]
    execution_freq = jobs[job]["Eksekusi"]
    cpu_freq = devices[device]["CPU"]

    # Hitung waktu eksekusi pada perangkat
    execution_time = job_size / (execution_freq / cpu_freq)

    return execution_time

# Fungsi untuk menghitung waktu transfer data
def calculate_transfer_time(source, destination, data_size):
    transfer_rate = devices[source]["TransferRate"]

    # Hitung waktu transfer data
    transfer_time = data_size / transfer_rate

    return transfer_time

# Fungsi untuk menghitung total waktu
def calculate_total_time(combination):
    total_time = 0

    for job, device in combination.items():
        data_size = jobs[job]["Ukuran"]
        execution_time = calculate_time(job, device)
        transfer_time = calculate_transfer_time(device, "Fog", data_size)
        total_time += execution_time + transfer_time

    return total_time

# Fungsi untuk menghasilkan populasi awal
def initialize_harmony_memory(hm_size):
    harmony_memory = []
    for _ in range(hm_size):
        solution = {}
        for job in range(1, 11):
            devices_copy = list(devices.keys())
            random.shuffle(devices_copy)
            device = devices_copy[0]
            solution[job] = device
        harmony_memory.append(solution)
    return harmony_memory

# Fungsi untuk memilih harmoni
def choose_harmony(harmony_memory):
    return random.choice(harmony_memory)

# Fungsi untuk membuat harmoni baru
def create_new_harmony(harmony_memory, hm_consider_rate, bandwidth, memory_size):
    new_harmony = {}
    for job in range(1, 11):
        if random.random() < hm_consider_rate:
            selected_harmony = choose_harmony(harmony_memory)
            new_harmony[job] = selected_harmony[job]
        else:
            devices_copy = list(devices.keys())
            random.shuffle(devices_copy)
            new_harmony[job] = devices_copy[0]
    return new_harmony

# Fungsi untuk evaluasi harmoni
def evaluate_harmony(harmony):
    total_time = calculate_total_time(harmony)
    return 1 / total_time

# Fungsi untuk menjalankan algoritma Harmony Search
def harmony_search(hm_size, max_iterations, hm_consider_rate, bandwidth, memory_size):
    harmony_memory = initialize_harmony_memory(hm_size)
    best_harmony = None
    best_evaluation = 0

    for iteration in range(max_iterations):
        new_harmony = create_new_harmony(harmony_memory, hm_consider_rate, bandwidth, memory_size)
        evaluation = evaluate_harmony(new_harmony)

        if evaluation > best_evaluation:
            best_harmony = new_harmony
            best_evaluation = evaluation

        worst_index = min(range(hm_size), key=lambda x: evaluate_harmony(harmony_memory[x]))
        if evaluation > evaluate_harmony(harmony_memory[worst_index]):
            harmony_memory[worst_index] = new_harmony

    return best_harmony, calculate_total_time(best_harmony)

# Jalankan algoritma Harmony Search
best_solution_hs, best_time_hs = harmony_search(
    hm_size=50, max_iterations=100, hm_consider_rate=0.7, bandwidth=0.1, memory_size=5
)

# Tampilkan hasil
print("Kombinasi tugas dan perangkat mobile dengan waktu minimum (Harmony Search):")
for job, device in best_solution_hs.items():
    print("Tugas", job, "-> Perangkat Mobile", device)
print("Total waktu:", best_time_hs)
solution_list_hs = list(best_solution_hs.values())
print("Kombinasi terbaik:", solution_list_hs)
print("Jumlah waktu terendah:", best_time_hs)