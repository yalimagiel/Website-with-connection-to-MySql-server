# -------------------------------------------------------------------------------
# Walker Finder
# -------------------------------------------------------------------------------
# A class to find a match between the Walker and the Owner in the DB
#-------------------------------------------------------------------------


# import logging so we can write messages to the log
import logging
# import the class DbHandler to interact with the database
import db_handler
from google.appengine.api import users


class DogWalker():
    def __init__(self):
        logging.info('Initializing DogWalker')
        self.u_DbHandler=db_handler.DbHandler()

        # create data members of the class WalkerFinder
        self.u_Walker_Email_Adress = ""
        self.u_WalkerName=""
        self.u_Phone_Number=""
        self.u_City=""
        self.u_Daily_Price=""
        self.u_Daily_Shift=""
        self.u_chosen_walker=""
        self.u_RetrievedWalkerList=[]
        self.u_NumberOfRows=0
        self.u_the_chosen_walker = ""
        self.u_the_chosen_day =""
        self.u_the_chosen_owner=""
        self.u_the_chosen_name_walker = ""
        
    #-----------------------------------------------------
    # finding all the walkers
    # that succeed the match query 
    #-----------------------------------------------------
    def FinderAllWalker(self):
        logging.info('In FinderAllWalker.getAllWalker')
        # connect to db
        self.u_DbHandler.connectToDb()
        # get a cursor
        cursor=self.u_DbHandler.getCursor()
        user = users.get_current_user()
        # We will save the user email in variable
        useremail = user.email()
        # match query - checks  the owner's city of residence,
        #his type of dog and which day  he prefers to find a dog walker
        sql =           """
                                                                select T1.Walker_Email_Adress, T1.WalkerName, T1.Phone_Number, T1.City, T1.Daily_Price, T1.Daily_Shift
from (select Dog_Owner.Owner_Email_Adress, Dog_Owner.City, Dog_Owner.DogType, Dog_Owner_Prefer_Day_For_Trip.Prefer_Day_For_Trip 
from Dog_Owner  , Dog_Owner_Prefer_Day_For_Trip
where (Dog_Owner.Owner_Email_Adress = Dog_Owner_Prefer_Day_For_Trip.Owner_Email_Adress)) as T2 left join 
(select Dog_Walker.Walker_Email_Adress, Dog_Walker.WalkerName, Dog_Walker.Phone_Number, Dog_Walker.City, Preferd_Type.DogType,
Dog_Walker_Daily_Shift.Daily_Shift, Dog_Walker_Daily_Shift.Daily_Price, Dog_Walker_Daily_Shift.Daily_Dog_Amount
from Dog_Walker , Preferd_Type , Dog_Walker_Daily_Shift
where (Dog_Walker.Walker_Email_Adress = Preferd_Type.Walker_Email_Adress) and 
(Dog_Walker_Daily_Shift.Walker_Email_Adress=Dog_Walker.Walker_Email_Adress)) as T1
on ( T1.city=T2.city and T1.DogType = T2.DogType and T2.Prefer_Day_For_Trip=T1.Daily_Shift)
where T2.Owner_Email_Adress=%s
                                                                """
        cursor.execute(sql, (useremail,))
        # return the number of rows the we got match query
        self.u_NumberOfRows = int(cursor.rowcount)
        logging.info("Number of records "+ str(self.u_NumberOfRows))
        walker_records=cursor.fetchall()
        logging.info(walker_records)
        # create a list of the walkers that succeed the match query 
        self.u_RetrievedWalkerList=[]
        # running over the option that we got from the match query
        for walker_record in walker_records:
            # create DogWalker object
            current_walker=DogWalker()
            if walker_record[0]==None:
                # there is no dog walker that succeed the match query
                continue
            else:
                current_walker.u_Walker_Email_Adress=walker_record[0]
                current_walker.u_WalkerName = walker_record[1]
                current_walker.u_Phone_Number = walker_record[2]
                current_walker.u_City = walker_record[3]
                current_walker.u_Daily_Price = walker_record[4]
                current_walker.u_Daily_Shift = walker_record[5]
                #append the relevant walker to the list of the walkers
                self.u_RetrievedWalkerList.append(current_walker)
        return self.u_RetrievedWalkerList

    #-----------------------------------------------------
    # creating a final list of walkers that available
    # and user hasn't already has already chosen
    # the walker with the specific day 
    #-----------------------------------------------------
    def getchosenwalker(self):
        logging.info('In WalkerFinder.getchosenwalker for Walker Name ')
        # connect to db
        self.u_DbHandler.connectToDb()
        # get a cursor
        cursor=self.u_DbHandler.getCursor()
        currentuser = users.get_current_user()
        # We will save the user email in variable
        usergmail = currentuser.email()
        # list of the selected dog walkers from the site
        list_from_html= (self.u_chosen_walker)
        # create a list the final selected dog walkers
        chosen_walkers =[]
        # running over the index of the selected list from the site 
        for indx in range(0,len(list_from_html)):
            # convert to string
            str_data=str(list_from_html[indx])
            logging.info(str_data)
            split_data = str_data.split(',')
            logging.info(split_data)
            # create a tuple that including the dog walker email and the chosen day
            tup = (split_data[0],split_data[1])
            # appending the tuple to the chosen dog walker list
            chosen_walkers.append(tup)
            
        

            
        logging.info(chosen_walkers)
        # create the final list
        final_list_walker=[]
        for chosen_walker in chosen_walkers:
            logging.info(chosen_walker[0])
            logging.info(chosen_walker[1])
            # checking if the walker has already jobs at the choosen day
            sql = """ select Walker_Email_Adress, Owner_Email_Adress, Working_Day
                        from Works
                        Where
                         exists (select Walker_Email_Adress,  Owner_Email_Adress, Working_Day
                        from Works
                        Where Walker_Email_Adress=%s and Working_Day=%s)
                        """
            cursor.execute(sql, (chosen_walker[0], chosen_walker[1]))
            is_work = cursor.fetchall()
            if len(is_work) != 0:
                # the walker has already jobs at the chosen day
                # checking if he is available for more jobs
                sql = """ select *
                        from Works
                        where Walker_Email_adress=%s and Working_Day=%s
                        group by Walker_Email_Adress, Working_Day
                        having count(Owner_Email_Adress)< (select Daily_Dog_Amount
                        from Dog_Walker_Daily_Shift
                        where Walker_Email_Adress=%s and Daily_Shift=%s)
                        """
                cursor.execute(sql, (chosen_walker[0], chosen_walker[1], chosen_walker[0], chosen_walker[1]))
                countersql = cursor.fetchall()
                logging.info(countersql)
            else:
                # the walker is available for the chosen job
                countersql = [1]
            # checking if the user has already chosen the walker with the specific day
            sql="""
                                                select Walker_Email_Adress, Owner_Email_Adress, Working_Day
                        from Works
                        Where
                         exists (select Walker_Email_Adress,  Owner_Email_Adress, Working_Day
                        from Works
                        Where Walker_Email_Adress=%s and Owner_Email_Adress = %s and Working_Day=%s)
                                                """
            cursor.execute(sql  ,(chosen_walker[0],usergmail, chosen_walker[1]))                                                                                          
            checking = cursor.fetchall()
            logging.info(checking)
            
            if len(countersql)>0 and len(checking)==0:
                # the walker is availabe to do the job
                # and user hasn't already sign to the chosen walker with the
                # specific day
                self.u_the_chosen_walker = chosen_walker[0]
                self.u_the_chosen_day = chosen_walker[1]
                self.u_the_chosen_owner = usergmail
                logging.info('p'+str(self.u_the_chosen_walker)+str(self.u_the_chosen_owner)+str(self.u_the_chosen_day))
                # insert the job information to the db
                sql="""
                                                INSERT INTO Works(Walker_Email_Adress, Owner_Email_Adress, Working_Day)
                        VALUES (%s,%s,%s)
                                                """
                cursor.execute(sql  ,(self.u_the_chosen_walker,self.u_the_chosen_owner, self.u_the_chosen_day))
                logging.info(self.u_the_chosen_walker,self.u_the_chosen_owner, self.u_the_chosen_day)
                self.u_DbHandler.commit()

                print_chosen=DogWalker()
                print_chosen.u_the_chosen_walker = chosen_walker[0]
                print_chosen.u_the_chosen_day = chosen_walker[1]

                #appendning the final chosen walker to the final list
                final_list_walker.append(print_chosen)
                
        self.u_DbHandler.disconnectFromDb()
        logging.info(final_list_walker)
        return final_list_walker
