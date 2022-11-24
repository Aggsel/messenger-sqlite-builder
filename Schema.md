# Facebook Messenger JSON Schema
The following file contains documentation regarding the JSON schema 

Each `message.json` file contains an JSON-object with the following root-level keys: 
* [participants](#participants)
* [title](#title)
* [is_still_participant](#is-still-participant)
* [thread_type](#thread-type)
* [thread_path](#thread-path)
* [thread_type](#thread-type)
* [image](#image)
* [joinable_mode](#joinable-mode)
* [messages](#messages)
    * [type](#type)
    * [is_unsent](#is-unsent)
    * [photos](#photos)
    * [videos](#videos)
    * [audio_files](#audio-files)
    * [share](#share)
    * [gifs](#gifs)
    * [call_duration](#call-duration)
    * [files](#files)
    * [sticker](#sticker)
    * [users](#users)

## Participants 
`participants`, a list of all participants in the conversation *at the time of export*. Users who've previously been in the conversation will not be listed, even though their messages are present in the export.

```json
"participants": [
    { "name": "Foo Bar" },
    { "name": "Foo Baz" }
]
```

## Title
`title`, the title of the conversation at the time of export.

```json
"title": "Foo Bar"
```

## Is still participant
`is_still_participant`, A boolean describing whether or not the person who exported the data is still a participant of the conversation.

```json
"is_still_participant": true
```
## Thread type
`thread_type`, A string describing what type the conversation is. Can be set to either "RegularGroup" or "Regular" depending on whether or not it is a group conversation.

```json
    "thread_type": "RegularGroup",
    "thread_type": "Regular"
```

## Thread path
`thread_path`, relative path to the specific conversation from the root directory of the export.

```json
    "thread_path": "inbox/foobar_threadid"
```

## Magic words
`magic_words`, unclear at the moment what this key contains. Seems to always be an empty array.

## Image
* `image`, an object containing information regarding the conversation image. Is only present in group conversations.

```json 
"image": {
    "uri": "path_to/image.jpg",
    "creation_timestamp": 1636300000
}
```

## Messages
`messages`, an array of message objects, each of which can contain a variety of different subobjects and/or values.

`sender_name` `String`, contains the name of the person who sent the message. 
`timestamp_ms` - `Int`, unix timestamp (ms) when the message was sent.
`content` - `String`, contains the content of the message.
`reactions` - `List`, a list of objects containing information regarding which participants have reacted to this message. `actor` being the participant making the react. `reaction` being a UTF-8 string for the emoji character. 

```json
{
    "sender_name": "John Smith",
    "timestamp_ms": 163628871000,
    "content": "Haha :)",
    "type": "Generic",
    "reactions": [
        {"reaction": "\u00f0\u009f\u0098\u00a2", "actor": "John Smith"}, 
        {"reaction": "\u00f0\u009f\u0098\u00a2", "actor": "John McClane"}, 
        {"reaction": "\u00f0\u009f\u0098\u00a2", "actor": "Hans Gruber"}
    ]
}
```

### Type
`type`, a string containing which type the message is. Contains one of the following: Generic, Share, Call, Subscribe or Unsubscribe.

`Generic`, a normal text message. 

`Share`, message will also include an object called `share`, which in turn will contain the link that was shared. If the shared message was a live location, the share key will not have a `link` inside. Instead it will have a `share_text`.

```json 
{
    "sender_name": "John Smith",
    "timestamp_ms": 163628871000,
    "share": 
    { 
        "link": "https://www.youtube.com/watch?v=dQw4w9WgXcQ" 
    },
    "type": "Share" 
}

//or

{
    "sender_name": "John Smith",
    "timestamp_ms": 163628871000,
    "share": 
    {
        "share_text": "Last updated 8 september"
    },
    "type": "Share"
}
```

`Call`, is sent whenever a voice or video call is initiated or ended. Message object will also contain information about the call duration. The duration does not seem to reflect the actual duration of the call however, or maybe I'm missing something...

```json 
{
    "sender_name": "John Smith",
    "timestamp_ms": 163628871000,
    "call_duration": 3872,
    "type": "Call" 
}
```

`Subscribe`, is sent whenever a user added a user to the group. Message object will also contain information about which user(s) were added.

```json 
{
    "sender_name": "John Smith",
    "timestamp_ms": 163628871000,
    "type": "Subscribe",
    "users": [
        {
            "name": "John McClane"
        },
        {
            "name": "Hans Gruber"
        }
    ]
}
```


`Unsubscribe`, is sent whenever a user leaves or is removed from the group. Message object will contain information about who left/was kicked. If the user leaves, `sender_name` will be the same as the first entry in `users`.

```json
{
    "sender_name": "John Smith",
    "timestamp_ms": 163628871000,
    "type": "Unsubscribe",
    "users": [
        {"name": "Hans Gruber"}
    ]
}
```


### Is unsent
`is_unsent`, a boolean describing whether or not this message was removed (unsent). If true, the message object will not contain a "content" key. If the message had any reactions before being removed, these will still remain.

```json
"messages": [
    {
        "sender_name": "John Smith",
        "timestamp_ms": 163628871000,
        "type": "Generic",
        "is_unsent": true,
        "reactions": [
            {
                "reaction": "\u00f0\u009f\u0098\u008d",
                "actor": "Hans Gruber"
            }
        ]
    }
]
```

### Photos
`photos`, a list containing URIs to the image(s) sent. If a text message was sent at the same time, the message object will contain a key `content`, otherwise this key will not be present. The objects in the photos list will also contain a timestamp describing when they were sent (in seconds, NOT milliseconds as messages `timestamp_ms`).

```json
"messages": [
    {
        "sender_name": "John Smith",
        "timestamp_ms": 163628871000,
        "type": "Generic",
        "is_unsent": false,
        "photos": [
            {
                "uri": "messages/inbox/chat_name/photos/32543254325_5325321121.jpg", 
                "creation_timestamp": 1635008000
            },
            {
                "uri": "messages/inbox/chat_name/photos/42141523532523_5243432.jpg", 
                "creation_timestamp": 1635008000
            }
        ]
    }
]
```

### Videos
`videos`, contains a list of objects with metadata regarding the video(s) sent. From what I've seen, the thumbnail object will always contain the same URI as the video.

```json
"messages": [
    {
        "sender_name": "John Smith", 
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
### Audio files
`audio_files`, a list of audio_file objects, each of which containing the URI to a audio file.

```json
"messages": [
    {
        "sender_name": "John Smith", 
        "timestamp_ms": 149805586000, 
        "audio_files": [
            { 
                "uri": "messages/inbox/chat_name/audio/audio_clip.mp4", 
                "creation_timestamp": 160344700 
            }
        ],
        "type": "Generic",
        "is_unsent": false
    }
]
```

### Share
`share`, only present whenever the message type is `Share` (see that entry for more information).

### Gifs
`gifs`, similar to `photos`, but all images are gifs.

```json
"messages": [
    {
        "sender_name": "John Smith",
        "timestamp_ms": 163628871000,
        "type": "Generic",
        "is_unsent": false,
        "gifs": [
            {"uri": "messages/inbox/chat_name/gifs/32543254325_5325321121.gif"}
        ]
    }
]
```

### Call duration
`call_duration`, only present whenever the message type is `Call` (see that entry for more information).

### Files
`files`, contains a list of files (other than photo, audio, sticker or videos) sent in the message. In this example, a LaTeX source file was sent.

```json
"messages": [
    {
        "sender_name": "John Smith",
        "timestamp_ms": 163628871000,
        "type": "Generic",
        "is_unsent": false,
        "files": [
            { 
                "uri": "messages/inbox/chat_name/files/file.tex",
                "creation_timestamp": 1611834000
            }
        ]
    }
]
```

### Sticker
`sticker`, an object containing a URI to an image of the sent sticker.

```json
"messages": [
    {
        "sender_name": "John Smith",
        "timestamp_ms": 163628871000,
        "type": "Generic",
        "is_unsent": false,
        "sticker": {
            "uri": "messages/stickers_used/3218421_21321.png"
        }
    }
]
```

### Users
`users`, contains a list of users who were affected by a Subscribe or Unsubscribe event. Only present whenever the message type is `Subscribe` or `Unubscribe` (see those entries in the section [types](#type) for more information).