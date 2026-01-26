from environs import Env

env = Env()
env.read_env(path='.env')

BOT_TOKEN = env.str("BOT_TOKEN")
DEVELOPER_ID = env.str("DEVELOPER_ID")
