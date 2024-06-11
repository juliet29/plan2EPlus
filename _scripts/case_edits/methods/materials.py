from icecream import ic
from geomeppy import IDF

from case_edits.epcase import EneryPlusCaseEditor
from case_edits.defaults import IDD_PATH, WEATHER_FILE

# TODO enum with cases that can pull from 

class Materials:
    def __init__(self, epcase:EneryPlusCaseEditor) -> None:
        self.epcase = epcase
       

    def study_reference_idf(self, idf_path):
        # TODO use os to simplify input .. 
        self.ref_idf = IDF(idf_path)
        self.extract_constructions()
        self.extract_materials()

    def extract_constructions(self):
        self.constructions = self.ref_idf.idfobjects["CONSTRUCTION"]
        self.constuction_names = [c.Name for c in self.constructions]
    
    def extract_materials(self):
        self.material_groups = [] 
        self.materials = []
        for k,v in self.ref_idf.idfobjects.items():
            if v:
                if "MATERIAL" in k:
                    self.material_groups.append(k)
                    self.materials.extend(self.ref_idf.idfobjects[k])

        

    def get_construction_materials(self, name):
        self.const = self.get_construction_by_name(name)
        self.const_materials = []
        const_mat_names = self.const.fieldvalues[2:]
        
        for m in const_mat_names:
            try: 
                mat = self.get_material_by_name(m, self.materials)
                self.const_materials.append(mat)
            except:
                raise Exception(f"{m} not found!")

        self.copy_to_idf()
                    

                       
    def copy_to_idf(self):
        assert self.is_unique_construction()
        self.epcase.idf.copyidfobject(self.const)

        for m in self.const_materials:
            try:
                assert self.is_unique_material(m)
                self.epcase.idf.copyidfobject(m)
            except:
                print(f"{m.Name} is already in idf")
                pass



    def is_unique_construction(self):
        const_objects = self.epcase.idf.idfobjects["CONSTRUCTION"]
        if self.const in const_objects:
            return False 
        else:
            return True
        
    def is_unique_material(self, m):
        for group_name in self.material_groups:
            mat_objects = self.epcase.idf.idfobjects[group_name]
   
            for obj in mat_objects:
                if m.Name == obj.Name:
                    ic("A MATCH", m.Name)
                    return False
        return True
    

    def get_construction_by_name(self, name):
        res =  [c for c in self.constructions if c.Name == name]

        assert len(res) != 0, f"No construction named {name} found in {self.constuction_names}"

        assert len(res) == 1, f"More than 1 object with {name}"
        return res[0]
    

    def get_material_by_name(self, name, reflist):
        res =  [c for c in reflist if c.Name == name]

        assert len(res) != 0, f"No material named {name} found"

        assert len(res) == 1, f"Found more than 1 object with {name}"
        return res[0]
    
    def get_case_constructions(self):
        self.case_constructions = self.epcase.idf.idfobjects["CONSTRUCTION"]
        return self.case_constructions

    
    



