#version 130

in vec3 normal_view_space;
in vec3 position_view_space;
in vec2 fragment_texCoord;
out vec4 final_color;

uniform sampler2D textureObject;
// uniform samplerCube below_cube;
uniform mat4 PVM; 	// the Perspective-View-Model matrix is received as a Uniform
uniform mat4 VM; 	// the View-Model matrix is received as a Uniform
uniform mat3 VMiT;  // The inverse-transpose of the view model matrix, used for normals
uniform mat3 VT;

void main(void)
{
	
	// vec4 reflectColour = texture(above_cube, fragment_texCoord);
	// vec4 refractColour = texture(above_cube, fragment_texCoord);

	// final_color = mix(reflectColour, refractColour, 0.5);
	final_color = texture2D(textureObject, fragment_texCoord);


	//final_color = texture(sampler_cube, fragment_texCoord);
//	frag_data = texture(sampler_cube, vec3(1,0,0));
	//final_color = vec4( fragment_texCoord, 1.0f );
}
