from flask import Flask, jsonify
from faker import Faker
import random
from datetime import datetime, timedelta
import json

# Créer l'instance Flask
app = Flask(__name__)

# Listes de locales pour chaque continent
afrique_locales = ['sw', 'yo_NG', 'zu_ZA']  # Afrique (uniquement black people)
europe_locales = ['fr_FR', 'de_DE', 'it_IT', 'es_ES', 'nl_NL', 'pl_PL', 'en_GB', 'en_IE', 'en_CA', 'en_US', 'fr_BE', 'fr_CH', 'fr_QC', 'de_AT', 'de_CH', 'es_AR', 'es_CL', 'es_CO', 'es_MX', 'pt_PT', 'pt_BR', 'ro_RO', 'ru_RU', 'sk_SK', 'sl_SI', 'sq_AL', 'sv_SE', 'ga_IE', 'hu_HU', 'hy_AM', 'lt_LT', 'lv_LV', 'mt_MT', 'nl_BE', 'no_NO', 'uk_UA']
asie_locales = ['ja_JP', 'zh_CN', 'ko_KR', 'hi_IN', 'th_TH', 'id_ID', 'bn_BD', 'fil_PH', 'he_IL', 'ka_GE', 'ne_NP', 'or_IN', 'ta_IN', 'th', 'tl_PH', 'tr_TR', 'uz_UZ', 'vi_VN', 'zh_TW']

# Fonction pour choisir aléatoirement une locale en fonction du continent
def get_random_locale(continent):
    if continent == 'afrique':
        return random.choice(afrique_locales)
    elif continent == 'europe':
        return random.choice(europe_locales)
    elif continent == 'asie':
        return random.choice(asie_locales)
    else:
        raise ValueError("Continent inconnu. Choisissez entre 'afrique', 'europe', ou 'asie'.")

# Fonction pour générer une identité avec les données JSON
def generate_fake_identity():
    # Choisir aléatoirement un continent parmi 'afrique', 'europe', ou 'asie'
    continent = random.choice(['afrique', 'europe', 'asie'])

    # Choisir une locale aléatoire en fonction du continent
    locale = get_random_locale(continent)
    
    # Initialiser Faker avec la locale choisie
    fake = Faker(locale)

    # Générer les données
    nom = fake.last_name()
    prenom = fake.first_name()
    date_naissance = fake.date_of_birth(minimum_age=30, maximum_age=80).strftime("%Y-%m-%d")
    sexe = fake.random_element(elements=("M", "F"))
    adresse = fake.address().replace("\n", " ")
    identifiant = fake.unique.random_number(digits=9)
    date_validite = (datetime.now() + timedelta(days=365*10)).strftime("%Y-%m-%d")

    # Créer un dictionnaire avec les données générées
    identity_data = {
        "nom": nom,
        "prenom": prenom,
        "date_naissance": date_naissance,
        "sexe": sexe,
        "continent": continent,
        "locale": locale,
        "adresse": adresse,
        "identifiant": f"ID{identifiant}",
        "date_validite": date_validite
    }
    
    # Retourner sous forme de JSON
    return identity_data

# Route pour générer une identité fictive
@app.route('/generate_id/<int:num_rows>', methods=['GET'])
def generate_id(num_rows):
    identity_data = [generate_fake_identity() for _ in range(num_rows)]
    return jsonify(identity_data)

# Lancer l'application Flask
if __name__ == '__main__':
    app.run(debug=True)
