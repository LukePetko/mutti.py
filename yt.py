from apiclient.discovery import build

youtube = build('youtube', 'v3', developerKey='AIzaSyBRZJGbujFn3dv5kSOQyBFafRxHvGCT0eQ')

req = youtube.search().list(q='Mars Argo', part='snippet', type='video')


print(req.execute()['items'][0]['id']['videoId'])
