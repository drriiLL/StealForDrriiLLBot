# snake_tk.py
# Простая Змейка на tkinter (только стандартная библиотека)
# Управление: стрелки ← ↑ → ↓, P — пауза/продолжить, R — рестарт, Esc — выход.
import random
import tkinter as tk

CELL = 20          # размер клетки (px)
GRID_W, GRID_H = 24, 24  # поле в клетках
SPEED_MS = 120     # скорость (мс между тиками)

BG_COLOR = "#0f0f0f"
SNAKE_COLOR = "#39ff14"
FOOD_COLOR = "#ff3b3b"
GRID_COLOR = "#202020"
TEXT_COLOR = "#e0e0e0"

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Змейка (tkinter)")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(
            root,
            width=GRID_W * CELL,
            height=GRID_H * CELL,
            bg=BG_COLOR,
            highlightthickness=0,
        )
        self.canvas.pack()

        self.status = tk.Label(
            root, text="Счёт: 0   [P] пауза  [R] рестарт  [Esc] выход", fg=TEXT_COLOR, bg=BG_COLOR
        )
        self.status.pack(fill="x")

        # направления: (dx, dy)
        self.dir = (1, 0)    # старт вправо
        self.next_dir = self.dir
        self.snake = []
        self.food = None
        self.score = 0
        self.running = True
        self.paused = False
        self.after_id = None

        self._bind_keys()
        self._restart()

    def _bind_keys(self):
        self.root.bind("<Left>",  lambda e: self._set_dir((-1, 0)))
        self.root.bind("<Right>", lambda e: self._set_dir((1, 0)))
        self.root.bind("<Up>",    lambda e: self._set_dir((0, -1)))
        self.root.bind("<Down>",  lambda e: self._set_dir((0, 1)))
        self.root.bind("<Escape>",lambda e: self.root.quit())
        self.root.bind("<p>",     lambda e: self._toggle_pause())
        self.root.bind("<P>",     lambda e: self._toggle_pause())
        self.root.bind("<r>",     lambda e: self._restart())
        self.root.bind("<R>",     lambda e: self._restart())

    def _set_dir(self, d):
        # запрет разворота на 180°
        if (d[0] == -self.dir[0] and d[1] == -self.dir[1]):
            return
        self.next_dir = d

    def _toggle_pause(self):
        if not self.running:
            return
        self.paused = not self.paused
        if not self.paused:
            self._loop()
        else:
            if self.after_id:
                self.root.after_cancel(self.after_id)
                self.after_id = None
        self._draw()

    def _restart(self, *_):
        # начальная змейка длиной 3 по центру
        cx, cy = GRID_W // 2, GRID_H // 2
        self.snake = [(cx - 2, cy), (cx - 1, cy), (cx, cy)]
        self.dir = (1, 0)
        self.next_dir = self.dir
        self.score = 0
        self.running = True
        self.paused = False
        self._spawn_food()
        self._draw()
        if self.after_id:
            self.root.after_cancel(self.after_id)
        self._loop()

    def _spawn_food(self):
        free = {(x, y) for x in range(GRID_W) for y in range(GRID_H)} - set(self.snake)
        self.food = random.choice(list(free)) if free else None

    def _loop(self):
        if not self.running or self.paused:
            return
        self.dir = self.next_dir
        head = self.snake[-1]
        new_head = (head[0] + self.dir[0], head[1] + self.dir[1])

        # проверка столкновений со стеной или собой
        x, y = new_head
        if not (0 <= x < GRID_W and 0 <= y < GRID_H) or (new_head in self.snake):
            self.running = False
            self._draw_game_over()
            return

        self.snake.append(new_head)

        if self.food and new_head == self.food:
            self.score += 1
            self._spawn_food()
        else:
            self.snake.pop(0)  # двигаемся без роста

        self._draw()
        self.after_id = self.root.after(max(40, SPEED_MS - min(self.score * 2, 60)), self._loop)

    def _draw_grid(self):
        # лёгкая сетка для ориентира
        for i in range(1, GRID_W):
            x = i * CELL
            self.canvas.create_line(x, 0, x, GRID_H * CELL, fill=GRID_COLOR)
        for j in range(1, GRID_H):
            y = j * CELL
            self.canvas.create_line(0, y, GRID_W * CELL, y, fill=GRID_COLOR)

    def _draw(self):
        self.canvas.delete("all")
        self._draw_grid()

        # еда
        if self.food:
            self._cell_rect(self.food, FOOD_COLOR)

        # змейка
        for i, c in enumerate(self.snake):
            self._cell_rect(c, SNAKE_COLOR)

        # голова чуть крупнее
        if self.snake:
            hx, hy = self.snake[-1]
            pad = 2
            self.canvas.create_rectangle(
                hx * CELL + pad,
                hy * CELL + pad,
                (hx + 1) * CELL - pad,
                (hy + 1) * CELL - pad,
                outline="",
                fill=SNAKE_COLOR,
            )

        state = "Пауза" if self.paused else ("Игра" if self.running else "Конец")
        self.status.config(text=f"Счёт: {self.score}   [{state}]   [P] пауза  [R] рестарт  [Esc] выход")

        if not self.running:
            self._draw_game_over()

    def _cell_rect(self, cell, color):
        x, y = cell
        self.canvas.create_rectangle(
            x * CELL + 1,
            y * CELL + 1,
            (x + 1) * CELL - 1,
            (y + 1) * CELL - 1,
            outline="",
            fill=color,
        )

    def _draw_game_over(self):
        self.canvas.create_rectangle(0, 0, GRID_W * CELL, GRID_H * CELL, fill=BG_COLOR, stipple="gray25", outline="")
        self.canvas.create_text(
            GRID_W * CELL // 2,
            GRID_H * CELL // 2 - 10,
            text=f"Игра окончена!\nСчёт: {self.score}",
            fill=TEXT_COLOR,
            font=("Segoe UI", 16, "bold"),
            justify="center",
        )
        self.canvas.create_text(
            GRID_W * CELL // 2,
            GRID_H * CELL // 2 + 40,
            text="Нажмите R для рестарта или Esc для выхода",
            fill=TEXT_COLOR,
            font=("Segoe UI", 11),
        )

def main():
    root = tk.Tk()
    SnakeGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
