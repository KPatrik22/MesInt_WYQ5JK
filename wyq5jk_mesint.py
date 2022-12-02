import random
import time
import matplotlib.pyplot as plt

def distance(point1, point2):
    distance = 0
    for x1, x2 in zip(point1, point2):
        difference = x2 - x1
        absolute_difference = abs(difference)
        distance += absolute_difference
    return distance
    
def transform(loc):
    _dict = {}
    for i in range(len(loc)):
        for j in range(len(loc)):
            _dict[(i, j)] = distance(loc[i], loc[j])
    return _dict
    
def object_function(dict, s):
    dist = 0
    prev = s[0]
    for i in s:
        dist += dict[(prev, i)]
        prev = i
    dist += dict[(s[-1], s[0])]
    return dist
    
def tabu_tsp(s, object_f, iterations, neighbors):
    
    tabulist = []
    tlcounter = 0
    s_best = list(s)
    f_best = object_f(s)
    s_base = list(s_best)
    f_base = f_best
    tabulist.append(list(s))
    while(tlcounter < 15):
        for _ in range(iterations):
            s_best_neighbor = list(s_base)
            f_best_neighbor = f_base
            for _ in range(neighbors):
                s_neighbor = list(s_base)
                a = random.randint(1, len(s) - 2)
                b = random.randint(1, len(s) - 2)
                s_neighbor[a], s_neighbor[b] = s_neighbor[b], s_neighbor[a]
                if list(s_neighbor) in tabulist:
                    tlcounter += 1
                tabulist.append(list(s_neighbor))
                f_neighbor = object_f(s_neighbor)
                if f_neighbor < f_best_neighbor:
                    f_best_neighbor = f_neighbor
                    s_best_neighbor = s_neighbor
            s_base = s_best_neighbor
            f_base = f_best_neighbor
            if f_base < f_best:
                f_best = f_base
                s_best = s_base

    return s_best
    
def tabu_vrp(s, object_f, iterations, neighbors, cities, vehicles):
    
    tabulist = []
    tlcounter = 0
    routehelp = []
    routes = []
    start = s.copy()
    start.remove(0)

    for i in range(vehicles): 
        routes.append([0])
        while((len(start) > 0) and (len(routes[i]) < ((cities/vehicles)+1))): 
            a = random.randint(0, len(start) - 1)
            if a not in routehelp:
                routes[i].append(start[a])
                routehelp.append(start[a])
                start.remove(start[a])
        routes[i].append(0)

    s_base = list(routes)
    f_base = 0
    for k in range(vehicles):
            f_base += object_f(routes[k])
    s_best = s_base
    f_best = f_base
    print("\nDefault full distance: ", f_base)
    temp_routes = routes.copy()

    for outer in range(iterations):
        
        f_route_best = f_base
        s_neighbor_best = s_base

        for x in range(vehicles):

            tlcounter = 0
            r = random.randint(0, vehicles-1)
            while(x==r):
                r = random.randint(0, vehicles-1)
            
            for inner in range(neighbors):
                s_neighbor = list(s_best[x])
                a = random.randint(1, len(routes[x]) - 2)
                b = random.randint(1, len(routes[x]) - 2)
                while(a==b):
                    b = random.randint(1, len(routes[x]) - 2)
                s_neighbor[a], s_neighbor[b] = s_neighbor[b], s_neighbor[a]
                temp_routes = list(s_base)
                temp_routes[x] = list(s_neighbor)
                f_neighbor = 0
                for p in range(vehicles):
                    f_neighbor += object_f(temp_routes[p])

                if s_neighbor in tabulist:
                    tlcounter += 1
                    if tlcounter > 15:
                        break
                    continue

                if f_neighbor < f_route_best:
                    f_route_best = f_neighbor
                    s_neighbor_best[x] = list(s_neighbor)

                else:
                    tabulist.append(s_neighbor)

            f_base = f_route_best
            s_base = list(s_neighbor_best)
            if f_base < f_best:
                s_best = s_base
                f_best = f_base
            f_route_best = f_best
            s_neighbor_best = s_best

            for inner in range(neighbors):
                temp_routes = list(s_base)
                a = random.randint(1, len(s_best[x]) - 2)
                b = random.randint(1, len(s_best[r]) - 2)
                s_first = list(s_best[x])
                s_second = list(s_best[r])
                s_first[a], s_second[b] = s_second[b], s_first[a]
                temp_routes[x] = s_first
                temp_routes[r] = s_second
                f_switched_sum = 0
                for p in range(vehicles):
                        f_switched_sum += object_f(temp_routes[p])

                if s_first in tabulist or s_second in tabulist:
                        tlcounter += 1
                        if tlcounter > 15:
                            break
                        continue

                if f_switched_sum < f_route_best:
                    s_neighbor_best = temp_routes
                    f_route_best = f_switched_sum

                else:
                    tabulist.append(s_first)
                    tabulist.append(s_second)

            f_base = f_route_best
            s_base = list(s_neighbor_best)
            if f_base < f_best:
                s_best = s_base
                f_best = f_base

    return s_best
    
