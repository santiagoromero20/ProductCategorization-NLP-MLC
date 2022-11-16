from langdetect import detect
from fastapi import status, HTTPException
from Notebooks import text_normalizer

#Feedback Cleaning
def clean(text):
    
    #Text Depuration
    text = text_normalizer.clean_text(
        text=text,
        puncts=True,
        stopwords=True,
        urls=True,
        emails=True,
        numbers=True,
        emojis=True,
        special_char=True,
        phone_num=True,
        non_ascii=True,
        multiple_whitespaces=True,
        contractions=True,
        currency_symbols=True,
        custom_pattern=None,
    )

    #Text lemattization
    text = text_normalizer.lemmatize_text(text)

    return text

#Feedback Restrictions
def check_language(feedback):
    flag = False
    language = detect(feedback)
    
    if language == 'en':
        flag = True
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "Please write your product information in English!") 

    return flag

def check_length(feedback):
    flag = False
    words = len(feedback.split())
    if words <= 5:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Product´s title and description, together, must be greater than 5 words")
    elif words >= 200:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Product´s title and description, together, can not be greater than 200 words")
    else:
        flag = True

    return flag

def feedback_restrictions(feedback):
    return check_length(feedback) and check_language(feedback) 

def restrictions(feedback):
    return feedback_restrictions(feedback) 

