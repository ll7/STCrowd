import json

base_name = 'STCrowd_official/anno/'
file_name = '33.json'
file_path = base_name + file_name

with open(file_path, 'r') as file:
    data = json.load(file)

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


total_frames = 0

for person_id, positions in movements.items():
    # Extract frame_ids from positions for each person
    frame_ids = [frame_id for _, _, frame_id in positions]
    if frame_ids:
        max_frame = max(frame_ids)
        if max_frame > total_frames:
            total_frames = max_frame

total_frames += 1  # Since frameId starts from 0


total_frames = max([max(frame_ids) for person_id, positions in movements.items()]) + 1

# Update movements dictionary to include missing frames
for person_id, positions in movements.items():
    existing_frame_ids = set(frame_id for _, _, frame_id in positions)
    missing_frames = set(range(total_frames)) - existing_frame_ids

    for missing_frame in missing_frames:
        # Add a placeholder for missing frames (None for x and y positions)
        movements[person_id].append((None, None, missing_frame))

    # Sort the positions by frameId
    movements[person_id].sort(key=lambda x: x[2])

def interpolate_position(prev_pos, next_pos, prev_frame, next_frame, missing_frame):
    # Linear interpolation for x and y
    x = prev_pos[0] + ((next_pos[0] - prev_pos[0]) * (missing_frame - prev_frame) / (next_frame - prev_frame))
    y = prev_pos[1] + ((next_pos[1] - prev_pos[1]) * (missing_frame - prev_frame) / (next_frame - prev_frame))
    return x, y

for person_id, positions in movements.items():
    for i in range(len(positions)):
        if positions[i][0] is None:  # Missing position
            prev_pos = next_pos = None

            # Find previous known position
            for j in range(i-1, -1, -1):
                if positions[j][0] is not None:
                    prev_pos = positions[j][:2]
                    prev_frame = positions[j][2]
                    break

            # Find next known position
            for k in range(i+1, len(positions)):
                if positions[k][0] is not None:
                    next_pos = positions[k][:2]
                    next_frame = positions[k][2]
                    break

            # Check if both previous and next positions are found
            if prev_pos is not None and next_pos is not None:
                # Interpolate
                interpolated_pos = interpolate_position(prev_pos, next_pos, prev_frame, next_frame, positions[i][2])
                movements[person_id][i] = (interpolated_pos[0], interpolated_pos[1], positions[i][2])
            else:
                # Handle the case where interpolation is not possible
                # Example: Skip interpolation or assign a default value
                pass

import matplotlib.pyplot as plt

for person_id, positions in movements.items():
    # Separate the positions into lists for plotting
    x_positions = [pos[0] for pos in positions if pos[0] is not None]
    y_positions = [pos[1] for pos in positions if pos[1] is not None]
    frame_ids = [pos[2] for pos in positions if pos[0] is not None and pos[1] is not None]

    # Plot the trajectory for each person
    plt.plot(x_positions, y_positions, marker='o', label=person_id)

    # Annotate each point with its frameId
    for x, y, frame_id in zip(x_positions, y_positions, frame_ids):
        plt.annotate(str(frame_id), (x, y))

plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.title(f'Interpolated Movements of People Across Frames in {file_name}')
plt.gca().set_aspect('equal', adjustable='box')
plt.legend()
plt.show()

