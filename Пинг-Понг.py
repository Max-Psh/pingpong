# -*- coding:utf-8 -*-

from tkinter import *
import random

WIDTH = 900
HEIGHT = 300

PAD_W = 10
PAD_H = 100

BALL_RADIUS = 40

BALL_X_CHANGE = 20

BALL_Y_CHANGE = 0

BALL_SPD_UP = 1.05
BALL_SPD_MAX = 30
INIT_SPD = 10
BALL_SPD_X = 10
BALL_SPD_Y = random.randrange(-10, 10)
right_line_distance = WIDTH - PAD_W
PLAYER_1_SCORE = 0
PLAYER_2_SCORE = 0


def update_score(player):
    global PLAYER_1_SCORE, PLAYER_2_SCORE
    if player == 'right':
        PLAYER_1_SCORE += 1
        c.itemconfig(po_1_text, text=PLAYER_1_SCORE)
    else:
        PLAYER_2_SCORE += 1
        c.itemconfig(po_2_text, text=PLAYER_2_SCORE)


def spawn_ball():
    global BALL_SPD_X, BALL_SPD_Y
    c.coords(BALL, WIDTH / 2 - BALL_RADIUS / 2,
             HEIGHT / 2 - BALL_RADIUS / 2,
             WIDTH / 2 + BALL_RADIUS / 2,
             HEIGHT / 2 + BALL_RADIUS / 2)
    BALL_SPD_X = - BALL_SPD_X / abs(BALL_SPD_X) * INIT_SPD
    BALL_SPD_Y = random.randrange(-10, 10)


def bounce(action):
    global BALL_SPD_X, BALL_SPD_Y
    ball_left, ball_top, ball_right, ball_bot = c.coords(BALL)
    if action == 'strike':
        if ball_right>WIDTH/2:
            if RIGHT_PAD_SPEED > 0:
                BALL_SPD_Y += 2
            elif RIGHT_PAD_SPEED<0:
                BALL_SPD_Y -= 2
        else:
            if LEFT_PAD_SPEED > 0:
                BALL_SPD_Y += 2
            elif LEFT_PAD_SPEED<0:
                BALL_SPD_Y -= 2
        if abs(BALL_SPD_X) < BALL_SPD_MAX:
            BALL_SPD_X *= -(BALL_SPD_UP)
            print(BALL_SPD_Y)
        else:
            BALL_SPD_X = -BALL_SPD_X
    else:
        BALL_SPD_Y = -BALL_SPD_Y


def move_ball():
    ball_left, ball_top, ball_right, ball_bot = c.coords(BALL)
    ball_center = (ball_top + ball_bot) / 2
    right_line_distance = WIDTH-PAD_W

    if ball_left == PAD_W:
        if c.coords(LEFT_PAD)[1] < ball_center < c.coords(LEFT_PAD)[3]:
            bounce('strike')
        else:
            update_score('right')
            spawn_ball()
    if ball_right == right_line_distance:
        if c.coords(RIGHT_PAD)[1] < ball_center < c.coords(RIGHT_PAD)[3]:
            bounce('strike')
        else:
            update_score('left')
            spawn_ball()

    ball_x_speed_new = BALL_SPD_X
    ball_y_speed_new = BALL_SPD_Y

    if ball_bot+ball_y_speed_new >= HEIGHT:
        ball_y_speed_old = ball_y_speed_new
        ball_x_speed_old = ball_x_speed_new
        ball_y_speed_new = HEIGHT-ball_bot
        ball_x_speed_new = ball_x_speed_old*ball_y_speed_new/ball_y_speed_old
        bounce('ricochet')

    elif ball_top + ball_y_speed_new <= 0:
        ball_y_speed_old = ball_y_speed_new
        ball_x_speed_old = ball_x_speed_new
        ball_y_speed_new = 0 - ball_top
        ball_x_speed_new = ball_x_speed_old * ball_y_speed_new / ball_y_speed_old
        bounce('ricochet')

    if ball_right+ball_x_speed_new>=right_line_distance:
        ball_y_speed_old = ball_y_speed_new
        ball_x_speed_old = ball_x_speed_new
        ball_x_speed_new = right_line_distance - ball_right
        ball_y_speed_new = ball_y_speed_old * ball_x_speed_new / ball_x_speed_old

    if ball_left+ball_x_speed_new<=PAD_W:
        ball_y_speed_old = ball_y_speed_new
        ball_x_speed_old = ball_x_speed_new
        ball_x_speed_new = PAD_W - ball_left
        ball_y_speed_new = ball_y_speed_old * ball_x_speed_new / ball_x_speed_old

    c.move(BALL, ball_x_speed_new, ball_y_speed_new)





