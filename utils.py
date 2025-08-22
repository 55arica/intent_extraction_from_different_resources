import spacy
from logger import logging
import easyocr
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



# --------------------------------------------------------------


tokenizer = spacy.load("en_core_web_sm")

def extract_intent_spacy(text):
  tokens = tokenizer(text)
  intents = []

  for token in tokens:
    if token.pos_ in ["VERB", "NOUN", "PROPN", "ADJ"]:
      intents.append(token.lemma_) # lemma = base form (better for intent)


  # for chunk in token.noun_chunks: # Also include noun chunks (multi-word phrases like "flight ticket")
  #     intents.append(chunk.text)
  logging.info(f"INTENT: {intents}")
  return list(set(intents))

text = 'Book me a flight to Paris
print(extract_intent_spacy(text))



# --------------------------- with bert (generate)

# from transformers import pipeline

# generator = pipeline("text2text-generation", model = "google/flan-t5-small")
# def extract_intent_bert(text):
#     prompt = f"Extract the intent from this sentence in a few words: {text}"
#     result = generator(prompt, max_length=20, do_sample=False)
#     return result[0]['generated_text']

# print(extract_intent_bert("Can you check the latest news for me?"))



#------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------
# ============================================================================================ extract from image



def text_extraction_image(image_path):
  reader = easyocr.Reader(['en'])
  results = reader.readtext(image_path)
  texts = []
  for result in results: # # Get only the text
    bbox = result[0]
    text = result[1]
    confidence = result[2]

    texts.append(text)

    full_text = " ".join(texts)
    logging.info(f"extracted text : {full_text}")  
  return full_text
    

image_path = 'Intent_12.jpg'
data = text_extraction_image(image_path)
logging.info(f"Full Texts: {data}")




#------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
# ============================================================================================ extract from wev


def setup_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.page_load_strategy = "eager"
    return webdriver.Chrome(options=options)

def web_extraction(url, wait_time=10):
    driver = setup_driver()
    try:
        driver.get(url)  # Open webpage

        WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        body_text = driver.find_element(By.TAG_NAME, "body").text
        logging.info(f"Extracted text from web: {body_text[:200]}...")  # first 200 chars
        return body_text

    except Exception as e:
        logging.error(f"Failed to extract text: {e}")
        return None

    finally:
        driver.quit()


url = 'https://www..............'
fetch_data = web_extraction(url)

