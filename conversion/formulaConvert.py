# IMPORTS
import json
import math

# DICTIONARIES
# States
states = {'solid': '(s)', 'liquid': '(l)', 'gas': '(g)', 'metal': '(s)', 'vapour': '(g)', 'powder': '(s)', 'flakes': '(s)', 'solution': '(aq)', 'aqueous': '(aq)'}

# Acid prefixes/suffixes
acidPrefixes = {'per': 1, 'hypo': -1}
acidSuffixes = {'ic': 0, 'ous': -1}

# Binary acid conversions
binaryAcids = {
    'carbonic': 'carbon',
    'nitric': 'nitrogen',
    'fluoric': 'fluorine',
    'silicic': 'silicon',
    'phosphoric': 'phosphorus',
    'sulfuric': 'sulfur',
    'sulphuric': 'sulphur',
    'chloric': 'chlorine',
    'arsenic': 'arsenic',
    'selenic': 'selenium',
    'bromic': 'bromine',
    'antimonic': 'antimony',
    'telluric': 'tellurium',
    'iodic': 'iodine'
}

# Roman numerals (used for multivalent compounds)
romanNumerals = {
    'i': 1,
    'ii': 2,
    'iii': 3,
    'iv': 4,
    'v': 5,
    'vi': 6,
    'vii': 7,
    'viii': 8,
    'ix': 9
}

# Greek prefixes
covalentBondPrefixes = {
    'mono': 1,
    'di': 2,
    'tri': 3,
    'tetra': 4,
    'penta': 5,
    'hexa': 6,
    'hepta': 7,
    'octa': 8,
    'nona': 9,
    'deca': 10
}

# Anion conversions
anionRootNames = {
    'carb': 'carbon',
    'nitr': 'nitrogen',
    'ox': 'oxygen',
    'fluor': 'fluorine',
    'silic': 'silicon',
    'phosph': 'phosphorus',
    'sulf': 'sulfur',
    'sulph': 'sulphur',
    'chlor': 'chlorine',
    'arsen': 'arsenic',
    'selen': 'selenium',
    'brom': 'bromine',
    'antim': 'antimony',
    'tellur': 'tellurium',
    'iod': 'iodine',
    'hydr': 'hydrogen',
    'cyan': 'cyanide'
}

# Oxy Acid conversions
acidRootNames = {
    'acet': 'acetate',
    'arsen': 'arsenate',
    'bor': 'borate',
    'brom': 'bromate',
    'carbon': 'carbonate',
    'chlor': 'chlorate',
    'chrom': 'chromate',
    'cyan': 'cyanate',
    'dichrom': 'dichromate',
    'iod': 'iodate',
    'nitr': 'nitrate',
    'oxal': 'oxalate',
    'mangan': 'manganate',
    'phosphor': 'phosphate',
    'silic': 'silicate',
    'sulphur': 'sulphate',
    'sulfur': 'sulfate',
    'thiosulphur': 'thiosulphate',
    'thiosulfur': 'thiosulfate'
}

# Polyatomic anion conversions
polyatomicRootNames = {
    'acet': 'acetate',
    'arsen': 'arsenate',
    'bor': 'borate',
    'brom': 'bromate',
    'carbon': 'carbonate',
    'chlor': 'chlorate',
    'chrom': 'chromate',
    'cyan': 'cyanate', 
    'dichrom': 'dichromate',
    'hydrox': 'hydroxide', 
    'iod': 'iodate',
    'nitr': 'nitrate',
    'oxal': 'oxalate', 
    'mangan': 'manganate',
    'phosph': 'phosphate',
    'silic': 'silicate',
    'sulph': 'sulphate',
    'sulf': 'sulfate',
    'thiocyan': 'thiocyanate',
    'thiosulph': 'thiosulphate',
    'thiosulf': 'thiosulfate',
    # Polyatomic anions that end in 'ide'
    'peroxide': 'peroxide',
    'cyanide': 'cyanide'
}

# LISTS
# Diatomic elements
diatomicElements = ['hydrogen', 'oxygen', 'fluorine', 'bromine', 'iodine', 'nitrogen', 'chlorine']

