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
    "button_width": 250,
    "button_spacing": 40,
    "text_spacing": 40,
    "demo_mode": False,
    "color_shift": 5,
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
    
    
def view_settings(win):
    to_draw = []    
    to_draw,buttons = draw_settings(win,to_draw)
    
    ### 
    for item in to_draw:
        item.draw(win)
    #########
    ## Stuff what be done goes here yo ##    
    choice = "default"
    while choice != "":
        click = win.getMouse()
        clickX = click.getX()
        clickY = click.getY()
        choice = ""
        for button in buttons:
            if clickX >= button["x1"] and clickX <= button["x2"] and clickY >= button["y1"] and clickY <= button["y2"]:
                choice = button["name"]
                print("Clicked on {} button".format(choice))
                adjust_setting(win,choice,button)
                redraw(win,to_draw)
                #to_draw,buttons = draw_settings(win,to_draw)
                win.update()
        if choice == "":
            break

            
    #########
    for item in to_draw:
        item.undraw()
    ###
    
    
def draw_settings(win,to_draw):
    for item in to_draw:
        item.undraw()
    
    to_draw = []
    buttons = []
    
    centerX = int(settings["window_x"]/2)
    centerY = int(settings["window_y"]/2)
    
    leftcol_centerX = int(centerX / 2)
    rightcol_centerX = centerX + leftcol_centerX
    
    header_height = settings["button_height"] + settings["button_spacing"]*2
    total_button_height = settings["button_height"] + settings["button_spacing"]

    ### Max buttons per column is limited by window Y ###
    ### Total height of button is (button + button_spacing)*number_of_buttons + header_height ###
    max_buttons_per_column = int((settings["window_y"]-header_height)/total_button_height)
    
    print("{} settings: {} buttons per column".format(
        str(len(settings)),str(max_buttons_per_column)))
    
    if max_buttons_per_column < len(settings):
        columns = 2
        print("Two columns needed")
    else:
        columns = 1
        print("One column needed")
        
    title = Text(Point(centerX, settings["button_spacing"]), "SETTINGS")
    title.setTextColor(settings["fg_color"])
    title.setSize(24)
    title.setStyle("bold")
    to_draw.append(title)
    
    #### COUNT TITLE AS A BUTTON FOR SPACING PURPOSES ####
    buttons_made = 2
    column = 1
    
    for item in settings:
        button_name = item
        button_value = settings[item]
        button_string = ("{}: {}".format(button_name, button_value))
        
        if columns == 1:
            box_P1X = centerX - settings["button_width"]/2
            box_P1Y = (settings["button_height"]*buttons_made) + settings["button_spacing"]*buttons_made
            box_P2X = box_P1X + settings["button_width"]
            box_P2Y = box_P1Y + settings["button_height"]
        elif columns == 2:
            if buttons_made-2 >= max_buttons_per_column:
                column = 2
                print("Column 2")
            else:
                column = 1
                print("Column 1")
            if column == 1:
                box_P1X = (centerX - settings["button_width"]/2) - settings["button_width"]*2
                box_P1Y = (settings["button_height"]*buttons_made) + settings["button_spacing"]*buttons_made
                box_P2X = box_P1X + settings["button_width"]
                box_P2Y = box_P1Y + settings["button_height"]
            elif column == 2:
                box_P1X = (centerX - settings["button_width"]/2) + settings["button_width"]*2
                box_P1Y = (settings["button_height"]*(buttons_made - max_buttons_per_column)) + (settings["button_spacing"]*(buttons_made - max_buttons_per_column))
                box_P2X = box_P1X + settings["button_width"] 
                box_P2Y = box_P1Y + settings["button_height"]
                #print("{},{}  x  {},{}".format(
                #    str(box_P1X),str(box_P1Y),str(box_P2X),str(box_P2Y)))
        
        
        box_centerX = (box_P1X + box_P2X)/2
        box_centerY = (box_P1Y + box_P2Y)/2
        
        box = Rectangle(Point(box_P1X,box_P1Y),Point(box_P2X,box_P2Y))
        box.setFill(settings["bg_color"])
        box.setOutline(settings["fg_color"])
        box.setWidth(2)
        
        box_text = Text(Point(box_centerX,box_centerY),button_string)
        box_text.setTextColor(settings["fg_color"])
        
        buttons_made += 1
        print("Buttons made: "+str(buttons_made))
        
        buttons.append(
            {"name": button_name,
             "value": button_value,
             "x1": box_P1X,
             "y1": box_P1Y,
             "x2": box_P2X,
             "y2": box_P2Y,
             "box": box,
             "text": box_text,
            })
        
        to_draw.append(box)
        to_draw.append(box_text)
        
    return(to_draw,buttons)

    
def redraw(win,to_draw):
    for item in to_draw:
        item.undraw()
    win.update()
    for item in to_draw:
        try:
            item.setColor(settings["fg_color"])
        except:
            pass
        try:
            item.setTextColor(settings["fg_color"])
        except:
            pass
        item.setOutline(settings["fg_color"])
        item.draw(win)
    win.setBackground(settings["bg_color"])
    win.update()
    
    
