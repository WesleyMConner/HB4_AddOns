
import bpy

def createCuboid (w,  # world-space width (along x-axis in prevailing units)
                  d,  # world-space depth (along y-axis in prevailing units)
                  h,  # world-space height (along x-axis in prevailing units)
                  location = (0, 0, 0), # location in the enclosing mesh
                  rectName = 'Unnamed Rectangle',
                  mesh = bpy.data.meshes.new("Unnamed Mesh")
                 ):
  # Abstract
  #     This methods adds a new Cuboid (a.k.a. Rectangular Prism) to the
  #     supplied mesh, creating a new enclosing mesh if none is supplied.
  # Design Notes
  #     (1) HomeBuilder 4 (HB4) conventions are followed.
  #           - Unit dimensions (in the mesh) correspond to world-space
  #             dimensions. The x, y and z unit measures as defined
  #             WHEN THE CUBOID IS CREATED.
  #           - Scale is locked to (1.0, 1.0, 1.0).
  #           - The object's bottom-front-left is placed at the supplied
  #             location.
  #     (2) Ideally, enclosing all nested objects (e.g., the newly-created
  #         rectangle, the enclosing Mesh) should have meaningful names!

  # Define rectangle's vertices (from bottom-front-left).
  vertices = [    # (x, y, z)
    ( 0,  0, 0),  # 0
    (-w,  0, 0),  # 1
    ( 0, -d, 0),  # 2
    (-w, -d, 0),  # 3
    ( 0,  0, h),  # 4
    (-w,  0, h),  # 5
    ( 0, -d, h),  # 6
    (-w, -d, h)   # 7
  ]

  # Define faces (vertex indices)
  faces = [        # Ordered, Self-Closing Vertices
    (0, 2, 6, 4),  # x=0 left face
    (1, 3, 7, 5),  # x=w right face
    (0, 1, 5, 4),  # y=0 back face
    (2, 3, 7, 6),  # y=w front face,
    (0, 1, 3, 2),  # z=0 bottom face,
    (4, 5, 7, 6)   # z=w top face,
  ]

  # Add data to the mesh
  mesh.from_pydata(vertices, [], faces) # Edges are inferred from faces.

  # Create a new object and link it to the mesh
  obj = bpy.data.objects.new(rectName, mesh)
  obj.scale = (1.0, 1.0, 1.0)
  obj.lock_scale = (True, True, True)

  # Add the object to the scene
  bpy.context.scene.collection.objects.link(obj)

  # Set the location of the object
  obj.location = location
  return

def Test_createCuboid ():
  mesh = bpy.data.meshes.new("Enclosing Mesh")
  location = (-1, 2, 3.5)
  rect = createCuboid(30, 24, 12, location, "Test Rectangle", mesh)

# Test_createCuboid()
