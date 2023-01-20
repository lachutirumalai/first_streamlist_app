
import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError



streamlit.title('My Mom''s New Healthy Diner')

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


# import pandas
# Display the table on the page.
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

#create a repeatable code called function
def get_fruitvice_data(fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
  # Parse the JSON and read the text 
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized
    
# New section to display fruitvice api response
streamlit.header('Fruitvice Fruit Advice!')

try:
  
  #lets add a text input
  #import requests
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    streamlit.write('The user entered ', fruit_choice)
    back_from_function = get_fruitvice_data(fruit_choice)
    # Display the data in a tabular format
    streamlit.dataframe(back_from_function)

except URLError as e:
    streamlit.error()
    

streamlit.header("View Our Fruit List - Add your favorites!")
#snowflake related functions
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
       my_cur.execute("SELECT * from fruit_load_list")
       return my_cur.fetchall()
      
# Add a button to load the fruit
if streamlit.button('Get Fruit List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  my_cnx.close()
  streamlit.dataframe(my_data_rows)

#dont run anything while we troubleshoot
#streamlit.stop()
def insert_row_snowflake(new_fruit):
   with my_cnx.cursor() as my_cur:
        my_cur.execute("Insert into fruit_load_list values ('" + new_fruit +"')")
        return 'Thanks for adding ' + new_fruit

#lets add a text input
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a fruit to the list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_function = insert_row_snowflake(add_my_fruit)
  streamlit.text(back_from_function)
