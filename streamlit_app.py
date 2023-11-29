import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omege 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avacado Toast')


streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#Import Data From S3 Bucket
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

#Set Fruit As Index
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
# Pre populate list to show example
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Apple', 'Banana'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

#Display table on page
streamlit.dataframe(fruits_to_show)

#New Section to Display FruityVice API Response
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")

# normalizes json response
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# Outputs it as table
streamlit.dataframe(fruityvice_normalized)

fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

# don't run anything past here while we troubleshoot
streamlit.stop()


my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list:")
streamlit.dataframe(my_data_rows)

fruit_to_add = streamlit.text_input('What fruit would you like to add?','Jackfruit')
streamlit.write('Thanks for adding ', fruit_to_add)


#This will not work correctly, but just go with it for now
my_cur.execute("insert into fruit_load_list values ('from streamlit')")
