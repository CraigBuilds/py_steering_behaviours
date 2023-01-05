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

time_of_last_pause = datetime.datetime.now()
paused = False
def pause() -> bool:
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

time_of_last_trail_toggle = datetime.datetime.now()
trails = True
def toggle_trail() -> bool:
    #toggle trail on and off when right shift button is pressed.
    #limit the toggle rate to 0.1 seconds
    global time_of_last_trail_toggle
    global trails
    now = datetime.datetime.now()
    if now - time_of_last_trail_toggle > datetime.timedelta(seconds=0.1):
        time_of_last_trail_toggle = now
        if pygame.key.get_pressed()[pygame.K_RSHIFT]:
            trails = not trails
            print(f"trails {trails}")

    return trails

time_of_last_draw_forces_toggle = datetime.datetime.now()
draw_forces = True
def toggle_draw_forces() -> bool:
    #toggle draw_forces on and off when right control button is pressed.
    #limit the toggle rate to 0.1 seconds
    global time_of_last_draw_forces_toggle
    global draw_forces
    now = datetime.datetime.now()
    if now - time_of_last_draw_forces_toggle > datetime.timedelta(seconds=0.1):
        time_of_last_draw_forces_toggle = now
        if pygame.key.get_pressed()[pygame.K_RCTRL]:
            draw_forces = not draw_forces
            print(f"draw_forces {draw_forces}")

    return draw_forces

"""
Parameters for steering behaviours
"""

max_atraction = 1000
time_of_last_attraction_change = datetime.datetime.now()
def change_max_attraction(my_font, screen) -> int:
    """
    Increase max attraction if a button is pressed, decrease if z button is pressed.
    Display current value onscreen as text uppon change and fade out to black.
    """
    global time_of_last_attraction_change
    global max_atraction
    now = datetime.datetime.now()
    if now - time_of_last_attraction_change > datetime.timedelta(seconds=0.1):
        time_of_last_attraction_change = now
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            max_atraction += 100
        if keys[pygame.K_z]:
            max_atraction -= 100
    
    text = my_font.render(f"max_atraction a/z {max_atraction}", False, (255, 255, 255))
    #draw on screen
    screen.blit(text, (0, 0))
    return max_atraction

friction_constant = 10
time_of_last_friction_change = datetime.datetime.now()
def change_friction_constant(my_font, screen) -> int:
    """
    Increase friction constant if f button is pressed, decrease if v button is pressed.
    Display current value onscreen as text uppon change and fade out to black.
    """
    global time_of_last_friction_change
    global friction_constant
    now = datetime.datetime.now()
    if now - time_of_last_friction_change > datetime.timedelta(seconds=0.1):
        time_of_last_friction_change = now
        keys = pygame.key.get_pressed()
        if keys[pygame.K_f]:
            friction_constant += 1
        if keys[pygame.K_v]:
            friction_constant -= 1
    
    text = my_font.render(f"friction_constant f/v {friction_constant}", False, (255, 255, 255))
    #draw on screen
    screen.blit(text, (0, 20))
    return friction_constant

deceleration_radius = 300
time_of_last_deceleration_change = datetime.datetime.now()
def change_deceleration_radius(my_font, screen) -> int:
    """
    Increase deceleration radius if d button is pressed, decrease if c button is pressed.
    Display current value onscreen as text uppon change and fade out to black.
    """
    global time_of_last_deceleration_change
    global deceleration_radius
    now = datetime.datetime.now()
    if now - time_of_last_deceleration_change > datetime.timedelta(seconds=0.1):
        time_of_last_deceleration_change = now
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            deceleration_radius += 10
        if keys[pygame.K_c]:
            deceleration_radius -= 10
    
    text = my_font.render(f"deceleration_radius d/c {deceleration_radius}", False, (255, 255, 255))
    #draw on screen
    screen.blit(text, (0, 40))
    return deceleration_radius

repulsion_radius = 100
time_of_last_repulsion_change = datetime.datetime.now()
def change_repulsion_radius(my_font, screen) -> int:
    """
    Increase repulsion radius if r button is pressed, decrease if e button is pressed.
    Display current value onscreen as text uppon change and fade out to black.
    """
    global time_of_last_repulsion_change
    global repulsion_radius
    now = datetime.datetime.now()
    if now - time_of_last_repulsion_change > datetime.timedelta(seconds=0.1):
        time_of_last_repulsion_change = now
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            repulsion_radius += 10
        if keys[pygame.K_e]:
            repulsion_radius -= 10
    
    text = my_font.render(f"repulsion_radius r/e {repulsion_radius}", False, (255, 255, 255))
    #draw on screen
    screen.blit(text, (0, 60))
    return repulsion_radius

max_repulsion = 1000
time_of_last_max_repulsion_change = datetime.datetime.now()
def change_max_repulsion(my_font, screen) -> int:
    """
    Increase max repulsion if t button is pressed, decrease if g button is pressed.
    Display current value onscreen as text uppon change and fade out to black.
    """
    global time_of_last_max_repulsion_change
    global max_repulsion
    now = datetime.datetime.now()
    if now - time_of_last_max_repulsion_change > datetime.timedelta(seconds=0.1):
        time_of_last_max_repulsion_change = now
        colour = (255, 255, 255) #white
        keys = pygame.key.get_pressed()
        if keys[pygame.K_t]:
            max_repulsion += 100
        if keys[pygame.K_g]:
            max_repulsion -= 100
    
    text = my_font.render(f"max_repulsion t/g {max_repulsion}", False, (255, 255, 255))
    #draw on screen
    screen.blit(text, (0, 80))
    return max_repulsion

max_speed = 100
time_of_last_max_speed_change = datetime.datetime.now()
def change_max_speed(my_font, screen) -> int:
    """
    Increase max speed if y button is pressed, decrease if h button is pressed.
    Display current value onscreen as text uppon change and fade out to black.
    """
    global time_of_last_max_speed_change
    global max_speed
    now = datetime.datetime.now()
    if now - time_of_last_max_speed_change > datetime.timedelta(seconds=0.1):
        time_of_last_max_speed_change = now
        colour = (255, 255, 255) #white
        keys = pygame.key.get_pressed()
        if keys[pygame.K_y]:
            max_speed += 10
        if keys[pygame.K_h]:
            max_speed -= 10
    
    text = my_font.render(f"max_speed y/h {max_speed}", False, (255, 255, 255))
    #draw on screen
    screen.blit(text, (0, 100))
    return max_speed