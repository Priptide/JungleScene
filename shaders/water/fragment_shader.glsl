# version 130 // required to use OpenGL core standard

in vec3 normal_view_space;
in vec4 clip_space;
in vec2 texture_Coord;
out vec4 final_color;

// texture samplers
uniform sampler2D textureObject;
uniform sampler2D secondaryTexture;
uniform sampler2D map;
uniform float movement;

uniform mat4 PVM; 	// the Perspective-View-Model matrix is received as a Uniform
uniform mat4 VM; 	// the View-Model matrix is received as a Uniform
uniform mat3 VMiT;  // The inverse-transpose of the view model matrix, used for normals
uniform mat3 VT;

const float strength = 0.01;

void main() {

    
    //Map the coordinates to a [0,1] 2d point
	vec2 normalised = ((clip_space.xy / clip_space.w) / 2) + 0.5;

    //Generate cordinates using the positive and negative y and x of these points
    vec2 reflect_cords = vec2(normalised.x, 1.0-normalised.y);
    vec2 refract_cords = vec2(normalised.x, normalised.y);

    //Distort our image twice using the dudv map and movement we earlier calculated
    vec2 first_distortion = (texture(map, vec2(texture_Coord.x+movement, texture_Coord.y)).rg  * 2.0 - 1.0) * strength;
    vec2 second_distortion = (texture(map, vec2(-texture_Coord.x+movement, texture_Coord.y+movement)).rg  * 2.0 - 1.0) * strength;
    vec2 distortion = first_distortion + second_distortion;

    //Update our cordinates too their new mappings and clamp to ensure no texture tearing
    reflect_cords += distortion;
    reflect_cords = clamp(reflect_cords, 0.001, 0.999);
    refract_cords += distortion;
    refract_cords = clamp(refract_cords, 0.001, 0.999);

    //Map our reflection and refraction textures too these cordinates
    vec4 reflectColour = texture(textureObject, reflect_cords);
    vec4 refractColour = texture(secondaryTexture, refract_cords);

    //Mix equally the two textures to give our final texture
    final_color = mix(reflectColour, refractColour, 0.5);

    //Mix lightly this final texture and colour with a light blue/white colour to give a water look
    final_color = mix(final_color, vec4(0.749, 0.8196, 0.9255, 0.356), 0.1);
}


