import bpy
import csv
import os

def clear_scene():
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()
    
    for material in bpy.data.materials:
        bpy.data.materials.remove(material)

def create_neuron_material(name):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    nodes.clear()
    
    output_node = nodes.new(type='ShaderNodeOutputMaterial')
    emission_node = nodes.new(type='ShaderNodeEmission')
    
    links.new(emission_node.outputs['Emission'], output_node.inputs['Surface'])
    
    return mat, emission_node

def import_neurons(base_path, session_id):
    data_dir = os.path.join(base_path, "Dataset", "Processed", str(session_id))
    
    probes = ['probeA', 'probeB', 'probeC', 'probeD', 'probeE', 'probeF']
    
    scale_factor = 0.001 
    
    for probe_name in probes:
        csv_file = os.path.join(data_dir, f"{probe_name}.csv")
        
        if not os.path.exists(csv_file):
            continue
            
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                unit_id = row['id']
                
                try:
                    x = float(row['anterior_posterior_ccf_coordinate']) * scale_factor
                    y = float(row['left_right_ccf_coordinate']) * scale_factor
                    z = float(row['dorsal_ventral_ccf_coordinate']) * scale_factor
                except ValueError:
                    continue
                
                bpy.ops.mesh.primitive_uv_sphere_add(radius=0.05, location=(x, y, z))
                obj = bpy.context.active_object
                obj.name = f"Neuron_{unit_id}"
                
                mat, emission_node = create_neuron_material(f"Mat_{unit_id}")
                obj.data.materials.append(mat)
                
                frame_keys = [k for k in row.keys() if k.startswith('frame_')]
                sorted_frames = sorted(frame_keys, key=lambda x: int(x.split('_')[1]))
                
                for frame_col in sorted_frames:
                    frame_idx = int(frame_col.split('_')[1])
                    val = float(row[frame_col])
                    
                    color_strength = val * 10.0 
                    emission_node.inputs['Strength'].default_value = color_strength
                    emission_node.inputs['Color'].default_value = (1.0, 0.2, 0.2, 1.0) 
                    
                    emission_node.inputs['Strength'].keyframe_insert(data_path="default_value", frame=frame_idx + 1)

if __name__ == "__main__":
    clear_scene()
    
    blend_file_dir = bpy.path.abspath('//')
    project_root = os.path.dirname(blend_file_dir) 
    
    session_id = 750749662
    
    import_neurons(project_root, session_id)
