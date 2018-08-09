import pygame
from math import *
pygame.init()

win = pygame.display.set_mode((824,1090))
clock = pygame.time.Clock()

background = pygame.image.load('images/background.png')
carImgs = pygame.image.load('images/car.png')

class Car(object):
    def __init__(self,x,y,width=178,height=242):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.length = 200
        self.orientation = pi / 2
        self.steer = 0
        self.vel = 0

    def move(self):
        # https://classroom.udacity.com/courses/cs373/lessons/48532754/concepts/487276450923
        beta = self.vel / self.length * tan(self.steer)
        print("beta: ", beta)
        if abs(beta) < 0.01:
            self.x = self.x + (cos(self.orientation) * self.vel)
            self.y = self.y + (sin(self.orientation) * self.vel)
        else:
            R = self.vel / beta
            cx = self.x + sin(self.orientation) * R
            cy = self.y + cos(self.orientation) * R
            self.x = cx - sin(self.orientation + beta)*R
            self.y = cy - cos(self.orientation + beta) * R
            self.orientation = (self.orientation + beta) % (2*pi)


    def show_states(self):
        print('orientation: {}, steer: {}'.format(self.orientation, self.steer))

    def draw(self, win):
        win.blit(carImgs, (self.x,self.y))

def redrawGameWindow():
    win.blit(background, (0,0))
    car.draw(win)
    pygame.display.update()


car = Car(400, 400)
time_count = 0 # set the minimal time interval for control

run = True
while run:
    clock.tick(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # car frection
    if car.vel > 0:
        car.vel -= 0.2
    elif car.vel < 0:
        car.vel += 0.2 

    if time_count > 5:
        time_count = 0

        keys = pygame.key.get_pressed()
        key_total = keys[pygame.K_LEFT] + keys[pygame.K_RIGHT] + keys[pygame.K_UP] + keys[pygame.K_DOWN]
        # anti-clockwise is positive
        if keys[pygame.K_LEFT]:
            # max steer is 20 degree(pi/9)
            if car.steer  < pi/8:
                car.steer += pi/90
            
        # clockwise is negative
        if keys[pygame.K_RIGHT]:
            if car.steer > -pi/8:
                car.steer -= pi/90

        if keys[pygame.K_UP]:
            if car.vel > -10:
                car.vel -=  1
            car.y += car.vel
        if keys[pygame.K_DOWN]:
            if car.vel < 10:
                car.vel +=  1
            car.y += car.vel

    time_count += 1

    car.show_states()
    car.move()

    redrawGameWindow()


pygame.quit()
    