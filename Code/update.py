import subprocess
import os
import fcntl

# def bot_git_update(branch = "main"):
#     script_path = "./Scripts/BotUpdate.sh"
#     # Dont need to get a response becouse the program will be terminated
#     subprocess.run([script_path, "--branch", branch], check = False)

def bot_git_update(branch="main"):
    lockfile = "/tmp/botupdate_python.lock"

    with open(lockfile, "w") as lock_fd:
        try:
            # Try to acquire a non-blocking exclusive lock
            fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            print("Update already in progress. Exiting.")
            return

        # Run the update script
        script_path = "./Scripts/BotUpdate.sh"
        subprocess.run([script_path, "--branch", branch], check=False)

def bot_reboot():
    subprocess.run(["bash", "./Scripts/BotReboot.sh"], check=True)
