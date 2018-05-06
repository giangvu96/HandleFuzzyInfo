import pygame
import random
import sys
import graphic.maps as maps
from graphic import car
from algorithm.dijkstra_algorithm import dijkstra
from algorithm.dijkstra_algorithm import GraphUndirectedWeighted
import xlrd
import graphic.traffic_lamp as traffic_lamp
import graphic.stone as stone
from pygame.locals import *

TRAFFIC_LAMP_POS = []
TRAFFIC_LAMP_COORDINATES = []

def main():
    clock = pygame.time.Clock()
    #map
    map = pygame.sprite.Group()
    map.add(maps.Map(0, 0, 1))

    #Find path
    g = GraphUndirectedWeighted(50)
    toa_do_graph = get_toa_do_graph()
    for i in range(0, len(toa_do_graph)-1):
        g.add_edge(toa_do_graph[i][0], toa_do_graph[i][1], toa_do_graph[i][2])
    shortest_path, distance = dijkstra(g, 1, 43)
    print(shortest_path, distance)

    toa_do_real = get_toa_do_real()
    print(toa_do_real)
    route = []
    for i in range(0, len(shortest_path)-1):
        route.append([round(float(toa_do_real[shortest_path[i]-1][1]), 1), round(float(toa_do_real[shortest_path[i]-1][2]), 1)])
    print(route)
    # #test route.
    # # route_2 = [[0.0, 186.0], [74.0, 186.0], [74.0, 0.0]]
    # # route_3 = [[494.0, 0.0], [494.0, 185.0], [595.0, 185.0], [595.0, 383.0], [549.0, 383.0], [549.0, 597.0],
    # #            [740.0, 597.0], [740.0, 480.0], [870.0, 480.0], [870.0, 700.0]]
    # #car
    cars = pygame.sprite.Group()
    cars2 = pygame.sprite.Group()
    cars3 = pygame.sprite.Group()
    controlled_car = car.Car(route[0][0], route[0][1], route[1][0], route[1][1])
    cars.add(controlled_car)
    # cars2.add(car.Car(route_2[0][0], route_2[0][1], route_2[1][0], route_2[1][1]))
    # cars3.add(car.Car(route_3[0][0], route_3[0][1], route_3[1][0], route_3[1][1]))

    #traffic
    traffic_lamp1 = traffic_lamp.TrafficLamp(148, 256, 0, 0)
    traffic_lamp2 = traffic_lamp.TrafficLamp(415, 255, 90, 1)
    traffic_lamps = pygame.sprite.Group()
    traffic_lamps.add(traffic_lamp1)
    traffic_lamps.add(traffic_lamp2)

    #stone
    stones = pygame.sprite.Group()
    stone_impediment = stone.Stone(218, 200, 90, 0)
    stones.add(stone_impediment)
    stone_status = (stone_impediment.status, len(route) - 1)

    running = True
    k = 0
    while running:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYUP:
                if keys[K_p]:
                    pass

                if keys[K_q]:
                    pygame.quit()
                    sys.exit(0)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
                break

            # mouse event

            if event.type == pygame.MOUSEBUTTONDOWN:
                pressed1, pressed2, pressed3 = pygame.mouse.get_pressed()
                if pressed1:
                    print("left click")
                    current_index = 300
                    random_index = random.randrange(int(218) + 3, int(300) + 6)
                    if random_index <= (len(route) - 3) and stone_impediment.status == 0:
                        x = route[random_index][0]
                        y = route[random_index][1]
                        stone_impediment.switch_status(x, y)
                        stone_status = (stone_impediment.status, random_index)
                    else:
                        stone_impediment.switch_status(0, 0)
                        stone_status = (0, len(route) - 1)

        screen.blit(background, (0, 0))

        # update thay doi
        map.draw(screen)
        cars.update(route)
        # cars2.update(route_2)
        # cars3.update(route_3)
        cars.draw(screen)
        # cars2.draw(screen)
        # cars3.draw(screen)

        #render again

        # update and render traffic lamps
        traffic_lamps_status = []
        traffic_lamps.update()
        traffic_lamps.draw(screen)
        lamp_status1 = traffic_lamp1.render(screen)
        lamp_status2 = traffic_lamp2.render(screen)
        traffic_lamps_status.append(lamp_status1)
        traffic_lamps_status.append(lamp_status2)

        # update stone
        stones.update()
        stones.draw(screen)

        pygame.display.flip()
        # Toc do Frame rate
        clock.tick(60)

def get_toa_do_graph():
    TOA_DO_GRAPH = []
    with xlrd.open_workbook('../media/toa_do_processed.xlsx') as book:
            sheet_1 = book.sheet_by_index(1)

            node = [x for x in sheet_1.col_values(0)]
            neighbor = [y for y in sheet_1.col_values(1)]
            distance = [z for z in sheet_1.col_values(2)]

            for i in range(1, len(node)):
                TOA_DO_GRAPH.append((int(node[i]), int(neighbor[i]), int(distance[i])))
    return TOA_DO_GRAPH

def get_toa_do_real():
    TOA_DO_REAL = []
    with xlrd.open_workbook('../media/toa_do_processed.xlsx') as book:
            sheet_0 = book.sheet_by_index(0)
            node_name = [x for x in sheet_0.col_values(0)]
            x_node = [y for y in sheet_0.col_values(1)]
            y_node = [z for z in sheet_0.col_values(2)]
            for i in range(1, len(node_name)):
                TOA_DO_REAL.append((int(node_name[i]), int(x_node[i]), int(y_node[i])))
    return TOA_DO_REAL

def get_toa_do_traffic():
    TOA_DO_REAL = []
    with xlrd.open_workbook('../media/toa_do_processed.xlsx') as book:
            sheet_0 = book.sheet_by_index(0)
            node_name = [x for x in sheet_0.col_values(0)]
            x_node = [y for y in sheet_0.col_values(1)]
            y_node = [z for z in sheet_0.col_values(2)]
            for i in range(1, len(node_name)):
                TOA_DO_REAL.append((int(node_name[i]), int(x_node[i]), int(y_node[i])))
    return TOA_DO_REAL

if __name__ == "__main__":
    pygame.init()

    #Set Dai rong man hinh game
    screen = pygame.display.set_mode((920, 700))

    #Set title game
    pygame.display.set_caption("Drive")

    #Set chuot(mouse) hien trong game
    pygame.mouse.set_visible(True)

    #Set font cho game
    font = pygame.font.Font(None, 24)

    # new background surface
    background = pygame.Surface(screen.get_size())
    background = background.convert_alpha(background)
    background.fill((82, 86, 94))

    # main loop
    main()

    pygame.quit()
    sys.exit(0)

