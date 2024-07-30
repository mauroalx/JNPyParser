# from src.config_writer import ConfigWriter

# if __name__ == "__main__":
#     config = """

#     """
#     config_writer = ConfigWriter(config)
#     converted_config = config_writer.write_configs()
#     print(converted_config)


import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from threading import Thread
from src.config_writer import ConfigWriter

def convert_and_save():
    def task():
        try:
            # Retrieve the configuration from the Text widget
            config = text_input.get("1.0", tk.END).strip()

            # Initialize the ConfigWriter and convert the configuration
            config_writer = ConfigWriter(config)
            converted_config = config_writer.write_configs()

            # Ask the user where to save the converted configuration
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )

            if file_path:
                # Write the converted configuration to the chosen file
                with open(file_path, 'w') as file:
                    file.write(converted_config)
                
                messagebox.showinfo("Success", "Configuration saved successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save the configuration: {e}")
        
        # Re-enable the UI elements
        convert_button.config(state=tk.NORMAL)
        text_input.config(state=tk.NORMAL)
        loading_label.pack_forget()

    # Disable the UI elements
    convert_button.config(state=tk.DISABLED)
    text_input.config(state=tk.DISABLED)
    
    # Show loading indicator
    loading_label.pack(pady=10)
    
    # Run the task in a separate thread to keep the UI responsive
    Thread(target=task).start()

# Set up the main window
root = tk.Tk()
root.title("Juniper Config Converter")
root.geometry("600x360")

# Create and place widgets
frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill=tk.BOTH, expand=True)

text_input = tk.Text(frame, height=15, width=70, wrap=tk.WORD)
text_input.pack(padx=10, pady=10)

convert_button = tk.Button(frame, text="Convert", command=convert_and_save, bg="lightblue", font=("Helvetica", 12))
convert_button.pack(pady=5)

loading_label = tk.Label(frame, text="Processing...", font=("Helvetica", 12), fg="red")
loading_label.pack_forget()

# Run the application
root.mainloop()
