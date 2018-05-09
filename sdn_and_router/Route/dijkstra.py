def dijkstra(graph, src, dst):
    if graph is None:
        return None
    nodes = [i for i in range(len(graph))]
    visited = []
    if src in nodes:
        visited.append(src)
        nodes.remove(src)
    else:
        return None
    distance = {src: 0}
    for i in nodes:
        distance[i] = graph[src][i]
    path = {src: {src: []}}
    k = pre = src
    while nodes:
        mid_distance = float('inf')
        for v in visited:
            for d in nodes:
                g1 = graph[src][v]
                g2 = graph[v][d]
                if g1 == 0 and src != v:
                    g1 = float('inf')
                if g2 == 0:
                    g2 = float('inf')
                new_distance = g1 + g2
                if new_distance < mid_distance:
                    mid_distance = new_distance
                    graph[src][d] = new_distance
                    k = d
                    pre = v
        distance[k] = mid_distance
        path[src][k] = [i for i in path[src][pre]]
        path[src][k].append(k)

        visited.append(k)
        nodes.remove(k)
    path[src][dst].insert(0, src)
    return path[src][dst]

