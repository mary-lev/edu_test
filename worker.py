class Worker():
  def do(self):
    pass
    

class ColorFilterWorker(Worker):
  colors = ['red', 'grey', 'yellow', 'black', 'brown', 'pink', 'purple', 'green', 'blue', 'white', 'magenta', 'orange', 'cyan']
  
  def do(self, s):
    res = [word for word in s.split(' ') if word not in ColorFilterWorker.colors]
    return ' '.join(list(dict.fromkeys(res)))
  
w = ColorFilterWorker()
print(w.do('My black pocket contains grey pocket dollars'))