import pygame
import sys
import heapq

from collections import defaultdict

GRID_SIZE = 20
BOX_SIZE = 30

WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
BLUE = (0,0,255)
YELLOW = (255, 255, 0)



def main():

    pygame.init()
    screen = pygame.display.set_mode((GRID_SIZE*BOX_SIZE , GRID_SIZE*BOX_SIZE))
    pygame.display.set_caption("Path Finder")
    clock = pygame.time.Clock()
    running = True

    start_point, end_point = None, None
    walls = set()
    is_mouse_dragging = False
    is_running_astar = False  # Flag to indicate if A* algorithm is running


    while running:
        for event in pygame.event.get():

            if event == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                    
                if not is_running_astar:

                    mouse_pos = pygame.mouse.get_pos()
                    row, col = get_box_indices(mouse_pos)

                    if start_point is None:
                        start_point = (row, col)                                    #Initialize Start point at first click
                    elif (end_point is None) and (row,col) != start_point:
                        end_point = (row, col)                                      #End point at second click
                    else:
                        is_mouse_dragging = True                                    #After first and second click, allow user to drag mouse

            if event.type == pygame.MOUSEBUTTONUP:
                is_mouse_dragging = False

            if event.type == pygame.MOUSEMOTION: #Add walls if they're not the initial and ending point

                if is_mouse_dragging and not is_running_astar:  # Only allow wall creation if A* algorithm is not running

                    mouse_pos = pygame.mouse.get_pos()
                    row, col = get_box_indices(mouse_pos)

                    if (row, col) != start_point and (row, col) != end_point:
                        walls.add((row, col))

                elif pygame.mouse.get_pressed()[0]:
                    mouse_pos = pygame.mouse.get_pos()
                    row, col = get_box_indices(mouse_pos)
                    if (row, col) != start_point and (row, col) != end_point and start_point and end_point:
                        walls.add((row, col))
                    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and not is_running_astar and start_point and end_point:
                    if start_point and end_point:
                        is_running_astar = True



            
        screen.fill(BLACK)
        draw_grid(screen)


        #Draw Starting, Ending point  -> then draw walls (green, red and white )

        if start_point is not None:
            pygame.draw.rect(screen, GREEN, (start_point[1] * BOX_SIZE, start_point[0] * BOX_SIZE, BOX_SIZE, BOX_SIZE))
        if end_point is not None:
            pygame.draw.rect(screen, RED, (end_point[1] * BOX_SIZE, end_point[0] * BOX_SIZE, BOX_SIZE, BOX_SIZE))


        for wall in walls:
            pygame.draw.rect(screen, WHITE, (wall[1] * BOX_SIZE, wall[0] * BOX_SIZE, BOX_SIZE, BOX_SIZE) )


        if is_running_astar:
            path = a_star(start_point, end_point, walls)

            if len(path) == 0:
                show_popup_message(screen, "No solution found!")
                pygame.display.update()
                pygame.time.delay(10000)
                pygame.quit()
                sys.exit()



            else:
                for node in path:
                    if node !=start_point and node != end_point:
                        pygame.draw.rect(screen, YELLOW, (node[1] * BOX_SIZE, node[0] * BOX_SIZE, BOX_SIZE, BOX_SIZE))
                        pygame.display.update()
                        pygame.time.delay(50)

        pygame.display.update()
        clock.tick(60)


def draw_grid(screen):

    """
    Draw grid lines on the screen.

    Args:
        screen (pygame.Surface): The Pygame surface representing the game window.
    """

    for x in range(0, GRID_SIZE*BOX_SIZE, BOX_SIZE):
        pygame.draw.line(screen, WHITE, (x, 0), (x, GRID_SIZE * BOX_SIZE))

    for y in range(0, GRID_SIZE*BOX_SIZE, BOX_SIZE):
        pygame.draw.line(screen, WHITE, (0, y), (GRID_SIZE * BOX_SIZE, y))



def get_box_indices(mouse_pos):
    """
    Get the row and column indices of the box that contains the given mouse position.

    Args:
        mouse_pos (tuple): The x and y coordinates of the mouse position.

    Returns:
        tuple: The row and column indices of the box.
    """
    row = mouse_pos[1] // BOX_SIZE
    col = mouse_pos[0] // BOX_SIZE
    return row, col


def get_neighbors(row, col):
    """
    Get the valid neighbors of a box in the grid.

    Args:
        row (int): The row index of the box.
        col (int): The column index of the box.

    Returns:
        list: A list of valid neighbor boxes.
    """
    
    neighbors = []

    #Check for if it's not the first/last row or the first/last column

    if row > 0:
        neighbors.append((row - 1, col))

    if row < GRID_SIZE - 1:
        neighbors.append((row + 1, col))

    if col > 0:
        neighbors.append((row, col - 1))

    if col < GRID_SIZE - 1:
        neighbors.append((row, col + 1))

    return neighbors



def manhattan_distance(p1, p2):
   
   """
   Calculate manhattan distance between p1 and p2 , where only horizontal and vertical movements are allowed

   Returns:
        int: Manhattan Distance between the points.
    
   """

   return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])



def a_star(start, end, walls):
    """
    Perform the A* algorithm to find the shortest path from the start point to the end point.

    Args:
        start (tuple): The coordinates of the start point.
        end (tuple): The coordinates of the end point.
        walls (set): A set containing the coordinates of the wall boxes.

    Returns:
        list: A list of coordinates representing the shortest path from start to end.
    """

    #Defining priority queue

    pq = [(0, start)]
    visited = set()

    parents = {}

    g_scores = defaultdict(lambda: float('inf'))
    g_scores[start] = 0                                 #Set all g_scores except starting node to infinity


    f_scores = defaultdict(lambda: float('inf'))
    f_scores[start] = manhattan_distance(start, end)

    while pq:

        _, current = heapq.heappop(pq) #Get current node to lowest priority one from pq


        if current == end:
            # Reconstruct the path from end to start using parent information
            path = []

            while current != start:
                path.append(current)
                current = parents[current]

            path.append(start)
            path.reverse()
            return path

        
        visited.add(current)

        for neighbour in get_neighbors(*current):
            if (neighbour in visited) or (neighbour in walls):
                continue

            neighbour_cost = g_scores[current] + 1

            if neighbour_cost < g_scores[neighbour]:

                g_scores[neighbour] = neighbour_cost
                parents[neighbour] = current

                # Calculate the estimated total cost from start to end through the neighbor
                f_scores[neighbour] = neighbour_cost + manhattan_distance(neighbour, end)

                # Add the neighbor to the priority queue
                heapq.heappush(pq, (f_scores[neighbour], neighbour))



    return []

def show_popup_message(screen, message):
    font = pygame.font.SysFont(None, 32)
    text = font.render(message, True, (255, 255, 255))
    text_rect = text.get_rect(center=(GRID_SIZE * BOX_SIZE // 2, GRID_SIZE * BOX_SIZE // 2))
    pygame.draw.rect(screen, (0, 0, 0), (text_rect.x - 10, text_rect.y - 10, text_rect.width + 20, text_rect.height + 20))
    pygame.draw.rect(screen, (255, 0, 0), (text_rect.x - 10, text_rect.y - 10, text_rect.width + 20, text_rect.height + 20), 3)
    screen.blit(text, text_rect)
    pygame.display.update()



if __name__ == '__main__':
    main()