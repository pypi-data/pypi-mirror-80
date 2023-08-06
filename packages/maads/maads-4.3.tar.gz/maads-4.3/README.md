**Multi-Agent Accelerator for Data Science (MAADS)**

*Revolutionizing Data Science with Artificial Intelligence*

**Overview**

*MAADS combines Artificial Intelligence, Machine Learning and Natural Language Processing (with data engineering task automation) in one easy to use library, that allows clients to connect to the MAADS server located anywhere in the world and perform advanced analytics and embed intelligence in their organization seamlessly and fast!*

This library allows users to harness the power of agent-based computing using hundreds of advanced linear and non-linear algorithms. Users can easily integrate Predictive Analytics and Prescriptive Analytics in any solution by wrapping additional code around the functions below. It can also connect to **Apache KAFKA brokers** using the MAADS-VIPER functions in this library.  

VIPER is currently the only **KAFKA connector in the market that seamlessly combines Auto Machine Learning, with Real-Time Machine Learning, Real-Time Optimization and Real-Time Predictions** while publishing these insights in to a Kafka cluster in real-time at scale, while allowing users to consume these insights from anywhere, anytime and in any format.  We also provide management of algorithms and insights using our AiMS product integrated with VIPER and Kafka, to **help businesses reduce cloud compute and storage costs by tracking and controlling what algorithms are producing, and who is consuming these insights.**  If no one is consuming these insights, AiMS can **automatically deactivate** these algorithms thus STOPPING its use of storage and compute, saving organizations upto 20% in cloud costs. 

The system can:

- Automatically analyse your data and perform feature selection to determine which variables are more important than others.
- Automatically model your data for seasonality *Winter, Shoulder, and Summer seasons.*
- Automatically clean your data for outliers.
- Automatically make predictions using the BEST algorithm (out of hundreds of advanced algorithms) that best model your data.
- Connect to *Apache KAFKA brokers* (integrated with MAADS and HPDE) to create topics, produce data to topics, consume data, activate/deactivate topics, create consumer groups. list all brokers statistics, and more..
- Automatically optimize the optimal algorithms by MINIMIZING or MAXIMIZING them to find the **GLOBAL OPTIMAL VALUES** of the independent variables using nonlinear optimization with constraints
- Perform *Natural Language Processing (NLP)* on large amounts of text data - and get MAADS to summarize the text or apply deep learning for predictive outcomes. 
  For example, you can tell it to scrape a website, read a PDF, or text data and it will 
  return a concise summary.  This summary can be used to refine your modeling and give users  
  an integrated view of their business from a TEXT and ADVANCED ANALYTIC perspective.     
  Or, apply machine learning to text data for deeper insights - such as analysing
  help desk tickets and uncovering issues before they occur. Or, apply deep learning
  to security logs and uncover more anomalies or threats in your networks. 
- Do all this in minutes.

To install this library a request should be made to **support@otics.ca** for a username and a MAADSTOKEN.  Once you have these credentials then install this Python library.

**Compatibility**
    - Python 3.5 or greater
    - Minimal Python skills needed

**License**
   - Author: Sebastian Maurice, PhD
   - OTICS Advanced Analytics Inc.

