import random

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
        transfer_energy_value = calculate_transfer_energy(device, "Fog", data_size)
        total_energy += execution_energy + transfer_energy_value

    return total_energy

# Fungsi untuk menghasilkan jalur ant
def generate_ant_path():
    ant_path = {}
    for job in range(1, 11):
        devices_copy = list(devices.keys())
        random.shuffle(devices_copy)
        device = devices_copy[0]
        ant_path[job] = device
    return ant_path

# Fungsi untuk melakukan pemilihan oleh semut
def ant_selection(ants, pheromone):
    selected_ant = None
    max_prob = 0.0

    for ant in ants:
        total_energy = calculate_total_energy(ant)
        pheromone_value = pheromone[ant]
        probability = pheromone_value / total_energy

        if probability > max_prob:
            max_prob = probability
            selected_ant = ant

    return selected_ant

def update_pheromone(pheromone, ants, evaporation_rate):
    for ant in ants:
        ant_tuple = tuple(sorted(ant.items()))  # Menggunakan tuple dari item yang diurutkan sebagai kunci
        total_energy = calculate_total_energy(ant)
        pheromone_value = pheromone.get(ant_tuple, 0.0)
        new_pheromone_value = (1 - evaporation_rate) * pheromone_value + (1 / total_energy)

        pheromone[ant_tuple] = new_pheromone_value

    return pheromone


# Fungsi untuk menjalankan algoritma ant colony optimization
def ant_colony_optimization(population_size, generations, evaporation_rate):
    pheromone = {}
    best_solution = None
    best_energy = float('inf')

    for generation in range(generations):
        ants = [generate_ant_path() for _ in range(population_size)]

        for ant in ants:
            total_energy = calculate_total_energy(ant)
            if total_energy < best_energy:
                best_energy = total_energy
                best_solution = ant

        pheromone = update_pheromone(pheromone, ants, evaporation_rate)

    return best_solution, best_energy

# Jalankan algoritma ant colony optimization
best_solution, best_energy = ant_colony_optimization(population_size=100, generations=50, evaporation_rate=0.1)

# Tampilkan hasil
if best_solution is None:
    print("Tidak ditemukan solusi yang memenuhi")
else:
    print("Kombinasi tugas dan perangkat mobile dengan energi minimum:")
    for job, device in best_solution.items():
        print("Tugas", job, "-> Perangkat Mobile", device)
    print("Total energi:", best_energy)
    solution_list = list(best_solution.values())
    print("Kombinasi terbaik:", solution_list)
    print("Jumlah energi terendah:", best_energy)
