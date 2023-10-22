import moderngl
import moderngl_window
from moderngl_window import WindowConfig, geometry


OPENGL_VERSION = (4, 6)
WINDOW_TITLE = "Slime"
WINDOW_SIZE = [1920, 1080]


class Window(WindowConfig):
    gl_version = OPENGL_VERSION
    title = WINDOW_TITLE
    window_size = WINDOW_SIZE
    resizable = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def render(self, time: float, frame_time: float):
        self.ctx.clear()


if __name__ == "__main__":
    moderngl_window.run_window_config(Window)
