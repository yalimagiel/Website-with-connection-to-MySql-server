# -------------------------------------------------------------------------------
# Users
# -------------------------------------------------------------------------------
# A class to manage the Users Details (the Owner Dog and his Dog) - create and save in the DB
#-------------------------------------------------------------------------


# import logging so we can write messages to the log
import logging
# import the class DbHandler to interact with the database
import db_handler

class Users():
    def __init__(self):
        logging.info('Initializing Users Details')
        self.u_DbHandler=db_handler.DbHandler()

        # create data members of the class Users
        self.u_Owner_Email = ""
        self.u_OwnerName = ""
        self.u_Owner_Phone = 0
        self.u_OwnerCity = ""
        self.u_Dog_Name = ""
        self.u_Dog_Sex = ""
        self.u_DogType = ""
        self.u_PreferDayForTrip = ""

    def insertToDbOwnerAndDog(self):
        # insert the data that the user posted to the db
        logging.info('In OwnerAndDog.insertToDb')
        # connect to db
        self.u_DbHandler.connectToDb()
        # get a cursor
        cursor=self.u_DbHandler.getCursor()
        logging.info(self.u_Owner_Email)
        # insert the user details to db
        sql =           """
                                                                INSERT INTO Dog_Owner(Owner_Email_Adress,OwnerName,Phone_Number,City,Dog_Name,Dog_Sex,DogType) 
                                                                VALUES(%s,%s,%s,%s,%s,%s,%s)
                                                                """
        cursor.execute( sql, 
                                                                (self.u_Owner_Email,self.u_OwnerName, self.u_Owner_Phone ,self.u_OwnerCity,self.u_Dog_Name,self.u_Dog_Sex,self.u_DogType))
        
        sql =           """
                                                                INSERT INTO Dog_Owner_Prefer_Day_For_Trip(Prefer_Day_For_Trip,Owner_Email_Adress) 
                                                                VALUES(%s ,%s)
                                                                """
        # for each day the owner choose
        # insert to db
        for day in self.u_PreferDayForTrip:
            cursor.execute( sql, 
                                                                     (day,self.u_Owner_Email))
        
        self.u_DbHandler.commit()
        self.u_DbHandler.disconnectFromDb()
        
        logging.info('insertToDbOwnerAndDog')
        return

# -------------------------------------------------------
# the Email calss checks if the user is already logged in
# -------------------------------------------------------
class Email():
    def __init__(self):
        logging.info('email')
        self.u_DbHandler=db_handler.DbHandler()

        # create data members of the class Email
        self.u_Email = ""


    def CompareToDbOwner(self):
        # the function checks if user exists
        logging.info('In Owner.insertToDb')
        self.u_DbHandler.connectToDb()
        cursor=self.u_DbHandler.getCursor()
        sql =           """
                                                                select Owner_Email_Adress
                                from Dog_Owner
                                where Owner_Email_Adress= %s 
                                                                """
        cursor.execute( sql, 
                                                                (str(self.u_Email),))
        self.u_owneremail = cursor.fetchall()
        self.u_DbHandler.commit()
        self.u_DbHandler.disconnectFromDb()
        logging.info(self.u_Email)
        return self.u_owneremail

# -------------------------------------------------------
# transfer list of cities from db to the html form 
# -------------------------------------------------------
class City():
    def __init__(self):
        logging.info('email')
        self.u_DbHandler=db_handler.DbHandler()

        # create data members of the class Email
        self.u_City = ""
        self.u_NumberOfRows = 0
        self.u_RetrievedCityList=[]


    def SelectCityFromDb(self):
        # connect to db
        self.u_DbHandler.connectToDb()
        # get a cursor
        cursor=self.u_DbHandler.getCursor()
        sql =           """
                            select *
                            from HomeTown
                            """
        cursor.execute(sql)
        self.u_NumberOfRows = int(cursor.rowcount)
        logging.info("Number of records "+ str(self.u_NumberOfRows))
        citys_records=cursor.fetchall()
        logging.info(citys_records)
        # create a list of all the cities from the db
        self.u_RetrievedCityList=[]
        for city_record in citys_records:
            # create City object
            current_city=City()
            if city_record[0]==None:
                # there is no city
                continue
            else:
                current_city.u_City=str(city_record[0])
                # appending the city to the list
                self.u_RetrievedCityList.append(current_city)
        self.u_DbHandler.disconnectFromDb()
        return self.u_RetrievedCityList
        
     


                                                                                                                                                  
