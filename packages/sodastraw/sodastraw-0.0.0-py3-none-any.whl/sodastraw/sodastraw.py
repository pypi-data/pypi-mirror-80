import sys
import argparse
import tkinter as tk
import threading
import queue

import requests
from PIL import Image
from io import BytesIO
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from matplotlib.widgets import TextBox
from matplotlib import colorbar

# crosshair location
X = 800
Y = 800


def main(argv=sys.argv[1:]):

    parser = argparse.ArgumentParser(
        description='Start Sodastraw'
    )
    
    parser.add_argument(dest='url', nargs='?',
                        help='URL of image source',
                        default='http://hpwren.ucsd.edu/cameras/L/wilson-n-mobo-c.jpg')

    parser.add_argument('-r', '--rate', dest='rate', 
                        help='Update frequency in ms. Default is 1000 (1 sec)',
                        default=1000)

    args = parser.parse_args(argv)


    root = tk.Tk()
    client = ThreadedClient(root, args.url, args.rate)
    root.mainloop()



# https://www.oreilly.com/library/view/python-cookbook/0596001673/ch09s07.html

class PlotWindow:
    def __init__(self, master, queue, destroy_fn):
        self.queue = queue
        self.master = master

        self.master.wm_title('Sodastraw')

        # calls the destroy_fn function when the GUI window is closed
        self.master.protocol("WM_DELETE_WINDOW", destroy_fn)

        self.fig = Figure(figsize=(7,7), dpi=100)
        self.ax = self.fig.add_subplot(1,1,1)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)

        self.x = X
        self.y = Y

    def dequeue(self):
        """Handle all messages currently in the queue, if any."""
        # handle messages currently in the queue, if any
        while self.queue.qsize():
            try:
                msg = self.queue.get(0)
                if msg.status_code == requests.codes.ok:
                    img = np.array(Image.open(BytesIO(msg.content)))
                    self.plot(img)
            except queue.Empty:
                pass

    def plot(self, img):
        self.ax.clear()
        im = self.ax.imshow(img)
        #self.ax.plot(self.x, self.y, 'r+')
        #self.ax.grid()
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

class ThreadedClient:
    """
    Launch the main part of the GUI and the worker thread. periodicCall and
    endApplication could reside in the GUI part, but putting them here
    means that you have all the thread controls in a single place.
    """
    def __init__(self, master, url, rate):
        """
        Start the GUI and the asynchronous threads. We are in the main
        (original) thread of the application, which will later be used by
        the GUI as well. We spawn a new thread for the worker (I/O).
        """
        self.master = master
        self.url = url
        self.rate = rate

        # Create the queue
        self.queue = queue.Queue()

        # Set up the GUI part
        self.gui = PlotWindow(master, self.queue, self.destroy)

        # Set up the thread to do asynchronous I/O
        # More threads can also be created and used, if necessary
        self.running = 1
        self.thread = threading.Thread(target=self.get_data)
        self.thread.start()

        # Start the periodic call in the GUI to check if the queue contains
        # anything
        self.poll_queue()

    def poll_queue(self):
        """
        Check every <rate> ms if there is something new in the queue.
        """
        self.gui.dequeue()
        if not self.running:
            # This is the brutal stop of the system. You may want to do
            # some cleanup before actually shutting it down.
            import sys
            sys.exit(1)
        self.master.after(self.rate, self.poll_queue)

    def get_data(self):
        '''This function handles the asynchronous I/O. This thread should
        yield control pretty regularly.
        '''
        while self.running:
            r = requests.get(self.url)
            self.queue.put(r)

    def destroy(self):
        self.running = 0


if __name__ == '__main__':
    root = tk.Tk()
    client = ThreadedClient(root)
    root.mainloop()
