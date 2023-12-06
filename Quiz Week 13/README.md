This is an information app.

There are three choices between information: "dictionary", "facts", and "bucket_list".

    The command "dictionary" will give the definition of a specified word.
    The command "facts" will give a specified number of facts.
    The command "bucket_list" will give a random bucket list idea.

Begin building the docker image by running 

        "docker build -t information -f Dockerfile ."
        
Then to use the app, use 

    "docker run -p 8080:8080 information [type] [arg]" 

where:

    type = "dictionary", "facts", or "bucket_list"
    arg = (a number up to 30 if type == "facts") OR (a word if type == "dictionary")
    arg is not necessary if type == "bucket_list"
