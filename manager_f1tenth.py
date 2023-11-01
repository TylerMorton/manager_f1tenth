#!/usr/bin/python3

import os, sys, re
import subprocess

# from subprocess import CalledProcessError

COMPOSE_PATH = "f1tenth_gym_ros/docker-compose.yml"


def process_error(cmd, statement=None):
    try:
        subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as err:
        if statement:
            print(statement)
        print(f"Error statement: {err.stderr}\n")
        sys.exit(1)


def env_setup():
    process_error(
        "git clone --quiet https://github.com/f1tenth/f1tenth_gym_ros.git > /dev/null"
    )
    process_error(
        "git clone --quiet https://github.com/f1tenth/f1tenth_labs_openrepo.git > /dev/null"
    )
    process_error("mv f1tenth_labs_openrepo f1tenth_gym_ros/")
    process_error("cp docker-compose.yml f1tenth_gym_ros/docker-compose.yml")


def build_container():
    process_error(
        "docker compose -f f1tenth_gym_ros/docker-compose.yml -p f1tenth_gym_ros up -d --quiet-pull",
        "\nUnable to run docker command. Is docker running?\n",
    )
    print("\nDocker container built.")


def destroy_container():
    process_error(
        "docker compose -f f1tenth_gym_ros/docker-compose.yml -p f1tenth_gym_ros down",
        "\nContainer doesn't exist.",
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
        print(
            "\nwhich lab do you want to work on?.. Or if you want to go back type 'b'\n"
        )
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
    process_error(
        "docker exec -it f1tenth_gym_ros-sim-1 /bin/bash",
        "\nContainer doesn't exist. Try building the container first [Option 3]",
    )


def main():
    print("\nWelcome to the f1tenth manager.\n")
    while True:
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
