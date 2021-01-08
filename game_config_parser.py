import configparser

config = configparser.ConfigParser()
config.read("config.ini")

gameplay_config = config["Gameplay"]
color_scheme_config = config["Color Scheme"]


def parse_color(start):
    r = int(color_scheme_config[f"{start}R"])
    g = int(color_scheme_config[f"{start}G"])
    b = int(color_scheme_config[f"{start}B"])

    return r, g, b


# Colors for game
background_color = parse_color("BackgroundColor")
border_color = parse_color("BorderAndFontColor")
snake_color = parse_color("SnakeColor")
food_color = parse_color("FoodColor")

# FPS for game (Larger FPS makes the game go faster)
fps = gameplay_config["FPS"]
