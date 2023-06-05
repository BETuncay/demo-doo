import moderngl
import numpy as np
import cv2

compute_shader_source = """
#version 450

layout (local_size_x = 16, local_size_y = 16) in;

layout (binding = 0, rgba8ui) uniform   uimage2D src_texture;
layout (binding = 1, rgba8ui) uniform   uimage2D dest_texture;

// rotate channels
void main() {
    ivec2 texel_pos = ivec2(gl_GlobalInvocationID.xy);
    uvec4 color = imageLoad(src_texture, texel_pos);
    uvec4 flipped_color = color.gbra;
    imageStore(dest_texture, texel_pos, flipped_color);
}
"""

dims            = (256, 128)

ctx             = moderngl.create_standalone_context()
compute_shader  = ctx.compute_shader(compute_shader_source)
compute_shader['src_texture']   = 0
compute_shader['dest_texture']  = 1

# Input Image (RED)
in_color    = np.array([0, 0, 100, 255] * dims[0] * dims[1], dtype=np.uint8)
in_texture  = ctx.texture(dims, 4, data = in_color)

# Output Image (initialized BLUE)
out_color   = np.array([100, 0, 0, 255] * dims[0] * dims[1], dtype=np.uint8)
out_texture = ctx.texture(dims, 4, data = out_color)

# Bind textures to units
in_texture.bind_to_image(0, read=True, write=True)
out_texture.bind_to_image(1, read=True, write=True)

# Input
a = np.frombuffer(in_texture.read(), dtype=np.uint8).reshape(in_texture.height, in_texture.width, -1)
cv2.imshow('input', a)

# Before shader execution
a = np.frombuffer(out_texture.read(), dtype=np.uint8).reshape(in_texture.height, in_texture.width, -1)
cv2.imshow('destination before', a)

# Execute the compute shader
compute_shader.run(dims[0] // 16, dims[1] // 16, 1)

# After shader execution (should be GREEN, is BLACK)
a = np.frombuffer(out_texture.read(), dtype=np.uint8).reshape(in_texture.height, in_texture.width, -1)
cv2.imshow('destination after', a)
cv2.waitKey()
