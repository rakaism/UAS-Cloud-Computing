import random
import copy

# ... (definisi pekerjaan, perangkat mobile, dan fungsi-fungsi lainnya)
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
def generate_initial_population(population_size):
    population = []
    for _ in range(population_size):
        solution = {}
        for job in range(1, 11):
            devices_copy = list(devices.keys())
            random.shuffle(devices_copy)
            device = devices_copy[0]
            solution[job] = device
        population.append(solution)
    return population

# Fungsi untuk melakukan seleksi turnamen
def tournament_selection(population, tournament_size):
    selected_candidates = random.sample(population, tournament_size)
    winner = min(selected_candidates, key=lambda x: calculate_total_time(x))
    return winner

# Fungsi crossover dua solusi
def crossover(parent1, parent2):
    child = {}
    crossover_point = random.randint(1, 9)
    child.update({job: parent1[job] for job in range(1, crossover_point + 1)})
    child.update({job: parent2[job] for job in range(crossover_point + 1, 11)})
    return child

# Fungsi mutasi solusi
def mutate(solution, mutation_rate):
    mutated_solution = solution.copy()
    for job in solution:
        if random.random() < mutation_rate:
            devices_copy = list(devices.keys())
            devices_copy.remove(solution[job])
            new_device = random.choice(devices_copy)
            mutated_solution[job] = new_device
    return mutated_solution

def generate_neighbor(solution):
    neighbor = solution.copy()
    jobs = list(neighbor.keys())
    random.shuffle(jobs)
    job1, job2 = jobs[:2]
    neighbor[job1], neighbor[job2] = neighbor[job2], neighbor[job1]
    return neighbor

# Fungsi untuk menjalankan algoritma memetic
def memetic_algorithm(population_size, generations, tournament_size, crossover_rate, mutation_rate, local_search_rate):
    population = generate_initial_population(population_size)

    for generation in range(generations):
        new_population = []

        # Elitisme: Pilih 10% solusi terbaik langsung masuk ke generasi berikutnya
        elite_size = int(0.1 * population_size)
        elite = sorted(population, key=lambda x: calculate_total_time(x))[:elite_size]
        new_population.extend(elite)

        # Generasi baru dengan crossover dan mutasi
        while len(new_population) < population_size:
            parent1 = tournament_selection(population, tournament_size)
            parent2 = tournament_selection(population, tournament_size)

            # Crossover
            if random.random() < crossover_rate:
                child = crossover(parent1, parent2)
            else:
                child = parent1

            # Mutasi
            child = mutate(child, mutation_rate)

            # Local search
            if random.random() < local_search_rate:
                child = local_search(child)

            new_population.append(child)

        population = new_population

    # Pilih solusi terbaik dari populasi akhir
    best_solution = min(population, key=lambda x: calculate_total_time(x))
    best_time = calculate_total_time(best_solution)

    return best_solution, best_time

# Fungsi local search
def local_search(solution):
    local_best = copy.deepcopy(solution)
    local_best_time = calculate_total_time(local_best)

    for _ in range(5):
        neighbor = generate_neighbor(local_best)
        neighbor_time = calculate_total_time(neighbor)

        if neighbor_time < local_best_time:
            local_best = copy.deepcopy(neighbor)
            local_best_time = neighbor_time

    return local_best

# Jalankan algoritma memetic
best_solution_ma, best_time_ma = memetic_algorithm(
    population_size=100, generations=50, tournament_size=5, crossover_rate=0.7, mutation_rate=0.2, local_search_rate=0.3
)

# Tampilkan hasil memetic
print("Kombinasi tugas dan perangkat mobile dengan waktu minimum (Memetic Algorithm):")
for job, device in best_solution_ma.items():
    print("Tugas", job, "-> Perangkat Mobile", device)
print("Total waktu:", best_time_ma)
solution_list_ma = list(best_solution_ma.values())
print("Kombinasi terbaik:", solution_list_ma)
print("Jumlah waktu terendah:", best_time_ma)
