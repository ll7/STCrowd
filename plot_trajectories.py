import json

base_name = 'STCrowd_official/anno/'
file_name = '13.json'
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
    frame_id = frame['frameId']
    for item in frame['items']:
        if item['category'] == 'person':
            person_id = item['id']
            if person_id not in movements:
                movements[person_id] = []
            # Append a tuple of (x position, y position, frameId)
            movements[person_id].append((item['position']['x'], item['position']['y'], frame_id))

import matplotlib.pyplot as plt

# Assuming movements dictionary is already populated
for person_id, positions in movements.items():
    # Extract x, y positions and frameIds
    x_positions, y_positions, frame_ids = zip(*positions)
    
    # Plot the trajectory for each person
    plt.plot(x_positions, y_positions, marker='o', label=person_id)

    # Annotate each point with its frameId
    for x, y, frame_id in positions:
        plt.annotate(str(frame_id), (x, y))

plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.title(f'{file_name}')
plt.gca().set_aspect('equal', adjustable='box')  # Set equal aspect ratio
plt.legend()
plt.show()

