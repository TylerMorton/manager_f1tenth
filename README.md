# Slugbotics F1tenth Manager
A program that sets up your developer environment for you! As well as manages your docker container, shell, and organizes files. **Does not work on Windows** (Maybe wsl.. idk)

## Make sure you have the following dependencies installed:
- Python3
- Docker Desktop (docker, docker-compose)
- Git

## Install Steps
1. Clone this repo.
2. Run this command:
```
cd manager_f1tenth && chmod +x manager_f1tenth.py
```
4. Run the script via ```./manager_f1tenth.py```

## Where to start?

First start the initial setup, docker container build options via the manager program.

When working on the labs, start in the directory of this repo and go into the labs directory:
```
cd f1tenth_gym_ros/f1tenth_labs_openrepo/
```
there you will see all of the lab documents labelled as f1tenth_lab[1-9].

If you have started the docker container you will also see lab1_ws. This is your workspace for lab1. It is a binding mount so both the container and your host computer have access to the files. You can develop locally... Nice. If you want to start any other lab make sure to update your docker container and rebuild via the manager.

## Bugs, Enhancements, Etc.
Feel free to contact me about bugs, enhancements, etc.