test = ['barium nitride', 'beryllium hypocarbonite', 'copper (I) bromide', 'chlorous acid', 'dinitrogen trioxide', 'mercury (I) peroxide', 'antimony (V) chromate', 'lithium hydrogen phosphite', 'xenon gas', 'titanium (IV) chloride', 'calcium phosphide', 'tetracarbon octahydride', 'magnesium selenide', 'hydrophosphoric acid', 'cobalt (III) iodite', 'copper (I) peroxide', 'lead (II) permanganate', 'potassium hydrogen carbonite']

'''
Shortened greek prefixes
- When an element starts with a vowel the last letter of greek prefix sometimes removed (ex: heptoxide instead of heptaoxide)
- List used to identify these shortened prefixes
- Note: 'di' and 'tri' not included in list as the last letter is never removed
'''
shortenedCovalentBondPrefixes = ['mon', 'tetr', 'pent', 'hex', 'hept', 'oct', 'non', 'dec']

# GENERAL FUCTIONS
'''
Function returns TUPLE containing # of each particle to create a balanced formula

Parameters
- chargeOne (charge of first particle)
- chargeTwo (charge of second particle)
'''
def balanceFormula(chargeOne, chargeTwo):
    chargeLcm = math.lcm(chargeOne, abs(chargeTwo)) # Determine lowest common multiple of 2 charges
    numParticleOne = int(chargeLcm/chargeOne) # Divide LCM by charge 1 to get # atoms of particle 1
    numParticleTwo = int(chargeLcm/abs(chargeTwo)) # Divide LCM by charge 2 to get # atoms of particle 2
    return (numParticleOne, numParticleTwo)

'''
Function returns True if element in elementsDict
* Used to determine whether string is an element

Parameters
- element (name of element)
'''
def isElement(element):
    if element in elementsDict.keys():
        return True 

'''
Function credit to https://www.w3resource.com/python-exercises/python-basic-exercise-24.php
Function returns True if character is a vowel

Parameters
- char (character to determine if it's a vowel)
'''
def isVowel(char):
    allVowels = 'aeiou'
    return char in allVowels

'''
Function returns 'True' if element is diatomic
Returns False otherwise

Paramaters
- element (element used to determine whether diatomic)
'''
def isDiatomic(element):
    if element in diatomicElements:
        return True 
    return False

'''
Function returns True if element ends in 'ide' AND element exists
* Used to determine whether string is an element AND proper anion syntax is used

Parameters
- element (string used to determine whether a valid anion)
'''
def isAnion(element):
    if element.endswith('ide'):
        newElement = element[:len(element)-3]
        if newElement in anionRootNames.keys():
            return True
    return False

'''
Function returns True if ion is in polyatomicIonsDict
* Used to determine whether ion is polyatomic

Parameters
- ion (ion to test whether polyatomic)
'''
def isPolyatomicIon(ion):
    if ion in polyatomicIonsDict.keys():
        return True 
    return False

'''
If element has negative charge, function returns TUPLE containing 'True', and the element's negative charge
If element doesn't have negative charge, function returns TUPLE with the value 'False'

Parameters
- element (string used to determine negative charge)
'''
def findNegativeCharge(element):
    if element in elementsDict.keys():
        for charge in elementsDict[element]['charges']:
            if charge < 0:
                return (True, charge)
    return (False, '')

'''
If element has positive charge, function returns TUPLE containing 'True', and the element's positive charge
If element doesn't have positive charge, function returns TUPLE with the value 'False'

Parameters
- element (string used to determine positive charge)
'''
def findPositiveCharge(element):
    if element in elementsDict.keys():
        for charge in elementsDict[element]['charges']:
            if charge > 0:
                return (True, charge)
    return (False, '')

'''
If anion is valid, function returns TUPLE containing 'True', the anion symbol, and the anion charge
If anion is not valid, function returns TUPLE with the value 'False'

Parameters
- anion (string used to determine whether valid anion)
'''
def convertAnion(anion):
    if anion.endswith('ide'):
        anion = anion[:len(anion)-3]
        if anion in anionRootNames.keys():
            anion = anionRootNames[anion]
            for charge in elementsDict[anion]['charges']:
                if charge < 0:
                    anionSymbol = elementsDict[anion]['symbol']
                    anionCharge = charge
                    return (True, anionSymbol, anionCharge)
    return (False, '', '')

