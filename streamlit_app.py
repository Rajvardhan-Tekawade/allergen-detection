import streamlit as st
import re

# ==========================
# 🎉 Page Configurations
# ==========================
st.set_page_config(
    page_title="Allergen Detection System",
    page_icon="🛑",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ==========================
# ✅ Allergen Synonyms Dictionary (Rule-based Matching)
# ==========================
allergen_synonyms = {
    "milk": ["casein", "whey", "lactose", "lactalbumin", "curds", "ghee", "cream", "butter", "cheese", "yogurt", "kefir", "caseinate", "rennet casein"],
    "eggs": ["albumin", "egg white", "egg yolk", "globulin", "livetin", "lysozyme", "ovoglobulin", "ovalbumin", "ovomucoid", "ovovitellin", "silici albuminate"],
    "peanuts": ["groundnut", "arachis oil", "monkey nut", "goober", "earthnut", "beer nuts", "peanut flour", "peanut protein"],
    "tree nuts": ["almond", "brazil nut", "cashew", "chestnut", "hazelnut", "macadamia", "pecan", "pine nut", "pistachio", "walnut", "nut butters", "nut meal", "nut paste"],
    "fish": ["anchovy", "bass", "catfish", "cod", "flounder", "grouper", "haddock", "hake", "halibut", "herring", "mackerel", "mahi mahi", "perch", "pike", "pollock", "salmon", "sardine", "snapper", "sole", "swordfish", "tilapia", "trout", "tuna", "fish sauce", "fish oil", "fish gelatin"],
    "shellfish": ["crab", "crayfish", "lobster", "prawns", "shrimp", "clams", "cockle", "cuttlefish", "limpet", "mussels", "octopus", "oysters", "scallops", "snails", "squid", "whelk", "periwinkle", "barnacle"],
    "soy": ["soybean", "edamame", "miso", "natto", "shoyu", "soya", "soy sauce", "tamari", "textured vegetable protein", "tofu", "yuba", "soy lecithin", "hydrolyzed soy protein"],
    "wheat": ["wheat", "whole wheat", "wholemeal", "bread flour", "bulgur", "couscous", "cracker meal", "durum", "einkorn", "emmer", "farina", "farro", "graham flour", "kamut", "matzo", "matza", "matzah", "matzoh", "seitan", "semolina", "spelt", "triticale", "atta", "maida", "refined wheat flour", "whole grain flour"],
    "gluten": ["wheat", "barley", "rye", "malt", "triticale", "spelt", "semolina", "einkorn", "emmer", "farro", "kamut", "gluten", "vital wheat gluten"],
    "sesame": ["benne", "benne seed", "gingelly", "sesame flour", "sesame oil", "sesame paste", "sesame seed", "tahini", "til"],
    "mustard": ["mustard seed", "mustard flour", "mustard oil", "mustard greens", "yellow mustard", "brown mustard", "black mustard"],
    "celery": ["celery stalk", "celery seed", "celery root", "celeriac"],
    "sulfites": ["sulfur dioxide", "potassium bisulfite", "potassium metabisulfite", "sodium bisulfite", "sodium metabisulfite", "sodium sulfite"],
    "lupin": ["lupine", "lupin flour", "lupin seed", "lupinus"],
    "mollusks": ["clam", "cockle", "cuttlefish", "limpet", "mussels", "octopus", "oyster", "periwinkle", "scallop", "snail", "squid", "whelk"]
}

# ==========================
# 🧹 Cleaning Function
# ==========================
def clean_ingredients(text):
    text = text.lower()  # Convert to lowercase
    text = re.sub(r"[^\w\s]", " ", text)  # Remove special characters
    text = re.sub(r"\s+", " ", text).strip()  # Normalize whitespace
    return text

# ==========================
# 🔍 Rule-Based Allergen Detection Function
# ==========================
def detect_allergens_rule_based(ingredient_text):
    cleaned_text = clean_ingredients(ingredient_text)

    # Rule-Based Synonym Detection
    allergens_detected = set()
    for allergen, synonyms in allergen_synonyms.items():
        if allergen in cleaned_text:
            allergens_detected.add(allergen)
        else:
            for synonym in synonyms:
                if synonym in cleaned_text:
                    allergens_detected.add(allergen)
                    break

    return sorted(allergens_detected)

# ==========================
# 🎨 Header and Intro
# ==========================
st.markdown("<h1 style='text-align: center;'>🛑 Allergen Detection System 🛑</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: gray;'>Check ingredients for potential allergens in your food!</h4>", unsafe_allow_html=True)
st.markdown("---")

# ==========================
# 🍽 Dish & Ingredients Input Section
# ==========================
st.subheader("🍽 Enter Dish Details:")

# Dish name input
dish_name = st.text_input("Dish Name", placeholder="E.g., Paneer Butter Masala")

# Ingredients input
ingredients_input = st.text_area(
    "List the Ingredients used (comma-separated)",
    placeholder="E.g., paneer, butter, cream, tomatoes, spices"
)

# ==========================
# ✅ Button & Prediction
# ==========================
if st.button("🔎 Check for Allergens"):
    if not dish_name.strip():
        st.warning("⚠ Please enter the Dish Name.")
    elif not ingredients_input.strip():
        st.warning("⚠ Please enter the Ingredients.")
    else:
        allergens_found = detect_allergens_rule_based(ingredients_input)

        st.markdown(f"## 🍽 Dish: *{dish_name}*")
        st.markdown(f"### 📝 Ingredients: {ingredients_input}")

        if not allergens_found:
            st.success("✅ No allergens detected in this dish!")
        else:
            st.error("🚨 Allergens detected in this dish:")
            for allergen in allergens_found:
                st.write(f"🔸 *{allergen.capitalize()}*")

# ==========================
# 🧠 Sidebar Information
# ==========================
st.sidebar.title("ℹ About This App")
st.sidebar.info("""
This system helps users detect common food allergens by analyzing the ingredient list of food products and dishes.
It's designed for:
- Individuals with *food allergies*
- Health-conscious consumers
- Parents concerned about *children's diets*
""")

st.sidebar.markdown("---")
st.sidebar.subheader("🚨 Common Allergens:")
st.sidebar.markdown("""
- Milk 🥛  
- Eggs 🥚  
- Peanuts 🥜  
- Tree Nuts 🌰  
- Fish 🐟  
- Shellfish 🦐  
- Soy 🌱  
- Wheat 🌾  
- Gluten 🍞  
- Sesame 🌿  
- Mustard 🌶  
- Celery 🥬  
- Sulfites 🧪  
- Lupin 🌾  
- Mollusks 🐚  
""")

st.sidebar.markdown("---")
st.sidebar.subheader("💡 Health Tips:")
st.sidebar.info("""
- Always read ingredient labels carefully.
- Consult with a healthcare provider if unsure.
- Cross-contamination is a risk in processed foods!
- Introduce potential allergens to infants with medical guidance.
""")

st.sidebar.markdown("---")

# ==========================
# 🎉 Footer
# ==========================
st.markdown("---")
st.markdown("<h6 style='text-align: center;'>🚀 Powered by Rule-Based Matching | Hackathon Project</h6>", unsafe_allow_html=True)