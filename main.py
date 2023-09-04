import pygame
import os
import math
import time
pygame.font.init()


WIDTH, HEIGHT = 500, 800
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Curling Game")

TARGET_CIRCLE = pygame.draw.circle(WINDOW, "white", (75, -30), 1)
TARGET_PNG = pygame.image.load(os.path.join("Assets", "Target.png"))
TARGET = pygame.transform.scale(TARGET_PNG, (350, 350))

RED_POINTS = 0
BLUE_POINTS = 0


class Rock:

    def __init__(self, color, x_cor):
        self.start_pos = (x_cor, 760)
        self.circle = pygame.draw.circle(WINDOW, "white", self.start_pos, 10)
        if color == "red":
            self.color = "red"
            self.image_file = pygame.image.load((os.path.join("Assets", "Red_Rock.png")))
        if color == "blue":
            self.color = "blue"
            self.image_file = pygame.image.load((os.path.join("Assets", "Blue_Rock.png")))
        self.image = pygame.transform.scale(self.image_file, (40, 50))
        self.hit_box = pygame.Rect(self.circle.x + 9, self.circle.y + 13, 25, 25)
        self.power = 0
        self.angle = 0
        self.x_interval = 0
        self.x_movement = 0
        self.y_movement = -1

    def move(self, rocks):
        self.x_movement += self.x_interval

        self.circle.y += self.y_movement
        self.hit_box.y += self.y_movement

        if self.x_movement > 1:
            self.circle.x += 1
            self.hit_box.x += 1
            self.x_movement = 0

        if self.x_movement < -1:
            self.circle.x -= 1
            self.hit_box.x -= 1
            self.x_movement = 0

        self.power -= 1

        self.collision(rocks)

    def collision(self, rocks):
        stones = [stone for stone in rocks if stone != self]

        for stone in stones:
            if self.hit_box.colliderect(stone.hit_box):
                stone.power = self.power / 4
                self.power /= 2

                stone.y_movement = -1
                self.y_movement *= -1
                self.x_movement *= -1

                self.circle.x += self.x_movement * 3
                self.hit_box.x += self.x_movement * 3
                stone.x_movement = self.x_movement
                stone.circle.x += stone.x_movement * 3
                stone.hit_box.x += stone.x_movement * 3

                self.circle.y += self.y_movement * 3
                self.hit_box.y += self.y_movement * 3
                stone.circle.y += stone.y_movement * 3
                stone.hit_box.y += stone.y_movement * 3


def draw_window(rocks):
    WINDOW.fill("white")
    WINDOW.blit(TARGET, (TARGET_CIRCLE.x, TARGET_CIRCLE.y))
    pygame.draw.circle(WINDOW, "black", (250, 145), 5)
    pygame.draw.circle(WINDOW, "black", (250, 800), 5)

    point_font = pygame.font.SysFont("comicsans", 40)
    red_points_text = point_font.render("Red: " + str(RED_POINTS), 1, "black")
    blue_points_text = point_font.render("Blue: " + str(BLUE_POINTS), 1, "black")
    WINDOW.blit(red_points_text, (10, 600))
    WINDOW.blit(blue_points_text, (500 - blue_points_text.get_width() - 10, 600))

    for rock in rocks:
        WINDOW.blit(rock.image, (rock.circle.x, rock.circle.y))
        pygame.draw.circle(WINDOW, "black", (rock.circle.x + 21, rock.circle.y + 25), 2)


def power_slider(clock):
    # 260 is the center of the power meter
    done = False
    direction = 1
    power_meter_png = pygame.image.load(os.path.join("Assets", "Power_Meter.png"))
    power_meter = pygame.transform.scale(power_meter_png, (500, 450))
    slider = pygame.Rect(50, 500, 10, 40)

    while not done:
        clock.tick(60)
        WINDOW.blit(power_meter, (0, 300))
        pygame.draw.rect(WINDOW, "black", slider)

        pygame.display.update()
        if slider.x < 500 and direction == 1:
            slider.x += 15
        elif slider.x >= 500 and direction == 1:
            direction = 2

        if slider.x > 20 and direction == 2:
            slider.x -= 15
        elif slider.x <= 20 and direction == 2:
            direction = 1
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return slider.x // 10
            elif event.type == pygame.QUIT:
                exit()


