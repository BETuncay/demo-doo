#version 430 core

layout (location = 0) in vec3 in_position;
layout (location = 1) in float in_importance;

out vec3 out_position;
out float out_importance;

uniform mat4 m_proj;
uniform mat4 m_view;
uniform mat4 m_model;

void main() {
    out_importance = in_importance;
    vec4 model_position = m_model * vec4(in_position, 1.0);
    out_position = model_position.xyz;
    gl_Position = m_proj * m_view * model_position;
}