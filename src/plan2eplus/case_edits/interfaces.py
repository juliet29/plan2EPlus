from dataclasses import dataclass

@dataclass
class EPClass:
    idd: str # this should be passing by user.. 
    initial_idf: str # this reasonably has local defaults
    weather_file: str
    analysis_period: str



# ideal run
