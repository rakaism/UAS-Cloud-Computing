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

# Fungsi untuk menghasilkan jalur semut
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
        total_time = calculate_total_time(ant)
        pheromone_value = pheromone.get(tuple(sorted(ant.items())), 0.0)
        probability = pheromone_value / total_time

        if probability > max_prob:
            max_prob = probability
            selected_ant = ant

    return selected_ant

# Fungsi untuk memperbarui nilai feromon
def update_pheromone(pheromone, ants, evaporation_rate):
    for ant in ants:
        ant_tuple = tuple(sorted(ant.items()))  # Menggunakan tuple dari item yang diurutkan sebagai kunci
        total_time = calculate_total_time(ant)
        pheromone_value = pheromone.get(ant_tuple, 0.0)
        new_pheromone_value = (1 - evaporation_rate) * pheromone_value + (1 / total_time)

        pheromone[ant_tuple] = new_pheromone_value

    return pheromone

# Fungsi untuk menjalankan algoritma ant colony optimization
def ant_colony_optimization(population_size, generations, evaporation_rate):
    pheromone = {}
    best_solution = None
    best_time = float('inf')

    for generation in range(generations):
        ants = [generate_ant_path() for _ in range(population_size)]

        for ant in ants:
            total_time = calculate_total_time(ant)
            if total_time < best_time:
                best_time = total_time
                best_solution = ant

        pheromone = update_pheromone(pheromone, ants, evaporation_rate)

    return best_solution, best_time

# Jalankan algoritma ant colony optimization
best_solution, best_time = ant_colony_optimization(population_size=100, generations=50, evaporation_rate=0.1)

# Tampilkan hasil
if best_solution is None:
    print("Tidak ditemukan solusi yang memenuhi")
else:
    print("Kombinasi tugas dan perangkat mobile dengan waktu minimum (Ant Colony Optimization):")
    for job, device in best_solution.items():
        print("Tugas", job, "-> Perangkat Mobile", device)
    print("Total waktu:", best_time)
    solution_list = list(best_solution.values())
    print("Kombinasi terbaik:", solution_list)
    print("Jumlah waktu terendah:", best_time)
