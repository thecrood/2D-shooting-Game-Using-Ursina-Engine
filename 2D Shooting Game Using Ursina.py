from ursina import *

app = Ursina()
bg = Entity(model = 'quad', texture = 'Resource/BG', scale = 35, z = 1)

window.fullscreen = True 
player = Animation('Resource/player', collider = 'box', scale = (2,2) , x = -10, y = 5)
fly = Entity(model = 'cube', texture = 'Resource/bat1', collider = 'box', scale = 1  , x = 20, y = -10)

flies = []
def newfly():
	new = duplicate(fly, y = -5+(5124*time.dt)%15)
	flies.append(new)
	invoke(newfly, delay = 1)
  
newfly()

camera.orthographic = True 
camera.fov = 20


def update():
	player.y += held_keys['w']*10*time.dt 
	player.y -= held_keys['s']*10*time.dt 
	player.x -= held_keys['a']*6*time.dt 
	player.x += held_keys['d']*6*time.dt 
	q = held_keys['w']*-10
	r = held_keys['s'] *10
	if q   != 0:
		player.rotation_z = q
	else:      
		player.roattion_z = r
 
	for fly in flies:
		fly.x -= 2*time.dt   
		touch = fly.intersects()
		if touch.hit:
			flies.remove(fly)
			destroy(fly)
			destroy(touch.entity)
		t= player.intersects()
		if t.hit and t.entity.scale == 2:
			quit()


def input(key):
	if key == 'space':
		e = Entity(y = player.y, x =  player.x+1, model = 'cube', scale = 0.2, texture = 'Resource/bullet-s', collider = 'cube')
		e.animate_x(30, duration = 2, curve = curve.linear) 
		invoke(destroy, e, delay = 2)


app.run()