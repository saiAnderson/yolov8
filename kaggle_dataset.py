import kagglehub

# Download latest version
path = kagglehub.dataset_download("fatemehboloori/trash-type-detection")

print("Path to dataset files:", path)