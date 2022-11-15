import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib
import pickle as pkl
import time
from sklearn import metrics
import warnings
warnings.filterwarnings("ignore")
from sklearn.model_selection import GridSearchCV

#FUNCTIONS USED TO TRAIN AND PREDICT RESULTS IN THE MLModel NOTEBOOK

def get_metrics(y_test, predictions):
  print("Evaluation Metrics")
  print('-'*30)
  print("F1 Score:",metrics.f1_score(y_test, predictions, average="micro"))
  print("Recall Score:",metrics.recall_score(y_test, predictions, average="micro"))
  print("Precision Score:",metrics.precision_score(y_test, predictions, average="micro"))
  print("Hamming Loss:",metrics.hamming_loss(y_test, predictions), "\n")

def train_predict_model(x_train, y_train, x_test, y_test, method, name):
  print(name)
  model = method
  try:
    inicio = time.time()
    model.fit(x_train,y_train)
    fin = time.time()
    print("The time it takes to fit the model is",round(fin-inicio),"seconds.")
    filename = str(name)+"_model.pkl"
    joblib.dump(model, filename)
    predictions = model.predict(x_test)
    get_metrics(y_test, predictions)
  except:
    pass

def train_predict_model_gridsearch(x_train, y_train, x_test, y_test, method, param_grid, cv, scoring):
    model_grid = GridSearchCV(method, param_grid, cv=cv, scoring=scoring)
    inicio = time.time()
    print("Training...")
    model_grid.fit(x_train, y_train)
    fin = time.time()
    print("We have finished!")
    print("The time it takes to fit the model is",round(fin-inicio),"seconds.")
    filename = "BRKNNa_gridsearch_model.pkl"
    joblib.dump(model_grid, filename)
    predictions = model_grid.predict(x_test)
    get_metrics(y_test, predictions)
    try:
        print("Best params: "+str(model_grid.best_params_))
    except:
        pass

#Functions use to Train and Predict Models with Grid Searches...

def train_predict_model_adapt(x_train, y_train, x_test, y_test, method):
    classifier = method 
    inicio = time.time()
    classifier.fit(x_train.toarray(), np.array(y_train))
    fin = time.time()
    print("The time it takes to fit the model is",round(fin-inicio),"seconds.")
    filename = "MLARAM_model.pkl"
    joblib.dump(classifier, filename)
    predictions = classifier.predict(x_test)
    print("Evaluation Metrics")
    print('-'*30)
    print("Accuracy Score:",metrics.accuracy_score(y_test, predictions))
    print("F1 Score:",metrics.f1_score(y_test, predictions))
    print("Recall Score:",metrics.recall_score(y_test, predictions))
    print("Precision Score:",metrics.precision_score(y_test, predictions))
    print("Hamming Loss:",metrics.hamming_loss(y_test, predictions), "\n")

def train_predict_model_gridsearch_adapt(x_train, y_train, x_test, y_test, method, param_grid, cv, scoring):
    model_grid = GridSearchCV(method, param_grid, cv=cv, scoring=scoring)
    inicio = time.time()
    print("Training...")
    model_grid.fit(x_train, y_train)
    fin = time.time()
    print("We have finished!")
    print("The time it takes to fit the model is",round(fin-inicio),"seconds.")
    filename = "BRKNNa_gridsearch_model.pkl"
    joblib.dump(model_grid, filename)
    predictions = model_grid.predict(x_test)
    try:
        print("Best params: "+str(model_grid.best_params_))
        print("Best Score: "+str(model_grid.best_score_))
        print("Hamming Loss:",metrics.hamming_loss(y_test, predictions), "\n")
    except:
        pass
  

"""

Functions called at the ml_service file to get the predicton for the uploaded text from the User (use for Model != Neural Netorks), 
my final Model ended up being a Neural Netowork this will not be used. Even though, I will keep the code for further use, just in 
case a new Model performs better than the current NN use.

def get_categories(pred, df):
    pred = pred.toarray()
    columns_numbers = []
    for i in range(pred.shape[1]):
        if pred[0][i] == 1:
            columns_numbers.append(i)

    a = df.columns.tolist()
    categories = []
    for k in range(len(columns_numbers)):
        for j in range(len(a)):
            if columns_numbers[k] == j:
                b = a[j].split("_")
                c = b[1]
                categories.append(c)
    
    return categories

def predict(text, df):
    #Load text received from the page then, run our ML model to get predictions.
    text = text_normalizer.clean_text(
    text, puncts=True, stopwords=True, urls=True, emails=True, numbers=True, emojis=True, special_char=True,
    phone_num=True, non_ascii=True, multiple_whitespaces=True, contractions=True, currency_symbols=True, custom_pattern=None,
    )
    text = text_normalizer.lemmatize_text(text)
    text_vectorized  = tfidf_vectorizer.transform([text])
    predictions = model.predict(text_vectorized)
    categories = get_categories(predictions, df)
    return categories 

"""