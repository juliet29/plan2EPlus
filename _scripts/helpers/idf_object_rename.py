def zone_rename(name):
        entry_name = name.split()[1]
        display_name = f"Block {entry_name}"
        bunch_name = f"B_{entry_name}"
        return entry_name, display_name, bunch_name