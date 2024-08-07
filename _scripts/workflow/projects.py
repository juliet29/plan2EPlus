import os
from copy import deepcopy
import pickle
from pprint import pprint, pformat
from deepdiff import DeepDiff
from jinja2 import Template
from html2image import Html2Image


from case_edits.ezcase import EzCase, EzCaseInput

INPUT_TEMPLATE_PATH = "/Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/geomeppy/_scripts/workflow/project_fig.html.j2"

class ProjectManager:
    def __init__(self, name, base_case_input: EzCaseInput, RUN_CASE=False) -> None:
        self.project_name = name
        self.base_case_input  = base_case_input
        self.plotly_jinja_data = {"project_name": self.project_name, "cases": [] }
        self.RUN_CASE = RUN_CASE
    

        self.create_project_directory()
        self.create_base_case()

    def create_project_directory(self):
        self.path = os.path.join("cases/projects", self.project_name)
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def create_base_case(self):
        # base_case_name = self.base_case_input.case_name
        # overwriting so that labeled base case
        self.base_case_input.case_name =  "a00-base_case"
        self.base_case_input.project_name = self.project_name

        self.base_ezcase = EzCase(self.base_case_input, self.RUN_CASE)
        # TODO check and automatically run the case? 
        self.save_input_pkl(self.base_case_input, self.base_ezcase.case.path)
        self.save_input_txt()
        self.plotly_jinja_data["cases"].append({"name": self.base_case_input.case_name, "fig": self.get_case_fig(self.base_ezcase)})



    def generate_new_case(self, mod_fx, name="",  prefix="", letter=""):
        # todo type ~ fx signature? 
        self.new_input = deepcopy(self.base_case_input)
        self.new_input:EzCaseInput = mod_fx(self.new_input)

        assert prefix or name, "Need a prefix or a name for the case"

        # generate new name 
        if not prefix:
            prefix = self.generate_prefix(letter)

        case_name = f"{prefix}-{name}"
        self.new_input.case_name = case_name

        self.new_ezcase = EzCase(self.new_input, self.RUN_CASE)
        self.save_input_pkl(self.new_input, self.new_ezcase.case.path)
        self.save_diff_input_txt()
        self.plotly_jinja_data["cases"].append({"name": self.new_input.case_name, "fig": self.get_case_fig(self.new_ezcase)})
 


    def generate_prefix(self, letter="a"): 
        # calc number of folders..
        n_cases = len(next(os.walk(self.path))[1])

        curr_n = str(n_cases+1).zfill(2)
        return f"{letter}_{curr_n}"
    


    
    def save_input_pkl(self, input, fpath):
        path = os.path.join(fpath, "input.pkl")

        with open(path, "wb") as file:
            pickle.dump(input, file, protocol=pickle.HIGHEST_PROTOCOL)

    


    def save_input_txt(self):
        path = os.path.join(self.base_ezcase.case.path, "input.txt")
        with open(path, "w+") as file:
            file.write(self.base_ezcase.sinput_vals)


    def save_diff_input_txt(self):
        differences = DeepDiff(self.base_case_input, self.new_input, exclude_paths=["class_vals", "case_name"])
        sdiff = pformat(differences, sort_dicts=False)

        path = os.path.join(self.new_ezcase.case.path, "diff.txt")
        with open(path, "w+") as file:
            file.write(sdiff)
        pass


    def save_project_fig(self):
        output_html_path = os.path.join(self.path, "project_figs.html")
        output_jpg_path = os.path.join(self.path, "project_figs.jpg")
        with open(output_html_path, "w+", encoding="utf-8") as output_file:
            with open(INPUT_TEMPLATE_PATH) as template_file:
                j2_template = Template(template_file.read())
                output_file.write(j2_template.render(self.plotly_jinja_data))

        print(output_html_path)
        # hti = Html2Image()
        # hti.screenshot(html_file=output_html_path, save_as="project_figs.jpg")


    
    def get_case_fig(self, case):
        return  case.base_plot.fig.to_html(full_html=False)


    