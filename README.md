# Messenger Archive SQLite Database Builder

This is a script used to create a SQLite database from exported facebook messenger JSON data.

## Usage

1. Request and download a collection of messages in JSON format from [Facebook](https://www.facebook.com/dyi/)
2. Clone the repo
3. Set the following environment variables, or alternatively create a file `.env` file in the root directory with the configuration:
```
    CONVERSATION_PATH=/PATH/TO/ROOT/CONVERSATION/FOLDER/messages/inbox/chat/
    DATABASE_NAME=database.db
```
4. Run the script: ```python main.py```

## JSON Schema
A more in-depth description of the JSON-schema used for the data export can be found [here.](Schema.md)

## Database Tables

These are the tables and corresponding fields generated in the database by the script. 

### audiofiles
**Field**|**Comment**
-----|-----
message\_id| Corresponds to a message id in the messages table.
uri| URI to audio file resource.
creation\_timestamp| 

### gifs
**Field**|**Comment**
-----|-----
message\_id| Corresponds to a message id in the messages table.
uri| URI to gif resource.

### messages
**Field**|**Comment**
-----|-----
message\_id| Unique message id.
sender\_name| Person who sent the message.
timestamp| When the message was sent.
content| The actual message sent.
type| Can one of 5 values: Generic, Share, Subscribe, Unsubscribe or Call
is\_unsent| Is true if the message was removed by the sender.
photos\_count| The number of photos sent.
videos\_count| The number of videos sent.
sticker\_count| The number of stickers sent.
audioclip\_count| The number of audioclips sent.
gif\_count| The number of gifs sent.
files\_count| The number of files sent.
users\_count| The number of users who were added or removed. Only applicable of message types Unsubscribe and Subscribe.
call\_duration| The duration of a call. Only applicable for message type Call.
reaction\_count| The number of reactions received for the message.

### participants

_NOTE: The JSON files participants object will only contain the participants at the time of the export. This table however will contain all users who've ever been in the conversation._

**Field**|**Comment**
-----|-----
participant\_id| Unique participant id
name| Name of participant

### photos
**Field**|**Comment**
-----|-----
message\_id| Corresponds to a message id in the messages table.
uri| URI to photo.
creation_timestamp

### reactions
**Field**|**Comment**
-----|-----
message\_id| Message id which the reaction was made on.
actor| Name of person who reacted on the message.
reaction| Emoji depicting which reaction was made.

### share
**Field**|**Comment**
-----|-----
message\_id| Corresponds to a message id in the messages table.
link| Link which was shared.
share\_text| Used when sharing locations.

### subscriptions
**Field**|**Comment**
-----|-----
message\_id| Corresponds to a message id in the messages table.
subscription\_type| Can be either Subscribe or Unsubscribe depending on adding or removing user from conversation.
user| The user who was removed or added to the conversation. The message table contains information on who removed/added the user in this table.

### videos
**Field**|**Comment**
-----|-----
message\_id| Corresponds to a message id in the messages table.
uri| URI to video.
creation_timestamp
thumbnail_uri | URI to video (same as uri field as of today).