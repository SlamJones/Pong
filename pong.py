#!/usr/bin/env python3

import math
import os
import time
import random

from graphics import *


settings = {
    "frame_rate": 30,
    "ball_radius": 8,
    "ball_speed": 8,
    "ball_speed_max": 30,
    "paddle_length": 100,
    "paddle_speed": 6,
    "paddle_speed_max": 28,
    "paddle_inset": 50,
    "window_x": 1920,
    "window_y": 980,
    "bg_color": "black",
    "fg_color": "white",
    "button_height": 50,
    "button_width": 200,
    "demo_mode": False,
    "color_shift": 10,
}

levels = [
    {"bg_color": "black", "fg_color": "white"},
    {"bg_color": "blue4", "fg_color": "white"},
    {"bg_color": "red4", "fg_color": "white"},
    {"bg_color": "green4", "fg_color": "white"},
    {"bg_color": "purple4", "fg_color": "white"},
    {"bg_color": "cyan4", "fg_color": "white"},
    {"bg_color": "firebrick4", "fg_color": "white"},
    {"bg_color": "cornsilk4", "fg_color": "white"},
    {"bg_color": "orange4", "fg_color": "white"},
    {"bg_color": "orchid4", "fg_color": "white"},
    {"bg_color": "sienna4", "fg_color": "white"},
]
    


def init():
    clear()
    print("Welcome!\n")
    
    
def clear():
    os.system("clear")
    
    
def main():
    ##
    win = GraphWin("Pong",settings["window_x"],settings["window_y"],autoflush=False)
    win.setBackground(settings["bg_color"])
    ##
    ##    
    draw_title(win)
    draw_menu(win)
    ##
    ##
    win.close()
    
    
def draw_title(win):
    text_title = "PONG"
    text_border = "----------"
    text_bottom = "SlamJones 2022"
    
    to_draw = []
    
    midX = settings["window_x"]/2
    midY = settings["window_y"]/2
    
    rows = 3
    rowsY = calc_rowsY(win,rows)
    
    title = Text(Point(midX,rowsY[0]),text_title)
    title.setSize(36)
    border = Text(Point(midX,rowsY[1]),text_border)
    border.setSize(36)
    bottom = Text(Point(midX,rowsY[2]),text_bottom)
    border.setSize(24)
    
    to_draw.append(title)
    to_draw.append(border)
    to_draw.append(bottom)
    
    for item in to_draw:
        item.setTextColor(settings["fg_color"])
        item.setStyle("bold")
        item.draw(win)
    update()
    ####
        
    win.getMouse()
    ####
    for item in to_draw:
        item.undraw()
    win.update()
        
        
def draw_menu(win):
    text_title = "PONG"
    button_names = ["Start","Demo","Settings","Quit"]
    buttons = []
    
    to_draw = []
    
    midX = settings["window_x"]/2
    rows = len(button_names)+1
    rowsY = calc_rowsY(win,rows)
    
    title = Text(Point(midX,rowsY[0]),text_title)
    title.setSize(36)
    title.setTextColor(settings["fg_color"])
    to_draw.append(title)
    
    count = 1
    for b in button_names:
        button_center_X = midX
        button_center_Y = rowsY[count]
        button_text = button_names[count-1]
        button_P1x = (
            (button_center_X-settings["button_width"]/2))
        button_P1y = (
            (button_center_Y-settings["button_height"]/2))
        button_P2x = (
            (button_center_X+settings["button_width"]/2))
        button_P2y = (
            (button_center_Y+settings["button_height"]/2))
        
        button_rect = Rectangle(Point(button_P1x,button_P1y),Point(button_P2x,button_P2y))
        button_rect.setFill(settings["bg_color"])
        button_rect.setOutline(settings["fg_color"])
        button_rect.setWidth(3)
        to_draw.append(button_rect)
        
        button_text = Text(Point(button_center_X,button_center_Y),button_text)
        button_text.setTextColor(settings["fg_color"])
        to_draw.append(button_text)
        buttons.append([button_rect,button_text.getText()])
        
        count += 1
    
    for item in to_draw:
        item.draw(win)
    win.update()
    ####
    choice = ""
    
    while choice != "Quit":
        click = win.getMouse()
        click_x = click.getX()
        click_y = click.getY()

        for button in buttons:
            button_P1 = button[0].getP1()
            button_P2 = button[0].getP2()
            if click_x >= button_P1.getX() and click_x <= button_P2.getX() and click_y >= button_P1.getY() and click_y <= button_P2.getY():
                print("Clicked on {}".format(button[1]))
                choice = button[1]
        if choice == "Start":
            for item in to_draw:
                item.undraw()
            win.update()

            draw_game(win)
            for item in to_draw:
                item.draw(win)
            win.update()
        elif choice == "Quit":
            break
        elif choice == "Demo":
            settings["demo_mode"] = True
            for item in to_draw:
                item.undraw()
            win.update()

            draw_game(win)
            for item in to_draw:
                item.draw(win)
            win.update()
            settings["demo_mode"] = False
        else:
            pass
    
    
