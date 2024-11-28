import tkinter as tk
import os, pandas as pd
from tkinter import filedialog,messagebox, scrolledtext
import shutil

#clean and save function
# Function to browse for input file
def Function():
    def browse_input_file():
        file_path = filedialog.askopenfilename(
            filetypes=[("Excel files", "*.xlsx"),("CSV files", "*.csv")]
        )
        input_entry.delete(0, 'end')
        input_entry.insert(0, file_path)

    # Function to browse for output file
    def browse_output_file():
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"),("CSV files", "*.csv")]
        )
        output_entry.delete(0, 'end')
        output_entry.insert(0, file_path)

    # Function to clean data
    def clean_data():
        input_path = input_entry.get().strip()
        output_path = output_entry.get().strip()

        try:
            # Load file
            if input_path.endswith('.csv'):
                df = pd.read_csv(input_path)
            elif input_path.endswith('.xlsx'):
                df = pd.read_excel(input_path, engine='openpyxl')
            else:
                messagebox.showerror("Error", "Unsupported file format. Use .csv or .xlsx.")
                return

            # Data cleaning: fill NA and remove duplicates
            df.fillna("N/A", inplace=True)
            df.drop_duplicates(inplace=True)

            # Save the cleaned file
            if output_path.endswith('.csv'):
                df.to_csv(output_path, index=False)
            elif output_path.endswith('.xlsx'):
                df.to_excel(output_path, index=False, engine='openpyxl')
            else:
                messagebox.showerror("Error", "Unsupported output format. Use .csv or .xlsx.")
                return

            messagebox.showinfo("Success", "Cleaned data saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # GUI setup
    window = tk.Tk()
    window.title("Data Cleaning Tool")
    window.geometry("500x200")
    window.resizable(False, False)

    # Input file selection
    tk.Label(window, text="Input File:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
    input_entry = tk.Entry(window, width=50)
    input_entry.grid(row=0, column=1, padx=10, pady=10)
    input_browse_button = tk.Button(window, text="Browse", command=browse_input_file)
    input_browse_button.grid(row=0, column=2, padx=10, pady=10)

    # Output file selection
    tk.Label(window, text="Output File:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
    output_entry = tk.Entry(window, width=50)
    output_entry.grid(row=1, column=1, padx=10, pady=10)
    output_browse_button = tk.Button(window, text="Browse", command=browse_output_file)
    output_browse_button.grid(row=1, column=2, padx=10, pady=10)

    # Clean data button
    clean_button = tk.Button(window, text="Clean and Save", command=clean_data)
    clean_button.grid(row=2, column=1, pady=20)

    window.mainloop()

# creating function for large files
def start_finding_large_files():
    directory = path_entry.get()
    if not os.path.isdir(directory):
        messagebox.showerror("Error", "Please select a valid directory!")
        return

    try:
        size_threshold = int(size_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid size threshold in MB!")
        return

    log_text.delete(1.0, tk.END)
    size_threshold_bytes = size_threshold * 1024 * 1024
    large_files = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.getsize(file_path) > size_threshold_bytes:
                large_files.append((file, os.path.getsize(file_path) / (1024 * 1024)))

    if large_files:
        log_text.insert(tk.END, f"\nLarge files (over {size_threshold} MB):\n")
        for file, size in large_files:
            log_text.insert(tk.END, f"{file}: {size:.2f} MB\n")
    else:
        log_text.insert(tk.END, "\nNo large files found.\n")

# creating function to browse
def BrowseDir():
  directory=filedialog.askdirectory()
  if directory:
        path_entry.delete(0,tk.END)
        path_entry.insert(0,directory)
  
# creating function for deep clean
def start_cleaning():
   
    directory = path_entry.get()
    if not os.path.isdir(directory):
        messagebox.showerror("Error", "Please select a valid directory!")
        return

    log_text.delete(1.0, tk.END)
    extensions_to_remove = ['.tmp', '.log', '.bak']
    removed_files = 0

    for root, dirs, files in os.walk(directory):
        for file in files:
            if any(file.endswith(ext) for ext in extensions_to_remove):
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    removed_files += 1
                    log_text.insert(tk.END, f"Removed: {file_path}\n")
                except Exception as e:
                    log_text.insert(tk.END, f"Error removing {file_path}: {e}\n")

    log_text.insert(tk.END, f"\nTotal temporary files removed: {removed_files}\n")

# creating function for Organizing
def OrganizeFiles(): 
    path=path_entry.get()
    extension=extension_entry.get()
    
    if not os.path.exists(path):
        messagebox.showerror("Error",f'The Path {path} does not exist')
        return

    extension_to_sort=[ext.strip() for ext in extension.split(',')] if extension else []
    
    files=os.listdir(path)
    for file in files:
        source=os.path.join(path,file)
        if os.path.isfile(source):
            filename,extension=os.path.splitext(file)
            extension=extension[1:] #Removing leading dot
            
            destination_folder=os.path.join(path,extension)
            if not os.path.exists(destination_folder):
                os.makedirs(destination_folder)
            destination= os.path.join(destination_folder,file)
            if os.path.exists(destination):
                log_text.insert(tk.END,f'skipping: {file} already exist in {destination_folder}')
                os.remove(source)
            else:
                shutil.move(source,destination)
                log_text.insert(tk.END,f'Moved: {file} -> {destination_folder} \n')
                
    messagebox.showinfo("Success","Files organized successfully..")
                
#creating GUI
root =tk.Tk()
root.title('File Management Suite')
root.geometry("1000x500")
root.resizable(False, False)

# path selcetion
tk.Label(root,text='Enter the Path to Organize files: ').grid(row=1,column=0,padx=10,pady=10,sticky='w')
path_entry=tk.Entry(root,width=50)
path_entry.grid(row=1,column=1,padx=10,pady=10)

# Size threshold input
tk.Label(root, text="Size Threshold for Large Files (MB):").grid(row=3,column=0,padx=10,pady=10,sticky='w')
size_entry = tk.Entry(root, width=20)
size_entry.grid(row=3,column=1,padx=25,pady=10, sticky='w')


# OrganizeButton
tk.Button(root,text='Browse' ,command=BrowseDir, width=15).grid(row=1,column=2,pady=10,padx=10)

#Extension_entry
tk.Label(root,text='Enter extension to Organize or Leave Blank').grid(row=2,column=0,padx=10,pady=10, sticky='w')
extension_entry=tk.Entry(root,width=50)
extension_entry.grid(row=2,column=1,padx=10,pady=10)


# creating button for that
tk.Button(root,text='Organize' ,command=OrganizeFiles, width=20).grid(row=0,column=1,pady=10)
tk.Button(root,text='Deep Clean' ,command=OrganizeFiles, width=20).grid(row=0,column=0,pady=10)
tk.Button(root,text='Find Large Files' ,command=start_finding_large_files, width=20).grid(row=0,column=2,pady=10)
tk.Button(root,text='Clean and Save',command=Function, width=20).grid(row=0,column=3,pady=10)

#Log area
log_text=tk.Text(root,height=15,width=120)
log_text.grid(row=4,column=0,columnspan=4,padx=10,pady=10)

root.mainloop()