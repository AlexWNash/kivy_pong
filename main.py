from kivy.app import App
from kivy.clock import Clock
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.resources import resource_add_path
from random import choice, randint

resource_add_path('.\\assets')



class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            if vel[0] > 10:
                vel[0] = 10
            elif vel[0] < -10:
                vel[0] = -10
            ball.velocity = vel.x, vel.y + offset


class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongGame(Widget):

    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self, dt):
        self.ball.move()

        # bounce off paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        # bounce off top and bottom
        if (self.ball.y < 0) or (self.ball.top > self.height):
            self.ball.velocity_y *= -1

        # defines how the bot moves, randomly moves a few pixels or no pixels and only reacts once the ball is off center from it's paddle by a random amount
        bot_move = [0, 0, 5, 5, 5]
        bot_react = randint(0, 50)
        if self.ball.y + bot_react < self.player2.center_y:
            self.player2.center_y = self.player2.center_y - choice(bot_move)
        if self.ball.y - bot_react > self.player2.center_y:
            self.player2.center_y = self.player2.center_y + choice(bot_move)

        # score a point if it goes off to the side
        if self.ball.x < self.x:
            if self.player2.score == 9:
                self.player1.score = 0
                self.player2.score = 0
                self.serve_ball(vel=(4, 0))
            else:
                self.player2.score += 1
                self.serve_ball(vel=(4, 0))
        if self.ball.x > self.width:
            if self.player1.score == 9:
                self.player1.score = 0
                self.player2.score = 0
                self.serve_ball(vel=(-4, 0))
            else:
                self.player1.score += 1
                self.serve_ball(vel=(-4, 0))

    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y


class PongApp(App):

    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 60)
        return game


if __name__ == '__main__':
    app = PongApp()
    app.run()
