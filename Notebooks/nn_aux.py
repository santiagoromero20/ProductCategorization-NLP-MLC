import matplotlib.pyplot as plt
import numpy as np
from sklearn import metrics
import operator
from keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import text_normalizer

#FUNCTIONS USE TO GET AND PLOT METRICS

def train_vs_valid(history, loss, val_loss, auc, val_auc):
  # Plotting losses wrt epochs(time)
  plt.plot(history.history[str(loss)], label="Training Loss") 
  plt.plot(history.history[str(val_loss)], label="Validation Loss")
  plt.legend()
  plt.show()
  # Plotting accuracy wrt epochs(time)
  plt.plot(history.history[str(auc)], label="Training AUC")
  plt.plot(history.history[str(val_auc)], label="Validation AUC")
  plt.legend()
  plt.show()

def get_metrics(model, x_test, y_test):
    metrics = model.evaluate(x_test, y_test)

def tranform_binary(predictions):
    a = predictions.tolist()
    for i in range(len(a)):
        for j in range(len(a[i])):
            if a[i][j] >= 0.5:
                a[i][j] = 1
            else:
                a[i][j] = 0

    a = np.array(a)
    return a
  
def get_standar_metrics(predictions, y_test):
  a = tranform_binary(predictions)
  print("Evaluation Metrics")
  print('-'*30)
  print("F1 Score:",metrics.f1_score(y_test, a, average="micro"))
  print("Recall Score:",metrics.recall_score(y_test, a, average="micro"))
  print("Precision Score:",metrics.precision_score(y_test, a, average="micro"))
  print("Hamming Loss:",metrics.hamming_loss(y_test, a), "\n")


#######################################################################################################

# FUNCTIONS USE TO RETURN CATEGORIES

def check_best(a):
  max_prob = a[0][2]
  best = a[0][1]
  if len(a) == 1:
    best = a[0][1]
  else:
    for i in range(len(a)):
      if a[i][2] >= max_prob:
        max_prob = a[i][2]
        best = a[i][1]
  
  return best
    
def clean_output(bests):
  info = []
  for i in range(len(bests)):
      a = bests[i][0]
      b = bests[i][1]
      level, cat = a.split("_")
      c = (level, cat, bests[i][1])
      info.append(c)
  
  output = []
  mains  = []
  first  = []
  second = []
  for i in range(len(info)):
    if info[i][0] == "Main Category":
      mains.append(info[i])
    elif info[i][0] == "1st Subcategory":
      first.append(info[i])
    elif info[i][0] == "2nd Subcategory":
      second.append(info[i])

  levels = [mains, first, second] 
  for i in range(len(levels)):
    if len(levels[i]) == 0:
      pass
    else:
      a = check_best(levels[i])
      output.append(a)

  return output

def categoryPredictionNN(information, classes, tokenizer, model, maxlen):
  # Data cleaning process
    information = text_normalizer.clean_text(
    information, puncts=True, stopwords=True, urls=True, emails=True, numbers=True, emojis=True, special_char=True,
    phone_num=True, non_ascii=True, multiple_whitespaces=True, contractions=True, currency_symbols=True, custom_pattern=None,
    )
    information = text_normalizer.lemmatize_text(information)

    # Necessary data preprocessing steps
    sequences = tokenizer.texts_to_sequences([information])
    x = pad_sequences(sequences, maxlen=maxlen)

    prediction = model.predict(x)
    predScores = [score for pred in prediction for score in pred]

    predDict = {}
    for cla,score in zip(classes,predScores):
        predDict[cla] = score
    bests = sorted(predDict.items(), key=operator.itemgetter(1),reverse=True)[:10]
    output = clean_output(bests)
    return output 


#######################################################################################################

#EXAMPLES TO USE AS TESTS

#Microwave, MacBookPrp, SmartTV, Washer, Guitar, Freezer-Refrigerator, SmartTV(II), CornerDesk, NespressoMachine
exs = [
["Insignia™ - 0.9 Cu. Ft. Compact Microwave - Stainless steel Only at Best BuyHeat food quickly and efficiently with this 0.9 cu. ft. Insignia microwave. One-touch buttons take the guesswork out of cooking common foods like popcorn and pizza, and the bright LED display lets you operate the device in low-light conditions. This Insignia microwave has an integrated child lock for safety"],
["MacBook Pro 13.3 Laptop - Apple M1 chip - 8GB Memory - 256GB SSD - Space Gray The Apple M1 chip redefines the 13-inch MacBook Pro. Featuring an 8-core CPU that flies through complex workflows in photography, coding, video editing, and more. Incredible 8-core GPU that crushes graphics-intensive tasks and enables super-smooth gaming."],
["Insignia™ - 43 Class F30 Series LED 4K UHD Smart Fire TV Take in every moment with breathtaking 4K Ultra HD on this 43-inch screen. It’s equipped with DTS Studio Sound to create realistic and immersive audio. Access live over-the-air channels and streaming—and control it all with your voice."],
["GE - 4.5 Cu. Ft. Top Load Washer with Precise Fill - White on white Simplify laundry washing with this 4.5 cu. ft. GE top-load washer. A speed wash setting provides clean clothes sooner, and the 14 washer cycles, six washer settings and six wash temperatures ensure the right setup for your fabrics. The auto soak option on the GE top-load washer helps you battle pesky stains before washing begins."],
["Carlo Robelli - 6-String Full-Size Dreadnought-Cutaway Acoustic/Electric Guitar - Beige/Black/Brown Entertain family and friends with this Samson Carlo Robelli D readnought acoustic-electric guitar package. The classic blend of a genuine spruce wood top and an agathis back and sides produce an ideal balance, deliver a warm tone and offer a natural projection."],
["Top-Freezer Refrigerator - Stainless steet Its 18 cubic foot capacity makes it an ideal option for apartments and smaller kitchens. Adjustable shelves let you customize your food storage to suit your needs. The top mount freezer puts frozen food within easy reach and reversable fridge door lets you position your new refrigerator to fit your kitchen layout or personal preference. Adjustable, spill-safe glass shelving in the fridge keeps your items neatly organized, and convenient door storage offers extra space for butter, eggs, bottled drinks and more."],
["Samsung - 70” Class 7 Series LED 4K UHD Smart Tizen TV Enhance your viewing experience with this 70-inch Samsung 4K UHD smart TV. The HDR technology and 4K UHD resolution render sharp details and realistic colors, while a Crystal processor delivers exceptional picture quality on the flat-panel display. This Bluetooth-enabled Samsung 4K UHD smart TV is voice controllable for hands-free operation and seamless wireless streaming."],
[" L-Shaped Modern Glass Corner Computer Desk - Silver Update your home office or study with this modern and sleek corner computer desk. Crafted from durable steel with a powder-coated finish and thick, tempered safety glass. The L-shape design provides the perfect fit for space-saving needs and features a sliding keyboard tray and unattached CPU stand. Its flexible configuration allows you to mount the tray on either side of the desk according to your needs. This contemporary l-shaped office desk gives you plenty of table space to place your computer on one side, with the other side left for décor or organizing your office supplies."],
["Nespresso Vertuo Next Coffee Maker by Breville Limited Edition Glossy Black with Aeroccino - Limited Edition Glossy Black Nespresso introduces the VERTUO NEXT Glossy Black, the latest VERTUO Nespresso coffee maker with an all-new design in a limited edition color for the ultimate brewing experience. In addition to its original espressos, NESPRESSO VERTUO NEXT produces an extraordinary cup of coffee with a smooth layer of crema, the signature of truly great cup of coffee."]
]

def examples():
  return exs

