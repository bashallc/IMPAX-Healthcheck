#!/usr/bin/env python
# coding: utf-8

# In[10]:


#!/usr/bin/env python
# coding: utf-8

# In[17]:

#import the modules

import pymysql.cursors
import time
from selenium import webdriver
import numpy as np
from bs4 import BeautifulSoup
import pandas as pd






# In[18]:
#App server List Prefix

url_list = ['http://dc1apps1','http://dc1apps2','http://dc1apps3','http://dc1apps4','http://dc1apps5','http://dc1apps6']


pymysql.converters.encoders[np.float64] = pymysql.converters.escape_float
pymysql.converters.conversions = pymysql.converters.encoders.copy()
pymysql.converters.conversions.update(pymysql.converters.decoders)


# In[19]:

#Cycle through the different app servers

for i in url_list:
    url = i+ "/AgfaHC.healthcheck.Escrow/AuthenticationForm.aspx"
    url2 = i+ "/AgfaHC.healthcheck.Escrow/EscrowForm.aspx"
    print(url)
    browser = webdriver.PhantomJS('C:\\temp\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe')
    browser.set_window_size(1366, 768)
    browser.get(url)
    browser.find_element_by_id("Username").send_keys('your_username')
    browser.find_element_by_id("Password").send_keys('your_password')
    browser.find_element_by_id("ButtonLogin").click()
    time.sleep(5)
    html = browser.page_source
    if 'AgfaHC' in html:
        print("You're logged in!")
    else:
        print("Logging in failed.")


# In[21]:


#get the healthcheck statuses and remove the last 4 characters
    items = []
    soup = BeautifulSoup(html,'html.parser')
    img = soup.select('img')
    [items.append(p['src']) for p in img if p['src']]
    new_status = [(x.split('.',1)[0]) for x in items]

    
# In[22]:


#convert the html page to a dataframe list
    dfs = pd.read_html(html)
    df = dfs[0]
    

# In[23]:


#replace status with actual values
    se = pd.Series(new_status)
    df['Status'] = se.values


# In[24]:


#rename columns
    df.columns = ['old status','Service','Operation','Time','Comment','Status']


# In[25]:


#delet first column
    df = df.drop(df.columns[[0]],axis=1)


# In[26]:


#replace the . with a _ so it is easier to create/update SQL tables
    df['Service'] = df['Service'].str.replace('.','_')
    df = df.replace(np.nan,'', regex=True)


# In[27]:


#import the list of table names
    df.to_csv('healthcheck.csv')


# In[28]:


# covert series into two lists
    names = pd.read_csv('columns.csv')
    names = list(names.names)
    times = list(df.Time)


# In[29]:


#zip the lists together
    df2 = pd.DataFrame(list(zip(names,times)))


