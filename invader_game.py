"""
    Name: Yiu Tung Hon
    Student ID: 20510099
"""

"""
    Turtle Graphics - Shooting Game
"""

import turtle

"""
    Constants and variables
"""

# Set up the backgound turtle
background = turtle.Turtle()
turtle.addshape("bg.gif")
background.shape("bg.gif")

timer = 0
enemy_stop = 0
# General parameters
window_height = 600
window_width = 600
window_margin = 50
update_interval = 25    # The screen update interval in ms, which is the
                        # interval of running the updatescreen function

# Player's parameters
player_size = 50        # The size of the player image plus margin
player_init_x = 0
player_init_y = -window_height / 2 + window_margin
player_speed = 10       # The speed the player moves left or right
player_score = 0

# Bonus enemy's parameter
bonus_size = 55
bonus_init_x = window_height / 2 - window_margin
bonus_init_y = window_height / 2 - window_margin
bonus_max_x = -window_height / 2 + window_margin
bonus_size = 30
bonus_speed = 3

# Enemy's parameters
enemy_number = 19        # The number of enemies in the game
enemy_size = 50         # The size of the enemy image plus margin
enemy_init_x = -window_width / 2 + window_margin
enemy_init_y = window_height / 2 - window_margin - bonus_size
enemy_min_x = enemy_init_x
enemy_max_x = window_width / 2 - enemy_size * enemy_number
    # The maximum x coordinate of the first enemy, which will be used
    # to restrict the x coordinates of all other enemies
enemy_kill_player_distance = 30
    # The player will lose the game if the vertical
    # distance between the enemy and the player is smaller
    # than this value

### Set up bonus turtle ###
bonus = turtle.Turtle()
bonus.hideturtle()
turtle.addshape("bonus.gif")
bonus.shape("bonus.gif")
bonus.left(180)
bonus.up()

score = turtle.Turtle()
score.hideturtle()

# Enemy movement parameters
enemy_speed = 2
enemy_speed_increment = 1
    # The increase in speed every time the enemies move
    # across the window and back
enemy_direction = 1
    # The current direction the enemies are moving:
    #     1 means from left to right and
    #     -1 means from right to left

# The list of enemies
enemies = []

# Laser parameter
laser_width = 2
laser_height = 15
laser_speed = 20
laser_kill_enemy_distance = 20
    # The laser will destory an enemy if the distance
    # between the laser and the enemy is smaller than
    # this value

"""
    Handle the player movement
"""

# This function is run when the "Left" key is pressed. The function moves the
# player to the left when the player is within the window area
def playermoveleft():
    
    # Get current player position
    x, y = player.position()

    # Part 2.2 - Keeping the player inside the window
    # Player should only be moved only if it is within the window range
    if x - player_speed > -window_width / 2 + window_margin:
        player.shape("spaceship_left.gif")
        player.goto(x - player_speed, y)
    turtle.update() # delete this line after finishing updatescreen()

# This function is run when the "Right" key is pressed. The function moves the
# player to the right when the player is within the window area
def playermoveright():
    
    # Get current player position
    x, y = player.position()

    # Part 2.2 - Keeping the player inside the window
    # Player should only be moved only if it is within the window range
    if x + player_speed < window_width / 2 - window_margin:
        player.shape("spaceship_right.gif")
        player.goto(x + player_speed, y)

    turtle.update() # delete this line after finishing updatescreen()

"""
    Handle the screen update and enemy movement
"""

