#version 130

in vec3 position;	// the position attribute contains the vertex position
in vec3 normal;		// store the vertex normal
in vec3 color; 		// store the vertex colour
in vec2 texCoord;

out vec3 pass_colour;

uniform vec3 lightDirection;
uniform vec3 lightColour;
uniform vec2 lightBias;

uniform mat4 projectionViewMatrix;

vec3 calculateLighting(){
	vec3 normal = normal.xyz * 2.0 - 1.0;
	float brightness = max(dot(-lightDirection, normal), 0.0);
	return (lightColour * lightBias.x) + (brightness * lightColour * lightBias.y);
}

void main(void){

	gl_Position = projectionViewMatrix * vec4(position, 1.0);
	
	vec3 lighting = calculateLighting();
	pass_colour = color * lighting;

}