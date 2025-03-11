class Category:
    def __init__(self, name, display_color="#FFFFFF", icon=None, id=None):
        self.name = name
        self.display_color = display_color
        self.icon = icon

    def to_dict(self):
        return {
            "name": self.name,
            "display_color": self.display_color,
            "icon": self.icon
        }
    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            display_color=data.get("display_color", "#FFFFFF"),
            icon=data.get("icon"),
            id=data["id"]
        )