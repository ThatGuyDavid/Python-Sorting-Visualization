import pygame
import random
import math
import time

pygame.init()


class DrawApp:
    # Create Class attributes for the colors being used in game window
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    RED = 255, 0, 0
    GREEN = 0, 255, 0
    BACKGROUND_COLOR = WHITE
    BAR_COLORS = [
        "#2e5090",
        "#5873a6",
        "#8296bc",
    ]

    FONT = pygame.font.SysFont("Arial", 25)
    DISPLAY_FONT = pygame.font.SysFont("Arial", 40)

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
        self.bar_height = math.floor(
            (self.height - self.TOP_PADDING) / (self.max_val - self.min_val)
        )

        # Set the starting position of the bars based off side padding
        self.start_x = self.SIDE_PADDING // 2


class Button:
    """ """

    def __init__(
        self,
        position_x,
        position_y,
        width,
        height,
        text,
        draw_app,
    ) -> None:
        self.position_x = position_x
        self.position_y = position_y
        self.width = width
        self.height = height
        self.text = text
        self.draw_app = draw_app
        # Check safe for over pressing
        self.pressed = False
        # Color pallete for buttons (normal, hover, pressing)
        self.fillColors = {
            "normal": "#2e5090",
            "hover": "#abb9d3",
            "pressed": "#5873a6",
        }

    def draw(self):
        # Draw the button to the window
        self.button_surface = pygame.draw.rect(
            self.draw_app.window,
            self.fillColors["normal"],
            (self.position_x, self.position_y, self.width, self.height),
        )
        # Create the text for the box
        self.button_text = self.draw_app.FONT.render(self.text, 1, self.draw_app.WHITE)

    def process(self):
        action = False
        # Get the position of the mouse on the window
        mouse_pos = pygame.mouse.get_pos()
        # Check if mouse overlaps/collides with the button surface/rect
        if self.button_surface.collidepoint(mouse_pos):
            # If true redraw button for button in hover profile
            self.button_surface = pygame.draw.rect(
                self.draw_app.window,
                self.fillColors["hover"],
                (self.position_x, self.position_y, self.width, self.height),
            )
            # Check if button is being pressed down by left-mouse button
            if pygame.mouse.get_pressed(num_buttons=3)[0] == 1:
                # If true redraw to indicate pressed profile
                self.button_surface = pygame.draw.rect(
                    self.draw_app.window,
                    self.fillColors["pressed"],
                    (self.position_x, self.position_y, self.width, self.height),
                )
                # Check to see if button is currently pressed / active
                if not self.pressed:
                    # If not active call function and set button parameter to pressed
                    self.pressed = True
                    action = True
            else:
                # Unpress button allowing to be repressed
                self.pressed = False
                action = False

        # Draw words onto buttons/rect
        self.draw_app.window.blit(
            self.button_text,
            (
                (self.width / 2 + self.position_x) - self.button_text.get_width() / 2,
                (self.height / 2 + self.position_y) - self.button_text.get_height() / 2,
            ),
        )

        return action


def draw(draw_app, buttons, algo_name, ascending):
    draw_app.window.fill(draw_app.BACKGROUND_COLOR)
    # Draw Display of Sort - Direction
    drawing_display(draw_app, algo_name, ascending)
    # Draw buttons onto screen and track for hovering and press
    for button in buttons:
        button.draw()
        button.process()
    # Draw bars to window
    draw_bars(draw_app)
    pygame.display.update()


def drawing_display(draw_app, algo_name, ascending):
    # Create display text
    display_text = draw_app.DISPLAY_FONT.render(
        f"{algo_name} - {'Ascending' if ascending else 'Descending'}",
        1,
        draw_app.BLACK,
    )
    # Draw display text onto app window
    draw_app.window.blit(
        display_text,
        (
            (400) - display_text.get_width() / 2,
            (71) - display_text.get_height() / 2,
        ),
    )


