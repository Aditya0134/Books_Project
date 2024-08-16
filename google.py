import json
import requests


def main():
    search = google(input("Enter details as a list: "))
    if search != None:
        print(json.dumps(search.json(), ensure_ascii=False, indent=2))
    else:
        print("No match")


def google(details):
    for i in range(1):
        if " " in details[i]:
            details[i].replace(" ", "_")

    if details[1] == "":
        response = requests.get(
            f"https://www.googleapis.com/books/v1/volumes?q={details[0]}+intitle:{details[0]}&printType=books"
        ).json()
        if response["totalItems"] == 0:
            response = requests.get(
                f"https://www.googleapis.com/books/v1/volumes?q={details[0]}&printType=books"
            ).json()
    else:
        response = requests.get(
            f"https://www.googleapis.com/books/v1/volumes?q={details[0]}+intitle:{details[0]}+inauthor:{details[1]}&printType=books"
        ).json()
        if response["totalItems"] == 0:
            response = requests.get(
                f"https://www.googleapis.com/books/v1/volumes?q={details[0]}+inauthor:{details[1]}&printType=books"
            ).json()
    des = []
    for i in response["items"]:
        try:
            des.append(i["volumeInfo"]["description"])
        except KeyError:
            continue
    descriptions = []
    for i in range(len(des)):
        if len(des[i]) < 2500 and len(des[i]) > 700:
            descriptions.append(des[i])

    if descriptions != []:
        return descriptions[0]
    else:
        for i in range(len(des)):
            if len(des[i]) < 4500 and len(des[i]) > 250:
                descriptions.append(des[i])
        if descriptions != []:
            return descriptions[0]
        else:
            return None


if __name__ == "__main__":
    main()
