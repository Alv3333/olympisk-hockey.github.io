"""Input-modul för att isolera tangentlogik från game loop."""

import pygame


class InputState:
    """Lagrar ett snapshot av aktuell input."""

    def __init__(self) -> None:
        self.move_x = 0
        self.move_y = 0
        self.shoot_pressed = False
        self.special_pressed = False
        self.restart_pressed = False
        self.quit_pressed = False


def read_input(events: list[pygame.event.Event]) -> InputState:
    """Läser keyboard-state för rörelse och actions."""
    keys = pygame.key.get_pressed()
    state = InputState()

    if keys[pygame.K_a]:
        state.move_x -= 1
    if keys[pygame.K_d]:
        state.move_x += 1
    if keys[pygame.K_w]:
        state.move_y -= 1
    if keys[pygame.K_s]:
        state.move_y += 1

    for event in events:
        if event.type == pygame.QUIT:
            state.quit_pressed = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                state.shoot_pressed = True
            elif event.key == pygame.K_e:
                state.special_pressed = True
            elif event.key == pygame.K_r:
                state.restart_pressed = True
            elif event.key == pygame.K_ESCAPE:
                state.quit_pressed = True

    return state
