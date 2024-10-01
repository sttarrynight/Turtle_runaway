# This example is not working in Spyder directly (F5 or Run)
# Please type '!python turtle_runaway.py' on IPython console in your Spyder.
import tkinter as tk
import turtle, random

class RunawayGame:
    def __init__(self, canvas, runner, chaser, catch_radius=50, game_time=60):
        self.canvas = canvas
        self.runner = runner
        self.chaser = chaser
        self.catch_radius2 = catch_radius**2
        self.remaining_time = game_time  # 남은 게임 시간 (초)
        self.score = 0  # 점수 초기화

        # Initialize 'runner' and 'chaser'
        self.runner.shape('turtle')
        self.runner.color('blue')
        self.runner.penup()

        self.chaser.shape('turtle')
        self.chaser.color('red')
        self.chaser.penup()

        # # Instantiate turtles for drawing
        self.drawer = turtle.RawTurtle(canvas)
        self.drawer.hideturtle()
        self.drawer.penup()

        self.timer_drawer = turtle.RawTurtle(canvas)  # 타이머 및 점수를 그릴 turtle
        self.timer_drawer.hideturtle()
        self.timer_drawer.penup()

        # 게임 화면 크기 설정
        self.screen_width = 700
        self.screen_height = 700

    def is_catched(self):
        p = self.runner.pos()
        q = self.chaser.pos()
        dx, dy = p[0] - q[0], p[1] - q[1]
        return dx**2 + dy**2 < self.catch_radius2

    def start(self, init_dist=400, ai_timer_msec=100):
        self.runner.setpos((-init_dist / 2, 0))
        self.runner.setheading(0)
        self.chaser.setpos((+init_dist / 2, 0))
        self.chaser.setheading(180)
        
        # TODO) You can do something here and follows.
        self.update_timer_and_score() # 타이머 및 점수판 시작
        # 게임 로직 시작
        self.ai_timer_msec = ai_timer_msec
        self.canvas.ontimer(self.step, self.ai_timer_msec)

    def update_timer_and_score(self):
        # 타이머와 점수를 우측 상단에 표시
        self.timer_drawer.clear()
        self.timer_drawer.setpos(200, 260)  # 타이머 위치 설정 (우측 상단)
        self.timer_drawer.write(f'남은 시간: {self.remaining_time}초  점수: {self.score}', align="center", font=("Arial", 16, "normal"))

        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.canvas.ontimer(self.update_timer_and_score, 1000)  # 1초마다 갱신
        else:
            self.end_game("시간 종료!")

    def step(self):
        self.runner.run_ai(self.chaser.pos(), self.chaser.heading())
        self.chaser.run_ai(self.runner.pos(), self.runner.heading())

        # TODO) You can do something here and follows.
        is_catched = self.is_catched()
        # 도망자가 잡혔는지 확인
        if is_catched:
            self.score += 1  # 점수 증가
            self.reset_positions()  # 도망자와 추격자의 위치 재설정

        # Note) The following line should be the last of this function to keep the game playing
        self.canvas.ontimer(self.step, self.ai_timer_msec)

    def reset_positions(self):
        # 도망자와 추격자의 위치를 다시 설정 (임의의 위치로 재설정)
        self.runner.setpos(random.randint(-300, 300), random.randint(-300, 300))
        self.chaser.setpos(random.randint(-300, 300), random.randint(-300, 300))

    def end_game(self, message):
        self.drawer.undo()
        self.drawer.penup()
        self.drawer.setpos(0, 0)
        self.drawer.write(message, align="center", font=("Arial", 24, "bold"))
        # 게임 종료 후 움직임 멈춤
        self.runner.hideturtle()
        self.chaser.hideturtle()

    def check_bounds(self, turtle_obj):
        # 거북이가 화면 밖으로 나가지 않도록 설정
        x, y = turtle_obj.pos()
        if abs(x) > self.screen_width // 2 or abs(y) > self.screen_height // 2:
            turtle_obj.setpos(random.randint(-300, 300), random.randint(-300, 300))  # 화면 안으로 위치 재설정


class ManualMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

        # Register event handlers
        canvas.onkeypress(lambda: self.forward(self.step_move), 'Up')
        canvas.onkeypress(lambda: self.backward(self.step_move), 'Down')
        canvas.onkeypress(lambda: self.left(self.step_turn), 'Left')
        canvas.onkeypress(lambda: self.right(self.step_turn), 'Right')
        canvas.listen()

    def run_ai(self, opp_pos, opp_heading):
        pass

class RandomMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

    def run_ai(self, opp_pos, opp_heading):
        # 0~6까지의 모드를 설정하여 더 다양한 방향으로 이동
        mode = random.randint(0, 6)
        if mode == 0:
            self.forward(self.step_move)
        elif mode == 1:
            self.left(self.step_turn)
        elif mode == 2:
            self.right(self.step_turn)
        elif mode == 3:
            self.forward(self.step_move * 2)  # 더 빠르게 전진
        elif mode == 4:
            self.right(self.step_turn // 2)  # 더 부드럽게 회전
        elif mode == 5:
            self.left(self.step_turn * 4)  # 크게 왼쪽 방향 전환
        elif mode == 6:
            self.right(self.step_turn * 4)  # 크게 오른쪽 방향 전환

        # 경계 체크
        self.getscreen().parent.check_bounds(self)


if __name__ == '__main__':
    # Use 'TurtleScreen' instead of 'Screen' to prevent an exception from the singleton 'Screen'
    root = tk.Tk()
    canvas = tk.Canvas(root, width=700, height=700)
    canvas.pack()
    screen = turtle.TurtleScreen(canvas)

    # TODO) Change the follows to your turtle if necessary
    runner = RandomMover(screen)
    chaser = ManualMover(screen)

    # 화면 밖으로 나가는 것을 방지하기 위해 RunawayGame 클래스에 screen 객체 전달
    game = RunawayGame(screen, runner, chaser)
    screen.parent = game  # check_bounds에서 screen으로 부모 참조

    game.start()
    screen.mainloop()