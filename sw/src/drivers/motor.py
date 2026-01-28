
def motor_clamp(x, lo, hi):
    return lo if x < lo else hi if x > hi else x

def error_to_motor_speeds(turn, base=0.5, max_speed=1.0, min_speed=0.0):
    '''
    Convert a turn command into left/right motor speeds.

    Parameters:
    turn: float, typically in [-1, 1] (from your PD controller)
    base: float, forward speed baseline (0..1)
    max_speed: float, cap for motor command
    min_speed: float, minimum allowed (0 means don't reverse)

    Returns:
    (left, right) floats in [min_speed, max_speed]
    '''
    left = base - turn
    right = base + turn

    left = motor_clamp(left, min_speed, max_speed)
    right = motor_clamp(right, min_speed, max_speed)
    return left, right