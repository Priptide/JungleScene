#version 130

in vec2 textureCoords;

uniform sampler2D reflectionTexture;
uniform sampler2D refractionTexture;

out vec4 final_color;

void main(void) {

	vec4 reflectColour = texture(reflectionTexture, textureCoords);
	vec4 refractColour = texture(refractionTexture, textureCoords);

	// final_color = mix(reflectColour, refractColour, 0.5);
	final_color = vec4(0.0, 0.0, 1.0, 1.0);


}