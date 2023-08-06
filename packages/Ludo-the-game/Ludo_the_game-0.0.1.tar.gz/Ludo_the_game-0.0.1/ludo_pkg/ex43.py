from sys import exit
from random import randint
from textwrap import dedent

class Scene(object):

    def enter(self):
        print("This scene is not yet configured.")
        print("Subclass it and implement enter().")
        exit(1)

class Engine(object):

    def __init__(self, scene_map):
        self.scene_map = scene_map

    def play(self):
        current_scene = self.scene_map.opening_scene()
        last_scene = self.scene_map.next_scene('finished')

        while current_scene != last_scene:
            next_scene_name = current_scene.enter()
            current_scene = self.scene_map.next_scene(next_scene_name)

            # be sure to print out the last scene

            current_scene.enter()

class Death(Scene):
    quips = [
        "You died. You kinda suck at this.",
        "your Mom would be proud... if she were smarter.",
        "Such a luser.",
        "I have a small puppy that's better at this.",
        "you are worse than your Dad's jokes."
    ]

    def enter(self):
        print(Death.quips[randint(0, len(self.quips) - 1)])

        exit(1)

class CentralCorridor(Scene):

    def enter(self):
        print(dedent("""
        The gothons of Planet Percel # 25 have invaded destroyed 
        your entire crew . you are the last member and your last mission
        is to get the neu bomb from the Weapons Armory, put it in the br
        blow the ship up after getting into an escape 
        
        you're running down the central corridor to the Armory when Gothon
        jumps out, red scaly skin teeth, and evil clown flowing around filled body.
        He's blocking the door to the Arm about to pull a weapon to blast you."""))


        action = input("> ")

        if action == "Shoot!":
            print(dedent("""
            Quick on the draw you yank out your blaster it at the Gothon.
            His clown constume is flow moving around his body, which throws off
            your laser hits his costume ruins his brand new costume
            bought him, which makes him fly into an in and blast you repeatedly in the face until
            dead.The he eats you."""))

            return 'death'

        elif action == "dodge!":
            print(dedent("""
            Like a world class boxer you dodge, weave, slide right as the Gothon's blaster
            cranks past your head, In the middle of your artr you foot slips and you 
            bangs your head on wall pass out. you wake up shortly after
            die as the Gothon stomps on your head and"""))

            return "death"

        elif action == "tell a joke":
            print(dedent("""
            Lucky for you they made you learn Gothon in the academy.
            you tell the one Gothon joke lbhezbgure vf fb sng, jura
            fvgf nebha fur not to laugh, then busts out laughing and while he's 
            laughing you run up and shoot the head putting him down, then jump
            through the Weapon armory door."""))

            return "laser_weapon_armory"

        else:
            print("DOES NOT COMPUTE!")
            return 'central_corridor'

class laserWeaponArmory(Scene):

    def enter(self):
        print(dedent("""
        you do a dive roll into the Weapon Armorym, created the room
        for more Gothons that might be hiding quite. you stand up and run
        to the room and find the neutron bomb in its con
        There;s a keypad lock on the box and you need get the bomb out.
        if you get code wrong 1 the lock close forever and you can't get the code is 
        3 digits."""))

        code = f"{randint(1,9)}{randint(1,9)}{randint(1,9)}"
        guess = input("[keypad]> ")
        guesses = 0
        while guess != code and guesses < 10:
            print("BZZZEDDD!")
            guesses += 1
            guess = input("[keypad]> ")

        if guess == code:
            print(dedent("""
            The container clicks opne and the seal breaks gas out.
            you grab the newtron bomb and run you can to the bridge
            where you must place right spot."""))

            return 'the_bridge'
        else:
            print(dedent("""
            The lock buzzess one last time and you sickening melting sound
            as the mechanism together. you decide to sit there, and find 
            gothons blow up the ship form their ship"""))

            return 'death'

class TheBridge(Scene):
        
    def enter(self):
        print(dedent("""
            You burst onto the Bridge with the netron des under your
            arm and surprise 5 Gothons who are take control of their ship.
            Each of them has an aclwn costume than the last . They haven't pul
            weapons out yet, as they see the activate bomb arm and don'twant to set it 
            off"""))

        action = input(">")

        if action == "throw the bomb":
            print(dedent("""In a 
                panic you throw the bomb at the ground and make a leap
                for the door.Right as you Gothon shoots you right in the back killi you die you see another Gothon 
                franticallicsarm the bomb. you die knowing they will blow up it goes off."""
                ))
            return 'death'

        elif action == "slowly place the bomb":
            print(dedent("""
                You point your blaster at the bomb under the Gothons
                put their hands up and start you inch backward to the door,
                open it, a carefully place the bomb on the floor, po blaster
                at it.you then jump back through punch the close button and blast 
                the lock Gothons can't get out. Now that the bomb you run to the escape
                pod to get off"""))
            return 'escape_pod'

        else:
            print("DOES NOT COMPUTE!")
            return "the_bridge"

class EscapePod(Scene):

    def enter(self):

        print(dedent("""
            You rush through the ship desperately trying the escape pod
            before the whole ship explodes like hardly any Gothons on the ship, so you 
            clear of interference. You get ot the chamber escape Pods, and now
            need to pick one to take them could be damaged but you don't have time 
            There's 5 pods which one do you take?"""))

        good_pod = randint(1, 5)
        guess = input("[pod #] >")

        if int(guess) != good_pod:
            print(dedent("""
            you jump into pod {guess} and hit eject the pod escapes
            out inot the void of space implodes as the hull ruptures, crushing you like
            jam jelly."""))
            return 'death'

        else:
            print(dedent("""
            You jump into pod {guess} and hit the eject the pod easily
            slides out inot space head planet below.As it flies to the planet, 
            bakc an see your ship implode them explode bright star, taking out
            the Gothon ship a time. you won!"""))

            return 'finished'

class Finished(Scene):
    
    def enter(self):
        print("you won! Good job.")
        return 'finished'

class Map(object):

    scenes = {
        'central_corridor': CentralCorridor() , 
        'laser_weapon_armory' : laserWeaponArmory(),
        'the_bridge' : TheBridge(),
        'escape_pod' : EscapePod(),
        'death' : Death(),
        'finished' : Finished()
    }

    def __init__(self, start_scene):
        self.start_scene = start_scene

    def next_scene(self, scene_name):
        val = Map.scenes.get(scene_name)
        return val

    def opening_scene(self):
        return self.next_scene(self.start_scene)

a_map = Map('central_corridor')
a_game = Engine(a_map)
a_game.play()



    


