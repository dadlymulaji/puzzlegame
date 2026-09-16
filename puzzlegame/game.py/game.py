# FOOTBALL BRICK BREAKER
# --------------------------------------------------------------
# NCEA Level 3 Digital Technologies
#
# The player controls a moving train/platform.
# The ball bounces around the screen and breaks bricks.
#
# When all the bricks are broken, the goal opens.
# The player must then get the ball into the goal to
# complete the level.
#
# Each level becomes harder by adding more bricks and
# increasing the speed of the ball.
# --------------------------------------------------------------

# ==============================================================
# 1. IMPORTS
# ==============================================================

# Tkinter is used to create the graphical interface.
import tkinter as tk

# Random is used to make power-ups appear randomly.
import random


# ==============================================================
# 2. GAME SETTINGS
# ==============================================================

WIDTH = 600
HEIGHT = 650

# Starting number of lives.
STARTING_LIVES = 3

# Starting ball speed.
STARTING_SPEED = 5


# ==============================================================
# 3. GAME VARIABLES
# ==============================================================

score = 0
lives = STARTING_LIVES
level = 1

# These keep track of the direction of the ball.
ball_dx = STARTING_SPEED
ball_dy = -STARTING_SPEED

# True means the game is currently running.
game_running = False

# The goal is locked until all bricks are destroyed.
goal_open = False

# Used to stop the game loop being started multiple times.
game_over = False

# Lists are used to store objects in the game.
bricks = []
powerups = []


# ==============================================================
# 4. CREATE THE MAIN WINDOW
# ==============================================================

root = tk.Tk()

root.title("Football Brick Breaker")
root.geometry("650x780")
root.resizable(False, False)


# ==============================================================
# 5. TITLE
# ==============================================================

title = tk.Label(
    root,
    text="⚽ FOOTBALL BRICK BREAKER",
    font=("Arial", 22, "bold")
)

title.pack(pady=8)


# ==============================================================
# 6. INFORMATION DISPLAY
# ==============================================================

info_label = tk.Label(
    root,
    text="Score: 0     Lives: 3     Level: 1",
    font=("Arial", 14, "bold")
)

info_label.pack(pady=5)


# ==============================================================
# 7. GAME CANVAS
# ==============================================================

# The Canvas is where all of the game objects are displayed.

canvas = tk.Canvas(
    root,
    width=WIDTH,
    height=HEIGHT,
    bg="darkgreen"
)

canvas.pack()


# ==============================================================
# 8. CREATE THE PLAYER
# ==============================================================

# The player is represented by a blue platform.

player = canvas.create_rectangle(
    260, 570,
    340, 590,
    fill="blue"
)


# ==============================================================
# 9. CREATE THE BALL
# ==============================================================

ball = canvas.create_oval(
    290, 530,
    310, 550,
    fill="white"
)


# ==============================================================
# 10. CREATE THE GOAL
# ==============================================================

# The goal is hidden at the beginning.

goal = canvas.create_rectangle(
    240, 600,
    360, 635,
    fill="gold",
    outline="white",
    width=3
)

goal_text = canvas.create_text(
    300, 618,
    text="GOAL",
    font=("Arial", 16, "bold"),
    fill="black"
)

# Hide the goal until the bricks are destroyed.
canvas.itemconfig(goal, state="hidden")
canvas.itemconfig(goal_text, state="hidden")


# ==============================================================
# 11. UPDATE THE INFORMATION
# ==============================================================

def update_info():
    """
    Updates the score, lives and level shown at the top.
    """

    info_label.config(
        text=f"Score: {score}     Lives: {lives}     Level: {level}"
    )


# ==============================================================
# 12. CREATE BRICKS
# ==============================================================

def create_bricks():
    """
    Creates the brick layout for the current level.

    Higher levels contain more rows and therefore take
    longer to complete.
    """

    # Remove any old bricks.
    for brick in bricks:
        canvas.delete(brick["id"])

    bricks.clear()

    # Number of rows increases with each level.
    rows = 2 + level

    # Maximum of 7 rows.
    if rows > 7:
        rows = 7

    columns = 7

    brick_width = 65
    brick_height = 25

    gap = 8

    start_x = 40
    start_y = 50

    for row in range(rows):

        for column in range(columns):

            x1 = start_x + column * (brick_width + gap)
            y1 = start_y + row * (brick_height + gap)

            x2 = x1 + brick_width
            y2 = y1 + brick_height

            # Different levels have stronger bricks.
            strength = 1

            if level >= 3 and row < 2:
                strength = 2

            brick_id = canvas.create_rectangle(
                x1, y1,
                x2, y2,
                fill="red",
                outline="white"
            )

            # Dictionaries allow us to store information
            # about each brick.
            bricks.append({
                "id": brick_id,
                "strength": strength
            })


# ==============================================================
# 13. MOVE THE PLAYER
# ==============================================================

def move_player(event):
    """
    Moves the player's platform using the arrow keys.
    """

    if not game_running:
        return

    # Get the player's current position.
    position = canvas.coords(player)

    # Move left.
    if event.keysym == "Left":

        if position[0] > 0:
            canvas.move(player, -35, 0)

    # Move right.
    elif event.keysym == "Right":

        if position[2] < WIDTH:
            canvas.move(player, 35, 0)


