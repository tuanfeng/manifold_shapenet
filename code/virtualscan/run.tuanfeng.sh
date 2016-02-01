/Applications/blender.app/Contents/MacOS/blender -b depth.blend -P depth_blender.py -- 500 500 5 /Users/tuanfeng/Documents/ResearchWork/manifold_shapenet/manifold_shapenet/data/model.obj /Users/tuanfeng/Documents/ResearchWork/manifold_shapenet/manifold_shapenet/data/tmp /Users/tuanfeng/Documents/ResearchWork/manifold_shapenet/manifold_shapenet/data/virtualscan


lua combineOFFandNormalTogether.lua /Users/tuanfeng/Documents/ResearchWork/manifold_shapenet/manifold_shapenet/data/virtualscan/model.normal /Users/tuanfeng/Documents/ResearchWork/manifold_shapenet/manifold_shapenet/data/virtualscan/model.off /Users/tuanfeng/Documents/ResearchWork/manifold_shapenet/manifold_shapenet/data/virtualscan/model.pointandnormal


/orions4-zfs/projects/haosu/codebase/geometryprocessing/C++/PoissonRecon/Bin/Linux/PoissonRecon --in /orions4-zfs/projects/haosu/codebase/geometryprocessing/models/virtualscan/model.pointandnormal --out /orions4-zfs/projects/haosu/codebase/geometryprocessing/models/virtualscan/model.ply --depth 10