def draw_game(win):
    to_draw = []
    
    centerX = settings["window_x"]/2
    centerY = settings["window_y"]/2
    centerline = Line(Point(centerX,0),Point(centerX,settings["window_y"]))
    centerline.setFill(settings["fg_color"])
    centerline.setOutline(settings["fg_color"])
    centerline.setWidth(5)
    to_draw.append(centerline)
    
    ball = Circle(Point(centerX,centerY),settings["ball_radius"])
    ball.setFill(settings["fg_color"])
    ball.setOutline(settings["fg_color"])
    to_draw.append(ball)
    
    paddles = []
    left_paddle = Line(
        Point(settings["paddle_inset"],
              (settings["window_y"]/2-settings["paddle_length"]/2)),
        Point(settings["paddle_inset"],
              (settings["window_y"]/2+settings["paddle_length"]/2)),
    )
    paddles.append(left_paddle)
    right_paddle = Line(
        Point(settings["window_x"]-settings["paddle_inset"],
              (settings["window_y"]/2-settings["paddle_length"]/2)),
        Point(settings["window_x"]-settings["paddle_inset"],
              (settings["window_y"]/2+settings["paddle_length"]/2)),
    )
    paddles.append(right_paddle)
    
    for item in paddles:
        item.setFill(settings["fg_color"])
        item.setOutline(settings["fg_color"])
        item.setWidth(3)
        to_draw.append(item)
    
    player_score_text = Text(Point(settings["window_x"]-100,100), "0")
    ai_score_text = Text(Point(100,100), "0")
    scores = [ai_score_text,player_score_text]
    
    for score in scores:
        score.setTextColor("white")
        score.setSize(36)
        to_draw.append(score)
    
    for item in to_draw:
        item.draw(win)
    win.update()
    ####
    
    print("Hit any key to continue")
    win.getKey()
    play_game(win,to_draw,ball,paddles,scores)
    
    ####
    for item in to_draw:
        item.undraw()
    win.update()
    
    
def play_game(win,to_draw,ball,paddles,scores):
    play = True
    reset = False
    player_points = 0
    ai_points = 0
    color_score = 0
    ball_v = [
        random.choice([settings["ball_speed"],-settings["ball_speed"]]),
        random.choice([settings["ball_speed"],-settings["ball_speed"]]),]
    left_paddle = paddles[0]
    right_paddle = paddles[1]
    while play:
        if color_score >= 5:
            next_color(win)
            color_score = 0
            
        if reset:
            ball_center = ball.getCenter()
            move_x = settings["window_x"]/2 - ball_center.getX()
            move_y = settings["window_y"]/2 - ball_center.getY()
            ball.move(move_x,move_y)
            ball_v = [
                random.choice([-settings["ball_speed"],settings["ball_speed"]]),
                random.randrange(int(-settings["ball_speed"]/2),int(settings["ball_speed"]/2)),]
            reset = False
        ball.move(ball_v[0],ball_v[1])
        ball_v,points = check_for_bounce(win,ball,ball_v,paddles)
        player_points += points[1]
        ai_points += points[0]
        if points[0] > 0 or points[1] > 0:
            reset = True
            color_score += 1
        scores[0].setText(str(ai_points))
        scores[1].setText(str(player_points))
        
        ######
        key = win.checkKey()
        if key == "Up":
            right_paddle.move(0,-settings["paddle_speed"]*2)
        elif key == "Down":
            right_paddle.move(0,settings["paddle_speed"]*2)
        elif key == "Escape":
            play = False
            
        paddles = move_ai_paddle(win,ball,paddles)
        
        update(settings["frame_rate"])
        
        
