import pygame
import random

pygame.init()


class DrawApp:
    # Create Class attributes for the colors being used in game window
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    RED = 255, 0, 0
    GREEN = 0, 255, 0
    BACKGROUND_COLOR = WHITE
    GREYS = [
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192),
    ]

    FONT = pygame.font.SysFont("Arial", 30)

    # Padding for the bars that are going to be sorted *(Placeholders currently)
    SIDE_PADDING = 100
    TOP_PADDING = 275

    def __init__(self, height, width, lst) -> None:

        self.height = height
        self.width = width

        # Initialize the window using height and width being passed
        self.window = pygame.display.set_mode((self.width, self.height))
        # Set the windows 'Caption' (Name at top bar)
        pygame.display.set_caption("Python Sorting Visualizer")
        # Call the set_list method to give lst attributes for window
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        # Get the minimum and maximum from the list
        self.min_val = min(lst)
        self.max_val = max(lst)

        # Make the bars dynamic to the amount in the list stretching ans shrinking using max and min values for proper height difference
        self.bar_width = round((self.width - self.SIDE_PADDING) / len(lst))
        self.bar_height = round(
            (self.height - self.TOP_PADDING) / (self.max_val - self.min_val)
        )

        # Set the starting position of the bars based off side padding
        self.start_x = self.SIDE_PADDING // 2


class Button:
    def __init__(
        self, position_x, position_y, width, height, text, on_click_func, draw_app
    ) -> None:
        self.position_x = position_x
        self.position_y = position_y
        self.width = width
        self.height = height
        self.text = text
        self.draw_app = draw_app
        self.on_click_func = on_click_func
        self.pressed = False

        self.fillColors = {
            "normal": "#23272a",
            "hover": "#99aab5",
            "pressed": "#2c2f33",
        }

    def draw(self):
        self.button_surface = pygame.draw.rect(
            self.draw_app.window,
            self.fillColors["normal"],
            (self.position_x, self.position_y, self.width, self.height),
        )

        self.button_text = self.draw_app.FONT.render(self.text, 1, self.draw_app.WHITE)

    def process(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.button_surface.collidepoint(mouse_pos):
            self.button_surface = pygame.draw.rect(
                self.draw_app.window,
                self.fillColors["hover"],
                (self.position_x, self.position_y, self.width, self.height),
            )
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.button_surface = pygame.draw.rect(
                    self.draw_app.window,
                    self.fillColors["pressed"],
                    (self.position_x, self.position_y, self.width, self.height),
                )
                if not self.pressed:
                    self.on_click_func()
                    self.pressed = True
            else:
                self.pressed = False

        self.draw_app.window.blit(
            self.button_text,
            (
                (self.width / 2 + self.position_x) - self.button_text.get_width() / 2,
                (self.height / 2 + self.position_y) - self.button_text.get_height() / 2,
            ),
        )


def draw(draw_app, buttons):
    draw_app.window.fill(draw_app.BACKGROUND_COLOR)
    draw_bars(draw_app)
    for button in buttons:
        button.draw()
        button.process()
    pygame.display.update()


def draw_bars(draw_app):
    # Use list created
    lst = draw_app.lst

    # Draw each bar based on the value in proportion to min and max within its boundaries
    for i, val in enumerate(lst):
        # amount of bars_height needed with min being 1 and max being difference + 1
        bar_val = val - draw_app.min_val + 1

        # Calculate the objects starting upper left position to each bar to draw out
        x = draw_app.start_x + i * draw_app.bar_width
        y = draw_app.height - bar_val * draw_app.bar_height

        # Alternate color gradient to make more visible
        color = draw_app.GREYS[i % 3]

        # Draw out the rectangles and determine the height and width needed for each bar
        pygame.draw.rect(
            draw_app.window,
            color,
            (
                x,
                y,
                draw_app.bar_width,
                draw_app.bar_height * bar_val,
            ),
        )


def button_press():
    print("Button Pressed")


def create_list(n, min_val, max_val):
    # Create empty list
    lst = []

    # Fill the list with random numbers within min and max values
    for _ in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)

    return lst


def main():
    # Set app loop trigger
    run = True

    # Initialiaze clock variable for tick rate
    clock = pygame.time.Clock()

    # Set list attributes
    n = 50
    min_val = 0
    max_val = 100

    # Create list
    lst = create_list(n, min_val, max_val)

    # Create App object
    draw_app = DrawApp(600, 800, lst)

    objects = []
    bubble = Button(0, 0, 150, 75, "Bubble", button_press, draw_app)
    insertion = Button(0, 75, 150, 75, "Insertion", button_press, draw_app)
    merge = Button(0, 150, 150, 75, "Merge", button_press, draw_app)
    objects.append(bubble)
    objects.append(insertion)
    objects.append(merge)

    while run:
        # refresh at 60ticks per second
        clock.tick(60)
        # Draw to window
        draw(draw_app, objects)
        # Update window
        pygame.display.update()

        # Listen for events
        for event in pygame.event.get():
            # If corner x is pressed exit loop
            if event.type == pygame.QUIT:
                run = False
            # Continue if random buttons are pressed down
            if event.type != pygame.KEYDOWN:
                continue
            # Refresh list and set to object if the 'R' key is pressed
            if event.key == pygame.K_r:
                lst = create_list(n, min_val, max_val)
                draw_app.set_list(lst)

    pygame.quit()


if __name__ == "__main__":
    main()
