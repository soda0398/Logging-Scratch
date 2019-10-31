from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer
import os,time,zipfile,json

path = ""
log_path = ""
zip_path = ""

target_file = "*.sb3"

def sb3tozip():
  os.chdir(path)
  for filename in os.listdir("."):
    if filename.endswith("sb3"):
      zip_file = filename[0:len(filename) - len("sb3")] + "zip"
      os.rename(filename,zip_file)
      return 1
  return 0

def extractfile():
    os.chdir(path)
    for filename in os.listdir("."):
        if filename.endswith("zip"):
            zip_ref = zipfile.ZipFile(filename,"r")
            zip_ref.extract("project.json",path=log_path,pwd=None)
            zip_ref.close()
            return 1
    return 0

def rotation():
  os.chdir(log_path)
  count = next(os.walk(log_path))[2]
  for filename in os.listdir("."):
    if filename == "project.json":
      rename = str(len(count)) + ".json"
      os.rename(filename,rename)
      return 1
  return 0

def move():
  os.chdir(path)
  count = next(os.walk(log_path))[2]
  for filename in os.listdir("."):
    if filename.endswith("zip"):
      os.rename(filename,zip_path+str(len(count)) + filename)
      return 1
  return 0


class FileChangeHandler(PatternMatchingEventHandler):
  def on_created(self,event):
    filepath = event.src_path
    filename = os.path.basename(filepath)
    #print('%s created' % filename)
    sb3tozip()
    extractfile()
    rotation()
    move()


if __name__ in '__main__':

  event_hander = FileChangeHandler([target_file])
  observer = Observer()
  observer.schedule(event_hander,path,recursive=True)
  observer.start()

  try:
    while True:
      time.sleep(1)
  except KeyboardInterrupt:
    observer.stop()
  observer.join()
