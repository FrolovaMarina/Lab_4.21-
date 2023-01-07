FPS = 30
WINDOW_SIZE = (900, 700)
#BACKGROUND = (140, 30, 200)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CELL_COUNT = 8
CELL_SIZE = 70
COLOURS = ['black square.jpg', 'white square.png']
names = 'ABCDEFGH'
DIRECTIONS = {'A': ['B'],
              'B': ['A', 'C'],
              'C': ['B', 'D'],
              'D': ['C', 'E'],
              'E': ['D', 'F'],
              'F': ['E', 'G'],
              'G': ['F', 'H'],
              'H': ['G']
              }
Q_FIELD = [['A8', 'B8', 'C8', 'D8', 'E8', 'F8', 'G8', 'H8'],
           ['A7', 'B7', 'C7', 'D7', 'E7', 'F7', 'G7', 'H7'],
           ['A6', 'B6', 'C6', 'D6', 'E6', 'F6', 'G6', 'H6'],
           ['A5', 'B5', 'C5', 'D5', 'E5', 'F5', 'G5', 'H5'],
           ['A4', 'B4', 'C4', 'D4', 'E4', 'F4', 'G4', 'H4'],
           ['A3', 'B3', 'C3', 'D3', 'E3', 'F3', 'G3', 'H3'],
           ['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2'],
           ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1']]

QUEEN_DIRECTIONS = {'A': [['B'], ['C'], ['D'], ['E'], ['F'], ['G'], ['H']],
                    'B': [['A', 'C'], ['D'], ['E'], ['F'], ['G'], ['H']],
                    'C': [['B', 'D'], ['A', 'E'], ['F'], ['G'], ['H']],
                    'D': [['C', 'E'], ['B', 'F'], ['A', 'G'], ['H']],
                    'E': [['D', 'F'], ['C', 'G'], ['B', 'H'], ['A']],
                    'F': [['E', 'G'], ['D', 'H'], ['C'], ['B'], ['A']],
                    'G': [['F', 'H'], ['E'], ['F'], ['F'], ['G'], ['H']],
                    'H': [['G'], ['F'], ['E'], ['D'], ['C'], ['B'], ['A']]
                    }
# QUEENS_DIRECTIONS = {'A': {'B': {'C': {'D': {'E': {'F': {'G': 'H'}}}}}},
#                      'B': {'A': None, 'C': {'D': {'E': {'F': {'G': 'H'}}}}},
#                      'C': {'B': 'A', 'D': {'E': {'F': {'G': 'H'}}}},
#                      'D': {'C': {'B': 'A'}, 'E': {'F': {'G': 'H'}}},
#                      'E': {'D': {'C': {'B': 'A'}}, 'F': {'G': 'H'}},
#                      'F': {'B': 'A', 'D': {'E': {'F': {'G': 'H'}}}},
#                      'G': {'H': None, 'F': {'E': {'D': {'C': {'B': 'A'}}}}},
#                      'H': {'G': {'F': {'E': {'D': {'C': {'B': 'A'}}}}}}
#                       }
HIT_DIRECTIONS = {'A': {'B': 'C'},
                  'B': {'C': 'D'},
                  'C': {'B': 'A', 'D': 'E'},
                  'D': {'C': 'B', 'E': 'F'},
                  'E': {'D': 'C', 'F': 'G'},
                  'F': {'E': 'D', 'G': 'H'},
                  'G': {'F': 'E'},
                  'H': {'G': 'F'}
                  }
WHITE_QUEEN_FIELD = {'B8', 'D8', 'F8', 'H8'}
BLACK_QUEEN_FIELD = {'A1', 'C1', 'E1', 'G1'}
types = {
    'ch': ('Checker2', 'b'), 'CH': ('Checker1', 'w'),
    'q': ('Queen2', 'b'), 'Q': ('Queen1', 'w'),
}
