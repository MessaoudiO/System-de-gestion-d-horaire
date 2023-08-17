from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form
from wtforms import SelectMultipleField, SelectField
from sqlalchemy.orm.exc import NoResultFound
from collections import defaultdict
import datetime
import icalendar
import itertools

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///omnivox.db"
app.config["WTF_CSRF_ENABLED"] = False
app.config["ANALYTICS_ID"] = "UA-7457807-9"
db = SQLAlchemy(app)


START_HOUR = datetime.time(hour=9, minute=15)
END_HOUR = datetime.time(hour=17, minute=45)
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
WEEK_ONE = datetime.date(year=2013, month=7, day=29)


def dt(time):
    return datetime.datetime.combine(datetime.date.today(), time)

@app.route('/')
def start():
    from random import randint
    import time

    start = time.time()
    board = []

    for x in range(6):
        board.append(["_"] * 10)

    def print_board(board):
        for row in board:
            print ("   ".join(row))

    def random_o():
        return randint(0, 5)

    def random_x():
        return randint(0, 7)

    def random_l():
        return randint(0, 9)

    def bot_place(board, tag):
        bot_row = random_o()
        bot_col = random_x()
        if board[bot_row][bot_col] == "_":
            board[bot_row][bot_col] = tag
        else:
            bot_place(board, tag)


    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

    for i in range(0, 6):
        board[i][3] = "Pause"
        

    k = 0
    for j in range(0, 6):
        board[j][0] = days[k]
        k += 1




    def lab_place1(board, sub):
        lab_row = random_o()
        list1 = [1, 4, 7]
        rw = list1[ranno()]
        if board[lab_row][rw] == "_":
            board[lab_row][rw] = sub
            board[lab_row][rw+1] = sub
        if board[lab_row][rw+2] == "_":
            board[lab_row][rw+2] = sub

        else:
            print("\n")

    def lab_place2(board, sub):
        lab_row = random_o()
        list1 = [1, 4, 7]
        rw = list1[ranno()]
        if board[lab_row][rw] == "_":
            board[lab_row][rw] = sub
            board[lab_row][rw+1] = sub
        if board[lab_row][rw+2] == "_":
            board[lab_row][rw+2] = sub
        else:
            print("\n")

    def tut_place(board):
        for i in range(0, 6):
            for j in range(7, 10):
                if board[i][j] == "_":
                    board[i][j] = "TUT"

    def sub_fill(board):
        for i in range(0, 6):
            for j in range(0, 10):
                if board[i][j] == "_":
                    board[i][j] = sub_list[randint(0, 5)]

    lab_row = random_o()
    for i in range(1, 2):
        lab_place1(board, "MPL")

    for i in range(1, 2):
        lab_place2(board, "ADL")

    sub_list = ["MAT", "SE ", "DAA", "MP ", "OOC", "DC "]
    for i in range(4):
        for j in range(0, 6):
            bot_place(board, sub_list[j])

    tut_place(board)
    sub_fill(board)
    print("\n")
    print (print_board(board))
    print("\n")

    print("Time elapsed = " + str(time.time() - start) + " ms")

    return render_template("zxc.html", board=board)


if __name__ == "__main__":
    app.run()