from tkinter import *
import random

GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = input("Which mode would you like to play in? Easy, Normal, Hard?" ).lower()
if SPEED == "easy":
    SPEED = 500
elif SPEED == "normal":
    SPEED = 250
elif SPEED == "hard":
    SPEED = 50
else:
    print("Invalid mode entered. Defaulting to Normal." )
    SPEED = 250
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

class Snake:

    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill = SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:

    def __init__(self):
        self.respawn()

    def respawn(self):
        
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE)-1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]
        self.food_item = canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")
        #canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

def next_turn(snake, food):

    global direction, score
    
    x, y = snake.coordinates[0]

    if direction == "up":
        y  -= SPACE_SIZE
    elif direction == "down":
        y  += SPACE_SIZE
    elif direction == "left":
        x  -= SPACE_SIZE
    elif direction == "right":
        x  += SPACE_SIZE
        
    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:

        score += 1
        label.config(text="Score:{}".format(score))

        canvas.delete("food")
        food.respawn()
    else:
        
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)


def change_direction(new_direction):
    global direction

    if new_direction == 'left' and direction != 'right':
        direction = 'left'
    elif new_direction == 'right' and direction != 'left':
        direction = 'right'
    elif new_direction == 'up' and direction != 'down':
        direction = 'up'
    if new_direction == 'down' and direction != 'up':
            direction = 'down'           


def check_collisions(snake):
    x, y = snake.coordinates[0]


    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True


    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            print("GAME OVER")
            return True
    return False

    
def game_over():
    canvas.delete("all")
    canvas.create_text(canvas.winfo_width() // 2, canvas.winfo_height() // 2,
                       font=('consolas', 70), text="GAME OVER", fill="red", tag="gameover")



window = Tk()
window.title("Snake game")
window.resizable(False, False)

score = 0
direction = 'down'

label = Label(window, text="Score:{}".format(score), font=('consolas',40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()
 
window.update()


window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")


window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

window.bind('w', lambda event: change_direction('up'))   
window.bind('a', lambda event: change_direction('left'))
window.bind('s', lambda event: change_direction('down'))
window.bind('d', lambda event: change_direction('right'))

snake = Snake()
food = Food()


next_turn(snake, food)

window.mainloop()




