import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError


streamlit.title("My Mom's New Healthy Diner")
streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Bluberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free_Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🍓 Build Your Own Fruit Smoothie 🥝🍇')
#import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

#pick list to include fruits
fruit_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Banana', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruit_selected]

#display table on the page
streamlit.dataframe(fruits_to_show)

#repeatable code block
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

#New section to display fruity advice
streamlit.header('🍒 Fruityvice Fruit Advice 🍒')
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  streamlit.caption('information source: https://fruityvice.com/')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    fruit_choice_return = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(fruit_choice_return)

except URLError as e:
  streamlit.error()

streamlit.header('📃 View Our Fruit List - Add Your Favorites! 🌟')

#Snowflake related functions
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from fruit_load_list")
        return my_cur.fetchall()
    
#add button to load the fruit
if streamlit.button('Get Fruit List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    my_cnx.close()
    streamlit.dataframe(my_data_rows)
    
#allow end user to add fruit to the list
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into fruit_load_list values ('"+ new_fruit +"')")
        return 'Thanks for adding:' + new_fruit
    
add_my_fruit = streamlit.text_input("What fruit would you like add?")
if streamlit.button('Add a Fruit to the List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    snowflake_return = insert_row_snowflake(add_my_fruit)
    my_cnx.close()
    streamlit.text(snowflake_return)
    

    
#stop running while troubleshooting
streamlit.stop()