**Installation**
   - At the command prompt write:
     **pip install maads**
     - This assumes you have [Downloaded Python](https://www.python.org/downloads/) and installed it on your computer.  

**Syntax**
  - There are literally two lines of code you need to write to train your data and make predictions:

**Main functions:**
   - **dotraining**
     Executes hundreds of agents, running hundreds of advanced algorithms and completes in minutes.  A master agent then chooses the BEST algorithm that best  models your data.
   - **dopredictions**
     After training, make high quality predictions - takes 1-2 seconds.
   - **hyperpredictions**
     After training, make high quality predictions - takes less than half a second (about ~100 milliseconds). Users can also generate predictions using **non-python code** such as JAVA.  Using the **maadshyperpredictions.CLASS** file, java apps can call the MAADS prediction server to return predictions very fast.  Other apps, using **any** other language, can also call the MAADS prediction server using standard TCP/IP client/server communication protocols like REST:  This gives MAADS users' the maximum flexibility to integrate MAADS predictions in any solution!  
	 
	 You can also use hyperpredictions as an API (Python not needed) and make calls from any application using the following format:
	 GET http://[maads server website]:[port]/[microserviceid]/?hyperpredict=[optimal algo key],[[input data]],[MAADSTOKEN]
	 
	 MAADS hyper-prediction can also be used in a MICROSERVICES architecture that utilize API gateways (reverse proxies).  This allows organizations to balance loads on the server and manage millions or billions of connections, to hyper-predictions, per day without experiencing latency issues.
	 
**Support functions:**

- **dolistkeys**
        - List all of the keys associated with the data you have analysed. 
- **dolistkeyswithkey**
        - List data associated with a single key.
- **dodeletewithkey**
        - Permanently delete all data associated with your key.
- **returndata**
        - Returns data from the string buffer.
- **getpicklezip**
        - Automatically downloads a ZIP file containing the optimal algorithms.  Users can modify the parameter estimates as they wish.
- **sendpicklezip**
        - Automatically upload a ZIP file containing the optimal algorithms to MAADS. The optimal algorithms will immediately take effect for predictions.
- **deploytoprod**
        - Automatically deploy the optimal algorithms to another MAADS server (i.e. production); MAADS will read the ZIP file, extract the algorithms and make all database updates.  This function is useful when your MAADS training server(s) and MAADS prediction server(s) are separate.  A powerful way to integrate MAADS in a distributed architecture is to automatically train your data, then deploy the optimal algorithms to some other server for predictions.  This is a great way to scale your analytics in a large (global) entreprise setting, seamlessly and fast, with MAADS!
- **algoinfo**
        - Get detailed information on the algorithm and other information.
- **genpdf**
        - Retrieve the PDF containing all of the detailed information on the algorithm and other information like model explanation and feature selection, etc.	
- **featureselectionjson**
        - Returns JSON collection of feature selection results for easier programmatic manipulation. Use dotraining feature selection switch to return a CSV file of 
		  feature selections.  This function conducts **unsupervised learning** and important part of model building.

**Optimization:**

- **optimize**
   - Automatically perform optimization of the optimal algorithms by minimizing or maximixing them to find optimal values for the independent variables:
       - MAADS offers a unique and powerful way to find the optimal values of the independent variables
       - Users can even minimize or maximize upto THREE optimal algorithms AT THE SAME TIME by building a multi-objective equation with the optimal algorithms
	   - By finding the optimal values of the independent variables you can "prescribe" the right combination of independent variables' values that will lead to the HIGHEST or LOWEST value for the optimal algorithms
	   - MAADS is one of the first technologies to offer a seamless integration between PREDICTIVE and PRESCRIPTIVE analytics.


**MAADS-VIPER Connector to Manage Apache KAFKA:** 
  - MAADS-VIPER python library connects to VIPER instances on any servers; VIPER manages Apache Kafka.  VIPER is REST based and cross-platform that can run on windows, linux, MAC, etc.. It also fully supports SSL/TLS encryption in Kafka brokers for producing and consuming.
  
- **viperlisttopics** 
  - List all topics in Kafka brokers
 
- **viperdeactivatetopic**
  - Deactivate topics in kafka brokers and prevent unused algorithms from consuming storage and computing resources that cost money 

- **viperactivatetopic**
  - Activate topics in Kafka brokers 

- **vipercreatetopic**
  - Create topics in Kafka brokers 
  
- **viperstats**
  - List all stats from Kafka brokers allowing VIPER and KAFKA admins with a end-end view of who is producing data to algorithms, and who is consuming the insights from the algorithms including date/time stamp on the last reads/writes to topics, and how many bytes were read and written to topics and a lot more

- **vipersubscribeconsumer**
  - Admins can subscribe consumers to topics and consumers will immediately receive insights from topics.  This also gives admins more control of who is consuming the insights and allows them to ensures any issues are resolved quickly in case something happens to the algorithms.
  
- **viperunsubscribeconsumer**
  - Admins can unsubscribe consumers from receiving insights, this is important to ensure storage and compute resources are always used for active users.  For example, if a business user leaves your company or no longer needs the insights, by unsubscribing the consumer, the algorithm will STOP producing the insights.

- **viperhpdetraining**
  - Users can do real-time machine learning (RTML) on the data in Kafka topics. This is very powerful and useful for "transactional learnings" on the fly using our HPDE technology.  HPDE will find the optimal algorithm for the data in less than 60 seconds.  

- **viperhpdepredict**
  - Using the optimal algorithm - users can do real-time predictions from streaming data into Kafka Topics.
  
- **viperhpdeoptimize**
  -  Users can even do optimization to MINIMIZE or MAXIMIZE the optimal algorithm to find the BEST values for the independent variables that will minimize or maximize the dependent variable.

- **viperproducetotopic**
  - Users can produce to any topics by injesting from any data sources.

- **viperconsumefromtopic**
  - Users can consume from any topic and graph the data. 
  
- **viperconsumefromstreamtopic**
  - Users can consume from a multiple stream of topics at once

- **vipercreateconsumergroup**
  - Admins can create a consumer group made up of any number of consumers.  You can add as many partitions for the group in the Kafka broker as well as specify the replication factor to ensure high availaibility and no disruption to users who consume insights from the topics.

- **viperconsumergroupconsumefromtopic**
  - Users who are part of the consumer group can consume from the group topic.

- **viperproducetotopicstream**
  - Users can join multiple topic streams and produce the combined results to another topic.
  
- **vipercreatejointopicstreams**
  - Users can join multiple topic streams
  
- **vipercreatetrainingdata**
  - Users can create a training data set from the topic streams for Real-Time Machine Learning (RTML) on the fly.

- **vipermodifyconsumerdetails**
  - Users can modify consumer details on the topic.  When topics are created an admin must indicate name, email, location and description of the topic.  This helps to better manage the topic and if there are issues, the admin can contact the individual consuming from the topic.
  
- **vipermodifytopicdetails**
  - Users can modify details on the topic.  When topics are created an admin must indicate name, email, location and description of the topic.  This helps to better manage the topic and if there are issues, the admin can contact the developer of the algorithm and resolve issue quickly to ensure disruption to consumers is minimal.
 
- **vipergroupdeactivate**
  - Admins can deactive a consumer group, which will stop all insights being delivered to consumers in the group.
  
- **vipergroupactivate**
  - Admins can activate a group to re-start the insights.
 
		
**Natural Language Processing (NLP):**

- **nlp**
   - Automatically perform NLP to summarize large amounts of text data.  Specifically, there are three data sources one can use:
       - **Website URL:** you can pass a URL to the NLP function and it will automatically scrape the site and return a summary of the text.
       - **PDF:** Send a PDF to be summarized.
       - **Text:** Paste text to be summarized.
       - This allows users to integrate NLP in unique and powerful ways with advanced analytics.

- **nlpgeosentiment**
   - Automatically perform NLP to summarize and find keywords for large amounts of twitter data and genenerate a sentiment score.  Users can perform
     GEO based searches on tweets within a specific radius.  This information could be very useful for risks and threats assessments.
	 
- **nlpaudiovideo**
   - Automatically extracts text from audio or video files.
       - This allows users to integrate text from audio and video in unique and powerful ways with machine learning (NLPCLASSIFY).
	   - Files must be .mp3, .mp4, .wav
	   - Users can specify how many seconds they want or get all of the recording.

- **nlpocr**
   - Automatically extracts text from image files.
       - This allows users to integrate text from images or scanned documents in unique and powerful ways with machine learning (NLPCLASSIFY).
	   - Files must be .jpg, .gif, .tiff, .png, .bmp, etc.

- **nlpclassify**
   - Automatically apply machine learning to predict outcomes from text data.  Specifically, MAADS will:
       - Preprocess text data and convert it to numeric vectors using over 50 Billion words to vector mappings plus custom mappings specific to your trained model
	   - Clean your text data by removing strange characters, punctuations, common words, lemmatize the words, etc..
	   - Convert the dependent category variable to labels.  
	   - If dependent variable is not categorical, you can tell MAADS not to convert the dependent variable.  This means you can regress TEXT data on NUMERIC data!
       - This function allows users to integrate NLP in unique and powerful ways with advanced analytics to text based systems like Help Desk or security platforms.

**First import the Python library.**

**import maads**

1. **maads.dotraining(MAADSTOKEN,CSV_local_file, feature_analysis, remove_outliers, has_seasonality, dependent_variable, maadsurl,throttle,theserverlocalname,summer,winter,shoulder,trainingpercentage,retrainingdays,retraindeploy,shuffle)**

**Parameters:**	

*MAADSTOKEN* : string, required

- A token given to you by MAADS administrator.

*CSV_local_file* : string, required

- A local comma-separated-file (csv) with Date in the first column.  Date must be MM/DD/YYYY format.  
- All other data must be numbers.

*feature_analysis* : int, required, 1 or 0

- If 1, then a feature analysis will be done on your data along with training.  If 0, no analysis is done. If -1, features will be generated, and downloaded to your local computer folder WITHOUT training.
    
*remove_outliers* : int, required, 1 or 0

- If 1, then outliers will be removed from your data.  If 0, no outliers are removed.

*has_seasonality* : int, required, 1 or 0
      
- If 1, then your data will be modeled for seasonality: Winter, Summer, Shoulder. If 0, then your data will 
  not be modeled for seasonality.  If modeling for seasonality, ensure you have enough data points that 
  covers the seasons, usually 1 year of data.

*dependent_variable* : string, required
       
- This is the dependent variable in your file.  All other variables will be modeled as independent variables.
       
*maadsurl* : string, required
       
- Indicate location of MAADS server.  You would have received this URL when you received your username and MAADSTOKEN. 

*throttle* : int, optional, Default=-1
       
- Indicates whether you want to throttle the data in the server. For example, if you are dealing with big data and facing memory limitations in the 
  server, then you can specify a smaller number of rows to use in the training process by specifying the number of rows in the throttle parameter.  

*theserverlocalname* : string, optional
       
- Indicates location of filename with full path in the server to use for training.  If this is specified, then CSV_local_file must be empty.

*summer* : string, optional

- Indicate summer months.  The default value is '6,7,8' for North America.  If you are analysing other continents you could change this value. 

*winter* : string, optional

- Indicate winter months.  The default value is '12,1,2,3' for North America.  If you are analysing other continents you could change this value. 

*shoulder* : string, optional

- Indicate shoulder months.  The default value is '4,5,9,10,11' for North America.  If you are analysing other continents you could change this value. 

*trainingpercentage* : number between 40 and 100, inclusive, optional

- Indicates how much of the complete data set to you as the Training data set. The default value is 75% or 75, the rest is used for test or validation.

*retrainingdays* : number, optional

- Indicates how many days to wait, from initial training, to re-train the model. This is convenient to automate re-training of models to take advantage of new data.  Default value is 0, for no re-training.

*retraindeploy* : number, 0 or 1, optional

- Indicates whether to deploy (retraindeploy=1) the optimal algorithm to a server (i.e. production) for immediate use after re-training. This assumes FTP server is listed in the MAADS lookup table. Default value is 0, for no deployment after re-training.

*shuffle* : number, 0 or 1, optional

- Indicates whether to shuffle the training dataset or not, default=0.

**Returns:** string buffer, PDF of Results, CSV of Prediction Data
        
- The string buffer contains the following sections:
        
- DATA: : This consists of the feature selection results
- PKEY: : This is the key to the BEST algorithm and must be used when making predictions.

			

**2. maads.dopredictions(MAADSTOKEN,attr,pkey,inputs,maadsurl)**

**Parameters:**	

*MAADSTOKEN* : string, required

- A token given to you by MAADS administrator.

*attr* : int, required

- This value should be 0.  It may change to other values in the future.

*pkey* : string, required

- This value must be retrieved from dotraining.  Note you can store PKEY after you have trained your file. 
  Training does not have to run before predictions, as training occurs more infrequently.

*inputs* : string, required
     
- This is a row of input data that must match the independent variables in your CSV. For example, if your 
  trained file is: Date, A, B, C, D and A is your dependent variable, then your inputs must be:
  Date, B, C, D
     
*maadsurl* : string, required
      
- Indicate location of MAADS server.  You would have received this URL when you received your username and MAADSTOKEN. 
	 
**Returns:** string buffer
        
- The string buffer contains the following sections:
        
  DATA: : This contains your prediction.

**3. maads.hyperpredictions(MAADSTOKEN,pkey,inputdata,host,port,use_reverse_proxy,microserviceid)**

**Parameters:**	

*MAADSTOKEN* : string, required

- A token given to you by MAADS administrator.
     
*pkey* : string, required
      
- This is the key to the optimal algorithm.

*inputdata* : string, required
      
- This is the input data for the optimal algorithm to produce a prediction.

*host* : string, required

- The host is the webserver that connects to the MAADS prediction server.  This will be provided by the MAADS administrator.

*port* : int, required

- This is the port that the MAADS prediction server listens on.  This will be provided by the MAADS administrator.  Note:  This will bypass any reverse proxy you are using.

*use_reverse_proxy* : int, optional, Default=0 for no reverse proxy
      
- For users that are using a reverse proxy to balance server load this can be set to 1. You will need to use the port that your proxy is listening on. Note: Your MAADS administrator will have this information.  A reverse proxy (or API Gateway) can be a very effective way to manage high loads on the server and route traffic accordingly.

*microserviceid* : string, optional, Default is empty.
      
- For users that are using a reverse proxy to balance server load and directing connection traffic to specific microservices listening on internal ports in the server then this should be provided.  Note: Your MAADS administrator will have this information as needed.  Using microservices with an API gateway is a very effective way to scale MAADS in a (global) enterprise environment.

**Returns:** json, prediction value
        
- The difference between doprediction and hyperpredictions is that do prediction returns 
        predictions in a few seconds, hyperpredictions returns predictions in milliseconds.  So if you require very fast predictions
		use hyperpredictions.  
  
**4. maads.returndata(thepredictions, section_attr)**

**Parameters:**	

*thepredictions* : string buffer

- This value is returned from dopredictions.

*section_attr* : string buffer

This value can be any one of the values:
        
- PKEY: : This returns the key from the dotraining function.  Note the semi-colon.
- DATA: : This returns the data from the dotraining or dopredictions functions.  Note the semi-colon.
- ALGO0: : This returns the BEST algorithm determined by MAADS - without seasonality.
- ACCURACY0: : This returns the forecast accuracy for the BEST algorithm - without seasonaility.
- SEASON0: : This returns allseason - for no seasonality.
- ALGO1: : This returns the BEST algorithm determined by MAADS for WINTER.
- ACCURACY1: : This returns the forecast accuracy for the BEST algorithm for WINTER.
- SEASON1: : This returns WINTER.
- ALGO2: : This returns the BEST algorithm determined by MAADS for SUMMER.
- ACCURACY2: : This returns the forecast accuracy for the BEST algorithm for SUMMER.
- SEASON2: : This returns SUMMER.
- ALGO3: : This returns the BEST algorithm determined by MAADS for SHOULDER season.
- ACCURACY3: : This returns the forecast accuracy for the BEST algorithm for SHOULDER season.
- SEASON3: : This returns SHOULDER.
        
**Returns:** string buffer
        
- The string buffer contains the prediction or the key or the feature analysis.
        
**5. maads.dodeletewithkey(MAADSTOKEN,pkey,maadsurl)**

**Parameters:**	

*MAADSTOKEN* : string, required

- A token given to you by MAADS administrator.

*pkey* : string buffer

- The key you want deleted.  This can be attained from dolistkeys function.

*maadsurl* : string, required
     
- Indicate location of MAADS server.  You would have received this URL when you received your username and MAADSTOKEN. 
	 
**Returns:** NULL
        
- Deletes all files and tables associated with the key permanently.
        
**6. maads.dolistkeys(MAADSTOKEN,maadsurl)**

**Parameters:**	

*MAADSTOKEN* : string, required

- A token given to you by MAADS administrator.

*maadsurl* : string, required
       
- Indicate location of MAADS server.  You would have received this URL when you received your username and MAADSTOKEN. 
	 
**Returns:** string buffer
        
- Lists all the keys associated with your MAADSTOKEN.
        
**7. maads.dolistkeyswithkey(MAADSTOKEN, pkey,maadsurl)**

**Parameters:**	

*MAADSTOKEN* : string, required

- A token given to you by MAADS administrator.

*pkey* : string buffer

- The key you want returned.

*maadsurl* : string, required
       
- Indicate location of MAADS server.  You would have received this URL when you received your username and MAADSTOKEN. 
	 
**Returns:** string buffer
        
- Returns the information (with independent variables) associated with your key.

        
**8. maads.getpicklezip(MAADSTOKEN,pkey,url,localfolder)**

**Parameters:**	

*MAADSTOKEN* : string, required

- A token given to you by MAADS administrator.

*pkey* : string buffer

- The key for the trained model.

*url* : string, required
       
- Indicate location of MAADS server.  This is the root location of the MAADS folder in the webserver. 

*localfolder* : string, required
       
- Indicates local folder location where file will be saved (i.e. C:/MAADS). Please use folder slashes.
	 
**Returns:** ZIP File
        
- This is a binary ZIP file and stored in the location of the localfolder.
        
**9. maads.sendpicklezip(MAADSTOKEN, pkey,url,localfilename)**

**Parameters:**	

*MAADSTOKEN* : string, required

- A token given to you by MAADS administrator.

*pkey* : string buffer

- The key for the trained model.

*url* : string, required
       
- Indicate location of MAADS PHP file in the webserver. 

*localfilename* : string, required
       
- Indicates local filename to be sent to the server. The file name should have a proper file format: key_DEPLOYTOPROD.zip 
	   
**Returns:** Server Response.
        
- The ZIP file will be stored and read by MAADS and all necessary changes will immediately take effect.
        
**10. maads.deploytoprod(MAADSTOKEN, pkey,url,localfilename,ftpserver,ftpuser,ftppass)**

**Parameters:**	

*MAADSTOKEN* : string, required

- A token given to you by MAADS administrator.

*pkey* : string buffer

- The key for the trained model.

*url* : string, required
       
- Indicate location of MAADS PHP file in the webserver. 

*localfilename* : string, optional
       
- Indicates local filename to be sent to the server. If indicating localfilename it must have a proper file format: key_DEPLOYTOPROD.zip 

*ftpserver* : string, optional
       
- Indicates ftp server you want to deploy the optimal algorithms to for predictions. If no FTP server is specified a default FTP server
  will used as listed on the MAADS server.  If none is listed this function will fail.
	   
*ftpuser* : string, optional
       
- Indicates ftp username to login to ftp server. If no FTP username is specified a default FTP username
  will used as listed on the MAADS server.

*ftppass* : string, optional
       
- Indicates ftp password to login to ftp server.  If no FTP password is specified a default FTP password
  will used as listed on the MAADS server.
	   
**Returns:** Server Response.
        
- The ZIP file will be stored and deployed to the MAADS PROD server (with FTP connection) and read by MAADS and all necessary changes will immediately take effect. The functions: dopredictions and hyperpredictions can immediately be used.

**11. maads.nlp(MAADSTOKEN,url,buffer,theserverfolder,wordcount,maxkeywords)**

**Parameters:**	

*MAADSTOKEN* : string, required

- A token given to you by MAADS administrator.

*url* : string, required
       
- Indicate location of MAADS PHP file in the webserver. 

*buffer* : string buffer, optional

- The data source to be summarized: URL, PDF, TEXT. If this is not specified, then theserverfolder cannot be empty.

*theserverfolder* : string buffer, optional

- This is a folder in the server that MAADS will read for files.  This is convenient when you do not want to transfer files to the server. If this is not specified, then buffer cannot be empty.

*wordcount* : int, required
       
- Indicates how many words you want returned. 

*maxkeywords* : int, optional, Default=10
       
- Indicates how many keywords you want returned. 

**Returns:** Two JSON objects separated by semi-colon.
        
- The first JSON are the extracted keywords in the text.  The second is the text summary.

**12. maads.nlpclassify(MAADSTOKEN,iscategory,maads_rest_url,csvfile,theserverlocalname,throttle,csvonly,
	username,trainingpercentage,retrainingdays,retraindeploy)**
    
**Parameters:**	

*MAADSTOKEN* : string, required

- A token given to you by MAADS administrator.

*iscategory* : int, required
       
- 1=Dependent Variable is a category, 0=Dependent variable is continuous

*maads_rest_url* : buffer, required
       
- Indicates the url for the MAADS training server with main PHP file.

*csvfile* : string buffer, optional

- The csvfile file to analyse.  The file must contain headers in the first row, and TWO columns: first column is the dependent variable (text or numeric), the 
  second column is text.  If this is not specified, then 

*theserverlocalname* : string buffer, optional

- The full path of the filename in the server that MAADS will read for training.  If this is empty, then csvfile must be specified.

*throttle* : int, optional, Default=-1
       
- Indicates whether you want to throttle the data in the server. For example, if you are dealing with big data and facing memory limitations in the 
  server, then you can specify a smaller number of rows to use in the training process by specifying the number of rows in the throttle parameter.  

*csvonly* : number, 0 or 1, optional, Default=0

- IF csvonly is set to 1, MAADS will return the converted file only in csv format.  This is convenient because nlpclassify can take several minutes for conversion and training, when a user may only want the converted file without the optimal algorithm.  Also, the converted file could be used as input into another model for training...especially when combining machine learning models that use only numeric data, and those using text data.

*username* : string, optional, Default=empty

- IF csvonly is set to 1, you must specify your username in the server.

*trainingpercentage* : number between 40 and 100, inclusive, optional

- Indicates how much of the complete data set to use as the Training data set. The default value is 75% or 75, the rest is used for test or validation.

*retrainingdays* : number, optional

- Indicates how many days to wait, from initial training, to re-train the model. This is convenient to automate re-training of models to take advantage of new data.  Default value is 0, for no re-training.

*retraindeploy* : number, 0 or 1, optional

- Indicates whether to deploy (retraindeploy=1) the optimal algorithm to a server (i.e. production) for immediate use after re-training. This assumes FTP server is listed in the MAADS lookup table. Default value is 0, for no deployment after re-training.
	   
**Returns:** Server Response.
        
- Key to the optimal algorithm used for predictions.  NOTE: This key must be used in the HYPERPREDICTION function only.


**13. maads.nlpaudiovideo(MAADSTOKEN,maads_rest_url,thefile,theserverfolder,duration,offset)**

**Parameters:**	

*MAADSTOKEN* : string, required

- A token given to you by MAADS administrator.

*maads_rest_url* : string, required
       
- Indicate location of MAADS PHP file in the webserver. 

*thefile* : string buffer, optional

- The data file to be analysed. If this is not specified, then theserverfolder cannot be empty.

*theserverfolder* : string buffer, optional

- This is a folder in the server that MAADS will read for files.  This is convenient when you do not want to transfer large audio/video files to the server. If this is not specified, then thefile cannot be empty.

*duration* : int, optional, Default=-1

- Specifies the number of seconds to play the audio for text extraction.  It defaults to playback of full recording.

*offset* : int, optional, Default=0

- Specifies the number of seconds to skip in the audio for text extraction.  It defaults to beginning of recording.

**Returns:** JSON object of summarized text.
        
- The JSON contains the text summary.


**14. maads.nlpocr(MAADSTOKEN,maads_rest_url,thefile,theserverfolder)**

**Parameters:**	

*MAADSTOKEN* : string, required

- A token given to you by MAADS administrator.

*maads_rest_url* : string, required
       
- Indicate location of MAADS PHP file in the webserver. 

*thefile* : string buffer, optional

- The data file to be analysed. If this is not specified, then theserverfolder cannot be empty.

*theserverfolder* : string buffer, optional

- This is a folder in the server that MAADS will read for files.  This is convenient when you do not want to transfer large image or scanned files to the server. If this is not specified, then thefile cannot be empty.

**Returns:** JSON object of summarized text.
        
- The JSON contains the text summary.


**15. maads.nlpgeosentiment(MAADSTOKEN,maads_rest_url,latitude,longitude,radius,searchterms,numtweets,wordcount)**

**Parameters:**	

*MAADSTOKEN* : string, required

- A token given to you by MAADS administrator.

*maads_rest_url* : string, required
       
- Indicate location of MAADS PHP file in the webserver. 

*latitude* : number, required

- The latitude of the search area.

*longitude* : number, required

- The longitude of the search area.

*radius* : number, required

- The radius of the search area - this will be in miles. For example, 200.

*searchterms* : string, required

- The terms to search for in the tweets. For example: "MAADS is Great,Python is awesome"

*numtweets* : int, optional. Default=50

- The number of tweets to search.

*wordcount* : int, optional. Default=300

- The number of words for the summary of the tweets.


*theserverfolder* : string buffer, optional

- This is a folder in the server that MAADS will read for files.  This is convenient when you do not want to transfer large image or scanned files to the server. If this is not specified, then thefile cannot be empty.

**Returns:** JSON object of summarized text.
        
- The JSON contains the text summary.


**16. maads.algoinfo(MAADSTOKEN,maads_rest_url,key,finddistribution)**

**Parameters:**	

*MAADSTOKEN* : string, required

- A token given to you by MAADS administrator.

*maads_rest_url* : string, required
       
- Indicates the url for the MAADS training server with main PHP file.

*key* : string, required

- The key to the optimal algorithm returned by dotraining function.

*finddistribution* : int, optional, Default=0

- Finds the distribution of the trained data.

**Returns:** JSON formatted information.
        
- The information contains all of the key details associated with the algorithm.


**17. maads.genpdf(MAADSTOKEN,maads_rest_url,key,urltomaadsserver,savetofolder)**

**Parameters:**	

*MAADSTOKEN* : string, required

- A token given to you by MAADS administrator.

*maads_rest_url* : string, required
       
- Indicates the url for the MAADS training server with main PHP file.

*key* : string, required

- The key to the optimal algorithm returned by dotraining function.

*urltomaadsserver* : string, required

- The website url to MAADS server.

*savetofolder* : string, required

- Your local folder names where you want the PDF saved.

**Returns:** PDF file.
        
- The PDF contains all of the key details associated with the algorithm.


**18. maads.featureselectionjson(MAADSTOKEN,maads_rest_url,key)**

**Parameters:**	

*MAADSTOKEN* : string, required

- A token given to you by MAADS administrator.

*maads_rest_url* : string, required
       
- Indicates the url for the MAADS training server with main PHP file.

*key* : string, required

- The key to the optimal algorithm returned by dotraining function.

**Returns:** JSON formatted information.
        
- The information contains all of the key details associated with feature selection.


**19. maads.optimize(MAADSTOKEN, maads_rest_url, algo1, ismin=1, objeq='1', a1cons=1, boundslimits='',
		forceupdate=0, algo2='', algo3='', a2cons=1,a3cons=1, iters=100, step=4, perc='min_0_max_0')**

**Parameters:**	

*MAADSTOKEN* : string, required

- A token given to you by MAADS administrator.

*maads_rest_url* : string, required
       
- Indicates the url for the MAADS training server with main PHP file.

*algo1* : string, required

- The optimal algo key to minimize or maximize - the optimal algorithm returned by dotraining function.

*algo2* : string, optional

- The optimal algo key to minimize or maximize - the optimal algorithm returned by dotraining function.

*algo3* : string, optional

- The optimal algo key to minimize or maximize - the optimal algorithm returned by dotraining function.

*ismin* : int, optional, default=1

- If ismin=1 then optimal algo will be minimized, if ismin=0 then it will be maximized.

*objeq* : string, optional, default='1'

- objeq is when you have a multi-objective optimal algorithms you want to maximize or minimize.  For example, if you want to minimize TWO optimal algorithms and you want an objective function= algo1 + algo2, then objeq=1,1.  If objective function=-algo1 - algo2 then objeq=-1,-1.  If objective function=-algo1 + algo2 + algo3 then objeq=-1,1,1, etc.  etc.  

*boundslimits* : string, default='none'
- Sets custom limits on the bounds of independent variable.  The lower and upper limit bounds can be for each variable or a subset of variable. The format must be the following:
 *variablename:[-1,0,1]:[lowervalue,equal,none]:[uppervalue,none]:[i,f]*
 
 - variablename is the name of your independent variable
 
 - [-1,0,1] must be ONE of -1,0,1.  -1 means values of variable name must be all negative, 0 means values can be negative or positive, 1 means values must be all positive
 
 - lowervalue is the lower bound on variable name or equal or none.  If 'equal' you must specify the value in the 'uppervalue' field.
 
 - uppervalue is the upper bound on variable name or none for no bound.  If no bound, MAADS will create a large value using the High value of variable.
 
 - [i,f] means i=integer, f=float, this allows users to specify the types of values for variables.
 
 For example:  If you have two variables named HOUR and MINUTE and you want to bound them, then you can specify:
 
 - *"hour:1:0:23,minute:1:0:59"* means hour is all positive, bounded between 0 and 23, AND minute is all positive bounded between 0 and 59.  You can also just specify
  
 - *"hour:1:none:none,minute:1:none:none"* means hour is all positive and minute is all positive. Or,  
 
 - *"hour:1:none:23,minute:1:0:none" means hour is all positive with no lower limit, and upper limit of 23, minute is all positive with lower limit of 0 and no upper limit.  

 - *"hour:1:equal:12,minute:1:0:59"* means hour will equal 12 (hour=12), AND minute is all positive bounded between 0 and 59.  You can also just specify
 
 - *Boundslimits* will give users maximum amount of flexibity when specifying bounds for constraints.
 
  *NOTE:* Variablename MUST match the variables that the model is trained on.  You can retrieve these EXACT names from the function: *maads.dolistkeyswithkey(MAADSTOKEN, pkey,maadsurl)*
 

*a1cons* : int, optional, default=1, can be 1,2,3,4

- a1cons specifies the bounds on the independent variables in the constraint equations for algo 1.  For example:

  - if a1cons=1, then MAADS will "USE MIN/MAX Of Variables For Bounds".  Specifically, min <= var <= max

  - if a1cons=2, then MAADS will "USE MEAN +/- STD Of Variables For Bounds". Specifically, mean-std <= var <= mean+std

  - if a1cons=3, then MAADS will "USE MIN/MAX +/- STD Of Variables For Bounds". Specifically, min-std <= var <= max+std

  - if a1cons=4, then MAADS will "USE MEDIAN +/- STD Of Variables For Bounds". Specifically, median-std <= var <= median+std

*a2cons* : int, optional, default=1, can be 1,2,3,4.  Only used if algo2 is specified.

- a2cons  specifies the bounds on the independent variables in the constraint equations for algo 2.  For example:

  - if a2cons=1, then MAADS will "USE MIN/MAX Of Variables For Bounds".  Specifically, min <= var <= max
  
  - if a2cons=2, then MAADS will "USE MEAN +/- STD Of Variables For Bounds". Specifically, mean-std <= var <= mean+std

  - if a2cons=3, then MAADS will "USE MIN/MAX +/- STD Of Variables For Bounds". Specifically, min-std <= var <= max+std

  - if a2cons=4, then MAADS will "USE MEDIAN +/- STD Of Variables For Bounds". Specifically, median-std <= var <= median+std

*a3cons* : int, optional, default=1, can be 1,2,3,4.  Only used if algo3 is specified.

- a3cons  specifies the bounds on the independent variables in the constraint equations for algo 3.  For example:

  - if a3cons=1, then MAADS will "USE MIN/MAX Of Variables For Bounds".  Specifically, min <= var <= max

  - if a3cons=2, then MAADS will "USE MEAN +/- STD Of Variables For Bounds". Specifically, mean-std <= var <= mean+std
 
  - if a3cons=3, then MAADS will "USE MIN/MAX +/- STD Of Variables For Bounds". Specifically, min-std <= var <= max+std

  - if a3cons=4, then MAADS will "USE MEDIAN +/- STD Of Variables For Bounds". Specifically, median-std <= var <= median+std

*forceupdate* : int, optional, default=0, can be 1, or 0

- forceupdate tells MAADS to update the optimal values.  If forceupdate=0, MAADS will decide if the NEW optimal values should replace the OLD optimal values.  Specifically, if you are maximizing an optimal algo and the new value is LOWER than old value, MAADS will NOT replace old value with new value, because the old value is better.  If forceupdate=1, MAADS will force an update regardless if the new value is better or worse than old value.


*iters* : int, optional, default=100, max=500
- Specifies the number of iterations to use in the optimization algorithms.

*step* : int, optional, default=3, can be 1,2,3,4
- Specifies how to generate the values of the independent variables for the constraint equations.  For example,

  - if step=1, then MAADS will use a uniform distribution bounded by the choices of a1cons, a2cons, a3cons, as applicable.

  - if step=2, then MAADS will use a Gaussian distribution bounded by the choices of a1cons, a2cons, a3cons, as applicable.

  - if step=3, then MAADS will combine uniform and Gaussian by averaging to create a distribution bounded by the choices of a1cons, a2cons, a3cons, as applicable.

  - if step=4, then MAADS will find values around an epsilon distance, using the standard deviation, around the values that have historically led to lowest or highest values depending on your optimization problem.

*perc* : string, optional, default='min_0_max_0' - 0 means 0%, values should be greater and equal to 0.
- Specifies by how much to "stretch" the bounds on the constraints.  For example, if "min_50_max_150", means to lower the MIN bound by 50%, and increase the MAX bound by 150%.  This allows users to specify any size of bounds. 


**Returns:** JSON formatted information.
        
- The information contains all of the key details associated with optimization including, value of the objective function, constraints, bounds, initial conditions, optimal values of independent variables, etc..


**20. maads.viperstats(vipertoken,host,port=-999,brokerhost='',brokerport=-999,microserviceid='')**

**Parameters:**	

*VIPERTOKEN* : string, required

- A token given to you by VIPER administrator.

*host* : string, required
       
- Indicates the url where the VIPER instance is located and listening.

*port* : int, required

- Port on which VIPER is listenting.


*brokerhost* : string, optional

- Address where Kafka broker is running - if none is specified, the Kafka broker address in the VIPER.ENV file will be used.


*brokerport* : int, optional

- Port on which Kafka is listenting.

*microserviceid* : string, optional

- If you are routing connections to VIPER through a microservice then indicate it here.

RETURNS: A JSON formatted object of all the Kafka broker information.

**21. maads.viperlisttopics(vipertoken,host,port=-999,brokerhost='', brokerport=-999,microserviceid='')**

**Parameters:**	

*VIPERTOKEN* : string, required

- A token given to you by VIPER administrator.

*host* : string, required
       
- Indicates the url where the VIPER instance is located and listening.

*port* : int, required

- Port on which VIPER is listenting.


*brokerhost* : string, optional

- Address where Kafka broker is running - if none is specified, the Kafka broker address in the VIPER.ENV file will be used.


*brokerport* : int, optional

- Port on which Kafka is listenting.

*microserviceid* : string, optional

- If you are routing connections to VIPER through a microservice then indicate it here.

RETURNS: A JSON formatted object of all the topics in the Kafka broker.


**22. maads.vipersubscribeconsumer(vipertoken,host,port,topic,companyname,contactname,contactemail,
		location,description,brokerhost='',brokerport=-999,groupid='',microserviceid='')**

**Parameters:**	

*VIPERTOKEN* : string, required

- A token given to you by VIPER administrator.

*host* : string, required
       
- Indicates the url where the VIPER instance is located and listening.

*port* : int, required

- Port on which VIPER is listenting.

*topic* : string, required

- Topic to subscribe to in Kafka broker

*companyname* : string, required

- Company name of consumer

*contactname* : string, required

- Contact name of consumer

*contactemail* : string, required

- Contact email of consumer

*location* : string, required

- Location of consumer

*description* : string, required

- Description of why consumer wants to subscribe to topic

*brokerhost* : string, optional

- Address of Kafka broker - if none is specified it will use broker address in VIPER.ENV file

*brokerport* : int, optional

- Port Kafka is listening on - if none is specified it will use port in the VIPER.ENV file

*groupid* : string, optional

- Subscribe consumer to group

*microserviceid* : string, optional

- If you are routing connections to VIPER through a microservice then indicate it here.

RETURNS: Consumer ID that the user must use to receive insights from topic.


**23. maads.viperunsubscribeconsumer(vipertoken,host,port,consumerid,brokerhost='',brokerport=-999,
	microserviceid='')**

**Parameters:**	

*VIPERTOKEN* : string, required

- A token given to you by VIPER administrator.

*host* : string, required
       
- Indicates the url where the VIPER instance is located and listening.

*port* : int, required

- Port on which VIPER is listenting.

*consumerid* : string, required
       
- Consumer id to unsubscribe

*brokerhost* : string, optional

- Address of Kafka broker - if none is specified it will use broker address in VIPER.ENV file

*brokerport* : int, optional

- Port Kafka is listening on - if none is specified it will use port in the VIPER.ENV file

RETURNS: Success/failure 

**24. maads.viperproducetotopic(vipertoken,host,port,topic,producerid,enabletls=0,delay=100,inputdata='',maadsalgokey='',
	maadstoken='',getoptimal=0,externalprediction='',brokerhost='',brokerport=-999,microserviceid='')**

**Parameters:**	

*VIPERTOKEN* : string, required

- A token given to you by VIPER administrator.

*host* : string, required
       
- Indicates the url where the VIPER instance is located and listening.

*port* : int, required

- Port on which VIPER is listenting.

*producerid* : string, required
       
- Topic to produce to in the Kafka broker

*enabletls* : int, optional
       
- Set to 1 if Kafka broker is enabled with SSL/TLS encryption, otherwise 0 for plaintext.

*delay*: int, optional

- Time in milliseconds from VIPER backsout from writing messages

*inputdata* : string, optional

- This is the inputdata for the optimal algorithm found by MAADS or HPDE

*maadsalgokey* : string, optional

- This should be the optimal algorithm key returned by maads.dotraining function.

*maadstoken* : string, optional
- If the topic is the name of the algorithm from MAADS, then a MAADSTOKEN must be specified to access the algorithm in the MAADS server

*getoptimal*: int, optional
- If you used the MAADS.OPTIMIZE function to optimize a MAADS algorithm, then if this is 1 it will only retrieve the optimal results in JSON format.

*externalprediction* : string, optional
- If you are using your own custom algorithms, then the output of your algorithm can be still used and fed into the Kafka topic.

*brokerhost* : string, optional

- Address of Kafka broker - if none is specified it will use broker address in VIPER.ENV file

*brokerport* : int, optional

- Port Kafka is listening on - if none is specified it will use port in the VIPER.ENV file

*microserviceid* : string, optional

- If you are routing connections to VIPER through a microservice then indicate it here.

RETURNS: Returns the value produced or results retrieved from the optimization.


**25. maads.viperconsumefromtopic(vipertoken,host,port,topic,consumerid,companyname,partition=-1,enabletls=0,delay=100,offset=0,
	brokerhost='',brokerport=-999,microserviceid='')**

**Parameters:**	

*VIPERTOKEN* : string, required

- A token given to you by VIPER administrator.

*host* : string, required
       
- Indicates the url where the VIPER instance is located and listening.

*port* : int, required

- Port on which VIPER is listenting.

*topic* : string, required
       
- Topic to consume from in the Kafka broker

*consumerid* : string, required

- Consumer id associated with the topic

*companyname* : string, required

- Your company name

*partition* : int, optional

- set to Kafka partition number or -1 to autodect

*enabletls*: int, optional

- Set to 1 if Kafka broker is SSL/TLS enabled for encrypted traffic, otherwise set to 0 for plaintext.

*delay*: int, optional

- Time in milliseconds before VIPER backsout from reading messages

*offset*: int, optional

- Offset to start the reading from..if 0 then reading will start from the beginning of the topic. If -1, VIPER will automatically go to the last offset.  Or, you 
  can extract the LastOffet from the returned JSON and use this offset for your next call.  

*brokerhost* : string, optional

- Address of Kafka broker - if none is specified it will use broker address in VIPER.ENV file

*brokerport* : int, optional

- Port Kafka is listening on - if none is specified it will use port in the VIPER.ENV file

*microserviceid* : string, optional

- If you are routing connections to VIPER through a microservice then indicate it here.

RETURNS: Returns a JSON object of the contents read from the topic.


**26. maads.viperhpdepredict(vipertoken,host,port,consumefrom,produceto,companyname,consumerid,producerid,
		hpdehost,enabletls=0,delay=100,hpdeport=-999,brokerhost='',brokerport=-999,timeout=120,usedeploy=0,
		microserviceid='')**

**Parameters:**	

*VIPERTOKEN* : string, required

- A token given to you by VIPER administrator.

*host* : string, required
       
- Indicates the url where the VIPER instance is located and listening.

*port* : int, required

- Port on which VIPER is listenting.

*consumefrom* : string, required
       
- Topic to consume from in the Kafka broker

*produceto* : string, required

- Topic to produce results of the prediction to

*companyname* : string, required

- Your company name

*consumerid*: string, required

- Consumerid associated with the topic to consume from

*producerid*: string, required

- Producerid associated with the topic to produce to

*hpdehost*: string, required

- Address of HPDE 

*enabletls*: int, optional

- Set to 1 if Kafka broker is SSL/TLS enabled for encryted traffic, otherwise 0 for plaintext.

*delay*: int, optional

- Time in milliseconds before VIPER backsout from reading messages

*hpdeport*: int, required

- Port number HPDE is listening on 

*brokerhost* : string, optional

- Address of Kafka broker - if none is specified it will use broker address in VIPER.ENV file

*brokerport* : int, optional

- Port Kafka is listening on - if none is specified it will use port in the VIPER.ENV file

*timeout* : int, optional

 - Number of seconds that VIPER waits when trying to make a connection to HPDE.

*usedeploy* : int, optional

 - If 0 will use algorithm in test, else if 1 use in production algorithm. 
 
*microserviceid* : string, optional

- If you are routing connections to VIPER through a microservice then indicate it here.

RETURNS: Returns a JSON object of the prediction.


**27. maads.viperhpdeoptimize(vipertoken,host,port,consumefrom,produceto,companyname,consumerid,producerid,
		hpdehost,enabletls=0,delay=100,hpdeport=-999,usedeploy=0,ismin=1,constraints='best',stretchbounds=20,
		constrainttype=1,epsilon=10,brokerhost='',brokerport=-999,timeout=120,microserviceid='')**

**Parameters:**	

*VIPERTOKEN* : string, required

- A token given to you by VIPER administrator.

*host* : string, required
       
- Indicates the url where the VIPER instance is located and listening.

*port* : int, required

- Port on which VIPER is listenting.

*consumefrom* : string, required
       
- Topic to consume from in the Kafka broker

*produceto* : string, required

- Topic to produce results of the prediction to

*companyname* : string, required

- Your company name

*consumerid*: string, required

- Consumerid associated with the topic to consume from

*producerid*: string, required

- Producerid associated with the topic to produce to

*hpdehost*: string, required

- Address of HPDE 

*enabletls*: int, optional

- Set to 1 if Kafka broker is SSL/TLS enabled for encrypted traffic, otherwise set to 0 for plaintext.

*delay*: int, optional

- Time in milliseconds before VIPER backsout from reading messages

*hpdeport*: int, required

- Port number HPDE is listening on 

*usedeploy* : int, optional
 - If 0 will use algorithm in test, else if 1 use in production algorithm. 

*ismin* : int, optional
- If 1 then function is minimized, else if 0 the function is maximized

*constraints*: string, optional

- If "best" then HPDE will choose the best values of the independent variables to minmize or maximize the dependent variable.  Users can also specify their own constraints for each variable and must be in the following format: varname1:min:max,varname2:min:max,...

*stretchbounds*: int, optional

- A number between 0 and 100, this is the percentage to stretch the bounds on the constraints.

*constrainttype*: int, optional

- If 1 then HPDE uses the min/max of each variable for the bounds, if 2 HPDE will adjust the min/max by their standard deviation, if 3 then HPDE uses stretchbounds to adjust the min/max for each variable.  

*epsilon*: int, optional

- Once HPDE finds a good local minima/maxima, it then uses this epsilon value to find the Global minima/maxima to ensure you have the best values of the independent variables that minimize or maximize the dependent variable.
					 
*brokerhost* : string, optional

- Address of Kafka broker - if none is specified it will use broker address in VIPER.ENV file

*brokerport* : int, optional

- Port Kafka is listening on - if none is specified it will use port in the VIPER.ENV file

*timeout* : int, optional

 - Number of seconds that VIPER waits when trying to make a connection to HPDE.

 
*microserviceid* : string, optional

- If you are routing connections to VIPER through a microservice then indicate it here.

RETURNS: Returns a JSON object of the optimization details and optimal values.


**28. maads.viperhpdetraining(vipertoken,host,port,consumefrom,produceto,companyname,consumerid,producerid,
                 hpdehost,hpdeport=-999,offset=0,islogistic=0,brokerhost='',brokerport=-999,timeout=120,
				 microserviceid='')**

**Parameters:**	

*VIPERTOKEN* : string, required

- A token given to you by VIPER administrator.

*host* : string, required
       
- Indicates the url where the VIPER instance is located and listening.

*port* : int, required

- Port on which VIPER is listenting.

*consumefrom* : string, required
       
- Topic to consume from in the Kafka broker

*produceto* : string, required

- Topic to produce results of the prediction to

*companyname* : string, required

- Your company name

*consumerid*: string, required

- Consumerid associated with the topic to consume from

*producerid*: string, required

- Producerid associated with the topic to produce to

*hpdehost*: string, required

- Address of HPDE 

*hpdeport*: int, required

- Port number HPDE is listening on 

*offset* : int, optional

 - If 0 will use the training data from the beginning of the topic
 
*islogistic*: int, optional

- If is 1, the HPDE will switch to logistic modeling, else continous.

*brokerhost* : string, optional

- Address of Kafka broker - if none is specified it will use broker address in VIPER.ENV file

*brokerport* : int, optional

- Port Kafka is listening on - if none is specified it will use port in the VIPER.ENV file

*timeout* : int, optional

 - Number of seconds that VIPER waits when trying to make a connection to HPDE.
 
*microserviceid* : string, optional

- If you are routing connections to VIPER through a microservice then indicate it here.

RETURNS: Returns a JSON object of the optimal algorithm that best fits your data.

**29. maads.viperproducetotopicstream(vipertoken,host,port,topic,producerid,offset,enabletls=0,delay=100,
	brokerhost='',brokerport=-999,microserviceid='')**

**Parameters:**	

*VIPERTOKEN* : string, required

- A token given to you by VIPER administrator.

*host* : string, required
       
- Indicates the url where the VIPER instance is located and listening.

*port* : int, required

- Port on which VIPER is listenting.

*topic* : string, required
       
- Topics to produce to in the Kafka broker - this is a topic that contains multiple topics, VIPER will consume from each topic and write results to the produceto topic

*producerid* : string, required

- Producerid of the topic producing to  

*offset* : int, optional
 
 - If 0 will use the stream data from the beginning of the topics, -1 will automatically go to last offset
 
*enabletls*: int, optional

- Set to 1 if Kafka broker is SSL/TLS enabled for encrypted traffic, otherwise 0 for plaintext

*delay*: int, optional

- Time in milliseconds before VIPER backsout from reading messages

*brokerhost* : string, optional

- Address of Kafka broker - if none is specified it will use broker address in VIPER.ENV file

*brokerport* : int, optional

- Port Kafka is listening on - if none is specified it will use port in the VIPER.ENV file
 
*microserviceid* : string, optional

- If you are routing connections to VIPER through a microservice then indicate it here.

RETURNS: Returns a JSON object of the optimal algorithm that best fits your data.

**30. maads.vipercreatetrainingdata(vipertoken,host,port,consumefrom,produceto,dependentvariable,
		independentvariables,consumerid,producerid,offset,companyname,enabletls=0,delay=100,maxrows=-1,
		brokerhost='',brokerport=-999,microserviceid='')**

**Parameters:**	

*VIPERTOKEN* : string, required

- A token given to you by VIPER administrator.

*host* : string, required
       
- Indicates the url where the VIPER instance is located and listening.

*port* : int, required

- Port on which VIPER is listenting.

*consumefrom* : string, required
       
- Topic to consume from 

*produceto* : string, required
       
- Topic to produce to 

*dependentvariable* : string, required
       
- Topic name of the dependentvariable 
 
*independentvariables* : string, required
       
- Topic names of the independentvariables - VIPER will automatically read the data streams 

*consumerid* : string, required

- Consumerid of the topic to consume to  

*producerid* : string, required

- Producerid of the topic producing to  

*offset* : int, optional

 - If 0 will use the stream data from the beginning of the topics
 
*companyname* : string, required

- Your company name  

*enabletls*: int, optional

- Set to 1 if Kafka broker is enabled for SSL/TLS encrypted traffic, otherwise set to 0 for plaintext.

*delay*: int, optional

- Time in milliseconds before VIPER backout from reading messages

*maxrows*: int, optional

- If -1, all data will be read from the topics - note this could slow down the training if there is a lot of data

*brokerhost* : string, optional

- Address of Kafka broker - if none is specified it will use broker address in VIPER.ENV file

*brokerport* : int, optional

- Port Kafka is listening on - if none is specified it will use port in the VIPER.ENV file
 
*microserviceid* : string, optional

- If you are routing connections to VIPER through a microservice then indicate it here.

RETURNS: Returns a JSON object of the training data set.

**31. maads.vipercreatetopic(vipertoken,host,port,topic,companyname,contactname,contactemail,location,
description,brokerhost='',brokerport=-999,numpartitions=1,replication=1,microserviceid='')**

**Parameters:**	

*VIPERTOKEN* : string, required

- A token given to you by VIPER administrator.

*host* : string, required
       
- Indicates the url where the VIPER instance is located and listening.

*port* : int, required

- Port on which VIPER is listenting.

*topic* : string, required
       
- Topic to create 

*companyname* : string, required

- Company name of consumer

*contactname* : string, required

- Contact name of consumer

*contactemail* : string, required

- Contact email of consumer

*location* : string, required

- Location of consumer

*description* : string, required

- Description of why consumer wants to subscribe to topic

*brokerhost* : string, optional

- Address of Kafka broker - if none is specified it will use broker address in VIPER.ENV file

*brokerport* : int, optional

- Port Kafka is listening on - if none is specified it will use port in the VIPER.ENV file

*numpartitions*: int, optional

- Number of the parititons to create in the Kafka broker - more parititons the faster Kafka will produce results.

*replication*: int, optional

- Specificies the number of brokers to replicate to - this is important for failover
 
*microserviceid* : string, optional

- If you are routing connections to VIPER through a microservice then indicate it here.

RETURNS: Returns a JSON object of the producer id for the topic.

**32. maads.viperconsumefromstreamtopic(vipertoken,host,port,topic,consumerid,companyname,partition=-1,
        enabletls=0,delay=100,offset=0,brokerhost='',brokerport=-999,microserviceid='')**

**Parameters:**	

*VIPERTOKEN* : string, required

- A token given to you by VIPER administrator.

*host* : string, required
       
- Indicates the url where the VIPER instance is located and listening.

*port* : int, required

- Port on which VIPER is listenting.

*topic* : string, required
       
- Topic to consume from 

*consumerid* : string, required

- Consumerid associated with topic

*companyname* : string, required

- Your company name

*partition*: int, optional

- Set to a kafka partition number, or -1 to autodetect partition.

*enabletls*: int, optional

- Set to 1 if Kafka broker is SSL/TLS enabled for encrypted traffic, otherwise set to 0 for plaintext.

*delay*: int, optional

- Time in milliseconds before VIPER backsout from reading messages

*offset* : int, optional

- Offset to start reading from ..if 0 VIPER will read from the beginning

*brokerhost* : string, optional

- Address of Kafka broker - if none is specified it will use broker address in VIPER.ENV file

*brokerport* : int, optional

- Port Kafka is listening on - if none is specified it will use port in the VIPER.ENV file
 
*microserviceid* : string, optional

- If you are routing connections to VIPER through a microservice then indicate it here.

RETURNS: Returns a JSON object of the contents of all the topics read


**33. maads.vipercreatejointopicstreams(vipertoken,host,port,topic,topicstojoin,companyname,contactname,contactemail,
		description,location,enabletls=0,brokerhost='',brokerport=-999,replication=1,numpartitions=1,microserviceid='')**

**Parameters:**	

*VIPERTOKEN* : string, required

- A token given to you by VIPER administrator.

*host* : string, required
       
- Indicates the url where the VIPER instance is located and listening.

*port* : int, required

- Port on which VIPER is listenting.

*topic* : string, required
       
- Topic to consume from 

*topicstojoin* : string, required

- Enter two or more topics separated by a comma and VIPER will join them into one topic

*companyname* : string, required

- Company name of consumer

*contactname* : string, required

- Contact name of consumer

*contactemail* : string, required

- Contact email of consumer

*location* : string, required

- Location of consumer

*description* : string, required

- Description of why consumer wants to subscribe to topic

*enabletls*: int, optional

- Set to 1 if Kafka broker is SSL/TLS enabled, otherwise set to 0 for plaintext.

*brokerhost* : string, optional

- Address of Kafka broker - if none is specified it will use broker address in VIPER.ENV file

*brokerport* : int, optional

- Port Kafka is listening on - if none is specified it will use port in the VIPER.ENV file

*numpartitions* : int, optional

- Number of partitions

*replication* : int, optional

- Replication factor

*microserviceid* : string, optional

- If you are routing connections to VIPER through a microservice then indicate it here.

RETURNS: Returns a JSON object of the producerid of the joined streams
								
**34. maads.vipercreateconsumergroup(vipertoken,host,port,topic,groupname,companyname,contactname,contactemail,
		description,location,brokerhost='',brokerport=-999,microserviceid='')**
**Parameters:**	

*VIPERTOKEN* : string, required

- A token given to you by VIPER administrator.

*host* : string, required
       
- Indicates the url where the VIPER instance is located and listening.

*port* : int, required

- Port on which VIPER is listenting.

*topic* : string, required
       
- Topic to dd to the group, multiple (active) topics can be separated by comma 

*groupname* : string, required

- Enter the name of the group

*companyname* : string, required

- Company name of consumer

*contactname* : string, required

- Contact name of consumer

*contactemail* : string, required

- Contact email of consumer

*location* : string, required

- Location of consumer

*description* : string, required

- Description of why consumer wants to subscribe to topic

*brokerhost* : string, optional

- Address of Kafka broker - if none is specified it will use broker address in VIPER.ENV file

*brokerport* : int, optional

- Port Kafka is listening on - if none is specified it will use port in the VIPER.ENV file

*microserviceid* : string, optional

- If you are routing connections to VIPER through a microservice then indicate it here.

RETURNS: Returns a JSON object of the groupid of the group.
								
**35. maads.viperconsumergroupconsumefromtopic(vipertoken,host,port,topic,consumerid,groupid,companyname,
		partition=-1,enabletls=0,delay=100,offset=0,brokerhost='',brokerport=-999,microserviceid='')**

**Parameters:**	

*VIPERTOKEN* : string, required

- A token given to you by VIPER administrator.

*host* : string, required
       
- Indicates the url where the VIPER instance is located and listening.

*port* : int, required

- Port on which VIPER is listenting.

*topic* : string, required
       
- Topic to dd to the group, multiple (active) topics can be separated by comma 

*consumerid* : string, required

- Enter the consumerid associated with the topic

*groupid* : string, required

- Enter the groups id

*companyname* : string, required

- Enter the company name

*partition*: int, optional

- set to Kakfa partition number or -1 to autodetect

*enabletls*: int, optional

- Set to 1 if Kafka broker is SSL/TLS enabled, otherwise set to 0 for plaintext.

*delay*: int, optional

- Time in milliseconds before VIPER backsout from reading messages

*offset* : int, optional

- Offset to start reading from.  If 0, will read from the beginning of topic, or -1 to automatically go to end of topic.

*brokerhost* : string, optional

- Address of Kafka broker - if none is specified it will use broker address in VIPER.ENV file

*brokerport* : int, optional

- Port Kafka is listening on - if none is specified it will use port in the VIPER.ENV file

*microserviceid* : string, optional

- If you are routing connections to VIPER through a microservice then indicate it here.

RETURNS: Returns a JSON object of the contents of the group.
    
**36. maads.vipermodifyconsumerdetails(vipertoken,host,port,topic,companyname,consumerid,contactname='',
contactemail='',location='',brokerhost='',brokerport=9092,microserviceid='')**

**Parameters:**	

*VIPERTOKEN* : string, required

- A token given to you by VIPER administrator.

*host* : string, required
       
- Indicates the url where the VIPER instance is located and listening.

*port* : int, required

- Port on which VIPER is listenting.

*topic* : string, required
       
- Topic to dd to the group, multiple (active) topics can be separated by comma 

*consumerid* : string, required

- Enter the consumerid associated with the topic

*companyname* : string, required

- Enter the company name

*contactname* : string, optional

- Enter the contact name 

*contactemail* : string, optional
- Enter the contact email

*location* : string, optional

- Enter the location

*brokerhost* : string, optional

- Address of Kafka broker - if none is specified it will use broker address in VIPER.ENV file

*brokerport* : int, optional

- Port Kafka is listening on - if none is specified it will use port in the VIPER.ENV file

*microserviceid* : string, optional

- If you are routing connections to VIPER through a microservice then indicate it here.

RETURNS: Returns success/failure

**37. maads.vipermodifytopicdetails(vipertoken,host,port,topic,companyname,isgroup=0,contactname='',contactemail='',
		location='',brokerhost='',brokerport=9092,microserviceid='')**
     
**Parameters:**	

*VIPERTOKEN* : string, required

- A token given to you by VIPER administrator.

*host* : string, required
       
- Indicates the url where the VIPER instance is located and listening.

*port* : int, required

- Port on which VIPER is listenting.

*topic* : string, required
       
- Topic to dd to the group, multiple (active) topics can be separated by comma 

*companyname* : string, required

- Enter the company name

*isgroup* : int, optional

- This tells VIPER whether this is a group topic if isgroup=1, or a normal topic if isgroup=0

*contactname* : string, optional

- Enter the contact name 

*contactemail* : string, optional
- Enter the contact email

*location* : string, optional

- Enter the location

*brokerhost* : string, optional

- Address of Kafka broker - if none is specified it will use broker address in VIPER.ENV file

*brokerport* : int, optional

- Port Kafka is listening on - if none is specified it will use port in the VIPER.ENV file

*microserviceid* : string, optional

- If you are routing connections to VIPER through a microservice then indicate it here.

RETURNS: Returns success/failure

**38. maads.viperactivatetopic(vipertoken,host,port,topic,microserviceid='')**

**Parameters:**	

*VIPERTOKEN* : string, required

- A token given to you by VIPER administrator.

*host* : string, required
       
- Indicates the url where the VIPER instance is located and listening.

*port* : int, required

- Port on which VIPER is listenting.

*topic* : string, required
       
- Topic to activate

*microserviceid* : string, optional

- If you are routing connections to VIPER through a microservice then indicate it here.

RETURNS: Returns success/failure
    
**39. maads.viperdeactivatetopic(vipertoken,host,port,topic,microserviceid='')**

**Parameters:**	

*VIPERTOKEN* : string, required

- A token given to you by VIPER administrator.

*host* : string, required
       
- Indicates the url where the VIPER instance is located and listening.

*port* : int, required

- Port on which VIPER is listenting.

*topic* : string, required
       
- Topic to deactivate

*microserviceid* : string, optional

- If you are routing connections to VIPER through a microservice then indicate it here.

RETURNS: Returns success/failure

**40. maads.vipergroupactivate(vipertoken,host,port,groupname,groupid,microserviceid='')**

**Parameters:**	

*VIPERTOKEN* : string, required

- A token given to you by VIPER administrator.

*host* : string, required
       
- Indicates the url where the VIPER instance is located and listening.

*port* : int, required

- Port on which VIPER is listenting.

*groupname* : string, required
       
- Name of the group

*groupid* : string, required
       
- ID of the group

*microserviceid* : string, optional

- If you are routing connections to VIPER through a microservice then indicate it here.

RETURNS: Returns success/failure
   
**41.  maads.vipergroupdeactivate(vipertoken,host,port,groupname,groupid,microserviceid='')**

**Parameters:**	

*VIPERTOKEN* : string, required

- A token given to you by VIPER administrator.

*host* : string, required
       
- Indicates the url where the VIPER instance is located and listening.

*port* : int, required

- Port on which VIPER is listenting.

*groupname* : string, required
       
- Name of the group

*groupid* : string, required
       
- ID of the group

*microserviceid* : string, optional

- If you are routing connections to VIPER through a microservice then indicate it here.

RETURNS: Returns success/failure
   
**Simple Example**      

#############################################################

Author: Sebastian Maurice, PhD

Copyright by Sebastian Maurice 2018

All rights reserved.

Email: Sebastian.maurice@otics.ca

#############################################################


** IMPORT THE MAAADS LIBRARY*
 import maads

** IMPORT ADDITIONAL LIBRARY**
 import imp


** LOAD ANY DATABASE LIBRARY TO STORE PREDICTIONS**
 sqlconn = imp.load_source('sqlconn','C:\\sqlsrvconnpython.py')

** OPEN DATABASE CONNECTION**
 connection = sqlconn.doconnect()

 cur = connection.cursor()

** TEST DATA    **   
 inputs = '1/12/2018,37.76896'
 
 pkey='demouser_test2log_csv'
 MAADSTOKEN=XXXXXXXXXXXXXXXXXXXX
 username='demouser'

 url='/maads/remotemasstreamremote.php'


** DO TRAINING - SERVER RETURNS A KEY THAT POINTS TO THE BEST ALGORITHM**
 thedata=maads.dotraining(MAADSTOKEN,'C:\\test2log.csv',1,0,0,'depvar',url)

** PARSE RETURNED DATA**
 pkey=maads.returndata(thedata,'PKEY:')

 algo=maads.returndata(thedata,'ALGO0:')

 accuracy=maads.returndata(thedata,'ACCURACY0:')
      
** DO PREDICTIONS WITH THE RETURNED KEY**
 thepredictions=maads.dopredictions(MAADSTOKEN,0,pkey,inputs,url)

** PARSE THE DATA**
 prediction=maads.returndata(thepredictions,'DATA:')


** INSERT PREDICTIONS TO ANY DATABASE TABLE**
 forecastdate=inputs.split(',')[0]

 predictionvalue=prediction[2]

 accuracy=prediction[3]

 SQL="INSERT INTO PREDICTIONS VALUES('%s','%s','%s','%s','%s',%.3f,%.3f)" % (forecastdate,username,pkey,company,inputs,predictionvalue,accuracy)

 cur.execute(SQL)

 cur.commit()

** CLOSE THE DATABASE CONNECTION**
 cur.close()

        
