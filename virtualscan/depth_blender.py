#   blender -b depth.blend -P depth_blender.py > log -- task_info.haosu
# /Applications/blender.app/Contents/MacOS/blender -b depth.blend -P depth_blender.py > log -- task_info.tuanfeng

import bpy
import os
import sys
import math
from shutil import move as shutil_move
from numpy import cross as np_cross
from numpy import array as np_array
from numpy import linalg as np_linalg
from subprocess import Popen

#change scene name to yours
Scenename = 'Scene'

argv = sys.argv
argv = argv[argv.index("--") + 1:]

task_info=open(argv[0],'r')
#task_info=open('/Users/tuanfeng/Documents/ResearchWork/manifold_shapenet/manifold_shapenet/virtualscan/task_info','r')



task_info_ = task_info.read().splitlines();
print("task info: ", task_info_)

bpy.data.scenes[Scenename].render.resolution_x = int(task_info_[3])
bpy.data.scenes[Scenename].render.resolution_y = int(task_info_[4])
bpy.data.scenes[Scenename].render.resolution_percentage = 100
#bpy.data.scenes[Scenename].render.image_settings.file_format = 'PNG'
bpy.data.scenes[Scenename].render.image_settings.quality = 100
#bpy.data.scenes[Scenename].render.image_settings.color_mode = 'RGB'
bpy.data.scenes[Scenename].render.use_stamp = 0
bpy.data.scenes[Scenename].render.use_placeholder = True
bpy.data.scenes[Scenename].render.use_overwrite = True
bpy.context.scene.render.engine = "BLENDER_RENDER"


bpy.data.scenes[0].node_tree.nodes[3].base_path = task_info_[1]+'/tmp_c1/'
bpy.data.scenes[0].node_tree.nodes[4].base_path = task_info_[1]+'/tmp_d1/'



#bpy.data.scenes[Scenename].cycles.samples = int(task_info_[5])

bpy.data.scenes[Scenename].render.use_antialiasing = True
bpy.data.scenes[Scenename].render.use_full_sample = True

bpy.ops.import_scene.obj(filepath=task_info_[0],use_split_groups=False)

bpy.context.scene.objects.active = bpy.data.objects[1]
bpy.ops.object.join()

obj_name = os.path.splitext(os.path.basename(task_info_[0]))[0]

if not os.path.exists(task_info_[1]+'/'+obj_name+'_cd/'): os.makedirs(task_info_[1]+'/'+obj_name+'_cd/')

#bpy.data.objects[obj_name].rotation_euler = (0,0,0)

vertex_avg_x = float(0)
vertex_avg_y = float(0)
vertex_avg_z = float(0)

vertex_min_x = float("+inf")
vertex_min_y = float("+inf")
vertex_min_z = float("+inf")
vertex_max_x = float("-inf")
vertex_max_y = float("-inf")
vertex_max_z = float("-inf")

vertex_num = float(len(bpy.data.objects[1].data.vertices))

vert_dis = float(0)

#centering
for vertex in bpy.data.objects[1].data.vertices:
	vertex_avg_x = vertex_avg_x + vertex.co[0] / vertex_num
	vertex_avg_y = vertex_avg_y + vertex.co[1] / vertex_num
	vertex_avg_z = vertex_avg_z + vertex.co[2] / vertex_num
	vertex_min_x = min(vertex_min_x,vertex.co[0])
	vertex_min_y = min(vertex_min_y,vertex.co[1])
	vertex_min_z = min(vertex_min_z,vertex.co[2])
	vertex_max_x = max(vertex_max_x,vertex.co[0])
	vertex_max_y = max(vertex_max_y,vertex.co[1])
	vertex_max_z = max(vertex_max_z,vertex.co[2])