def angle_selection(rocks, clock):
    done = False
    x, y = 250, 450
    while not done:
        clock.tick(60)

        draw_window(rocks)
        pygame.draw.line(WINDOW, "black", (250, 770), (x, y), width=3)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_LEFT] and x > 0:
            x -= .5
        if keys_pressed[pygame.K_RIGHT] and x < 500:
            x += .5
        if keys_pressed[pygame.K_SPACE]:
            return int(x)


def set_angle_and_power(rock):
    rock.power *= 20
    if rock.angle < 250:
        rock.x_interval = (250 - rock.angle) / 320 * -1
    elif rock.angle > 250:
        rock.x_interval = (rock.angle - 250) / 320
    else:
        rock.x_interval = 0


def check_winner(rocks):
    closest = 500
    winning_color = "none"

    for rock in rocks:

        vertical = (rock.circle.y + 21) - 145
        horizontal = (rock.circle.x + 20) - 250

        if vertical < 0:
            vertical *= -1
        if horizontal < 0:
            horizontal *= -1

        distance = math.hypot(horizontal, vertical)

        if distance < closest:
            closest = distance
            winning_color = rock.color

    return winning_color


def draw_winner(winner):
    winner_font = pygame.font.SysFont("comicsans", 80)
    winner_text = winner_font.render(winner, 1, "black")
    WINDOW.blit(winner_text, (250 - winner_text.get_width() // 2, 350))
    pygame.display.update()
    time.sleep(5)


def main():
    done = False
    turn = 1
    clock = pygame.time.Clock()

    global RED_POINTS, BLUE_POINTS
    RED_POINTS, BLUE_POINTS = 0, 0

    r1 = Rock("red", 50)
    r2 = Rock("red", 100)
    r3 = Rock("red", 150)
    b1 = Rock("blue", 450)
    b2 = Rock("blue", 400)
    b3 = Rock("blue", 350)
    rocks = [r1, r2, r3, b1, b2, b3]

    while not done:
        clock.tick(60)
        draw_window(rocks)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        rock = rocks[0]

        if turn == 2:
            rock = rocks[3]
        elif turn == 3:
            rock = rocks[1]
        elif turn == 4:
            rock = rocks[4]
        elif turn == 5:
            rock = rocks[2]
        elif turn == 6:
            rock = rocks[5]

        if turn <= 6:
            rock.circle.x, rock.circle.y = 230, 750
            rock.hit_box.x, rock.hit_box.y = 239, 763
            if rock.angle == 0:
                rock.angle = angle_selection(rocks, clock)
            if rock.power == 0 and rock.angle != 0:
                rock.power = power_slider(clock)
                set_angle_and_power(rock)

            while r1.power > 0 or r2.power > 0 or r3.power > 0 or b1.power > 0 or b2.power > 0 or b3.power > 0:
                if r1.power > 0:
                    r1.move(rocks)
                if r2.power > 0:
                    r2.move(rocks)
                if r3.power > 0:
                    r3.move(rocks)
                if b1.power > 0:
                    b1.move(rocks)
                if b2.power > 0:
                    b2.move(rocks)
                if b3.power > 0:
                    b3.move(rocks)
                draw_window(rocks)
                pygame.display.update()

        elif turn == 7:
            winner = check_winner(rocks)
            if winner == "blue":
                BLUE_POINTS += 1
            elif winner == "red":
                RED_POINTS += 1

            if RED_POINTS < 3 and BLUE_POINTS < 3:
                turn = 0
                draw_window(rocks)
                pygame.display.update()
                time.sleep(2)
                for rock in rocks:
                    rock.__init__(rock.color, rock.start_pos[0])
            else:
                if RED_POINTS > BLUE_POINTS:
                    draw_winner("RED WINS")
                elif BLUE_POINTS > RED_POINTS:
                    draw_winner("BLUE WINS")
                main()

        draw_window(rocks)
        pygame.display.update()
        turn += 1


if __name__ == "__main__":
    main()