# This function is run in a fixed interval. It updates the position of all
# elements on the screen, including the player and the enemies. It also checks
# for the end of game conditions.
def updatescreen():
    
    # Use the global variables here because we will change them inside this
    # function
    global enemy_direction, enemy_speed, enemy_max_x, player_score, timer

    # Move the enemies depending on the moving direction

    # The enemies can only move within an area, which is determined by the
    # position of enemy at the top left corner, enemy_min_x and enemy_max_x

    # x and y displacements for all enemies
    dx = enemy_speed * enemy_direction
    dy = 0

    # Change enemy_max_x base on enemy number
    row_number = min(enemy_number, 7)
    enemy_max_x = window_width / 2 - enemy_size * row_number

    # Part 3.3
    # Perform several actions if the enemies hit the window border

    # Perform severl action when the enemies hit the window border
    x0 = enemies[0].xcor()

    if x0 + dx > enemy_max_x or x0 + dx < enemy_min_x:
        
        # Switch the moving direction
        enemy_direction = -enemy_direction

        # Bring the enemies closer to the player
        dy = -enemy_size / 2

        # Increase the speed when the direction switches to right again
        if enemy_direction == 1:
            enemy_speed += enemy_speed_increment

    # Move the enemies according to the dx and dy values determined above
    for enemy in enemies:
        x, y = enemy.position()
        enemy.goto(x + dx, y + dy)
        
        if (x // 50) % 2 == 0:
            enemy.shape("enemy.gif")
        else:
            enemy.shape("enemy2.gif")

    # Show and move bonus enemy every 6 seconds
    if timer % 240 == 0 and timer != 0:
        bonus.goto(bonus_init_x, bonus_init_y)
        bonus.showturtle()
    
    # Move the bonus enemy when it is visible
    if bonus.isvisible():
        bonus.forward(bonus_speed)
    
    if bonus.xcor() < -window_width / 2 + window_margin:
        bonus.hideturtle()

    # Part 4.3 - Moving the laser
    # Perfrom several actions if the laser is visible

    if laser.isvisible():
        # Move the laser
        laser.forward(laser_speed)

        # Hide the laser if it goes beyond the window
        if laser.ycor() > window_height / 2:
            laser.hideturtle()

        # Check the laser against every enemy using for loop
        for enemy in enemies:
            # If the enemy is visble AND the laser is very close to the enemy
            if enemy.isvisible() and laser.distance(enemy) < 20:
            
                # Remove the enemy and the laser
                laser.hideturtle()
                enemy.hideturtle()
                player_score += 20
                score.clear()
                score.write(player_score, font=("System", 15, "bold"))
                turtle.update()
                # Stoop of some enemy has been hit
                break
        
        # Check the laser against bonus
        if bonus.isvisible() and laser.distance(bonus) < 20:
            
            # Remove laser and bonus if hit
            laser.hideturtle()
            bonus.hideturtle()
            player_score += 100
            score.clear()
            score.write(player_score, font=("System", 15, "bold"))
            turtle.update()
                        
    # Part 5.1 - Gameover when one of the enemies is close to the player

    # If one of the enemies is very close to the player, the game will be over
    for enemy in enemies:
        if enemy.isvisible() and enemy.ycor()-player.ycor() < enemy_kill_player_distance:
            # Show a message
            gameover("You lose!")

            # Return and do not run updatescreen() again
            return

    # Part 5.2 - Gameover when you have killed all enemies

    # Set up a variable as a counter
    count = 0

    # For each enemy
    for enemy in enemies:
        # Increase the counter if the enemy is visible
        if enemy.isvisible():
            count += 1

    # If the counter is 0, that means you have killed all enemies
    if count == 0:
        # Perform several gameover actions
        gameover("You win!")

        return
    # Part 3.2 - Controlling animation using the timer event

    # Update the screen
    turtle.update()

    if not enemy_stop:
        timer += 1

    #Schedule the next screen update
    turtle.ontimer(updatescreen, update_interval)

"""
    Shoot the laser
"""

# This function is run when the player presses the spacebar. It shoots a laser
# by putting the laser in the player's current position. Only one laser can
# be shot at any one time.
def shootlaser():
    
    # Part 4.2 - the shooting function
    # Shoot the laser only if it is not visible

    # When the laser is available
    if not laser.isvisible():
        # Make the laser to become visble
        laser.showturtle()

        # Move the laser to the position of the player
        laser.setposition(player.xcor(), player.ycor())

"""
    Stop the enemy function
"""
def resume():
    global enemy_speed, bonus_speed, enemy_stop
    enemy_stop = 0
    enemy_speed = 2
    bonus_speed = 3

    turtle.onkeypress(pause, "c")
    
def pause():
    global enemy_speed, bonus_speed, enemy_stop
    enemy_stop = 1
    enemy_speed = 0
    bonus_speed = 0

    turtle.onkeypress(resume, "c")
            
"""
    Game start
"""
# This function contains things that have to be done when the game starts.
def gamestart(x, y):
    start_button.clear()
    start_button.hideturtle()

    title.clear()
    instruction.clear()
    enemy_amount.clear()
    left_arrow.hideturtle()
    right_arrow.hideturtle()

    # Set up the score area 
    labels.clear()
    labels.goto(-50, 275)
    labels.write("Score:", font=("System", 15, "bold"))
    # Score board
    score.up()
    score.goto(10, 275)
    score.color("dark blue")
    score.write(player_score, font=("System", 15, "bold"))

    turtle.addshape("enemy2.gif")
    # Use the global variables here because we will change them inside this
    # function
    global player, laser

    ### Player turtle ###

    # Add the spaceship picture
    turtle.addshape("spaceship_left.gif")
    turtle.addshape("spaceship_right.gif")
    # Create the player turtle and move it to the initial position
    player = turtle.Turtle()
    player.shape("spaceship_right.gif")
    player.up()
    player.goto(player_init_x, player_init_y)

    # Part 2.1
    # Map player movement handlers to key press events

    turtle.onkeypress(playermoveleft, "Left")
    turtle.onkeypress(playermoveright, "Right")
    turtle.onkeypress(pause, "c")
    turtle.listen()
    ### Enemy turtles ###

    # Add the enemy picture
    turtle.addshape("enemy.gif")

    for i in range(enemy_number):
        # Create the turtle for the enemy
        enemy = turtle.Turtle()
        enemy.shape("enemy.gif")
        enemy.up()

        # Move to a proper position counting from the top left corner
        enemy.goto(enemy_init_x + enemy_size * (i % 7), enemy_init_y - enemy_size * (i // 7))

        # Add the enemy to the end of the enemies list
        enemies.append(enemy)


    ### Laser turtle ###

    # Create the laser turtle using the square turtle shape
    laser = turtle.Turtle()
    turtle.addshape("laser.gif")
    laser.shape("laser.gif")

    # Change the size of the turtle and change the orientation of the turtle
    laser.shapesize(laser_width / 20, laser_height / 20)
    laser.left(90)
    laser.up()

    # Hide the laser turtle
    laser.hideturtle()

    # Part 4.2 - Mapping the shooting function to key press event
    turtle.onkeypress(shootlaser, "space")

    turtle.update()

    # Part 3.2 - Controlling animation using the timer event

    # Start the game by running updatescreen()
    turtle.ontimer(updatescreen, update_interval)

"""
    Game over
"""

# This function shows the game over message.
def gameover(message):
    
    # Part 5.3 - Improving the gameover() function
    noti = turtle.Turtle()
    noti.hideturtle()
    noti.pencolor("Yellow")
    noti.write(message, align="center", font=("System", 30, "bold"))
    turtle.update()

"""
    Handle enemy number
"""

def decrease_enemy_number(x, y):
    global enemy_number
    if enemy_number > 1:
        enemy_number -= 1
        enemy_amount.clear()
        enemy_amount.write(str(enemy_number), font=("System", 18, "bold"), align="center")
    turtle.update()

def increase_enemy_number(x, y):
    global enemy_number
    if enemy_number < 48:
        enemy_number += 1
        enemy_amount.clear()
        enemy_amount.write(str(enemy_number), font=("System", 18, "bold"), align="center")
    turtle.update()
    
"""
    Set up main Turtle parameters
"""

# Set up the turtle window
turtle.setup(window_width, window_height)
turtle.bgcolor("Black")
turtle.up()
turtle.hideturtle()
turtle.tracer(False)

"""
    Set up the option
"""

# Create required turtles
title = turtle.Turtle()
instruction = turtle.Turtle()
labels = turtle.Turtle()
right_arrow = turtle.Turtle()
left_arrow = turtle.Turtle()
enemy_amount = turtle.Turtle()

# Draw the start button
start_button = turtle.Turtle()
start_button.up()
start_button.goto(-40, -180)
start_button.color("white", "DarkGray")
start_button.begin_fill()
for _ in range(2):
    start_button.forward(80)
    start_button.left(90)
    start_button.forward(25)
    start_button.left(90)
start_button.end_fill()

# Write text on the button
start_button.goto(0, -175)
start_button.write("Start", font=("System", 12, "bold"), align="center")

# Cover the image with start_button turtle
start_button.goto(0, -168)
start_button.shape("square")
start_button.shapesize(1.3, 4)
start_button.color("")
    
# Set up the title turtle
title.hideturtle()
title.up()
title.color("black")
title.goto(0, 150)
title.write("Hello Kitty Land Invaders", align="center", font=("System", 30, "bold"))

# Set up the instruction turtle
instruction.hideturtle()
instruction.up()
instruction.color("black")
instruction.goto(0, -80)
instruction.write("Instruction:\nMove left: left arrow key\nMove right: right arrow key\nShoot Daniel: spacebar\n\n   Kill all the monster Hello Kitty!"\
,font=("System", 18), align=("center"))

# Set up labels turtle
labels.hideturtle()
labels.up()
labels.color("black")
labels.goto(-200, -140)
labels.write("Number of Enemies:", font=("System", 18, "bold"))

# Set up enemy_amount turtle
enemy_amount.hideturtle()
enemy_amount.up()
enemy_amount.color("black")
enemy_amount.goto(108, -140)
enemy_amount.write(str(enemy_number), font=("System", 18, "bold"), align="center")

# Set up left_arrow turtle
left_arrow.shape("arrow")
left_arrow.color("red")
left_arrow.shapesize(0.75, 1.4)
left_arrow.left(180)
left_arrow.up()
left_arrow.goto(85, -125)

left_arrow.onclick(decrease_enemy_number)

# Set up right_arrow turtle
right_arrow.shape("arrow")
right_arrow.color("red")
right_arrow.shapesize(0.75, 1.4)
right_arrow.up()
right_arrow.goto(130, -125)

right_arrow.onclick(increase_enemy_number)

turtle.update()

"""
    Start
"""

# Start the game
start_button.onclick(gamestart)

# Switch focus to turtle graphics window
turtle.done()
