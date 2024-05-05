from manim import *

# This function returns an array containing all reachable positions for the knight.
def position_array(board, row, column):
    num_rows = len(board)
    num_columns = len(board[0])
    delta_row = [2, 1, 2, 1, -2, -1, -2, -1]
    delta_column = [1, 2, -1, -2, 1, 2, -1, -2]
    reachable_positions = []
    for i in range(8):
        if (row + delta_row[i] >= 0 and row + delta_row[i] <= num_rows - 1
            and column + delta_column[i] >= 0 and column + delta_column[i] <= num_columns - 1
                and board[row + delta_row[i]][column + delta_column[i]] == - 1):
            reachable_positions.append([row + delta_row[i], column + delta_column[i]])
    return reachable_positions

# This function returns a (rows x columns) knight's tour matrix, starting from (row, column).
def tour_matrix(rows, columns, row, column):
    board = [[-1 for _ in range(columns)] for _ in range(rows)]
    number = 0
    board[row][column] = number
    end_loop = columns * rows - 1
    for i in range(end_loop):
        pos_array = position_array(board, row, column)
        if len(pos_array) > 0:
            reachable_positions = position_array(board, row, column)
        else:
            return board
        minimum = reachable_positions[0]
        for pos in reachable_positions:
            if len(position_array(board, pos[0], pos[1])) < len(position_array(board, minimum[0], minimum[1])):
                minimum = pos
        row = minimum[0]
        column = minimum[1]
        board[row][column] = number + 1
        number = number + 1
    return board

# This function searches for a number in a matrix and returns its row and column indices, or it returns None if not found.
def find_pos(number, matrix):
    for row_index, row in enumerate(matrix):
        if number in row:
            col_index = row.index(number)
            return [row_index, col_index, 0]
    return None

class Warnsdorffs_Algorithm(MovingCameraScene):
    def construct(self):
        self.camera.background_color = BLACK

        # This function returns a visualization of a chessboard (VGroups of Rectangle objects).
        def return_ChessBoard(rows, columns):
            side_length = 1.5
            chess_board = VGroup()
            for j in range(rows):
                vg = VGroup()
                for i in range(columns):
                    x = i * (side_length) * 1.025
                    y = j * (side_length) * 1.025
                    if (i + j) % 2 == 0:
                        rect = Rectangle(width=side_length, height=side_length, color=BLACK, fill_color=WHITE, fill_opacity=1,
                                         stroke_width=0, stroke_color=BLACK).move_to(x * RIGHT + y * DOWN)
                    else:
                        rect = Rectangle(width=side_length, height=side_length, color=BLACK, fill_color=GREY_D,
                                         fill_opacity=1,
                                         stroke_width=0, stroke_color=BLACK).move_to(x * RIGHT + y * DOWN)
                    vg.add(rect)
                chess_board.add(vg)
            chess_board.move_to(ORIGIN)
            return chess_board

        # This function visualizes a knight's tour on a (rows x columns) chessboard, starting from (row, column).
        # Input:
        #   - rows: number of rows of the board
        #   - columns: number of columns of the board
        #   - row: row of the starting position
        #   - column: column of the starting position
        def visualize_KnightsTour(rows, columns, row, column):
            board = return_ChessBoard(rows, columns)
            knight = ImageMobject('KNIGHT_BLACK.png').scale(0.1).move_to(board[row][column])

            while board.height >= self.camera.frame.height or board.width >= self.camera.frame.width:
                self.camera.frame.scale(1.05)

            self.add_foreground_mobjects(knight)
            self.play(FadeIn(board, knight))
            self.wait(1)

            line_width = 6

            circ = Circle(radius=0.4, fill_color=WHITE, fill_opacity=1, stroke_width=line_width, stroke_color=BLACK).move_to(board[row][column].get_center())
            number_tex = Tex(0, color=BLACK, stroke_width=2).move_to(circ.get_center())
            vg_circ = VGroup(circ, number_tex)
            self.play(
            board[row][column].animate.set_fill(GREEN_E),
                  GrowFromCenter(vg_circ)
            )

            matrix = tour_matrix(rows, columns, row, column)
            number = 1
            for i in range(1, rows * columns):
                pos = find_pos(i-1, matrix)
                pos_next = find_pos(i , matrix)

                if pos_next == None:
                   fail_tex = Tex('WARNSDORFF\'S HEURISTIC FAILED!', stroke_width=2).scale(1.3)
                   rec_fail = Rectangle(width=fail_tex.width+0.5, height=fail_tex.height+0.5, fill_color=BLACK, fill_opacity=0.9, stroke_width=4, stroke_color=PURE_RED, stroke_opacity=0.9)
                   vg_fail = VGroup(rec_fail, fail_tex)
                   self.wait(1)
                   self.remove_foreground_mobjects(knight)
                   self.play(
                       GrowFromCenter(vg_fail),
                             board[pos[0]][pos[1]].animate.set_fill(RED_E),
                             FadeOut(knight)
                             )
                   self.wait(1)
                   return

                start_coord = knight.get_center()
                end_coord = board[pos_next[0]][pos_next[1]].get_center()
                vec = end_coord - start_coord
                arr = Line(start_coord + 1 * 0.4 * vec / np.linalg.norm(vec),
                           end_coord - 1 * 0.4 * vec / np.linalg.norm(vec),
                           color=BLACK, stroke_width=line_width)

                if i < rows * columns - 1:
                    circ = Circle(radius=0.4, fill_color=WHITE, fill_opacity=1, stroke_width=line_width, stroke_color=BLACK).move_to(board[pos_next[0]][pos_next[1]].get_center())
                    number_tex = Tex(number, color=BLACK, stroke_width=2).move_to(circ.get_center())
                    vg_circ = VGroup(circ, number_tex)
                    self.play(
                        Create(arr),
                        knight.animate.move_to(board[pos_next[0]][pos_next[1]].get_center()),
                        run_time=0.4
                    )
                    self.play(
                     GrowFromCenter(vg_circ),
                         board[pos_next[0]][pos_next[1]].animate.set_color(BLACK).set_fill(GOLD_E),
                         run_time=0.25
                     )
                else:
                     circ = Circle(radius=0.4, fill_color=WHITE, fill_opacity=1, stroke_width=line_width, stroke_color=BLACK).move_to(board[pos_next[0]][pos_next[1]].get_center())
                     number_tex = Tex(number, color=BLACK, stroke_width=2).move_to(circ.get_center())
                     vg_circ = VGroup(circ, number_tex)
                     self.play(
                        Create(arr),
                        knight.animate.move_to(board[pos_next[0]][pos_next[1]].get_center()),  # FadeOut(vg_txt_neighbors),
                        run_time=0.4
                     )
                     self.play(
                  GrowFromCenter(vg_circ),
                        board[pos_next[0]][pos_next[1]].animate.set_color(BLACK).set_fill(RED_E),
                        run_time=0.25
                     )
                number = number + 1

            self.wait(1)
            self.remove_foreground_mobjects(knight)
            self.play(FadeOut(knight))
            self.wait(1)
            self.play(
                *[FadeOut(mob) for mob in self.mobjects]
            )

        # Visualization of a knight's tour on a (3 x 4) board, starting from (0,0).
        visualize_KnightsTour(3,4,
                               0,0)
