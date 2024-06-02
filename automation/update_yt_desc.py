import os
import pickle
import json
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google.auth.transport.requests import Request

description_template = """
#BigData #Spark #بالعربي #DataEngineering
**Big Data Engineering in Depth with Apache Spark**

Welcome to our comprehensive guide on Apache Spark! In this episode, we cover the following topics:

📌 **Objectives:**
- {obj1}
- {obj2}
- {obj3}

🔗 **Course Links:**
- Lesson Link: https://www.garageeducation.org/docs/apache-spark/{video_link}
- Discord Group: https://discord.gg/v7HEaJhHmg

📢 **Disclaimer:**
This disclaimer informs the audience that the views, thoughts, and opinions presented in the video belong solely to the author and not necessarily to the author's employer, organization, committee, or other group or individual.

📣 **Follow us on Social Media:**
- Twitter: https://twitter.com/garageeducation
- Facebook: https://www.facebook.com/GarageEducationCourses/
- YouTube: https://www.youtube.com/c/GarageEducation
- Website: https://www.GarageEducation.org/
- LinkedIn: https://www.linkedin.com/in/MoustafaAMahmoud

🔖 **Tags:**
#BigData #Spark #Hadoop #DataEngineering #ApacheSpark #BigDataAnalytics #DataScience #MachineLearning #Python #Scala #DataLake #CloudComputing #DistributedComputing #DataProcessing #Analytics
"""

# Set up the necessary credentials and initialize the YouTube API client
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "secret-yp.json"  # Replace with your client secret file
credentials_file = "token.pickle"

# Load credentials from file if available
credentials = None
if os.path.exists(credentials_file):
    with open(credentials_file, 'rb') as token:
        credentials = pickle.load(token)

# If there are no valid credentials available, let the user log in.
if not credentials or not credentials.valid:
    if credentials and credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())
    else:
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
        credentials = flow.run_console()

    # Save the credentials for the next run
    with open(credentials_file, 'wb') as token:
        pickle.dump(credentials, token)

youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)

# Load video data from JSON file
with open('video_data.json', 'r') as file:
    video_data = json.load(file)


# Function to update video description
def update_video_description(video_id, title, description):
    request = youtube.videos().update(
        part="snippet",
        body={
            "id": video_id,
            "snippet": {
                "title": title,
                "categoryId": "27",  # Education category
                "description": description
            }
        }
    )
    response = request.execute()
    return response


# Loop through each video and update the description
for video_num, details in video_data.items():
    video_id = details['video_id']
    title = details['title']
    objectives = details['objectives']
    video_link = details['video_link']
    description = description_template.format(obj1=objectives[0], obj2=objectives[1], obj3=objectives[2],
                                              video_link=video_link)
    update_video_description(video_id, title, description)
    print(f"Updated description for video ID: {title} ({video_id})")

print("All video descriptions updated successfully!")
