import random

# ... (definisi pekerjaan, perangkat mobile, dan fungsi-fungsi lainnya)
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

# Fungsi untuk menghitung energi
def calculate_energy(job, device):
    job_size = jobs[job]["Ukuran"]
    execution_freq = jobs[job]["Eksekusi"]
    cpu_freq = devices[device]["CPU"]
    battery = devices[device]["Battery"]
    transfer_rate = devices[device]["TransferRate"]

    # Hitung energi eksekusi pada perangkat
    execution_energy = (execution_freq / cpu_freq) * (job_size / transfer_rate) * battery

    return execution_energy

# Fungsi untuk menghitung energi transfer data
def calculate_transfer_energy(source, destination, data_size):
    transfer_rate = devices[source]["TransferRate"]
    transfer_energy_per_kb = transfer_energy[destination]

    # Hitung energi transfer data
    transfer_energy_value = (data_size / transfer_rate) * transfer_energy_per_kb

    return transfer_energy_value

# Fungsi untuk menghitung total energi
def calculate_total_energy(combination):
    total_energy = 0

    for job, device in combination.items():
        data_size = jobs[job]["Ukuran"]
        execution_energy = calculate_energy(job, device)
        transfer_energy = calculate_transfer_energy(device, "Fog", data_size)
        total_energy += execution_energy + transfer_energy

    return total_energy

# Fungsi untuk membangkitkan harmoni awal
def generate_initial_harmony():
    harmony = {}
    for job in range(1, 11):
        devices_copy = list(devices.keys())
        random.shuffle(devices_copy)
        device = devices_copy[0]
        harmony[job] = device
    return harmony

# Fungsi untuk memilih harmoni terbaik dari populasi
def select_best_harmony(population):
    return min(population, key=lambda x: calculate_total_energy(x))

# Fungsi untuk memutakhirkan populasi dengan proses improvisasi harmoni
def update_harmonies(population, harmony_memory_size, pitch_adjust_rate):
    new_population = population.copy()

    for _ in range(harmony_memory_size):
        # Generate new harmony through improvisation
        new_harmony = {}
        for job in range(1, 11):
            devices_copy = list(devices.keys())
            random.shuffle(devices_copy)
            if random.random() < pitch_adjust_rate:
                # Adjust pitch by selecting from the memory
                memory_harmony = random.choice(population)
                new_harmony[job] = memory_harmony[job]
            else:
                # Generate a new pitch
                new_harmony[job] = devices_copy[0]

        # Select the best harmony between the new and old harmonies
        current_best_harmony = select_best_harmony(new_population)
        if calculate_total_energy(new_harmony) < calculate_total_energy(current_best_harmony):
            new_population.remove(current_best_harmony)
            new_population.append(new_harmony)

    return new_population

# Fungsi untuk menjalankan algoritma Harmony Search
def harmony_search_algorithm(population_size, harmony_memory_size, iterations, pitch_adjust_rate):
    population = [generate_initial_harmony() for _ in range(population_size)]

    for iteration in range(iterations):
        population = update_harmonies(population, harmony_memory_size, pitch_adjust_rate)

    # Select the best solution from the final population
    best_solution = select_best_harmony(population)
    best_energy = calculate_total_energy(best_solution)

    return best_solution, best_energy

# Jalankan algoritma Harmony Search
best_solution_hs, best_energy_hs = harmony_search_algorithm(
    population_size=100, harmony_memory_size=10, iterations=50, pitch_adjust_rate=0.3
)

# Tampilkan hasil
if best_solution_hs is None:
    print("Tidak ditemukan solusi yang memenuhi")
else:
    print("Kombinasi tugas dan perangkat mobile dengan energi minimum (Harmony Search):")
    for job, device in best_solution_hs.items():
        print("Tugas", job, "-> Perangkat Mobile", device)
    print("Total energi:", best_energy_hs)
    solution_list_hs = list(best_solution_hs.values())
    print("Kombinasi terbaik:", solution_list_hs)
    print("Jumlah energi terendah:", best_energy_hs)