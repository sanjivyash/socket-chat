import os
from dotenv import load_dotenv

PATH = os.path.join(os.getcwd(), '..', 'config', '.env')
load_dotenv(PATH)