def draw_bars(draw_app, color_positions={}, clear_bg=False):
    # Use list created
    lst = draw_app.lst

    # Clear the window space for redrawing of visual sort
    if clear_bg:
        clear_rect = (
            draw_app.SIDE_PADDING // 2,
            draw_app.TOP_PADDING,
            draw_app.width - draw_app.SIDE_PADDING,
            draw_app.height - draw_app.TOP_PADDING,
        )
        pygame.draw.rect(draw_app.window, draw_app.BACKGROUND_COLOR, clear_rect)

    # Draw each bar based on the value in proportion to min and max within its boundaries
    for i, val in enumerate(lst):
        # amount of bars_height needed with min being 1 and max being difference + 1
        bar_val = val - draw_app.min_val + 1

        # Calculate the objects starting upper left position to each bar to draw out
        x = draw_app.start_x + i * draw_app.bar_width
        y = draw_app.height - bar_val * draw_app.bar_height

        # Alternate color gradient to make more visible
        color = draw_app.BAR_COLORS[i % 3]

        if i in color_positions:
            color = color_positions[i]

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
    if clear_bg:
        pygame.display.update()


def create_list(n, min_val, max_val):
    # Create empty list
    lst = []

    # Fill the list with random numbers within min and max values
    for _ in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)

    return lst


# Bubble Sort Algo
def bubble_sort(draw_app, lst, ascending):

    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j + 1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                draw_bars(draw_app, {j: draw_app.GREEN, j + 1: draw_app.RED}, True)
                yield True
    return lst


# Insertion Sort Algo
def insertion_sort(draw_app, lst, ascending):

    for i in range(1, len(lst)):
        current = lst[i]

        while True:
            ascending_sort = i > 0 and lst[i - 1] > current and ascending
            descending_sort = i > 0 and lst[i - 1] < current and not ascending

            if not ascending_sort and not descending_sort:
                break

            lst[i] = lst[i - 1]
            i = i - 1
            lst[i] = current
            draw_bars(draw_app, {i - 1: draw_app.GREEN, i: draw_app.RED}, True)
            yield True

    return lst


# Merge Sort Algorithm
def merge_sort(draw_app, lst, ascending, sort_list=[]):
    # Keep track of original indexes to allow for swap visualization in merge function
    # Initialize sort list at initial call of iteration
    if len(sort_list) == 0:
        # Create a list of pairs [value, index]
        for idx in range(len(lst)):
            sort_list.append([lst[idx], idx])
    if len(lst) <= 1:
        return

    mid = len(lst) // 2
    left = lst[:mid]
    right = lst[mid:]
    # Create sorted list with index and values shared by left list and right list
    l_srt = sort_list[:mid]
    r_srt = sort_list[mid:]
    merge_sort(draw_app, left, ascending, l_srt)
    merge_sort(draw_app, right, ascending, r_srt)
    # Create a combined list of left and right listed pairs to manage index for swaps
    srt = l_srt + r_srt

    merge(draw_app, left, right, lst, ascending, r_srt, srt)


