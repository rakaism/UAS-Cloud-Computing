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

# Fungsi untuk menghitung estimasi heuristik
def calculate_heuristic(job, device):
    job_size = jobs[job]["Ukuran"]
    execution_freq = jobs[job]["Eksekusi"]
    cpu_freq = devices[device]["CPU"]
    transfer_rate = devices[device]["TransferRate"]

    # Hitung estimasi waktu eksekusi pada perangkat
    execution_time = job_size / (execution_freq / cpu_freq)

    # Hitung estimasi waktu transfer data
    transfer_time = job_size / transfer_rate

    # Hitung estimasi heuristik sebagai jumlah waktu eksekusi dan transfer
    heuristic = execution_time + transfer_time

    return heuristic

# Fungsi untuk inisialisasi semut
def initialize_ants(num_ants):
    ants = [{"current_solution": {}, "visited_jobs": set()} for _ in range(num_ants)]
    return ants

# Fungsi untuk memilih langkah berdasarkan aturan probabilitas
def choose_next_job(ant, pheromone_matrix, alpha, beta):
    remaining_jobs = set(jobs.keys()) - ant["visited_jobs"]
    probabilities = []

    for job in remaining_jobs:
        pheromone = pheromone_matrix[(ant["current_solution"], job)]
        heuristic = calculate_heuristic(job, ant["current_solution"])
        probability = pheromone ** alpha * heuristic ** beta
        probabilities.append((job, probability))

    total_probability = sum(prob for _, prob in probabilities)
    probabilities = [(job, prob / total_probability) for job, prob in probabilities]

    chosen_job = random.choices(*zip(*probabilities))[0]
    return chosen_job

# Fungsi untuk memperbarui matriks feromon
def update_pheromone_matrix(pheromone_matrix, ants, rho, Q):
    evaporation = 1 - rho

    for ant in ants:
        total_time = calculate_total_time(ant["current_solution"])
        for job, device in ant["current_solution"].items():
            pheromone_matrix[(device, job)] = evaporation * pheromone_matrix[(device, job)] + Q / total_time

    return pheromone_matrix

# Fungsi untuk menjalankan algoritma Ant Colony Optimization
def ant_colony_optimization(num_ants, max_iterations, alpha, beta, rho, Q):
    pheromone_matrix = {((device, job)): 1.0 for device in devices for job in jobs}
    best_solution = None
    best_time = float('inf')

    for iteration in range(max_iterations):
        ants = initialize_ants(num_ants)

        for ant in ants:
            while len(ant["visited_jobs"]) < len(jobs):
                next_job = choose_next_job(ant, pheromone_matrix, alpha, beta)
                ant["visited_jobs"].add(next_job)
                ant["current_solution"][next_job] = random.choice(list(devices.keys()))

            current_time = calculate_total_time(ant["current_solution"])
            if current_time < best_time:
                best_time = current_time
                best_solution = ant["current_solution"]

        pheromone_matrix = update_pheromone_matrix(pheromone_matrix, ants, rho, Q)

    return best_solution, best_time

# Jalankan algoritma Ant Colony Optimization
best_solution_aco, best_time_aco = ant_colony_optimization(
    num_ants=10, max_iterations=50, alpha=1, beta=2, rho=0.5, Q=1
)

# Tampilkan hasil
if best_solution_aco is None:
    print("Tidak ditemukan solusi yang memenuhi")
else:
    print("Kombinasi tugas dan perangkat mobile dengan waktu minimum (Ant Colony Optimization):")
    for job, device in best_solution_aco.items():
        print("Tugas", job, "-> Perangkat Mobile", device)
    print("Total waktu:", best_time_aco)
    solution_list_aco = list(best_solution_aco.values())
    print("Kombinasi terbaik:", solution_list_aco)
    print("Jumlah waktu terendah:", best_time_aco)
