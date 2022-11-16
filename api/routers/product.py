from fastapi import Depends, APIRouter, status
from api import models, utils, schemas
from api.database import get_db
from sqlalchemy.orm import Session

import json
from tensorflow import keras
from keras_preprocessing.text import tokenizer_from_json
import pandas as pd
from Notebooks import nn_aux

router = APIRouter(
    prefix = "/product",
    tags = ["product"]
)

#Get all 496 classes
df = pd.read_csv("bestmodel/y_test.csv", index_col=0)
classes = [col for col in df.columns]
classes = classes[:]

#Loading the Model and the Tokenizer
model =  keras.models.load_model('bestmodel/best_nn-conv1d.h5')
with open('bestmodel/tokenizer.json') as f:
    data = json.load(f)
    tokenizer = tokenizer_from_json(data)

#MaxLen for a word after being padded
maxlen = 57

def predict(information, model):
    cats = nn_aux.categoryPredictionNN(information, classes, tokenizer, model, maxlen)
    return cats


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ProductOut)
def create_product(product:schemas.ProductCreate,db: Session = Depends(get_db)):

    #Merging the product info
    title = product.title
    description = product.description
    text =  title + " " + description

    #Restriction Check
    if utils.restrictions(text) == True:
        pass
    
    #Cleaning the Data
    text = utils.clean(text)
    
    #Getting Prediction
    product.prediction = predict(text, model)
    print(product.prediction, type(product.prediction), product.prediction[0])
    #Saving product into db for future retraining
    new_product = models.Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product 