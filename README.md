# Messenger Archive SQLite Database Builder

This is a tool for populating a SQLite database with exported facebook messenger JSON data.

## Usage

1. Request and download a collection of messages in JSON format from Facebook.
2. Clone the repo
3. Create a file `.env` file in the root directory with the configuration:
```
    CONVERSATION_PATH=/PATH/TO/ROOT/CONVERSATION/FOLDER/messages/inbox/chat/
    DATABASE_NAME=database.db
```
4. Run the script.

# Facebook Messenger JSON Schema

For a somewhat outdated but "proper" schema, click [here.](https://github.com/SamuelePilleri/facebook-schemas/blob/master/messages/message.json)

## Conversation Keys

* `participants` - `List`, participants in the conversation *at the time of export*.

    ### Example:
    ```json
    "participants": [
        { "name": "Foo Bar" },
        { "name": "Foo Baz" }
    ]
    ```

* `messages` - `Object`, can contain a variety of different subobjects and/or values.

    * `sender_name` - `String`, contains the name of the person who sent the message. 
    * `timestamp_ms` - `Int`, unix timestamp (ms) when the message was sent.
    * `content` - `String`, contains the content of the message.
    * `reactions` - `List`, a list of objects containing information regarding which participants have reacted to this message. `actor` being the participant making the react. `reaction` being a UTF-8 string for the emoji character. 

        ### Example:
        ```json
        {
            "sender_name": "Foo Bar",
            "timestamp_ms": 163628871000,
            "content": "Haha :)",
            "type": "Generic",
            "reactions": [
                {"reaction": "\u00f0\u009f\u0098\u00a2", "actor": "Foo Baz"}, 
                {"reaction": "\u00f0\u009f\u0098\u00a2", "actor": "Baz Foo"}, 
                {"reaction": "\u00f0\u009f\u0098\u00a2", "actor": "Bar Baz"}
            ]
        }
        ```

    * `type` - `String`, contains which type the message is. Contains one of the following:
        * `Generic`, a "normal" text message. 
        * `Share`, message will also include a key called `share`, which in turn will contain the link that was shared. If the shared message was a live location, the share key will not have a `link` inside. Instead it will have a `share_text`.

            ### Example:
            ```json 
            {
                "sender_name": "Foo Bar",
                "timestamp_ms": 163628871000,
                "share": 
                { 
                    "link": "https://www.youtube.com/watch?v=dQw4w9WgXcQ" 
                },
                "type": "Share" 
            }

            //or

            {
                "sender_name": "Foo Bar",
                "timestamp_ms": 163628871000,
                "share": 
                {
                    "share_text": "Last updated 8 september"
                },
                "type": "Share"
            }
            ```

        * `Call`, is sent whenever a voice or video call is initiated or ended. Message object will also contain information about the call duration.

            ### Example:
            ```json 
            {
                "sender_name": "Foo Bar",
                "timestamp_ms": 163628871000,
                "call_duration": 3872,
                "type": "Call" 
            }
            ```

        * `Subscribe`, is sent whenever a user added a user to the group. Message object will also contain information about which user(s) were added.

            ### Example:
            ```json 
            {
                "sender_name": "Foo Bar",
                "timestamp_ms": 163628871000,
                "type": "Subscribe",
                "users": [
                    {"name": "Foo Baz"},
                    {"name": "Baz Foo"}
                ]
            }
            ```


        * `Unsubscribe`, is sent whenever a user leaves or is removed from the group. Message object will contain information about who left/was kicked. If the user leaves, `sender_name` will be the same as the first entry in `users`.

            ### Example:
            ```json 
            {
                "sender_name": "Foo Bar",
                "timestamp_ms": 163628871000,
                "type": "Unsubscribe",
                "users": [
                    {"name": "Foo Baz"}
                ]
            }
            ```

    * `is_unsent` - `Bool`, whether or not this message was removed (unsent). If true, message content will be empty. If the message had any reactions before being removed, these will still remain.

        ### Example: 

        ```json
        "messages": [
            {
                "sender_name": "Foo Bar",
                "timestamp_ms": 163628871000,
                "type": "Generic",
                "is_unsent": true,
                "reactions": [
                    {
                        "reaction": "\u00f0\u009f\u0098\u008d",
                        "actor": "Foo Baz"
                    }
                ]
            }
        ]
        ```

    * `photos` - `List`, contains a list of uris to the image(s). If a text message was sent at the same time, the message object will contain a key `content`, otherwise this key will not be present. The objects in the photos list will also contain a timestamp describing when they were sent (in seconds, NOT milliseconds as messages `timestamp_ms`).
        ### Example: 

        ```json
        "messages": [
            {
                "sender_name": "Foo Bar",
                "timestamp_ms": 163628871000,
                "type": "Generic",
                "is_unsent": false,
                "photos": [
                    {"uri": "messages/inbox/chat_name/photos/32543254325_5325321121.jpg", "creation_timestamp": 1635008000},
                    {"uri": "messages/inbox/chat_name/photos/42141523532523_5243432.jpg", "creation_timestamp": 1635008000}
                ]
            }
        ]
        ```

    * `videos` - `List`, contains a list of objects with metadata regarding the video(s) sent.

        ### Example: 

        ```json
        "messages": [
            {
                "sender_name": "Foo Bar", 
                "timestamp_ms": 1498055860985, 
                "videos": [
                    {
                        "uri": "messages/inbox/chat_name/videos/video.mp4", 
                        "creation_timestamp": 1498055000, 
                        "thumbnail": {
                            "uri": "messages/inbox/chat_name/videos/video.mp4"
                        }
                    }
                ],
                "type": "Generic", 
                "is_unsent": false
            }
        ]
        ```

    * `audio_files`

        ### Example: 

        ```json
        "messages": [
            {
                "sender_name": "Foo Bar", 
                "timestamp_ms": 149805586000, 
                "audio_files": [
                    { "uri": "messages/inbox/chat_name/audio/audio_clip.mp4", "creation_timestamp": 160344700 }
                ],
                "type": "Generic",
                "is_unsent": false
            }
        ]
        ```

    * `share` - `List`, only present whenever the message type is `Share` (see that entry for more information).
    * `gifs` - `List`, similar to `photos`, but all images are gifs.

        ### Example: 

        ```json
        "messages": [
            {
                "sender_name": "Foo Bar",
                "timestamp_ms": 163628871000,
                "type": "Generic",
                "is_unsent": false,
                "gifs": [
                    {"uri": "messages/inbox/chat_name/gifs/32543254325_5325321121.gif"}
                ]
            }
        ]
        ```
    * `call_duration` - `Int`, only present whenever the message type is `Call` (see that entry for more information).
    * `files` - `List`, contains a list of files (other than photo, audio, sticker or videos) sent in the message. In this example, a LaTeX source file was sent.

        ### Example: 

        ```json
        "messages": [
            {
                "sender_name": "Foo Bar",
                "timestamp_ms": 163628871000,
                "type": "Generic",
                "is_unsent": false,
                "files": [
                    { "uri": "messages/inbox/chat_name/files/file.tex", "creation_timestamp": 1611834000 }
                ]
            }
        ]
        ```

    * `sticker`

        ### Example: 

        ```json
        "messages": [
            {
                "sender_name": "Foo Bar",
                "timestamp_ms": 163628871000,
                "type": "Generic",
                "is_unsent": false,
                "sticker": {
                    "uri": "messages/stickers_used/3218421_21321.png"
                }
            }
        ]
        ```
    
    * `users` - `List`, only present whenever the message type is `Subscribe` or `Unubscribe` (see those entries for more information).

* `title` - `String`, Title of the conversation at the time of export.

    ### Example:
    ```json
    {
        "title": "Foo Bar"
    }
    ```

* ```is_still_participant``` - ```Bool```, Is true if the person exporting the data is still a participant of the conversation.

    ### Example:
    ```json
    {
        "is_still_participant": true
    }
    ```

* `thread_type` - `String`, describing what type the conversation is.

    ### Example:
    ```json
    {
        "thread_type": "RegularGroup",
        "thread_type": "Regular"
    }
    ```
* `thread_path` - `String`, path to the conversation.

    ### Example:
    ```json
    {
        "thread_path": "inbox/foobar_threadid"
    }
    ```
* `magic_words` - `List` <!-- TODO: Find out what this does. --> 
* `image` - `Object`, contains information regarding the conversation image. Is only present in group conversations.

    ### Example:
    ```json 
    "image": {
        "uri": "path_to/image.jpg",
        "creation_timestamp": 1636300000
    }
    ```