'''
Function returns chemical formula as string based on cation/anion symbol and their # of atoms

Parameters
- cation (symbol of positively charged particle)
- numCations (# of cation atoms)
- anion (symbol of negatively charged particle)
- numAnions (# of anion atoms)
'''
def getChemicalFormula(cation, numCations, anion, numAnions, state=''):
    # If cation is polyatomic and more than 1, put brackets around it
    if (sum(1 for c in cation if c.isupper()) > 1) and (numCations > 1):
        cation = f'({cation})'
    # If anion is polyatomic and more than 1, put brackets around it 
    if ((sum(1 for a in anion if a.isupper()) > 1) or anion == 'O2') and (numAnions > 1):
        anion = f'({anion})'
    
    # If only 1 atom, don't need to show number in formula
    numCations = numCations if numCations > 1 else ''
    numAnions = numAnions if numAnions > 1 else ''

    # Make chemical formula a string and return it
    chemicalFormula = f'{cation}{numCations}{anion}{numAnions} {state}'
    return chemicalFormula

'''
Function returns 'True' if first particle is positively charged and second particle is negatively charged
Returns 'False' otherwise

Parameters
- chargeOne (charge of first particle)
- chargeTwo (charge of second particle)
'''
def canBeBalanced(chargeOne, chargeTwo):
    # If chargeOne positive and chargeTwo negative return True
    if (chargeOne > 0) and (chargeTwo < 0):
        return True 
    return False

# ACID FUNCTIONS
'''
If valid prefixes/suffixes, function returns TUPLE containing 'True', acid name, and # oxygen atoms that must be added/subtracted from acid
If not valid prefixes/suffixes, function returns TUPLE containing 'False'
'''
def calcOxyAcidOxygen(acidName):
    oxygenDiff = 0 # Used to hold # of oxygen atoms that must be +/-
    if acidName.endswith('ic'):
        acidName = acidName[:len(acidName)-2] # Acid name without 'ic'
        if acidName.startswith('per'):
            oxygenDiff += 1 # Prefix of 'per' results in +1 oxygen atom
            acidName = acidName[3:] # Acid name without 'per'
        return (True, acidName, oxygenDiff)
    elif acidName.endswith('ous'):
        oxygenDiff -= 1 # Suffix of 'ous' results in -1 oxygen atom
        acidName = acidName[:len(acidName)-3] # Acid name without 'ous'
        if acidName.startswith('hypo'):
            oxygenDiff -= 1 # Prefix of 'hypo' results in -1 oxygen atom
            acidName = acidName[4:] # Acid name without 'hypo'
        return (True, acidName, oxygenDiff)
    return (False, '', '')

# COVALENT BOND FUNCTIONS
'''
If valid elements + greek prefixes, function returns TUPLE containing:
- 'True'
- Name of first element
- # of atoms of first element
- Name of second element
- # of atoms of second element
If not valid elements or greek prefixes, function returns TUPLE with the value 'False'

Parameters
- elementOne (first element)
- elementTwo (second element)
'''
def calcCovalentPrefixes(elementOne, elementTwo):
    numElementOne = 1 # If no prefix on elementOne # of atoms defaults to 1
    foundElementTwo = False # Must be a prefix on second element (even if 1 atom)
    # Find # atoms of first element
    for prefix in covalentBondPrefixes.keys():
        if elementOne.startswith(prefix):
            newElementOne = elementOne[len(prefix):] # Contains element with prefix removed
            # Set name/# atoms of element one if element exists
            if isElement(newElementOne):
                elementOne = newElementOne
                numElementOne = covalentBondPrefixes[prefix]
                break 
        shortenedPrefix = prefix[:len(prefix)-1] # Get prefix with last letter removed
        '''
        In order for a shortened prefix to be valid:
        - Element must start with shortened prefix
        - First letter of element must be a vowel
        - Shortened prefix must be in shortenedCovalentBondPrefixes dict (since some greek prefixes don't follow this rule, eg, 'tri')
        '''
        if elementOne.startswith(shortenedPrefix) and isVowel(elementOne[len(prefix)-1]) and (shortenedPrefix in shortenedCovalentBondPrefixes):
            newElementOne = elementOne[len(prefix)-1:] # Contains element without shortened prefix
            # Set name/# atoms of element one if element exists
            if isElement(newElementOne):
                elementOne = newElementOne
                numElementOne = covalentBondPrefixes[prefix]
                break
    # Find # atoms of second element
    for prefix in covalentBondPrefixes.keys():
        if elementTwo.startswith(prefix):
            newElementTwo = elementTwo[len(prefix):] # Contains root element name without prefix
            # Set name/# atoms of element two if root name exists
            if newElementTwo in anionRootNames.keys():
                elementTwo = newElementTwo
                numElementTwo = covalentBondPrefixes[prefix]
                foundElementTwo = True # Found element two
                break 
        shortenedPrefix = prefix[:len(prefix)-1] # Get prefix with last letter removed
        if elementTwo.startswith(shortenedPrefix) and isVowel(elementTwo[len(prefix)-1]) and (shortenedPrefix in shortenedCovalentBondPrefixes):
            newElementTwo = elementTwo[len(prefix)-1:] # Contains root element name without shortened prefix
            # Set name/# atoms of element two if root name exists
            if newElementTwo in anionRootNames.keys():
                elementTwo = newElementTwo
                numElementTwo = covalentBondPrefixes[prefix]
                foundElementTwo = True # Found element two
                break
    if foundElementTwo:
        return (True, elementOne, numElementOne, elementTwo, numElementTwo)
    return (False, '', '', '', '')

