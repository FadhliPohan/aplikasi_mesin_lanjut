from pydantic import BaseModel
from fastapi import APIRouter
from typing import List
import math

router = APIRouter()  # Router khusus untuk tugas1

# Pydantic model untuk request body
class NumbersRequest(BaseModel):
    numbers: List[int]

# Fungsi untuk memisahkan angka ganjil dan genap
def sort_odd_even(numbers: List[int]):
    ganjil = [num for num in numbers if num % 2 != 0]  # Memilih angka ganjil : angka yang tidak habis dibagi 2
    genap = [num for num in numbers if num % 2 == 0]  # Memilih angka genap : angka yang habis dibagi 2
    return {"ganjil": ganjil, "genap": genap}

# Fungsi penentuan rata-rata nilai ganjil dan genap
def average_odd_even(numbers: List[int]):
    ganjil = [num for num in numbers if num % 2 != 0]  # Memilih angka ganjil
    genap = [num for num in numbers if num % 2 == 0]  # Memilih angka genap
    rata_ganjil = sum(ganjil) / len(ganjil) if ganjil else 0  # Menghitung rata-rata ganjil
    rata_genap = sum(genap) / len(genap) if genap else 0  # Menghitung rata-rata genap
    return {"rata_ganjil": rata_ganjil, "rata_genap": rata_genap}

# Fungsi untuk menghitung simpangan baku (standard deviation)
def standard_deviation(numbers: List[int]):
    mean = sum(numbers) / len(numbers) if numbers else 0 #cari rata rata
    variance = sum((x - mean) ** 2 for x in numbers) / len(numbers) if numbers else 0 #cari variansi
    return math.sqrt(variance) #cari akar dari variansi

# Fungsi untuk menghitung simpangan baku ganjil dan genap
def standard_deviation_odd_even(numbers: List[int]):
    ganjil = [num for num in numbers if num % 2 != 0]  # Memilih angka ganjil
    genap = [num for num in numbers if num % 2 == 0]  # Memilih angka genap
    std_ganjil = standard_deviation(ganjil)  # Menghitung simpangan baku ganjil
    std_genap = standard_deviation(genap)  # Menghitung simpangan baku genap
    return {"std_ganjil": std_ganjil, "std_genap": std_genap}

#fungsi rata rata simpangan baku ganjil dan genap
    averages_based_on_std = average_based_on_std(request.numbers)  # Menghitung rata-rata berdasarkan simpangan baku
def average_based_on_std(numbers: List[int]):
    ganjil = [num for num in numbers if num % 2 != 0]  # Memilih angka ganjil
    genap = [num for num in numbers if num % 2 == 0]  # Memilih angka genap
    std_ganjil = standard_deviation(ganjil)  # Menghitung simpangan baku ganjil
    std_genap = standard_deviation(genap)  # Menghitung simpangan baku genap
    rata_rata = (std_ganjil + std_genap)/2
    return {"standar_deviasi_genap_ganjil": rata_rata}


# Endpoint untuk menerima array angka dan mengurutkan ganjil-genap serta menghitung rata-rata dan simpangan baku
@router.post("/sort")
def sort_numbers(request: NumbersRequest):  # Gunakan model Pydantic untuk request body
    sorted_data = sort_odd_even(request.numbers)  # Mengakses 'numbers' dari body
    averages = average_odd_even(request.numbers)  # Menghitung rata-rata ganjil dan genap
    std_devs = standard_deviation_odd_even(request.numbers)  # Menghitung simpangan baku ganjil dan genap
    total_std_devs = standard_deviation(request.numbers)  # Menghitung simpangan baku total
    averages_based_on_std = average_based_on_std(request.numbers)  # Menghitung rata-rata berdasarkan simpangan baku
    return {
        "data": sorted_data,
        "rata-rata": averages,
        "simpangan_baku": std_devs,
        "simpangan_baku_total": total_std_devs,
        "rata-rata_simpangan_baku": averages_based_on_std

    }
