from PIL import Image
import numpy as np
import cv2
import svgwrite
import tkinter as tk
from tkinter import filedialog, messagebox
import time

# Create the main application window (optional, can be hidden)
root = tk.Tk()
root.withdraw()  # Hide the root window

n = "y"
while n=="y":

    # Open the file selection dialog
    file_path = filedialog.askopenfilename(
        title="Select a File",
        filetypes=[("Images", "*.png"), ("All Files", "*.*")]
    )

    if file_path:

        # Load the generated skyline image
        image_path = file_path
        image = Image.open(image_path).convert("L")

        # Convert image to numpy array and apply threshold
        image_np = np.array(image)
        _, binary = cv2.threshold(image_np, 128, 255, cv2.THRESH_BINARY_INV)

        # Find contours (shapes) in the binary image
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Create SVG file
        height, width = binary.shape
        svg = svgwrite.Drawing(size=(f"{width}px", f"{height}px"))

        # Draw each contour as a polygon
        for contour in contours:
            points = [(int(x), int(y)) for [[x, y]] in contour]
            svg.add(svg.polygon(points, fill='black'))

        # Save file location dialog
        Save_path = filedialog.asksaveasfilename(
            title="Save File As",
            defaultextension=".svg",  # Default file extension
            filetypes=[("SVG Vector", "*.svg"), ("All Files", "*.*")]  # File type options
        )
        
        # Save SVG file
        if Save_path:
            svg_output_path = Save_path
            print("Almost there...")
            svg.saveas(svg_output_path)
            print("Exported As", svg_output_path)
        else:
            print("Save operation canceled.")

    else:
        image_selected = 0
        print("No File Selected.")

    # Again?
    response = messagebox.askyesno("One more?", "Do you want to Convert one more Image to SVG?")
    if response:
        n = "y"
    else:
        n = "n"
        print("Closing")

# 2 sec delay
if n=="n":
    time.sleep(2)