'''
If valid elements + greek prefixes, function returns TUPLE containing:
- 'True'
- Symbol of first element
- # of atoms of first element
- Symbol of second element
- # of atoms of second element
If not valid elements or greek prefixes, function returns TUPLE with the value 'False'

Parameters
- elementOne (first element)
- elementTwo (second element)
'''
def convertCovalentFormula(elementOne, elementTwo):
    if elementTwo.endswith('ide'):
        elementTwo = elementTwo[:len(elementTwo)-3]

        # Determine # atoms of element one/two, name of element one/two
        elementResult = calcCovalentPrefixes(elementOne, elementTwo)
        if elementResult[0]:
            elementOne = elementResult[1]
            numElementOne = elementResult[2]
            elementTwo = elementResult[3]
            numElementTwo = elementResult[4]
        else: 
            return (False, '', '', '', '')

        # Find full name of element two in exists
        if elementTwo in anionRootNames.keys():
            elementTwo = anionRootNames[elementTwo]
        else:
            return (False, '', '', '', '')

        # Return 'True' if both elements are valid and have negative charges
        if isElement(elementOne) and isElement(elementTwo):
            if findNegativeCharge(elementOne)[0] and findNegativeCharge(elementTwo)[0]:
                symbolOne = elementsDict[elementOne]['symbol']
                symbolTwo = elementsDict[elementTwo]['symbol']
                return (True, symbolOne, numElementOne, symbolTwo, numElementTwo)
    return (False, '', '', '', '')

# POLYATOMIC ION FUNCTIONS
'''
If valid prefixes/suffixes, function returns TUPLE containing 'True', polyatomic ion name, and # of oxygen atoms that must be added/subtracted from ion 
If not valid prefixes/suffixes, function returns TUPLE containing 'False'

Parameters
- ion (polyatomic ion to convert)
'''
def calcPolyOxygen(ion):
    oxygenDiff = 0 # Used to hold # oxygen atoms that must be +/-
    if ion.endswith('ate'):
        ion = ion[:len(ion)-3] # Ion without 'ate'
        if ion.startswith('per'):
            oxygenDiff += 1 # +1 oxygen atom if prefix of 'per'
            ion = ion[3:] # Ion without 'per'
        return (True, ion, oxygenDiff)
    elif ion.endswith('ite'):
        oxygenDiff -= 1 # -1 oxygen atom if suffix of 'ite'
        ion = ion[:len(ion)-3] # Ion without 'ite'
        if ion.startswith('hypo'):
            oxygenDiff -= 1 # -1 oxygen atom if prefix of 'hypo'
            ion = ion[4:] # Ion without 'hypo'
        return (True, ion, oxygenDiff)
    # For polyatomic ions ending in 'ide' (no change to # oxygen atoms)
    elif ion.endswith('ide'):
        return (True, ion, 0)
    else:
        return (False, '', '')

