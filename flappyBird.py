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


bg_surface = pygame.image.load('sprites/background-day.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)
  
floor_surface = pygame.image.load('sprites/base.png')
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

game_is_running = True

bird_surface = pygame.image.load('sprites/bluebird-midflap.png').convert()
bird_surface = pygame.transform.scale2x(bird_surface)
bird_rect = bird_surface.get_rect(center = (100,512))

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
    new_pipe = pipe_surface.get_rect(midtop = (600,312 + pipe_random_movement))
    return new_pipe

def move_pipes(pipes):  
    for pipe in pipes:
        pipe.centerx -= pipe_movement
    return pipes
def draw_pipes(pipes):
    for pipe in pipes:
        screen.blit(pipe_surface, pipe)
        screen.blit(pipe_roof, pipe.move(0, -812)) 

def check_collisions():
        if bird_rect.y >= 850:
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
            game_over()

def game_over():
    game_over_font = pygame.font.Font("freesansbold.ttf", 60)
    display_game_over = game_over_font.render("Game over", True, green, blue)
    screen.blit(display_game_over, (200, 300))

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
    #if bird_rect == pipe_roof || pipe_surface
    #Floor
    floor_x_pos -= floor_movement
    draw_floor()
    screen.blit(floor_surface,(floor_x_pos,900))
    if floor_x_pos <= -576:
        floor_x_pos = 0
    check_collisions()
    #takes everything before and draws it
    pygame.display.update()
    #set framerate to 120fps
    clock.tick(120)