import tkinter as tk
from tkinter import messagebox
import random

free_tile_cord = [0, 0]

def create_solvable(tiles, free):
	N = free[0] + 1
	for i in range(0, len(tiles)):
		for j in range(i, len(tiles)):
			if(tiles[i] > tiles[j]):
				N += 1

	new_tiles = tiles

	if (N % 2 == 1):
		random.shuffle(new_tiles)
		new_tiles = create_solvable(new_tiles, free)

	return new_tiles


def new_game():
	global free_tile_cord
	tiles_order = list(range(15))
	random.shuffle(tiles_order)

	free_tile_cord[0] = random.randint(0, 3)
	free_tile_cord[1] = random.randint(0, 3)

	tiles_order = create_solvable(tiles_order, free_tile_cord)

	count = 0
	for i in range(16):
		r = i//4
		c = i%4
		if(r != free_tile_cord[0] or c != free_tile_cord[1]):
			tile_buttons[tiles_order[count]].grid(row = r*2, column = c*2, sticky="NEWS", columnspan = 2, rowspan = 2)
			count += 1

def move(idx):
	def move_tile():
		global free_tile_cord
		grid_info = tile_buttons[idx].grid_info()
		r = grid_info['row']//grid_info['rowspan']
		c = grid_info['column']//grid_info['columnspan']
		if abs(free_tile_cord[0] - r) + abs(free_tile_cord[1] - c) > 1:
			return
		tile_buttons[idx].grid_configure(row=free_tile_cord[0]*2, column=free_tile_cord[1]*2)
		free_tile_cord = [r, c]

		win = True
		for i in range(15):
			grid_info = tile_buttons[i].grid_info()
			r = grid_info['row'] // grid_info['columnspan']
			c = grid_info['column'] // grid_info['columnspan']
			if r != i // 4 or c != i % 4:
				win = False
				break
		if win:
			messagebox.showinfo('15 game', 'VICTORY')

	return move_tile

main_window = tk.Tk()
main_window.title("15 game")
main_window.geometry('600x600')
main_window.configure(background='yellow')

main_window.columnconfigure(0, weight=1)
main_window.rowconfigure(1, weight=1)

menu = tk.LabelFrame(main_window, text = "MENU", relief=tk.RAISED)
menu.configure(background='orange')
menu.grid(row = 0, column = 0, sticky="NEWS")

for i in range(8):
	menu.columnconfigure(i, weight=2)

new_game_button = tk.Button(menu, text="NEW GAME", command = new_game, bg="green", fg='black')
new_game_button.grid(row=0, column=1, sticky="NEWS", columnspan=2)

exit_game_button = tk.Button(menu, text="EXIT", command = main_window.destroy, bg="red", fg='black')
exit_game_button.grid(row=0, column=5, sticky="NEWS", columnspan=2)

game = tk.Frame(main_window)
game.rowconfigure(0, weight=2)
for i in range(8):
	game.columnconfigure(i, weight=2)
	game.rowconfigure(i, weight=2)

game.grid(row = 1, column = 0, sticky="NEWS")

tile_buttons = []

for i in range(15):
	if i % 2 == 0:
		tile_buttons.append(tk.Button(game, text=str(i+1), command=move(i), bg="white", fg='black'))
	else:
		tile_buttons.append(tk.Button(game, text=str(i+1), command=move(i), bg="blue", fg='black'))


main_window.mainloop()