#from nis import match
from cmath import log
from os import pipe
import pygame, sys, random
    
green = (0, 255, 0)
blue = (0, 0, 128)

pygame.init()

#create display surface
screen_width = 576
scree_height = 1024
screen = pygame.display.set_mode((screen_width, scree_height))
clock = pygame.time.Clock()

# Game Variables
gravity = 0.18
bird_movement = 0
floor_movement = 1
pipe_movement = 2
bird_starting_height = 512
player_score = 0
highscore = 0
bird_flapping_timer = 0
game_is_running = False
pre_game = True

score_zero_surface = pygame.image.load('sprites/0.png')
score_zero_surface = pygame.transform.scale2x(score_zero_surface)
score_one_surface = pygame.image.load('sprites/1.png')
score_one_surface = pygame.transform.scale2x(score_one_surface)
score_two_surface = pygame.image.load('sprites/2.png')
score_two_surface = pygame.transform.scale2x(score_two_surface)
score_three_surface = pygame.image.load('sprites/3.png')
score_three_surface = pygame.transform.scale2x(score_three_surface)
score_four_surface = pygame.image.load('sprites/4.png')
score_four_surface = pygame.transform.scale2x(score_four_surface)
score_five_surface = pygame.image.load('sprites/5.png')
score_five_surface = pygame.transform.scale2x(score_five_surface)
score_six_surface = pygame.image.load('sprites/6.png')
score_six_surface = pygame.transform.scale2x(score_six_surface)
score_seven_surface = pygame.image.load('sprites/7.png')
score_seven_surface = pygame.transform.scale2x(score_seven_surface)
score_eight_surface = pygame.image.load('sprites/8.png')
score_eight_surface = pygame.transform.scale2x(score_eight_surface)
score_nine_surface = pygame.image.load('sprites/9.png')
score_nine_surface = pygame.transform.scale2x(score_nine_surface)
score_character_distance = 52
score_x_pos = (screen_width / 2) - (score_character_distance / 2)
score_y_pos = 150

game_over_surface = pygame.image.load('sprites/gameover.png')
game_over_surface = pygame.transform.scale2x(game_over_surface)

