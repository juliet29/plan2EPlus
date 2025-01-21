from eppy.bunch_subclass import EpBunch
from helpers.helpers import chain_flatten


def get_layer_fields():
    return ["Outside_Layer"] + [f"Layer_{i}" for i in range(2, 11)]


def get_construction_materials(cons: EpBunch):
    layer_fields = get_layer_fields()
    return [cons.get_referenced_object(field) for field in layer_fields if cons[field]]


def get_construction_set_materials(cons_set: list[EpBunch]) -> list[EpBunch]:
    all_mats = chain_flatten([get_construction_materials(i) for i in cons_set])

    unique_mats = []
    unique_names = []
    for i in all_mats:
        assert i
        if i.Name not in unique_names:
            unique_mats.append(i)
            unique_names.append(i.Name)
    return unique_mats
