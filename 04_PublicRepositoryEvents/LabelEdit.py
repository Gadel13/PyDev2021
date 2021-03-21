import tkinter as tk
from tkinter import font

class InputLabel(tk.Label):
	def __init__(self, wind):

		self.text_var = tk.StringVar(value="")
		self.font_size = 16
		self.LabelFont = font.Font(family="Courier", size=self.font_size)
		self.default_LabelWidth = 12

		tk.Label.__init__(self, wind, font=self.LabelFont, textvariable=self.text_var,
							cursor='xterm', highlightthickness=1, padx=2, pady=2, relief=tk.RAISED,
							width=self.default_LabelWidth, anchor='w')


		self.cursor = tk.Frame(self, height=self.font_size, width = 1.5, bg='red')
		self.cursor_position = 0

		self.bind('<Key>', func=self.pressed_key_action)
		self.bind('<Button-1>', func=self.pressed_left_mouse_button)


		self.grid(row=0, sticky="EW")

	def update_cursor_pos(self, new_cursor_pos):
		str_len = len(self.text_var.get())
		self.cursor_position = min(max(new_cursor_pos, 0), str_len)

		tmp = self.text_var.get()[:self.cursor_position]
		cursor_place = self.LabelFont.measure(tmp)
		self.cursor.place(x=cursor_place)


	def pop_prev_char(self, ):
		cur = self.text_var.get()
		self.text_var.set(cur[:self.cursor_position - 1] + cur[self.cursor_position:])

		cur = self.text_var.get()
		self.configure(width=max(self.default_LabelWidth, len(cur)))

		self.update_cursor_pos(self.cursor_position - 1)

	def pop_next_char(self):
		cur = self.text_var.get()
		self.text_var.set(cur[:self.cursor_position] + cur[min(len(cur), self.cursor_position + 1):])
		cur = self.text_var.get()
		self.configure(width=max(self.default_LabelWidth, len(cur)))
		self.update_cursor_pos(self.cursor_position - 1)

	def push_char(self, c):
		cur = self.text_var.get()
		self.text_var.set(cur[:self.cursor_position] + c + cur[self.cursor_position:])
		cur = self.text_var.get()
		self.configure(width=max(self.default_LabelWidth, len(cur)))
		self.update_cursor_pos(self.cursor_position + 1)



	def pressed_key_action(self, act):
		if act.char.isprintable() and len(act.char) > 0:
			self.push_char(act.char)
		elif act.keysym == 'BackSpace':
			self.pop_prev_char()
		elif act.keysym == 'Delete':
			self.pop_next_char()
		elif act.keysym == 'Left':
			self.update_cursor_pos(self.cursor_position - 1)
		elif act.keysym == 'Right':
			self.update_cursor_pos(self.cursor_position + 1)
		elif act.keysym == 'Home':
			self.update_cursor_pos(0)
		elif act.keysym == 'End':
			newpos = len(self.text_var.get())
			self.update_cursor_pos(newpos)

	def pressed_left_mouse_button(self, act):
		x_cor = act.x
		cur = self.text_var.get()
		new_cursor_pos = len(cur)
		for i in range(len(cur) + 1):
			if self.LabelFont.measure(cur[:i]) >= x_cor:
				new_cursor_pos = i - 1
				break

		self.focus()
		self.update_cursor_pos(new_cursor_pos)


main_window = tk.Tk()
main_window.title("Label Edit")

quit_button = tk.Button(main_window, text="QUIT", command = main_window.destroy, fg='black')
quit_button.grid(row=1, sticky="E")

IL = InputLabel(main_window)

main_window.mainloop()