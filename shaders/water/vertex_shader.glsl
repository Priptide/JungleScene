#version 130

in vec3 position;

out vec2 textureCoords;

uniform mat4 PVM;
uniform mat4 VM;


void main(void) {

	gl_Position = PVM * vec4(position, 1.0f);
	textureCoords = vec2(position.x/2.0 + 0.5, position.y/2.0 + 0.5);
 
}