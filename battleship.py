import numpy as np

#Can be clever and combine the horizontal/vertical parts but keeping for clarity

class Board:
    def __init__(self, N=10, N_limit=10):
        self.N = N
        self.N_limit = N_limit
        self.board = np.zeros(shape=(N,N))

    def place_ships(self):
        N = self.N
        for ship_length in range(1, 6):
            placed = False
            N_iter = 0

            while (not placed) and N_iter < self.N_limit:
                N_iter += 1
                
                #horizontal or vertical
                hv = np.random.randint(2)
                if hv==0:
                    #horizontal
                    min_col = 0
                    max_col = (N-ship_length)

                    row = np.random.randint(N)
                    col = np.random.randint(low=min_col, high=max_col+1)

                    if self.board[row, col:col+ship_length].sum()==0:
                        placed = True
                        self.board[row, col:col+ship_length] = ship_length
                        
                elif hv==1:
                    #vertical
                    min_row = 0
                    max_row = (N-ship_length)
                
                    col = np.random.randint(N)
                    row = np.random.randint(low=min_row, high=max_row+1)

                    if self.board[row:row+ship_length, col].sum()==0:
                        placed = True
                        self.board[row:row+ship_length, col] = ship_length


    def play(self):
        self.state = np.zeros(shape=(self.N, self.N)) #what the opposite player sees
        
        
    def hit(self, row, col, print_state=True):
        if row < 0 or row >= self.N:
            raise ValueError(f"Please ensure row is between 0 and {self.N-1} [inclusive]")
        if col < 0 or col >= self.N:
            raise ValueError(f"Please ensure col is between 0 and {self.N-1} [inclusive]")
        
        if self.board[row, col] > 0:
            print(f"Hit at (row, col)")
            self.state[row, col] = 1 #hit

        else:
            print(f"Miss at (row, col)")
            self.state[row, col] = -1 #miss

        if print_state:
            print(self.state)
        #self.state[row, col] = 0 means unknown

    def autoplay(self):
        '''
        1. Start with a uniform prior on full grid (N^2 elements)
        2. Use np.random.choice to sample (might have to flatten, sample and reshape)
        3. If hit: increase probability mass for 2 vertical neighbors, 2 horizontal neighbors
           If miss: decrease probability mass for 2 vertical neighbors, 2 horizontal neighbors (not sure if this is optimal)
        4. Go to step 2

        Questions: 
        1. how much to increase/decrease weights by?
        2. is there a principled way to do so? some likelihood model
        
        Measure:
        1. distribution of number of tries to discover all ships
        Victory involves discovering before opponent discovers our ships
        '''
        pass

    
        