def output(cities, vehicles, loc, s_improved, distances, fulldistance):

    f = open("output.txt", "a")
    f.write("Number of cities: ")
    f.write(str(cities))
    f.write("\nNumber of vehicles: ")
    f.write(str(vehicles))
    f.write("\nCoordinates: ")
    f.write(str(loc))
    f.write("\n")
    for i in range(vehicles):
        f.write("\nRoute of vehicle No. ")
        f.write(str(i+1))
        f.write(": ")
        f.write(str(s_improved[i]))
        f.write("\nDistance of vehicle No.")
        f.write(str(i+1))
        f.write(": ")
        f.write(str(distances[i]))

    f.write("\n\nFull Distnace: ")
    f.write(str(fulldistance))
    f.write("\n-----\n")
    f.close()

def plot(loc, s_improved):
    plt.plot(loc[0][0], loc[0][1], 'hotpink')
    plt.annotate('Depot', (loc[0][0], loc[0][1]))
    for i in range(1, len(loc)):
        plt.plot(loc[i][0], loc[i][1], 'black')
        plt.annotate(i, (loc[i][0], loc[i][1]))
    colors = ['r', 'g', 'b', 'y', 'c', 'm', 'k']
    for i in range(len(s_improved)):
        for k in range(len(s_improved[i])):
            if k == len(s_improved[i]) - 1:
                plt.plot([loc[s_improved[i][k]][0], loc[s_improved[i][0]][0]],
                          [loc[s_improved[i][k]][1], loc[s_improved[i][0]][1]], colors[i % 7])
            else:
                plt.plot([loc[s_improved[i][k]][0], loc[s_improved[i][k + 1]][0]],
                          [loc[s_improved[i][k]][1], loc[s_improved[i][k + 1]][1]], colors[i % 7])

    plt.show()

def main():
    
    start_time = time.time()
    cities_list = [10, 20, 50, 100, 200, 500]
    few_vehicles_list = [1, 2, 4, 5]
    many_vehicles_list = [10, 20]
    c = random.randint(0, len(cities_list)-1)
    cities = cities_list[c]
    if cities > 50:
        v = random.randint(0, len(many_vehicles_list)-1)
        vehicles = many_vehicles_list[v]
    if cities == 50:
        vehicles = 10
    if cities < 50 and cities != 10:
        v = random.randint(0, len(few_vehicles_list)-1)
        vehicles = few_vehicles_list[v]
    few_vehicles_list.remove(4)
    if cities == 10:
        v = random.randint(0, len(few_vehicles_list)-1)
        vehicles = few_vehicles_list[v]
    s = []
    for i in range(cities+1):
        s.append(i)      

    loc = [0] * (cities + 1)
    for l in range(cities+1):
        point1 = random.randint(0, 1000)
        point2 = random.randint(0, 1000)
        loc[l] = (point1, point2)

    print("depo: ", loc[0])
    print("depo: ", loc[0][0], loc[0][1])
    
    print("\nNumber of cities: ", cities)
    print("Number of vehicles: ", vehicles)
    
    _dict = transform(loc)
    object_f = lambda sched: object_function(_dict, sched)

    iterations = 200
    neighbors = 100
    fulldistance = 0
    distances = []

    if vehicles == 1: 
        s_improved = tabu_tsp(s, object_f, iterations, neighbors)
        print(s_improved)
        print("Distance: ", object_f(s_improved))
        print("\nExecution time: ",(time.time() - start_time)," seconds\n")
    
    if vehicles > 1: 
        s_improved = tabu_vrp(s, object_f, iterations, neighbors, cities, vehicles)
        for l in range(vehicles):
            distances.append(object_f(s_improved[l]))
            fulldistance += object_f(s_improved[l])
        for m in range(vehicles):
            print("\nRoute of vehicle No.",m+1,": ", s_improved[m])
            print("Distance of vehicle No.",m+1,": ", distances[m])
        print("\nFull Distance: ", fulldistance)
        output(cities, vehicles, loc, s_improved, distances, fulldistance)
        print("\nExecution time: ",(time.time() - start_time)," seconds\n")
        plot(loc, s_improved)   
      
if __name__ == '__main__':
    main()
    