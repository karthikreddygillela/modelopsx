import base64
import time
from selenium import webdriver
from PIL import Image
from io import BytesIO
import os

def take_screenshot(url, save_path):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--window-size=1280,800")

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(2)  # wait for full page render
    png = driver.get_screenshot_as_png()
    driver.quit()

    image = Image.open(BytesIO(png))
    image.save(save_path)
    return save_path

def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode('utf-8')
    return f"![Screenshot - {os.path.basename(image_path)}](data:image/png;base64,{encoded})"

def update_readme_with_images(readme_path, images_base64, section_title="## UI Preview"):
    with open(readme_path, "r") as file:
        content = file.read()

    block = "\n\n".join(images_base64)

    if section_title in content:
        new_content = content.split(section_title)[0] + section_title + "\n\n" + block
    else:
        new_content = content + "\n\n" + section_title + "\n\n" + block

    with open(readme_path, "w") as file:
        file.write(new_content)

    print("✅ README updated with", len(images_base64), "inline screenshots.")

# -------------- Configurable Part -----------------
screenshots = [
    {"url": "http://127.0.0.1:8000/", "filename": "home.png"},
    {"url": "http://127.0.0.1:8000/hub/", "filename": "hub.png"},
    {"url": "http://127.0.0.1:8000/shell/", "filename": "shell.png"},
    {"url": "http://127.0.0.1:8000/usecases/", "filename": "usecases.png"}
]
# --------------------------------------------------

# Process all
inline_blocks = []
for item in screenshots:
    print(f"📸 Capturing {item['url']} ...")
    path = take_screenshot(item["url"], item["filename"])
    inline_blocks.append(image_to_base64(path))

# Update README
update_readme_with_images("README.md", inline_blocks)
