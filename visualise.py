import pygame
from steering_behaviours import *
import get_input_keys
from dataclasses import dataclass
from typing import *
from motion import *

#TODO display other keyboard shortcuts on screen
#TODO Add state machine to cycle through behaviours

@dataclass
class Agent:
    x: int = 400
    y: int = 300
    vx: int = 0
    vy: int = 0

#a test using pygame
def main():
    import pygame
    pygame.init()
    pygame.font.init()
    myfont = pygame.font.SysFont('Comic Sans MS', 15)
    myfont2 = pygame.font.SysFont('Comic Sans MS', 10)
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    running = True
    trail: List[Tuple[float, float, int]] = []
    agents = [Agent()]
    current_behaviours = [STEERING_BEHAVIOUR.SEEK, STEERING_BEHAVIOUR.FRICTION]

    while running:
        running = main_loop(
            screen,
            clock,
            agents,
            current_behaviours,
            myfont,
            myfont2,
            trail
        )

def main_loop(
    screen: pygame.Surface,
    clock: pygame.time.Clock,
    agents: List[Agent],
    current_behaviours: List[STEERING_BEHAVIOUR],
    myfont: pygame.font.Font,
    myfont2: pygame.font.Font,
    trail: List[Tuple[float, float, int]]
):

    screen.fill((0, 0, 0))

    #GET INPUT
    dt = clock.tick()/1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    target_x, target_y = pygame.mouse.get_pos()
    get_input_keys.toggle_behaviours(current_behaviours)
    get_input_keys.add_remove_element(agents, Agent)
    max_attraction = get_input_keys.change_max_attraction(myfont, screen)
    max_repulsion = get_input_keys.change_max_repulsion(myfont, screen)
    deceleration_radius = get_input_keys.change_deceleration_radius(myfont, screen)
    max_speed = get_input_keys.change_max_speed(myfont, screen)
    friction_constant = get_input_keys.change_friction_constant(myfont, screen)
    repulsion_radius = get_input_keys.change_repulsion_radius(myfont, screen)
    show_trail = get_input_keys.toggle_trail()
    draw_forces = get_input_keys.toggle_draw_forces()

    for i, agent in enumerate(agents):
        #simulate
        behaviour_forces = []
        for current_behaviour in current_behaviours:
            f = apply_behaviour(
                current_behaviour=current_behaviour,
                current_pos=(agent.x, agent.y),
                current_vel=(agent.vx, agent.vy),
                target_pos=(target_x, target_y),
                repulsors=[(other.x,other.y) for other in agents if other is not agent],
                max_attraction=max_attraction,
                deceleration_radius=deceleration_radius,
                friction_constant=friction_constant,
                repulsion_radius=repulsion_radius,
                max_repulsion=max_repulsion,
            )
            behaviour_forces.append(f)

        fx, fy = combine(behaviour_forces)
        acc_x, acc_y = force((fx, fy), 1)
        agent.vx, agent.vy = direct((agent.vx, agent.vy), (max_speed, max_speed), (acc_x, acc_y), dt)
        agent.x, agent.y = step((agent.x, agent.y), (agent.vx, agent.vy), dt)

        trail.append((agent.x, agent.y, pygame.time.get_ticks()))
    
        #draw
        pygame.draw.circle(screen, (0, 0, 255), (agent.x, agent.y), 10)
        if i == 0 and draw_forces:
            draw_forces_and_vel(
                behaviours = current_behaviours,
                behaviour_forces=behaviour_forces,
                screen=screen,
                agent=agent,
                myfont=myfont2,
                fx=fx,
                fy=fy
            )
        if show_trail: draw_trail(trail, screen)

    #write current behaviours at top center of screen in white if enabled, grey if disabled
    for i, behaviour in enumerate(STEERING_BEHAVIOUR):
        if behaviour in current_behaviours:
            textsurface = myfont.render(f"{i} {behaviour.name}", False, (255, 255, 255))
        else:
            textsurface = myfont.render(f"{i} {behaviour.name}", False, (100, 100, 100))
        screen.blit(textsurface, (400 - textsurface.get_width()/2, 20 + i * 20))

    #draw target mouse as a red circle
    pygame.draw.circle(screen, (255, 0, 0), (target_x, target_y), 10)

    pygame.display.flip()
    return True


def draw_forces_and_vel(behaviours, behaviour_forces, screen, agent, myfont, fx, fy):
        scale = 0.1
        #draw behaviour forces as a green line with text "fi" where i is the index (scaled)
        for b, f in zip(behaviours, behaviour_forces):
            pygame.draw.line(screen, (0, 255, 0), (agent.x, agent.y), (agent.x + f[0] * scale, agent.y + f[1] * scale))
            textsurface = myfont.render(b.name, False, (0, 255, 0))
            screen.blit(textsurface, (agent.x + f[0] * scale, agent.y + f[1] * scale))
        #draw resultant force vector as a red line with text "f" (scaled)
        pygame.draw.line(screen, (255, 0, 0), (agent.x, agent.y), (agent.x + fx * scale, agent.y + fy * scale))
        textsurface = myfont.render('f', False, (255, 0, 0))
        screen.blit(textsurface, (agent.x + fx * scale, agent.y + fy * scale))
        #draw velocity vector as a yellow line with text "v"
        pygame.draw.line(screen, (255, 255, 0), (agent.x, agent.y), (agent.x + agent.vx, agent.y + agent.vy))
        textsurface = myfont.render('v', False, (255, 255, 0))
        screen.blit(textsurface, (agent.x + agent.vx, agent.y + agent.vy))

def draw_trail(trail, screen):
    #draw trail as a white line, more black the further back in time
    current_time = pygame.time.get_ticks()            
    for x, y, t in trail:
        #get more black the further back in time
        colour = 255 - (current_time - t) / 2000 * 255
        if colour > 0:
            pygame.draw.line(screen, (colour,colour,colour), (x, y), (x, y))
        else:
            trail.remove((x, y, t))

if __name__ == "__main__":
    main()

