#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed May 20 17:36:05 2020

@author: anton
"""

from SLiCAPplots import *


# Initialize HTML globals
ini.htmlIndex    = ''
ini.htmlPrefix   = ''
ini.htmlPage     = ''
ini.htmlLabels   = {}
ini.htmlPages    = []
HTMLINSERT       = '<!-- INSERT -->' # pattern to be replaced in html files
LABELTYPES       = ['headings', 'data', 'fig', 'eqn', 'analysis']

class Label(object):
    """
    """
    def __init__(self, name, typ, page, text):
        """
        """
        self.name = name
        self.type = typ
        self.page = page
        self.text = text
        return

def startHTML(projectName):
    """
    Creates main project index page.
    """
    global HTMLINDEX, HTMLPAGES
    ini.htmlIndex = 'index.html'
    toc = '<h2>Table of contents</h2>'
    html = HTMLhead(projectName) + toc + '<ol>' + HTMLINSERT + '</ol>' + HTMLfoot(ini.htmlIndex)
    f = open(ini.htmlPath + ini.htmlIndex, 'w')
    f.write(html)
    f.close()
    ini.htmlPages.append(ini.htmlIndex)
    return

def HTMLhead(pageTitle):
    """
    Returns the html page head, ignores MathJax settings in SLiCAPini.py
    """
    html = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"\n'
    html += '"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\n'
    html += '<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">\n'
    html += '<head><meta http-equiv="Content-Type" content="text/html;charset=iso-8859-1"/>\n'
    html += '<meta name="Language" content="English"/>\n'
    html += '<title>"' + pageTitle + '"</title><link rel="stylesheet" href="css/slicap.css">\n'
    if ini.mathml == True:
        print 'MathML is not (yet) supported. Only MathJaX cloud is supported!'
    else:
        html += '<script>MathJax = {tex:{tags: \'ams\', inlineMath:[[\'$\',\'$\'],]}, svg:{fontCache:\'global\'}};</script>\n'
        html += '<script type="text/javascript" id="MathJax-script" async  src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>\n'
    html += '</head><body><div id="top"><h1>' + pageTitle + '</h1></div>\n'  
    return(html)
    
def HTMLfoot(indexFile):
    """
    Returns html page footer with link to 'indexFile'.
    """
    idx = ini.htmlIndex.split('.')[0]
    html = '\n<div id="footnote">\n'
    html += '<p>Go to <a href="' + ini.htmlIndex + '">' + idx + '</a></p>\n'
    html += '<p>SLiCAP: Symbolic Linear Circuit Analysis Program, Version 1.0 &copy 2009-2020 SLiCAP development team</p>\n'
    html += '<p>For documentation, examples, support, updates and courses please visit: <a href="http://www.analog-electronics.eu">analog-electronics.eu</a></p>\n'
    html += '<p>Last project update: %s</p>\n'%(ini.lastUpdate.strftime("%Y-%m-%d %H:%M:%S"))
    html += '</div></body></html>'
    return(html)

def insertHTML(fileName, htmlInsert):
    """
    Inserts html in the file specified by 'fileName' at the location of
    HTMLINSERT.
    
    ToDo: check if this file exists.
    """
    html = readFile(fileName)
    html = html.replace(HTMLINSERT, htmlInsert + HTMLINSERT)
    writeFile(fileName, html)
    return

def readFile(fileName):
    """
    Returns the contents of a file as a string.
    
    ToDo: check if this file exists.
    """
    f = open(fileName, 'r')
    txt = f.read()
    f.close()
    return txt

def writeFile(fileName, txt):
    """
    Writes a text string to a file.
    
    ToDo: check if this file exists.
    """
    f = open(fileName, 'w')
    f.write(txt)
    f.close()
    return

### User Functions ###########################################################

def htmlPage(pageTitle, index = False, label = ''):
    """
    Creates an HTML page with the title in the title bar. If index==True
    then the page will be used as new index page, else a link to this page will
    be placed on the current index page.
    The global HTMLINDEX holds the name of the current index page.
    """
    if index == True:
        # The page is a new index page
        fileName = ini.htmlPrefix + 'index.html'
        # Place link on old index page
        href = '<li><a href="' + fileName +'">' + pageTitle + '</a></li>'
        insertHTML(ini.htmlPath + ini.htmlIndex, href)
        # Create the new HTML file
        toc = '<h2>Table of contents</h2>'
        html = HTMLhead(pageTitle) + toc + '<ol>' + HTMLINSERT + '</ol>' + HTMLfoot(ini.htmlIndex)
        writeFile(ini.htmlPath + fileName, html)
        # Make this page the new index page
        ini.htmlIndex = fileName
    else:
        fileName = ini.htmlPrefix + '-'.join(pageTitle.split()) + '.html'
        # Place link on the current index page
        href = '<li><a href="' + fileName +'">' + pageTitle + '</a></li>'
        insertHTML(ini.htmlPath + ini.htmlIndex, href)
        # Create the new HTML page
        if label != '':
            #
            newlabel = Label(label, 'headings', fileName, pageTitle)
            ini.htmlLabels[label] = newlabel
            #
            #ini.htmlLabels[label] = ini.htmlPage
            label = '<a id="' + label + '"></a>'
        html = label + HTMLhead(pageTitle) + HTMLINSERT + HTMLfoot(ini.htmlIndex)
        writeFile(ini.htmlPath + fileName, html)
    # Make this page the active HTML page
    ini.htmlPage = fileName
    ini.htmlPages.append(fileName)
    # Remove double entries in ini.htmlPages
    ini.htmlPages = list(set(ini.htmlPages))
    return
    
def head2html(headText, label=''):
    """
    Placed a level-2 heading on the active HTML page.
    """
    if label != '':
        #
        newlabel = Label(label, 'headings', ini.htmlPage, headText)
        ini.htmlLabels[label] = newlabel
        #
        #ini.htmlLabels[label] = ini.htmlPage
        label = '<a id="' + label + '"></a>'
    html = '<h2>' + label + headText + '</h2>\n'
    insertHTML(ini.htmlPath + ini.htmlPage, html)
    if ini.notebook:
        html = html.replace('$', '$$')
    return html

def head3html(headText, label=''):
    """
    Placed a level-3 heading on the active HTML page.
    """
    if label != '':
        #
        newlabel = Label(label, 'headings', ini.htmlPage, headText)
        ini.htmlLabels[label] = newlabel
        #
        #ini.htmlLabels[label] = ini.htmlPage
        label = '<a id="' + label + '"></a>'
    html = '<h3>' + label + headText + '</h3>\n'
    insertHTML(ini.htmlPath + ini.htmlPage, html)
    if ini.notebook:
        html = html.replace('$', '$$')
    return html

def text2html(txt):
    """
    Places txt on the active HTML page.
    """
    html = '<p>' + txt + '</p>\n'
    insertHTML(ini.htmlPath + ini.htmlPage, html)
    if ini.notebook:
        html = html.replace('$', '$$')
    return html

def netlist2html(fileName, label=''):
    """
    Places the netlist of HTMLCIRCUIT on HTMLPAGE
    """
    try:
        if label != '':
            newlabel = Label(label, 'data', ini.htmlPage, 'Netlist: ' + fileName)
            ini.htmlLabels[label] = newlabel
            label = '<a id="' + label + '"></a>'
        netlist = readFile(ini.circuitPath + fileName)
        html = '<h2>' + label + 'Netlist: ' + fileName + '</h2>\n<pre>' + netlist + '</pre>\n'
        insertHTML(ini.htmlPath + ini.htmlPage, html)
    except:
        print "Error: could not open netlist file: '%s'."%(fileName)
    return html

def elementData2html(circuitObject, label = '', caption = ''):
    """
    Displays element data on the active html page:
        - refDes
        - nodes
        - referenced elements
        - parameters with symbolic and numeric values
    """
    if label != '':
        #
        newlabel = Label(label, 'data', ini.htmlPage, circuitObject.title + ': element data')
        ini.htmlLabels[label] = newlabel
        #
        #ini.htmlLabels[label] = ini.htmlPage
        label = '<a id="' + label + '"></a>'
    caption = "<caption>Table: Element data of expanded netlist '%s'</caption>"%(circuitObject.title)
    html = '%s<table>%s\n'%(label, caption)
    html += '<tr><th class="left">RefDes</th><th class="left">Nodes</th><th class="left">Refs</th><th class="left">Model</th><th class="left">Param</th><th class="left">Symbolic</th><th class="left">Numeric</th></tr>\n'
    elementNames = circuitObject.elements.keys()
    elementNames.sort()
    for el in elementNames:
        elmt = circuitObject.elements[el]
        html += '<tr><td class="left">' + elmt.refDes + '</td><td class = "left">'
        for node in elmt.nodes:
            html += node + ' '
        html += '</td><td class = "left">'
        for ref in elmt.refs:
            html += ref + ' '
        html += '</td><td class = "left">' + elmt.model +'</td>\n'
        parNames = elmt.params.keys()
        if len(parNames) == 0:
            html += '<td></td><td></td><td></td><tr>'
        else:
            i = 0
            for param in parNames:
                symValue = '$' + sp.latex(roundN(elmt.params[param])) +'$'
                numValue = '$' + sp.latex(roundN(fullSubs(elmt.params[param], circuitObject.parDefs), numeric=True)) + '$'
                if i == 0:
                    html += '<td class="left">' + param + '</td><td class="left">' + symValue + '</td><td class="left">' + numValue + '</td></tr>\n'
                else:
                    html += '<tr><td></td><td></td><td></td><td></td><td class="left">' + param + '</td><td class="left">' + symValue + '</td><td class="left">' + numValue + '</td></tr>\n'
                i += 1
    html += '</table>\n'
    insertHTML(ini.htmlPath + ini.htmlPage, html)
    if ini.notebook:
        html = html.replace('$', '$$')
    return html

def params2html(circuitObject, label = '', caption = ''):
    """
    Displays all parameters with definitions and numeric value.
    """
    if label != '':
        #
        newlabel = Label(label, 'data', ini.htmlPage, circuitObject.title + ': circuit parameters')
        ini.htmlLabels[label] = newlabel
        #
        #ini.htmlLabels[label] = ini.htmlPage
        label = '<a id="' + label + '"></a>'
    caption = "<caption>Table: Parameter definitions in '%s'.</caption>"%(circuitObject.title)
    html = '%s<table>%s\n'%(label, caption)
    html += '<tr><th class="left">Name</th><th class="left">Symbolic</th><th class="left">Numeric</th></tr>\n'
    parNames = circuitObject.parDefs.keys()
    # Sort the list with symbolic keys such that elements are grouped and 
    # sorted per sub circuit
    parNames = [str(parNames[i]) for i in range(len(parNames))]
    localPars = []  # list for sub circuit parameters
    globalPars = [] # list for main circuit parameters
    for i in range(len(parNames)):
        par = str(parNames[i]).split('_')
        if par[-1][0].upper() == 'X':
            localPars.append(str(parNames[i]))
        else:
            globalPars.append(str(parNames[i]))
    # Group per sub circuit ignore case
    #localParams = sorted(localParams, key = lambda x: x.split('_')[-1].upper() + x.split('_')[0].upper())
    # Group per parname respect case
    localPars = sorted(localPars)
    names = sorted(globalPars) + localPars
    parNames = [sp.Symbol(names[i]) for i in range(len(names))]
    for par in parNames:
        parName = '$' + sp.latex(par) + '$'
        symValue = '$' + sp.latex(roundN(circuitObject.parDefs[par])) + '$'
        numValue = '$' + sp.latex(roundN(fullSubs(circuitObject.parDefs[par], circuitObject.parDefs), numeric=True)) + '$'
        html += '<tr><td class="left">' + parName +'</td><td class="left">' + symValue + '</td><td class="left">' + numValue + '</td></tr>\n'
    html += '</table>\n'
    if len(circuitObject.params) > 0:
        caption = "<caption>Table: Parameters without definition in '%s.</caption>\n"%(circuitObject.title)
        html += '<table>%s\n'%(caption)
        html += '<tr><th class="left">Name</th></tr>\n'
        for par in circuitObject.params:
            parName = '$' + sp.latex(par) + '$'
            html += '<tr><td class="left">' + parName +'</td></tr>\n'
        html += '</table>\n'
    insertHTML(ini.htmlPath + ini.htmlPage, html)
    if ini.notebook:
        html = html.replace('$', '$$')
    return html

def img2html(fileName, width, label = '', caption = ''):
    """
    Copies the image file to the 'img.' subdirectory of the 'html/' directory
    set by HTMLPATH in SLiCAPini.py and creates a link to this file on the 
    active html page.
    """
    if label != '':
        #
        if caption == '':
            labelText = fileName
        else:
            labelText = caption
        newlabel = Label(label, 'fig', ini.htmlPage, labelText)
        ini.htmlLabels[label] = newlabel
        label = '<a id="' + label + '"></a>'
    try:
        cp(ini.imgPath + fileName, ini.htmlPath + 'img/' + fileName)
    except:
        print("Error: could not copy: '%s'."%(fileName))
    html = '<figure>%s<img src="img/%s" alt="%s" style="width:%spx">\n'%(label, fileName, caption, width)
    if caption != '':
        html+='<figcaption>Figure: %s<br>%s</figcaption>\n'%(fileName, caption)
    html += '</figure>\n'
    insertHTML(ini.htmlPath + ini.htmlPage, html)
    return '%s'%(ini.htmlPath + 'img/' + fileName)

def csv2html(fileName, label = '', separator = ',', caption = ''):
    """
    Displays the contents of a csv file as a table on the active HTML page.
    """
    if label != '':
        #
        if caption == '':
            labelText = fileName
        else:
            labelText = caption
        newlabel = Label(label, 'data', ini.htmlPage, labelText)
        ini.htmlLabels[label] = newlabel
        #
        #ini.htmlLabels[label] = ini.htmlPage
        label = '<a id="' + label + '"></a>'
    caption = '<caption>Table: %s<br>%s.</caption>'%(fileName, caption)
    html = '%s<table>%s'%(label, caption)
    csvLines = readFile(ini.csvPath + fileName).splitlines()
    for i in range(len(csvLines)):
        cells = csvLines[i].split(separator)
        html += '<tr>'
        if i == 0:
            for cell in cells:
                html += '<th>%s</th>'%(cell)
        else:
            for cell in cells:
                html += '<td>%s</td>'%(cell)
        html += '</tr>\n'
    html += '</table>\n'
    insertHTML(ini.htmlPath + ini.htmlPage, html)
    if ini.notebook:
        html = html.replace('$', '$$')
    return html

def expr2html(expr, units = ''):
    """
    Inline display of an expression optional with units.
    """
    if isinstance(expr, tuple(sp.core.all_classes)):
        if units != '':
            units = '\\left[\\mathrm{' + sp.latex(sp.sympify(units)) + '}\\right]'
        html = '$' + sp.latex(roundN(expr)) + units + '$'
        insertHTML(ini.htmlPath + ini.htmlPage, html)
    else:
        print "Error: expr2html, expected a Sympy expression."
        html = ''
    if ini.notebook:
        html = html.replace('$', '$$')
    return html

def eqn2html(arg1, arg2, units = '', label = '', labelText = ''):
    """
    Displays an equation on the active HTML page'.
    """
    if arg1 == None or arg2 == None:
        return
    if not isinstance(arg1, tuple(sp.core.all_classes)):
        arg1 = sp.sympify(arg1)
    if not isinstance(arg2, tuple(sp.core.all_classes)):
        arg2 = sp.sympify(arg2)
    if units != '':
        units = '\\,\\left[ \\mathrm{' + sp.latex(sp.sympify(units)) + '}\\right]'

    if label != '':
        #
        if labelText == '':
            labelText = label
        newlabel = Label(label, 'eqn', ini.htmlPage, labelText)
        ini.htmlLabels[label] = newlabel
        label   = '<a id="'+ label +'"></a>\n'
    html = label + '\\begin{equation}\n' + sp.latex(roundN(arg1)) + '=' + sp.latex(roundN(arg2)) + units + '\n'
    html += '\\end{equation}\n'
    insertHTML(ini.htmlPath + ini.htmlPage, html)
    if ini.notebook:
        html = ('$$' + html + '$$')
    return html

def matrices2html(instrObj, label = '', labelText = ''):
    """
    Displays the MNA equation on the active HTML page.
    """
    if instrObj.errors != 0:
        print "Errors found during executeion."
        return ''
    elif instrObj.dataType != 'matrix':
        print "Error: expected dataType 'matrix' for 'matrices2html()', got: '%s'."%(instrObj.dataType)
        return ''
    try:
        (Iv, M, Dv) = (instrObj.Iv, instrObj.M, instrObj.Dv)
        Iv = sp.latex(roundN(Iv))
        M  = sp.latex(roundN(M))
        Dv = sp.latex(roundN(Dv))
        if label != '':
            #
            if labelText == '':
                labelText = label
            newlabel = Label(label, 'eqn', ini.htmlPage, labelText)
            ini.htmlLabels[label] = newlabel
            label = '<a id="' + label + '"></a>'
        html = '<h3>' + label + 'Matrix equation:</h3>\n'
        html += '\\begin{equation}\n' + Iv + '=' + M + '\\cdot' + Dv + '\n'
        html += '\\end{equation}\n'
        insertHTML(ini.htmlPath + ini.htmlPage, html)
    except:
        print "Error: unexpected input for 'matrices2html()'."
    if ini.notebook:
        html = html.replace('$', '$$')
    return html

def pz2html(instObj, label = '', labelText = ''):
    """
    Displays the DC transfer, and tables with poles and zeros on the active 
    HTML page.
    
    ToDo:
        
        Make it work for stepped instructions
        
    """
    if instObj.errors != 0:
        print "Errors found in instruction."
        return
    elif instObj.dataType != 'poles' and instObj.dataType != 'zeros' and instObj.dataType != 'pz':
        print "Error: 'pz2html()' expected dataType: 'poles', 'zeros', or 'pz', got: '%s'."%(instObj.dataType)
        return
    elif instObj.step == True :
        print "Error: parameter stepping not yet implemented for 'pz2html()'."
        return  
    
    if label != '':
        if labelText == '':
            labelText = label
        newlabel = Label(label, 'analysis', ini.htmlPage, labelText)
        ini.htmlLabels[label] = newlabel
        label = '<a id="' + label + '"></a>'
    (poles, zeros, DCgain) = (instObj.poles, instObj.zeros, instObj.DCvalue)
    if instObj.dataType == 'poles':
        headTxt = 'Poles '
    elif instObj.dataType == 'zeros':
        headTxt = 'Zeros '
    elif instObj.dataType == 'pz':
        headTxt = 'PZ '
    html = '<h2>' + label + headTxt + ' analysis results</h2>\n'
    html += '<h3>Gain type: %s</h3>'%(instObj.gainType)
    if DCgain != None and instObj.dataType =='pz':
        html += '\n' + '<p>DC gain = ' + str(sp.N(DCgain, ini.disp)) + '</p>\n'
    elif instObj.dataType =='pz':
        html += '<p>DC gain could not be determined.</p>\n'
    if ini.Hz == True:
        unitsM = 'Mag [Hz]'
        unitsR = 'Re [Hz]'
        unitsI = 'Im [Hz]'
    else:
        unitsM = 'Mag [rad/s]'
        unitsR = 'Re [rad/s]'
        unitsI = 'Im [rad/s]'
    if len(poles) > 0 and instObj.dataType == 'poles' or instObj.dataType == 'pz':
        html += '<table><tr><th>pole</th><th>' + unitsR + '</th><th>' + unitsI + '</th><th>' + unitsM + '</th><th>Q</th></tr>\n'
        for i in range(len(poles)):
            p = poles[i]
            if ini.Hz == True:
                p  = p/2/sp.pi
            Re = sp.re(p)
            Im = sp.im(p)
            F  = sp.sqrt(Re**2+Im**2)
            if Im != 0:
                Q = str(sp.N(F/2/abs(Re), ini.disp))
            else:
                Q = ''
            F  = str(sp.N(F, ini.disp))
            Re = str(sp.N(Re, ini.disp))
            if Im != 0.:
                Im = str(sp.N(Im, ini.disp))
            else:
                Im = ''
            name = 'p<sub>' + str(i + 1) + '</sub>'
            html += '<tr><td>' + name + '</td><td>' + Re + '</td><td>' + Im + '</td><td>' + F + '</td><td>' + Q +'</td></tr>\n'
        html += '</table>\n'
    elif instObj.dataType == 'poles' or instObj.dataType == 'pz':
        html += '<p>No poles found.</p>\n'
    if len(zeros) > 0 and instObj.dataType == 'zeros' or instObj.dataType == 'pz':
        html += '<table><tr><th>zero</th><th>' + unitsR + '</th><th>' + unitsI + '</th><th>' + unitsM + '</th><th>Q</th></tr>\n'
        for i in range(len(zeros)):
            z = zeros[i]
            if ini.Hz == True:
                z = z/2/sp.pi
            Re = sp.re(z)
            Im = sp.im(z)
            F  = sp.sqrt(Re**2+Im**2)
            if Im != 0:
                Q = str(sp.N(F/2/abs(Re), ini.disp))
            else:
                Q = ''
            F  = str(sp.N(F, ini.disp))
            Re = str(sp.N(Re, ini.disp))
            if Im != 0.:
                Im = str(sp.N(Im, ini.disp))
            else:
                Im = ''
            name = 'z<sub>' + str(i + 1) + '</sub>'
            html += '<tr><td>' + name + '</td><td>' + Re + '</td><td>' + Im + '</td><td>' + F + '</td><td>' + Q +'</td></tr>\n'
        html += '</table>\n'
    elif instObj.dataType == 'zeros' or instObj.dataType == 'pz':
        html += '<p>No zeros found.</p>\n'
    insertHTML(ini.htmlPath + ini.htmlPage, html)
    return html

def noise2html(instObj, label = '', labelText = ''):
    """
    """
    if instObj.errors != 0:
        print "Errors found in instruction."
        return
    elif instObj.dataType != 'noise':
        print "Error: 'noise2html()' expected dataType: 'noise', got: '%s'."%(instObj.dataType)
        return
    elif instObj.step == True :
        print "Error: parameter stepping not yet implemented for 'noise2html()'."
        return  
    if label != '':
        if labelText == '':
            labelText = label
        newlabel = Label(label, 'analysis', ini.htmlPage, labelText)
        ini.htmlLabels[label] = newlabel
        label = '<a id="' + label + '"></a>'
    detUnits = '\mathrm{\left[\\frac{%s^2}{Hz}\\right]}'%(instObj.detUnits)
    srcUnits = '\mathrm{\left[\\frac{%s^2}{Hz}\\right]}'%(instObj.srcUnits)
    if instObj.simType == 'symbolic':
        html = '<h2>Symbolic noise analysis results</h2>\n'
        numeric = False
    else:
        html = '<h2>Numeric noise analysis results</h2>\n'
        numeric = True
    html += '<h3>Detector-referred noise spectrum</h3>\n'
    html += '$$S_{out}=%s\, %s$$\n'%(sp.latex(roundN(instObj.onoise, numeric = instObj.numeric)), detUnits)
    if instObj.source != None:
        html += '<h3>Source-referred noise spectrum</h3>\n'
        html += '$$S_{in}=%s\, %s$$\n'%(sp.latex(roundN(instObj.inoise, numeric = instObj.numeric)), srcUnits)
    html += '<h3>Contributions of individual noise sources</h3><table>\n'    
    keys = instObj.snoiseTerms.keys()
    keys.sort()
    for key in keys:
        nUnits = key[0].upper()
        if nUnits == 'I':
            nUnits = 'A'
        nUnits = '\mathrm{\left[\\frac{%s^2}{Hz}\\right]}'%(nUnits)
        html += '<th colspan = "3" class="center">Noise source: %s</th>'%(key)
        srcValue = instObj.snoiseTerms[key]
        if numeric:
            srcValue = fullSubs(srcValue, instObj.parDefs)
        html += '<tr><td class="title">Spectral density:</td><td>$%s$</td><td class="units">$\,%s$</td></tr>\n'%(sp.latex(roundN(srcValue, numeric = instObj.numeric)), nUnits)
        html += '<tr><td class="title">Detector-referred:</td><td>$%s$</td><td class="units">$\,%s$</td></tr>\n'%(sp.latex(roundN(instObj.onoiseTerms[key], numeric = instObj.numeric)), detUnits)
        if instObj.source != None:
            html += '<tr><td class="title">Source-referred:</td><td>$%s$</td><td class="units">$\,%s$</td></tr>\n'%(sp.latex(roundN(instObj.inoiseTerms[key], numeric = instObj.numeric)), srcUnits)
    html += '</table>\n'
    insertHTML(ini.htmlPath + ini.htmlPage, html)
    if ini.notebook:
        html = html.replace('$', '$$')
        html = html.replace('$$$$', '$$')
    return html

def dcVar2html(instObj, label = '', labelText = ''):
    """
    """
    if instObj.errors != 0:
        print "Errors found in instruction."
        return
    elif instObj.dataType != 'analysis':
        print "Error: 'dcvar2html()' expected dataType: 'dcvar', got: '%s'."%(instObj.dataType)
        return
    elif instObj.step == True :
        print "Error: parameter stepping not yet implemented for 'dcvar2html()'."
        return  
    if label != '':
        if labelText == '':
            labelText = label
        newlabel = Label(label, 'dcvar', ini.htmlPage, labelText)
        ini.htmlLabels[label] = newlabel
        label = '<a id="' + label + '"></a>'
    detUnits = '\mathrm{\left[ %s^2 \\right]}'%(instObj.detUnits)
    srcUnits = '\mathrm{\left[ %s^2 \\right]}'%(instObj.srcUnits)
    if instObj.simType == 'symbolic':
        html = '<h2>Symbolic dcvar analysis results</h2>\n'
        numeric = False
    else:
        html = '<h2>Numeric dcvar analysis results</h2>\n'
        numeric = True
    html += '<h3>DC solution of the network</h3>\n'
    html += '$$%s=%s$$\n'%(sp.latex(roundN(instObj.Dv)), sp.latex(roundN(instObj.dcSolve, numeric = instObj.numeric)))
    html += '<h3>Detector-referred variance</h3>\n'
    html += '$$\sigma_{out}^2=%s\, %s$$\n'%(sp.latex(roundN(instObj.ovar, numeric = instObj.numeric)), detUnits)
    if instObj.source != None:
        html += '<h3>Source-referred variance</h3>\n'
        html += '$$\sigma_{in}^2=%s\, %s$$\n'%(sp.latex(roundN(instObj.ivar, numeric = instObj.numeric)), srcUnits)
    html += '<h3>Contributions of individual component variances</h3><table>\n'    
    keys = instObj.svarTerms.keys()
    keys.sort()
    for key in keys:
        nUnits = key[0].upper()
        if nUnits == 'I':
            nUnits = 'A'
        nUnits = '\mathrm{\left[ %s^2 \\right]}'%(nUnits)
        html += '<th colspan = "3" class="center">Variance of source: %s</th>'%(key)
        srcValue = instObj.svarTerms[key]
        if numeric:
            srcValue = fullSubs(srcValue, instObj.parDefs)
        html += '<tr><td class="title">Source variance:</td><td>$%s$</td><td class="units">$\,%s$</td></tr>\n'%(sp.latex(roundN(srcValue, numeric = instObj.numeric)), nUnits)
        html += '<tr><td class="title">Detector-referred:</td><td>$%s$</td><td class="units">$\,%s$</td></tr>\n'%(sp.latex(roundN(instObj.ovarTerms[key], numeric = instObj.numeric)), detUnits)
        if instObj.source != None:
            html += '<tr><td class="title">Source-referred:</td><td>$%s$</td><td class="units">$\,%s$</td></tr>\n'%(sp.latex(roundN(instObj.ivarTerms[key], numeric = instObj.numeric)), srcUnits)
    html += '</table>\n'
    insertHTML(ini.htmlPath + ini.htmlPage, html)
    if ini.notebook:
        html = html.replace('$', '$$')
        html = html.replace('$$$$', '$$')
    return html

def coeffsTransfer2html(transferCoeffs, label = '', labelText = ''):
    """
    Displays the coefficients of the numerator and the denominator of a transfer function on the active html page.
    """
    if label != '':
        if labelText == '':
            labelText = label
        newlabel = Label(label, 'analysis', ini.htmlPage, labelText)
        ini.htmlLabels[label] = newlabel
        label = '<a id="' + label + '"></a>'
    (gain, numerCoeffs, denomCoeffs) = transferCoeffs
    html = '<h3>Gain factor</h3>\n<p>$%s$</p>\n'%(sp.latex(roundN(gain)))
    html += '<h3>Normalized coefficients of the numerator:</h3>\n<table><tr><th class=\"center\">order</th><th class=\"left\">coefficient</th></tr>\n'
    for i in range(len(numerCoeffs)):
        value = sp.latex(roundN(numerCoeffs[i]))
        html += '<tr><td class=\"center\">$' + str(i) + '$</td><td class=\"left\">$' + value + '$</td></tr>\n'
    html += '</table>\n'
    html += '<h3>Normalized coefficients of the denominator:</h3>\n<table><tr><th class=\"center\">order</th><th class=\"left\">coefficient</th></tr>\n'
    for i in range(len(denomCoeffs)):
        value = sp.latex(roundN(denomCoeffs[i]))
        html += '<tr><td class=\"center\">$' + str(i) + '$</td><td class=\"left\">$' + value + '$</td></tr>\n'
    html += '</table>\n'
    insertHTML(ini.htmlPath + ini.htmlPage, html)
    if ini.notebook:
        html = html.replace('$', '$$')
    return html

def stepArray2html(stepVars, stepArray):
    """
    """
    numVars = len(stepVars)
    numRuns = len(stepArray[0])
    html = '<h3>Step array</h3>\n<table><tr><th>Run</th>'
    for i in range(numVars):
        html += '<th>$%s$</th>'%(sp.latex(stepVars[i]))
    html += '</tr>\n'
    for i in range(numRuns):
        html += '<tr><td>%s</td>'%(i+1)
        for j in range(numVars):
            html += '<td>%8.2e</td>'%(stepArray[j][i])
        html += '</tr>\n'
    html += '</table>\n'
    insertHTML(ini.htmlPath + ini.htmlPage, html)
    return html

def fig2html(figureObject, width, label = '', caption = ''):
    """
    Copies the image file to the 'img.' subdirectory of the 'html/' directory
    set by HTMLPATH in SLiCAPini.py and creates a link to this file on the 
    active html page.
    """
    if label != '':
        if caption == '':
            labelText = figureObject.fileName
        else:
            labelText = caption
        newlabel = Label(label, 'fig', ini.htmlPage, labelText)
        ini.htmlLabels[label] = newlabel
        label = '<a id="' + label + '"></a>'
    html = '<figure>%s<img src="img/%s" alt="%s" style="width:%spx">\n'%(label, figureObject.fileName, caption, width)
    if caption != '':
        html+='<figcaption>Figure: %s<br>%s</figcaption>\n'%(figureObject.fileName, caption)
    html += '</figure>\n'
    insertHTML(ini.htmlPath + ini.htmlPage, html)
    try:
        cp(ini.imgPath + figureObject.fileName, ini.htmlPath + 'img/' + figureObject.fileName)
    except:
        print("Error: could not copy: '%s'."%(ini.imgPath + figureObject.fileName))
    return '%s'%(ini.htmlPath + 'img/' + figureObject.fileName)

def roundN(expr, numeric=False):
    """
    Rounds all number atoms in an expression to ini.disp digits, but only
    converts integers into floats if their number of digites is more than
    ini.disp
    """
    if numeric:
        expr = sp.N(expr, ini.disp)
    try:
        expr = expr.xreplace({n : sp.N(n, ini.disp) for n in expr.atoms(sp.Float)})
        ints = list(expr.atoms(sp.Number))
        for i in range(len(ints)):
            if sp.N(sp.Abs(ints[i])) > 10**ini.disp or sp.N(sp.Abs(ints[i])) < 10**-ini.disp:
                expr = expr.xreplace({ints[i]: sp.N(ints[i], ini.disp)})
            if sp.N(ints[i]) == 1.0:
                expr = expr.xreplace({ints[i]: 1})
            if sp.N(ints[i]) == -1.0:
                expr = expr.xreplace({ints[i]: -1})
    except:
        pass
    return expr

### HTML links and labels
    
def href(label, fileName = ''):
    """
    Returns the html code for a jump to a label 'labelName'.
    This label can be on any page. If referring backwards 'fileName' can be
    detected automatically. When referring forward 'fileName' must be the 
    name of the file that will be created later. Run a project 2 times without
    closing it after the first run, automaitcally detects all labels.
    """
    if fileName == '':
        fileName = ini.htmlLabels[label].page
    if fileName == ini.htmlPage:
        html = '<a href="#' + label + '">' + ini.htmlLabels[label].text + '</a>'
    else:
        html = '<a href="' + fileName + '#' + label + '">' + ini.htmlLabels[label].text + '</a>'
    return html

def links2html():
    htmlPage('Links')
    labelDict = {}
    html = ''
    for labelType in LABELTYPES:
        labelDict[labelType] = []
    for labelName in ini.htmlLabels.keys():
        labelDict[ini.htmlLabels[labelName].type].append(labelName)
    for labelType in LABELTYPES:
        if len(labelDict[labelType]) != 0:
            labelDict[labelType].sort()
            if labelType == 'headings':
                html += '<h2>Pages and sections</h2>\n'
                for name in labelDict[labelType]:
                    html += '<p>%s</p>'%(href(name))
            elif labelType == 'data':
                html += '<h2>Circuit data and imported tables</h2>\n'
                for name in labelDict[labelType]:
                    html += '<p>%s</p>'%(href(name))
            elif labelType == 'fig':
                html += '<h2>Figures</h2>\n'
                for name in labelDict[labelType]:
                    html += '<p>%s</p>'%(href(name))
            elif labelType == 'eqn':
                html += '<h2>Equations</h2>\n'
                for name in labelDict[labelType]:
                    html += '<p>%s</p>'%(href(name))
            elif labelType == 'analysis':
                html += '<h2>Analysis results</h2>\n'
                for name in labelDict[labelType]:
                    html += '<p>%s</p>'%(href(name))
    insertHTML(ini.htmlPath + ini.htmlPage, html)
    return

if __name__ == '__main__':
    ini.projectPath = ini.installPath + 'testProjects/MOSamp/'
    ini.htmlPath    = ini.projectPath + 'html/'
    startHTML('Test project') 