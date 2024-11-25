import subprocess

def bot_git_update():
    script_path = "./Scripts/BotUpdate.sh"
    # Dont need to get a response becouse the program will be terminated
    subprocess.run([script_path], check = True)