#!/usr/bin/env python
# coding: utf-8
import numpy as np

# PARAMETERS

GAMMA = 0.999  # discount factor
DELTA = 1e-3  # bellman error
STEPCOST = -5  # timestep penalty


class Position:
    '''Class to store parameters about a position, and to easily find final position after movement.'''

    def __init__(self, name, acts, prob1, prob2, prob3=0):
        self.name = name
        self.move_prob = prob1  # up, down, left, right, stay
        self.spec_prob = prob2  # hit, craft, gather
        self.shoot_prob = prob3  # shoot
        self.actions = list(np.array(actions)[acts])

    def up(self):
        i = positions.index(self)
        return positions[i+1]

    def down(self):
        i = positions.index(self)
        return positions[i-1]

    def right(self):
        i = positions.index(self)
        return positions[i+2]

    def left(self):
        i = positions.index(self)
        return positions[i-2]

    def default(self):
        return positions[-1]

# STATE VARIABLES


actions = ['UP', 'LEFT', 'DOWN', 'RIGHT', 'STAY',
           'SHOOT', 'HIT', 'CRAFT', 'GATHER', 'NONE']

center = Position('C', [0, 1, 2, 3, 4, 5, 6], 0.85, 0.1, 0.5)
north = Position('N', [2, 4, 7], 0.85, [0.5, 0.35, 0.15])
south = Position('S', [0, 4, 8], 0.85, 0.75)
east = Position('E', [1, 4, 5, 6], 1, 0.2, 0.9)
west = Position('W', [3, 4, 5], 1, 0, 0.25)

positions = [west, south, center, north, east]
mm_state = ['D', 'R']


def get_states():
    '''Returns a dictionary with all state tuples as keys and an array of optimal action-utility pairs as the value, initialised to ['NONE', 0]'''
    newdict = {}
    for pos in positions:
        for mat in range(0, 3):
            for arrow in range(0, 4):
                for mm in range(0, 2):
                    for health in range(0, 5):
                        newdict.update(
                            {(pos, mat, arrow, mm, health*25): [[actions[-1], 0]]})
    return newdict


def num_iter(dicx):
    '''Returns number of iterations for the input states dictionary'''
    return len(list(dicx.values())[0])


def get_util(state, itr, **kwargs):
    '''Returns the utility of the state obtained after given changes relative to the input state. Gives utility of the input state if no changes are specified.'''
    p, m, a, s, h = state
    p = kwargs.get('pos', p)
    m = kwargs.get('mat', m)
    a = kwargs.get('arrow', a)
    s = kwargs.get('mm', s)
    h = kwargs.get('health', h)
    newstate = (p, m, a, s, h)
    return states[newstate][itr][1]


