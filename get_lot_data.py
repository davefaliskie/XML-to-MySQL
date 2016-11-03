import xmltodict, mysql.connector, datetime, urllib.request, time
import xml.etree.ElementTree as ET

def get_data():
  starttime = time.time()
  while True:
    unwrap_data()
    time.sleep(60.0 - ((time.time() - starttime) % 60.0))

 
def unwrap_data():
  r = urllib.request.urlopen("http://www.jmu.edu/cgi-bin/parking_get_sign_data.cgi")
  
  tree = ET.parse(r)
  root = tree.getroot()

  # https://docs.python.org/3/library/xml.etree.elementtree.html
  
  count = 0

  for child in root:
    for carparks in child:
      for levels in carparks:
        for level in levels:
          for signs in level:
            for sign in signs:
              # inside all the actual sign objects
              # print(sign.tag, sign.attrib)
              if count == 0 or count == 11 or count == 12:
                SignId = sign[0].text
                Display = sign[4].text
                LastUpdate = sign[5].text
                RetrievalTime = datetime.datetime.now()

                print ('********* New Entry *********')
                print (SignId) 
                print (Display) 
                print (LastUpdate)
                print (RetrievalTime)


                connect(SignId, Display, LastUpdate, RetrievalTime)

              count +=1

             
    

def connect(SignId, Display, LastUpdate, RetrievalTime):
  """ Connect to MySQL database """
  cnx = mysql.connector.connect(user='root', 
                                password='root',
                                host='127.0.0.1',
                                database='deck_data'
                                )

  cursor = cnx.cursor()

  add_data = ("INSERT INTO spots "
               "(SignId, Display, LastUpdate, RetrievalTime) "
               "VALUES (%s, %s, %s, %s)")

  data = (SignId, Display, LastUpdate, RetrievalTime)

  cursor.execute(add_data, data)
  print ("Data Was Successfully Entered!")


  cnx.commit()
  cursor.close()
  cnx.close()
 
 
if __name__ == '__main__':
    get_data()



