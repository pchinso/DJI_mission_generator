import streamlit as st
from functions import mission_planning
from datetime import datetime
import ast


def today_str():

    today = datetime.today()
    formatted_date = today.strftime('%Y%m%d')
    
    return str(formatted_date)

def convert_string_to_list(string):
    try:
        # Safely evaluate the input string as a Python list
        result = ast.literal_eval(string)
        # Ensure that the result is a list
        if isinstance(result, list):
            return result
        else:
            raise ValueError("Input is not a valid Python list.")
    
    except (SyntaxError, ValueError) as e:
        raise ValueError("Input is not a valid string representation of a Python list.") from e

class StreamlitApp:
    def __init__(self):
        self.current_screen = None
        
        self.screens = [
        {
        'title': 'Input Coordinates',
        'header': 'Upload your .json coordinates files',
        'write': """Provide a coodinates files like this format,

                 { 
                   "Point_name": "Name", 
                   "long": -6.255055093404169, 
                   "lat": 37.44088650083901, 
                   "elev": 68.53300727087723 
                  }"""
                  ,
        'image': 'img/m200.jpeg',
        'image_caption': 'Matrice M200 v2',
        },
        {
        'title': 'About',
        'header': 'About Screen',
        'write': 'This is the about screen.',
        'image': 'img/m200.jpeg',
        'image_caption': 'About image',
        },
        {
        'title': 'Contact',
        'header': 'Contact Screen',
        'write': 'You can contact us at contact@example.com',
        'image': 'img/m200.jpeg',
        'image_caption': 'Contact image',
        },
        {
        'title': 'Send',
        'header': 'Send Results',
        'write': 'Sending results to contact@example.com',
        'image': '',
        'image_caption': 'No Image',
        },        
        ]

        self.radio_buttons = [screen['title'] for screen in self.screens]


        self.navigation = st.sidebar.radio("Select Screen", 
                                           self.radio_buttons
                                           )

    def run(self):

        # Main App Title
        st.title("DJI Mission Planner Tool for for Matrice M200 v2 as .klm")
        
        self.show_screen()
            


    def show_screen(self):

        # Index of actual navigation button selected
        screen_index = next((
        screen_index
        for screen_index, screen in enumerate(self.screens)
        if screen['title'] == self.navigation
        ), None)   

        # Shows screen data
        st.header(self.screens[screen_index]['header'])
        st.write(self.screens[screen_index]['write'])
        
        if self.screens[screen_index]['image'] != '':
            try:
                st.image(self.screens[screen_index]['image'], 
                        caption=self.screens[screen_index]['image_caption'],
                        )
                
            except FileNotFoundError:
                st.error("File not found. Please provide a valid file path.")      

        # Update current screen
        self.current_screen = self.navigation

        print(self.current_screen)

        if self.current_screen == self.screens[0]['title']:
            coordinates_file = st.file_uploader("Upload coordinates .json file", 
                                                type="json"
                                                )
            print('Uploaded: ', coordinates_file)

            if coordinates_file is not None:

                project_name = today_str()
                output_dir = str('/home/pcs/Documents/Python/DJI_mission_generator/' 
                                 + today_str() 
                                 + '_mission/'
                                 )

                project_name = st.text_input("Enter project name", project_name)
                output_dir = st.text_input("Enter project name", output_dir)

                altitude = int(st.text_input('Set mission altitude', '35'))
                
                gimbal = [-900,-450, -300, -150] 
                gimbal = convert_string_to_list(
                            st.text_input('Set mission gimbal inclinations', 
                                          '[-900,-450, -300, -150]'
                                          )
                            )

                heading = int(st.text_input('Set mission heading' , '0'))

                N_photos = int(st.text_input('Set mission number of photos' , len(gimbal)))

                # 'hover','gohome','autoland','gofirstpoint'
                onfinish = st.text_input('Set mission on finish action: (hover,gohome,autoland,gofirstpoint)', 
                                         'gohome'
                                         )
                
                speed = int(st.text_input('Set mission speed', '2'))

                turnmode = st.text_input('Set mission turnmode', 'Auto')

                over_time_before_picture = int(st.text_input('Set mission time before shoot' , '1'))

                if st.button("GENERATE MISSION"):
                    mission_planning.create_mission_for_DJI_Pilot(coordinates_file, 
                                                                  project_name, 
                                                                  output_dir,
                                                                  altitude,
                                                                  gimbal,
                                                                  heading,
                                                                  N_photos,
                                                                  onfinish,
                                                                  speed,
                                                                  turnmode,
                                                                  over_time_before_picture
                                                                  )

if __name__ == "__main__":

    app = StreamlitApp()
    app.run()