import os
from subprocess import Popen
from time import sleep

file_list = []
for xx in os.listdir("/home/tuanfeng/Documents/car_data/core_list"):
	if xx.endswith(".png"):
		file_list.append(xx)
		
for file_i in file_list:

	with open('task_info','r') as file:
		data = file.readlines()

	yy = os.path.splitext(os.path.basename(file_i))[0]

	data[0] = "/home/tuanfeng/Documents/car_data/obj_wt_all/" + yy[0:len(yy)-8] + ".obj\n"

	with open('task_info','w') as file:
		file.writelines(data)

	p = Popen("blender -b depth.blend -P depth_blender.py > log".split())
	print("start: ", file_i)
	p.communicate()
	print('done')

	sleep(1)