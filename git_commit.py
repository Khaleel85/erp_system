import subprocess


def git_command(command):
    process = subprocess.Popen(command, shell=True)
    process.wait()


def main():
    message = input("Enter a message: ")
    git_command("git add .")
    git_command('git commit -am "' + message + '"')
    git_command("git push origin")


if __name__ == "__main__":
    main()
