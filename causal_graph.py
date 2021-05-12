from graphviz import Digraph
import os
import shutil
import json


class CausalGraph():
    def __init__(self):
        self.APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    def show(self, data):
        #static i = 0;
        dot = Digraph(format="png")
        image_filename = "output.gv";
        image_file = os.path.join(self.APP_ROOT, image_filename)
        for parent, children in data.items():
            dot.node(parent, label=parent)
            for child_pair in children:
                child, coef = child_pair
                dot.node(child, label=child)
                if int(coef) != -1:
                    dot.edge(child, parent, style="dashed")
                else:
                    dot.edge(child, parent)

        #print(dot.source)
        dot.render(image_file, view=True)
        # if self.x >=1:
        #     old_image_file = "./static/images/output" + str(self.x-1) + ".gv"
        #     os.remove(old_image_file)
        #     os.remove(old_image_file+".png")
        #dot.save(image_file)
        return image_filename

    def reset(self):
        path = os.path.join(self.APP_ROOT,"static/images/")
        for f in os.listdir(path):
            os.remove(os.path.join(path, f))
        self.x = 0;
