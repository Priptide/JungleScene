# version 130 // required to use OpenGL core standard

in vec3 normal_view_space;
in vec4 clip_space;
in vec3 fragment_texCoord;
out vec4 final_color;

// texture samplers
uniform sampler2D textureObject;
uniform sampler2D secondaryTexture;

uniform mat4 PVM; 	// the Perspective-View-Model matrix is received as a Uniform
uniform mat4 VM; 	// the View-Model matrix is received as a Uniform
uniform mat3 VMiT;  // The inverse-transpose of the view model matrix, used for normals
uniform mat3 VT;
void main() {

    
	vec2 ndsp = ((clip_space.xy / clip_space.w) / 2) + 0.5;

    vec2 reflect_cords = vec2(ndsp.x, 1.0-ndsp.y);

    vec2 refract_cords = vec2(ndsp.x, ndsp.y);

    vec4 reflectColour = texture(textureObject, reflect_cords);

    vec4 refractColour = texture(secondaryTexture, refract_cords);

    final_color = mix(reflectColour, refractColour, 0.5);
}


