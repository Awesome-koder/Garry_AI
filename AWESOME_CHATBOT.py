import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk, ImageSequence

# Import langchain-huggingface (assuming it's installed)
from langchain_huggingface import HuggingFaceEndpoint
# Set up your API key (replace with your own)
sec_key = "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"

import os
os.environ["HUGGINGFACEHUB_API_TOKEN"] = sec_key

repo_id = "mistralai/Mistral-7B-Instruct-v0.2" # Replace with the correct repo ID if needed
llm = HuggingFaceEndpoint(repo_id=repo_id, temperature=0.7)

# Create GUI window
# Function to show main window
def show_main_window():
  def send_message(event=None):
    user_input = entry.get().capitalize()
    if user_input.lower() == 'exit':
      root.destroy() # Close the window
    else:
    # Update conversation display
     conversation.config(state=tk.NORMAL)
     conversation.insert(tk.END, "\n\nYou: " + user_input + "\n\n\n\n", "user")
     conversation.tag_configure("user", foreground="#888", font=("Arial", 10, "bold"))
     conversation.config(state=tk.DISABLED)
     entry.delete(0, tk.END)

    # sending user query for response
    response = llm.invoke(user_input)

    # Update conversation display with response
    conversation.config(state=tk.NORMAL)
    conversation.insert(tk.END, "ChatBot: " + response + "\n\n\n\n", "bot")
    conversation.tag_configure("bot", foreground="white", font=("Arial", 10, "bold"))
    conversation.config(state=tk.DISABLED)
    conversation.see(tk.END) # Scroll to the bottom

  def caps(event):
    v.set(v.get().capitalize())

  # Destroy Splash Screen
  splash_root.destroy()

  root = tk.Tk()
  root.title("Garry ChatBot")
  root.geometry("500x550")
  root.configure(bg="#2c3e50")

  # Create conversation display
  conversation = tk.Text(root, wrap="word", state=tk.DISABLED, bg="#2c3e51")
  conversation.pack(expand=True, fill=tk.BOTH)
  conversation.tag_configure("user", foreground="#888", font=("Arial", 10, "bold"))
  conversation.tag_config("bot", foreground="white", font=("Arial", 10, "bold"))

  # Create styled input field
  style = ttk.Style()
  style.theme_use('default')
  style.configure('TEntry', padding=5, relief="flat", borderwidth=3)
  style.map('TEntry', fieldbackground=[('readonly', 'white')])

  v = StringVar()
  entry = ttk.Entry(root, width=40, font="helvetica 12 bold", background="#87CEEB", textvariable=v)
  entry.insert(0, "Enter your message...") # Clear placeholder text
  entry.pack(side=tk.BOTTOM, padx=10, pady=10)
  entry.bind("<KeyRelease>", caps)
  entry.bind("<FocusIn>", lambda event: entry.delete(0, tk.END)) # Clear on focus
  entry.bind("<Return>", send_message) # Send message on Enter key
  entry.focus() # Set initial focus

  # Run the main event loop
  root.mainloop()

# Splash Screen Setup
splash_root = tk.Tk()
splash_root.geometry("500x550")
# splash_root.overrideredirect(True)

# Load GIF image (replace with your GIF path)
gif_image = Image.open("A:\coding\CHAT_BOT_MODELS\GARRY_AI\Garry_AI.gif")
frames = [frame.copy() for frame in ImageSequence.Iterator(gif_image)]
gif_images = [ImageTk.PhotoImage(frame) for frame in frames]

# Create canvas with GIF image
canvas = Canvas(splash_root, width=500, height=550)
canvas.pack()
canvas_image = canvas.create_image(0, 0, anchor=NW, image=gif_images[0])

# Autoplay the GIF
def update_gif(frame):
  canvas.itemconfig(canvas_image, image=gif_images[frame])
  splash_root.after(60, update_gif, (frame + 1) % len(gif_images))

update_gif(0)

# Show Splash Screen for 6.5 seconds (6500 milliseconds) and then show main window
splash_root.after(6500, show_main_window)

splash_root.mainloop()