'''
If valid # of oxygen atoms added/remove from polyatomic ion, function returns TUPLE containing 'True', and polyatomic ion formula
If not valid # oxygen atoms, function returns TUPLE containing 'False'

Parameters
- polyatomicIonSymbol (polyatomic ion which is getting it's # oxygen atoms changed)
- oxygenDiff (# oxygen atoms to +/-)
'''
def calcPolyFormula(polyatomicIonSymbol, oxygenDiff): 
    oxygenIndex = polyatomicIonSymbol.find('O') # Contains index of oxygen atom (allows to find # oxygen atoms)
    # If 1 oxygen atom
    if (oxygenIndex == len(polyatomicIonSymbol) - 1) or (polyatomicIonSymbol[oxygenIndex + 1].isalpha()): # no index overflow
        baseOxygenNum = 1 
    # If more than 1 oxygen atom
    else:
        baseOxygenNum = int(polyatomicIonSymbol[oxygenIndex + 1]) # Contains # oxygen atoms in base polyatomic ion

    numOxygens = baseOxygenNum + oxygenDiff # Number of oxygen atoms present in updated polyatomic ion
    # Make sure valid # of oxygen atoms
    if numOxygens >= 1:
        # If ion started with 1 oxygen atom
        if baseOxygenNum == 1:
            # If ion starts with 1 oxygen atom and ends with 1 then no change
            # Update # oxygen atoms
            if numOxygens > 1:
                polyatomicIonSymbol = polyatomicIonSymbol[:oxygenIndex + 1] + str(numOxygens) + polyatomicIonSymbol[oxygenIndex + 1:]
        # If ion started with more than 1 oxygen atom
        else: 
            # If updated ion has 1 oxygen atom
            if numOxygens == 1:
                polyatomicIonSymbol = polyatomicIonSymbol[:oxygenIndex + 1] + polyatomicIonSymbol[oxygenIndex + 2:]
            # If updated ion has more than 1 oxygen atom
            else:
                polyatomicIonSymbol = polyatomicIonSymbol[:oxygenIndex + 1] + str(numOxygens) + polyatomicIonSymbol[oxygenIndex + 2:]
        return (True, polyatomicIonSymbol)
    return (False, '')

'''
Function returns polyatomic ion formula and charge

Parameters:
- ion (polyatomic ion to be converted)
'''
def convertPolyatomicIon(ion):
    ionResult = calcPolyOxygen(ion)
    # If true, get root ion name and oxygen difference
    if ionResult[0]:
        ion = ionResult[1]
        oxygenDiff = ionResult[2]

        # If valid root ion name, get ion name and formula
        if ion in polyatomicRootNames.keys():
            ionName = polyatomicRootNames[ion]
            ionFormula = polyatomicIonsDict[ionName]['symbol']

            formulaResult = calcPolyFormula(ionFormula, oxygenDiff)
            # If ture, return ion formula and charge
            if formulaResult[0]:
                ionFormula = formulaResult[1]
                ionCharge = polyatomicIonsDict[ionName]['charge']
                return (True, ionFormula, ionCharge)
    return (False, '', '')

# ACID RADICAL FUNCTIONS
'''
If valid acid radical syntax, function returns TUPLE containing 'True' and # of hydrogen atoms
If not valid acid radical syntax, function returns TUPLE containing 'False'

Parameters
- hydrogen (string used to determine # hydrogen atoms)
'''
def calcHydrogenPrefixes(hydrogen):
    numHydrogens = 1 # Set base # hydrogen atoms (1 hydrogen atom if no prefix)
    # Loop through all prefixes
    for prefix in covalentBondPrefixes.keys():
        # If hydrogen starts with prefix
        if hydrogen.startswith(prefix):
            numHydrogens = covalentBondPrefixes[prefix] # Set number of hydrogen atoms
            hydrogen = hydrogen[len(prefix):] # Contains string without prefix
            break 
    # If string without prefix is 'hydrogen', syntax is valid
    if hydrogen == 'hydrogen':
        return (True, numHydrogens)
    return (False, 0)

'''
Function returns TUPLE containing 'True', the balanced acid radical, and acid radical charge if the formula is valid
Functions returns TUPLE containing 'False' if acid radical charge is invalid

Parameters 
- numHydrogens (# hydrogen atoms)
- anion (polyatomic anion to bond to hydrogen atoms)
- anionCharge (charge of polyatomic anion)
'''
def balanceAcidRadical(numHydrogens, anion, anionCharge):
    # Determine overall charge of acid radical
    overallCharge = numHydrogens + anionCharge 
    # Overall charge must be negative
    if overallCharge < 0:
        hydrogenSymbol = f'H{numHydrogens}' if numHydrogens > 1 else 'H' # Put hydrogen atoms as string
        return (True, f'{hydrogenSymbol}{anion}', overallCharge) # Returns acid radical formula + charge
    return (False, '', 0)

