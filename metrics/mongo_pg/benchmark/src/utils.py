import csv
import time
from typing import Generator


def get_metrics_info(func):
    def inner(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        work_time =(end_time - start_time) * 1000
        print(f"Время работы функции {work_time:.2f} мс.")
        return result
    return inner


def read_csv(path_file: str) -> Generator:
    with open(path_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = []
        for row in reader:
            row['like_'] = int(row['like_'])
            rows.append(row)
            if len(rows) == 10000:
                yield rows
                rows = []
                
