import pygame
import sys
import graphic.maps as maps
from graphic import car
from algorithm.dijkstra_algorithm import dijkstra
from algorithm.dijkstra_algorithm import GraphUndirectedWeighted

def main():
    clock = pygame.time.Clock()
    #map
    map = pygame.sprite.Group()
    map.add(maps.Map(0, 0, 1))

    #Find path
    g = GraphUndirectedWeighted(9)
    g.add_edge(0, 1, 4)
    g.add_edge(1, 7, 6)
    g.add_edge(1, 2, 1)
    g.add_edge(2, 3, 3)
    g.add_edge(3, 7, 1)
    g.add_edge(3, 4, 2)
    g.add_edge(3, 5, 1)
    g.add_edge(4, 5, 1)
    g.add_edge(5, 6, 1)
    g.add_edge(6, 7, 2)
    g.add_edge(6, 8, 2)
    g.add_edge(7, 8, 2)
    shortest_path, distance = dijkstra(g, 0, 7)
    print(shortest_path, distance)

    # start_x = maps.MAP_NAVS[0][0]
    # start_y = maps.MAP_NAVS[0][1]
    start_x = 150
    start_y = 3
    print(start_x, start_y)
    maps.FINISH_INDEX = len(maps.MAP_NAVS) - 2

    #test route.
    route_1 = [[155.0, 3.0],[155.0, 124.0], [214.0, 124.0], [214.0, 283.0],
             [150.0, 283.0], [150.0, 478.0], [41.0, 478.0], [41.0, 700.0]]
    route_2 = [[0.0, 186.0], [74.0, 186.0], [74.0, 0.0]]
    route_3 = [[494.0, 0.0], [494.0, 185.0], [595.0, 185.0], [595.0, 383.0], [549.0, 383.0], [549.0, 597.0],
               [740.0, 597.0], [740.0, 480.0], [870.0, 480.0], [870.0, 700.0]]
    #car
    # start_angle = calculate_angle(maps.MAP_NAVS[0][0], maps.MAP_NAVS[0][1], maps.MAP_NAVS[1][0], maps.MAP_NAVS[1][1])
    cars = pygame.sprite.Group()
    cars2 = pygame.sprite.Group()
    cars3 = pygame.sprite.Group()
    cars.add(car.Car(route_1[0][0], route_1[0][1], route_1[1][0], route_1[1][1]))
    cars2.add(car.Car(route_2[0][0], route_2[0][1], route_2[1][0], route_2[1][1]))
    cars3.add(car.Car(route_3[0][0], route_3[0][1], route_3[1][0], route_3[1][1]))

    running = True
    k = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

        screen.blit(background, (0, 0))

        # update thay doi
        map.draw(screen)


        cars.update(route_1)
        cars2.update(route_2)
        cars3.update(route_3)


        cars.draw(screen)
        cars2.draw(screen)
        cars3.draw(screen)

        #render again
        pygame.display.flip()
        # Toc do Frame rate
        clock.tick(1000000)

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