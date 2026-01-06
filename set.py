import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.lines as lines
import matplotlib.path as path
import math, copy, time

PADDING = 0.1
ROW_LENGTH = 3
COLORS = {'green': '#66FF00', 'red':'red', 'blue':'blue'}

class Card:
    def __init__(self, shape: str, num: str, filling: str, color: str):
        self.shape = shape; self.num = num; self.filling = filling; self.color = color
        self.selected=False
    
    def __str__(self):
        return f'{self.num} {self.color} {self.filling} {self.shape}(s)'


def create_cylinder(x: float, y: float, ax, filling:str=None, color:str = COLORS['green'], size: float=0.6/1.75):
    Path = path.Path
    x -= size/2
    y -= size/2
    scale_x = 1.15
    path_data = [
        (Path.MOVETO, (x,y)),
        (Path.LINETO, (x,y+size)),
        (Path.CURVE4, (x,y+size+size/2)),
        (Path.CURVE4, (x+size/scale_x,y+size+size/2)),
        (Path.CURVE4, (x+size/scale_x,y+size)),
        (Path.LINETO, (x+size/scale_x,y)),
        (Path.CURVE4, (x+size/scale_x,y-size/2)),
        (Path.CURVE4, (x,y-size/2)),
        (Path.CURVE4, (x,y)),
    ]
    codes, verts = zip(*path_data)
    p = path.Path(verts, codes)

    fill = False
    if filling == 'full':
        fill=True
    patch = patches.PathPatch(p, linewidth=3, fill=fill, color=color)
    ax.add_patch(patch)

    if filling == 'striped':
        for idx in range(-1,9):
            line=lines.Line2D([x+0.02, x+size/1.2], [y + idx * 0.05, y + idx * 0.05], lw=1, color=color)
            ax.add_artist(line)

def create_diamond(x: float, y: float,ax, filling:str=None, size: float = 0.6/2.1, color: str = COLORS['green']):
    x -= size/2
    path_data = [
        (path.Path.MOVETO, (x-0.01/2, y-0.01)),
        (path.Path.LINETO, (x + size / 2, y+size)),
        (path.Path.LINETO, (x + size, y)),
        (path.Path.LINETO, (x + size / 2, y-size)),
        (path.Path.LINETO, (x-0.01/2, y+0.01)),
    ]

    codes, verts = zip(*path_data)
    p = path.Path(verts, codes)

    fill = False
    if filling == 'full':
        fill=True

    patch = patches.PathPatch(p, linewidth=3, fill=fill, color=color)
    ax.add_patch(patch)

    if filling == 'striped':
        sizes= [(x+0.06 , x+size/1.3), [x+0.06 , x+size/1.3], [x+0.02 , x+size/1.15], [x , x+size/1], [x+0.02 , x+size/1.15], [x+0.06 , x+size/1.3], [x+0.06 , x+size/1.3]]
        for idx in range(-3,4):
            line=lines.Line2D(sizes[idx+3], [y + idx * 0.05, y + idx * 0.05], lw=1, color=color)
            ax.add_artist(line)

def create_squiggle(x: float, y: float,  ax, filling:str=None, size: float = 0.36/2.1, color: str = COLORS['green']):
    x -= size/2
    y += size/1.4
    Path  = path.Path
    path_data = [
        (Path.MOVETO, (x, y)),
        (Path.CURVE4, (x-size,y+size/2)),
        (Path.CURVE4, (x+size,(6/3) * size + y)),
        (Path.CURVE4, (x+size,y)),

        (Path.CURVE4, (x+size,y- (0.1/0.3) * size)),
        (Path.CURVE4, (x+size,y- (0.3/0.3) * size)),
        (Path.CURVE4, (x + (0.26/0.3) * size,y- (0.6/0.3) * size)),

        (Path.CURVE4, (x + (0.25/0.3) * size,y- (0.65/0.3) * size)),
        (Path.CURVE4, (x + size,y- (0.65/0.3) * size)),
        (Path.CURVE4, (x + (0.35/0.3) * size,y- (0.7/0.3) * size)),

        (Path.CURVE4, (x + (0.38/0.3) * size,y- (0.8/0.3) * size)),
        (Path.CURVE4, (x + (0.2/0.3) * size,y- (0.85/0.3) * size)),
        (Path.CURVE4, (x + (0.05/0.3) * size,y- (0.8/0.3) * size)),

        (Path.CURVE4, (x - (0.1/0.3) * size,y- (0.7/0.3) * size)),
        (Path.CURVE4, (x,y- (0.6/0.3) * size)),
        (Path.CURVE4, (x + (0.05/0.3) * size,y- (0.4/0.3) * size)),

        (Path.CURVE4, (x + (0.1/0.3) * size,y)),
        (Path.CURVE4, (x + (0.05/0.3) * size,y)),
        (Path.CURVE4, (x - (0.02/0.3) * size,y)),
    ]

    codes, verts = zip(*path_data)
    p = path.Path(verts, codes)

    fill = False
    if filling == 'full':
        fill=True

    patch = patches.PathPatch(p, linewidth=3, fill=fill, color=color)
    ax.add_patch(patch)

    if filling == 'striped':
        sizes= [
            (x , x+size),
            [x, x+size/1.3],
            [x , x+size/1.2],
            [x+0.01 , x+size/1.1], 
            [x+0.04 , x+size/1.1],
            [x+0.05 , x+size/1.1],
            [x+0.05 , x+size/1.1],
            [x+0.05 , x+size/1.1],
            [x+0.02 , x+size/1.1],
            [x-0.02 , x+size/1.1],
            [x-0.03 , x+size/1.1],
            ]
        for idx in range(-8,3):
            line=lines.Line2D(sizes[idx+8], [y + idx * 0.05, y + idx * 0.05], lw=1, color=color)
            ax.add_artist(line)

