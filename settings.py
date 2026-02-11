SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

SCREEN_RES = (SCREEN_WIDTH, SCREEN_HEIGHT)
GAME_BG = (30, 120, 30)
FPS = 60
TRACKS = {
    "track_1": {
        "image": "track_1.png",
        "collision": "track_1_collision.png",
        "start_pos": (840, 1817),
        "start_angle": 0,
        "laps": 3,
        "checkpoints": [
            (990, 1770), 
            (1670, 1093), 
            (1236, 442), 
            (480, 747)
        ],
        "checkpoint_radius": 80  
    },
    "track_2": {
        "image": "track_2.png",
        "start_pos": (1200, 300),
        "start_angle": 45
    }
}
