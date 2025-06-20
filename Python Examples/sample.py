import bpy
import mathutils

# Clean slate
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.delete(use_global=False)

# Add a base cube object
bpy.ops.mesh.primitive_cube_add()
obj = bpy.context.active_object
obj.name = "GN_HomeBuilderBlock"

# Create a new Geometry Nodes modifier
modifier = obj.modifiers.new(name="GN_BuilderBlock", type='NODES')
node_group = bpy.data.node_groups.new("HomeBuilder_CompatibleBlock", 'GeometryNodeTree')
modifier.node_group = node_group

# Create nodes
nodes = node_group.nodes
links = node_group.links
nodes.clear()

# Input and Output nodes
input_node = nodes.new(type='NodeGroupInput')
input_node.location = (-600, 0)
output_node = nodes.new(type='NodeGroupOutput')
output_node.location = (300, 0)

# Expose parameters
node_group.inputs.new("NodeSocketFloat", "Width")
node_group.inputs.new("NodeSocketFloat", "Depth")
node_group.inputs.new("NodeSocketFloat", "Height")
node_group.inputs["Width"].default_value = 0.6
node_group.inputs["Depth"].default_value = 0.45
node_group.inputs["Height"].default_value = 0.15

# Create cube node
cube_node = nodes.new(type='GeometryNodeMeshCube')
cube_node.location = (-300, 0)
cube_node.inputs['Size X'].default_value = 1.0
cube_node.inputs['Size Y'].default_value = 1.0
cube_node.inputs['Size Z'].default_value = 1.0

# Transform node
transform = nodes.new(type='GeometryNodeTransform')
transform.location = (0, 0)

# Math nodes for translate
divide_x = nodes.new(type='ShaderNodeMath')
divide_x.operation = 'DIVIDE'
divide_x.inputs[1].default_value = 2
divide_x.location = (-200, -200)

divide_y = nodes.new(type='ShaderNodeMath')
divide_y.operation = 'DIVIDE'
divide_y.inputs[1].default_value = 2
divide_y.location = (-200, -250)

divide_z = nodes.new(type='ShaderNodeMath')
divide_z.operation = 'DIVIDE'
divide_z.inputs[1].default_value = 2
divide_z.location = (-200, -300)

combine_xyz = nodes.new(type='ShaderNodeCombineXYZ')
combine_xyz.location = (-20, -200)

# Connect geometry
links.new(input_node.outputs['Width'], cube_node.inputs['Size X'])
links.new(input_node.outputs['Depth'], cube_node.inputs['Size Y'])
links.new(input_node.outputs['Height'], cube_node.inputs['Size Z'])

links.new(cube_node.outputs['Mesh'], transform.inputs['Geometry'])

# Scale not needed as cube size is directly set

# Translate setup
links.new(input_node.outputs['Width'], divide_x.inputs[0])
links.new(input_node.outputs['Depth'], divide_y.inputs[0])
links.new(input_node.outputs['Height'], divide_z.inputs[0])

links.new(divide_x.outputs[0], combine_xyz.inputs['X'])
links.new(divide_y.outputs[0], combine_xyz.inputs['Y'])
links.new(divide_z.outputs[0], combine_xyz.inputs['Z'])

links.new(combine_xyz.outputs[0], transform.inputs['Translation'])

links.new(transform.outputs['Geometry'], output_node.inputs['Geometry'])
