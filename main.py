from graphics import Canvas
import random
import time

# Size
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
GAME_DURATION = 15 

# Color
GB_DARKEST = "#0f380f"
GB_DARK = "#306230"
GB_LIGHT = "#8bac0f"
GB_LIGHTEST = "#9bbc0f"

def main():
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    
    # Home Page
    show_start_screen(canvas)
    
    # Main 
    run_game(canvas)

def show_start_screen(canvas):
    # Outside border color
    canvas.set_canvas_background_color("white")
    
    # screen background
    border_rect = canvas.create_rectangle(20, 20, CANVAS_WIDTH - 20, CANVAS_HEIGHT - 20)
    canvas.set_color(border_rect, "black")

    # screen background star
    for _ in range(200):
        sx = random.randint(0, CANVAS_WIDTH)
        sy = random.randint(0, CANVAS_HEIGHT)
        star = canvas.create_oval(sx, sy, sx + 2, sy + 2)
        canvas.set_color(star, "white")
    
    # Title
    title_x = CANVAS_WIDTH / 2 - 240 
    title_y = CANVAS_HEIGHT / 2 - 120
    
    title = canvas.create_text(title_x, title_y, "CITY NIGHT LIGHTS", font_size = 50)
    canvas.set_color(title, "white") 

    # Start Button
    btn_w, btn_h = 240, 60
    btn_x = CANVAS_WIDTH / 2 - btn_w / 2
    btn_y = CANVAS_HEIGHT / 2 + 50
    
    button_rect = canvas.create_rectangle(btn_x, btn_y, btn_x + btn_w, btn_y + btn_h)
    canvas.set_color(button_rect, "#306230") 
    button_text = canvas.create_text(btn_x + 45, btn_y + 15, "START GAME", font_size = 20)
    canvas.set_color(button_text, "white")

    # Guide
    title_x = CANVAS_WIDTH / 2 - 260 
    title_y = CANVAS_HEIGHT / 4 * 3
    
    title = canvas.create_text(title_x, title_y, "Click how many light windows you can!", font_size = 30)
    canvas.set_color(title, "white") 

    # Click Button
    while True:
        click = canvas.get_last_click()
        if click is not None:
            cx, cy = click[0], click[1]
            if btn_x <= cx <= btn_x + btn_w and btn_y <= cy <= btn_y + btn_h:
                canvas.clear()
                break
        time.sleep(0.1)

# Game Logic
def run_game(canvas):
    canvas.set_canvas_background_color("#0b132b") 
    
    # Game Background
    for _ in range(20):
        sx = random.randint(0, CANVAS_WIDTH)
        sy = random.randint(0, int(CANVAS_HEIGHT * 0.5))
        star = canvas.create_oval(sx, sy, sx + 2, sy + 2)
        canvas.set_color(star, "white")

    windows = []
    generate_cityscape(canvas, windows)

    score = 0
    score_text = canvas.create_text(30, 30, "Score: 0")
    canvas.set_color(score_text, "#ffffff")
    
    timer_text = canvas.create_text(CANVAS_WIDTH - 180, 30, "Time Left: 15s")
    canvas.set_color(timer_text, "#ff6b6b")

    start_time = time.time()

    # Game Logic
    while True:
        elapsed_time = time.time() - start_time
        time_left = int(GAME_DURATION - elapsed_time)
        canvas.change_text(timer_text, "Time Left: " + str(max(0, time_left)) + "s")
        
        if time_left <= 0:
            break

        # Random light the windows
        if random.random() < 0.08:
            dark_windows = [w for w in windows if not w["is_bright"]]
            if dark_windows:
                chosen_window = random.choice(dark_windows)
                chosen_window["is_bright"] = True
                chosen_window["duration"] = random.uniform(1.5, 3.5)
                chosen_window["bright_start_time"] = time.time()
                canvas.set_color(chosen_window["shape"], "#ffd166") 

        # check time
        current_now = time.time()
        for w in windows:
            if w["is_bright"] and current_now - w["bright_start_time"] >= w["duration"]:
                w["is_bright"] = False
                canvas.set_color(w["shape"], "#1f2438") 

        # player click
        click = canvas.get_last_click()
        if click is not None:
            cx, cy = click[0], click[1]
            for w in windows:
                if w["is_bright"]:
                    lx = canvas.get_left_x(w["shape"])
                    ty = canvas.get_top_y(w["shape"])
                    if lx <= cx <= lx + 20 and ty <= cy <= ty + 30:
                        score += 1
                        canvas.change_text(score_text, "Score: " + str(score))
                        w["is_bright"] = False
                        canvas.set_color(w["shape"], "#1f2438")
                        break 

        time.sleep(0.05)

    # calculate score
    show_end_screen(canvas, score)

def show_end_screen(canvas, score):
    canvas.clear()
    canvas.set_canvas_background_color(GB_DARKEST)
    msg = canvas.create_text(CANVAS_WIDTH / 2 - 120, CANVAS_HEIGHT / 2 - 50, "Your Result!", font_size = 50)
    canvas.set_color(msg, GB_LIGHTEST)
    
    res = canvas.create_text(CANVAS_WIDTH / 2 - 60, CANVAS_HEIGHT / 2 + 20, "FINAL SCORE: " + str(score), font_size = 20)
    canvas.set_color(res, "white")

def generate_cityscape(canvas, windows):
    current_x = 20
    while current_x < CANVAS_WIDTH - 40:
        bw = random.randint(100, 160)
        bh = random.randint(250, 450)
        bx, by = current_x, CANVAS_HEIGHT - bh
        
        b_shape = canvas.create_rectangle(bx, by, bx + bw, CANVAS_HEIGHT)
        canvas.set_color(b_shape, "#1c2541")
        
        for wx in range(bx + 15, bx + bw - 20, 35):
            for wy in range(by + 20, CANVAS_HEIGHT - 50, 50):
                w_shape = canvas.create_rectangle(wx, wy, wx + 20, wy + 30)
                canvas.set_color(w_shape, "#1f2438")
                windows.append({"shape": w_shape, "is_bright": False, "bright_start_time": 0, "duration": 0})
        current_x += bw + 15

if __name__ == '__main__':
    main()
