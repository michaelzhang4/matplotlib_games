import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.collections as collections
import matplotlib, math
import numpy as np

# Settings
grid_size = 16
mines = 25

# Block
class Block:
    def __init__(self, row: int, col: int, mine: bool):
        self.row = row
        self.col = col
        self.mine = mine
        self.revealed = False
        self.flagged = False
        self.nearby_mines = 0

    def __str__(self):
        return f'[{self.nearby_mines}] - {self.mine} '

class Minesweeper:
    def __init__(self, grid_size: int = 9, mines: int = 10):
        self.grid_size = grid_size
        self.mines = mines
        self.total_revealed = grid_size * grid_size - self.mines
        self.revealed = 0

        # Create grid and set mines
        self.grid = []
        mine_locations = np.random.choice(grid_size * grid_size, mines, replace=False)

        for row in range(grid_size):
            temp_row = []
            for col in range(grid_size):
                index = row * grid_size + col
                mine = index in mine_locations
                block = Block(row, col, mine)
                temp_row.append(block)
            self.grid.append(temp_row)

        for index in range(grid_size*grid_size):
            row = index // self.grid_size
            col = index % self.grid_size
            dirs=[-grid_size-1, -grid_size, -grid_size+1, -1, +1, -1 + grid_size, grid_size, grid_size + 1]
            count = 0
            for dir in dirs:
                if col == self.grid_size - 1:
                    if dir in [-grid_size+1, 1, grid_size+1]:
                        continue
                if col == 0:
                    if dir in [-grid_size-1, -1, grid_size-1]:
                        continue
                new_index = index +dir
                if new_index in mine_locations:
                    count += 1
            self.grid[index // grid_size][index % grid_size].nearby_mines = count

        self.grid = np.array(self.grid)

        # # print blocks        
        # for row in range(grid_size):
        #     row_str = ''
        #     for col in range(grid_size):
        #         row_str += str(self.grid[row, col])
        #     print(row_str)


        # Visualize grid
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(right = grid_size)
        self.ax.set_ylim(top = grid_size)
        self.ax.set_aspect('equal')
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_title('Minesweeper')
        self.rect_size = 1.0
        self.pc = None

        self.display_grid()
        # self.rects = []
        # for idx in np.ndindex(self.grid.shape):
        #     color = 'r' if self.grid[idx].mine == True else 'b'
        #     rect = patches.Rectangle((idx[1], grid_size - idx[0]-1),self.rect_size,self.rect_size, color =color)
        #     self.rects.append(rect)

        # self.pc = collections.PatchCollection(self.rects, match_original = True)
        # self.ax.add_collection(self.pc)

        for col in range(self.grid.shape[1]+1):
            self.ax.axvline(col, linewidth=6, color='white')

        for row in range(self.grid.shape[0]+1):
            self.ax.axhline(row, linewidth=6, color='white')

        self.cid = self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        plt.show()

    # Interactivity
    def on_click(self, event: matplotlib.backend_bases.Event):
        if event.inaxes:
            x = math.floor(event.xdata)
            y = math.floor(event.ydata)
            col = x
            row = grid_size -1 - y

            # Normal click for mining
            if event.button == 1:
                if self.grid[row, col].mine:
                    self.ax.text(2,4, 'You lose!', size = 40, color='red')
                    self.fig.canvas.mpl_disconnect(self.cid)
                else:
                    stack = [(row,col)]
                    while len(stack) > 0:
                        r,c = stack.pop(0)
                        self.grid[r, c].revealed = True
                        if self.grid[r,c].nearby_mines == 0:
                            dirs = [(-1,-1), (-1,0),(-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
                            for d_row, d_col in dirs:
                                new_row = r + d_row
                                new_col = c + d_col
                                if new_row < 0 or new_row >= self.grid_size or new_col < 0 or new_col >= self.grid_size:
                                    continue
                                if not self.grid[new_row, new_col].revealed and not self.grid[new_row, new_col].mine:
                                    stack.append((new_row, new_col))

            # Right Click for flag
            elif event.button == 3:
                self.grid[row, col].flagged = not self.grid[row, col].flagged

            self.display_grid()
            self.count_mines()
            self.check_win()

    def check_win(self):
        if self.revealed == self.total_revealed:
            self.ax.text(2,4, 'You win!', size = 40, color='green')
            self.fig.canvas.mpl_disconnect(self.cid)
        
    def count_mines(self):
        count = 0
        for index in np.ndindex(self.grid.shape):
            count += (not self.grid[index].mine) and self.grid[index].revealed
        self.revealed = count

    def display_grid(self):
        rects = []
        if self.pc:
            self.pc.remove()
        for index in np.ndindex(self.grid.shape):
            blk = self.grid[index]
            x = index[1]
            y = self.grid_size - 1 - index[0]
            if blk.revealed:
                clr = 'white'
                text_clr = 'black'
                if blk.nearby_mines > 0 and not blk.mine:
                    self.ax.text(x+0.4, y+0.4,str(blk.nearby_mines), color=text_clr)
            elif blk.flagged:
                clr = 'red'
                text_clr = 'red'
            else:
                clr = 'blue'
                text_clr = 'white'
            rect = patches.Rectangle((x,y), self.rect_size, self.rect_size, color = clr)
            rects.append(rect)
        self.pc = collections.PatchCollection(rects, match_original=True)
        self.ax.add_collection(self.pc)
        self.fig.canvas.draw_idle()
            
if __name__ == '__main__':
    minesweeper = Minesweeper(grid_size=grid_size, mines=mines)
    