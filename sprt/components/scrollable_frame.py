from tkinter import HORIZONTAL, NSEW, VERTICAL, Canvas, ttk


class ScrollableFrame(ttk.Frame):
    def __init__(self, master, direction: str, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Create a canvas and add it to the frame
        self.__canvas = Canvas(self, height=150, bd=0)
        self.__canvas.grid(row=0, column=0, sticky=NSEW, padx=0, pady=0, ipadx=0, ipady=0)

        # Create a scrollbar and attach it to the canvas
        if direction == VERTICAL:
            self.scrollbar = ttk.Scrollbar(self, orient=VERTICAL, command=self.__canvas.yview)
            self.scrollbar.grid(column=1, row=0, sticky=NSEW)
            self.__canvas.configure(yscrollcommand=self.scrollbar.set)
        else:
            self.scrollbar = ttk.Scrollbar(self, orient=HORIZONTAL, command=self.__canvas.xview)
            self.scrollbar.grid(column=0, row=1, sticky=NSEW)
            self.__canvas.configure(xscrollcommand=self.scrollbar.set)

        # Create a frame to hold the widgets
        self.inner_frame = ttk.Frame(self.__canvas)
        self.inner_frame.grid_rowconfigure(0, weight=1)
        self.inner_frame.grid_columnconfigure(0, weight=1)
        self.__holder = self.__canvas.create_window((0, 0), window=self.inner_frame)

        # Bind events to update the scroll region
        if direction == VERTICAL:
            self.__canvas.bind("<Configure>", self.on_canvas_configure_x)
        else:
            self.__canvas.bind("<Configure>", self.on_canvas_configure_y)

        self.inner_frame.bind("<Configure>", self.on_frame_configure)
        self.inner_frame.bind("<Enter>", self.__handle_enter)
        self.inner_frame.bind("<Leave>", self.__handle_mouse_leave)

    def __handle_enter(self, event):
        if str(self.scrollbar.cget("orient")) == VERTICAL:
            self.inner_frame.bind_all("<MouseWheel>", self.on_mouse_wheel_y)
        else:
            self.inner_frame.bind_all("<MouseWheel>", self.on_mouse_wheel_x)

    def __handle_mouse_leave(self, event):
        self.inner_frame.unbind_all("<MouseWheel>")

    def on_frame_configure(self, event):
        # # Update the scroll region to match the size of the inner frame
        self.__canvas.configure(scrollregion=self.__canvas.bbox("all"))

    def on_canvas_configure_x(self, event):
        # Update the canvas window to match the size of the canvas
        self.__canvas.itemconfig(self.__holder, width=event.width)

    def on_canvas_configure_y(self, event):
        # Update the canvas window to match the size of the canvas
        self.__canvas.itemconfig(self.__holder, height=event.height)

    def on_mouse_wheel_x(self, event):
        # Handle mouse wheel scrolling
        self.__canvas.xview_scroll(-1 * event.delta, "units")

    def on_mouse_wheel_y(self, event):
        # Handle mouse wheel scrolling
        self.__canvas.yview_scroll(-1 * event.delta, "units")
