import moderngl
import numpy as np
from pathlib import Path
import moderngl_window
from moderngl_window import WindowConfig


OPENGL_VERSION_NUMBER = (4, 6)
WINDOW_TITLE = "Slime"
WINDOW_RESOLUTION = [1280, 720]
SHADER_FILENAMES = {"vert": "vertex_shader", "frag": "fragment_shader"}
SLIME_SHADER_GROUPS = {"X": 16, "Y": 1, "Z": 1}
SHADERS_DIR = Path(__file__).parent
AGENTS = 25000


class Window(WindowConfig):
    gl_version = OPENGL_VERSION_NUMBER
    title = WINDOW_TITLE
    window_size = WINDOW_RESOLUTION
    resizable = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.program = self.ctx.program(**self.load_shaders())
        self.buffer = self.ctx.buffer(self.init_agents().tobytes())
        self.vao = self.ctx.simple_vertex_array(
            self.program, self.buffer, 'position')

    def init_agents(self):
        dtype = np.dtype([
            ('position', 'f4', (2,)),
            ('angle', 'f4')
        ])

        agents = np.zeros(AGENTS, dtype=dtype)

        agents['position'] = np.random.rand(AGENTS, 2) * 2 - 1
        agents['angle'] = np.random.rand(AGENTS) * 2 * np.pi

        return agents

    def load_shaders(self):
        shaders = {}

        for shader, shader_name in SHADER_FILENAMES.items():
            path = SHADERS_DIR / ("window." + shader)
            if path.exists():
                with path.open() as file:
                    shaders[shader_name] = file.read()
                    print(shader_name, "loaded")
            else:
                print(f"Could not find shader: {path}")

        return shaders

    def render(self, time, _):
        self.ctx.clear()
        self.vao.render(moderngl.POINTS)


if __name__ == "__main__":
    moderngl_window.run_window_config(Window)
