import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My parents New Healthy Diner')

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
# Choose fruits by fruit name not by index numbers
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page
if len(fruits_to_show) == 0:
  streamlit.dataframe(my_fruit_list)
else:
  streamlit.dataframe(fruits_to_show)

#New Section to display Fruityvice API response
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    #import requests
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    #Take the JSON version of response and normalize it
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    #Output it the screen as a table
    streamlit.dataframe(fruityvice_normalized)

except URLError as e:
  streamlit.error()





# don't run anything past here while we troubleshoot
streamlit.stop()

#Importing of snowflake connector python from requirements.txt
#import snowflake.connector

#Selecting fruits from Snowflake table
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_cur.execute("SELECT * from fruit_load_list")
my_data_rows = my_cur.fetchall()
#streamlit.text("Hello from Snowflake:")
streamlit.header("My fruit load list contains:")
streamlit.dataframe(my_data_rows)

# Allow the end user to add a fruit to the list
add_my_fruit = streamlit.text_input('What fruit would you like information about?','jackfruit')
streamlit.write('Thanks for adding: ', add_my_fruit)

# This will not work correctly , but just go with it for now
my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values ('from streamlit')")
