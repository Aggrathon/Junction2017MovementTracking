
import csv
import random

def generate_random_walk_data(n_rows=1000):
    values = [0 for _ in xrange(n_rows)]
    values[0] = round(random.uniform(-10, 10), 2)
    for i in range(1, n_rows):
        values[i] = round(values[i - 1] + random.uniform(-1, 1), 2)
    return values


def main():
    n_rows = 1000
    x = generate_random_walk_data(n_rows)
    y = generate_random_walk_data(n_rows)
    z = generate_random_walk_data(n_rows)
    with open('data/angular_velocity.csv', 'w') as csvfile:
        fieldnames = ['x', 'y', 'z']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(n_rows):            
            writer.writerow({'x': x[i], 'y': y[i], 'z': z[i]})


if __name__ == '__main__':
    main()