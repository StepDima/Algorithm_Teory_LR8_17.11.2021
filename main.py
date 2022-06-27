import time
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from math import inf, ceil, log10, fabs
import xml.etree.ElementTree as ET
from typing import List, Any, Callable


class Graph:
    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.edges = edges


class Vertex:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y


class Edge:
    def __init__(self, start_vertex, end_vertex, weight, name):
        self.start = start_vertex
        self.end = end_vertex
        self.weight = weight
        self.name  = name


def radix_sort(arr: List[Any], crt: Callable[[Any], int]) -> List[Any]:
    res, shift = arr, 1
    max_key = crt(arr[0])
    for item in arr:
        max_key = max(crt(item), max_key)
    key_size = ceil(1 + log10(max_key))
    for loop in range(key_size):
        bucket = [[] for i in range(10)]
        for item in arr:
            bucket[(crt(item) // shift) % 10].append(item)
        arr = []
        for iterator in range(10):
            arr += bucket[iterator]
        shift *= 10
    for iterator in range(len(res)):
        res[iterator] = arr[iterator]
    return res


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.graph = None
        self.chosed_e = {}
        self.chosed_v = {}
        self.vertex = {}
        self.edge = {}
        self.id = None
        self.geometry("960x750")
        self.resizable(width=False, height=False)
        self.canvas = tk.Canvas(self, height=700, width=960, bg='#DDDDDD')
        self.canvas.place(relx=0, rely=0, height=700, width=960)
        self.button_B = tk.Button(self, command=lambda: self.start_action('B'), text="Borůvka\'s algorithm")
        self.button_B.place(x=0, y=700, width=320, height=50)
        self.button_K = tk.Button(self, command=lambda: self.start_action('K'), text="Kruskal\'s algorithm")
        self.button_K.place(x=640, y=700, width=320, height=50)
        self.button_P = tk.Button(self, command=lambda: self.start_action('P'), text="Prim\'s algorithm")
        self.button_P.place(x=320, y=700, width=320, height=50)
        self.main_menu = tk.Menu()
        self.file_menu = tk.Menu(tearoff=0)
        self.file_menu.add_command(label="Save", command=self.save_graph)
        self.file_menu.add_command(label="Open", command=self.open_graph)
        self.main_menu.add_cascade(label="File", menu=self.file_menu)
        self.config(menu=self.main_menu)

    def start_action(self, caller):
        if self.graph is None:
            messagebox.showerror("Error", "Graph is not chosed")
        else:
            self.button_B.config(state=tk.DISABLED)
            self.button_K.config(state=tk.DISABLED)
            self.button_P.config(state=tk.DISABLED)
            if 'P' == caller:
                thread = threading.Thread(target=self.prim)
            if 'K' == caller:
                thread = threading.Thread(target=self.kruskal)
            if 'B' == caller:
                thread = threading.Thread(target=self.boruvka)
            print(threading.main_thread().name)
            print(thread.name)
            thread.start()
            self.check_thread(thread)

    def check_thread(self, thread):
        if thread.is_alive():
            self.after(100, lambda: self.check_thread(thread))
        else:
            self.button_B.config(state=tk.NORMAL)
            self.button_K.config(state=tk.NORMAL)
            self.button_P.config(state=tk.NORMAL)

    def prim(self):
        self.chosed_e = set()
        self.chosed_v = set()
        used = {self.id}
        self.draw()
        while len(self.chosed_e) != len(self.graph.vertices) - 1:
            min_edge = None
            min_weight = inf
            for edge in self.graph.edges:
                if (((edge.start in used) and (edge.end not in used)) or (
                        (edge.start not in used) and (edge.end in used))) and \
                        (edge.weight < min_weight):
                    min_edge = edge
                    min_weight = edge.weight
            print(f'{min_edge.start}{min_edge.end}\n{min_edge.weight}')
            self.chosed_e.add(min_edge)
            self.canvas.itemconfig(self.edge[min_edge.name], fill = '#00DD00', width=4)
            used.add(min_edge.start)
            used.add(min_edge.end)
            self.canvas.itemconfig(self.vertex[min_edge.start], fill ='#00DD00')
            self.canvas.itemconfig(self.vertex[min_edge.end], fill='#00DD00')
            time.sleep(0.8)



    def kruskal(self):
        v_sets = {item: {item} for item in self.graph.vertices}
        self.chosed_e = set()
        self.chosed_v = set()
        edges = radix_sort([item for item in self.graph.edges], lambda item: item.weight)
        self.draw()
        for edge in edges:
            if edge.start not in v_sets[edge.end]:
                for vertex in v_sets[edge.end]:
                    v_sets[edge.start].add(vertex)
                    v_sets[vertex] = v_sets[edge.start]
                self.chosed_e.add(edge)
                self.chosed_v.add(edge.start)
                self.chosed_v.add(edge.end)
                time.sleep(2.5)
                self.draw()


    def boruvka(self):
        self.chosed_v = set()
        self.chosed_e = set()
        self.draw()
        self.chosed_v = {item for item in self.graph.vertices}
        v_sets = {item: {item} for item in self.graph.vertices}
        while len(self.chosed_e) != len(self.graph.vertices)-1:
            used = []
            for key in v_sets:
                if v_sets[key] not in used:
                    min_edge = None
                    min_weight = inf
                    for edge in self.graph.edges:
                        if (((edge.start in v_sets[key]) and (edge.end not in v_sets[key])) or (
                                (edge.start not in v_sets[key]) and (edge.end in v_sets[key]))) and \
                                (edge.weight < min_weight):
                            min_edge = edge
                            min_weight = edge.weight
                    for vertex in v_sets[min_edge.end]:
                        self.chosed_e.add(min_edge)
                        v_sets[min_edge.start].add(vertex)
                        v_sets[vertex] = v_sets[min_edge.start]
                    self.chosed_e.add(min_edge)
                    used.append(v_sets[min_edge.start])
            time.sleep(2)
            self.draw()



    def draw(self):
        self.canvas.delete('all')
        radius = 15
        max_x, max_y = 0, 0
        min_x, min_y = inf, inf
        for key in self.graph.vertices:
            ver = self.graph.vertices[key]
            max_x = max(max_x, ver.x)
            max_y = max(max_y, ver.y)
            min_x = min(min_x, ver.x)
            min_y = min(min_y, ver.y)
        for edge in self.graph.edges:
            color = '#999999'
            w = 1
            if edge in self.chosed_e:
                w = 4
                color = '#00DD00'
            start = self.graph.vertices[edge.start]
            end = self.graph.vertices[edge.end]
            x_1 = (start.x - min_x) * (self.canvas.winfo_width() - 2 * radius) / (max_x - min_x) + radius
            y_1 = (start.y - min_y) * (self.canvas.winfo_height() - 2 * radius) / (max_y - min_y) + radius
            x_2 = (end.x - min_x) * (self.canvas.winfo_width() - 2 * radius) / (max_x - min_x) + radius
            y_2 = (end.y - min_y) * (self.canvas.winfo_height() - 2 * radius) / (max_y - min_y) + radius
            self.edge[edge.name] = self.canvas.create_line(x_1, y_1, x_2, y_2, fill=color, width=w)
            self.canvas.create_text(fabs(x_1 + x_2) / 2, fabs(y_1 + y_2) / 2, text=f"{edge.weight}", fill="black")
        for key in self.graph.vertices:
            color = 'red'
            w = 2
            if key in self.chosed_v:
                w = 2
                color = '#00DD00'
            ver = self.graph.vertices[key]
            x_mod = (ver.x - min_x) * (self.canvas.winfo_width() - 2 * radius) / (max_x - min_x) + radius
            y_mod = (ver.y - min_y) * (self.canvas.winfo_height() - 2 * radius) / (max_y - min_y) + radius
            self.vertex[key] = self.canvas.create_oval(x_mod - radius + w + 1, y_mod - radius + w + 1, x_mod + radius - w - 1,
                                    y_mod + radius - w - 1, fill=color, outline='black', width=w)
            self.canvas.create_text(x_mod, y_mod, text=key, fill="black")

    def save_graph(self):
        filename = filedialog.asksaveasfilename(initialfile='*.xml', filetypes=(("xml files (*.xml)", "*.xml"), ("text files (*.txt)", "*.txt"), ("All files", "*.*")))
        print(filename)
        lines = []
        points = []
        i = 0
        for vertex in self.graph.vertices.values():
            points.append(f'<point id="{vertex.name}" x="{vertex.x}" y="{vertex.y}" />')
        for edge in self.chosed_e:
            lines.append(f' <line id="{i}" from="{edge.start}" to="{edge.end}" weight="{edge.weight}" />')
        str_points = '\n\t\t\t\t'.join(points)
        str_lines = '\n\t\t\t\t'.join(lines)
        fout = open(f'{filename}', 'w')
        result = f'''<?xml version="1.0" encoding="windows-1251"?>
        <graph_data>
            <graph id="1">
                <title></title>
                <points>
                    {str_points}
                </points>
                <lines>
                    {str_lines}
                </lines>
            </graph>
        </graph_data>
        '''
        fout.write(result)

    def open_graph(self):
        self.chosed_e = {}
        self.chosed_v = {}
        self.id = None
        filename = filedialog.askopenfilename(
            filetypes=(("xml files (*.xml)", "*.xml"),), )
        if filename != '':
            tree = ET.parse(f'{filename}')
            root = tree.getroot()
            self.graph = Graph({}, set())
            for vert in root[0][1]:
                self.id = vert.attrib['id']
                self.graph.vertices[vert.attrib['id']] = Vertex(vert.attrib['id'], int(vert.attrib['x']),
                                                                int(vert.attrib['y']))
            for edge in root[0][2]:
                self.graph.edges.add(Edge(edge.attrib['from'], edge.attrib['to'], int(edge.attrib['weight']), edge.attrib['id']))
            self.draw()


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
