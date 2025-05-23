from dataclasses import dataclass
from dotenv import dotenv_values

@dataclass
class Config:
    bot_token: str
    colab_url: str

def load_config(path: str) -> Config:
    config = dotenv_values(path)
    return Config(
        bot_token=config["BOT_TOKEN"],
        colab_url=config["COLAB_URL"]
    )
