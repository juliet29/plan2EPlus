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
        # TODO this is too specific to this idf.. 
        self.materials = self.ref_idf.idfobjects["MATERIAL"]
        self.materials_air = self.ref_idf.idfobjects["MATERIAL:AIRGAP"]
        self.materoals_no_mass = self.ref_idf.idfobjects["MATERIAL:NOMASS"]
    

    def get_construction_materials(self, name):
        self.const = self.get_construction_by_name(name)
        self.const_materials = []
        const_mat_names = self.const.fieldvalues[2:]
        
        for m in const_mat_names:
            try: 
                mat = self.get_material_by_name(m, self.materials)
                self.const_materials.append(mat)
            except:
                try:
                    mat = self.get_material_by_name(m, self.materials_air)
                    self.const_materials.append(mat)
                except:
                    try:
                        mat = self.get_material_by_name(m, self.materials_no_mass)
                        self.const_materials.append(mat)
                    except:
                        raise Exception(f"{m} not found!")
        self.copy_to_idf()
                    

                    
        
    def copy_to_idf(self):
        self.epcase.idf.copyidfobject(self.const)
        for m in self.const_materials:
            self.epcase.idf.copyidfobject(m)
        # TODO check that not already in idf! 

        # self.const = ""
        # self.const_materials = []


    def is_unique_construction(self):
        if self.const not in self.epcase.idf.idfobjects["CONSTRUCTION"]:
            return True 
        
    def is_unique_material(self):
        pass


        

    def get_construction_by_name(self, name):
        res =  [c for c in self.constructions if c.Name == name]

        assert len(res) != 0, f"No construction named {name} found in {self.constuction_names}"

        assert len(res) == 1, f"More than 1 object with {name}"
        return res[0]
    

    def get_material_by_name(self, name, reflist):
        res =  [c for c in reflist if c.Name == name]

        assert len(res) != 0, f"No material named {name} found"

        assert len(res) == 1, f"Found ore than 1 object with {name}"
        return res[0]
    
    



