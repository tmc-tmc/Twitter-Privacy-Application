# Twitter-Privacy-Application - An application for locating potential privacy issue that can be found in user tweets. 

The application first requires a number of necessary tokens from the user that are required (Bearer Token, etc.) before allowing the user to do one of two things:
 
- Search Recent Tweets (Up to 7 Days, an unfortuate limit of the free standard API)
- Search Random Tweets 

The amount that is pulled can specified with each option, after which they are stored to their respective text files. From these, a PDF report can be generated that highlights the following:

- Names
- Emails
- Locations
- Numbers (UK Mobile)


Sentiment analysis is then performed on each tweet, using UClassify with the IAB Taxonomy V3. The most likely category is returned to the user, along with the potential privacy flags, in the form of a pdf report. Additionally, a user can also email the report to themselves. 

