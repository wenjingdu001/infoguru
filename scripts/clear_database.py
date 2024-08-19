import os
import shutil

CHROMA_PATH = "data/chroma"
def clear_database():
    if os.path.exists(CHROMA_PATH):
        print("clearing...")
        shutil.rmtree(CHROMA_PATH)


if __name__ == "__main__":
    clear_database()