# Merge Function
def merge(draw_app, left, right, lst, ascending, r_srt, srt):
    len_left = len(left)
    len_right = len(right)
    i = j = k = 0
    # Ascending Order
    if ascending:
        while i < len_left and j < len_right:
            time.sleep(0.07)
            if left[i] <= right[j]:
                draw_app.lst[srt[k][1]] = left[i]
                lst[k] = left[i]
                draw_bars(
                    draw_app,
                    {srt[k][1]: draw_app.GREEN},
                    True,
                )
                i += 1
                k += 1
            else:
                draw_app.lst[r_srt[j][1]] = draw_app.lst[srt[k][1]]
                draw_app.lst[srt[k][1]] = right[j]
                lst[k] = right[j]
                draw_bars(
                    draw_app,
                    {srt[k][1]: draw_app.GREEN, r_srt[j][1]: draw_app.RED},
                    True,
                )
                j += 1
                k += 1
        while i < len_left:
            time.sleep(0.07)
            draw_app.lst[srt[k][1]] = left[i]
            lst[k] = left[i]
            draw_bars(draw_app, {srt[k][1]: draw_app.GREEN}, True)
            i += 1
            k += 1
        while j < len_right:
            time.sleep(0.07)
            draw_app.lst[srt[k][1]] = right[j]
            lst[k] = right[j]
            draw_bars(draw_app, {srt[k][1]: draw_app.GREEN}, True)
            j += 1
            k += 1
    # Descending Order
    else:
        while i < len_left and j < len_right:
            time.sleep(0.07)
            if left[i] >= right[j]:
                draw_app.lst[srt[k][1]] = left[i]
                lst[k] = left[i]
                draw_bars(
                    draw_app,
                    {srt[k][1]: draw_app.GREEN},
                    True,
                )
                i += 1
                k += 1
            else:
                draw_app.lst[r_srt[j][1]] = draw_app.lst[srt[k][1]]
                draw_app.lst[srt[k][1]] = right[j]
                lst[k] = right[j]
                draw_bars(
                    draw_app,
                    {srt[k][1]: draw_app.GREEN, r_srt[j][1]: draw_app.RED},
                    True,
                )
                j += 1
                k += 1
        while i < len_left:
            time.sleep(0.07)
            draw_app.lst[srt[k][1]] = left[i]
            lst[k] = left[i]
            draw_bars(
                draw_app,
                {srt[k][1]: draw_app.GREEN},
                True,
            )
            i += 1
            k += 1
        while j < len_right:
            time.sleep(0.07)
            draw_app.lst[srt[k][1]] = right[j]
            lst[k] = right[j]
            draw_bars(
                draw_app,
                {srt[k][1]: draw_app.GREEN},
                True,
            )
            j += 1
            k += 1


def main():
    # Set app loop trigger
    run = True

    # Initialiaze clock variable for tick rate
    clock = pygame.time.Clock()

    # Set list attributes
    n = 50
    min_val = 0
    max_val = 100

    # Create initial list
    lst = create_list(n, min_val, max_val)

    # Set init ascending
    ascending = True

    # Set init sorting
    sorting = False
    # Create App object (Standard: ascending = True at initialization)
    draw_app = DrawApp(600, 800, lst)

    #### Buttons ####
    objects = []
    bubble_button = Button(
        0,
        0,
        150,
        70,
        "Bubble",
        draw_app,
    )
    insertion_button = Button(0, 71, 150, 70, "Insertion", draw_app)
    merge_button = Button(0, 142, 150, 70, "Merge", draw_app)
    ascending_button = Button(650, 0, 150, 105, "Ascending", draw_app)
    descending_button = Button(
        650,
        107,
        150,
        105,
        "Descending",
        draw_app,
    )
    start_button = Button(151, 142, 248, 70, "Start", draw_app)
    reset_button = Button(
        401,
        142,
        248,
        70,
        "Reset",
        draw_app,
    )
    objects.append(bubble_button)
    objects.append(insertion_button)
    objects.append(merge_button)
    objects.append(ascending_button)
    objects.append(descending_button)
    objects.append(start_button)
    objects.append(reset_button)
    #### Buttons ####

    # Sorting Algorithm / Name / Generator
    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None

    while run:
        # refresh at 60ticks per second
        clock.tick(60)
        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
            except TypeError:
                sorting = False
        else:
            # Draw to window
            draw(draw_app, objects, sorting_algo_name, ascending)

        # Listen for events
        for event in pygame.event.get():
            # If corner x is pressed exit loop
            if event.type == pygame.QUIT:
                run = False

        if bubble_button.process():
            sorting_algorithm = bubble_sort
            sorting_algo_name = "Bubble Sort"
        if merge_button.process():
            sorting_algorithm = merge_sort
            sorting_algo_name = "Merge Sort"
        if insertion_button.process():
            sorting_algorithm = insertion_sort
            sorting_algo_name = "Insertion Sort"
        if reset_button.process():
            lst = create_list(n, min_val, max_val)
            draw_app.lst = lst
            sorting = False
        if start_button.process():
            sorting = True
            sorting_algorithm_generator = sorting_algorithm(
                draw_app, draw_app.lst, ascending
            )
        if ascending_button.process():
            ascending = True
            sorting = False
        if descending_button.process():
            ascending = False
            sorting = False

    pygame.quit()


if __name__ == "__main__":
    main()
