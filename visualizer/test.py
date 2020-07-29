from math import cos, sin

from Box2D.examples.framework import (Framework, Keys, main)
from Box2D import (b2CircleShape, b2EdgeShape, b2FixtureDef, b2PolygonShape,
                   b2_pi, b2BodyDef, b2_dynamicBody)
import time
import sys

box1 = 0
startTime = 0

timeBetweenDrops = 2

class CharacterCollision(Framework):
    def __init__(self, sequence):
        super(CharacterCollision, self).__init__()
        global startTime

        ground = self.world.CreateStaticBody(
            position=(0, 0),
            shapes=b2EdgeShape(vertices=[(-20, 0), (20, 0)])
        )

        self.startTime = 0
        self.stacks = sequence

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
        self.triangle = b2BodyDef(position=(-4.3, 40),
                            fixedRotation=False,
                            allowSleep=False,
                            type=2,
                            fixtures=b2FixtureDef(
                            shape=b2PolygonShape(
                                vertices=[(0,0),(8,0),(4,6)]),
                            density=100.0
                            ))

        self.square = b2BodyDef( position=(0, 40),
                            fixedRotation=False,
                            allowSleep=False,
                            type=2,
                            linearDamping=1,
                            fixtures=b2FixtureDef(shape=b2PolygonShape(
                            box=(4, 4)), density=100.0),)

        # self.world.CreateBody(self.triangle)
        # self.world.CreateBody(self.square)


        self.pressed = None
        self.startTime = time.time()
        self.count = 0


        # # Hexagon character
        # a = b2_pi / 3.0
        # self.world.CreateDynamicBody(
        #     position=(-5, 8),
        #     fixedRotation=True,
        #     allowSleep=False,
        #     fixtures=b2FixtureDef(
        #         shape=b2PolygonShape(
        #             vertices=[(0.5 * cos(i * a), 0.5 * sin(i * a))
        #                       for i in range(6)]),
        #         density=20.0
        #     ),
        # )

        # Circle character
        # self.world.CreateDynamicBody(
        #     position=(-3, 1),
        #     fixedRotation=False,
        #     allowSleep=False,
        #     fixtures=b2FixtureDef(
        #         shape=b2CircleShape(radius=0.5),
        #         density=20.0
        #     ),
        # )

    def Keyboard(self, key):
        if key == Keys.K_s:
            self.pressed = "s"

        if key == Keys.K_t:
            self.pressed = "t"

    def KeyboardUp(self, key):
            self.pressed = None

    def Step(self, settings):
        super(CharacterCollision, self).Step(settings)
        global startTime, timeBetweenDrops

        elapsed = time.time() - self.startTime
        if elapsed > timeBetweenDrops:
            if len(self.stacks) > 0:
                next_shape = self.stacks.pop()

                if next_shape == "square":
                    self.world.CreateBody(self.square)
                elif next_shape == "triangle":
                    self.world.CreateBody(self.triangle)

                self.startTime = time.time()
            else:
                self.count += 1
                if self.count == 5:
                    sys.exit(0)
                self.startTime = time.time()



        # if self.pressed == "s":
        #     self.world.CreateDynamicBody(
        #         position=(-3, 50),
        #         fixedRotation=False,
        #         allowSleep=False,
        #         fixtures=b2FixtureDef(shape=b2PolygonShape(
        #             box=(4, 4)), density=20.0),
        #     )
        #     self.pressed = None

        # if self.pressed == "t":
        #     self.world.CreateDynamicBody(
        #     position=(-7, 50),
        #     fixedRotation=False,
        #     allowSleep=False,
        #     fixtures=b2FixtureDef(
        #         shape=b2PolygonShape(
        #             vertices=[(0,0),(8,0),(4,6)]),
        #         density=100.0
        #     ),
        # )
            # self.pressed = None
def startSim(sequence):
    c = CharacterCollision(sequence)
    c.run()

if __name__ == "__main__":
    startSim(['square', 'triangle'])
    # main(CharacterCollision)