# ==============================================================
# 14. RESET BALL
# ==============================================================

def reset_ball():
    """
    Places the ball back in its starting position.
    """

    global ball_dx
    global ball_dy

    canvas.coords(
        ball,
        290, 530,
        310, 550
    )

    # Reset the direction.
    ball_dx = STARTING_SPEED + level - 1
    ball_dy = -(STARTING_SPEED + level - 1)


# ==============================================================
# 15. CHECK BRICK COLLISIONS
# ==============================================================

def check_brick_collision():

    global score

    ball_position = canvas.coords(ball)

    for brick in bricks[:]:

        brick_position = canvas.coords(brick["id"])

        # Check whether the ball overlaps the brick.
        collision = (
            ball_position[2] >= brick_position[0]
            and
            ball_position[0] <= brick_position[2]
            and
            ball_position[3] >= brick_position[1]
            and
            ball_position[1] <= brick_position[3]
        )

        if collision:

            # Strong bricks need to be hit twice.
            brick["strength"] -= 1

            # Bounce the ball.
            global ball_dy
            ball_dy = -ball_dy

            if brick["strength"] <= 0:

                # Delete the brick.
                canvas.delete(brick["id"])

                # Remove it from the list.
                bricks.remove(brick)

                # Give the player points.
                score += 10

                # There is a chance of spawning a power-up.
                create_powerup(
                    (brick_position[0] + brick_position[2]) / 2,
                    (brick_position[1] + brick_position[3]) / 2
                )

            else:

                # Change the colour to show the brick
                # has been damaged.
                canvas.itemconfig(
                    brick["id"],
                    fill="orange"
                )

            return


# ==============================================================
# 16. CREATE POWER-UP
# ==============================================================

def create_powerup(x, y):
    """
    Creates a power-up with a random type.
    """

    # Only a 20% chance of creating a power-up.
    if random.randint(1, 5) != 1:
        return

    # Randomly choose a power-up.
    power_type = random.choice([
        "wide",
        "life",
        "slow"
    ])

    powerup = canvas.create_oval(
        x - 10,
        y - 10,
        x + 10,
        y + 10,
        fill="yellow"
    )

    powerups.append({
        "id": powerup,
        "type": power_type
    })


# ==============================================================
# 17. MOVE POWER-UPS
# ==============================================================

def move_powerups():

    global lives

    player_position = canvas.coords(player)

    for powerup in powerups[:]:

        # Move the power-up down.
        canvas.move(powerup["id"], 0, 4)

        position = canvas.coords(powerup["id"])

        # Check if the player catches it.
        caught = (
            position[2] >= player_position[0]
            and
            position[0] <= player_position[2]
            and
            position[3] >= player_position[1]
            and
            position[1] <= player_position[3]
        )

        if caught:

            power_type = powerup["type"]

            # Remove the power-up.
            canvas.delete(powerup["id"])
            powerups.remove(powerup)

            # -------------------------------
            # Wide platform power-up
            # -------------------------------

            if power_type == "wide":

                current = canvas.coords(player)

                canvas.coords(
                    player,
                    current[0] - 25,
                    current[1],
                    current[2] + 25,
                    current[3]
                )

            # -------------------------------
            # Extra life power-up
            # -------------------------------

            elif power_type == "life":

                lives += 1

            # -------------------------------
            # Slow ball power-up
            # -------------------------------

            elif power_type == "slow":

                global ball_dx
                global ball_dy

                ball_dx *= 0.7
                ball_dy *= 0.7

        # Delete power-ups that leave the screen.
        elif position[1] > HEIGHT:

            canvas.delete(powerup["id"])
            powerups.remove(powerup)


# ==============================================================
# 18. OPEN THE GOAL
# ==============================================================

def open_goal():

    global goal_open

    goal_open = True

    canvas.itemconfig(
        goal,
        state="normal"
    )

    canvas.itemconfig(
        goal_text,
        state="normal"
    )


# ==============================================================
# 19. CHECK GOAL
# ==============================================================

def check_goal():

    if not goal_open:
        return False

    ball_position = canvas.coords(ball)

    goal_position = canvas.coords(goal)

    # Check if the ball is inside the goal.
    return (
        ball_position[2] >= goal_position[0]
        and
        ball_position[0] <= goal_position[2]
        and
        ball_position[3] >= goal_position[1]
        and
        ball_position[1] <= goal_position[3]
    )


# ==============================================================
# 20. NEXT LEVEL
# ==============================================================

def next_level():

    global level
    global goal_open

    level += 1

    goal_open = False

    # Clear power-ups.
    for powerup in powerups:
        canvas.delete(powerup["id"])

    powerups.clear()

    # Hide the goal.
    canvas.itemconfig(
        goal,
        state="hidden"
    )

    canvas.itemconfig(
        goal_text,
        state="hidden"
    )

    # Move player back to the centre.
    canvas.coords(
        player,
        260, 570,
        340, 590
    )

    # Create the new level.
    create_bricks()

    reset_ball()

    update_info()