bg_surface = pygame.image.load('sprites/background-day.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)
  
floor_surface = pygame.image.load('sprites/base.png')
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0
floor_y_pos = 900

bird_surface = pygame.image.load('sprites/bluebird-midflap.png').convert()
bird_surface = pygame.transform.scale2x(bird_surface)
bird_rect = bird_surface.get_rect(center = (80, bird_starting_height))
bird_surface_upflap = pygame.image.load('sprites/bluebird-upflap.png').convert()
bird_surface_upflap = pygame.transform.scale2x(bird_surface_upflap)
#bird_surface_upflap = pygame.transform.rotate(bird_surface_upflap, 45)
bird_surface_downflap = pygame.image.load('sprites/bluebird-downflap.png').convert()
bird_surface_downflap = pygame.transform.scale2x(bird_surface_downflap)
#bird_surface_downflap = pygame.transform.rotate(bird_surface_downflap, -45)

pipe_surface = pygame.image.load('sprites/pipe-green.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_roof = pygame.image.load('sprites/pipe-green.png')
pipe_roof = pygame.transform.scale2x(pipe_roof)
pipe_roof = pygame.transform.rotate(pipe_roof, 180)
pipe_starting_x = 600

pipe_list = []

SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1300)

######################################################################################################################################

def load_highscore():
    global highscore
    # Using 'w' as in write because it creates the file if it does not exist and has the ability to read and write.
    with open('highscore.txt', 'w') as file:
        try:
            highscore = file.read()
            file.close()
        except:
            highscore = 0
load_highscore()
del load_highscore

def save_highscore():
    global highscore
    with open('highscore.txt', 'w') as file:
        try:
            file.write(str(player_score))
            file.close()
            highscore = player_score
        except:
            print('Unable to save highscore')

def draw_floor():
    screen.blit(floor_surface,(floor_x_pos, floor_y_pos))
    screen.blit(floor_surface,(floor_x_pos + 576, floor_y_pos))

def create_pipe():
    pipe_random_movement = random.randint(1, 400)
    new_pipes = [
        pipe_surface.get_rect(midtop = (pipe_starting_x, 312 + pipe_random_movement)), 
        pipe_roof.get_rect(midtop = (pipe_starting_x, -512 + pipe_random_movement))
        ]
    return new_pipes

def move_pipes(pipes):  
    for pipe in pipes:
        pipe[0].centerx -= pipe_movement
        pipe[1].centerx -= pipe_movement
    return pipes

def draw_bird():
    global bird_flapping_timer
    if bird_flapping_timer < 20:
        screen.blit(bird_surface_upflap, bird_rect)
    else:
        screen.blit(bird_surface_downflap, bird_rect)
    if bird_flapping_timer >= 40:
        bird_flapping_timer = 0 

def check_score():
    global player_score
    if len(pipe_list) > 1:
        last_pipe = pipe_list[len(pipe_list) - 2] 
        if bird_rect.centerx == last_pipe[0].centerx:
            player_score += 1   

def draw_score():
    global player_score
    player_score_as_string = str(player_score)
    player_score_length = len(player_score_as_string)
    for i in range(player_score_length):
        this_character = player_score_as_string[i]
        score_x_pos_altered = (score_x_pos + score_character_distance * i) - (score_character_distance / 2 * (player_score_length - 1))
        if this_character == "0":
            screen.blit(score_zero_surface, (score_x_pos_altered, score_y_pos))
        if this_character == "1":
            screen.blit(score_one_surface, (score_x_pos_altered, score_y_pos))
        if this_character == "2":
            screen.blit(score_two_surface, (score_x_pos_altered, score_y_pos))
        if this_character == "3":
            screen.blit(score_three_surface, (score_x_pos_altered, score_y_pos))
        if this_character == "4":
            screen.blit(score_four_surface, (score_x_pos_altered, score_y_pos))
        if this_character == "5":
            screen.blit(score_five_surface, (score_x_pos_altered, score_y_pos))
        if this_character == "6":
            screen.blit(score_six_surface, (score_x_pos_altered, score_y_pos))
        if this_character == "7":
            screen.blit(score_seven_surface, (score_x_pos_altered, score_y_pos))
        if this_character == "8":
            screen.blit(score_eight_surface, (score_x_pos_altered, score_y_pos))
        if this_character  == "9":
            screen.blit(score_nine_surface, (score_x_pos_altered, score_y_pos))
        

def draw_pipes(pipes):
    for pipe in pipes:
        screen.blit(pipe_surface, pipe[0])
        screen.blit(pipe_roof, pipe[1])

def check_collisions(pipes):
        for pipe in pipes:
            if bird_rect.colliderect(pipe[0]) or bird_rect.colliderect(pipe[1]):
                game_over()
        if bird_rect.y >= 850:
            game_over()

def game_over():
    global gravity
    global bird_movement   
    global floor_movement
    global pipe_movement
    global game_is_running
    gravity = 0
    bird_movement = 0
    floor_movement = 0
    pipe_movement = 0
    game_is_running = False
    screen.blit(game_over_surface, (100, 50))
    if player_score > highscore:
        save_highscore()

def restart_game():
    global gravity
    global bird_movement
    global floor_movement
    global pipe_movement
    global pipe_list
    global player_score
    global game_is_running
    global pre_game
    gravity = 0.18
    bird_movement = 0
    floor_movement = 1
    pipe_movement = 2
    pipe_list = []
    player_score = 0
    bird_rect.centery = bird_starting_height
    game_is_running = True
    pre_game = True
    print(pre_game)

#TODO: set the game into an idle state after dying
    

#######################################################################################################################################
while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #makes the X button work on window
            event.type = pygame.quit
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_is_running:
                bird_movement = 0
                bird_movement -= 5
            if event.key == pygame.K_SPACE and not game_is_running:
                restart_game()
            if event.key == pygame.K_SPACE and pre_game and game_is_running:
                
                pre_game = False
                bird_movement = 0
                bird_movement -= 5
        if event.type == SPAWNPIPE and game_is_running:
            pipe_list.append(create_pipe())
            print("new pipe", len(pipe_list))

    #set img
    screen.blit(bg_surface,(0,0))

    #Bird
    if not pre_game:
        bird_movement += gravity
        bird_rect.centery += bird_movement
    bird_flapping_timer += 1
    draw_bird()

    #Pipes
    if not pre_game:
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        check_collisions(pipe_list)

    #Score
    check_score()
    draw_score()

    #Floor
    floor_x_pos -= floor_movement
    draw_floor()
    screen.blit(floor_surface,(floor_x_pos, floor_y_pos))
    if floor_x_pos <= -576:
        floor_x_pos = 0
    #takes everything before and draws it
    pygame.display.update()
    #set framerate to 120fps
    clock.tick(120)