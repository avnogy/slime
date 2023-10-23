import math
import random
import moderngl
import numpy as np
from pathlib import Path
import moderngl_window
from moderngl_window import WindowConfig


OPENGL_VERSION_NUMBER = (4, 6)
WINDOW_TITLE = "Slime"
WINDOW_RESOLUTION = [1280, 720]
SLIME_SHADER_GROUPS = {"X": 1, "Y": 1, "Z": 1}
SHADERS_DIR = Path(__file__).parent
AGENTS = 4000

Agent = np.dtype(
    [('position', 'f4', (2,)), ('angle', 'f4'), ('padding', 'f4')])


class Window(WindowConfig):
    gl_version = OPENGL_VERSION_NUMBER
    title = WINDOW_TITLE
    window_size = WINDOW_RESOLUTION
    resizable = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        shaders = {
            "vertex_shader": self.load_shader("window.vert"),
            "fragment_shader": self.load_shader("window.frag")
        }
        print(shaders)
        self.program = self.ctx.program(**shaders)

        self.buffer = self.ctx.buffer(self.init_agents().tobytes())
        self.vao = self.ctx.simple_vertex_array(
            self.program, self.buffer, 'position')

        self.compute_shader = self.load_compute_shader(
            SHADERS_DIR/"slime.comp", SLIME_SHADER_GROUPS)

        self.compute_shader_frame_time = self.compute_shader["frame_time"]

    def init_agents(self):
        agents = np.zeros(AGENTS, dtype=Agent)
        agents['position'] = np.random.rand(AGENTS, 2) * 2 - 1
        agents['angle'] = np.arctan2(
            agents['position'][:, 1], agents['position'][:, 0])
        return agents

    def load_shader(self, shader_filename):
        shader_source = ""
        path = SHADERS_DIR / shader_filename
        if path.exists():
            with path.open() as file:
                shader_source = file.read()
                print(shader_filename, "loaded")
        else:
            print(f"Could not find shader: {path}")
            exit(1)

        return shader_source

    def render(self, time: float, frame_time: float):
        self.ctx.clear()

        frame_time = frame_time if frame_time > 0 else 1 / 60

        self.compute_shader_frame_time.value = frame_time

        self.buffer.bind_to_storage_buffer(binding=0)
        self.compute_shader.run(group_x=AGENTS)

        # print(np.frombuffer(self.buffer.read(),dtype=Agent))

        self.vao.render(moderngl.POINTS)


if __name__ == "__main__":
    moderngl_window.run_window_config(Window)
