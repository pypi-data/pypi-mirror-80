"""Timer"""

import time


def get_elasped_minutes_since_first_keypress(start_time):
    """Get time elapsed since initial keypress. This is required to calculate
    speed.

    Args:
        start_time (float): The time when user starts typing
        the sample text.

    Returns:
        float: Time elasped since start of typing session till calling
            this function.
    """
    return time.time() - start_time
