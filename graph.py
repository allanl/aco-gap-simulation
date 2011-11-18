import pydot

def graph_pheromones(node_list, task, filename):
    graph = pydot.Dot(graph_type='digraph')
    graph_nodes = {node : pydot.Node(node.get_name()) for node in node_list}
    for node in node_list:
        if node.has_task(task):
            graph_nodes[node].set_label("%s: %s" % (node.get_name(), task.get_name()))
        for conn in node.get_connections():
            edge = pydot.Edge(graph_nodes[node], graph_nodes[conn.get_node()])
            label_text = ''
            if conn.get_pheromone(task) == conn.get_max_pheromone(task):
                label_text = 'M'
            edge.set_label("%d%s" % (conn.get_pheromone(task), label_text))
            graph.add_edge(edge)
        graph.add_node(graph_nodes[node])
    graph.write_png('%s.png' % filename)
    
