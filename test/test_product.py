import pytest

invalid_description_large = ("The first time I used it, the app seemed good to me. Afterwards," 
"I started it to use it daily and started realizing certain annoying errors such as the music"
"being outdated, there are no local bands in my area and also that it cannot be used without internet."
"On the other hand, I value certain functionalities such as being able to share my list of favorite"
"songs on different social networks just by clicking and how easy and intuitive it was to learn to use it."
"I really do not think I will pay for the premium subscription for the things mentioned but I am sure I will" 
"continue to be a regular user of the free version as long as it stays that way. I hope some day this features"
"will be solved and the user could have a most pleasure exoerience, until that I will mantain my posture"
"mentioned earlier and still use my cds for my favourite local bands. Nespresso Vertuo Next Coffee Maker by"
"Breville Limited Edition Glossy Black with Aeroccino - Limited Edition Glossy Black Nespresso introduces"
"the VERTUO NEXT Glossy Black, the latest VERTUO Nespresso coffee maker with an all-new design in a limited"
"edition color for the ultimate brewing experience. In addition to its original espressos, NESPRESSO VERTUO NEXT"
"produces an extraordinary cup of coffee with a smooth layer of crema, the signature of truly great cup of coffee")

invalid_description_short = "Smart tv 43 inches" 

invalid_description_nonenglish = ("43 Clase F30 Serie LED 4K UHD inteligente fuego TV Disfruta de cada momento con 4K Ultra"
"HD impresionante en esta pantalla de 43 pulgadas. Está equipado con DTS Studio Sound para crear audio realista e inmersivo." 
"Acceda a canales y transmisiones en vivo por aire, y contrólelo todo con su voz")

valid_title = "Insignia"

valid_description = ("Insignia™ - 43 Class F30 Series LED 4K UHD Smart Fire TV Take in every moment with breathtaking 4K Ultra HD on this 43-inch screen."
"It’s equipped with DTS Studio Sound to create realistic and immersive audio. Access live over-the-air channels and streaming—and control it all with your voice.")

@pytest.mark.parametrize("title, description, prediction, status_code", [
    (None, valid_description, "prediction", 422), 
    (valid_title, None, "prediction", 422),
    (valid_title, invalid_description_large, "prediction", 400),
    (valid_title, invalid_description_short, "prediction", 400),
    (valid_title, invalid_description_nonenglish, "prediction", 400),
    (valid_title, valid_description, "prediction", 201),

])
def test_create_product(client, title, description, prediction, status_code):
    res = client.post(
        "/product/", json={"title": title, "description": description, "prediction": prediction})
    
    assert res.status_code == status_code

 