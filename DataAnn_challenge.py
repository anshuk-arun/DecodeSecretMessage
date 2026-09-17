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
            # print(f"DEBUG: found y coord, {i}, {i+1}, {tagStr}")
            startIndex = i + 1
            break
    
    # Format is X Coordinate, Character, Y Coordinate
    # X Coordinate Increasing means stepping right across grid, which means columns, which means second index in 2d array
    # Y coordinate increasing means stepping down the grid, which means rows, which means first index in 2d array
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
                    xCoord = int(tags[i].text)
                    print(f"X: {xCoord}", end=" || ")
                    decodeTypeCounter = decodeTypeCounter + 1
            case 1:
                code = tags[i].text
                print(f"Code: {code}", end=" || ")
                decodeTypeCounter = decodeTypeCounter + 1
            case 2:
                if (tags[i].text.isdigit()):
                    yCoord = int(tags[i].text)
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

    # Initializing the Grid
    grid = [[" " for i in range(len(arr))] for j in range(len(arr))]

    print(f"DEBUG: {grid}")    
    for line in grid:
        for elem in line:
            print(elem, end="")
        print()
    print("End DEBUG GRID")

    for elem in range(len(arr)):
        
        # Format is [(X, Y) , Code]
        # X Coordinate Increasing means stepping right across grid, which means columns, which means second index in 2d array
        # Y coordinate increasing means stepping down the grid, which means rows, which means first index in 2d array
        point = arr[elem][0]
        x = point[0]
        y = point[1]

        code = arr[elem][1]
        print(f"DEBUG: Point: {point} = Row {y} Col {x} || Code: {code}")
        
        grid[y][x] = code

        print("DEBUG Grid Update")
        for line in grid:
            for elem in line:
                print(elem, end="")
            print()
    

    # Rows, Bottom to Top
    for row in range(len(grid)-1, -1, -1):
        # Cols, Left to Right
        for col in range(len(grid)):
            print(grid[row][col], end="")
        print()
    
    # TEST: Message Prints correctly!
    


def main():

    # Needed Variables
    inputStr = ""

    # Take Input of URL to decode from
    print("Please enter the URL to decode: ")
    inputStr = input()

    # Decode the URL
    if (inputStr == ""):
        print(f"DEBUG: Default URL is being used.")
        decodeUrl()

    else:
        print(f"DEBUG: The URL given is {inputStr}")
        decodeUrl(inputStr)


if __name__ == "__main__":
    print("Data Annotation - Decode Secret Message")
    main()


