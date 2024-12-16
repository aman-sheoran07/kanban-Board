def calculate_position(prev_position: float | None, next_position: float | None) -> float:
    """
    Calculate a position between two items for smooth reordering.
    """
    if prev_position is None and next_position is None:
        return 65535  # Middle of a 16-bit integer range

    if prev_position is None:
        return next_position / 2

    if next_position is None:
        return prev_position + 65535

    return (prev_position + next_position) / 2