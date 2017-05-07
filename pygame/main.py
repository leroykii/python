import pygame
import time
from pygame.locals import *
import classdefs

# To execute: $ python main.py

[a, b] = pygame.init()
print ("Modules loaded: ", a, "--- Module errors: ", b)

screen = pygame.display.set_mode((800, 600))

background = pygame.Surface(screen.get_size())
background.fill((0, 0, 0))

# instantiate our player; right now he's just a rectangle
player = classdefs.Player()
player.rect.x = 400
player.rect.y = 300

enemies = pygame.sprite.Group()
food = pygame.sprite.Group()
venomous_food = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
bullets = pygame.sprite.Group()
bosses = pygame.sprite.Group()

# Program events
ADDENEMY = pygame.USEREVENT + 1
ADDFOOD = pygame.USEREVENT + 2
ADDVENOMOUSFOOD = pygame.USEREVENT + 3
VENOMSTATE = pygame.USEREVENT + 4
ADDBOSS = pygame.USEREVENT + 5
pygame.time.set_timer(ADDENEMY, 1000)
pygame.time.set_timer(ADDFOOD, 500)
pygame.time.set_timer(ADDVENOMOUSFOOD, 2000)
pygame.time.set_timer(ADDBOSS, 6800)

# Set score
font = pygame.font.Font(None, 36)
text_r = font.render("Score: " + str(player.points), 1, (0, 255, 127))
textpos = text_r.get_rect(centerx=background.get_width() / 2)

# Variable to keep our main loop running
running = True

# Our main loop!
while running:
    # for loop through the event queue
    for event in pygame.event.get():
        # Check for KEYDOWN event; KEYDOWN is a constant defined in
        # pygame.locals, which we imported earlier
        if event.type == KEYDOWN:
            # If the Esc key has been pressed set running to false to exit the
            # main loop
            if event.key == K_ESCAPE or event.key == K_c:
                running = False
            elif event.key == K_SPACE:
                new_bullet = classdefs.Shoot(player.rect)
                bullets.add(new_bullet)
                all_sprites.add(new_bullet)

        # Check for QUIT event; if QUIT, set running to false
        elif event.type == QUIT:
            running = False

        elif event.type == ADDENEMY:
            new_enemy = classdefs.Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        elif event.type == ADDFOOD:
            new_food = classdefs.Food()
            new_food.surf = pygame.Surface((10, 10))
            new_food.surf.fill((0, 255, 0))
            food.add(new_food)
            all_sprites.add(new_food)

        elif event.type == ADDVENOMOUSFOOD:
            new_vfood = classdefs.VenomousFood()
            new_vfood.surf = pygame.Surface((10, 10))
            new_vfood.surf.fill((255, 0, 0))
            venomous_food.add(new_vfood)
            all_sprites.add(new_vfood)

        elif event.type == VENOMSTATE:
            pygame.time.set_timer(VENOMSTATE, 0)  # Delete timer
            player.velocity = 2
            print("Got back to normal state")

        elif event.type == ADDBOSS:
            new_boss = classdefs.Boss()
            bosses.add(new_boss)
            all_sprites.add(new_boss)

    pressed_keys = pygame.key.get_pressed()

    player.update(pressed_keys)
    enemies.update()
    food.update()
    venomous_food.update()
    bullets.update()
    bosses.update()

    collided_enemy = pygame.sprite.spritecollideany(player, enemies)
    if collided_enemy:
        print("You are DEAD! :(")
        collided_enemy.kill()
        player.kill()
        time.sleep(1)
        running = False

    collided_food = pygame.sprite.spritecollideany(player, food)
    if collided_food:
        collided_food.kill()
        player.points += 1
        print("Points: ", player.points)

    collided_vfood = pygame.sprite.spritecollideany(player, venomous_food)
    if collided_vfood:
        collided_vfood.kill()
        player.points -= 5
        print("Points: ", player.points)
        # Create timer
        pygame.time.set_timer(VENOMSTATE, 4000)
        # Increase speed
        player.velocity = 1
        print("Got poisoned")

    for entity in bullets:
        collided_boss = pygame.sprite.spritecollideany(entity, bosses)
        if collided_boss:
            player.points += 1
            entity.kill()  # Delete bullet
            collided_boss.hits += 1
            if (collided_boss.hits == 5):
                collided_boss.kill()
                player.points += 10

    # Update screen
    screen.blit(background, (0, 0))
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Update score and render text
    text_r = font.render("Score: " + str(player.points), 1, (0, 255, 127))
    screen.blit(text_r, textpos)

    # Update the display
    pygame.display.flip()

    # time.sleep(0.1)
