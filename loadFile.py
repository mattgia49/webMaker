from project import Project
from term import Term
import json


class LoadFile:
    def __init__(self, file):
        with open(file, "r") as inFile:
            self.proj = json.load(inFile)
            self.new_proj = Project(self.proj["name"])
            self.new_proj.set_term_id(self.proj['term id'])
            for t in self.proj["terms"]:
                curr_term = Term(t['id'], t['x'], t['y'])
                curr_term.set_names(t['names'])
                curr_term.set_lines(t['desc'])
                curr_term.change_color(t['color'])
                self.new_proj.add_term(curr_term)

            for c in self.proj["connections"]:
                self.new_proj.create_connection(c[0], c[1])

    def get_loaded(self):
        return self.new_proj
