import json, glob, sqlite3, re, datetime, os
from functools import partial

class DatabaseBuilder():

    def _insert_tables(self, db_name):
        with sqlite3.connect(db_name) as con:
            cur = con.cursor()

            cur.execute("""CREATE TABLE messages (
            "message_id"	INTEGER NOT NULL UNIQUE,
            "sender_name"	TEXT,
            "timestamp"	INTEGER,
            "content"	TEXT,
            "type"	TEXT,
            "is_unsent"	INTEGER,
            "photos_count"	INTEGER,
            "videos_count"	INTEGER,
            "sticker_count"	INTEGER,
            "audioclip_count"	INTEGER,
            "gif_count"	INTEGER,
            "files_count"	INTEGER,
            "users_count"	INTEGER,
            "call_duration"	INTEGER,
            "reaction_count" INTEGER,
            PRIMARY KEY("message_id" AUTOINCREMENT))""")

            cur.execute("""CREATE TABLE reactions ("message_id"	INTEGER NOT NULL, actor, reaction)""")
            cur.execute("""CREATE TABLE participants ("participant_id" INTEGER, name,PRIMARY KEY("participant_id" AUTOINCREMENT))""")
            cur.execute("""CREATE TABLE subscriptions ("message_id"	INTEGER NOT NULL, "subscription_type" TEXT, "user" TEXT)""")
            cur.execute("""CREATE TABLE photos ("message_id"	INTEGER NOT NULL, uri, creation_timestamp)""")
            cur.execute("""CREATE TABLE videos ("message_id"	INTEGER NOT NULL, uri, creation_timestamp, thumbnail_uri)""")
            cur.execute("""CREATE TABLE audiofiles ("message_id"	INTEGER NOT NULL, uri, creation_timestamp)""")
            cur.execute("""CREATE TABLE gifs ("message_id"	INTEGER NOT NULL, uri)""")
            cur.execute("""CREATE TABLE share ("message_id"	INTEGER NOT NULL, link, share_text)""")

    def _path_to_dict(self, file_path):
        #Thank you Martijn Pieters!!
        #https://stackoverflow.com/questions/50008296/facebook-json-badly-encoded

        fix_mojibake_escapes = partial(
        re.compile(rb'\\u00([\da-f]{2})').sub, lambda m: bytes.fromhex(m.group(1).decode()))

        with open(file_path, 'rb') as binary_data:
            repaired = fix_mojibake_escapes(binary_data.read())
        data = json.loads(repaired.decode('utf8'), strict=False)
        return data

    #Will read a json file and populate the database based on that files content.
    def _populate_database(self, file_path, db_name):
        con = sqlite3.connect(db_name)
        cur = con.cursor()

        json_object = self._path_to_dict(file_path)
        
        cur.execute("""SELECT max(message_id) FROM messages""")
        result = cur.fetchone()
        if(result == (None, )):
            current_message_id = 1
        else:
            current_message_id = result[0] + 1

        cur.execute("""BEGIN TRANSACTION""")

        for message in json_object["messages"]:
            sender_name = message["sender_name"]
            timestamp = datetime.datetime.fromtimestamp(message["timestamp_ms"]/1000.0)
            message_type = message["type"]
            is_unsent = message["is_unsent"]

            content = ""
            if("content" in message):
                content = message["content"]

            photos_count = 0
            videos_count = 0
            sticker_count = 0
            audioclip_count = 0
            gif_count = 0
            files_count = 0
            users_count = 0
            call_duration = 0
            reaction_count = 0

            if("photos" in message):
                photos_count = len(message["photos"])
            if("videos" in message):
                videos_count = 1
            if("sticker" in message):
                sticker_count = 1
            if("audio_files" in message):
                audioclip_count = len(message["audio_files"])
            if("gifs" in message):
                gif_count = len(message["gifs"])
            if("files" in message):
                files_count = len(message["files"])
            if("users" in message):
                users_count = len(message["users"])
            if("call_duration" in message):
                call_duration = message["call_duration"]
            if("reactions" in message):
                reaction_count = len(message["reactions"])

            #Populate messages table
            cur.execute("""INSERT INTO messages (sender_name, timestamp, content, type, is_unsent, photos_count, videos_count, sticker_count, audioclip_count, gif_count, files_count, users_count, call_duration, reaction_count) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", [sender_name, timestamp, content, message_type, is_unsent, photos_count, videos_count, sticker_count, audioclip_count, gif_count, files_count, users_count, call_duration, reaction_count])

            #Populate reactions table
            if(reaction_count > 0):
                for react in message["reactions"]:
                    cur.execute("""INSERT INTO reactions (message_id, actor, reaction) VALUES (?, ?, ?)""", [current_message_id, react["actor"], react["reaction"]])

            #Populate subscriptions table
            if("users" in message and (message["type"] == "Subscribe" or message["type"] == "Unsubscribe")):
                for user in message["users"]:
                    cur.execute("""INSERT INTO subscriptions (message_id, subscription_type, user) VALUES (?, ?, ?)""", [current_message_id, message["type"], user["name"]])
            
            #Populate photos table
            if(photos_count > 0 and "photos" in message):
                for photo in message["photos"]:
                    creation_timestamp = datetime.datetime.fromtimestamp(photo["creation_timestamp"])
                    cur.execute("""INSERT INTO photos (message_id, uri, creation_timestamp) VALUES (?, ?, ?)""", [current_message_id, photo["uri"], creation_timestamp])
            
            #Populate videos table
            if(videos_count > 0 and "videos" in message):
                for video in message["videos"]:
                    creation_timestamp = datetime.datetime.fromtimestamp(video["creation_timestamp"])
                    cur.execute("""INSERT INTO videos (message_id, uri, creation_timestamp, thumbnail_uri) VALUES (?, ?, ?, ?)""", [current_message_id, video["uri"], creation_timestamp, video["thumbnail"]["uri"]])
            
            #Populate audiofiles table
            if(audioclip_count > 0 and "audio_files" in message):
                for audiofile in message["audio_files"]:
                    creation_timestamp = datetime.datetime.fromtimestamp(audiofile["creation_timestamp"])
                    cur.execute("""INSERT INTO audiofiles (message_id, uri, creation_timestamp) VALUES (?, ?, ?)""", [current_message_id, audiofile["uri"], creation_timestamp])

            #Populate gifs table
            if(gif_count > 0 and "gifs" in message):
                for gif in message["gifs"]:
                    cur.execute("""INSERT INTO gifs (message_id, uri) VALUES (?, ?)""", [current_message_id, gif["uri"]])

            #Populate share table
            if(message["type"] == "Share" and "share" in message):
                if("link" in message["share"]):
                    cur.execute("""INSERT INTO share (message_id, link, share_text) VALUES (?, ?, ?)""", [current_message_id, message["share"]["link"], None])
                elif("share_text" in message["share"]):
                    cur.execute("""INSERT INTO share (message_id, link, share_text) VALUES (?, ?, ?)""", [current_message_id, None, message["share"]["share_text"]])
            current_message_id += 1

        cur.execute("""COMMIT""")
        con.close()

    def _populate_participants(self):
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        cur.execute("SELECT DISTINCT user FROM subscriptions ORDER BY user")
        results = cur.fetchall()
        participant_id = 1

        cur.execute("""BEGIN TRANSACTION""")
        for participant in results:
            cur.execute("""INSERT INTO participants (participant_id, name) VALUES (?, ?)""", (participant_id, participant[0]))
            participant_id += 1
        cur.execute("""COMMIT""")

    def _get_conversation_jsons(self):
        file_paths = glob.glob(f"{self.conversation_location}*.json")
        #Sort files by id, 'message_<id>.json', instead of alphabetical order.
        return sorted(file_paths, key=lambda file: int(file.split("/")[-1].split("_")[-1].split(".")[0]))

    def create_database(self, overwrite=False):
        if(glob.glob(self.db_name)):
            if(overwrite):
                os.remove(self.db_name)
            else:
                print("Database with same name was already found. Aborting...")
                return
            
        self._insert_tables(self.db_name)
        file_paths = self._get_conversation_jsons()

        for file_path in file_paths:
            print(f"Parsing and adding {file_path.split('/')[-1]} to the database.")
            self._populate_database(file_path, self.db_name)
        self._populate_participants()

    def __init__(self):
        self.conversation_location = os.getenv("CONVERSATION_PATH")
        self.db_name = os.getenv("DATABASE_NAME")