import streamlit as st
import pandas as pd
import numpy as np
import joblib

# ------------------ Page Config ------------------
st.set_page_config(page_title="Pokémon Battle Predictor", page_icon="⚔️", layout="wide")

# ------------------ Background wallpaper ------------------
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://imgs.search.brave.com/_o4F5Ua-3eNstipHsxMLQAByx7-BLFgibxErG_gY2zo/rs:fit:500:0:1:0/g:ce/aHR0cHM6Ly93YWxs/cGFwZXJzLWNsYW4u/Y29tL3dwLWNvbnRl/bnQvdXBsb2Fkcy8y/MDI1LzA2L3Bva2Vt/b24tcG9rZWJhbGwt/ZW5lcmd5LWJ1cnN0/LWRlc2t0b3Atd2Fs/bHBhcGVyLWNvdmVy/LmpwZw");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}
[data-testid="stHeader"] {
    background-color: rgba(0,0,0,0);
}
[data-testid="stToolbar"] {
    visibility: hidden;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# ------------------ Dropdown Styling ------------------
dropdown_style = """
<style>
div[data-baseweb="select"] > div {
    background-color: rgba(0, 0, 0, 0.5);
    border-radius: 10px;
    width: 300px;
}
div[data-baseweb="select"] span {
    color: #fff;
    font-weight: 700;
    font-size: 16px;
    letter-spacing: 0.5px;
}
</style>
"""
st.markdown(dropdown_style, unsafe_allow_html=True)

# ------------------ Label Styling ------------------
label_style = """
<style>
label {
    color: white !important;
    font-weight: bold;
    font-size: 20px;
    font-style: italic;
}
</style>
"""
st.markdown(label_style, unsafe_allow_html=True)

# ------------------ Battle Animation Styling ------------------
battle_animation_style = """
<style>
.battle-img {
    width: 200px;
    animation: shake 0.5s;
    animation-iteration-count: infinite;
}
@keyframes shake {
    0% { transform: translate(1px, 1px) rotate(0deg); }
    25% { transform: translate(-1px, -2px) rotate(-1deg); }
    50% { transform: translate(-3px, 0px) rotate(1deg); }
    75% { transform: translate(3px, 2px) rotate(0deg); }
    100% { transform: translate(1px, -1px) rotate(1deg); }
}
</style>
"""
st.markdown(battle_animation_style, unsafe_allow_html=True)

# ------------------ Load Data and Model ------------------
pokemon = pd.read_csv("C:/Users/shrey/Desktop/code/projects/Pokemon Winner/pokemon.csv")
model = joblib.load("C:/Users/shrey/Desktop/code/projects/Pokemon Winner/model.pkl")
scaler = joblib.load("C:/Users/shrey/Desktop/code/projects/Pokemon Winner/scaler.pkl")

# ------------------ Type Effectiveness Dictionary ------------------
type_effectiveness = {
    ('Fire','Grass'):2.0,('Grass','Fire'):0.5,
    ('Water','Fire'):2.0,('Fire','Water'):0.5,
    # ... complete as per your training
}

def get_type_effectiveness(attacking_type, defending_type):
    return type_effectiveness.get((attacking_type, defending_type), 1.0)

# ------------------ Title ------------------
st.markdown("""
    <h1 style='text-align: center; color: #FFD700; text-shadow: 2px 2px black; font-size: 50px;'>
        ⚔️ Pokémon Battle ⚔️
    </h1>
""", unsafe_allow_html=True)

st.markdown("""
    <h3 style='text-align: center; color: #FFD700;text-shadow: 2px 2px black ; font-style: italic;'>
        Select two Pokémon to see who will win in a battle
    </h3>
""", unsafe_allow_html=True)

# ------------------ Pokémon Dropdown Side by Side (centered next to each other) ------------------

# Create empty columns to center the dropdowns horizontally
spacer_left, col1, col_gap, col2, spacer_right = st.columns([2, 3, 0.5, 3, 2])

with col1:
    poke1_name = st.selectbox("Choose First Pokémon", pokemon['Name'].values, key="poke1")
with col2:
    poke2_name = st.selectbox("Choose Second Pokémon", pokemon['Name'].values, key="poke2")
# ------------------ Centered "Who will win?" Button ------------------
st.markdown("<br>", unsafe_allow_html=True)
button_col = st.columns([1,2,1])

with button_col[1]:
    predict_button = st.button("🔮 Who will win ?", use_container_width=True)

# ------------------ Prediction Logic ------------------
if predict_button:
    poke1_row = pokemon[pokemon['Name'] == poke1_name].iloc[0]
    poke2_row = pokemon[pokemon['Name'] == poke2_name].iloc[0]

    selected_columns = ['Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed', 'HP']
    diff_stats = poke1_row[selected_columns].values - poke2_row[selected_columns].values
    legendary_diff = int(poke1_row['Legendary']) - int(poke2_row['Legendary'])

    type_eff_1_vs_2 = get_type_effectiveness(poke1_row['Type 1'], poke2_row['Type 1'])
    type_eff_2_vs_1 = get_type_effectiveness(poke2_row['Type 1'], poke1_row['Type 1'])
    type_effectiveness_diff = type_eff_1_vs_2 - type_eff_2_vs_1

    input_df = pd.DataFrame([np.append(diff_stats, [legendary_diff, type_effectiveness_diff])],
                            columns=['Attack_diff', 'Defence_diff', 'Sp. Atk_diff', 'Sp. Def_diff',
                                     'Speed_diff', 'HP_diff', 'Legendary_diff', 'type_effectiveness_diff'])

    input_df_scaled = scaler.transform(input_df)
    pred = model.predict(input_df_scaled)
    winner = poke1_name if pred[0] == 0 else poke2_name

    # ------------------ Display Battle Simulation with VS ------------------
    st.markdown(f"""
        <div style='display: flex; justify-content: center; align-items: center; gap: 30px;'>
            <div style='text-align: center;'>
                <img src='https://img.pokemondb.net/artwork/{poke1_name.lower()}.jpg' class='battle-img'>
                <div style='color: #FFD700; font-weight: bold; font-size: 20px; margin-top: 5px;'>{poke1_name}</div>
            </div>
            <div style='font-size: 50px; font-weight: bold; color: red; text-shadow: 2px 2px black;'>VS</div>
            <div style='text-align: center;'>
                <img src='https://img.pokemondb.net/artwork/{poke2_name.lower()}.jpg' class='battle-img'>
                <div style='color: #FFD700; font-weight: bold; font-size: 20px; margin-top: 5px;'>{poke2_name}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # ------------------ Display Winner ------------------
    st.markdown(f"""
        <div style='display: flex; justify-content: center; align-items: center; height: 200px;'>
            <h2 style='
                font-size: 40px;
                background: -webkit-linear-gradient(#FFD700, #FF4500);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                text-align: center;
                text-shadow: 2px 2px black, 2px 2px white;
            '>
                🏆 Winner: {winner} 🏆
            </h2>
        </div>
    """, unsafe_allow_html=True)

    # ------------------ Stats Comparison ------------------
    with st.expander("📊 Show Stats Comparison"):
        stats_df = pd.DataFrame({
            'Stat': selected_columns,
            poke1_name: poke1_row[selected_columns].values,
            poke2_name: poke2_row[selected_columns].values
        })
        st.dataframe(stats_df, use_container_width=True)

# ------------------ Footer ------------------
st.markdown("---")
st.caption("Made by Sachin Mishra")
