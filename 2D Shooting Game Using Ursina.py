from ursina import *

app = Ursina()

# Set up background
bg = Entity(model='quad', texture='Resource/BG', scale=35, z=1)

# Fullscreen mode
window.fullscreen = True

# Set up player
player = Animation('Resource/player', collider='box', scale=(2, 2), x=-10, y=5)

# Set up fly (enemy)
fly = Entity(model='cube', texture='Resource/bat1', collider='box', scale=1, x=20, y=-10)

# List to store flies
flies = []

# Function to spawn new flies
def newfly():
    new = duplicate(fly, y=-5 + (5124 * time.dt) % 15)
    flies.append(new)
    invoke(newfly, delay=1)

newfly()

# Camera settings
camera.orthographic = True
camera.fov = 20

# Update function to handle movement and interactions
def update():
    # Player movement
    player.y += held_keys['w'] * 10 * time.dt
    player.y -= held_keys['s'] * 10 * time.dt
    player.x -= held_keys['a'] * 6 * time.dt
    player.x += held_keys['d'] * 6 * time.dt

    # Player rotation
    q = held_keys['w'] * -10
    r = held_keys['s'] * 10
    if q != 0:
        player.rotation_z = q
    else:
        player.rotation_z = r

    # Fly movement and collision detection
    for fly in flies:
        fly.x -= 2 * time.dt
        touch = fly.intersects()
        if touch.hit:
            flies.remove(fly)
            destroy(fly)
            destroy(touch.entity)
    
    # Player collision detection
    t = player.intersects()
    if t.hit and t.entity.scale == (2, 2):
        application.quit()

# Input handling
def input(key):
    if key == 'space':
        bullet = Entity(y=player.y, x=player.x + 1, model='cube', scale=0.2, texture='Resource/bullet-s', collider='cube')
        bullet.animate_x(30, duration=2, curve=curve.linear)
        invoke(destroy, bullet, delay=2)

app.run()
