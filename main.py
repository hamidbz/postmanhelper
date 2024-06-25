import tkinter as tk
from tkinter import simpledialog, messagebox
import random
import networkx as nx
from genetic import GA


class GraphApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Traffic Simulator')
        self.geometry('800x600')
        
        label = tk.Label(self, text="برای رسم گره، روی صفحه کلیک کنید. برای وصل کردن گره‌ها، روی یک گره راست کلیک کنید و سپس گره دیگری را انتخاب کنید.", wraplength=400)
        label.pack(side=tk.TOP, pady=10)

        self.graph = nx.Graph()
        self.positions = {}
        self.node_names = {}
        
        self.canvas = tk.Canvas(self, width=800, height=600, bg='White')
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        
        self.canvas.bind('<Button-1>', self.create_node)
        self.canvas.bind('<Button-3>', self.create_edge)
        
        self.calculate_button = tk.Button(self, text='Calculate Shortest Path', command=self.calculate_shortest_path)
        self.clear_button = tk.Button(self, text='Clear', command=self.clear_graph)
        
    def clear_graph(self):
        self.graph.clear()
        self.canvas.delete('all')
        self.positions.clear()
        self.node_names.clear()

    def find_path_genetic(self, start, end):
        n = nx.number_of_nodes(self.graph)
        l = list(nx.nodes(self.graph))
        total = self.graph.size(weight='weight')
    
        def fit(choro):
        
            def get_w(n1, n2):
                if self.graph.has_edge(n1, n2):
                    return self.graph[n1][n2]['weight']
                else:
                    return total
        
            cost = 0
            for i in range(len(choro)-1):
                cost += get_w(choro[i], choro[i+1])
    
            return ((n * total) - cost)
        

        ga = GA(population_size=100, number_of_nodes=n, mutation_rate=0.6, crossover_rate=0.6,
            iterations=100,graph_nodes=l, start=start, end=end, fitness_function=fit)
        path = ga.main()
        return list(path)

    def create_node(self, event):
        node_name = simpledialog.askstring('Node Name', 'Enter node name:')
        if node_name in self.node_names:
            messagebox.showerror('Error', 'Duplicated node name!')
            return
        if node_name:
            self.positions[node_name] = (event.x, event.y)
            self.node_names[node_name] = node_name
            self.graph.add_node(node_name)
            self.canvas.create_oval(event.x - 10, event.y - 10, event.x + 10, event.y + 10, fill='blue')
            self.canvas.create_text(event.x, event.y, text=node_name, font=('Arial', 12))
            self.calculate_button.pack(side=tk.BOTTOM)
            self.clear_button.pack(side=tk.BOTTOM)

    
    def create_edge(self, event):
        x, y = event.x, event.y
        closest_node = min(self.positions, key=lambda node: (self.positions[node][0] - x)**2 + (self.positions[node][1] - y)**2)
        second_node = simpledialog.askstring('Input', 'Enter the node to connect with:')
        edge_weight = simpledialog.askfloat('Input', 'Enter the edge weight:')
        if second_node in self.graph.nodes and edge_weight is not None:
            self.graph.add_edge(closest_node, second_node, weight=edge_weight)
            line = self.canvas.create_line(self.positions[closest_node], self.positions[second_node], fill='black')
            self.apply_random_traffic(closest_node, second_node, line)
    
    def apply_random_traffic(self, node1, node2, line):
        traffic = random.random() < 0.5
        amount = random.choice(['heavy','light']) 
        weight = self.graph[node1][node2]['weight']
        if traffic:
            txt = f'{weight:.2f} ,{amount}'
            if amount == 'heavy':
                weight = weight + weight/2
            else:
                weight = weight + weight/8
            self.graph[node1][node2]['weight'] += weight
        else:
            txt = f'{weight:.2f}'
        color = 'black' if traffic else 'green'
        self.canvas.itemconfig(line, fill=color)
        self.canvas.create_text((self.positions[node1][0] + self.positions[node2][0]) / 2,
                                (self.positions[node1][1] + self.positions[node2][1]) / 2,
                                text=txt, font=('Arial', 10), width=2)


    def calculate_shortest_path(self):
        start_node_name = simpledialog.askstring('Input', 'Enter start node name:')
        end_node_name = simpledialog.askstring('Input', 'Enter end node name:')
        if start_node_name in self.node_names.values() and end_node_name in self.node_names.values():
            start_node = [node_id for node_id, name in self.node_names.items() if name == start_node_name][0]
            end_node = [node_id for node_id, name in self.node_names.items() if name == end_node_name][0]
            try:
                path, cost = self.find_path_genetic(start=start_node, end=end_node)
                if cost == 0:
                    path = nx.shortest_path(self.graph, source=start_node, target=end_node, weight='weight')
                for i in range(len(path) - 1):
                    self.canvas.create_line(self.positions[path[i]], self.positions[path[i+1]], fill='red', width=4)
                messagebox.showinfo('Shortest Path', f'The shortest path is: {[self.node_names[node] for node in path]}')
            except nx.NetworkXNoPath:
                messagebox.showerror('Error', 'No path exists between the selected nodes due to traffic.')
        else:
            messagebox.showerror('Error', 'One or both of the entered node names do not exist in the graph.')



if __name__ == '__main__':
    app = GraphApplication()
    app.mainloop()