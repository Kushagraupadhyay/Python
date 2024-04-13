# this file is used to monitor the folder where the reports are generated and delete all files except the latest one
import pyarrow
import os
import pandas as pd
import glob as gb # to read all files in a folder
import time # to get current time
from watchdog.observers import Observer # to monitor file changes
from watchdog.events import FileSystemEvent, FileSystemEventHandler # to handle file changes

class ExcelFileHandler(FileSystemEventHandler): # Class to handle file changes
    def on_created(self, event: FileSystemEvent) -> None:
        print(f'File created: {event.src_path}')
        directory = os.path.dirname(event.src_path) # Get the directory of the file 
        for file in os.listdir(directory):
            if file.endswith('.xlsx')  and file != os.path.basename(event.src_path):
                print(f'Removing file: {file}')
                os.remove(os.path.join(directory,file)) # Remove all files except the newly created file
        
def start_file_observer():
    event_handler = ExcelFileHandler() 
    file_observer = Observer() # Create an observer to monitor file changes
    file_observer.schedule(event_handler,path='C:/Users/kuupadh/Downloads/reportfolder/',recursive=False)
    file_observer.start()
    try:
        while True:
            time.sleep(1) 
    except KeyboardInterrupt:
        file_observer.stop() 
    file_observer.join() # Wait for the observer to stop

    


