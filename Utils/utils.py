from datetime import datetime
import os

def get_xray_iso_time():
    _time = datetime.now().isoformat()
    return _time[:_time.find('.')] + "+01:00"

def create_directory():
    parent_dir = os.path.join(os.getcwd(), "Reports")
    directory = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    dir_path = os.path.join(parent_dir, directory) 
    os.mkdir(dir_path)
    return dir_path