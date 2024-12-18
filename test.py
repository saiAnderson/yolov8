import os

# Directory containing the files
directory = r"C:\Users\user\OneDrive\桌面\trash dataset\labels\train_labels"

# Loop through all files in the directory
for filename in os.listdir(directory):
    if filename.startswith("plastic") and filename.endswith(".txt"):
        file_path = os.path.join(directory, filename)
        
        # Open the file in read mode
        with open(file_path, "r") as file:
            content = file.read()

        # Split the content into words
        words = content.split()

        # Replace the first word
        if words:  # Check if there are any words
            words[0] = "2"  # Replace with your desired word

        # Join the words back into a single string
        new_content = " ".join(words)

        # Open the file in write mode and save the changes
        with open(file_path, "w") as file:
            file.write(new_content)

        print(f"Updated the first word in {filename}")

    elif filename.startswith("trash") and filename.endswith(".txt"):
        file_path = os.path.join(directory, filename)
        
        # Open the file in read mode
        with open(file_path, "r") as file:
            content = file.read()

        # Split the content into words
        words = content.split()

        # Replace the first word
        if words:  # Check if there are any words
            words[0] = "3"  # Replace with your desired word

        # Join the words back into a single string
        new_content = " ".join(words)

        # Open the file in write mode and save the changes
        with open(file_path, "w") as file:
            file.write(new_content)

        print(f"Updated the first word in {filename}")