'''
Function returns TUPLE containing 'True', acid radical formula, and acid radical charge

Parameters
- anion (polyatomic anion name)
- hydrogen (prefix + hydrogen)
'''
def convertAcidRadicalAnion(anion, hydrogen):
    # Get polyatomic anion symbol + charge
    anionResult = convertPolyatomicIon(anion)
    if anionResult[0]:
        anionSymbol = anionResult[1]
        anionCharge = anionResult[2]
    else:
        return (False, '', '')

    # Determine number of hydrogen atoms
    hydrogenResult = calcHydrogenPrefixes(hydrogen)
    if hydrogenResult[0]:
        numHydrogens = hydrogenResult[1]
    else:
        return (False, '', '')

    # Determine acid radical formula + charge and return in tuple
    acidRadicalResult = balanceAcidRadical(numHydrogens, anionSymbol, anionCharge)
    if acidRadicalResult[0]:
        return (True, acidRadicalResult[1], acidRadicalResult[2])
    return (False, '', '')

# MULTIVALENT FUNCTIONS
'''
If valid multivalent syntax, function returns TUPLE containing 'True', particle symbol, and charge of particle
If not valid multivalent syntax, function returns TUPLE containing 'False'

Parameters
- element (element whose charge will be determined)
- romanNumeral (charge of particle in form of roman numeral) - ex: '(III)'
'''
def convertMultiValent(element, romanNumeral):
    # Remove brackets from roman numeral
    if (romanNumeral[0] == '(') and (romanNumeral[-1] == ')'):
        newRomanNumeral = romanNumeral.replace('(', '')
        newRomanNumeral = newRomanNumeral.replace(')', '')
        # If valid roman numeral, get value from romanNumerals dict
        if newRomanNumeral.lower() in romanNumerals.keys():
            romanInt = romanNumerals[newRomanNumeral.lower()]
            # If valid element + charge, return element symbol + charge
            if isElement(element):
                if romanInt in elementsDict[element]['charges']:
                    return (True, elementsDict[element]['symbol'], romanInt)
            # If valid polyatomic ion + charge, return polyatomic ion symbol + charge
            elif isPolyatomicIon(element): 
                if romanInt == polyatomicIonsDict[element]['charge']:
                    return (True, polyatomicIonsDict[element]['symbol'], romanInt)
    return (False, '', '')

