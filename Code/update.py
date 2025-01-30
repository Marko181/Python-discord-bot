import subprocess

def bot_git_update(branch = "main"):
    script_path = "./Scripts/BotUpdate.sh"
    # Dont need to get a response becouse the program will be terminated
    subprocess.run([script_path, "--branch", branch], check = False)

def bot_reboot():
    subprocess.run(["bash", "./Scripts/BotReboot.sh"], check=False)
