#version 430 core

layout (location = 0) out float a_k1;
layout (location = 1) out float a_k2;
layout (location = 2) out float b_k1;
layout (location = 3) out float b_k2;

in vec3 out_position;
in float out_importance;

uniform vec3 camera_pos;

#define PI 3.1415926538

void main() {

    float dist = distance(out_position, camera_pos);
    importance_squared = out_importance * out_importance;


    a_k1 = 2 * importance_squared * cos(2 * PI * 1 * dist);
    a_k2 = 2 * importance_squared * cos(2 * PI * 2 * dist);
    b_k1 = 2 * importance_squared * sin(2 * PI * 1 * dist);
    b_k2 = 2 * importance_squared * sin(2 * PI * 2 * dist);
}