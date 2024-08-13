def zone_rename(name):
        entry_name = name.split()[1]
        display_name = f"Block {entry_name}"
        bunch_name = f"B_{entry_name}"
        return entry_name, display_name, bunch_name

def wall_rename(name, zone, direction, number):
        display_name = (
            f"Block {zone.entry_name} - {direction.title()} - W{number}"
        )
        bunch_name = (
            f"B_{zone.entry_name}_{direction.title()}_W{number}"
        )
        short_name = f"B{zone.entry_name}-W{number}"