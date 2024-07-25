import os
from copy import deepcopy
import pickle
from pprint import pprint, pformat
from deepdiff import DeepDiff

from case_edits.ezcase import EzCase, EzCaseInput

class ProjectManager:
    def __init__(self, name, base_case_input: EzCaseInput) -> None:
        self.project_name = name
        self.base_case_input  = base_case_input

    def create_project_directory(self):
        self.path = os.path.join("cases/projects", self.project_name)
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def create_base_case(self):
        # base_case_name = self.base_case_input.case_name
        # overwriting so that labeled base case
        self.base_case_input.case_name =  "a01-base_case"
        self.base_case_input.project_name = self.project_name

        self.base_ezcase = EzCase(self.base_case_input)
        # TODO check and automatically run the case? 
        self.save_input_pkl(self.base_case_input, self.base_ezcase.case.path)
        self.save_input_txt()



    def generate_new_case(self, mod_fx, name="", letter="a"):
        # todo type ~ fx signature? 
        self.new_input = deepcopy(self.base_case_input)
        self.new_input:EzCaseInput = mod_fx(self.new_input)

        # generate new name 
        prefix = self.generate_prefix(letter)
        case_name = f"{prefix}-{name}"
        self.new_input.case_name = case_name

        self.new_ezcase = EzCase(self.new_input)
        self.save_input_pkl(self.new_input, self.new_ezcase.case.path)
        self.save_diff_input_txt()
        # TODO check and automatically run the case? 


    def generate_prefix(self, letter="a"): 
        # calc number of folders..
        n_cases = len(next(os.walk("cases/projects"))[1])

        curr_n = str(n_cases+1).zfill(2)
        return f"{letter}{curr_n}"
    
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



    