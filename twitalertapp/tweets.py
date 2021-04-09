import pandas as pd 
import json
import ast
import yaml
import requests
import urllib.parse
# from azure.ai.textanalytics import TextAnalyticsClient
# from azure.core.credentials import AzureKeyCredential

#################################
# Twitter setup
#################################

def create_twitter_url(location="San Francisco"):
    max_results = 10
    mrf = f"max_results={max_results}"
    search = urllib.parse.quote("car crash OR fire OR tornado OR earthquake")
    search = "(" + search +")"
    query = urllib.parse.quote(f'-is:retweet entity:"{location}"')
    query = "query=" + search + query
    print(query)
    url = f"https://api.twitter.com/2/tweets/search/recent?{mrf}&{query}"
    return url

def process_yaml():
    with open("config.yaml") as file:
        return yaml.safe_load(file)

def create_bearer_token(data):
    return data["search_tweets_api"]["bearer_token"]

def twitter_auth_and_connect(bearer_token, url):
    headers = {"Authorization": f"Bearer {bearer_token}"}
    response = requests.request("GET", url, headers=headers)
    return response.json()

#################################
# Azure setup
#################################

def connect_to_azure(data):
    azure_url = "https://twitalert.cognitiveservices.azure.com/"
    language_api_url = f"{azure_url}text/analytics/v3.0/languages"
    sentiment_url = f"{azure_url}text/analytics/v3.0/sentiment"
    subscription_key = data["azure"]["subscription_key"]
    return language_api_url, sentiment_url, subscription_key

def azure_header(subscription_key):
    headers = {"Ocp-Apim-Subscription-Key": f"{subscription_key}", "Content-Type": "application/json", "Accept": "application/json"}
    return headers

def lang_data_shape(res_json):
    data_only = res_json["data"]
    doc_start = f'"documents": {data_only}'
    str_json = "{" + doc_start + "}"
    dump_doc = json.dumps(str_json)
    doc = json.loads(dump_doc)
    return ast.literal_eval(doc)

def generate_languages(headers, language_api_url, documents):
    response = requests.post(language_api_url, headers = headers, json = documents)
    return response.json()

def combine_lang_data(documents, with_languages):
    langs = pd.DataFrame(with_languages["documents"])
    lang_iso = [d.get("iso6391Name") 
                for d in langs.detectedLanguage if d]
    data_only = documents["documents"]
    tweet_data = pd.DataFrame(data_only)
    tweet_data.insert(2, "language", lang_iso, True)
    print(tweet_data)
    json_lines = tweet_data.to_json(orient="records")
    return json_lines

def add_document_format(json_lines):
    docu_format = '"' + "documents" + '"'
    json_docu_format = f"{docu_format}:{json_lines}"
    docu_align = "{" + json_docu_format + "}"
    jd_align = json.dumps(docu_align)
    jl_align = json.loads(jd_align)
    return ast.literal_eval(jl_align)

def sentiment_scores(headers, sentiment_url, document_format):
    response = requests.post(sentiment_url, headers=headers, json=document_format)
    response_json = response.json()
    response_df = pd.DataFrame(response_json["documents"])
    print(response_df)
    return response.json()

#################################
# Main
#################################

def tweet_main():
    url = create_twitter_url()
    data = process_yaml()
    bearer_token = create_bearer_token(data)
    res_json = twitter_auth_and_connect(bearer_token, url)
    documents = lang_data_shape(res_json)
    language_api_url, sentiment_url, subscription_key = connect_to_azure(data)
    headers = azure_header(subscription_key)
    with_languages = generate_languages(headers, language_api_url, documents)
    json_lines = combine_lang_data(documents, with_languages)
    document_format = add_document_format(json_lines)
    sentiments = sentiment_scores(headers, sentiment_url, document_format)
    # print(sentiments)

if __name__ == "__main__":
    tweet_main()