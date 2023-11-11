import requests

def main():
    hello = requests.get("http://localhost:8000/hello_world").text
    print(hello)

if __name__ == "__main__":
    main()