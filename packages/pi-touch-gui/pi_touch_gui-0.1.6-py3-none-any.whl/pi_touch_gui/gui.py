
import pygame

from .colors import BLACK


class Page(object):

    def __init__(self, widgets=None, background=None, function=None):
        self._widgets = [] if widgets is None else widgets

        if background is not None:
            self.background = pygame.image.load(background).convert()
        else:
            self.background = None
        self.function = function

    def add_widgets(self, widgets):
        self._widgets += widgets

    def touch_handler(self, event, touch):
        """Update all widgets with a specific touch event, first one
            to consume it wins.
        """
        for widget in self._widgets:
            consumed, new_page = widget.event(event, touch)
            if consumed:
                return new_page

        if callable(self.function):
            return self.function(None)
        return None

    def render(self, screen):
        """Redraw all widgets to screen"""
        if self.background is not None:
            screen.blit(self.background, (0,0))
        else:
            screen.fill(BLACK)
        for widget in self._widgets:
            widget.render(screen)

class GUI(object):

    FPS = 60
    FADE_TIME = 60
    BLACKOUT_TIME = 300
    # FADE_TIME = 5
    # BLACKOUT_TIME = 10
    BRIGHT_LEVEL = 128
    FADE_LEVEL = 16

    last_event = pygame.time.get_ticks()

    def __init__(self, touchscreen):
        self._touchscreen = touchscreen
        self._current_page = None
        self._first_page = None
        self.faded = False
        self.blacked = False

        with open('/sys/class/backlight/rpi_backlight/max_brightness', 'r') as f:
            max_str = f.readline()
        self.max_brightness = min(int(max_str), 255)
        self.set_brightness(self.BRIGHT_LEVEL)

    def reset_display(self):
        self.last_event = pygame.time.get_ticks()

        if self.faded:
            self.set_brightness(self.BRIGHT_LEVEL)
            self.fade = False
        if self.blacked:
            self.set_light(True)
            self.blacked = False

    def set_brightness(self, level):
        level_str = f"{min(self.max_brightness, level)}\n"
        with open('/sys/class/backlight/rpi_backlight/brightness', 'w') as f:
            f.write(level_str)

    def set_light(self, on):
        if on is True:
            blank_str = "0"
        else:
            blank_str = "1"
            self._current_page = self._first_page
            self._current_page.render(self._touchscreen.surface)
        with open('/sys/class/backlight/rpi_backlight/bl_power', 'w') as f:
            f.write(blank_str)

    def run(self, page):
        self._current_page = page
        self._first_page = page

        self._touchscreen.run()

        fpsClock = pygame.time.Clock()

        def handle_touches(e, t):
            self.reset_display()

            touch_result = self._current_page.touch_handler(e, t)
            if touch_result is not None:
                if isinstance(touch_result, Page):
                    self._current_page = touch_result
                else:
                    print(f"Unsupported touch result {type(touch_result)!r}")

        for touch in self._touchscreen.touches:
            touch.on_press = handle_touches
            touch.on_release = handle_touches
            touch.on_move = handle_touches

        try:
            while True:
                time = pygame.time.get_ticks()
                # deltaTime in seconds.
                deltaTime = (time - self.last_event) / 1000.0
                if deltaTime > self.BLACKOUT_TIME:
                    self.set_light(False)
                    self.blacked = True
                elif deltaTime > self.FADE_TIME:
                    self.set_brightness(self.FADE_LEVEL)
                    self.faded = True

                self._current_page.render(self._touchscreen.surface)
                pygame.display.flip()
                fpsClock.tick(60)
        except (KeyboardInterrupt, Exception) as e:
            self.reset_display()
            print(f"Received exception {type(e)!r}: {e}")
            print("Stopping touchscreen thread...")
            self._touchscreen.stop()
            print("Exiting GUI...")
            exit()
