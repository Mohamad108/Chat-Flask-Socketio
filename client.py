from socketio import Client

sio = Client('http://hironika.ir',headers={'device_id':'Mohamad'})

def send_sensor_readings():
	i = 0
	while True:
		print(i)
		if i>1:
			sio.emit('join', {'msg': 'Mohamad.'})
		elif i == 1:
			sio.emit('recive_message',{'msg':'Ali'})
		else:
			sio.emit('recive_message',{'msg':'Reza'+str(i)})
		sio.sleep(5)
		i+=1

@sio.event
def connect():
	print('connection established')
	print(1)
	print(2)
	sio.emit('status', {'msg': ' has entered the room.'})
	print(3)
	# sio.start_background_task(send_sensor_readings)

@sio.event
def my_response_app(data):
	print('my_response_app ', data['msg'])

@sio.event
def my_message(data):
	print(10)
	print('my_response_app ', data['msg']+'  '+data['count'] +'  '+data['Tiny'])
	print(11)

@sio.event
def disconnect():
	print('disconnect from server')


# sio.connect('http://192.168.1.102:5000',headers={'device_id':'Mohamad'})
# sio.connect('http://127.0.0.1:5000',headers={'device_id':'Mohamad'})
if __name__ == '__main__':
	sio.connect('http://hironika.ir',headers={'device_id':'Mohamad'})

