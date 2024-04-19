import csv
import random
import uuid

user_ids = [uuid.uuid4() for i in range(0, 10000)] 
films_ids = [uuid.uuid4() for i in range(0, 1000)]


def generate_likes():
    rows = {}
    for u_id in user_ids:
        for f_id in films_ids[0:1000]:
            rows[f'{u_id}:{f_id}'] =  {'key': f'{u_id}:{f_id}', 'user_id': u_id, 'film_id': f_id, 'like_' :random.randint(0, 1)}

    with open('tables/likes.csv', 'w', newline='') as csvfile:
        fieldnames = ['key', 'user_id', 'film_id', 'like_']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in rows.values():
            writer.writerow(row)


if __name__ == '__main__':
    generate_likes()



