'''-----------------------------------------------------------------------------
Name:        ChemCam
Purpose:     To provide a resource for grade 11U chemistry students to be able to check their nomenclature by using ChemCam to convert formula names to chemical formulas
Author:      Evan Dennison
Created:     10-Dec-2021
Updated:     14-Jan-2022
-----------------------------------------------------------------------------
I think this project deserves a level 4+ because ChemCam is a very user friendly, well designed, 
responsive website that allows grade 11U chemistry students to check their homework. Furthermore,
this website has the ability to upload an image of a formula name, and convert it to text using pytesseract.
This means that I not only met the level 4 requirements for the project, but I also learned and applied new things
to my project that wasn't taught in the course (image upload, pytesseract, cv2 binary threshold, etc.). Another 
aspect of my program that I am proud of is the ability for my formula conversion algorithm to detect when a formula isn't valid.
This means that no matter what you type in the input field, the program won't crash, but unless the formula syntax is spot on,
it won't provide you with the chemical formula.

Features Added:
- Input/output forms (conversion page)
- Used 'if', 'or', 'and', 'elif', 'else' conditional statements
- Used loop structures
- Used built-in functions + properties (ex, len(), .lower())
- Created + used custom functions
- Used multiple lists + dictionaries (mostly found in formulaConvert.py file in conversion folder) 
- Read/write to external file (read from json file, read/write to pastConversions.txt file)
- Intro screen (home page), main screen (conversion page), end screen (didn't include any extra pages that I didn't need to improve user efficiency)
- Project fully documented + follows naming conventions
- Code is efficient + fast and clear user interface
- Data input fully sanitized
- Modular program

EXTRA FEATURES:
- Created my project as a website using Flask framework
- Used pytesseract to convert image to text
    - Use cv2 to apply binary threshold to image to improve pytesseract accuracy
- Used os library to upload and delete user inputted images (images stored in static/uploads)
- Used JavaScript (static/js/inputChange.js) to disable input not being used + only make the input being used required
- Used bootstrap + css to make a responsive website
- Used Json file to store element/polyatomic ion charges + symbols
- Used flask 'flash' and bootstrap to create well designed error messages

WEBSITE LINK:


PROJECT DIRECTORY:
- conversion (folder)
    - conversions.py (image-to-text file)
    - formulaConvert.py (formula name conversion algorithm)
- static (folder)
    - css (folder w/ css file)
    - img (folder w/ images used in website)
    - js (folder)
        - inputChange.js (disables input not being inputted in/changes required input fields based on user input)
    - uploads (folder - location where user inputted images are uploaded to)
- templates (folder)
    - base.html (base file)
    - convert.html (conversion page)
    - help.html (help page)
    - index.html (home page)
    - past-conversions.html (past conversions page)
- elements.json (contains all element/polyatomic ion charges + symbols)
- main.py (main server file - all the flask stuff)
- pastConversions.txt (text file that stores past conversions)
-----------------------------------------------------------------------------'''

# IMPORTS
from flask import Flask, render_template, url_for, request, flash
import os 
from werkzeug.utils import secure_filename
import conversion.formulaConvert as formulaConvert
import conversion.conversions as conversions

# CONSTANTS
UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# SETUP
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['UPLOAD_FOLDER'] = 'static/uploads/'

# FUNCTIONS
'''
Function returns 'True' if files extension is supported by ChemCam

Parameters
- filename (filename being tested whether contains valid extension)
'''
def allowedFile(filename):
    # .rsplit() used to set max split value
    # Returns True if . in filename and the letters after dot are a valid extension
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

