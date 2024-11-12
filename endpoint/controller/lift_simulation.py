import pygame
import random
import math
import requests
import io
from model.lift import LiftState

class LiftSeat:
    def __init__(self, capacity, index):
        self.capacity = capacity
        self.passengers = 0
        self.position = index / 30  # Evenly space seats

class LiftSimulator:
    def __init__(self, lift):
        self.lift = lift
        self.seats = [LiftSeat(4, i) for i in range(30)]  # 30 seats, each with 4-person capacity

        pygame.init()
        self.width, self.height = 1600, 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(f"Ski Lift Simulation - {lift.lift_id}")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.buttons = self.create_buttons()

        self.bg_color = (30, 30, 30)
        self.text_color = (200, 200, 200)
        self.lift_path_color = (100, 100, 100)
        self.seat_color_up = (0, 200, 0)
        self.seat_color_down = (100, 100, 100)
        self.icon_color = "#0baab5"

        # Load Material Icons
        self.icon_font = self.load_material_symbols_font()

        # Define icon characters
        self.base_icon_char = '\uE88A'  # 'home' icon
        self.peak_icon_char = '\uE564'  # 'landscape' icon

    def load_material_symbols_font(self):
        font_url = "https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200"
        response = requests.get(font_url)
        font_url = response.text.split("src: url(")[1].split(")")[0]
        font_response = requests.get(font_url)
        return pygame.font.Font(io.BytesIO(font_response.content), 48)

    def create_buttons(self):
        button_width, button_height = 120, 40
        buttons = []
        for i, state in enumerate(LiftState):
            buttons.append({
                'rect': pygame.Rect(10, 10 + i * (button_height + 10), button_width, button_height),
                'color': (80, 80, 80),
                'text': state.value,
                'state': state
            })
        return buttons

    def update(self, dt):
        if self.lift.state != LiftState.STOP:
            speed = 0.05 if self.lift.state == LiftState.FULL_STEAM else 0.025
            for seat in self.seats:
                seat.position += speed * dt
                if seat.position >= 1:
                    seat.position -= 1
                    # Passengers depart at high elevation)
                    seat.passengers = 0
                elif 0.49 <= seat.position < 0.51:
                    # Passengers board at low elevation)
                    seat.passengers = random.randint(1, seat.capacity)

    def draw_station_icon(self, x, y, is_top):
        icon_char = self.peak_icon_char if is_top else self.base_icon_char
        icon_surface = self.icon_font.render(icon_char, True, self.icon_color)
        icon_rect = icon_surface.get_rect(center=(x, y))
        self.screen.blit(icon_surface, icon_rect)

    def draw_lift(self):
        ellipse_width = self.width * 0.8
        ellipse_height = self.height * 0.7
        center_x, center_y = self.width // 2, self.height // 2
        pygame.draw.ellipse(self.screen, self.lift_path_color, (center_x - ellipse_width // 2, center_y - ellipse_height // 2, ellipse_width, ellipse_height), 2)

        for i, seat in enumerate(self.seats):
            angle = seat.position * 2 * math.pi
            x = center_x + int(math.cos(angle) * ellipse_width / 2)
            y = center_y + int(math.sin(angle) * ellipse_height / 2)

            is_up = math.pi < angle < 2 * math.pi
            color = self.seat_color_up if is_up else self.seat_color_down
            pygame.draw.rect(self.screen, color, (x - 15, y - 10, 30, 20))

            seat_text = self.font.render(f"{i+1}", True, self.text_color)
            self.screen.blit(seat_text, (x - 5, y - 8))
            if is_up:  # Display passenger count for seats on the upper half
                pass_text = self.font.render(f"{seat.passengers}", True, self.text_color)
                self.screen.blit(pass_text, (x - 5, y + 22))

        self.draw_station_icon(center_x - ellipse_width // 2 - 50, center_y - 20, False)  # Bottom station
        self.draw_station_icon(center_x + ellipse_width // 2 + 50, center_y - 20, True)  # Top station

        bottom_elevation = self.font.render(f"Elevation: {self.lift.start_elevation}m", True, self.text_color)
        top_elevation = self.font.render(f"Elevation: {self.lift.end_elevation}m", True, self.text_color)
        self.screen.blit(bottom_elevation, (center_x - ellipse_width // 2 - 60, center_y + 30))
        self.screen.blit(top_elevation, (center_x + ellipse_width // 2 + 10, center_y + 30))

    def draw_buttons(self):
        for button in self.buttons:
            pygame.draw.rect(self.screen, button['color'], button['rect'])
            text = self.font.render(button['text'], True, self.text_color)
            text_rect = text.get_rect(center=button['rect'].center)
            self.screen.blit(text, text_rect)

    def draw_info(self):
        info_text = [
            f"Lift ID: {self.lift.lift_id}",
            f"State: {self.lift.state.value}",
            f"Start: ({self.lift.start_lat}, {self.lift.start_lon})",
            f"End: ({self.lift.end_lat}, {self.lift.end_lon})",
            f"Total Capacity: {self.lift.num_seats} passengers",
            f"Seats: 30 x 4-person capacity"
        ]
        for i, text in enumerate(info_text):
            rendered_text = self.font.render(text, True, self.text_color)
            self.screen.blit(rendered_text, (10, self.height - 150 + i * 25))

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for button in self.buttons:
                            if button['rect'].collidepoint(event.pos):
                                self.lift.set_state(button['state'])

            self.update(dt)

            self.screen.fill(self.bg_color)
            self.draw_lift()
            self.draw_buttons()
            self.draw_info()
            pygame.display.flip()

        pygame.quit()
