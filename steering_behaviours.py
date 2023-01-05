from typing import List
import math
from motion import Pos, Vel, Force

def seek(current: Pos, target: Pos, max_attraction: float) -> Force:
    dx = target[0] - current[0]
    dy = target[1] - current[1]
    theta = math.atan2(dy, dx)
    force_x = math.cos(theta) * max_attraction
    force_y = math.sin(theta) * max_attraction
    return Force((force_x, force_y))

def flee(current: Pos, target: Pos, max_repulsion: float) -> Force:
    dx = target[0] - current[0]
    dy = target[1] - current[1]
    theta = math.atan2(dy, dx)
    force_x = math.cos(theta) * -max_repulsion
    force_y = math.sin(theta) * -max_repulsion
    return Force((force_x, force_y))

def arrive(current: Pos, target: Pos, max_attraction: float, deceleration_radius: float) -> Force:
    """Like Seek behavior but decelerates to be at zero speed on target"""
    dx = target[0] - current[0]
    dy = target[1] - current[1]
    distance = math.sqrt(dx * dx + dy * dy)
    if distance > deceleration_radius:
        return seek(current, target, max_attraction)
    else:
        return seek(current, target, max_attraction * (distance / deceleration_radius))

#randomly move areound within a circular area
#TODO test
import random
def wander(current: Pos, wander_center: Pos, wander_radius: float) -> Force:
    dx = current[0] - wander_center[0]
    dy = current[1] - wander_center[1]
    theta = math.atan2(dy, dx)
    theta += random.uniform(-math.pi, math.pi)
    force_x = math.cos(theta) * wander_radius
    force_y = math.sin(theta) * wander_radius
    return Force((force_x, force_y))

#raycast avoidance
#TODO test
def raycast_avoidance(current_pos: Pos, current_vel: Vel, target: Pos, obstacles: List[Pos], raycast_length: float, max_repulsion: float) -> Force:
    raycast_angle = math.atan2(current_vel[1], current_vel[0])
    raycast_x = current_pos[0] + math.cos(raycast_angle) * raycast_length
    raycast_y = current_pos[1] + math.sin(raycast_angle) * raycast_length
    raycast = Pos((raycast_x, raycast_y))
    closest_obstacle = (None, None) #obstacle, distance
    for obstacle in obstacles:
        dx = raycast[0] - obstacle[0]
        dy = raycast[1] - obstacle[1]
        distance = math.sqrt(dx * dx + dy * dy)
        if closest_obstacle[1] is None or distance < closest_obstacle[1]:
            closest_obstacle = (obstacle, distance)
    if closest_obstacle[1] is None:
        return Force((0, 0))
    else:
        #return a force away from the obstacle
        obstacle = closest_obstacle[0]
        dx = obstacle[0] - current_pos[0]
        dy = obstacle[1] - current_pos[1]
        theta = math.atan2(dy, dx)
        force_x = math.cos(theta) * -1 * max_repulsion
        force_y = math.sin(theta) * -1 * max_repulsion
        return Force((force_x, force_y))

#repulsion from other agents
#TODO test
def repulsion(current_pos: Pos, agents: List[Pos], repulsion_radius: float, max_repulsion: float) -> Force:
    force_x = 0
    force_y = 0
    for agent in agents:
        dx = agent[0] - current_pos[0]
        dy = agent[1] - current_pos[1]
        distance = math.sqrt(dx * dx + dy * dy)
        if distance < repulsion_radius:
            theta = math.atan2(dy, dx)
            force_x += math.cos(theta) * -1 * max_repulsion
            force_y += math.sin(theta) * -1 * max_repulsion
    return Force((force_x, force_y))

def friction(current_vel: Vel, friction: float) -> Force:
    force_x = -current_vel[0] * friction
    force_y = -current_vel[1] * friction
    return Force((force_x, force_y))

def combine(forces: List[Force]) -> Force:
    force_x = 0.0
    force_y = 0.0
    for force in forces:
        force_x += force[0]
        force_y += force[1]
    return Force((force_x, force_y))

from enum import Enum
class STEERING_BEHAVIOUR(Enum):
    FRICTION = 0
    SEEK = 1
    FLEE = 2
    ARRIVE = 3
    REPULSE = 4


def apply_behaviour(
    current_behaviour: STEERING_BEHAVIOUR,
    current_pos: Pos,
    current_vel: Vel,
    target_pos: Pos,
    repulsors: List[Pos],
    max_attraction=1000,
    deceleration_radius=300,
    friction_constant=10,
    repulsion_radius=100,
    max_repulsion=1000,
    ) -> Force:

    if current_behaviour == STEERING_BEHAVIOUR.FRICTION:
        f1_x, f2_x = friction(current_vel, friction_constant)
    elif current_behaviour == STEERING_BEHAVIOUR.SEEK:
        f1_x, f2_x = seek(current_pos, target_pos, max_attraction)
    elif current_behaviour == STEERING_BEHAVIOUR.FLEE:
        f1_x, f2_x = flee(current_pos, target_pos, max_repulsion)
    elif current_behaviour == STEERING_BEHAVIOUR.ARRIVE:
        f1_x, f2_x = arrive(current_pos, target_pos, max_attraction, deceleration_radius)
    elif current_behaviour == STEERING_BEHAVIOUR.REPULSE:
        f1_x, f2_x = repulsion(current_pos, repulsors, repulsion_radius, max_repulsion)
        
    else:
        raise Exception("Unknown behaviour")
    return Force((f1_x, f2_x))