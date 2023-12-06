import numpy as np

# Inisialisasi data pekerjaan dan perangkat mobile
jumlah_pekerjaan = 50
jumlah_perangkat_mobile = 50

# Generate data secara acak
nilai_energi = np.random.uniform(1, 10, (jumlah_pekerjaan, jumlah_perangkat_mobile))
nilai_waktu = np.random.uniform(5, 20, (jumlah_pekerjaan, jumlah_perangkat_mobile))

# Inisialisasi parameter Bee Algorithm
jumlah_lebah = 100
iterasi = 50
lokasi_mobile_awal = np.random.choice(jumlah_perangkat_mobile, jumlah_pekerjaan)

# Fungsi evaluasi
def evaluasi(lokasi_mobile):
    nilai_energi_total = np.sum(nilai_energi[np.arange(jumlah_pekerjaan), lokasi_mobile])
    nilai_waktu_total = np.sum(nilai_waktu[np.arange(jumlah_pekerjaan), lokasi_mobile])
    return nilai_energi_total, nilai_waktu_total

# Inisialisasi lebah secara acak
lokasi_mobile_lebah = np.random.choice(jumlah_perangkat_mobile, (jumlah_lebah, jumlah_pekerjaan))

# Algoritma Bee
for _ in range(iterasi):
    # Evaluasi nilai untuk setiap lebah
    nilai_evaluasi = np.array([evaluasi(lokasi_mobile) for lokasi_mobile in lokasi_mobile_lebah])

    # Sorting lebah berdasarkan nilai evaluasi (minimasi)
    urutan_sorting = np.lexsort((nilai_evaluasi[:, 1], nilai_evaluasi[:, 0]))
    lokasi_mobile_lebah = lokasi_mobile_lebah[urutan_sorting]

    # Pembaruan posisi lebah terbaik dan lebah pengintai
    lokasi_mobile_terbaik = lokasi_mobile_lebah[0]
    lokasi_mobile_pengintai = np.random.choice(jumlah_perangkat_mobile, (jumlah_lebah - 1, jumlah_pekerjaan))

    # Pencarian lokal dengan perturbasi
    lokasi_mobile_pengintai += np.random.choice([-1, 0, 1], size=(jumlah_lebah - 1, jumlah_pekerjaan))

    # Pembaruan posisi lebah
    probabilitas = np.exp(-nilai_evaluasi / nilai_evaluasi.std(axis=0))
    probabilitas /= probabilitas.sum(axis=0)
    indeks_lebah_terbaik = np.argmin(nilai_evaluasi[:, 0] + nilai_evaluasi[:, 1])

    for i in range(jumlah_lebah - 1):
        if np.random.rand() < probabilitas[i, 0]:
            lokasi_mobile_lebah[i + 1] = np.copy(lokasi_mobile_terbaik)
        else:
            lokasi_mobile_lebah[i + 1] = np.copy(lokasi_mobile_pengintai[i])

    # Mutasi pada beberapa lebah
    jumlah_mutasi = int(jumlah_lebah * 0.1)
    indeks_mutasi = np.random.choice(jumlah_lebah, jumlah_mutasi, replace=False)
    lokasi_mobile_lebah[indeks_mutasi] = np.random.choice(jumlah_perangkat_mobile, (jumlah_mutasi, jumlah_pekerjaan))

# Hasil akhir
lokasi_mobile_terbaik = lokasi_mobile_lebah[0]
nilai_energi_terbaik, nilai_waktu_terbaik = evaluasi(lokasi_mobile_terbaik)

print("Alokasi Pekerjaan pada Perangkat Mobile Terbaik:")
print(lokasi_mobile_terbaik)
print("Total Nilai Energi Terbaik:", nilai_energi_terbaik)
print("Total Nilai Waktu Terbaik:", nilai_waktu_terbaik)
