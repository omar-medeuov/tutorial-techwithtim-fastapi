from dotenv import load_dotenv
from imagekitio import ImageKit
import os

load_dotenv()

# The class no longer has some parameters.
imagekit = ImageKit(
    private_key=os.getenv("IMAGEKIT_PRIVATE_KEY"),
    # public_key=os.getenv("IMAGEKIT_PUBLIC_KEY"),

)
URL_ENDPOINT=os.getenv("IMAGEKIT_URL"),