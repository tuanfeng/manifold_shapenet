-- /orions-zfs/software/blender-2.71/blender -b depth.blend -P depth_blender.py -- 500 500 5 /orions4-zfs/projects/haosu/codebase/geometryprocessing/models/model.obj /orions4-zfs/projects/haosu/codebase/geometryprocessing/models/intermediate /orions4-zfs/projects/haosu/codebase/geometryprocessing/models/virtualscan
if #arg<3 then
  print("usage: lua "..arg[0].." obj_model intermediate_folder pc_folder")
else
  os.execute('/orions-zfs/software/blender-2.71/blender -b depth.blend -P depth_blender.py -- 400 400 4 '..arg[1]..' '..arg[2]..' '..arg[3])
end