for vertex in bpy.data.objects[1].data.vertices:
	vertex.co[0] = (vertex.co[0] - vertex_avg_x)
	vertex.co[1] = (vertex.co[1] - vertex_avg_y)
	vertex.co[2] = (vertex.co[2] - vertex_avg_z)
	vert_dis = max(vert_dis, math.pow(math.pow(vertex.co[0],2)+math.pow(vertex.co[1],2)+math.pow(vertex.co[2],2),0.5))

#scaling
for vertex in bpy.data.objects[1].data.vertices:
	vertex.co[0] = vertex.co[0]/vert_dis/1.01
	vertex.co[1] = vertex.co[1]/vert_dis/1.01
	vertex.co[2] = vertex.co[2]/vert_dis/1.01

for material_ in bpy.data.materials:
	bpy.data.materials[material_.name].use_shadeless = True
	bpy.data.materials[material_.name].use_transparency = False

S = int(task_info_[5])

Rad = float(5.0)

sp_vert_num = 0

if os.path.isfile(task_info_[2]+'/'+obj_name+'.off'):
	os.remove(task_info_[2]+'/'+obj_name+'.off')

for i in range(1, 2 * S + 1):
	ui = math.asin(1 - float(2*i-1)/float(2*S))
	vi = ui * math.pow(2*float(S)*math.pi, 0.5)
	ni = [math.cos(ui)*math.cos(vi), math.cos(ui)*math.sin(vi), math.sin(ui)]
	
	bpy.data.objects['Camera'].location[0] = ni[0] * Rad
	bpy.data.objects['Camera'].location[1] = ni[1] * Rad
	bpy.data.objects['Camera'].location[2] = ni[2] * Rad

	cross_product = np_cross(np_array([0,0,-ni[2]]),np_array([-ni[0],-ni[1],-ni[2]]))
	la = np_linalg.norm(cross_product)

	bpy.data.objects['Camera'].rotation_axis_angle[1] = cross_product[0] / la 
	bpy.data.objects['Camera'].rotation_axis_angle[2] = cross_product[1] / la 
	bpy.data.objects['Camera'].rotation_axis_angle[3] = cross_product[2] / la

	bpy.data.objects['Camera'].rotation_axis_angle[0] = math.atan(math.pow(math.pow(ni[0],2)+math.pow(ni[1],2),0.5)/math.fabs(ni[2]))
	if ni[2] <= 0 : bpy.data.objects['Camera'].rotation_axis_angle[0] = math.pi + bpy.data.objects['Camera'].rotation_axis_angle[0]

	bpy.ops.render.render(animation=False,write_still=True,scene=Scenename)

	f = open('render_report', 'w')
	f.write(str(bpy.data.objects['Camera'].location[0])+' '+str(bpy.data.objects['Camera'].location[1])+' '+str(bpy.data.objects['Camera'].location[2])+'\n')
	f.write(str(bpy.data.objects['Camera'].rotation_axis_angle[0])+' '+str(bpy.data.objects['Camera'].rotation_axis_angle[1])+' '+str(bpy.data.objects['Camera'].rotation_axis_angle[2])+' '+str(bpy.data.objects['Camera'].rotation_axis_angle[3])+'\n')
	f.close()

	process_sp = Popen(("python process_sp.py -- "+argv[0]).split())
	process_sp.communicate()

	shutil_move(task_info_[1]+'/tmp_c1/Image0001.png',task_info_[1]+'/'+obj_name+'_cd/'+obj_name+'_'+str(i).zfill(2)+'_c.png')
	shutil_move(task_info_[1]+'/tmp_d1/Image0001.png',task_info_[1]+'/'+obj_name+'_cd/'+obj_name+'_'+str(i).zfill(2)+'_d.png')



with open(task_info_[2]+'/'+obj_name+'.off','r') as file:
	data = file.readlines()

f = open(task_info_[2]+'/'+obj_name+'.off','w')
f.write('COFF\n')
f.write(str(len(data))+' 0 0\n')
f.writelines(data)
f.close()




