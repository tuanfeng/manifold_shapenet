# manifold_shapenet



modify ./virtualscan/run.sh to process

template:

path_to_blender -b depth.blend -P depth_blender.py -- resolution1 resolution2 half_samples input_obj_path rendered_imgs_path output_path


lua combineOFFandNormalTogether.lua path_to_model_normal path_to_model_off path_to_model_pointandnormal


path_to_PoissonRecon --in path_to_model_pointandnormal --out output_result_ply --depth 10







