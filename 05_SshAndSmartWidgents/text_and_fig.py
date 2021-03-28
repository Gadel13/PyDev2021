import tkinter as tk
import random

class Oval():
	def __init__(self, line):
		self.str = line
		tmp = line.split(';')

		if len(tmp) != 7:
			raise BaseException

		self.xl = int(tmp[0])
		self.yl = int(tmp[1])
		self.xr = int(tmp[2])
		self.yr = int(tmp[3])
		self.in_color = tmp[4]
		self.out_color = tmp[5]
		self.w = int(tmp[6])

class Text(tk.Text):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.bind('<<Modified>>', self.text_update)
		self.tag_configure("incorrect", background="red")

	def text_update(self, args):
		self.tag_remove("incorrect", "1.0", "end")

		self.master.figure_field.delete('all')

		lines = self.get("1.0", "end").split('\n')
		self.master.figure_field.figs = []

		for cur_line, l in enumerate(lines):
			try:
				new_figure = Oval(l)
				self.master.figure_field.add_oval(new_figure, cur_line+1)
			except:
				line_start = "%d.0" % (cur_line+1)
				line_stop = "%d.end" % (cur_line+1)
				self.tag_add("incorrect", line_start, line_stop)

		self.edit_modified(False)

	def add_string(self, figure):
		self.insert('end', figure + '\n')

	def update_string(self, dx, dy, line):
		cur = self.get(str(line)+'.0', str(line)+'.end')
		self.delete(str(line)+'.0', str(line)+'.end')

		cur = cur.split(';')
		new = str(int(cur[0]) + dx) + ';'
		new += str(int(cur[1]) + dy) + ';'
		new += str(int(cur[2]) + dx) + ';'
		new += str(int(cur[3]) + dy) + ';'
		new += cur[4] + ';'
		new += cur[5] + ';'
		new += cur[6]

		self.insert(str(line)+'.0', new)



		
class Figure(tk.Canvas):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.figs = []
		self.action = ["NOTHING"]

		self.bind("<Button-1>", self.right_mouse_click)
		self.bind("<ButtonRelease-1>", self.right_mouse_release)

	def right_mouse_click(self, event):
		overlap = self.find_overlapping(event.x, event.y, event.x, event.y)

		if len(overlap) > 0:
			self.action = []
			self.action.append("MOVE")
			self.action.append(event.x)
			self.action.append(event.y)
			self.action.append(self.gettags(overlap[-1]))
		else:
			self.action = []
			self.action.append("NEW")

			xl = event.x
			yl = event.y
			in_color = '#%06x' % random.randint(0, 256*256*256-1)
			out_color = '#%06x' % random.randint(0, 256*256*256-1)
			w = random.randint(1, 5)

			self.action.append(xl)
			self.action.append(yl)
			self.action.append(in_color)
			self.action.append(out_color)
			self.action.append(w)




	def right_mouse_release(self, event):
		if self.action[0] == "NOTHING":
			return
		elif self.action[0] == "NEW":
			xl = self.action[1]
			yl = self.action[2]
			xr = event.x
			yr = event.y
			in_color = self.action[3]
			out_color = self.action[4]
			w = self.action[5]

			oval_line = str(xl) + ";" + str(yl) + ";" + str(xr) + ";" + str(yr) + ";" + str(in_color) + ";" + str(out_color) + ";" + str(w)
			self.master.text_field.add_string(oval_line)


		elif self.action[0] == "MOVE":
			move_x = event.x - self.action[1]
			move_y = event.y - self.action[2]
			cur_line = int(self.action[3][0])
			self.master.text_field.update_string(move_x, move_y, cur_line)



	def add_oval(self, new_figure, line):
		self.create_oval(new_figure.xl, new_figure.yl, new_figure.xr, new_figure.yr, fill=new_figure.in_color,
						outline=new_figure.out_color, width=new_figure.w, tag=line)
		self.figs.append(new_figure)


class Application(tk.Tk):
	def __init__(self, title="title", *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.title(title)
		self.columnconfigure(0, weight=1)
		self.rowconfigure(0, weight=1)

		self.create_widgets()
		
	def create_widgets(self):
		self.text_field = Text(self)
		self.text_field.grid(row=0, column=0, sticky="NEWS")

		self.figure_field = Figure(self)
		self.figure_field.grid(row=0, column=1, sticky="NEWS")

		self.menu = tk.Frame(self)
		self.menu.grid(row=1, column=0, sticky="NEWS")
		self.quit_button = tk.Button(self.menu, text="Quit", command=self.destroy)
		self.quit_button.grid(row=0, column=0)

application = Application(title="Text and Figures")
application.mainloop()