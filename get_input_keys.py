import pygame
from steering_behaviours import *
import datetime


def toggle(behaviour: STEERING_BEHAVIOUR, current_behaviours: List[STEERING_BEHAVIOUR]):
    if behaviour in current_behaviours:
        print(f"{behaviour.name} off")
        current_behaviours.remove(behaviour)
    else:
        print(f"{behaviour.name} on")
        current_behaviours.append(behaviour)

time_of_last_toggle = datetime.datetime.now()
def toggle_behaviours(current_behaviours: List[STEERING_BEHAVIOUR]):
    #toggle behaviours on and off when keys 1 to 10 are pressed.
    #limit the toggle rate to 0.1 seconds
    global time_of_last_toggle
    now = datetime.datetime.now()
    if now - time_of_last_toggle > datetime.timedelta(seconds=0.1):
        time_of_last_toggle = now
        keys = pygame.key.get_pressed()
        if keys[pygame.K_0]:
            toggle(STEERING_BEHAVIOUR.FRICTION, current_behaviours)
        if keys[pygame.K_1]:
            toggle(STEERING_BEHAVIOUR.SEEK, current_behaviours)
        if keys[pygame.K_2]:
            toggle(STEERING_BEHAVIOUR.FLEE, current_behaviours)
        if keys[pygame.K_3]:
            toggle(STEERING_BEHAVIOUR.ARRIVE, current_behaviours)
        if keys[pygame.K_4]:
            toggle(STEERING_BEHAVIOUR.REPULSE, current_behaviours)

time_of_last_pause = datetime.datetime.now()
paused = False
def pause():
    #pause if right space button is pressed.
    #limit the pause rate to 0.1 seconds
    global time_of_last_pause
    global paused
    now = datetime.datetime.now()
    if now - time_of_last_pause > datetime.timedelta(seconds=0.1):
        time_of_last_pause = now
        if pygame.mouse.get_pressed()[2]:
            paused = not paused
            print(f"pause {paused}")

    return paused

time_of_last_element_change = datetime.datetime.now()
def add_remove_element(list: List, Element: type):
    """
    Add to list if + button is pressed, remove from list if - button is pressed.
    """
    global time_of_last_element_change
    now = datetime.datetime.now()
    if now - time_of_last_element_change > datetime.timedelta(seconds=0.1):
        time_of_last_element_change = now
        keys = pygame.key.get_pressed()
        if keys[pygame.K_EQUALS]:
            print(f"add {Element}")
            list.append(Element())
        if keys[pygame.K_MINUS]:
            print(f"remove")
            try:
                list.pop()
            except IndexError:
                pass

"""
properties:
    max_attraction=1000,
    deceleration_radius=300,
    friction_constant=10,
    repulsion_radius=100,
    max_repulsion=1000,
"""

max_atraction = 1000
time_of_last_attraction_change = datetime.datetime.now()
def change_max_attraction(my_font, screen) -> int:
    """
    Increase max attraction if ] button is pressed, decrease if [ button is pressed.
    Display current value onscreen as text uppon change and fade out to black.
    """
    global time_of_last_attraction_change
    global max_atraction
    now = datetime.datetime.now()
    if now - time_of_last_attraction_change > datetime.timedelta(seconds=0.1):
        time_of_last_attraction_change = now
        colour = (255, 255, 255) #white
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHTBRACKET]:
            max_atraction += 100
        if keys[pygame.K_LEFTBRACKET]:
            max_atraction -= 100
    
    text = my_font.render(f"max_atraction [ ] {max_atraction}", False, (255, 255, 255))
    #draw on screen
    screen.blit(text, (0, 0))
    return max_atraction

deceleration_radius = 300
time_of_last_deceleration_change = datetime.datetime.now()
def change_deceleration_radius(my_font, screen) -> int:
    """
    Increase deceleration radius if } button is pressed, decrease if { button is pressed.
    Display current value onscreen as text uppon change and fade out to black.
    """
    global time_of_last_deceleration_change
    global deceleration_radius
    now = datetime.datetime.now()
    if now - time_of_last_deceleration_change > datetime.timedelta(seconds=0.1):
        time_of_last_deceleration_change = now
        colour = (255, 255, 255) #white
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            deceleration_radius += 10
        if keys[pygame.K_LEFT]:
            deceleration_radius -= 10
    
    text = my_font.render(f"deceleration_radius {{ }} {deceleration_radius}", False, (255, 255, 255))
    #draw on screen
    screen.blit(text, (0, 20))
    return deceleration_radius

friction_constant = 10
time_of_last_friction_change = datetime.datetime.now()
def change_friction_constant(my_font, screen) -> int:
    """
    Increase friction constant if / button is pressed, decrease if . button is pressed.
    Display current value onscreen as text uppon change and fade out to black.
    """
    global time_of_last_friction_change
    global friction_constant
    now = datetime.datetime.now()
    if now - time_of_last_friction_change > datetime.timedelta(seconds=0.1):
        time_of_last_friction_change = now
        colour = (255, 255, 255) #white
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SLASH]:
            friction_constant += 1
        if keys[pygame.K_PERIOD]:
            friction_constant -= 1
    
    text = my_font.render(f"friction_constant . / {friction_constant}", False, (255, 255, 255))
    #draw on screen
    screen.blit(text, (0, 40))
    return friction_constant

repulsion_radius = 100
time_of_last_repulsion_change = datetime.datetime.now()
def change_repulsion_radius(my_font, screen) -> int:
    """
    Increase repulsion radius if > button is pressed, decrease if < button is pressed.
    Display current value onscreen as text uppon change and fade out to black.
    """
    global time_of_last_repulsion_change
    global repulsion_radius
    now = datetime.datetime.now()
    if now - time_of_last_repulsion_change > datetime.timedelta(seconds=0.1):
        time_of_last_repulsion_change = now
        colour = (255, 255, 255) #white
        keys = pygame.key.get_pressed()
        if keys[pygame.K_COMMA]:
            repulsion_radius += 10
        if keys[pygame.K_LESS]:
            repulsion_radius -= 10
    
    text = my_font.render(f"repulsion_radius < > {repulsion_radius}", False, (255, 255, 255))
    #draw on screen
    screen.blit(text, (0, 60))
    return repulsion_radius

max_repulsion = 1000
time_of_last_max_repulsion_change = datetime.datetime.now()
def change_max_repulsion(my_font, screen) -> int:
    """
    Increase max repulsion if ; button is pressed, decrease if # button is pressed.
    Display current value onscreen as text uppon change and fade out to black.
    """
    global time_of_last_max_repulsion_change
    global max_repulsion
    now = datetime.datetime.now()
    if now - time_of_last_max_repulsion_change > datetime.timedelta(seconds=0.1):
        time_of_last_max_repulsion_change = now
        colour = (255, 255, 255) #white
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SEMICOLON]:
            max_repulsion += 100
        if keys[pygame.K_HASH]:
            max_repulsion -= 100
    
    text = my_font.render(f"max_repulsion ; # {max_repulsion}", False, (255, 255, 255))
    #draw on screen
    screen.blit(text, (0, 80))
    return max_repulsion