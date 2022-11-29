#version 130

//=== in attributes are read from the vertex array, one row per instance of the shader
in vec3 position;	// the position attribute contains the vertex position
in vec3 normal;		// store the vertex normal

//=== out attributes are interpolated on the face, and passed on to the fragment shader
out vec4 clip_space;   // the position of the vertex in view coordinates
out vec3 normal_view_space;     // the normal of the vertex in view coordinates
out vec3 fragment_texCoord;


uniform mat4 PVM; 	// the Perspective-View-Model matrix is received as a Uniform
uniform mat4 VM; 	// the View-Model matrix is received as a Uniform
uniform mat3 VMiT;  // The inverse-transpose of the view model matrix, used for normals
uniform int mode;	// the rendering mode (better to code different shaders!)

void main(){
    // 1. first, we transform the position using PVM matrix.
    // note that gl_Position is a standard output of the
    // vertex shader.

    clip_space = PVM * vec4(position, 1.0);

    gl_Position = clip_space;

    // 2. calculate vectors used for shading calculations
    // those will be interpolate before being sent to the
    // fragment shader.
    // TODO WS4
}
