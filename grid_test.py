import pyglet
import random

window = pyglet.window.Window(width=500, height=500)
grid_size = 5
cell_size = window.width // grid_size
grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]  # Store count of points in each cell

def draw_grid():
    """Draw the grid with changing colors based on the count of points."""
    for i in range(grid_size):
        for j in range(grid_size):
            intensity = min(255, grid[i][j] * 40)  # Calculate color intensity, max out at 255
            color = (255 - intensity, 255 - intensity, 255)  # Darken color as points increase
            x, y = j * cell_size, i * cell_size
            # Define vertices and their order for two triangles making up the rectangle
            vertices = [
                x, y,  # Bottom left
                x + cell_size, y,  # Bottom right
                x + cell_size, y + cell_size,  # Top right
                x, y + cell_size  # Top left
            ]
            indices = [0, 1, 2, 0, 2, 3]  # Indices for two triangles
            # Create vertex list and draw
            vertex_list = pyglet.graphics.vertex_list_indexed(4, indices,
                ('v2i', vertices),
                ('c3B', color * 4))
            vertex_list.draw(pyglet.gl.GL_TRIANGLES)

def update(dt):
    """Randomly place a point in the grid on each update."""
    x = random.randint(0, grid_size - 1)
    y = random.randint(0, grid_size - 1)
    grid[y][x] += 1

@window.event
def on_draw():
    window.clear()
    draw_grid()

# Schedule updates at 0.5 seconds interval
pyglet.clock.schedule_interval(update, 0.5)
pyglet.app.run()
