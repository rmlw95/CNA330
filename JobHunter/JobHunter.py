# This script pulls from a job website and stores positions into a database. If there is a new posting it notifies the user.
# CNA 330
# Modified version of code originally written by Zachary Rubin, zrubin@rtc.edu
import mysql.connector, sys, json, urllib.request, os, time

# Global variable to assign name of table that will be manipulated:
table = "jobhunt"

# Connect to database - You may need to edit the connect function based on your local settings.
def connect_to_sql():
    conn = mysql.connector.connect(user='root', password='',
                                  host='127.0.0.1',
                                  database='cna330')
    return conn

# Create the table structure
def create_tables(cursor, newtable):
    ## Starter code was here before, more code has now been added
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {newtable} (id INT PRIMARY KEY AUTO_INCREMENT, type TEXT, url TEXT, created_at TEXT, company_url TEXT, location TEXT, title TEXT, description TEXT, how_to_apply TEXT, company_logo TEXT);")
    return

# Query the database. You should not need to edit anything in this function
def query_sql(cursor, query):
    cursor.execute(query)
    return cursor

# Add a new job
def add_new_job(cursor, newtable, jobdetails):
    ## Starter code was here before, more code has now been added
    #print(jobdetails['description'])
    # IGNORE ignores pre-existing values without the need to individually check each potentially redundant value.
    query = cursor.execute(f"INSERT IGNORE INTO {newtable} (type, url, created_at, company_url, location, title, description, how_to_apply, company_logo) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);", [jobdetails['type'], jobdetails['url'], jobdetails['created_at'], jobdetails['company_url'], jobdetails["location"], jobdetails['title'], jobdetails['description'].encode('unicode_escape'), jobdetails['how_to_apply'],jobdetails['company_logo']]) # jobdetails would be a list of values
    return cursor #query_sql(cursor, query)

# Check if new job
def check_if_job_exists(cursor, jobdetails):
    ## Starter code was here before, more code has now been added
    query = (f"SELECT {title} FROM {newtable}")
    return query_sql(cursor, query)

def delete_job(cursor, jobdetails):
    ## Starter code was here before, more code has now been added
    query = (f"DELETE FROM {newtable} WHERE title = {title};")
    return query_sql(cursor, query)

# Grab new jobs from a website
def fetch_new_jobs(arg_dict):
    # Code from https://github.com/RTCedu/CNA336/blob/master/Spring2018/Sql.py
    query = f"https://jobs.github.com/positions.json{arg_dict}"  ## Appends arguments from argdict.txt
    #print(query)
    jsonpage = 0
    try:
        contents = urllib.request.urlopen(query)
        response = contents.read()
        jsonpage = json.loads(response)
    except:
        pass
    return jsonpage

# Load a text-based configuration file
def load_config_file(filename):
    argument_dictionary = 0
    # Code from https://github.com/RTCedu/CNA336/blob/master/Spring2018/FileIO.py
    rel_path = os.path.abspath(os.path.dirname("FileIO.py"))
    file = 0
    file_contents = 0
    try:
        file = open(filename, "r")
        file_contents = file.read()
    except FileNotFoundError:
        print("File not found, it will be created.")
        file = open(filename, "w")
        file.write("")
        file.close()

    ## Added in information for argument dictionary
    return file_contents #argument_dictionary

# Main area of the code.
def jobhunt(arg_dict, cursor):
    # Fetch jobs from website
    jobpage = fetch_new_jobs(arg_dict)
    #print(jobpage)                 #debugger
    #print (json.loads(jobpage))    #debugger
    for job in jobpage:
        add_new_job(cursor, table, job)

    ## Add your code here to parse the job page

    ## Add in your code here to check if the job already exists in the DB

    ## Add in your code here to notify the user of a new posting

    ## EXTRA CREDIT: Add your code to delete old entries
    #cursor.execute(f"DROP TABLE {newtable};")

# Setup portion of the program. Take arguments and set up the script
# You should not need to edit anything here.
def main():
    # Connect to SQL and get cursor
    conn = connect_to_sql()
    cursor = conn.cursor()
    create_tables(cursor, table)
#   Failed attempt to fix a unicode parsing error because mySQL only supports a maximum of 3-byte characters:
#    cursor.execute("ALTER DATABASE cna330 CHARACTER SET 'utf8' COLLATE 'utf8_unicode_ci';")
#    conn.commit()      #debugger
    # Load text file and store arguments into dictionary
    arg_dict = load_config_file("argdict.txt")      #modifyed from 'sys.argv[1]' to '"argdict.txt"'
    while(1):
        jobhunt(arg_dict, cursor)
        time.sleep(3600) # Sleep for 1h

if __name__ == '__main__':
    main()
