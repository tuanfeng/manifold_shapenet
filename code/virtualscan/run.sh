OBJModel=/orions4-zfs/projects/haosu/codebase/geometryprocessing/models/f0ca6f9383ee9aae517376ab44a447e5/model.obj
/orions-zfs/software/blender-2.71/blender -b depth.blend -P depth_blender.py -- 400 400 20 $OBJModel /orions4-zfs/projects/haosu/codebase/geometryprocessing/models/tmp /orions4-zfs/projects/haosu/codebase/geometryprocessing/models/virtualscan

lua combineOFFandNormalTogether.lua /orions4-zfs/projects/haosu/codebase/geometryprocessing/models/virtualscan/model.normal /orions4-zfs/projects/haosu/codebase/geometryprocessing/models/virtualscan/model.off /orions4-zfs/projects/haosu/codebase/geometryprocessing/models/virtualscan/model.pointandnormal

# /orions4-zfs/projects/haosu/codebase/geometryprocessing/manifold_shapenet/code/PoissonRecon/Bin/Linux/PoissonRecon --in /orions4-zfs/projects/haosu/codebase/geometryprocessing/models/virtualscan/model.pointandnormal --out /orions4-zfs/projects/haosu/codebase/geometryprocessing/models/virtualscan/model.ply --depth 10

echo "done!"
