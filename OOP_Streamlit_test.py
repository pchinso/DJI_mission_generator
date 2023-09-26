import streamlit as st

class StreamlitApp:
    def __init__(self):
        self.current_screen = None
        self.screens = ["Home", 
                        "About", 
                        "Contact",
                        ]
        
        self.screens = [
        {
        'title': 'Home',
        'header': 'Home Screen',
        'write': 'Welcome to the home screen!',
        'image': 'images/Me_profile_pic.jpeg',
        'image_caption': 'Home image',
        },
        {
        'title': 'About',
        'header': 'About Screen',
        'write': 'This is the about screen.',
        'image': 'images/Me_profile_pic.jpeg',
        'image_caption': 'About image',
        },
        {
        'title': 'Contact',
        'header': 'Contact Screen',
        'write': 'You can contact us at contact@example.com',
        'image': 'images/Me_profile_pic.jpeg',
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
        st.title("Object-Oriented Streamlit App")
        
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
                        caption=self.screens[screen_index]['image_caption']
                        )
                
            except FileNotFoundError:
                st.error("File not found. Please provide a valid file path.")      

            
        # Update current screen
        self.current_screen = self.navigation
        
if __name__ == "__main__":

    app = StreamlitApp()
    app.run()