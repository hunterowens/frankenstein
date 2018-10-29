# frankenstein


## Using the API 

To use the API, first call the `start-show` endpoint. This should return a `show_id` that you will use for the rest of the session. 

To send texts to the api, send a post to `interact`. Example in `curl`

```shell 
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"string":"bankds happy happy bands", "show_id": 1}' \
  http://frankenstein.hunterowens.net/interact
```

To get the most recent text plus Sentiment scores. 

```shell 

curl http://frankenstein.hunterowens.net/interact?show_id=$YOUR_SHOW_ID
```

To get the talk functions from the api. 

```shell
curl http://frankenstein.hunterowens.net/talk?show_id=$YOUR_SHOW_ID
```

To get the summary themes

```shell
curl http://frankenstein.hunterowens.net/summary?show_id$YOUR_SHOW_ID
```