from PIL import Image
from numpy import array as np_array
from numpy import asarray as np_asarray
from numpy import linalg as np_linalg
from numpy import eye as np_eye
import os, math, sys

argv = sys.argv
argv = argv[argv.index("--") + 1:]

task_info=open(argv[0],'r')
#task_info=open('/home/tuanfeng/Documents/smart_texture/code/depth_buffer/task_info','r')

task_info_ = task_info.read().splitlines()

obj_name = os.path.splitext(os.path.basename(task_info_[0]))[0]

render_info = open('render_report', 'r')
render_info_ =  render_info.read().splitlines()

camera_pos_x = float(render_info_[0].split()[0])
camera_pos_y = float(render_info_[0].split()[1])
camera_pos_z = float(render_info_[0].split()[2])

#print camera_pos_x,' ', camera_pos_y,' ',camera_pos_z

dir_vector_x = -camera_pos_x / np_linalg.norm([-camera_pos_x, -camera_pos_y, -camera_pos_z])
dir_vector_y = -camera_pos_y / np_linalg.norm([-camera_pos_x, -camera_pos_y, -camera_pos_z])
dir_vector_z = -camera_pos_z / np_linalg.norm([-camera_pos_x, -camera_pos_y, -camera_pos_z])

camera_rot_w = float(render_info_[1].split()[0])
camera_rot_x = float(render_info_[1].split()[1])
camera_rot_y = float(render_info_[1].split()[2])
camera_rot_z = float(render_info_[1].split()[3])

#print camera_rot_w,' ',camera_rot_x,' ',camera_rot_y,' ',camera_rot_z

cosi = math.cos(camera_rot_w)
sini = math.sin(camera_rot_w)
ux = camera_rot_x
uy = camera_rot_y
uz = camera_rot_z

Rot = np_eye(3)
Rot[0][0] = cosi+ux*ux*(1-cosi)
Rot[0][1] = ux*uy*(1-cosi)-uz*sini
Rot[0][2] = ux*uz*(1-cosi)+uy*sini
Rot[1][0] = uy*ux*(1-cosi)+uz*sini
Rot[1][1] = cosi+uy*uy*(1-cosi)
Rot[1][2] = uy*uz*(1-cosi)-ux*sini
Rot[2][0] = uz*ux*(1-cosi)-uy*sini
Rot[2][1] = uz*uy*(1-cosi)+ux*sini
Rot[2][2] = cosi+uz*uz*(1-cosi)

dir_up = [Rot[0][1],Rot[1][1],Rot[2][1]]
dir_ri = [Rot[0][0],Rot[1][0],Rot[2][0]]
dir_o = [dir_vector_x,dir_vector_y,dir_vector_z]

#print np_linalg.norm(dir_up), np_linalg.norm(dir_ri)
#print(dir_up[0]*dir_ri[0]+dir_up[1]*dir_ri[1]+dir_up[2]*dir_ri[2])

image_c_path = task_info_[1]+'/tmp_c1/Image0001.png'
image_d_path = task_info_[1]+'/tmp_d1/Image0001.png'
image_n_path = task_info_[1]+'/tmp_n1/Image0001.png'
image_c_ori = Image.open(image_c_path, 'r')
image_d_ori = Image.open(image_d_path, 'r')
image_n_ori = Image.open(image_n_path, 'r')
image_c = np_asarray(image_c_ori)
image_d = np_asarray(image_d_ori)
image_n = np_asarray(image_n_ori)


sp_file_path = task_info_[2]+'/'+obj_name+'.off'
nl_file_path = task_info_[2]+'/'+obj_name+'.obj'

fout = open(sp_file_path,'a')
nout = open(nl_file_path,'a')


for pi in range(0,image_c_ori.size[0]):
	for pj in range(0,image_c_ori.size[1]):
		
		imgd = image_d[pi,pj]

	#	if imgd > 0 and imgd < 32760:
	#		print(imgd)
	#	imgd = 65535
	#	if pi>200 and pi<300 and pj>200 and pj<300:
	#		imgd = 1
	#	if pi>300 and pi<400 and pj>300 and pj<400:
	#		imgd = 65534
	#	if pi>200 and pi<300 and pj>300 and pj<400:
	#		imgd = 32767
	#	if pi>300 and pi<400 and pj>200 and pj<300:
	#		imgd = 32767
		if imgd > 0 and imgd < 65535:
			pixel_color = image_c[pi,pj]
			pixel_depth = float(4.0) + float(imgd)/float(65535)*float(2.0)
			pixel_plan_up = (-float(pi)+float(image_c_ori.size[0])/float(2))/(float(image_c_ori.size[0])/float(2))
			pixel_plan_ri = (+float(pj)-float(image_c_ori.size[1])/float(2))/(float(image_c_ori.size[1])/float(2))
			pixel_plan_pos_x = pixel_plan_up * dir_up[0] + pixel_plan_ri * dir_ri[0]
			pixel_plan_pos_y = pixel_plan_up * dir_up[1] + pixel_plan_ri * dir_ri[1]
			pixel_plan_pos_z = pixel_plan_up * dir_up[2] + pixel_plan_ri * dir_ri[2]
			real_pos_x = camera_pos_x + pixel_plan_pos_x + pixel_depth * dir_vector_x
			real_pos_y = camera_pos_y + pixel_plan_pos_y + pixel_depth * dir_vector_y
			real_pos_z = camera_pos_z + pixel_plan_pos_z + pixel_depth * dir_vector_z
			fout.write(str(real_pos_x)+' '+str(real_pos_y)+' '+str(real_pos_z)+' '+str(pixel_color[0])+' '+str(pixel_color[1])+' '+str(pixel_color[2])+'\n')

			normal_color = image_n[pi,pj]
			ncr = float(normal_color[0])/255.*2.-1. # -1 ~ 1
			ncg = float(normal_color[1])/255.*2.-1.
			if ncr*ncr+ncg*ncg > 1:
				sncrncg = 0
			else:
				sncrncg = 1-ncr*ncr-ncg*ncg

			nct = math.sqrt(sncrncg)
			nm0 = -ncr * dir_ri[0] + -ncg * dir_up[0] + -nct * dir_o[0]
			nm1 = -ncr * dir_ri[1] + -ncg * dir_up[1] + -nct * dir_o[1]
			nm2 = -ncr * dir_ri[2] + -ncg * dir_up[2] + -nct * dir_o[2]

			nout.write('v '+str(real_pos_x)+' '+str(real_pos_y)+' '+str(real_pos_z)+'\n')
			nout.write('vn '+str(nm0)+' '+str(nm1)+' '+str(nm2)+'\n')

fout.close()
nout.close()
