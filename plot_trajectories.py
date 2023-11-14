import json

base_name = 'STCrowd_official/anno/'
file_name = '1.json'
file_path = base_name + file_name

with open(file_path, 'r') as file:
    data = json.load(file)

""" x_positions = []
y_positions = []

for frame in data['frames']:
    for item in frame['items']:
        if item['category'] == 'person':
            x_positions.append(item['position']['x'])
            y_positions.append(item['position']['y'])

import matplotlib.pyplot as plt

plt.scatter(x_positions, y_positions)
plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.title('X, Y Positions of People')
plt.show() """

movements = {}  # Dictionary to store movements

for frame in data['frames']:
    for item in frame['items']:
        if item['category'] == 'person':
            person_id = item['id']
            if person_id not in movements:
                movements[person_id] = []
            movements[person_id].append((item['position']['x'], item['position']['y']))

import matplotlib.pyplot as plt

for person_id, positions in movements.items():
    # Unpack positions into separate x and y lists
    x_positions, y_positions = zip(*positions)
    
    # Plot each person's path
    plt.plot(x_positions, y_positions, marker='o', label=person_id)

plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.title(f'{file_name}')
plt.gca().set_aspect('equal', adjustable='box')  # Set equal aspect ratio
plt.legend()
plt.show()

