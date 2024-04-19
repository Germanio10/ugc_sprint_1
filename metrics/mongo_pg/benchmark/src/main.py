import mongo_benchmark
import pg_benchmark
from generate_csv import generate_likes

if __name__ == '__main__':
    print('Генерация данных...')
    generate_likes()
    print('-----------Postgres------------')
    pg_benchmark.run()
    print('-------------Mongo-------------')
    mongo_benchmark.run()
