import sys
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class RestartDaphneEventHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.is_directory:
            return
        if event.event_type in ['created', 'modified']:
            print("Restarting Daphne...")
            subprocess.run(['pkill', '-HUP', '-f', 'daphne'])


if __name__ == "__main__":
    path = '.'  # Monitor current directory for changes
    event_handler = RestartDaphneEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True: 
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
