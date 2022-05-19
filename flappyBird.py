from os import pipe
import pygame, sys, random
    
green = (0, 255, 0)
blue = (0, 0, 128)

pygame.init()

#create display surface
screen = pygame.display.set_mode((576,1024))
clock = pygame.time.Clock()

# Game Variables
gravity = 0.25
bird_movement = 0
floor_movement = 1
pipe_movement = 5
bird_starting_height = 512
game_is_running = True

game_over_surface = pygame.image.load('sprites/gameover.png')
game_over_surface = pygame.transform.scale2x(game_over_surface)

bg_surface = pygame.image.load('sprites/background-day.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)
  
floor_surface = pygame.image.load('sprites/base.png')
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

bird_surface = pygame.image.load('sprites/bluebird-midflap.png').convert()
bird_surface = pygame.transform.scale2x(bird_surface)
bird_rect = bird_surface.get_rect(center = (100, bird_starting_height))

pipe_surface = pygame.image.load('sprites/pipe-green.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_roof = pygame.image.load('sprites/pipe-green.png')
pipe_roof = pygame.transform.scale2x(pipe_roof)
pipe_roof = pygame.transform.rotate(pipe_roof, 180)

pipe_list = []

SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200)

######################################################################################################################################

def draw_floor():
    screen.blit(floor_surface,(floor_x_pos,900))
    screen.blit(floor_surface,(floor_x_pos + 576,900))

def create_pipe():
    pipe_random_movement = random.randint(1, 400)
    new_pipes = [pipe_surface.get_rect(midtop = (600, 312 + pipe_random_movement)), pipe_roof.get_rect(midtop = (600, -512 + pipe_random_movement))]
    return new_pipes

def move_pipes(pipes):  
    for pipe in pipes:
        pipe[0].centerx -= pipe_movement
        pipe[1].centerx -= pipe_movement 
    return pipes

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
    screen.blit(game_over_surface, (100, 200))
    game_is_running = False

def restart_game():
    global gravity
    global bird_movement
    global floor_movement
    global pipe_movement
    global pipe_list
    global game_is_running
    gravity = 0.25
    bird_movement = 0
    floor_movement = 1
    pipe_movement = 5
    pipe_list = []
    bird_rect.centery = bird_starting_height
    game_is_running = True

######################################################################################################################################

while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #makes the X button work on window
            event.type = pygame.quit
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_is_running:
                bird_movement = 0
                bird_movement -= 8
            if event.key == pygame.K_SPACE and not game_is_running:
                restart_game()
        if event.type == SPAWNPIPE and game_is_running:
            pipe_list.append(create_pipe())

    #set img
    screen.blit(bg_surface,(0,0))

    #Bird
    bird_movement += gravity
    bird_rect.centery += bird_movement
    screen.blit(bird_surface, bird_rect)

    #Pipes
    pipe_list = move_pipes(pipe_list)
    draw_pipes(pipe_list)
    check_collisions(pipe_list)

    #Floor
    floor_x_pos -= floor_movement
    draw_floor()
    screen.blit(floor_surface,(floor_x_pos,900))
    if floor_x_pos <= -576:
        floor_x_pos = 0
    #takes everything before and draws it
    pygame.display.update()
    #set framerate to 120fps
    clock.tick(120)