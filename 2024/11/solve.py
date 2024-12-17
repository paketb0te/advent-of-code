# Import required modules
import sys

# Read the input from stdin and split it into a list of strings
stones = sys.stdin.read().split()

# Convert each string to an integer
stones = [int(stone) for stone in stones]

# Define the number of blinks
NUM_BLINKS = 25

# Iterate for the specified number of blinks
for _ in range(NUM_BLINKS):
    # Create a new list to store the updated stones
    new_stones = []

    # Iterate over each stone
    for stone in stones:
        # If the stone is 0, replace it with 1
        if stone == 0:
            new_stones.append(1)
        # If the number of digits in the stone is even
        elif len(str(stone)) % 2 == 0:
            # Split the digits into left and right halves
            mid = len(str(stone)) // 2
            left = int(str(stone)[:mid])
            right = int(str(stone)[mid:])
            # Append the left and right stones to the new list
            new_stones.append(left)
            new_stones.append(right)
        # If none of the above conditions are met
        else:
            # Multiply the stone by 2024 and append it to the new list
            new_stones.append(stone * 2024)

    # Update the stones list with the new stones
    stones = new_stones

# Print the number of stones after the specified number of blinks
print(len(stones))
