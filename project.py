import json
import sys
from libgen_api import LibgenSearch
from google import google


def main():
    # Call all functions and monitors program flow
    details = names()
    if details[0] == "" or details[1] == "":
        libgen = clean(onelib(details), details)
        output(libgen)
        print(description(libgen))

    else:
        libgen = clean(bothlib(details), details)
        output(libgen)
        print(description(libgen))

        more = input("Do you want to see additional results? (y/n) ").lower()
        if more == "y":
            others = otherlib(details, libgen)
            if others != None:
                output(others)
                print(description(others))
            else:
                print("No additional results")

    print("Thank you!")


def names():
    # Returns the user input of book and/or author.

    book = input("Book: ").strip()
    author = input("Author: ").strip()
    if book == "" and author == "":
        sys.exit("No inputs")
    else:
        return [book, author]


def bothlib(details):
    # Does an exact match search of book and author on Libgen and returns results

    s = LibgenSearch()
    title_filters = {"Author": details[1].title()}
    results = s.search_title_filtered(
        details[0].title(), title_filters, exact_match=True
    )
    if results == []:
        return "No exact match results"
    else:
        return results


def onelib(details):
    # Does a search of a book OR an author on Libgen and returns results

    s = LibgenSearch()

    if details[0] == "":
        results = s.search_author(details[1])
    else:
        results = s.search_title(details[0])

    if results == []:
        sys.exit("No matches")
    else:
        return results


def otherlib(details, exact):
    # Does a non-exact filtered search of book name with author. Returns results not in exact search, else None.

    s = LibgenSearch()
    auth = details[1].title()

    title_filters = {"Author": auth}
    initial = s.search_title_filtered(details[0], title_filters, exact_match=False)

    if exact != []:
        initial = clean(initial, details)
        results = [i for i in initial if i not in exact]
    if results == []:
        return None  # sys.exit("No additional matches") # change to return None?

    else:
        clean(results, details)
        return results


def clean(results, details):
    # Cleans the JSON output from Libgen API
    for result in results:
        for i in range(2, 6):
            try:
                mir = "Mirror_" + str(i)
                result.pop(mir)
            except KeyError:
                pass
        try:
            del result["ID"]
            del result["Year"]
            del result["Pages"]
            del result["Language"]
            del result["Size"]
            if result["Publisher"] == "":
                del result["Publisher"]
        except KeyError:
            pass
    return results


def description(libgen):
    ...
    # Calls the imported google function on user chosen input, selected from Libgen results.
    des = input(
        "Do you want to see a description of a book? from the above list? (y/n) "
    )
    if des == "y":
        index = int(input("Please type the index number of the chosen book result: "))
        try:
            bookdet = [libgen[index]["Title"], libgen[index]["Author"]]
        except IndexError:
            return "Index not in range"

        search = google(bookdet)

        if search == None:
            return "No descriptions available"
        else:
            return json.dumps(search, ensure_ascii=False, indent=2)
    else:
        return "\n"


def output(results):
    # Outputs results with index and formatting

    for i in range(len(results)):
        print(i, json.dumps(results[i], indent=2))


if __name__ == "__main__":
    # Call main
    main()