# ==============================================================
# 21. LOSE A LIFE
# ==============================================================

def lose_life():

    global lives
    global game_running

    lives -= 1

    if lives <= 0:

        game_running = False

        canvas.create_text(
            WIDTH / 2,
            HEIGHT / 2,
            text="GAME OVER",
            fill="white",
            font=("Arial", 35, "bold")
        )

    else:

        reset_ball()


# ==============================================================
# 22. MOVE THE BALL
# ==============================================================

def move_ball():

    global ball_dx
    global ball_dy
    global game_running

    if not game_running:
        return

    # Move the ball.
    canvas.move(
        ball,
        ball_dx,
        ball_dy
    )

    position = canvas.coords(ball)

    # ----------------------------------------------------------
    # LEFT AND RIGHT WALL
    # ----------------------------------------------------------

    if position[0] <= 0 or position[2] >= WIDTH:

        ball_dx = -ball_dx


    # ----------------------------------------------------------
    # TOP WALL
    # ----------------------------------------------------------

    if position[1] <= 0:

        ball_dy = -ball_dy


    # ----------------------------------------------------------
    # BRICKS
    # ----------------------------------------------------------

    check_brick_collision()


    # ----------------------------------------------------------
    # PLAYER
    # ----------------------------------------------------------

    player_position = canvas.coords(player)

    if (
        position[2] >= player_position[0]
        and
        position[0] <= player_position[2]
        and
        position[3] >= player_position[1]
        and
        position[1] <= player_position[3]
        and
        ball_dy > 0
    ):

        # Bounce the ball upwards.
        ball_dy = -abs(ball_dy)

        # Change the angle depending on where the ball
        # hits the platform.
        player_middle = (
            player_position[0] +
            player_position[2]
        ) / 2

        ball_middle = (
            position[0] +
            position[2]
        ) / 2

        difference = ball_middle - player_middle

        ball_dx += difference * 0.05


    # ----------------------------------------------------------
    # ALL BRICKS DESTROYED
    # ----------------------------------------------------------

    if len(bricks) == 0 and not goal_open:

        open_goal()


    # ----------------------------------------------------------
    # GOAL
    # ----------------------------------------------------------

    if check_goal():

        next_level()


    # ----------------------------------------------------------
    # BALL MISSED
    # ----------------------------------------------------------

    if position[1] > HEIGHT:

        lose_life()


    # Move power-ups.
    move_powerups()

    # Update the information.
    update_info()

    # Run the game again after 20 milliseconds.
    root.after(20, move_ball)


# ==============================================================
# 23. START GAME
# ==============================================================

def start_game():

    global game_running
    global game_over

    game_running = True
    game_over = False

    create_bricks()
    reset_ball()
    update_info()

    move_ball()


# ==============================================================
# 24. RESTART GAME
# ==============================================================

def restart_game():

    global score
    global lives
    global level
    global game_running
    global goal_open

    score = 0
    lives = STARTING_LIVES
    level = 1

    game_running = True
    goal_open = False

    # Remove everything from the Canvas.
    canvas.delete("all")

    # Re-create the player.
    global player

    player = canvas.create_rectangle(
        260, 570,
        340, 590,
        fill="blue"
    )

    # Re-create the ball.
    global ball

    ball = canvas.create_oval(
        290, 530,
        310, 550,
        fill="white"
    )

    # Re-create the goal.
    global goal
    global goal_text

    goal = canvas.create_rectangle(
        240, 600,
        360, 635,
        fill="gold",
        outline="white",
        width=3
    )

    goal_text = canvas.create_text(
        300, 618,
        text="GOAL",
        font=("Arial", 16, "bold"),
        fill="black"
    )

    canvas.itemconfig(goal, state="hidden")
    canvas.itemconfig(goal_text, state="hidden")

    create_bricks()
    reset_ball()
    update_info()

    move_ball()


# ==============================================================
# 25. BUTTONS
# ==============================================================

button_frame = tk.Frame(root)

button_frame.pack(pady=10)


start_button = tk.Button(
    button_frame,
    text="Start Game",
    font=("Arial", 12),
    command=start_game
)

start_button.pack(side="left", padx=5)


restart_button = tk.Button(
    button_frame,
    text="Restart",
    font=("Arial", 12),
    command=restart_game
)

restart_button.pack(side="left", padx=5)


quit_button = tk.Button(
    button_frame,
    text="Quit",
    font=("Arial", 12),
    command=root.destroy
)

quit_button.pack(side="left", padx=5)


# ==============================================================
# 26. KEYBOARD CONTROLS
# ==============================================================

# The left and right arrow keys control the player.

root.bind("<Left>", move_player)
root.bind("<Right>", move_player)


# ==============================================================
# 27. CREATE THE FIRST LEVEL
# ==============================================================

create_bricks()
reset_ball()
update_info()


# ==============================================================
# 28. START THE PROGRAM
# ==============================================================

# mainloop keeps the window running.

root.mainloop()