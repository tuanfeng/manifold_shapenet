import os
fout = open('renderBatch.sh', 'w')
intFolder = '/orions4-zfs/projects/haosu/rgb2depth/data/intermediate'
pcFolder = '/orions4-zfs/projects/haosu/rgb2depth/data/pc'
for line in open('/orions4-zfs/projects/haosu/codebase/geometryprocessing/modelList.txt').readlines():
	modelPath = line.strip()
	folder, dummy = os.path.split(modelPath)
	rootFolder, modelId = os.path.split(folder)
	fout.write('lua run_renderonly.lua %s %s %s\n' % (modelPath, os.path.join(intFolder, modelId), os.path.join(pcFolder, modelId)))
fout.close()