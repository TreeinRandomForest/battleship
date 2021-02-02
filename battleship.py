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

        self.n_to_hit = (self.board > 0).sum()

    def play(self):
        self.state = np.zeros(shape=(self.N, self.N)) #what the opposite player sees
        
        
    def hit(self, row, col, print_state=True):
        if row < 0 or row >= self.N:
            raise ValueError(f"Please ensure row is between 0 and {self.N-1} [inclusive]")
        if col < 0 or col >= self.N:
            raise ValueError(f"Please ensure col is between 0 and {self.N-1} [inclusive]")
        
        if self.state[row, col] != 0:
            raise ValueError(f"Hitting cell ({row}, {col}) again")

        if self.board[row, col] > 0:
            print(f"Hit at ({row}, {col})")
            self.state[row, col] = 1 #hit
            return 1

        else:
            print(f"Miss at ({row}, {col})")
            self.state[row, col] = -1 #miss
            return -1

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
    
        Modifications to rules below: updates to prob control moves
        1. Use epsilon-greedy strategy: argmax probs with 1-epsilon and random from probs with epsilon
        2. 

        '''
        prob = np.ones_like(self.state) #start with uniform probability
        prob_norm = prob / prob.sum()

        #get mappings
        flattened_domain = np.arange(self.N*self.N)
        idx_to_loc = {}
        loc_to_idx = {}

        idx_mat = np.arange(self.N*self.N).reshape(self.N, -1)
        for row in range(self.N):
            for col in range(self.N):
                idx = idx_mat[row, col]
                idx_to_loc[idx] = (row, col)
                loc_to_idx[(row, col)] = idx


        n_current_hits = 0
        n_misses = 0
        while n_current_hits != self.n_to_hit:
            #keep playing till hit all ships
            #in real games, game might terminate if opponent hits all your ships

            row, col = idx_to_loc[np.random.choice(flattened_domain, p=prob_norm.flatten())]
            hit_or_miss = self.hit(row, col)

            prob[row, col] = 0 #don't hit this spot again
            if hit_or_miss == 1: #increase weights for neighbors if hit
                n_current_hits += 1

                if row+1 < self.N: 
                    if self.state[row+1, col]==0: #if not probed before                    
                        prob[row+1, col] += 1

                if row-1 >= 0: 
                    if self.state[row-1, col]==0:
                        prob[row-1, col] += 1
    
                if col+1 < self.N: 
                    if self.state[row, col+1]==0:
                        prob[row, col+1] += 1
    
                if col-1 >= 0:
                    if self.state[row, col-1]==0:
                        prob[row, col-1] += 1

                print(self.board)
                print("-----------")
                print(self.state)
                print("-----------")
                print(prob)
                print("-----------")
            elif hit_or_miss==-1:
                n_misses += 1    

            prob_norm = prob / prob.sum() #re-normalize

            print(f'Hits: {n_current_hits} Misses: {n_misses}')

