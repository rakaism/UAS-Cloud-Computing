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
        transfer_energy = calculate_transfer_energy(device, "Fog", data_size)
        total_energy += execution_energy + transfer_energy

    return total_energy

# Fungsi untuk menghitung estimasi heuristik
def calculate_heuristic(job, device):
    job_size = jobs[job]["Ukuran"]
    execution_freq = jobs[job]["Eksekusi"]
    cpu_freq = devices[device]["CPU"]
    transfer_rate = devices[device]["TransferRate"]

    # Hitung estimasi waktu eksekusi pada perangkat
    execution_time = (job_size / transfer_rate) / cpu_freq

    # Hitung estimasi waktu transfer data
    transfer_time = job_size / transfer_rate

    # Hitung estimasi heuristik sebagai jumlah waktu eksekusi dan transfer
    heuristic = execution_time + transfer_time

    return heuristic

# ... (fungsi-fungsi lainnya)

# Fungsi untuk inisialisasi semut
def initialize_ants(num_ants):
    ants = [{"current_solution": {}, "visited_jobs": set()} for _ in range(num_ants)]
    return ants

# Fungsi untuk memilih langkah berdasarkan aturan probabilitas
def choose_next_job(ant, pheromone_matrix, alpha, beta):
    remaining_jobs = set(jobs.keys()) - ant["visited_jobs"]
    probabilities = []

    for job in remaining_jobs:
        pheromone = pheromone_matrix[ant["current_solution"], job]
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
        total_energy = calculate_total_energy(ant["current_solution"])
        for job, device in ant["current_solution"].items():
            pheromone_matrix[device, job] = evaporation * pheromone_matrix[device, job] + Q / total_energy

    return pheromone_matrix

# Fungsi untuk menjalankan algoritma Ant Colony Optimization
def ant_colony_optimization(num_ants, max_iterations, alpha, beta, rho, Q):
    pheromone_matrix = {(device, job): 1.0 for device in devices for job in jobs}
    best_solution = None
    best_energy = float("inf")

    for iteration in range(max_iterations):
        ants = initialize_ants(num_ants)

        for ant in ants:
            while len(ant["visited_jobs"]) < len(jobs):
                next_job = choose_next_job(ant, pheromone_matrix, alpha, beta)
                ant["visited_jobs"].add(next_job)
                ant["current_solution"][next_job] = random.choice(list(devices.keys()))

        # Update pheromone matrix
        pheromone_matrix = update_pheromone_matrix(pheromone_matrix, ants, rho, Q)

        # Find the best solution so far
        for ant in ants:
            total_energy = calculate_total_energy(ant["current_solution"])
            if total_energy < best_energy:
                best_solution = ant["current_solution"].copy()
                best_energy = total_energy

    return best_solution, best_energy

# Jalankan algoritma Ant Colony Optimization
best_solution, best_energy = ant_colony_optimization(
    num_ants=10, max_iterations=50, alpha=1, beta=2, rho=0.5, Q=1
)

# Tampilkan hasil
if best_solution is None:
    print("Tidak ditemukan solusi yang memenuhi")
else:
    print("Kombinasi tugas dan perangkat mobile dengan energi minimum (Ant Colony Optimization):")
    for job, device in best_solution.items():
        print("Tugas", job, "-> Perangkat Mobile", device)
    print("Total energi:", best_energy)
    solution_list = list(best_solution.values())
    print("Kombinasi terbaik:", solution_list)
    print("Jumlah energi terendah:", best_energy)