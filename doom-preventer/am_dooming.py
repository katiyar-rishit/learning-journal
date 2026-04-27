import psutil


def is_process_running(process_name):

    for process in psutil.process_iter(["name"]):
        try:
            if process_name.lower() in process.info["name"].lower():
                return True

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    return False


app_name = "firefox"

if is_process_running:
    print(f"{app_name} is currently running.")
else:
    print(f"{app_name} is not running.")
