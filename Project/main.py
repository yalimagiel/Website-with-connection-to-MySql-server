# ------------------------------------------------------
# Find a match for a dog walker
# ------------------------------------------------------
# The application is designed to find a match between a dog owner and a dog walker.
# In order to find the match, the dog owner will enter to our site.
# On our site he will be required to complete his details and his dog details.
# The details include, among other things, the owner's city of residence, his type of dog and which day  he prefer to find a dog walker
# If there is a match, we will return the relevant dog walker.
# Otherwise, we will tell the owner that there is no match.
# ------------------------------------------------------


#import importent classes
import webapp2
import jinja2
# import operating system library
import os
# import logging so we can write messages to the log
import logging
from google.appengine.api import users
jinja_environment = jinja2.Environment(        loader=
                                                                                                                                                                jinja2.FileSystemLoader(os.path.dirname(__file__)))

# import the class userclient
import userclient
# import the class walker_finder
import walker_finder


# -------------------------------------------------------------
# Class of Welcome Page.
# the class checks if the user is already logged in
# -------------------------------------------------------------
class Welcome(webapp2.RequestHandler):
    # When we receive an HTTP GET request - 
    def get(self):
        user = users.get_current_user()
        # Create an Email object
        useremail=userclient.Email()
        # We will save the user email in variable
        useremail.u_Email=user.email()
        # Using CompareToDbOwner function
        compareEmail=useremail.CompareToDbOwner()
        # Cheking if the user already logged in
        if compareEmail=="" or compareEmail ==None or compareEmail==0 or compareEmail== 'Null' or len(compareEmail)==0:
            # The user didn't log in
            # display the Welcome Page
            template = jinja_environment.get_template('page_welcome.html')
            self.response.write(template.render())

        else:
            # The user logged in
            # send to the Show All Walkers page
            self.redirect('/Show_All_Walkers')



# ----------------------------------------------
# Display the registration form 
# ----------------------------------------------        
class Get_Owner_Inputs(webapp2.RequestHandler):

    def get(self):
        my_city=userclient.City()
        # using SelectCityFromDb function to get a list of cities
        retrieved_city_list=my_city.SelectCityFromDb()
        # display the Get owner inputs page
        my_template = jinja_environment.get_template('get_owner_inputs.html')
        parameters_for_template = {'list_of_city': retrieved_city_list}
        self.response.out.write(my_template.render(parameters_for_template))
    

# -------------------------------------------------------------
# When we receive an HTTP POST request -
# we get the parameters from the post request, and
# insert to sql 
# The post method will be called when someone clicks
# submit button (send) in the get owner inputs form
# -------------------------------------------------------------
class GetInfo(webapp2.RequestHandler):

    def post(self):
        # Create an Users object
        owner=userclient.Users()
        currentuser = users.get_current_user()
        # We will save the user email in variable
        usergmail = currentuser.email()
        owner.u_Owner_Email = usergmail
        #Request data from the POST request
        owner.u_OwnerName = self.request.get('OwnerName')
        owner.u_Owner_Phone = self.request.get('Phone_Number')
        owner.u_OwnerCity = self.request.get('City')
        owner.u_Dog_Name = self.request.get('DogName')
        owner.u_Dog_Sex = self.request.get('gender')
        owner.u_DogType = self.request.get('Type')
        # allow the Dog Owner to choose more than one day
        owner.u_PreferDayForTrip = self.request.get('days', allow_multiple=True)
        # using insertToDbOwnerAndDog function to insert the data to sql
        owner.insertToDbOwnerAndDog()
        # send to the Show All Walkers page
        self.redirect('/Show_All_Walkers')
        logging.info('Show_All_Walkers.post()')
        

        


# --------------------------------------------------
# Display all the possible matches by matching query
# --------------------------------------------------        
class Show_All_Walkers(webapp2.RequestHandler):

    def get(self):
        logging.info('Show_All_Walkers.get()')
        # Create an DogWalker object
        my_walker_finder=walker_finder.DogWalker()
        # using FinderAllWalker function to get a list of the match walkers
        retrieved_walker_list=my_walker_finder.FinderAllWalker()
        logging.info('retrieved_walker_list')
        # checking if there is a possible match
        if len(retrieved_walker_list)==0:
            # there is no possible match
            # display the bad match page
            template = jinja_environment.get_template('bad_match.html')
            self.response.write(template.render())

        
        else:
            # there is a possible match
            # display the show all walkers page
            # with a table of the possible walkers
            my_template = jinja_environment.get_template('show_all_walkers.html')
            parameters_for_template = {'list_of_walkers': retrieved_walker_list}
            self.response.out.write(my_template.render(parameters_for_template))
        
        
# -------------------------------------------------------------
# When we receive an HTTP POST request -
# we get the parameters from the post request, and
# display the chosen walker
# The post method will be called when someone clicks
# submit button (send) in the show all walkers table
# -------------------------------------------------------------   
class Matchchecking (webapp2.RequestHandler):

    def post(self):
        # Create an DogWalker object
        walker=walker_finder.DogWalker()
        #Request data from the POST request
        # allow the Dog Owner to choose more than one dog walker from the list of the chosen one
        walker.u_chosen_walker = self.request.get('dogwalker', allow_multiple=True)
        # using getchosenwalker function to creat a list of the final chosen dog walker
        final_walker=walker.getchosenwalker()
        # checking if there is a relevant dog walker
        if len(final_walker)==0:
            # there is no relevant dog walker
            # display the bad match page
            template = jinja_environment.get_template('bad_match.html')
            self.response.write(template.render())
        else:
            # there is a relevant dog walker
            # display the good match page
            # with a message from the chosen walkers
            my_template = jinja_environment.get_template('good_match.html')
            parameters_for_template = {'final_walker_list': final_walker}
            self.response.out.write(my_template.render(parameters_for_template))


  
                                
# -------------------------------------------------------------
# Routing
# -------------------------------------------------------------
app = webapp2.WSGIApplication([ ('/welcome',     Welcome),
                                ('/',               Welcome),
                                ('/Get_Owner_Inputs', Get_Owner_Inputs),
                                                                                                                             
                                ('/GetInfo', GetInfo),
                                ('/Show_All_Walkers', Show_All_Walkers),
                                ('/Matchchecking', Matchchecking)],
                                                                                                                                                                
                                            debug=True)
