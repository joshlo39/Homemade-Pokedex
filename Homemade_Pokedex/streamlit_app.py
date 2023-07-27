import streamlit as st
import pandas as pd
import numpy as np
import requests
import json 
import altair as alt
import Pokemon
import datetime
st.set_page_config(
    page_title="Homemade Pokedex",
    layout="wide",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://joshlopes.netlify.app/",
        'About':"Welcome to the Homemade Pokedoex! \n\n This is a simple app that allows you to search for a Pokemon and see its stats and where it can be found in the wild. \n\n Made by Josh Lopes"
    }
)

with open ("app.css") as f:
  st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)


st.markdown("<h1 style = text-align:center;>Homemade Pokedex</h1>", unsafe_allow_html=True)
st.sidebar.markdown("<h2 style = text-align:center;>Trainer's Info</h2>", unsafe_allow_html=True)
name = st.sidebar.text_input("What is your Trainer Name?")
if name: 
    st.sidebar.success("Hello " + name.capitalize()+ " welcome to your own homemade pokedex!")
trainerAge = st.sidebar.slider("How old are you?", 10, 100, 20)
version = st.sidebar.selectbox("What version of Pokemon do you play?",[
        "HeartGold","SoulSilver","Platinum",
        "Diamond","Pearl","Black","White","Black 2",
        "White 2","X","Y","Omega Ruby","Alpha Sapphire"
        ,"Sun","Moon","Ultra Sun","Ultra Moon","Sword","Shield"
    ])
startDate = st.sidebar.date_input("When did you start playing Pokemon?", datetime.date(2019, 7, 6))

favoritePokemon = st.sidebar.radio("Who is your favorite first generation Pokemon Starter?",("Squirtle", "Bulbasaur", "Charmander"))


favoritePokemon = Pokemon.Pokemon(favoritePokemon) #default pokemon
listOfPokemon = Pokemon.Pokemon.get_list_of_all_pokemon()

selectedPokemon = st.selectbox("What Pokemon do you want to search for?", listOfPokemon)

if not selectedPokemon:
    st.warning("Please enter a Pokemon name")
selectedPokemon = Pokemon.Pokemon(selectedPokemon)
col1,col2,col3= st.columns([1.5,1,1])
with col2: #Pokemon Description
    type1html = f'<span class="icon type-{selectedPokemon.type1.lower()}">{selectedPokemon.type1.capitalize()}</span>'
    if selectedPokemon.get_number_of_types() == 2 :
        type2html = f'<span class="icon type-{selectedPokemon.type2.lower()}">{selectedPokemon.type2.capitalize()}</span>'
    st.markdown("<h5>Type:</h5>", unsafe_allow_html=True)
    if selectedPokemon.get_number_of_types() == 2:
        st.markdown(f"<h2>{type1html} {type2html}</h2>", unsafe_allow_html=True)
    else:
        st.markdown(f"<h2>{type1html}</h2>", unsafe_allow_html=True)
    st.markdown("<h5 style = margin-bottom:0px;>Height:</h5>", unsafe_allow_html=True)
    st.markdown(f"<h2>{selectedPokemon.height}m</h2>", unsafe_allow_html=True)
    st.markdown("<h5 style = margin-bottom:0px;>Weight:</h5>", unsafe_allow_html=True)
    st.markdown(f"<h2>{selectedPokemon.weight} kg</h2>", unsafe_allow_html=True)

   
with col1: #Picture of Pokemon
    #st.subheader(selectedPokemon.name.capitalize() + " #"+ str(selectedPokemon.id))
    st.markdown(f"<h2 style = text-align:center;>{selectedPokemon.name.capitalize()} #{selectedPokemon.id}</h2>", unsafe_allow_html=True)
    pokemon_image = selectedPokemon.pictureFront
    st.image(pokemon_image, width=None, use_column_width=True)
