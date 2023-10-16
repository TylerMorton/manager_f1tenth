#!/usr/bin/python3

import os, sys, re


COMPOSE_PATH = "f1tenth_gym_ros/docker-compose.yml"


def env_setup():
    pattern = r"- \.:/sim_ws/src/f1tenth_gym_ros"
    replacement = "- ./f1tenth_labs_openrepo/lab1_ws/src/:/sim_ws/src/"

    os.system(
        "git clone --quiet https://github.com/f1tenth/f1tenth_gym_ros.git > /dev/null"
    )
    os.system(
        "git clone --quiet https://github.com/f1tenth/f1tenth_labs_openrepo.git > /dev/null"
    )
    os.system("mv f1tenth_labs_openrepo f1tenth_gym_ros/")

    file = open(COMPOSE_PATH, "r")
    content = file.read()
    # print(re.search(pattern, content, flags=re.DOTALL))
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    file = open(COMPOSE_PATH, "w")
    file.write(content)


def build_container():
    os.system(
        "docker-compose -f f1tenth_gym_ros/docker-compose.yml -p f1tenth_gym_ros up -d --quiet-pull "
    )


def destroy_container():
    os.system(
        "docker-compose -f f1tenth_gym_ros/docker-compose.yml -p f1tenth_gym_ros down"
    )


def adjust_compose():
    destroy_container()
    file = open(COMPOSE_PATH, "r")
    full_content = []

    print(
        "This program updates your docker-compose file to the lab you want to work on."
    )
    print(
        "If you don't want to update your docker-compose file please exit this program (control + c)"
    )

    while True:
        print("which lab do you want to work on?.. Or if you want to go back type 'b'")
        inp = input()
        if inp == "b":
            return
        try:
            if int(inp) in range(10):
                break
        except ():
            continue

    for content in file.readlines():
        content = re.sub(r"lab\d+_ws", "lab" + str(inp) + "_ws", content, re.DOTALL)
        full_content.append(content)

    file = open(COMPOSE_PATH, "w")
    file.writelines(full_content)

    print("\n\n Your compose file is updated!!\n")


def exec_container():
    os.system("docker exec -it f1tenth_gym_ros-sim-1 /bin/bash")


def main():
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


if __name__ == "__main__":
    main()
