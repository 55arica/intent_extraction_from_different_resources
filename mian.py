from utiles import extract_intent_spacy, text_extraction_image, web_extraction
from logger import logging

url = 'https://www..............'
image_path = 'Intent_12.jpg'
text = 'Book me a flight to Paris

fetch_data_web = web_extraction(url)
image_data = text_extraction_image(image_path)
logging.info(f"Full Texts: {data}")

text_data = extract_intent_spacy(text))
