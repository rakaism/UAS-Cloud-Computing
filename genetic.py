import numpy as np
from deap import creator, base, tools, gp, algorithms

# Fungsi untuk menghitung jarak antar dua kota
def hitung_jarak(individu, kota):
    formula = toolbox.compile(expr=individu)
    total_jarak = 0
    for i in range(len(kota) - 1):
        kota1 = kota[i]
        kota2 = kota[i + 1]
    return total_jarak,

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

# Definisi fungsi dan terminal untuk GP
pset = gp.PrimitiveSet("MAIN", arity=2)
pset.addPrimitive(np.add, arity=2)
pset.addPrimitive(np.subtract, arity=2)
pset.addPrimitive(np.multiply, arity=2)
pset.addPrimitive(np.divide, arity=2)
pset.addPrimitive(np.square, arity=1)
pset.addPrimitive(np.sqrt, arity=1)
pset.addTerminal(1)
pset.addTerminal(2)
pset.renameArguments(ARG0="x")
pset.renameArguments(ARG1="y")

# Definisi tipe objektif (fitness)
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin)

# Inisialisasi toolbox
toolbox = base.Toolbox()
toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=3)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)
toolbox.register("evaluate", hitung_jarak, kota=kota)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("mutate", gp.mutNodeReplacement, pset=pset)

# Algoritma Genetic Programming
populasi_size = 100
generasi = 50
mutasi_rate = 0.2
crossover_rate = 0.7

populasi = toolbox.population(n=populasi_size)
algorithms.eaSimple(populasi, toolbox, cxpb=crossover_rate, mutpb=mutasi_rate, ngen=generasi, stats=None, halloffame=None, verbose=True)

# Mendapatkan individu terbaik setelah evolusi
best_individu = tools.selBest(populasi, k=1)[0]
formula_terbaik = toolbox.compile(expr=best_individu)

# Evaluasi hasil individu terbaik
jarak_terpendek = hitung_jarak(best_individu, kota)

print("Formula Terbaik:", best_individu)
print("Jarak Terpendek:", jarak_terpendek)