# In[30]:


    df3 = df.iloc[:,[0,4]]

    def database_input(df2,i):
        connection = pymysql.connect(host='ip_address',
                                     user='username',
                                     password='password'
                                     db='table_name'
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)






        with connection.cursor() as cursor:
                    # Create a new record
                    sql =  "INSERT INTO `MASTER` (`AgfaHC_BackOffice_Web_Services_CALL_SERVICE`, `AgfaHC_BackOffice_Web_Services_CONNECT_DBASE`,`AgfaHC_BackOffice_Web_Services_CONNECT_ADAM`, `AgfaHC_BackOffice_Web_Services_CONNECT_ODBC`, `AgfaHC_Connectivity_Web_Services_CALL_SERVICE`, `AgfaHC_Connectivity_Web_Services_CONNECT_DBASE`, `AgfaHC_Connectivity_Web_Services_CONNECT_ADAM`, `AgfaHC_Connectivity_Web_Services_ADAM_REP`, `AgfaHC_Connectivity_Web_Services_APP_CLUST`,`AgfaHC_Connectivity_Web_Services_CONNECT_ODBC`, `AgfaHC_Messaging_Server_WebServices_CALL_SERVICE`,`AgfaHC_Messaging_Server_WebServices_CONNECT_ADAM`, `AgfaHC_Messaging_Server_WebServices_MAP_SIGNAL`, `AgfaHC_Messaging_Server_WebServices_SIG_MESSAGE`, `AgfaHC_Pacs_Web_CALL_SERVICE`, `AgfaHC_Pacs_Web_CONNECT_DBASE`, `AgfaHC_Pacs_Web_CONNECT_ADAM`, `AgfaHC_Pacs_Web_CONNECT_ODBC`, `AgfaHC_Pacs_Web_CECHO`, `AgfaHC_Pacs_Web_Services_CALL_SERVICE`, `AgfaHC_Pacs_Web_Services_CONNECT_DBASE`,`AgfaHC_Pacs_Web_Services_CONNECT_ADAM`, `AgfaHC_Pacs_Web_Services_ADAM_REP`, `AgfaHC_Pacs_Web_Services_APPS`,`AgfaHC_Pacs_Web_Services_CONNECT_ODBC`, `AgfaHC_Ris_Web_Services_CALL_SERVICE`, `AgfaHC_Ris_Web_Services_DBASE_CONFIG`,`AgfaHC_Ris_Web_Services_OPEN_ECOMPASS`, `AgfaHC_Ris_Web_Services_CLOSE_ECOMPASS`,`AgfaHC_User_Administration_Web_Services_CALL_SERVICE`, `AgfaHC_User_Administration_Web_Services_CONNECT_DBASE`,`AgfaHC_User_Administration_Web_Services_CONNECT_ADAM`, `AgfaHC_User_Security_Web_Services_CALL_SERVICE`,`AgfaHC_User_Security_Web_Services_CONNECT_DBASE`, `AgfaHC_User_Security_Web_Services_CONNECT_ADAM`,`AgfaHC_User_Security_Web_Services_CERTS`, `AgfaHC_User_Security_Web_Services_LICENSE`, `AgfaHC_User_Web_Services_CALL_SERVICE`,`AgfaHC_User_Web_Services_CONNECT_DBASE`, `AgfaHC_User_Web_Services_CONNECT_ADAM`,`appserver`) VALUES (%s, %s,%s,%s,%s,%s,%s,%s, %s,%s,%s,%s,%s,%s,%s, %s,%s,%s,%s,%s,%s,%s, %s,%s,%s,%s,%s,%s,%s, %s,%s,%s,%s,%s,%s,%s, %s,%s,%s,%s,%s)"


                    cursor.execute(sql, (str(df2.iloc[0][1]),str(df2.iloc[1][1]),str(df2.iloc[2][1]),str(df2.iloc[3][1]),str(df2.iloc[4][1])
                                         ,str(df2.iloc[5][1]),str(df2.iloc[6][1]),str(df2.iloc[7][1]),str(df2.iloc[8][1]),str(df2.iloc[9][1])
                                         ,str(df2.iloc[10][1]),str(df2.iloc[11][1]),str(df2.iloc[12][1]),str(df2.iloc[13][1])
                                         ,str(df2.iloc[14][1]),str(df2.iloc[15][1]),str(df2.iloc[16][1]),str(df2.iloc[17][1])
                                         ,str(df2.iloc[18][1]),str(df2.iloc[19][1]),str(df2.iloc[20][1]),str(df2.iloc[21][1])
                                         ,str(df2.iloc[22][1]),str(df2.iloc[23][1]),str(df2.iloc[24][1]),str(df2.iloc[25][1])
                                         ,str(df2.iloc[26][1]),str(df2.iloc[27][1]),str(df2.iloc[28][1]),str(df2.iloc[29][1])
                                         ,str(df2.iloc[30][1]),str(df2.iloc[31][1]),str(df2.iloc[32][1]),str(df2.iloc[33][1])
                                         ,str(df2.iloc[34][1]),str(df2.iloc[35][1]),str(df2.iloc[36][1]),str(df2.iloc[37][1])
                                         ,str(df2.iloc[38][1]),str(df2.iloc[39][1]),str(i)))

                # connection is not autocommit by default. So you must commit to save
                # your changes.
                    connection.commit()

    

    


