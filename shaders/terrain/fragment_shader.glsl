#version 130

in vec3 pass_colour;

out vec4 final_color;


void main(void){

	final_color = vec4(pass_colour, 1.0);

}