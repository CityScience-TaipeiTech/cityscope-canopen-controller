#!/usr/bin/python3
import time
import tomli
from cs_gesture_detector import CsGestureDetector

def load_config(config_file):
    with open(config_file, "rb") as f:
            toml_dict = tomli.load(f)
            return toml_dict

def main():
    config = load_config("./tw-island.toml")
    gesture = CsGestureDetector(config["gesture"], config["proximity"])
    print("active node 15")
    for i in range(0, 100):
        gesture.update_prox(15, 10)
        gesture.update_prox(18, 100)
        time.sleep(0.05)
    print("active node 18")
    for i in range(0, 100):
        gesture.update_prox(15, 200)
        gesture.update_prox(18, 3)
        time.sleep(0.05)
    print("no node active")
    for i in range(0, 200):
        gesture.update_prox(15, 200)
        gesture.update_prox(18, 200)
        time.sleep(0.05)

if __name__ == "__main__":
    main()