'''
Function updates and returns list containing last 10 converted formulas

Parameters 
- pastConversions (list of converted formulas which is to be updated)
- formulaName (name of the formula in last conversion)
- chemicalFormula (chemical formula in last conversion)
'''
def updatePastConversions(pastConversions, formulaName, chemicalFormula):
    # Remove oldest conversion if added conversion will put # of past conversions over 10 (only shows last 10 conversions)
    if len(pastConversions) >= 10:
        pastConversions.pop()
    # Inserts newest conversion to front of past conversions list
    pastConversions.insert(0, f"<p class='past-conversion'><b>{formulaName}</b> to <b>{chemicalFormula}</b></p>\n")
    return pastConversions

'''
Function applies html <sub> tags to add a subscript to the appropriate areas of the formula
Function returns updated formula

Parameters
- formula (formula which is being configured)
'''
def convertToHTML(formula):
    # Set starting string
    formulaHTML = ''
    # Loop through each character in formula
    for i in range(len(formula)):
        # Put subcript on number beside elements (# of atoms)
        if formula[i].isdigit():
            formulaHTML += f'<sub>{formula[i]}</sub>'
        # Put subscript on state (ex: (aq))
        elif formula[i:] in formulaConvert.states.values():
            formulaHTML += f'<sub>{formula[i:]}</sub>'
            break
        # Add unchanged character to HTML string
        else:
            formulaHTML += formula[i]
    return formulaHTML

# ROUTES
@app.route('/')
# Home page
def home():
    # Show home page file
    return render_template('index.html', title='Home')

# Conversion page
@app.route('/convert', methods=['GET', 'POST'])
def convert():
    # Set default chemical formula string
    chemicalFormula = ''
    # If input given
    if request.method == 'POST':
        # Control variable to know if valid input
        invalid = False
        # Photo was inputted
        if request.files:
            # Check if image in request dict
            if 'formula-image' not in request.files:
                invalid = True 
                flash('No file part', 'danger')
            # Ensure value is an image
            if request.files['formula-image'].filename == '':
                invalid = True
                flash('No image selected for uploading', 'danger')
            # Check if valid image name and file extension is valid
            if request.files['formula-image'] and allowedFile(request.files['formula-image'].filename):
                # Get filename, upload image to server
                filename = secure_filename(request.files['formula-image'].filename)
                request.files['formula-image'].save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                # Convert image to text
                formulaResult = conversions.imageToChemicalFormula(filename)
                # Remove image from server
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # Invalid file type
            else:
                invalid = True
                flash('Allowed image types are - png, jpg, jpeg', 'danger')
        # Text was inputted
        else:
            formulaResult = conversions.textToChemicalFormula(request.form['formula-name'])
        
        # If valid file
        if not invalid:
            formulaName = formulaResult[0]
            chemicalFormula = formulaResult[1]

            # Check if valid chemical formula
            if chemicalFormula:
                # Add subscripts to characters that should be subscripted in formula
                chemicalFormula = convertToHTML(chemicalFormula)
                
                # Write to past conversions file
                file = open('pastConversions.txt', 'r')
                fileContents = file.readlines()
                file.close()

                pastConversions = updatePastConversions(fileContents, formulaName, chemicalFormula)

                file = open('pastConversions.txt', 'w')
                file.write(''.join(pastConversions))
                file.close()
            # Invalid formula name
            else:
                flash('Unable to convert formula. Please try again.', 'danger')
    # Show conversion page 
    return render_template('convert.html', title='Convert', chemicalFormula=chemicalFormula)

# Help page
@app.route('/help')
def helpScreen():
    # Show help page
    return render_template('help.html', title='Help')

# Recent conversions page
@app.route('/past-conversions')
def pastConversions():
    # Read past conversions file
    file = open('pastConversions.txt', 'r')
    fileContents = file.readlines()
    file.close()

    htmlString = ''
    
    # Convert list to string and eliminate '\n'
    for item in fileContents:
        itemStrip = item.strip()
        htmlString += itemStrip

    # Show recent conversions page
    return render_template('past-conversions.html', title='Past Conversions', pastConversions=htmlString)

# Run app
if __name__ == '__main__':
    app.run(debug=False)



