"""Interaktiv tutorial som guidar spelaren genom grundmoment."""

class Tutorial:
    """Stegvis tutorial som validerar spelarens handlingar."""

    def __init__(self) -> None:
        self.steps = [
            "Rör dig med WASD",
            "Skjut pucken med SPACE",
            "Använd din specialförmåga med E",
        ]
        self.current = 0
        self.move_timer = 0.0
        self.completed = False

    def update(self, dt: float, input_state, game_state, special_used: bool) -> None:
        """Uppdatera tutorial-status baserat på input och spelhändelser."""
        if self.completed:
            return

        if self.current == 0:
            if input_state.move_x != 0 or input_state.move_y != 0:
                self.move_timer += dt
            if self.move_timer >= 0.8:
                self.current += 1

        elif self.current == 1:
            if input_state.shoot_pressed:
                self.current += 1

        elif self.current == 2:
            if special_used:
                self.current += 1

        if self.current >= len(self.steps):
            self.completed = True

    def hint(self) -> str:
        """Returnerar aktuell instruktionstext."""
        if self.completed:
            return "Tutorial klar! Spela matchen."
        return f"Tutorial: {self.steps[self.current]}"