def iteration(itr):
    '''A single iteration of MDP for all 600 states'''
    for state in states:
        global diff
        pos, mat, arrow, mm, health = state
        u_t1 = {}
        p1 = pos.move_prob
        p2 = pos.spec_prob

        if health:
            if mm:  # READY
                regain = health+25 if health < 100 else 100
                u_failure = get_util(state, itr, arrow=0, mm=0, health=regain)
                penalty = -40 if pos == east or pos == center else 0
                # action: UP
                if 'UP' in pos.actions:
                    u_success = get_util(state, itr, pos=pos.up())
                    u_default = get_util(state, itr, pos=pos.default())
                    u_independant = p1 * \
                        (STEPCOST + GAMMA*u_success) + \
                        (1-p1)*(STEPCOST + GAMMA*u_default)
                    if penalty == 0:
                        u_success_d = get_util(state, itr, pos=pos.up(), mm=0)
                        u_default_d = get_util(
                            state, itr, pos=pos.default(), mm=0)
                        u_dormant = p1 * \
                            (STEPCOST + GAMMA*u_success_d) + \
                            (1-p1)*(STEPCOST + GAMMA*u_default_d)
                        util = 0.5*(u_independant) + 0.5*(u_dormant)
                    else:
                        util = 0.5*(u_independant) + 0.5 * \
                            (STEPCOST + penalty + GAMMA*u_failure)
                    u_t1.update({util: 'UP'})

                # action: LEFT
                if 'LEFT' in pos.actions:
                    u_success = get_util(state, itr, pos=pos.left())
                    u_default = get_util(state, itr, pos=pos.default())
                    u_independant = p1 * \
                        (STEPCOST + GAMMA*u_success) + \
                        (1-p1)*(STEPCOST + GAMMA*u_default)
                    if penalty == 0:
                        u_success_d = get_util(
                            state, itr, pos=pos.left(), mm=0)
                        u_default_d = get_util(
                            state, itr, pos=pos.default(), mm=0)
                        u_dormant = p1 * \
                            (STEPCOST + GAMMA*u_success_d) + \
                            (1-p1)*(STEPCOST + GAMMA*u_default_d)
                        util = 0.5*(u_independant) + 0.5*(u_dormant)
                    else:
                        util = 0.5*(u_independant) + 0.5 * \
                            (STEPCOST + penalty + GAMMA*u_failure)
                    u_t1.update({util: 'LEFT'})

                # action: DOWN
                if 'DOWN' in pos.actions:
                    u_success = get_util(state, itr, pos=pos.down())
                    u_default = get_util(state, itr, pos=pos.default())
                    u_independant = p1 * \
                        (STEPCOST + GAMMA*u_success) + \
                        (1-p1)*(STEPCOST + GAMMA*u_default)
                    if penalty == 0:
                        u_success_d = get_util(
                            state, itr, pos=pos.down(), mm=0)
                        u_default_d = get_util(
                            state, itr, pos=pos.default(), mm=0)
                        u_dormant = p1 * \
                            (STEPCOST + GAMMA*u_success_d) + \
                            (1-p1)*(STEPCOST + GAMMA*u_default_d)
                        util = 0.5*(u_independant) + 0.5*(u_dormant)
                    else:
                        util = 0.5*(u_independant) + 0.5 * \
                            (STEPCOST + penalty + GAMMA*u_failure)
                    u_t1.update({util: 'DOWN'})

                # action: RIGHT
                if 'RIGHT' in pos.actions:
                    u_success = get_util(state, itr, pos=pos.right())
                    u_default = get_util(state, itr, pos=pos.default())
                    u_independant = p1 * \
                        (STEPCOST + GAMMA*u_success) + \
                        (1-p1)*(STEPCOST + GAMMA*u_default)
                    if penalty == 0:
                        u_success_d = get_util(
                            state, itr, pos=pos.right(), mm=0)
                        u_default_d = get_util(
                            state, itr, pos=pos.default(), mm=0)
                        u_dormant = p1 * \
                            (STEPCOST + GAMMA*u_success_d) + \
                            (1-p1)*(STEPCOST + GAMMA*u_default_d)
                        util = 0.5*(u_independant) + 0.5*(u_dormant)
                    else:
                        util = 0.5*(u_independant) + 0.5 * \
                            (STEPCOST + penalty + GAMMA*u_failure)
                    u_t1.update({util: 'RIGHT'})

                # action: STAY
                if 'STAY' in pos.actions:
                    u_success = get_util(state, itr)
                    u_default = get_util(state, itr, pos=pos.default())
                    u_independant = p1 * \
                        (STEPCOST + GAMMA*u_success) + \
                        (1-p1)*(STEPCOST + GAMMA*u_default)
                    if penalty == 0:
                        u_success_d = get_util(state, itr, mm=0)
                        u_default_d = get_util(
                            state, itr, pos=pos.default(), mm=0)
                        u_dormant = p1 * \
                            (STEPCOST + GAMMA*u_success_d) + \
                            (1-p1)*(STEPCOST + GAMMA*u_default_d)
                        util = 0.5*(u_independant) + 0.5*(u_dormant)
                    else:
                        util = 0.5*(u_independant) + 0.5 * \
                            (STEPCOST + penalty + GAMMA*u_failure)
                    u_t1.update({util: 'STAY'})

                # action: SHOOT
                if ('SHOOT' in pos.actions) and arrow:
                    reward = 50 if health == 25 else 0
                    p3 = pos.shoot_prob
                    u_success = get_util(
                        state, itr, arrow=arrow-1, health=health-25)
                    u_default = get_util(state, itr, arrow=arrow-1)
                    u_independant = p3 * \
                        (STEPCOST + reward + GAMMA*u_success) + \
                        (1-p3)*(STEPCOST + GAMMA*u_default)
                    if penalty == 0:
                        u_success_d = get_util(
                            state, itr, arrow=arrow-1, health=health-25, mm=0)
                        u_default_d = get_util(state, itr, arrow=arrow-1, mm=0)
                        u_dormant = p3 * \
                            (STEPCOST + reward + GAMMA*u_success_d) + \
                            (1-p3)*(STEPCOST + GAMMA*u_default_d)
                        util = 0.5*(u_independant) + 0.5*(u_dormant)
                    else:
                        util = 0.5*(u_independant) + 0.5 * \
                            (STEPCOST + penalty + GAMMA*u_failure)
                    u_t1.update({util: 'SHOOT'})

                # action: HIT
                if 'HIT' in pos.actions:
                    if health > 50:
                        reward = 0
                        u_success = get_util(state, itr, health=health-50)
                        u_success_d = get_util(
                            state, itr, health=health-50, mm=0)
                    else:
                        reward = 50
                        u_success = get_util(state, itr, health=0)
                        u_success_d = get_util(state, itr, health=0, mm=0)
                    u_default = get_util(state, itr)
                    u_independant = p2 * \
                        (STEPCOST + reward + GAMMA*u_success) + \
                        (1-p2)*(STEPCOST + GAMMA*u_default)
                    if penalty == 0:
                        u_default_d = get_util(state, itr, mm=0)
                        u_dormant = p2 * \
                            (STEPCOST + reward + GAMMA*u_success_d) + \
                            (1-p2)*(STEPCOST + GAMMA*u_default_d)
                        util = 0.5*(u_independant) + 0.5*(u_dormant)
                    else:
                        util = 0.5*(u_independant) + 0.5 * \
                            (STEPCOST + penalty + GAMMA*u_failure)
                    u_t1.update({util: 'HIT'})

                # action: CRAFT
                if ('CRAFT' in pos.actions) and mat:
                    u_3 = get_util(state, itr, arrow=3, mat=mat-1)
                    u_2 = get_util(state, itr, arrow=2, mat=mat -
                                   1) if not arrow else get_util(state, itr, arrow=3, mat=mat-1)
                    u_1 = get_util(state, itr, arrow=arrow+1, mat=mat -
                                   1) if arrow < 3 else get_util(state, itr, arrow=3, mat=mat-1)
                    u_independant = p2[0]*(STEPCOST + GAMMA*u_1) + p2[1] * \
                        (STEPCOST + GAMMA*u_2) + p2[2]*(STEPCOST + GAMMA*u_3)
                    if penalty == 0:
                        u_3d = get_util(state, itr, arrow=3, mat=mat-1, mm=0)
                        u_2d = get_util(state, itr, arrow=2, mat=mat - 1, mm=0) if not arrow else get_util(
                            state, itr, arrow=3, mat=mat-1, mm=0)
                        u_1d = get_util(state, itr, arrow=arrow+1, mat=mat - 1,
                                        mm=0) if arrow < 3 else get_util(state, itr, arrow=3, mat=mat-1, mm=0)
                        u_dormant = p2[0]*(STEPCOST + GAMMA*u_1d) + p2[1] * \
                            (STEPCOST + GAMMA*u_2d) + \
                            p2[2]*(STEPCOST + GAMMA*u_3d)
                        util = 0.5*(u_independant) + 0.5*(u_dormant)
                    else:
                        util = 0.5*(u_independant) + 0.5 * \
                            (STEPCOST + penalty + GAMMA*u_failure)
                    u_t1.update({util: 'CRAFT'})

                # action: GATHER
                if 'GATHER' in pos.actions:
                    u_default = get_util(state, itr)
                    u_success = get_util(
                        state, itr, mat=mat+1) if mat < 2 else u_default
                    u_independant = p2 * \
                        (STEPCOST + GAMMA*u_success) + \
                        (1-p2)*(STEPCOST + GAMMA*u_default)
                    if penalty == 0:
                        u_default_d = get_util(state, itr, mm=0)
                        u_success_d = get_util(
                            state, itr, mat=mat+1, mm=0) if mat < 2 else u_default_d
                        u_dormant = p2 * \
                            (STEPCOST + GAMMA*u_success_d) + \
                            (1-p2)*(STEPCOST + GAMMA*u_default_d)
                        util = 0.5*(u_independant) + 0.5*(u_dormant)
                    else:
                        util = 0.5*(u_independant) + 0.5 * \
                            (STEPCOST + penalty + GAMMA*u_failure)
                    u_t1.update({util: 'GATHER'})

            else:  # DORMANT
                # action: UP
                if 'UP' in pos.actions:
                    u_success = get_util(state, itr, pos=pos.up())
                    u_success_r = get_util(state, itr, pos=pos.up(), mm=1)
                    u_default = get_util(state, itr, pos=pos.default())
                    u_default_r = get_util(state, itr, pos=pos.default(), mm=1)
                    u_independant = p1 * \
                        (STEPCOST + GAMMA*u_success) + \
                        (1-p1)*(STEPCOST + GAMMA*u_default)
                    u_ready = p1*(STEPCOST + GAMMA*u_success_r) + \
                        (1-p1)*(STEPCOST + GAMMA*u_default_r)
                    util = 0.2*(u_ready) + 0.8*(u_independant)
                    u_t1.update({util: 'UP'})

                # action: LEFT
                if 'LEFT' in pos.actions:
                    u_success = get_util(state, itr, pos=pos.left())
                    u_success_r = get_util(state, itr, pos=pos.left(), mm=1)
                    u_default = get_util(state, itr, pos=pos.default())
                    u_default_r = get_util(state, itr, pos=pos.default(), mm=1)
                    u_independant = p1 * \
                        (STEPCOST + GAMMA*u_success) + \
                        (1-p1)*(STEPCOST + GAMMA*u_default)
                    u_ready = p1*(STEPCOST + GAMMA*u_success_r) + \
                        (1-p1)*(STEPCOST + GAMMA*u_default_r)
                    util = 0.2*(u_ready) + 0.8*(u_independant)
                    u_t1.update({util: 'LEFT'})

                # action: DOWN
                if 'DOWN' in pos.actions:
                    u_success = get_util(state, itr, pos=pos.down())
                    u_success_r = get_util(state, itr, pos=pos.down(), mm=1)
                    u_default = get_util(state, itr, pos=pos.default())
                    u_default_r = get_util(state, itr, pos=pos.default(), mm=1)
                    u_independant = p1 * \
                        (STEPCOST + GAMMA*u_success) + \
                        (1-p1)*(STEPCOST + GAMMA*u_default)
                    u_ready = p1*(STEPCOST + GAMMA*u_success_r) + \
                        (1-p1)*(STEPCOST + GAMMA*u_default_r)
                    util = 0.2*(u_ready) + 0.8*(u_independant)
                    u_t1.update({util: 'DOWN'})

                # action: RIGHT
                if 'RIGHT' in pos.actions:
                    u_success = get_util(state, itr, pos=pos.right())
                    u_success_r = get_util(state, itr, pos=pos.right(), mm=1)
                    u_default = get_util(state, itr, pos=pos.default())
                    u_default_r = get_util(state, itr, pos=pos.default(), mm=1)
                    u_independant = p1 * \
                        (STEPCOST + GAMMA*u_success) + \
                        (1-p1)*(STEPCOST + GAMMA*u_default)
                    u_ready = p1*(STEPCOST + GAMMA*u_success_r) + \
                        (1-p1)*(STEPCOST + GAMMA*u_default_r)
                    util = 0.2*(u_ready) + 0.8*(u_independant)
                    u_t1.update({util: 'RIGHT'})

                # action: STAY
                if 'STAY' in pos.actions:
                    u_success = get_util(state, itr)
                    u_success_r = get_util(state, itr, mm=1)
                    u_default = get_util(state, itr, pos=pos.default())
                    u_default_r = get_util(state, itr, pos=pos.default(), mm=1)
                    u_independant = p1 * \
                        (STEPCOST + GAMMA*u_success) + \
                        (1-p1)*(STEPCOST + GAMMA*u_default)
                    u_ready = p1*(STEPCOST + GAMMA*u_success_r) + \
                        (1-p1)*(STEPCOST + GAMMA*u_default_r)
                    util = 0.2*(u_ready) + 0.8*(u_independant)
                    u_t1.update({util: 'STAY'})

                # action: SHOOT
                if ('SHOOT' in pos.actions) and arrow:
                    reward = 50 if health == 25 else 0
                    p3 = pos.shoot_prob
                    u_success = get_util(
                        state, itr, arrow=arrow-1, health=health-25)
                    u_success_r = get_util(
                        state, itr, arrow=arrow-1, health=health-25, mm=1)
                    u_default = get_util(state, itr, arrow=arrow-1)
                    u_default_r = get_util(state, itr, arrow=arrow-1, mm=1)
                    u_independant = p3 * \
                        (STEPCOST + reward + GAMMA*u_success) + \
                        (1-p3)*(STEPCOST + GAMMA*u_default)
                    u_ready = p3*(STEPCOST + reward + GAMMA*u_success_r) + \
                        (1-p3)*(STEPCOST + GAMMA*u_default_r)
                    util = 0.2*(u_ready) + 0.8*(u_independant)
                    u_t1.update({util: 'SHOOT'})

                # action: HIT
                if 'HIT' in pos.actions:
                    if health > 50:
                        reward = 0
                        u_success = get_util(state, itr, health=health-50)
                        u_success_r = get_util(
                            state, itr, health=health-50, mm=1)
                    else:
                        reward = 50
                        u_success = get_util(state, itr, health=0)
                        u_success_r = get_util(state, itr, health=0, mm=1)
                    u_default = get_util(state, itr)
                    u_default_r = get_util(state, itr, mm=1)
                    u_independant = p2 * \
                        (STEPCOST + reward + GAMMA*u_success) + \
                        (1-p2)*(STEPCOST + GAMMA*u_default)
                    u_ready = p2*(STEPCOST + reward + GAMMA*u_success_r) + \
                        (1-p2)*(STEPCOST + GAMMA*u_default_r)
                    util = 0.2*(u_ready) + 0.8*(u_independant)
                    u_t1.update({util: 'HIT'})

                # action: CRAFT
                if ('CRAFT' in pos.actions) and mat:
                    u_3 = get_util(state, itr, arrow=3, mat=mat-1)
                    u_3r = get_util(state, itr, arrow=3, mat=mat-1, mm=1)
                    u_2 = get_util(state, itr, arrow=2, mat=mat -
                                   1) if not arrow else get_util(state, itr, arrow=3, mat=mat-1)
                    u_2r = get_util(state, itr, arrow=2, mat=mat-1, mm=1) if not arrow else get_util(
                        state, itr, arrow=3, mat=mat-1, mm=1)
                    u_1 = get_util(state, itr, arrow=arrow+1, mat=mat -
                                   1) if arrow < 3 else get_util(state, itr, arrow=3, mat=mat-1)
                    u_1r = get_util(state, itr, arrow=arrow+1, mat=mat-1,
                                    mm=1) if arrow < 3 else get_util(state, itr, arrow=3, mat=mat-1, mm=1)
                    u_independant = p2[0]*(STEPCOST + GAMMA*u_1) + p2[1] * \
                        (STEPCOST + GAMMA*u_2) + p2[2]*(STEPCOST + GAMMA*u_3)
                    u_ready = p2[0]*(STEPCOST + GAMMA*u_1r) + p2[1] * \
                        (STEPCOST + GAMMA*u_2r) + p2[2]*(STEPCOST + GAMMA*u_3r)
                    util = 0.2*(u_ready) + 0.8*(u_independant)
                    u_t1.update({util: 'CRAFT'})

                # action: GATHER
                if 'GATHER' in pos.actions:
                    u_default = get_util(state, itr)
                    u_default_r = get_util(state, itr, mm=1)
                    u_success = get_util(
                        state, itr, mat=mat+1) if mat < 2 else u_default
                    u_success_r = get_util(
                        state, itr, mat=mat+1, mm=1) if mat < 2 else u_default_r
                    u_independant = p2 * \
                        (STEPCOST + GAMMA*u_success) + \
                        (1-p2)*(STEPCOST + GAMMA*u_default)
                    u_ready = p2*(STEPCOST + GAMMA*u_success_r) + \
                        (1-p2)*(STEPCOST + GAMMA*u_default_r)
                    util = 0.2*(u_ready) + 0.8*(u_independant)
                    u_t1.update({util: 'GATHER'})

        if len(u_t1):
            utility = np.max(list(u_t1.keys()))
            action = u_t1[utility]
        else:
            utility = get_util(state, itr)
            action = actions[-1]
        states[state].append([action, utility])

    # print(diff)
    arr = np.array(list(states.values()))
    diff = np.max(abs(arr[:, itr+1, 1].astype(float) -
                      arr[:, itr, 1].astype(float)))


def trace(itr, file):
    '''Prints the trace of the a single iteration.'''
    file.write('iteration=' + str(itr-1) + '\n')
    for state in states:
        pos, mat, arrow, mm, health = state
        action, utility = states[state][itr]
        file.write('({},{},{},{},{}):{}=[{}]\n'.format(pos.name, str(mat), str(
            arrow), mm_state[mm], str(health), action, format(utility, '.3f')))


if __name__ == '__main__':
    states = get_states()
    i = 0
    diff = 50
    while diff > DELTA:
        iteration(i)
        i += 1

    f = open('./part_2_trace.txt', 'w')
    n = num_iter(states)
    for i in range(1, n):
        trace(i, f)
    f.close()