def next_color(win):
    new_settings = random.choice(levels)
    settings["bg_color"] = new_settings["bg_color"]
    settings["fg_color"] = new_settings["fg_color"]
    win.setBackground(settings["bg_color"])
    if settings["paddle_speed"] < settings["paddle_speed_max"]:
        settings["paddle_speed"] += 1
        #settings["paddle_inset"] += 2
    if settings["ball_speed"] < settings["ball_speed_max"]:
        settings["ball_speed"] += 1
        
        
def move_ai_paddle(win,ball,paddles):
    ball_center = ball.getCenter()
    ball_x = ball_center.getX()
    ball_y = ball_center.getY()
    
    paddle_center = paddles[0].getCenter()
    paddle_y = paddle_center.getY()
    if ball_y < paddle_y:
        paddles[0].move(0,-settings["paddle_speed"])
    elif ball_y > paddle_y:
        paddles[0].move(0,settings["paddle_speed"])
        
    if settings["demo_mode"]:
        paddle_center = paddles[1].getCenter()
        paddle_y = paddle_center.getY()
        if ball_y < paddle_y:
            paddles[1].move(0,-settings["paddle_speed"])
        elif ball_y > paddle_y:
            paddles[1].move(0,settings["paddle_speed"])
    
    return(paddles)
            
        
def check_for_bounce(win,ball,ball_v,paddles):
    ball_center = ball.getCenter()
    ball_x = ball_center.getX()
    ball_y = ball_center.getY()
    bounce_x = False
    bounce_y = False
    points = [0,0]
    bounce_strength = 0
    
    ## Check if ball hits far wall first ##
    if ball_x + settings["ball_radius"] >= settings["window_x"]:
        bounce_x = True
        points[0] += 1
    elif ball_x - settings["ball_radius"] <= 0:
        bounce_x = True
        points[1] += 1
    if ball_y + settings["ball_radius"] >= settings["window_y"]:
        bounce_y = True
    elif ball_y - settings["ball_radius"] <= 0:
        bounce_y = True
        
    ## Then check if it hit a paddle ##
    for paddle in paddles:
        paddle_center = paddle.getCenter()
        paddle_p1 = paddle.getP1()
        paddle_p2 = paddle.getP2()
        
        max_x = ball_x + settings["ball_radius"]
        min_x = ball_x - settings["ball_radius"]
        max_y = ball_y + settings["ball_radius"]
        min_y = ball_y - settings["ball_radius"]
        
        if max_x >= paddle_p1.getX() and min_x <= paddle_p1.getX():
            if max_y >= paddle_p1.getY() and min_y <= paddle_p2.getY():
                bounce_x = True
                ### Calculate extra velocity based on distance from center of paddle ###
                distance = math.sqrt(
                    (paddle_center.getX() - ball_x)**2 + (paddle_center.getY() - ball_y)**2)
                ball_v[1] += distance/4
                
    
    if bounce_x:
        #if settings["ball_speed"] < settings["ball_speed_max"]:
        #    settings["ball_speed"] += 1
        #if settings["paddle_speed"] < settings["paddle_speed_max"]:
        #    settings["paddle_speed"] += 1
        print("Bounce X")
        if ball_v[0] > 0:
            ball_v[0] = 0 - ball_v[0]
        elif ball_v[0] < 0:
            ball_v[0] = abs(ball_v[0])
            
    if bounce_y:
        #if settings["ball_speed"] < settings["ball_speed_max"]:
        #    settings["ball_speed"] += 1
        #if settings["paddle_speed"] < settings["paddle_speed_max"]:
        #    settings["paddle_speed"] += 1
        print("Bounce Y")
        if ball_v[1] > 0:
            ball_v[1] = 0 - ball_v[1]
        elif ball_v[1] < 0:
            ball_v[1] = abs(ball_v[1])
        print(str(ball_v))
    
    return(ball_v,points)
    
    
def calc_rowsY(win,rows):
    rowsY = []
    for i in range(1,rows+1):
        new_y = i/(rows+1)
        #print("{} = int({}/({}+1))".format(
        #    str(new_y),str(i),str(rows)))
        rowsY.append(new_y*settings["window_y"])
    return(rowsY)
    
    
def farewell():
    print("\nFarewell!\n")
    clear()


init()
main()
farewell()
