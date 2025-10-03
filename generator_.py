
def generate_combinations(total_balls, num_bins):
    """
    Generate all combinations of distributing identical balls into different bins.
    Each bin must have at least 1 ball.
    
    Args:
        total_balls: Total number of identical balls
        num_bins: Number of different bins
    
    Yields:
        Tuple representing the number of balls in each bin
    """
    if num_bins > total_balls:
        return  # Impossible to put at least 1 ball in each bin
    
    if num_bins == 1:
        yield (total_balls,)
        return
    
    # Recursively distribute balls
    for first_bin in range(1, total_balls - num_bins + 2):
        remaining_balls = total_balls - first_bin
        remaining_bins = num_bins - 1
        
        # Generate all combinations for the remaining bins
        for rest in generate_combinations(remaining_balls, remaining_bins):
            yield (first_bin,) + rest