class Set:
    def __init__(self):
        self.deck = self.generate_deck()
        self.grid = []
        self.total_selected = set()
        self.sets_cleared = 0
        self.rows = 4
        self.start_time = time.time()
        self.shuffle_deck()
        self.draw_cards()
        self.check_possible_selections()
        self.draw_until_valid()
        self.check_possible_selections()
        self.init_plot()
    
    def init_plot(self):
        self.fig, self.ax = plt.subplots(figsize=(10,6))
        self.cid = self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.display_game()
        plt.show()
    
    def draw_cards(self):
        while len(self.grid) < 12:
            self.grid.append(self.deck.pop(0))
    
    def draw_card(self):
        return self.deck.pop(0)
    
    def generate_deck(self) -> list[Card]:
        shapes = ['squiggle', 'round', 'diamond']
        num = ['1','2','3']
        fillings = ['full', 'striped', 'empty']
        colors = ['red', 'green', 'blue']
        deck = []
        for shape in shapes:
            for n in num:
                for filling in fillings:
                    for color in colors:
                        deck.append(Card(shape,n,filling,color))
        return deck

    def shuffle_deck(self):
        np.random.shuffle(self.deck)

    def create_block(self, x: str, y: str, color: str = COLORS['green'], filling: str = 'empty', shape: str = 'round', num: str = '3', selected=False):
        x = x * 4/3 + PADDING * (x+1)
        y = y + PADDING * (y+1)
        box_color = 'gray'
        if selected:
            box_color = 'black'
        box = patches.FancyBboxPatch((x,y),4/3,1.0, boxstyle='Round,pad=0, rounding_size=0.1', fill=None, linewidth=2, color=box_color)
        self.ax.add_patch(box)

        if shape == 'round':
            jitter =0.025
            if num == '1':
                create_cylinder(x + (2/3)+ jitter,y + (0.5), self.ax,filling=filling, color=color)
            elif num == '2':
                create_cylinder(x + (2/3) -0.2+ jitter,y + (0.5), self.ax, filling=filling, color=color)
                create_cylinder(x + (2/3) +0.2+ jitter,y + (0.5), self.ax, filling=filling, color=color)
            elif num =='3':
                create_cylinder(x + (2/3 - 0.4)+ jitter,y + (0.5), self.ax,filling=filling, color=color)
                create_cylinder(x + (2/3)+ jitter,y + (0.5), self.ax,filling=filling, color=color)
                create_cylinder(x + (2/3 + 0.4)+ jitter,y + (0.5),self.ax, filling=filling, color=color)
        elif shape == 'diamond':
            if num == '1':
                create_diamond(x + (2/3),y + (0.5), self.ax,filling=filling, color=color)
            elif num == '2':
                create_diamond(x + (2/3) -0.2,y + (0.5), self.ax,filling=filling, color=color)
                create_diamond(x + (2/3) +0.2,y + (0.5), self.ax,filling=filling, color=color)
            elif num =='3':
                create_diamond(x + (2/3 - 0.4),y + (0.5),self.ax, filling=filling, color=color)
                create_diamond(x + (2/3),y + (0.5), self.ax,filling=filling, color=color)
                create_diamond(x + (2/3 + 0.4),y + (0.5), self.ax,filling=filling, color=color)
        elif shape == 'squiggle':
            if num == '1':
                create_squiggle(x + (2/3),y + (0.5),self.ax, filling=filling, color=color)
            elif num == '2':
                create_squiggle(x + (2/3) -0.17,y + (0.5),self.ax, filling=filling, color=color)
                create_squiggle(x + (2/3) +0.17,y + (0.5), self.ax,filling=filling, color=color)
            elif num =='3':
                create_squiggle(x + (2/3 - 0.33),y + (0.5), self.ax,filling=filling, color=color)
                create_squiggle(x + (2/3),y + (0.5), self.ax,filling=filling, color=color)
                create_squiggle(x + (2/3 + 0.33),y + (0.5), self.ax,filling=filling, color=color)


    def display_game(self):
        self.ax.cla()
        if len(self.deck)==0 and self.total_possible ==0:
            self.fig.canvas.mpl_disconnect(self.cid)
            clear_time = round(time.time() - self.start_time)
            minutes = clear_time//60
            seconds = clear_time % 60
            self.ax.set_title(f'You cleared all {self.sets_cleared} possible sets in {minutes} minutes {seconds} seconds!')
        else:
            self.ax.set_title(f'Sets {self.sets_cleared} / Total possible {self.total_possible}')
        self.ax.set_aspect('equal')
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_xlim(right=4 + PADDING*4)
        self.ax.set_ylim(top=self.rows + PADDING * (self.rows+1))
        for index in range(len(self.grid)):
            row = index // ROW_LENGTH
            col = index % ROW_LENGTH
            card: Card = self.grid[index]
            self.create_block(col, row, color=COLORS[card.color], filling=card.filling, shape=card.shape, num=card.num, selected=card.selected)
        self.fig.canvas.draw_idle()

    def draw_until_valid(self):
        while len(self.deck) >= 3 and self.total_possible == 0:
            for idx in range(3):
                self.grid.append(self.draw_card())
            self.check_possible_selections()
        
        self.rows = len(self.grid) // 3

    def on_click(self, event):
        if event.inaxes:
            x = math.floor(event.xdata * 3/4 * 1/1.1)
            y = math.floor(event.ydata * 1/1.1)
            row = y 
            col = x
            card = self.grid[row * ROW_LENGTH +col]
            if card.selected:
                card.selected = False
                self.total_selected.remove(card)
            elif not card.selected:
                card.selected = True
                self.total_selected.add(card)
            if len(self.total_selected) >=3:
                cards = list(self.total_selected)
                if not self.check_selected(cards):
                    for card in self.total_selected:
                        card.selected = False
                    self.total_selected.clear()
                else:
                    if len(self.deck) >= 3:
                        # Cards in grid == 12
                        if len(self.grid) == 12:
                            for card in self.total_selected:
                                idx = self.grid.index(card)
                                self.grid[idx] = self.draw_card()
                        elif len(self.grid) >= 12:
                            # If grid - 3 has possibilities, just remove
                            temp = copy.deepcopy(self.grid)
                            for card in self.total_selected:
                                self.grid.remove(card)
                            if self.check_possible_selections() == 0:
                            # else redraw
                                self.grid = temp
                                for card in self.total_selected:
                                    idx = self.grid.index(card)
                                    self.grid[idx] = self.draw_card()

                    else:
                        for card in self.total_selected:
                            self.grid.remove(card)
                    self.total_selected.clear()
                    self.sets_cleared+=1
                self.check_possible_selections()
                self.draw_until_valid()
            self.display_game()

            # print(f'{self.grid[row * ROW_LENGTH +col]} row={row} col={col}, x={x} y={y}')
    
    def check_possible_selections(self):
        self.total_possible = 0
        # Checks all remaining possibilities
        for left in range(len(self.grid)-2):
            for middle in range(left+1,len(self.grid)-1):
                for right in range(middle+2,len(self.grid)):
                    self.total_possible += self.check_selected((self.grid[left],self.grid[middle],self.grid[right]))

    def check_selected(self, cards):
        card1: Card = cards[0]
        card2: Card  = cards[1]
        card3: Card  = cards[2]

        # Check colour
        if not ((card1.color == card2.color and card2.color == card3.color and card1.color==card3.color) or (card1.color !=card2.color and card2.color!=card3.color and card1.color !=card3.color)):
            return False
        # Check shapes
        if not ((card1.shape == card2.shape and card2.shape == card3.shape and card1.shape==card3.shape) or (card1.shape !=card2.shape and card2.shape!=card3.shape and card1.shape !=card3.shape)):
            return False
        # Check filling
        if not ((card1.filling == card2.filling and card2.filling == card3.filling and card1.filling==card3.filling) or (card1.filling !=card2.filling and card2.filling!=card3.filling and card1.filling !=card3.filling)):
            return False
        # Check number
        if not ((card1.num == card2.num and card2.num == card3.num and card1.num==card3.num) or (card1.num !=card2.num and card2.num!=card3.num and card1.num !=card3.num)):
            return False
        

        return True

    def __str__(self):
        pass


if __name__ == '__main__':
    game = Set()