with col3: #Pokemon Description
    abilities = selectedPokemon.get_list_of_abilities()
    st.markdown("<h5 style = margin-bottom:0px;>Abilities:</h4>", unsafe_allow_html=True)
    for ability in abilities:
        st.markdown(f"<h2>{ability.capitalize()}</h3>", unsafe_allow_html=True) 
    st.markdown("<h5 style = margin-bottom:0px;>Evolves to:</h5>", unsafe_allow_html=True)
    st.markdown("<h2>" + selectedPokemon.get_evolution().capitalize() + "</h2>", unsafe_allow_html=True)
    st.markdown("<h5 style = margin-bottom:0px;>At Level: </h5>", unsafe_allow_html=True)
    st.markdown("<h2>" + selectedPokemon.get_evolution_level() + "</h2>", unsafe_allow_html=True)
    
    
    
        
        
#------------------Bar Chart-----------------
st.markdown(f"<h2 style = text-align:center;>{selectedPokemon.name.capitalize()}'s stats</h3>", unsafe_allow_html=True)
df = pd.read_csv("pokemon.csv")
pokemonStats = df[df["Name"] == selectedPokemon.name.capitalize()]
pokemonHp = pokemonStats["HP"].values[0]
pokemonAttack = pokemonStats["Attack"].values[0]
pokemonDefense = pokemonStats["Defense"].values[0]
pokemonSpAtk = pokemonStats["Sp. Atk"].values[0]
pokemonSpDef = pokemonStats["Sp. Def"].values[0]
pokemonSpeed = pokemonStats["Speed"].values[0]

#--------------bar chart for all pokemon stats-----------------
barChartData = pd.DataFrame({
    'Pokemon Stats Data': [pokemonHp, pokemonAttack,pokemonDefense,pokemonSpAtk,pokemonSpDef,pokemonSpeed],
    'Pokemon Stats': ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']
}
)
bar_chart = alt.Chart(barChartData).mark_bar().encode(
    x = 'Pokemon Stats',
    y = 'Pokemon Stats Data'
)
st.altair_chart(bar_chart, use_container_width=True)

if st.button("More stats"): 
    st.dataframe(pokemonStats)



pokemonGo_map = st.checkbox("Show " +selectedPokemon.name.capitalize() + "'s PokemonGo locations")
if pokemonGo_map:
    #------------------Map of location's to find selected pokemon in pokemonGo-----------------
    st.markdown(f"<h2 style = text-align:center;>{selectedPokemon.name.capitalize()}'s locations</h3>", unsafe_allow_html=True)
    locations = selectedPokemon.find_latAndLong_from_dataset()
    locationData = pd.DataFrame({
        'latitude': locations[0],
        'longitude': locations[1]
    })
    st.map(locationData)
    st.caption("This is the map of locations to find " + selectedPokemon.name.capitalize() + " in PokemonGo")

#----Interactive table of the selected pokemon's abilities----
st.markdown("<h2 style = text-align:center;>Compare Pokemons</h2>", unsafe_allow_html=True)
secondPokemon = st.selectbox("What is the second Pokemon you want to compare?", listOfPokemon)
if not secondPokemon:
    st.warning("Please enter a Pokemon name")
secondPokemon = Pokemon.Pokemon(secondPokemon)
col1,col2= st.columns(2)
with col1: 
    firstPokemonStats = np.array(selectedPokemon.get_list_of_stats())
    first_chart_data = {
        selectedPokemon.name.capitalize(): firstPokemonStats}
    df_first_pokemon = pd.DataFrame(first_chart_data, index=['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed'])
    st.area_chart(df_first_pokemon)
with col2:
    secondPokemonStats = np.array(secondPokemon.get_list_of_stats())
    second_chart_data = {
        secondPokemon.name.capitalize(): secondPokemonStats
    }
    df_second_pokemon = pd.DataFrame(second_chart_data, index=['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed'])
    st.area_chart(df_second_pokemon)