root = Tk()
root.title("Пинг-понг")

c = Canvas(root, width=WIDTH, height=HEIGHT, background='#008B8B')
c.pack()

c.create_line(PAD_W, 0, PAD_W, HEIGHT, fill="white")

c.create_line(WIDTH - PAD_W, 0, WIDTH - PAD_W, HEIGHT, fill="white")

c.create_line(WIDTH / 2, 0, WIDTH / 2, HEIGHT, fill="white")

BALL = c.create_oval(WIDTH / 2 - BALL_RADIUS / 2,
                     HEIGHT / 2 - BALL_RADIUS / 2,
                     WIDTH / 2 + BALL_RADIUS / 2,
                     HEIGHT / 2 + BALL_RADIUS / 2, fill="#FF4500")
LEFT_PAD = c.create_line(PAD_W / 2, 0, PAD_W / 2, PAD_H, width=PAD_W, fill="#DA70D6")

RIGHT_PAD = c.create_line(WIDTH - PAD_W / 2, 0, WIDTH - PAD_W / 2, PAD_H, width=PAD_W, fill="#DA70D6")

po_1_text = c.create_text(WIDTH - WIDTH / 6, PAD_H / 4, text=PLAYER_1_SCORE,
                          font='Arial 20', fill='aqua')
po_2_text = c.create_text(WIDTH / 6, PAD_H / 4, text=PLAYER_1_SCORE,
                          font='Arial 20', fill='aqua')
PAD_SPEED = 20

LEFT_PAD_SPEED = 0

RIGHT_PAD_SPEED = 0


def move_pads():
    global LEFT_PAD_SPEED, RIGHT_PAD_SPEED
    PADS = {LEFT_PAD: LEFT_PAD_SPEED,
            RIGHT_PAD: RIGHT_PAD_SPEED}
    for pad in PADS:
        c.move(pad, 0, PADS[pad])
        if c.coords(pad)[1] < 0:
            c.move(pad, 0, -c.coords(pad)[1])
        elif c.coords(pad)[3] > HEIGHT:
            c.move(pad, 0, HEIGHT - c.coords(pad)[3])


def main():
    move_ball()
    move_pads()
    root.after(30, main)


c.focus_set()


def movement_handler(event):
    global LEFT_PAD_SPEED, RIGHT_PAD_SPEED
    if event.keycode == 87:
        LEFT_PAD_SPEED = -PAD_SPEED

    if event.keycode == 83:
        LEFT_PAD_SPEED = PAD_SPEED

    if event.keysym == 'Up':
        RIGHT_PAD_SPEED = -PAD_SPEED
    if event.keysym == 'Down':
        RIGHT_PAD_SPEED = PAD_SPEED


c.bind("<KeyPress>", movement_handler)


def stop_pad(event):
    global LEFT_PAD_SPEED, RIGHT_PAD_SPEED
    if event.keysym in 'ws':
        LEFT_PAD_SPEED = 0
    if event.keysym in ("Up", "Down"):
        RIGHT_PAD_SPEED = 0


c.bind("<KeyRelease>", stop_pad)

main()

root.mainloop()
