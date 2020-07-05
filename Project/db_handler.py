# -------------------------------------------------------------------------------
# DbHandler
# -------------------------------------------------------------------------------
# A class to interact with the database
#-------------------------------------------------------------------------



# import logging so we can write messages to the log
import logging
# import operating system library
import os
#import DB library
import MySQLdb

# Database connection parameters 
DB_USER_NAME='group05'
DB_PASSWORD='hulhsyep'
DB_DEFALUT_DB='group05'

class DbHandler():
	def __init__(self):
		logging.info('Initializing DbHandler new')
		self.u_user=DB_USER_NAME
		self.u_password=DB_PASSWORD
		self.u_default_db=DB_DEFALUT_DB
		self.u_unixSocket='/cloudsql/dbcourse2015:mysql'
		self.u_charset='utf8'
		self.u_host='173.194.228.96'
		self.u_port=3306
		self.u_DbConnection=None

	def connectToDb(self):
                # make a connection to db
		logging.info('In ConnectToDb')
		# we will connect to the DB only once
		if self.u_DbConnection is None:
			env = os.getenv('SERVER_SOFTWARE')
			if (env and env.startswith('Google App Engine/')):
				#Running from Google App Engine
				logging.info('In env - Google App Engine')
				# connect to the DB
				self.u_DbConnection = MySQLdb.connect(
				unix_socket=self.u_unixSocket,
				user=self.u_user,
				passwd=self.u_password,
				charset=self.u_charset,
				db=self.u_default_db)
			else:
				#Connecting from an external network.
				logging.info('In env - Launcher')
				# connect to the DB
				self.u_DbConnection = MySQLdb.connect(
				host=self.u_host,
				db=self.u_default_db,
				port=self.u_port,
				user= self.u_user,
				passwd=self.u_password,
				charset=self.u_charset)

	def disconnectFromDb(self):
                # make a disconnection to db
		logging.info('In DisconnectFromDb')
		if self.u_DbConnection:
			self.u_DbConnection.close()
			
	def commit(self):
                # runing the action
		logging.info('In commit')
		if self.u_DbConnection:
			self.u_DbConnection.commit()			
			
	def getCursor(self):
                # get a cursor that pass over the db
		logging.info('In DbHandler.getCursor')
		self.connectToDb()
		return (self.u_DbConnection.cursor())
				


									  
