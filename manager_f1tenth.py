#!/usr/bin/python3

import os, sys, re, atexit, json


COMPOSE_PATH = "f1tenth_gym_ros/docker-compose.yml"
CURRENT_LAB = "current_lab"
CONFIG = None

def write_config():
    print('Writing out config...')
    
    with open("config.json", 'w') as f:
        json.dump(CONFIG, f)


def init_config():
    global CONFIG
    atexit.register(write_config)
    
    print('Initializing config...')
    with open('config.json', 'r') as f:
        CONFIG = json.load(f)

def env_setup():
    os.system(
        "git clone --quiet https://github.com/f1tenth/f1tenth_gym_ros.git > /dev/null"
    )
    os.system(
        "git clone --quiet https://github.com/f1tenth/f1tenth_labs_openrepo.git > /dev/null"
    )
    os.system("cp docker-compose.yml f1tenth_gym_ros/docker-compose.yml")


def build_container():
    os.system(
        "docker compose -f f1tenth_gym_ros/docker-compose.yml -p f1tenth_lab" + str(CONFIG[CURRENT_LAB]) + " up -d --quiet-pull "
    )


def destroy_container():
    print("Here")
    os.system(
        "docker compose -f f1tenth_gym_ros/docker-compose.yml -p f1tenth_lab" + str(CONFIG[CURRENT_LAB]) + " down"
    )


def adjust_compose():
    destroy_container()
    file = open(COMPOSE_PATH, "r")
    full_content = []

    print(
        "\nThis program updates your docker-compose file to the lab you want to work on."
    )
    print(
        "\nIf you don't want to update your docker-compose file please exit this program (control + c)"
    )

    while True:
        print("\nwhich lab do you want to work on?.. Or if you want to go back type 'b'\n")
        inp = input()
        if inp == "b":
            return
        try:
            if int(inp) in range(10):
                CONFIG[CURRENT_LAB] = int(inp)
                break
        except ():
            continue

    for content in file.readlines():
        content = re.sub(r"f1tenth_lab\d+", "f1tenth_lab" + str(CONFIG[CURRENT_LAB]), content, re.DOTALL)
        full_content.append(content)

    file = open(COMPOSE_PATH, "w")
    file.writelines(full_content)

    print("\n\n Your compose file is updated!!\n")


def exec_container():
    os.system("docker exec -it f1tenth_gym_ros-sim-1 /bin/bash")


def cycle_commands():
    while True:
        print("\nWelcome to the f1tenth manager.\n")
        print("What are you trying to do?\n\n")
        print("1. Setup my environment for me please.")
        print(
            "2. I would like to work on lab [blank]. CAUTION THIS closes any processes running in an open container"
        )
        print("3. Build container.")
        print(
            "4. Destroy container. CAUTION: This closes any processes running in an open container."
        )
        print("5. Enter container shell.")
        print("0. I'm done, Goodbye.")
        print("\n\nEnter number here:\n")

        inp = input()
        try:
            i = int(inp)
            if i == 1:
                env_setup()
                print(
                    "\nYour developer environment is setup. Now you can choose the build option.\n"
                )
            if i == 2:
                adjust_compose()
            if i == 3:
                build_container()
            if i == 4:
                destroy_container()
            if i == 5:
                exec_container()
            if i == 0:
                print("\nGoodbye.\n")
                sys.exit()
        except ():
            continue


def main():
    init_config()
    cycle_commands()

if __name__ == "__main__":
    main()
