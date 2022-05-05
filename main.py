from turtle import *
from pprint import pprint
import random
import scoreboard

# --- Screen where to draw
screen = Screen()
screen.bgcolor("black")
screen.setup(1400, 1200)
screen.register_shape("brick", ((-10, -30), (-10, 30), (10, 30), (10, -30)))

# --- Scoreboard
scoreboard = scoreboard.Scoreboard()

# --- Turtles
tim = Turtle()
tim.hideturtle()
tim.penup()
tim.pencolor("white")
tim.width(16)
tim.speed(0)

brick = Turtle()
brick.shape("brick")
brick.color("white")
brick.penup()
brick.speed(0)

ball = Turtle()
ball.goto(x=random.randint(-3, 3)*100, y=0)
ball.penup()
ball.shape("circle")
ball.color("white")
ball.setheading(135)

# Draw game area edges
tim.goto(x=400, y=-592)
tim.setheading(90)
tim.pendown()
tim.goto(x=400, y=592)
tim.left(90)
tim.goto(x=-400, y=592)
tim.left(90)
tim.goto(x=-400, y=-592)
tim.penup()

# Draw paddle
brick.goto(x=-40, y=-550)
paddle = brick.clone()

# Creates 48 bricks, 12 per row, last 12 in list are at bottom
all_bricks = {}
for i in range(4):
    all_bricks[f"row_{i}"] = []

for row_index in range(4):
    brick.goto(x=-364, y=480 - row_index * 44)
    for brick_index in range(12):
        all_bricks[f"row_{row_index}"].append(brick.clone())
        brick.forward(66)
brick.goto(800, -300)


def paddle_left():
    paddle.backward(50)


def paddle_right():
    paddle.forward(50)


def turn_right():
    ball.right(90)


def turn_left():
    ball.left(90)


def check_paddle_hit():
    if ball.heading() == 225 and ball.distance(paddle) < 50:
        turn_right()
    elif ball.heading() == 315 and ball.distance(paddle) < 50:
        turn_left()


def check_horizontal_collision():
    """Returns true if collision in horizontal plane happens and moves the brick that was collided with."""
    for row, bricks in all_bricks.items():
        for item in bricks:
            # noinspection PyTypeChecker
            if ball.distance(item) < 22 or ball.distance(item.xcor() + 10, item.ycor()) < 22\
                    or ball.distance(item.xcor() - 10, item.ycor()) < 22:
                item.goto(800, -300)
                scoreboard.update_score()
                return True


def check_vertical_collision():
    """Returns true if collision in vertical plane happens and moves the brick that was collided with."""
    for row, bricks in all_bricks.items():
        for item in bricks:
            # noinspection PyTypeChecker
            if ball.distance(item) < 22 or ball.distance(item.xcor(), item.ycor() + 5) < 22 \
                    or ball.distance(item.xcor(), item.ycor() - 5) < 22:
                item.goto(800, -300)
                scoreboard.update_score()
                return True


# TODO Restrict paddle movement in the game area

game_is_on = True
while game_is_on:
    screen.onkey(paddle_left, "Left")
    screen.onkey(paddle_right, "Right")
    screen.listen()

    ball.forward(6)

    if -540 < ball.ycor() < 550:
        check_paddle_hit()

# Make dictionaries for the coordinates to check for ball collision with bricks
    brick_y_coordinates = [480, 436, 392, 348]  # 44 between them
    brick_plane_rad = 9
    brick_plane_ranges = {}
    for y_cor in brick_y_coordinates:
        brick_plane_ranges[f"brick_row_{brick_y_coordinates.index(y_cor)}"] = [y_cor - brick_plane_rad, y_cor + brick_plane_rad]

    empty_planes = [492, 448, 404, 360, 316]
    empty_plane_rad = 14
    empty_plane_ranges = {}
    for y_cor in empty_planes:
        empty_plane_ranges[f"plane_{empty_planes.index(y_cor)}"] = [y_cor - empty_plane_rad, y_cor + empty_plane_rad]


# Checking for collisions
    # Collisions with the bricks left and right side
    for nro in range(len(brick_plane_ranges)):
        if brick_plane_ranges[f"brick_row_{nro}"][0] < ball.ycor() < brick_plane_ranges[f"brick_row_{nro}"][1]:
            if check_vertical_collision():
                print("ver collision")
                if ball.heading() == 45 or ball.heading() == 225:
                    turn_right()
                    print("vertical collision and turn right")
                elif ball.heading() == 135 or ball.heading() == 315:
                    turn_left()
                    print("vertical collision and turn left")

    # Collisions with the bricks top and bottom side
    for nro in range(len(empty_plane_ranges)):
        if empty_plane_ranges[f"plane_{nro}"][0] < ball.ycor() < empty_plane_ranges[f"plane_{nro}"][1]:
            if check_horizontal_collision():
                print("hor collision")
                if ball.heading() == 45 or ball.heading() == 225:
                    turn_right()
                    print("horizontal collision and turn right")
                elif ball.heading() == 135 or ball.heading() == 315:
                    turn_left()
                    print("horizontal collision and turn left")


# Hitting the walls
    corr = 16
    if ball.heading() == 45 and ball.xcor() >= 400 - corr:
        turn_left()
    if ball.heading() == 45 and ball.ycor() >= 592 - corr:
        turn_right()
    if ball.heading() == 135 and ball.xcor() <= -400 + corr:
        turn_right()
    if ball.heading() == 135 and ball.ycor() >= 592 - corr:
        turn_left()
    if ball.heading() == 225 and ball.xcor() <= -400 + corr:
        turn_left()
    if ball.heading() == 315 and ball.xcor() >= 400 - corr:
        turn_right()

# TODO 9 Can you make a "loading" screen while tim draws the game?

# Lose condition
    if ball.ycor() <= -600:
        print("LOSE THE GAME")
        game_is_on = False
        if scoreboard.score > scoreboard.hi_score:
            scoreboard.update_high_score()

exitonclick()
mainloop()
