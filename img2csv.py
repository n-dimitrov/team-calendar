from PIL import Image
from openai import OpenAI
import base64

client = OpenAI()

image_file = "./data/2024.06.png"
print('Encoding ', image_file)
with open(image_file, 'rb') as image_file:
    image_data = image_file.read()
    encoded_image = base64.b64encode(image_data)
    base64_image = encoded_image.decode('utf-8')
print('Done')

print('Creating client')
response = client.chat.completions.create(
model="gpt-4o",
messages=[
    {
    "role": "system",
    "content": "You are a helpful assistant. Your task is to convert images containing tabular data into structured CSV files. You will use Optical Character Recognition (OCR) to extract text from the images and then process this text to create a CSV file with specific headers. The image contains a table with the following columns: Name, Request no., Date of request, Status, From, To, Duration in search period, Duration, Absence, Short description, Comment. The table may have multiple rows with data for different employees. Your goal is to extract this data and save it to a CSV file. You can use any tools or libraries you need to accomplish this task. Please let me know if you need any additional information or guidance."   ,
    },
    {
    "role": "user",
    "content": [
        {"type": "text", "text": "Extract the data from the image. The separtor must be ';'. Combine columns Short description, Comment and Project into one column called Description. The end result must contains this header: Name;Request_no;Date_of_request;Status;From;To;Days;Duration;Absence;Description and employee data only. "},
        {
        "type": "image_url",
        "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}"
        },
        },
    ],
    }
],
max_tokens=1000,
# response_format={ "type": "json_object" }
)

print('Analyzing...')
result = response.choices[0].message.content
print(result)