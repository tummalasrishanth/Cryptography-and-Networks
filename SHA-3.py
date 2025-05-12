import random

# Constants
LANE_SIZE = 64  # bits
TOTAL_LANES = 25
RATE_LANES = 16
CAPACITY_LANES = TOTAL_LANES - RATE_LANES

def random_nonzero_lane():
    # Return a random 64-bit integer that's not zero
    return random.getrandbits(LANE_SIZE) or 1

def simulate_sha3_absorption():
    # Initialize 25 lanes: 16 rate lanes with non-zero, 9 capacity lanes with 0
    state = [random_nonzero_lane() for _ in range(RATE_LANES)] + [0 for _ in range(CAPACITY_LANES)]

    # Track which capacity lanes have become non-zero
    capacity_indices = list(range(RATE_LANES, TOTAL_LANES))
    rounds = 1

    while True:
        # Simulate message block absorption: XOR new non-zero values into rate lanes
        for i in range(RATE_LANES):
            state[i] ^= random_nonzero_lane()

        # Simulate rate lanes affecting capacity (abstracting permutation)
        for rate_val in state[:RATE_LANES]:
            # Randomly "mix" this value into a random capacity lane
            target_idx = random.choice(capacity_indices)
            state[target_idx] ^= rate_val

        # Check if all capacity lanes are now non-zero
        if all(state[i] != 0 for i in capacity_indices):
            break

        rounds += 1

    return rounds

# Run simulation
required_blocks = simulate_sha3_absorption()
print(f"It took {required_blocks} message blocks until all capacity lanes became non-zero.")
