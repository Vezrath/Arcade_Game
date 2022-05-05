from turtle import *

FONT = ("Arial", 24, "normal")
HI_SCORE_FONT = ("Arial", 34, "normal")


class Scoreboard:

    def __init__(self):
        self.score = 0
        with open("hi_score", "r") as file:
            self.hi_score = int(file.read())

        self.hi_sam = Turtle()
        self.hi_sam.hideturtle()
        self.hi_sam.goto(x=420, y=500)
        self.hi_sam.pencolor("purple")
        self.hi_sam.write(f"Hi-score: {self.hi_score}", False, font=HI_SCORE_FONT)

        self.sam = Turtle()
        self.sam.hideturtle()
        self.sam.goto(x=420, y=300)
        self.sam.pencolor("white")
        self.sam.write(f"Current score: {self.score}", False, font=FONT)

    def update_score(self):
        self.sam.clear()
        self.score += 1
        self.sam.write(f"Current score: {self.score}", False, font=FONT)

    def update_high_score(self):
        self.hi_sam.clear()
        self.hi_sam.write(f"Hi-score: {self.score}", False, font=HI_SCORE_FONT)
        with open("hi_score", "w") as file:
            file.write(f"{self.score}")