# In[32]:



    def database_input2(df2,i):
        connection = pymysql.connect(host='ip_address',
                                     user='username',
                                     password='password',
                                     db='table_name',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)






        with connection.cursor() as cursor:
                    # Create a new record

                    sql =  "INSERT INTO `STATUS` (`AgfaHC_BackOffice_Web_Services_CALL_SERVICE`, `AgfaHC_BackOffice_Web_Services_CONNECT_DBASE`,`AgfaHC_BackOffice_Web_Services_CONNECT_ADAM`, `AgfaHC_BackOffice_Web_Services_CONNECT_ODBC`, `AgfaHC_Connectivity_Web_Services_CALL_SERVICE`, `AgfaHC_Connectivity_Web_Services_CONNECT_DBASE`, `AgfaHC_Connectivity_Web_Services_CONNECT_ADAM`, `AgfaHC_Connectivity_Web_Services_ADAM_REP`, `AgfaHC_Connectivity_Web_Services_APP_CLUST`,`AgfaHC_Connectivity_Web_Services_CONNECT_ODBC`, `AgfaHC_Messaging_Server_WebServices_CALL_SERVICE`,`AgfaHC_Messaging_Server_WebServices_CONNECT_ADAM`, `AgfaHC_Messaging_Server_WebServices_MAP_SIGNAL`, `AgfaHC_Messaging_Server_WebServices_SIG_MESSAGE`, `AgfaHC_Pacs_Web_CALL_SERVICE`, `AgfaHC_Pacs_Web_CONNECT_DBASE`, `AgfaHC_Pacs_Web_CONNECT_ADAM`, `AgfaHC_Pacs_Web_CONNECT_ODBC`, `AgfaHC_Pacs_Web_CECHO`, `AgfaHC_Pacs_Web_Services_CALL_SERVICE`, `AgfaHC_Pacs_Web_Services_CONNECT_DBASE`,`AgfaHC_Pacs_Web_Services_CONNECT_ADAM`, `AgfaHC_Pacs_Web_Services_ADAM_REP`, `AgfaHC_Pacs_Web_Services_APPS`,`AgfaHC_Pacs_Web_Services_CONNECT_ODBC`, `AgfaHC_Ris_Web_Services_CALL_SERVICE`, `AgfaHC_Ris_Web_Services_DBASE_CONFIG`,`AgfaHC_Ris_Web_Services_OPEN_ECOMPASS`, `AgfaHC_Ris_Web_Services_CLOSE_ECOMPASS`,`AgfaHC_User_Administration_Web_Services_CALL_SERVICE`, `AgfaHC_User_Administration_Web_Services_CONNECT_DBASE`,`AgfaHC_User_Administration_Web_Services_CONNECT_ADAM`, `AgfaHC_User_Security_Web_Services_CALL_SERVICE`,`AgfaHC_User_Security_Web_Services_CONNECT_DBASE`, `AgfaHC_User_Security_Web_Services_CONNECT_ADAM`,`AgfaHC_User_Security_Web_Services_CERTS`, `AgfaHC_User_Security_Web_Services_LICENSE`, `AgfaHC_User_Web_Services_CALL_SERVICE`,`AgfaHC_User_Web_Services_CONNECT_DBASE`, `AgfaHC_User_Web_Services_CONNECT_ADAM`,`appserver`) VALUES (%s, %s,%s,%s,%s,%s,%s,%s, %s,%s,%s,%s,%s,%s,%s, %s,%s,%s,%s,%s,%s,%s, %s,%s,%s,%s,%s,%s,%s, %s,%s,%s,%s,%s,%s,%s, %s,%s,%s,%s,%s)"


                    cursor.execute(sql, (str(df2.iloc[0][1]),str(df2.iloc[1][1]),str(df2.iloc[2][1]),str(df2.iloc[3][1]),str(df2.iloc[4][1])
                                         ,str(df2.iloc[5][1]),str(df2.iloc[6][1]),str(df2.iloc[7][1]),str(df2.iloc[8][1]),str(df2.iloc[9][1])
                                         ,str(df2.iloc[10][1]),str(df2.iloc[11][1]),str(df2.iloc[12][1]),str(df2.iloc[13][1])
                                         ,str(df2.iloc[14][1]),str(df2.iloc[15][1]),str(df2.iloc[16][1]),str(df2.iloc[17][1])
                                         ,str(df2.iloc[18][1]),str(df2.iloc[19][1]),str(df2.iloc[20][1]),str(df2.iloc[21][1])
                                         ,str(df2.iloc[22][1]),str(df2.iloc[23][1]),str(df2.iloc[24][1]),str(df2.iloc[25][1])
                                         ,str(df2.iloc[26][1]),str(df2.iloc[27][1]),str(df2.iloc[28][1]),str(df2.iloc[29][1])
                                         ,str(df2.iloc[30][1]),str(df2.iloc[31][1]),str(df2.iloc[32][1]),str(df2.iloc[33][1])
                                         ,str(df2.iloc[34][1]),str(df2.iloc[35][1]),str(df2.iloc[36][1]),str(df2.iloc[37][1])
                                         ,str(df2.iloc[38][1]),str(df2.iloc[39][1]),str(i)))

                # connection is not autocommit by default. So you must commit to save
                # your changes.
                    connection.commit()

    
# In[31]:

    database_input(df2,i)
    database_input2(df3,i)

    browser.quit()
    
    print("close session :  ",url)


# In[ ]:



# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




