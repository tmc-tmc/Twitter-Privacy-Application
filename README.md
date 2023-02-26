# Twitter-Privacy-Application

An application for locating potential privacy issue that can be found in user tweets. 

The application takes a number of necessary tokens from the user that are required, which are then in turn used for when the user
uses the search username feature to get a list of their previous tweets. These tweets are saved to a txt file and, using the privacy viewer, a person can view potential privacy flags, such as

- Email
- Number
- Location
- Names

Sentiment analysis is then performed on each tweet, using UClassify with the IAB Taxonomy V2. The most likely catoegry is returned to the user, along with the potential privacy flags, in the form of a pdf report. Additionally, a user can also email the report to themselves. 

