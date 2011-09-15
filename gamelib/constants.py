MAX_FRAME_RATE = 60
MIN_FRAME_RATE = 30
TIME_STEP = (1.0 / MAX_FRAME_RATE)
TIME_STEP_SQ = TIME_STEP * TIME_STEP
MAX_CYCLES_PER_FRAME = (MAX_FRAME_RATE / MIN_FRAME_RATE)

# RESOLUTION
WIDTH = 640
HEIGHT = 400

# DIFFICULTY
EASY, NORMAL, HARD, WTF = range(4)

