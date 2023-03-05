debug:
	python web.py


up:
	nohup python web.py > log &


down:
	ps aux | grep web.py | awk '{print $2}' | xargs kill 

