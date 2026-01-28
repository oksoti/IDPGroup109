from utime import ticks_ms, ticks_diff

class PDLineController:
    def __init__(self, kp, kd, turn_limit=1.0):
        self.kp = kp
        self.kd = kd
        self.turn_limit = turn_limit
        self._prev_error = 0.0
        self._prev_ms = ticks_ms()
        self._has_prev = False
        self._last_turn = 0.0

    # ensure controller does not instruct a turn beyond turn limits
    def turn_clamp(self, x):
        if x > self.turn_limit:
            return self.turn_limit
        if x < -self.turn_limit:
            return -self.turn_limit
        return x

    # resets controller state - useful for restarting line following
    def reset(self):
        self._prev_error = 0.0
        self._prev_ms = ticks_ms()
        self._has_prev = False
        self._last_turn = 0.0

    # inputs line position error and outputs steering/turn correction
    def update(self, error):
        now = ticks_ms()
        dt_ms = ticks_diff(now, self._prev_ms) # computes elapsed time since last update
        self._prev_ms = now # updates stored time for next iteration
        dt = dt_ms / 1000.0 if dt_ms > 0 else 1e-3 # convert milliseconds to seconds

        # error will be None if line is lost (no white tape detected)
        if error is None: 
            search = 0.25 if self._last_turn >= 0 else -0.25 # choose gentle steer direction of +/-0.25
            return self.turn_clamp(search)

        # for first time calling update, set d_error to 0 (no derivation)
        if not self._has_prev:
            d_error = 0.0
            self._has_prev = True
        else: # computes derivative of error function
            d_error = (error - self._prev_error) / dt

        self._prev_error = error
        turn = self.kp * error + self.kd * d_error # fundamental PD logic
        turn = self.turn_clamp(turn)
        self._last_turn = turn
        return turn
