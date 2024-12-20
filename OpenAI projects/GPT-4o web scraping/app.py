from selenium import webdriver
from openai import OpenAI
import base64
import pandas as pd

driver = webdriver.Chrome()
driver.set_window_size(1504,768)
driver.execute_script("document.body.style.zoom = '50%'")
driver.get("https://www.aliexpress.us/w/wholesale-laptop.html?g=y&SearchText=laptop")
driver.save_screenshot("webpage1.png")
driver.quit()

def image_converter(image_path):
  with open(image_path, "rb") as image_file: 
    return base64.b64encode(image_file.read()).decode('utf-8') 
  

img = image_converter('webpage.png')

client = OpenAI()

response = client.chat.completions.create(
  model="gpt-4o",
  messages=[
    {
      "role": "system",
      "content": [
        {
          "type": "text",
          "text": "You are a professional data scraper. Scrape the data about all laptops from the provided image and store it in a csv file named data.csv."
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{img}" 
          }
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "type": "text",
          "text": "Based on the provided image, here's the data about the laptops that I was able to extract:\n\n1. **Laptop 1**\n   - **Brand/Model:** ASUS ROG Zephyrus GX501\n   - **Price:** ZAR 10,091.4\n   - **Shipping:** Free shipping\n   - **Store:** Shop912577372 Store\n\n2. **Laptop 2**\n   - **Brand/Model:** Intel Celeron N95/N100 Laptop (No specific brand is visible)\n   - **Screen Size:** 16-inch\n   - **Processor:** Intel Celeron N95/N100\n   - **Display:** 1920x1200 FHD Screen\n   - **Storage:** 32GB RAM, 2TB SSD\n   - **Price:** ZAR 9,232.83\n   - **Shipping:** Free shipping\n   - **Store:** BSLAY Official Store\n\n3. **Laptop 3**\n   - **Brand/Model:** AK56 (Brand not clear)\n   - **Screen Size:** 15.6 inch\n   - **OS:** Windows 10\n   - **Sales:** 14 sold\n   - **Rating:**  (not specified)\n   - **"
        }
      ]
    }
  ],
  temperature=1,
  max_tokens=256,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)


print(response.choices[0])

str=response.choices[0]

data = []
lines = str.split('\n')
columns = []
for line in lines:
    if line.startswith('|'):
        cells = [cell.strip() for cell in line.split('|')[1:-1]]
        if not columns:
            columns = cells
        else:
            data.append(cells)

# Creating a DataFrame
df = pd.DataFrame(data, columns=columns)

# Saving the DataFrame to a CSV file
csv_file_path = 'data.csv'
df.to_csv(csv_file_path, index=False)

print(f"Data saved to {csv_file_path}")