'''
Function returns chemical formula from formula name
Function converts:
* Single elements
* Binary acids
* Oxy acids
* Covalent bonds
* Compounds (w/ polyatomic ions)
* Multivalent compounds (w/ polyatomic ions)
* Acid radicals (w/ polyatomic ions)
* Multivalent acid radicals (w/ polyatomic ions)

Parameters
- formulaName (name of chemical formula) - ex: 'sodium chloride'
'''
def convertToFormula(formulaName):
    # Single element conversion
    if (len(formulaName) == 1) or ((len(formulaName) == 2) and ((formulaName[0] in states.keys()) or (formulaName[1] in states.keys()))):
        # Set default state
        state = ''
        # Determine state if formula name length is 2
        if len(formulaName) == 2:
            if formulaName[0] in states.keys():
                state = states[formulaName[0]]
                element = formulaName[1]
            elif formulaName[1] in states.keys():
                state = states[formulaName[1]]
                element = formulaName[0]
            # invalid state
            else:
                return ''
        else:
            element = formulaName[0]

        # Check if element exists
        if isElement(element):
            # Determine element symbol
            elementSymbol = elementsDict[element]['symbol']
            # Diatomic element
            if isDiatomic(element):
                return f'{elementSymbol}2 {state}'
            # Phosphorus has 4 atoms when by itself
            elif element == 'phosphorus':
                return f'{elementSymbol}4 {state}'
            # Sulfur has 8 atoms when by itself
            elif (element == 'sulfur') or (element == 'sulphur'):
                return f'{elementSymbol}8 {state}'
            else:
                return f'{elementSymbol} {state}'
        return ''        

    # Binary acids, oxy acids, covalent bonds, compounds
    elif len(formulaName) == 2:
        # Acids
        if formulaName[1] == 'acid':
            # Binary acids
            if (formulaName[0].startswith('hydro')) and (formulaName[0][5:] in binaryAcids.keys()):
                # Determine non-metal 
                acidName = formulaName[0][5:]
                elementName = binaryAcids[acidName]

                # Find charge of non-metal
                chargeResult = findNegativeCharge(elementName)
                anionCharge = chargeResult[1]

                # Determine # atoms and symbols for H and anion
                numAtoms = balanceFormula(1, anionCharge)
                anionSymbol = elementsDict[elementName]['symbol']
                numHydrogen = numAtoms[0]
                numAnion = numAtoms[1]
                # Return chemical formula
                return getChemicalFormula('H', numHydrogen, anionSymbol, numAnion, '(aq)')
            # Oxy acids
            else:
                acidName = formulaName[0]
                # Determine acid name and # oxygen atoms to +/-
                acidResult = calcOxyAcidOxygen(acidName)
                if acidResult[0]:
                    acidName, oxygenDiff = acidResult[1], acidResult[2]
                else:
                    return ''
                
                # Find polyatomic name/formula if valid oxy acid
                if acidName in acidRootNames.keys():
                    polyatomicIonName = acidRootNames[acidName]
                    polyatomicIonFormula = polyatomicIonsDict[polyatomicIonName]['symbol']

                    # Determine updated polyatomic formula (# oxygen atoms updated)
                    polyFormulaResult = calcPolyFormula(polyatomicIonFormula, oxygenDiff)
                    if polyFormulaResult[0]:
                        # Balance hydrogen and polyatomic anion
                        numAtoms = balanceFormula(1, polyatomicIonsDict[polyatomicIonName]['charge'])
                        # Determine formula + charge for each particle
                        updatedPolyatomic = polyFormulaResult[1]
                        numHydrogen = numAtoms[0]
                        numAnion = numAtoms[1]
                        # Return chemical formula
                        return getChemicalFormula('H', numHydrogen, updatedPolyatomic, numAnion, '(aq)')
                return ''
        # Covalent bonds
        elif (
            (any(
                (formulaName[1].startswith(prefix)) and isAnion(formulaName[1][len(prefix):]) for prefix in covalentBondPrefixes.keys()
            ))
            or 
            (any(
                (formulaName[1].startswith(prefix)) and isVowel(formulaName[1][len(prefix)]) and isAnion(formulaName[1][len(prefix):]) for prefix in shortenedCovalentBondPrefixes
            ))
        ):  
            # Determine both elements
            elementOne = formulaName[0]
            elementTwo = formulaName[1]

            # Get element symbols and quantity of each element
            elementResult = convertCovalentFormula(elementOne, elementTwo)
            if elementResult[0]:
                symbolOne = elementResult[1]
                numElementOne = elementResult[2]
                symbolTwo = elementResult[3]
                numElementTwo = elementResult[4]
                # Return chemical formula
                return getChemicalFormula(symbolOne, numElementOne, symbolTwo, numElementTwo)
            return ''
        # Compounds
        else:
            # Determine cation + anion
            cation = formulaName[0]
            anion = formulaName[1]

            # Get cation charge + symbol
            # Cation is an element
            if isElement(cation):
                chargeResult = findPositiveCharge(cation)
                if chargeResult[0]:
                    cationSymbol = elementsDict[cation]['symbol']
                    cationCharge = chargeResult[1]
                else:
                    return ''
            # Cation is polyatomic
            elif isPolyatomicIon(cation):
                cationSymbol = polyatomicIonsDict[cation]['symbol']
                cationCharge = polyatomicIonsDict[cation]['charge']
            else:
                return ''

            # Get anion charge + symbol
            # Anion is an element
            if isAnion(anion):
                anionResult = convertAnion(anion)
                if anionResult[0]:
                    anionSymbol = anionResult[1]
                    anionCharge = anionResult[2]
                else:
                    return ''
            # Anion is polyatomic
            else:
                anionResult = convertPolyatomicIon(anion)
                if anionResult[0]:
                    anionSymbol = anionResult[1]
                    anionCharge = anionResult[2]
                else:
                    return ''

            # Check if formula can be balanced
            if canBeBalanced(cationCharge, anionCharge):
                # Determine # atoms for cation and anion
                numAtoms = balanceFormula(cationCharge, anionCharge)
                numCation = numAtoms[0]
                numAnion = numAtoms[1]
                # Return chemical formula
                return getChemicalFormula(cationSymbol, numCation, anionSymbol, numAnion)
            return ''
    # Multivalent compounds, acid radicals
    elif len(formulaName) == 3:
        # Multivalent compounds
        if ('(' in formulaName[1]) and (')' in formulaName[1]):
            cation = formulaName[0]
            anion = formulaName[2]
            
            # Get cation charge + symbol
            cationResult = convertMultiValent(cation, formulaName[1])
            if cationResult[0]:
                cationSymbol = cationResult[1]
                cationCharge = cationResult[2]
            else:
                return ''

            # Get anion charge + symbol
            if isAnion(anion):
                anionResult = convertAnion(anion)
                if anionResult[0]:
                    anionSymbol = anionResult[1]
                    anionCharge = anionResult[2]
                else:
                    return ''
            else:
                anionResult = convertPolyatomicIon(anion)
                if anionResult[0]:
                    anionSymbol = anionResult[1]
                    anionCharge = anionResult[2]
                else:
                    return ''
            
            # Check if formula can be balanced
            if canBeBalanced(cationCharge, anionCharge):
                # Determine number of atoms of each particle
                numAtoms = balanceFormula(cationCharge, anionCharge)
                numCation = numAtoms[0]
                numAnion = numAtoms[1]
                # Return chemical formula
                return getChemicalFormula(cationSymbol, numCation, anionSymbol, numAnion)
            return ''

        # Acid radicals
        else:
            cation = formulaName[0]
            hydrogen = formulaName[1]
            anion = formulaName[2]

            # Determine cation symbol + charge
            if isElement(cation):
                chargeResult = findPositiveCharge(cation)
                if chargeResult[0]:
                    cationSymbol = elementsDict[cation]['symbol']
                    cationCharge = chargeResult[1]
                else:
                    return ''
            elif isPolyatomicIon(cation):
                cationSymbol = polyatomicIonsDict[cation]['symbol']
                cationCharge = polyatomicIonsDict[cation]['charge']
            else:
                return ''

            # Determine acid radical symbol + charge
            acidRadicalResult = convertAcidRadicalAnion(anion, hydrogen)
            if acidRadicalResult[0]:
                anionSymbol = acidRadicalResult[1]
                anionCharge = acidRadicalResult[2]
            else:
                return ''
            
            # Determine if formula can be balanced
            if canBeBalanced(cationCharge, anionCharge):
                # Find number of atoms of each particle
                numAtoms = balanceFormula(cationCharge, anionCharge)
                numCation = numAtoms[0]
                numAnion = numAtoms[1]
                # Return chemical formula
                return getChemicalFormula(cationSymbol, numCation, anionSymbol, numAnion)
            return ''
    
    # Multivalent acid radicals
    elif len(formulaName) == 4:
        # Determine if multivalent
        if ('(' in formulaName[1]) and (')' in formulaName[1]):
            cation = formulaName[0]
            romanNumeral = formulaName[1]
            hydrogen = formulaName[2]
            anion = formulaName[3]
            
            # Get cation charge + symbol
            cationResult = convertMultiValent(cation, romanNumeral)
            if cationResult[0]:
                cationSymbol = cationResult[1]
                cationCharge = cationResult[2]
            else:
                return ''

            # Get acid radical charge + symbol
            acidRadicalResult = convertAcidRadicalAnion(anion, hydrogen)
            if acidRadicalResult[0]:
                anionSymbol = acidRadicalResult[1]
                anionCharge = acidRadicalResult[2]
            else:
                return ''
            
            # Determine if formula can be balanced
            if canBeBalanced(cationCharge, anionCharge):
                # Determine number of atoms of each particle
                numAtoms = balanceFormula(cationCharge, anionCharge)
                numCation = numAtoms[0]
                numAnion = numAtoms[1]
                # Return chemical formula
                return getChemicalFormula(cationSymbol, numCation, anionSymbol, numAnion)
            return ''
    return ''

# Load json file
with open('elements.json') as file:
    jsonFile = json.load(file)
    elementsDict = jsonFile['elements']
    polyatomicIonsDict = jsonFile['polyatomicIons']
