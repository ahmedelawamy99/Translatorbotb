from app import *
import os


if os.name != "nt":
    import uvloop
    uvloop.install()

if __name__ == "__main__":
    Bot().runbot()
