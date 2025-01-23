metrics = [
    [10, 20, 30],
    [12, 22, 32],
    [15, 25, 35]
]

if not metrics:
    averages = []
else:
    num_positions = len(metrics[0])  # Assumes all inner lists have the same length
    averages = [sum(metrics[i][j] for i in range(len(metrics))) / len(metrics) for j in range(num_positions)]

print(f"The averages for each position are: {averages}")