import argparse
import requests

def main():
    parser = argparse.ArgumentParser("Information App")
    parser.add_argument("-t", "--type", type=str, choices = ["dictionary, facts, bucket_list"], required=True)
    #subparsers = parser.add_subparsers()

    #parser_word = subparsers.add_subparsers('word')
    #parser_word.add_argument('--word', type=str)

    #parser_fact = subparsers.add_subparsers('num')
    #parser_fact.add_argument("--num",type=str)

    # Dictionary
    if "-t" == "dictionary":
        word = 'code'
        api_url = 'https://api.api-ninjas.com/v1/dictionary?word={}'.format(word)
        response = requests.get(api_url, headers={'X-Api-Key': '0N8v9yzHD+xX0cCOMb+Fog==U7gJjbbVBq9N1i4i'})
        if response.status_code == requests.codes.ok:
            print(response.text)
        else:
            print("Error:", response.status_code, response.text)

    # Fact
    elif "-t" == "facts":
        limit = 30
        api_url = 'https://api.api-ninjas.com/v1/facts?limit={}'.format(limit)
        response = requests.get(api_url, headers={'X-Api-Key': '0N8v9yzHD+xX0cCOMb+Fog==U7gJjbbVBq9N1i4i'})
        if response.status_code == requests.codes.ok:
            print(response.text)
        else:
            print("Error:", response.status_code, response.text)

    elif "-t" == "bucket_list":
        api_url = 'https://api.api-ninjas.com/v1/bucketlist'
        response = requests.get(api_url, headers={'X-Api-Key': '0N8v9yzHD+xX0cCOMb+Fog==U7gJjbbVBq9N1i4i'})
        if response.status_code == requests.codes.ok:
            print(response.text)
        else:
            print("Error:", response.status_code, response.text)


if __name__ == "__main__":
    main()

