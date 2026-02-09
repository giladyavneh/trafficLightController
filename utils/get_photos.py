import requests
from pathlib import Path

url = "https://www.kaggle.com/api/v1/datasets/download/yusufberksardoan/traffic-detection-project"
# save_dir = Path(r"C:\Users\gilad\OneDrive\Desktop\datasets")
# save_dir.mkdir(parents=True, exist_ok=True)

# output_file = save_dir / "traffic-detection-project.zip"

with requests.get(url, stream=True) as r:
    r.raise_for_status()
    with open(output_file, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)

print("Saved to:", output_file)

def get_photos(url: str, save_path: Path):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    with open(save_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    print(f"Saved to: {save_path}")