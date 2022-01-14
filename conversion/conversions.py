# IMPORTS
import pytesseract
import cv2
import conversion.formulaConvert as formulaConvert

# Tesseract location
pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'

'''
Function returns list containing each word in the formula name (also converted to all lowercase)
'''
def configureName(formulaName):
    # .strip() -> Remove spaces from each side of formula name
    # .lower() -> Convert all letters to lowercase
    # .split() -> Put each word in formula name as an index of a list
    return formulaName.strip().lower().split()

'''
Function converts image to text and returns TUPLE containing formula name, and converted chemical formula
* 3 parts to function:
1. Convert image to text, check if text can be converted (if yes, return tuple, if not, continue to part 2)
2. Apply slight binary threshold, check if text can be converted (if yes, return tuple, if not, continue to part 3)
3. Apply strong binary threshold, return tuple containing formula name and converted chemical formula

Parameters
- filename (name of image file)
'''
def imageToChemicalFormula(filename):
    # Part 1
    # Find and read image
    image = cv2.imread('static/uploads/' + filename) # Try both
    # Convert image to string
    formulaName = pytesseract.image_to_string(image)
    # Attempt to convert string to chemical formula
    chemicalFormula = formulaConvert.convertToFormula(configureName(formulaName))
    # Return tuple if valid chemical formula
    if chemicalFormula:
        return (formulaName, chemicalFormula)

    # Part 2
    # Make image gray (must be gray for binary threshold to work)
    imgGrey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply slight binary threshold
    _, threshedImage = cv2.threshold(imgGrey, 70, 255, cv2.THRESH_BINARY)
    # Convert image to string
    formulaName = pytesseract.image_to_string(threshedImage)
    # Attempt to convert string to chemical formula
    chemicalFormula = formulaConvert.convertToFormula(configureName(formulaName))
    # Return tuple if valid chemical formula
    if chemicalFormula:
        return (formulaName, chemicalFormula)
    
    # Part 3
    # Apply strong binary threshold
    _, threshedImage = cv2.threshold(imgGrey, 130, 255, cv2.THRESH_BINARY)
    # Convert image to string
    formulaName = pytesseract.image_to_string(threshedImage)
    # Return tuple with formula name + chemical formula
    return (formulaName, formulaConvert.convertToFormula(configureName(formulaName)))

'''
Function converts text and returns TUPLE containing formula name, chemical formula

Parameters
- formulaName (formula name to be converted to chemical formula)
'''
def textToChemicalFormula(formulaName):
    configuredName = configureName(formulaName)
    return (formulaName, formulaConvert.convertToFormula(configuredName))