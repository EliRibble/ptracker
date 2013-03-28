USERNAME=eribble@hirevue.com
PASSWORD=iI9jXZtrbD

#curl -u $USERNAME:$PASSWORD -X GET https://www.pivotaltracker.com/services/v3/tokens/active


GUID=3bd49390f706d0b9b00ba9f65cc9cc1a
TOKEN=$GUID

# Project ID for E2

PROJECT_ID=361893
# Get projects

#curl -H "X-TrackerToken: $TOKEN" -X GET https://www.pivotaltracker.com/services/v3/projects
#curl -H "X-TrackerToken: $TOKEN" -X GET http://www.pivotaltracker.com/services/v3/projects/$PROJECT_ID/stories
#curl -H "X-TrackerToken: $TOKEN" -X GET https://www.pivotaltracker.com/services/v3/projects/$PROJECT_ID/stories?filter=type%3Abug
bin/ptracker --guid=$GUID projects
