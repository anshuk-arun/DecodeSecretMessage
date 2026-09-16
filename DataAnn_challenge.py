from bs4 import BeautifulSoup
import requests

# Example URL = "https://docs.google.com/document/d/e/2PACX-1vTMOmshQe8YvaRXi6gEPKKlsC6UpFJSMAk4mQjLm_u1gmHdVVTaeh7nBNFBRlui0sTZ-snGwZM4DBCT/pub"
# Verification URL = https://docs.google.com/document/d/e/2PACX-1vSvM5gDlNvt7npYHhp_XfsJvuntUhq184By5xO_pA4b_gCWeXb6dM6ZxwN8rE6S4ghUsCj2VKR21oEP/pub

exampleURL = "https://docs.google.com/document/d/e/2PACX-1vTMOmshQe8YvaRXi6gEPKKlsC6UpFJSMAk4mQjLm_u1gmHdVVTaeh7nBNFBRlui0sTZ-snGwZM4DBCT/pub"

def decodeUrl(url=f"{exampleURL}"):
    
    outputArr = []

    # BS4 Decodes
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")
    tags = doc.find_all("span")
    
    # Find Index of Message data
    startIndex = 0
    for i in range(len(tags)):

        tagStr = tags[i].text
        
        if(tagStr == "y-coordinate"):
            print(f"found y coord, {i}, {i+1}, {tagStr}")
            startIndex = i + 1
            break
    
    # Format is X Coordinate, Character, Y Coordinate
    # counter increments, at 2 - the y coordinate - inputs the code into array, then variables reset
    decodeTypeCounter = 0
    xCoord = -1
    yCoord = -1
    code = ""

    # Retrieving the Points and Coded Message
    for i in range(startIndex, len(tags)):
        match decodeTypeCounter:
            case 0:
                if (tags[i].text.isdigit()):
                    xCoord = tags[i].text
                    print(f"X: {xCoord}", end=" || ")
                    decodeTypeCounter = decodeTypeCounter + 1
            case 1:
                code = tags[i].text
                print(f"Code: {code}", end=" || ")
                decodeTypeCounter = decodeTypeCounter + 1
            case 2:
                if (tags[i].text.isdigit()):
                    yCoord = tags[i].text
                    print(f"Y: {yCoord}")

                    # Insert code into array
                    outputArr.append([(xCoord, yCoord), code])
                    # Reset the variables
                    decodeTypeCounter = 0
                    xCoord = -1
                    yCoord = -1
                    code = ""
            case _:
                print("ERROR: Unknown Count")

    # Calls helper function
    # Prints the grid of characters specified by input data, displaying a graphic of correctly oriented Uppercase Letters
    finalMessage = printSecretMessage(outputArr)
    return finalMessage


def printSecretMessage(arr=[(0, 0), "N/A"]):

    # DEBUG Print the array
    for i in range(len(arr)):
        print(arr[i])
    


def main():

    # Needed Variables
    inputStr = ""
    result = "DEBUG: This is where the result goes"

    # Take Input of URL to decode from
    print("Please enter the URL to decode: ")
    inputStr = input()

    # Decode the URL
    if (inputStr == ""):
        print(f"DEBUG: Default URL is being used.")
        result = decodeUrl()

    else:
        print(f"DEBUG: The URL given is {inputStr}")
        result = decodeUrl(inputStr)

    # Print out the Result for DEBUG
    print(f"DEBUG: Result of decodeUrl \n {result}")


if __name__ == "__main__":
    print("Data Annotation - Decode Secret Message")
    main()



# prices = doc.find_all(text="$")
# print(prices)

# print(doc.prettify())


# with open("index.html", "r") as f:
#     doc = BeautifulSoup(f, "html.parser")

# tags = doc.find_all("p")
# print(tags)
# tag = doc.title
# tag.string = "hello"
# print(doc)

# print(tag.string)
# print(tag)
# print(doc.prettify())
