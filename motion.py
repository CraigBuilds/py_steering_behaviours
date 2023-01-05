from typing import NewType, Tuple

Pos=NewType('Pos',Tuple[float,float])
Vel=NewType('Vel',Tuple[float,float])
Acc=NewType('Acc',Tuple[float,float])
Force=NewType('Force',Tuple[float,float])
Sec=NewType('Sec',float)
Mass=NewType('Mass',float)

#use vel, get pos
def step(current: Pos, vel: Vel, dt: Sec) -> Pos:
    new_x = current[0] + vel[0] * dt
    new_y = current[1] + vel[1] * dt
    return Pos((new_x, new_y))

#use acc, get vel
def direct(current: Vel, max_vel: Vel, acc: Acc, dt: Sec) -> Vel:
    new_x = current[0] + acc[0] * dt
    new_y = current[1] + acc[1] * dt
    if new_x > max_vel[0] or new_x < -max_vel[0]:
        new_x = current[0]
    if new_y > max_vel[1] or new_y < -max_vel[1]:
        new_y = current[1]
    return Vel((new_x, new_y))

#use force, get acc
def force(force: Force, mass: Mass) -> Acc:
    acc_x = force[0] / mass
    acc_y = force[1] / mass
    return Acc((acc_x, acc_y))