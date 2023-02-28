import time,sys,random,keyboard
print('''
OBJECTIVE:  have the character (o) at the same place as the goal (O)
CONTROL:    left and right arrow key to move character
            up arrow key to claim victory when standing on goal
            s for speeding
            space for pausing
                               
      ''')

while True:
    #setting for the game mode
    difficulty = input("easy, normal, hard, or insane : ")
    if difficulty == "easy" or difficulty == "":
        indent = 20                                            # player start location
        goal_location = random.randint(0,50)     # goal location range
        step_for_jump = 14                               # how many counter require for goal to change place 
        reset_range = 4                                     # how far the goal change to
        count_data_reset_step = 1                    # how far from goal only then the counter reset to empty 
        
    elif difficulty == "normal":
        indent = 27                                             
        goal_location = random.randint(0,80)     
        step_for_jump = 8
        reset_range = 11
        count_data_reset_step = 2
        
    elif difficulty == "hard":
        indent = 35
        goal_location = random.randint(0,110)     
        step_for_jump = 5
        reset_range = 25
        count_data_reset_step = 2
        start = time.monotonic()
        time_allow = 15
        print("beat the game in 15 seconds")

    elif difficulty == "insane":
        indent = 15
        goal_location = random.randint(0,150) 
        step_for_jump = 5
        reset_range = 50
        count_data_reset_step = 3
        start = time.monotonic()
        time_allow = 8
        print("beat the game in 8 seconds")

    #data assigning
    counter = 0 #to prevent player take long time waiting on top of goal
    count_data = [] #list to record counter when player is waiting on top of goal
    fast_speed = 2
    character = "o"

    #indicator of moving direction
    L_direction = ""
    R_direction = ""

    time.sleep(1)
    #main function to print out the player and goal
    def start_location():
        if indent == goal_location: #star when player on top of goal
            print(" " * indent_left, end="")
            print("*")
        else:
            print(" " * indent_left,end='')
            print(first, end="")
            print(" " * indent_right, end="" )
            print(second)
                    
    try:
        while True: #main game loop
            if indent <= goal_location: #player at left
                indent_left = indent - len(L_direction) #indent belong to player and minus off any left moving icon (<) so it remain accurate
                indent_right = goal_location - indent - 1 - len(R_direction) 
                #(goal_location - indent) to get extra indent of goal from player; (-1 ) or else will have 5 indent indent but goal is only exactly
                #at number goal_location + 1(for A symbol) = goal_location + 1;and minus off any right moving icon(>) from the player 
                second = "O"
                if indent_right < 0: #to correct the speed emoji to the goal when in contact
                    if indent_right == -1 and not keyboard.is_pressed('s'):
                        R_direction = "O"
                    elif indent_right == -1 and keyboard.is_pressed('s'):
                        R_direction = ">>O"
                    elif indent_right == -2:
                        R_direction = ">O>"
                    elif indent_right == -3:
                        R_direction = "O>>"
                    second = ""
                first = L_direction + character + R_direction
                start_location()
                
            elif goal_location <= indent: #player at right
                indent_left = goal_location
                indent_right = indent - goal_location - 1 - len(L_direction)
                first = "O"
                if indent_right < 0: #to correct the speed emoji to the goal when in contact
                    if indent_right == -1 and not keyboard.is_pressed('s'):
                        L_direction = "O"
                    elif indent_right == -1 and keyboard.is_pressed('s'):
                        L_direction = "O<<"
                    elif indent_right == -2:
                        L_direction = "<O<"
                    elif indent_right == -3:
                        L_direction = "<<O"
                    first = ""
                second = L_direction + character + R_direction
                start_location()
            
            #to reset the direction icon again so when not moving it will show nothing           
            L_direction = ""
            R_direction = ""
            
            #make sure player not take too long on top of goal
            counter += 1
            if indent in range(goal_location -count_data_reset_step+1,goal_location +count_data_reset_step): #if player is in a range of the goal, the counter will be recorded
                count_data.append(counter)
                if len(count_data) == step_for_jump: #if counter exceed a certain length, the goal will jump to a certain range from it's initial location
                    goal_location = random.randint(goal_location -reset_range, goal_location +reset_range)
                    count_data = [] #reset to empty
            if indent <= goal_location -count_data_reset_step or indent >= goal_location +count_data_reset_step: 
                count_data = [] 
                # player need to stand on or outside of the range of the goal to reset the count_data back to 0 so goal won't jump
            
            time.sleep(0.1)
            
            #registering movement
            if keyboard.is_pressed('right'):
                indent += 1
                R_direction = ">"
                if keyboard.is_pressed('s'):
                    indent += fast_speed
                    R_direction =  ">>>"
            elif keyboard.is_pressed('left'):
                indent -= 1
                L_direction = "<"
                if keyboard.is_pressed('s'):
                    indent -= fast_speed
                    L_direction = "<<<"
            
            #win
            if keyboard.is_pressed('up'): 
                if indent == goal_location:    #need to separate or else python need take time to check both and will delay register
                    if difficulty == "insane" or difficulty == "hard":
                        end = time.monotonic()
                        time_used = round(end-start,2)
                        print("the time you used is : ")
                        time.sleep(2.5)
                        print(str(time_used) + " seconds")
                        if time_used > time_allow:
                            print("Challenge losed")
                            print("Do you want to replay?")
                            replay = input("yes or no? : ") 
                            if replay == "no":
                                sys.exit()
                    print("congratulations")
                    print("Do you want to replay?")
                    replay = input("yes or no? : ")
                    if replay == "no":
                        sys.exit()
                    
            #to prevnt going to negative block
            if indent < 0:
                indent = 0
                L_direction = ""
            elif indent > 150:
                indent = 150
            if goal_location < 0:
                goal_location = 0
            elif goal_location > 150:
                goal_location = 150
            
            def setting():
                print('''
    type                     setting
      up                  increase speed
    down                 decrease speed
  right/left            change character''')
                while True:
                    time.sleep(0.14)
                    global fast_speed
                    show = False
                    if keyboard.is_pressed('up'):
                        if fast_speed < 10: 
                            show = True
                            fast_speed += 1
                        else:
                            print('The maximum speeding_speed is 10')
                    elif keyboard.is_pressed('down'):
                        if fast_speed > 1:
                            show = True
                            fast_speed -= 1
                        else:
                            print('The minimum speeding_speed is 1')
                    if show:
                        print('speeding speed : ' + str(fast_speed))
                        
                    global character
                    show = False
                    skin = ['o','🌐','😡','🐢','❤️','😁','🤢','💩','👻','🏎️','🍟']
                    i = skin.index(character)
                    if keyboard.is_pressed('right'):
                        if i < len(skin) - 1:
                            i += 1
                            show = True
                    elif keyboard.is_pressed('left'):
                        if i > 0:
                            i -= 1
                            show = True
                    character = skin[i]
                    if show:
                        print(character)
                    if keyboard.is_pressed('space'):
                        break
                
                
            #pausing
            if keyboard.is_pressed('space'):
                print('pausing')
                time.sleep(0.3)
                setting()
                while True:
                    if keyboard.is_pressed('space'):
                        print('continuing')
                        time.sleep(1)
                        break

    except KeyboardInterrupt:
        sys.exit()
        