def adjust_setting(win,setting_name,button):
    ### Draw a box with text, entry, and two buttons ("Accept", "Cancel") ###
    to_draw = []
    
    for setting in settings:
        if setting_name == setting:
            setting_value = settings[setting]
            print("Setting: "+str(setting))
            print("Setting value: "+str(setting_value))
    
    centerX = settings["window_x"]/2
    centerY = settings["window_y"]/2
    
    box_P1X = centerX - settings["button_width"]
    box_P2X = centerX + settings["button_width"]
    box_P1Y = centerY - settings["button_height"]*4
    box_P2Y = centerY + settings["button_height"]*4
    box_centerX = (box_P1X + box_P2X)/2
    box_centerY = (box_P1Y + box_P2Y)/2
    box_topY = box_P1Y
    
    box = Rectangle(Point(box_P1X,box_P1Y),Point(box_P2X,box_P2Y))
    box.setFill(settings["bg_color"])
    box.setOutline(settings["fg_color"])
    box.setWidth(3)
    to_draw.append(box)
    
    title = Text(
        Point(box_centerX,box_topY + settings["button_spacing"]),setting_name)
    title.setTextColor(settings["fg_color"])
    title.setSize(24)
    title.setStyle("bold")
    to_draw.append(title)
    
    value = Text(
        Point(box_centerX,box_topY + settings["button_spacing"]*2),str(setting_value))
    value.setTextColor(settings["fg_color"])
    value.setSize(18)
    to_draw.append(value)
    
    entry = Entry(Point(box_centerX,box_topY + settings["button_spacing"]*4),16)
    entry.setText(str(setting_value))
    entry.setTextColor("black")
    entry.setFill("white")
    to_draw.append(entry)
    
    
    for item in to_draw:
        item.draw(win)
        
    #####
    win.getMouse()
    new_value = entry.getText()
    
    entry.undraw()
    for setting in settings:
        if setting == setting_name:
            if new_value.isdigit():
                new_value = int(new_value)
            settings[setting] = new_value
            button["text"].setText(setting+": "+str(new_value))
            show_info_box(win,"New value set!\nRe-open settings for some values to take effect.")
    entry.draw(win)
    
    for item in to_draw:
        item.undraw()
    
    
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
        choice = ""
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
            ####
            draw_game(win)
            ####
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
        elif choice == "Settings":
            for item in to_draw:
                item.undraw()
            win.update()
            ####
            view_settings(win)
            ####
            for item in to_draw:
                item.draw(win)
            win.update()
        else:
            choice = ""
    
    
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
    
    show_info_box(win,"Hit any key to continue")
    play_game(win,to_draw,ball,paddles,scores)
    
    ####
    for item in to_draw:
        item.undraw()
    win.update()
    
    
def show_info_box(win,text):
    to_draw = []
    
    box_width = len(text) * 20
    
    if len(text) > 30:
        height = 2
    else:
        height = 1
    
    centerX = int(settings["window_x"]/2)
    centerY = int(settings["window_y"]/2)
    rect_P1X = centerX - box_width/2
    rect_P2X = centerX + box_width/2
    rect_P1Y = centerY - (settings["button_height"]/2)*height
    rect_P2Y = centerY + (settings["button_height"]/2)*height
    
    rect = Rectangle(Point(rect_P1X,rect_P1Y),Point(rect_P2X,rect_P2Y))
    rect.setFill(settings["bg_color"])
    rect.setOutline(settings["fg_color"])
    rect.setWidth(3)
    to_draw.append(rect)
    
    info_text = Text(Point(centerX,centerY),text)
    info_text.setTextColor(settings["fg_color"])
    info_text.setStyle("bold")
    info_text.setSize(20)
    to_draw.append(info_text)
    
    for item in to_draw:
        item.draw(win)
        
    key = ""
    click = None
    while key == "" and click == None:
        key = win.checkKey()
        click = win.checkMouse()
    time.sleep(1)
    
    for item in to_draw:
        item.undraw()
    
    
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
        if color_score >= settings["color_shift"]:
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
    if settings["ball_speed"] < settings["ball_speed_max"]:
        settings["ball_speed"] += 1
        
        
def move_ai_paddle(win,ball,paddles):
    choices = ["Straight","Tilt Up","Tilt Down"]
    shot = random.choice(choices)
    
    ball_center = ball.getCenter()
    ball_x = ball_center.getX()
    ball_y = ball_center.getY()
    
    if shot == "Straight":
        paddle_center = paddles[0].getCenter()
        paddle_y = paddle_center.getY()
    elif shot == "Tilt Up":
        paddle_center = paddles[0].getP1()
        paddle_y = paddle_center.getY()
    elif shot == "Tilt Down":
        paddle_center = paddles[0].getP2()
        paddle_y = paddle_center.getY()
        
    if ball_y < paddle_y:
        paddles[0].move(0,-settings["paddle_speed"])
    elif ball_y > paddle_y:
        paddles[0].move(0,settings["paddle_speed"])
        
    if settings["demo_mode"]:
        shot = random.choice(choices)
        if shot == "Straight":
            paddle_center = paddles[1].getCenter()
            paddle_y = paddle_center.getY()
        elif shot == "Tilt Up":
            paddle_center = paddles[1].getP1()
            paddle_y = paddle_center.getY()
        elif shot == "Tilt Down":
            paddle_center = paddles[1].getP2()
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
