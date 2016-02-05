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
import numpy as np


def obj_centened_camera_pos(dist, phi_deg, theta_deg):
    phi = float(phi_deg) / 180 * math.pi
    theta = float(theta_deg) / 180 * math.pi
    x = (dist * math.cos(theta) * math.cos(phi))
    y = (dist * math.sin(theta) * math.cos(phi))
    z = (dist * math.sin(phi))
    return (x, y, z)

#change scene name to yours
Scenename = 'Scene'

argv = sys.argv
argv = argv[argv.index("--") + 1:]

# task_info = open(argv[0],'r')
# task_info=open('/Users/tuanfeng/Documents/ResearchWork/manifold_shapenet/manifold_shapenet/virtualscan/task_info.tuanfeng','r')

# task_info_ = task_info.read().splitlines();
# print("task info: ", task_info_)
if len(argv) < 5:
	print("usage: /orions-zfs/software/blender-2.71/blender -b depth.blend -P depth_blender.py > log -- res_x res_y num_cam modelname.obj intermediate_folder result_folder")
	exit()

res_x = int(argv[0])
res_y = int(argv[1])
num_cam = int(argv[2])
modelname = argv[3]
intermediate_folder = argv[4]
result_folder = argv[5]

bpy.data.scenes[Scenename].render.resolution_x = res_x
bpy.data.scenes[Scenename].render.resolution_y = res_y
# bpy.data.scenes[Scenename].render.resolution_percentage = 100
#bpy.data.scenes[Scenename].render.image_settings.file_format = 'PNG'
# bpy.data.scenes[Scenename].render.image_settings.quality = 100
#bpy.data.scenes[Scenename].render.image_settings.color_mode = 'RGB'
bpy.data.scenes[Scenename].render.use_stamp = 0
bpy.data.scenes[Scenename].render.use_placeholder = True
bpy.data.scenes[Scenename].render.use_overwrite = True
bpy.context.scene.render.engine = "CYCLES" #"BLENDER_RENDER"


bpy.data.scenes[0].node_tree.nodes[0].base_path = intermediate_folder+'/tmp_c1/'
bpy.data.scenes[0].node_tree.nodes[3].base_path = intermediate_folder+'/tmp_d1/'
bpy.data.scenes[0].node_tree.nodes[11].base_path = intermediate_folder+'/tmp_n1/'


#bpy.data.scenes[Scenename].cycles.samples = int(task_info_[5])
bpy.data.scenes[Scenename].cycles.samples = 200

bpy.data.scenes[Scenename].render.use_antialiasing = True
bpy.data.scenes[Scenename].render.use_full_sample = True

bpy.ops.import_scene.obj(filepath=modelname,use_split_groups=False)

if bpy.data.objects[0].name != 'Camera' and bpy.data.objects[0].name != 'Point':
	bpy.context.scene.objects.active = bpy.data.objects[0]
	bpy.ops.object.join()
	objid = 0

if bpy.data.objects[1].name != 'Camera' and bpy.data.objects[1].name != 'Point':
	bpy.context.scene.objects.active = bpy.data.objects[1]
	bpy.ops.object.join()
	objid = 1

"""
if bpy.data.objects[2].name != 'Camera' and bpy.data.objects[2].name != 'Point':
	bpy.context.scene.objects.active = bpy.data.objects[2]
	bpy.ops.object.join()
	objid = 2
"""

obj_name = os.path.splitext(os.path.basename(modelname))[0]

if not os.path.exists(intermediate_folder+'/'+obj_name+'_cd/'): os.makedirs(intermediate_folder+'/'+obj_name+'_cd/')
if not os.path.exists(result_folder+'/'+obj_name+'_cd/'): os.makedirs(result_folder+'/'+obj_name+'_cd/')

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

vertex_num = float(len(bpy.data.objects[objid].data.vertices))

vert_dis = float(0)

#centering
for vertex in bpy.data.objects[objid].data.vertices:
	vertex_avg_x = vertex_avg_x + vertex.co[0] / vertex_num
	vertex_avg_y = vertex_avg_y + vertex.co[1] / vertex_num
	vertex_avg_z = vertex_avg_z + vertex.co[2] / vertex_num
	vertex_min_x = min(vertex_min_x,vertex.co[0])
	vertex_min_y = min(vertex_min_y,vertex.co[1])
	vertex_min_z = min(vertex_min_z,vertex.co[2])
	vertex_max_x = max(vertex_max_x,vertex.co[0])
	vertex_max_y = max(vertex_max_y,vertex.co[1])
	vertex_max_z = max(vertex_max_z,vertex.co[2])

for vertex in bpy.data.objects[objid].data.vertices:
	vertex.co[0] = (vertex.co[0] - vertex_avg_x)
	vertex.co[1] = (vertex.co[1] - vertex_avg_y)
	vertex.co[2] = (vertex.co[2] - vertex_avg_z)
	vert_dis = max(vert_dis, math.pow(math.pow(vertex.co[0],2)+math.pow(vertex.co[1],2)+math.pow(vertex.co[2],2),0.5))

#scaling
for vertex in bpy.data.objects[objid].data.vertices:
	vertex.co[0] = vertex.co[0]/vert_dis/1.01
	vertex.co[1] = vertex.co[1]/vert_dis/1.01
	vertex.co[2] = vertex.co[2]/vert_dis/1.01

for material_ in bpy.data.materials:
	bpy.data.materials[material_.name].use_shadeless = False
	bpy.data.materials[material_.name].use_transparency = False

Rad = float(5.0)

sp_vert_num = 0

if os.path.isfile(result_folder+'/'+obj_name+'.off'):
	os.remove(result_folder+'/'+obj_name+'.off')
if os.path.isfile(result_folder+'/'+obj_name+'.normal'):
	os.remove(result_folder+'/'+obj_name+'.normal')

lightDist = 4
for i in range(20):
    light_phi_deg = np.random.uniform(-90, 90)
    light_theta_deg  = np.random.uniform(0, 360)
    lx, ly, lz = obj_centened_camera_pos(lightDist, light_phi_deg, light_theta_deg)
    bpy.ops.object.lamp_add(type='POINT', view_align = False, location=(lx, ly, lz))    
bpy.data.objects['Point'].data.energy = 5000
for i in range(1,20):
	bpy.data.objects['Point.%03d' % i].data.energy = 5000


for i in range(1, 2 * num_cam + 1):
	ui = math.asin(1 - float(2*i-1)/float(2*num_cam))
	vi = ui * math.pow(2*float(num_cam)*math.pi, 0.5)
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

	process_sp = Popen(("python process_sp.py -- "+modelname+" "+intermediate_folder+" "+result_folder).split())
	process_sp.communicate()

	shutil_move(intermediate_folder+'/tmp_c1/Image0001.png',intermediate_folder+'/'+obj_name+'_cd/'+obj_name+'_'+str(i).zfill(2)+'_c.png')
	shutil_move(intermediate_folder+'/tmp_d1/Image0001.png',intermediate_folder+'/'+obj_name+'_cd/'+obj_name+'_'+str(i).zfill(2)+'_d.png')
	shutil_move(intermediate_folder+'/tmp_n1/Image0001.png',intermediate_folder+'/'+obj_name+'_cd/'+obj_name+'_'+str(i).zfill(2)+'_n.png')


with open(result_folder+'/'+obj_name+'.off','r') as file:
	data = file.readlines()

f = open(result_folder+'/'+obj_name+'.off','w')
f.write('COFF\n')
f.write(str(len(data))+' 0 0\n')
f.writelines(data)
f.close()
