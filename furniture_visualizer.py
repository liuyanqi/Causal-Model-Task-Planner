from math import cos, sin

from Box2D.examples.framework import (Framework, Keys, main)
from Box2D import (b2CircleShape, b2EdgeShape, b2FixtureDef, b2PolygonShape,
                   b2_pi, b2BodyDef, b2_dynamicBody, b2Vec2)
import time
import sys
import random
import math
import copy
from customerrors import SimulationOver
from planner import Planner
from blockworld import BlockTowerState
# from blockworld import stack as statestack

box1 = 0
startTime = 0

timeBetweenStacks = 3

class CharacterCollision(Framework):
    def __init__(self, plan, state):
        super(CharacterCollision, self).__init__()
        print("Initializing simulator...")
        global startTime

        ground = self.world.CreateStaticBody(
            position=(0, 0),
            shapes=b2EdgeShape(vertices=[(-40, 0), (40, 0)]),
            userData="ground"
        )

        self.startTime = 0
        self.plan = plan
        self.bottom_block = None
        self.state = state
        self.obj_dict = state.obj_dict
        self.shape_dict = state.getShapeDict()

        # box1 = self.world.CreateDynamicBody(
        #     position=(-3, 20),
        #     fixedRotation=False,
        #     allowSleep=False,
        #     fixtures=b2FixtureDef(shape=b2PolygonShape(
        #         box=(4, 4)), density=20.0),
        # )

        # b2BodyDef??

        # print(type(box1))

        # self.world.CreateDynamicBody(
        #     position=(-2, 40),
        #     fixedRotation=False,
        #     allowSleep=False,
        #     fixtures=b2FixtureDef(shape=b2PolygonShape(
        #         box=(4, 4)), density=20.0),
        # )

        # bodydef = (position=(-7, 3),
        #         fixedRotation=False,
        #         allowSleep=False,
        #         fixtures=b2FixtureDef(
        #             shape=b2PolygonShape(
        #                 vertices=[(0,0),(8,0),(4,6)]),
        #             density=100.0
        #         ),)
        # self.triangle = b2BodyDef(position=(-2.3, 40),
        #                     fixedRotation=False,
        #                     allowSleep=True,
        #                     type=2,
        #                     fixtures=b2FixtureDef(
        #                     shape=b2PolygonShape(
        #                         vertices=[(0,0),(4,0),(2,math.sqrt(12))]),
        #                     density=100.0
        #                     ))
        self.square = b2BodyDef(position=(0,40),
                                fixedRotation=False,
                                allowSleep=True,
                                type=2,
                                fixtures=b2FixtureDef(
                                shape=b2PolygonShape(
                                box=(1,1)), density=100.0)
                                )

        self.triangle = b2BodyDef(position=(-2.3, 40),
                            fixedRotation=False,
                            allowSleep=True,
                            type=2,
                            fixtures=b2FixtureDef(
                            shape=b2PolygonShape(
                                vertices=[(-2,0),(2,0),(0,math.sqrt(12))]),
                            density=100.0
                            ))

        self.ball = b2BodyDef(position=(0,40),
                            fixedRotation=False,
                            allowSleep=True,
                            type=2,
                            fixtures=b2FixtureDef(
                            shape=b2CircleShape(pos=(0,2), radius=1),
                            density=100.0
                            ))

        self.base = b2BodyDef(position=(0,40),
                            fixedRotation=False,
                            allowSleep=True,
                            type=2,
                            fixtures=[b2FixtureDef(
                            shape=b2PolygonShape(
                                box=(2,1)),
                            density=100.0
                            ),b2FixtureDef(
                            shape=b2PolygonShape(
                                vertices=[(-2,1), (-1.1,1), (-1.1,2), (-2,2)]),
                            density=100.0
                            ), b2FixtureDef(
                            shape=b2PolygonShape(
                                vertices=[(1.1,1), (2,1), (2,2), (1.1,2)]),
                            density=100.0,
                            )
                            ])
        self.rod = b2BodyDef( position=(0, 40),
                            fixedRotation=False,
                            allowSleep=True,
                            type=2,
                            linearDamping=1,
                            fixtures=b2FixtureDef(shape=b2PolygonShape(
                            box=(1, 3)), density=100.0),)
        self.light = self.ball

        self.head = b2BodyDef( position=(0, 40),
                            fixedRotation=False,
                            allowSleep=True,
                            type=2,
                            linearDamping=1,
                            fixtures=b2FixtureDef(
                            shape=b2PolygonShape(vertices=[(-1,0), (-2,2), (2,2), (1,0)]), density=100.0),)
        # x_coord = random.randrange(-290,-100, 1)/10
        # print(x_coord)
        # self.triangle.position = (x_coord, 0)
        # self.triangle.userData = "dog"
        # self.world.CreateBody(self.triangle)
        # self.triangle.position = (-2.3, 40)
        # self.world.CreateBody(self.square)

        self.pressed = None
        self.startTime = time.time()
        self.count = 0
        self.objs = {}
        self.intower = []


        self.initShapesOnGround()
        self.initTower()

    def initTower(self):
        '''
        Plan is to create dict of who is on who
        Figure out who is in values, but not in keys
        That will be bottom block
        Then remove that entry and repeat to get whole tower from bottom up
        '''

        tower = self.towerFromState()
        # print(tower)
        for x in range(0, len(tower)-1, 1):
            # print(str(tower[x]) + " " + str(tower[x+1]))
            self.stack(tower[x], tower[x+1], jostling=False)


    #Modifies state to remove that entry
    def towerFromState(self):
        on_dict = {}
        for o in self.state.objects:
            if o.on != "floor":
                on_dict[o.name] = o.on


        tower = []
        while len(on_dict) > 0:
            keys = list(on_dict.keys())
            vals = list(on_dict.values())
            if len(on_dict) == 1:
                tower.append(vals[0])
                tower.append(keys[0])
                on_dict.pop(keys[0])
            else:

                for v in vals:
                    if v not in keys:
                        tower.append(v)
                        on_dict.pop(keys[vals.index(v)])
        return tower


    def initShapesOnGround(self):
        for block in self.state.objects:
            block_shape = block.shape
            block_name = block.name
            block_height = block.height

            if block_shape == "ROD":
                self.rod.userData = block_name
                self.rod.position = (self.getEmptySpot(),5)
                self.rod.fixtures = b2FixtureDef(shape=b2PolygonShape(
                 box=(1, block_height)),density=100.0)
                self.objs[block_name] = self.world.CreateBody(self.rod)
            elif block_shape == "BASE":
                self.base.position = (self.getEmptySpot(),10)
                self.base.userData = block_name
                self.objs[block_name] = self.world.CreateBody(self.base)

            elif block_shape == "LIGHT":
                self.light.position = (self.getEmptySpot(), 5)
                self.light.userData = block_name
                self.objs[block_name] = self.world.CreateBody(self.light)
            elif block_shape == "HEAD":
                self.head.position = (self.getEmptySpot(), 5)
                self.head.userData = block_name
                self.objs[block_name] = self.world.CreateBody(self.head)
            else:
                self.square.position = (self.getEmptySpot(), 5)
                self.square.userData = block_name
                self.objs[block_name] = self.world.CreateBody(self.square)

    def Keyboard(self, key):
        if key == Keys.K_s:
            self.pressed = "s"

        if key == Keys.K_t:
            self.pressed = "t"

        if key == Keys.K_y:
            self.pressed = "y"

        if key == Keys.K_u:
            self.pressed = "u"

        if key == Keys.K_i:
            self.pressed = "i"

    def KeyboardUp(self, key):
        self.pressed = None

    #This just checks if every block is asleep or not
    def shouldEndSim(self):
        everyone_asleep = True
        for obj in self.world.bodies:
            if not (obj.userData == "ground" or obj.userData == None):
                everyone_asleep = (everyone_asleep and not(obj.awake))
        return everyone_asleep

    # def didTowerFall(self):
    #     for x in self.world.bodies:
    #         #Iterate through all the contacts for a given body
    #         #Check if any one other than the bottom block is touching the ground
    #         #If this is true then the tower fell over
    #         for contact in x.contacts:
    #             if contact.other.userData == "ground":
    #                 if not(x.userData == self.bottom_block[0]):
    #                     return True

    #     return False


    def didTowerFall(self):
        for name in self.intower:
            if self.didBlockFall(name):
                return True

        return False


    def didBlockFall(self, block_name):
        for contact in self.objs[block_name].contacts:
            if contact.other.userData == "ground":
                if not(self.objs[block_name].userData == self.bottom_block[0]):
                    return True
        return False

    def getEmptySpot(self):
        unitWidth = 4

        candidate = random.randrange(-25, 25, 1)
        for b in self.world.bodies:
            x = b.position[0]
            if (not(b.userData == None) and  not(b.userData == "ground")):
                l = x - unitWidth
                r = x + unitWidth

                if candidate <= r and candidate >= l:
                    return self.getEmptySpot()

        return candidate

    def getBlockXCoord(self, name):
        return copy.copy(self.objs[name].position[0])

    #a and b here are the names of the blocks
    def stack(self, b1, b2, jostling = False):
        stack_height = 30
        # #This weird hardcoded offset is so that boxes are unbalanced and don't sleep on triangles
        # if self.shape_dict[b1] == "triangle":
        #      coord = (self.getBlockXCoord(b1) + 0.2, stack_height)
        # #This adds nondeterminism to stacking squares together
        # elif b2 == "c" or b2 == "b":
        #     if random.randint(0, 1):
        #         offset = random.randrange(20, 40, 1) / 10
        #         sign = random.choice([-1, 1])
        #         coord = (self.getBlockXCoord(b1) + (offset * sign), stack_height)
        #         print("Tower was jostled!")
        #     else:
        #         coord = (self.getBlockXCoord(b1), stack_height)
        # else:
        #     coord = (self.getBlockXCoord(b1), stack_height)

        #This weird hardcoded offset is so that boxes are unbalanced and don't sleep on triangles
        if self.shape_dict[b1] == "light":
             coord = (self.getBlockXCoord(b1) + 0.2, stack_height)
        #This adds nondeterminism to stacking squares together
        else:
            coord = (self.getBlockXCoord(b1), stack_height)

        self.intower.append(b2)

        self.objs[b2].position = coord
        self.objs[b2].awake = True
        return coord[0]

    def insert(self,b1,b2):
        stack_height=30
        coord = (self.getBlockXCoord(b1), stack_height)
        self.intower.append(b2)
        self.objs[b2].position = coord
        self.objs[b2].awake = True
        return coord[0]

    def updateState(self):
        state = BlockTowerState()
        # print("Added: from bblock" + str(state.get(self.bottom_block[0]).weight))
        state.no_placement_yet = False

        alreadyseen = []
        for x in self.world.bodies:
            x.awake = True
            # print(x)
            #Used to get rid of edge case where triangle is on top of both

            if not(x.userData == "ground") and not(x.userData == None):
                # print("x.userdata " + str(x.userData))
                # print(alreadyseen)
                for contact in x.contacts:
                    above = contact.contact.fixtureA.body.userData
                    below = contact.contact.fixtureB.body.userData

                    names = [above,below]
                    names.sort()

                    # print(above)
                    # print(below)
                    # print(contact.contact)

                    if contact.contact.touching and not(below == "ground") and not(above == "ground"):# and above == x.userData:
                        # if contact.contact.manifold.localNormal[1] > 0:
                            # print("STackec")
                            # print(above)
                            # print(below)
                            normal  = contact.contact.manifold.localNormal
                            if ((names not in alreadyseen) and (normal[1] == 1 or normal[1] == -1)):
                                alreadyseen.append(names)
                                if normal[1] > 0:
                                    print("Recorded " + str(below) + " on " + str(above))
                                    state.get(below).on = above
                                    state.get(above).clear = False
                                    #state.total_weight += state.get(below).weight
                                    #state.total_height += state.get(below).height
                                else:
                                    print("Recorded " + str(above) + " on " + str(below))
                                    state.get(above).on = below
                                    state.get(below).clear = False
                                    #state.total_weight += state.get(above).weight
                                    #state.total_height += state.get(above).height

        #EDGE CASE CHECK
        #IF nothing is stacked at all
        on_floor = True
        for obj in state.objects:
            if not(obj.on == "floor"):
                on_floor = False

        if on_floor:
            # state.total_height = 0
            # state.total_weight = 0
            state.no_placement_yet = True

        return state

        # def initState(self, state): adcb
        #normal = negative


    def Step(self, settings):
        super(CharacterCollision, self).Step(settings)
        global startTime, timeBetweenDrops

        # if self.shouldEndSim():
        #     raise SimulationOver(self.didTowerFall())

        # if self.pressed == "y":
        #     # print(self.objs["a"].transform)
        #     # self.objs["a"].transform = ((0,0), 0)
        #     y = (self.getEmptySpot(),20)
        #     print(type(y))
        #     self.objs["a"].position = y
        #     # self.world.DestroyBody(self.objs["a"])
        #     self.pressed = None
        if self.pressed =="y":
            if self.didTowerFall():
                print("Unexpected, action failed")
                recovered_state = self.updateState()
                print("State recovered:")
                print(recovered_state)
                raise SimulationOver(recovered_state)

            elapsed = time.time() - self.startTime
            if elapsed > timeBetweenStacks:
                if len(self.plan) > 0:
                    next_action, params = self.plan.pop(0)
                    print(str(next_action) + " " + str(params))

                    if next_action == "stack":
                        #Bottom block need to know for fall detection
                        if self.bottom_block == None:
                            self.bottom_block = [params[0], self.stack(params[0], params[1])]
                        else:
                            self.stack(params[0], params[1])
                    elif next_action == "insert":
                        if self.bottom_block== None:
                            self.bottom_block = [params[0], self.insert(params[0], params[1])]
                        else:
                            self.insert(params[0], params[1])
                else:
                    #If all the moves are done
                    #Think about ending the simulation
                    if self.shouldEndSim():
                        print("Simulation complete")
                        # print("Recovered state: ")
                        # print(self.updateState())
                        raise SimulationOver(None)



                self.startTime = time.time()

            #         # if next_shape == "square":
            #         #     self.square.userData = u_data
            #         #     self.objs.append(self.world.CreateBody(self.square))
            #         # elif next_shape == "triangle":
            #         #     self.triangle.userData = u_data
            #         #     self.objs.append(self.world.CreateBody(self.triangle))

            #     self.startTime = time.time()
            # else:
            #     #Every block has been placed
            #     #We are now starting to check if we should end the simulation yet
            #     self.count += 1

def runSim(res, planner):
    plan = planner.parseHistorytoList(res)
    #shape_dict = planner.domain.state.getShapeDict()
    state = planner.domain.state


    c = CharacterCollision(plan, state)
    c.run()
    # except SimulationOver as e:
    #     if e.message:
    #         print("The tower fell over")
    #     else:
    #         print("The tower stayed up")
