import os
import tkinter as tk
import uuid
from tkinter import filedialog, messagebox

import pyautogui


class ScreenshotApp:
	def __init__(self, root):
		self.root = root
		self.root.attributes("-fullscreen", True)
		self.root.attributes("-alpha", 0.3)  # Transparenz setzen
		self.canvas = tk.Canvas(self.root, cursor="cross")
		self.canvas.pack(fill=tk.BOTH, expand=True)

		self.start_x = None
		self.start_y = None
		self.rect = None

		self.canvas.bind("<ButtonPress-1>", self.on_button_press)
		self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
		self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

	def on_button_press(self, event):
		self.start_x = event.x
		self.start_y = event.y
		self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red')

	def on_mouse_drag(self, event):
		cur_x, cur_y = (event.x, event.y)
		self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

	def on_button_release(self, event):
		end_x, end_y = (event.x, event.y)
		self.root.destroy()
		self.take_screenshot(self.start_x, self.start_y, end_x, end_y)

	def take_screenshot(self, start_x, start_y, end_x, end_y):
		x = min(start_x, end_x)
		y = min(start_y, end_y)
		width = abs(end_x - start_x)
		height = abs(end_y - start_y)

		screenshot = pyautogui.screenshot(region=(x, y, width, height))

		save_path = self.choose_save_location()
		if save_path:
			short_uuid = str(uuid.uuid4())[:8]  # Erzeuge eine kurze UUID (8 Zeichen)
			save_path = save_path.replace('.png', f'_{short_uuid}.png')
			screenshot.save(save_path)
			messagebox.showinfo("Erfolg", f"Screenshot gespeichert unter: {save_path}")
		else:
			messagebox.showwarning("Abgebrochen", "Screenshot wurde nicht gespeichert.")

	def choose_save_location(self):
		# Holen des Verzeichnisses, in dem das Skript läuft
		base_dir = os.path.dirname(os.path.abspath(__file__))

		options = [
			("work_dir/screenshots", os.path.join(base_dir, "work_dir","screenshots", "screenshot.png"))
			# ("conf/mehr_suchergebnisse", os.path.join(base_dir, "conf", "mehr_suchergebnisse", "screenshot.png")),
			# ("conf/search_templates", os.path.join(base_dir, "conf", "search_templates", "screenshot.png")),
			# ("conf/yesweeat_weiter", os.path.join(base_dir, "conf", "yesweeat_weiter", "screenshot.png")),
			# ("conf/accept_templates", os.path.join(base_dir, "conf", "accept_templates", "screenshot.png")),
		]

		save_dialog = tk.Tk()
		save_dialog.withdraw()  # Hauptfenster ausblenden

		choice = tk.simpledialog.askstring("Speicherort auswählen",
		                                   "Wähle den Speicherort:\n1 - work_dir\n2 save ass ",
		                                   parent=save_dialog)

		if choice == "1":
			return options[0][1]

		elif choice == "2":
			# Benutzerdefinierter Speicherort
			return filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
		else:
			return None


if __name__ == "__main__":
	root = tk.Tk()
	app = ScreenshotApp(root)
	root.mainloop()