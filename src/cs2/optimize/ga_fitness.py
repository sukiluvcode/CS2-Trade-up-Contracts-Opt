def container_possibilities(containers: dict[str, tuple]):
    """Get product container possibilities from all used containers in the trade up contract.
    Args:
        containers (dict[str, tuple]): Dictionary of container names and their # used weapons and # next rarity weapons."""
    summation = sum(v[0] * v[1] for v in containers.values())
    return {k: v[0] / summation for k, v in containers.items()}

def weapon_float(wear_floats: list[float], min_float: float, max_float: float):
    """Get the float of output weapon"""
    avg = sum(wear_floats) / len(wear_floats)
    output_float = min_float + (max_float - min_float) * avg
    return output_float
