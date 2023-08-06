import tkinter as tk
from microspeclib.datatypes.command import *
from microspeclib.datatypes.types   import *
from microspeclib.expert            import MicroSpecExpertInterface as expert

class Spectrometer(tk.Canvas):
  def __init__(self, *args, **kwargs):
    tk.Canvas.__init__(self, *args, **kwargs)
    #self.create_rectangle(50, 50, 100, 100)

  def redraw(self, pixels):
    if not pixels:
      return
    self.update() # or else the width and height commands won't work
    self.width  = self.winfo_width()
    self.height = self.winfo_height()
    npixels = len(pixels)
    minpixel = None
    maxpixel = None
    for p in pixels:
      minpixel = p if minpixel is None or p < minpixel else minpixel
      maxpixel = p if maxpixel is None or p > maxpixel else maxpixel
    if minpixel is None or maxpixel is None:
      return
    pixelrange = maxpixel - minpixel
    self.delete("all")
    n = 0
    for p in pixels:
      yrelative = p - minpixel
      ynormalized = yrelative * self.height / pixelrange
      xnormalized = n * self.width / npixels
      self.draw_dot(xnormalized, ynormalized)
      n = n + 1

  def draw_dot(self, x, y):
      self.create_rectangle(x,   self.height - y, 
                            x+1, self.height - y+1)

class BridgeLED(tk.Frame):
  def __init__(self, *args, **kwargs):
    tk.Frame.__init__(self, *args, **kwargs)
    self.state = tk.IntVar()
    self.label = tk.Label(self, text="Bridge LED", justify=tk.LEFT, padx=10)
    self.off   = tk.Radiobutton(self, text="Off",   padx=10, variable=self.state, value=LEDOff,  command=lambda:self.usb_send(self.state.get()))
    self.green = tk.Radiobutton(self, text="Green", padx=10, variable=self.state, value=LEDGreen,command=lambda:self.usb_send(self.state.get()))
    self.red   = tk.Radiobutton(self, text="Red",   padx=10, variable=self.state, value=LEDRed,  command=lambda:self.usb_send(self.state.get()))
    self.label.grid(row=0, column=0)
    self.off.grid(  row=0, column=1)
    self.green.grid(row=0, column=2)
    self.red.grid(  row=0, column=3)

  def usb_send(self, state):
    self.master.push_command(CommandSetBridgeLED(led_num=0, led_setting=state))

  def usb_receive(self, reply):
    if reply and reply.status == 0 and hasattr(reply, "led_setting"):
      self.set(reply.led_setting)

  def set(self, state):
    self.state.set(state)

  def get(self):
    return self.state.get()
  
class MicrospecGUI(tk.Frame):
  def __init__(self, *args, emulation=False, **kwargs):
    tk.Frame.__init__(self, *args, **kwargs)
    self.spec = Spectrometer(self, width=400, height=600)
    self.led  = BridgeLED(self)

    self.spec.grid(row=0, column=0)
    self.led.grid( row=0, column=1)

    self.queue = []
    self.wait  = []

    self.usb  = expert(emulation=emulation)

    self.push_command(CommandGetBridgeLED(led_num=0), self.led)
    self.push_command(CommandSetExposure(cycles=100))
    self.push_command(CommandSetSensorConfig(binning=True, gain=100, row_bitmap=0x1F))

    self.main_thread()

  def push_command(self, command, requestor=None):
    self.queue.append((command, requestor))

  def usb_receive(self, reply):
    if reply and reply.status == 0:
      #print("pixels: %s"%(reply))
      self.spec.redraw(reply.pixels)
      pass

  def main_thread(self):
    self.push_command(CommandCaptureFrame(), self)

    reply = self.usb.receiveReply()
    while reply:
      recipient = self.wait.pop(0)
      if recipient[1]:
        recipient[1].usb_receive(reply)
      reply = self.usb.receiveReply()

    while self.queue:
      command = self.queue.pop(0)
      self.usb.sendCommand(command[0])
      self.wait.append(command)

    self.after(100, self.main_thread)
    
    
    

root = tk.Tk()
gui = MicrospecGUI(root, emulation=False)
gui.pack()
gui.mainloop()
