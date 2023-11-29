Sub GetManifests()
' Testing GETting a list of manifests
'Things to improve
' Error handling
' Parse the Authentication and get results JSON to values

' Variable Setting variables defined when used see comments below
Dim result As String
Dim resultloadtype As String
Dim locbeg As Integer
Dim locend As Integer
Dim location As Integer
Dim i As Integer
Dim URL As String
Dim NewURL As String
Dim winHttpReq As Object

MsgBox ("Start Getting Manifests")
'For Debugging Ignore MsgBox ()

'Creating the object so we can use services in thsi macro
Set winHttpReq = CreateObject("msxml2.xmlhttp.6.0")

'Setting the URL for Authentication, Please note APIID and APIKey are named ranges in the excel file
URL = "https://rcrainfopreprod.epa.gov/rcrainfo/rest/api/v1/auth/" & Range("APIID") & "/" & Range("APIKey")

'For Debugging Ignore MsgBox (URL)
'Calling methds from the winHttpReq object to get the authentiucation token

winHttpReq.Open "GET", URL, False
winHttpReq.Send
result = winHttpReq.responseText
'For debugging
'result2 = result

'Parsing the Authentication token.  There is a better way to parse data, but this is a proof on concept.
locbeg = InStr(result, ": ") + 3
locend = InStr(result, "expiration") - 22
result = "Bearer " & Mid(result, locbeg, locend)

'For debugging
'locend2 = locend + 10
'MsgBox (Mid(result2, locend, locend2))
'Cells(10, 4).Value = result

'Information placed here in Macro4()
location = Range("B18")

'looping through the Manifest Tracking Numbers placed here in Macro4() to get the Manifest data.
For i = 1 To location
    ' The URL for each Manifest, by Manifest tracking number
    NewURL = "https://rcrainfopreprod.epa.gov/rcrainfo/rest/api/v1/emanifest/manifest/" & Cells(i + 21, 1)
    ' The call for each Manifest, by Manifest tracking number, Please note this is a GET
    winHttpReq.Open "GET", NewURL, False
    winHttpReq.setRequestHeader "Accept", "application/json"
    winHttpReq.setRequestHeader "Authorization", result
    'Send the call
    winHttpReq.Send
    resultloadtype = winHttpReq.responseText

    'Writing the full text of the manifest to the cell next to the Manifesst Tracking Number
    Cells(i + 20, 2).Value = resultloadtype
'GET the next Manifest Tracking Number
Next i
End Sub

Sub GetManifestsIDs()
' Testing POSTing a search for a list of manifests

'Things to improve
' Error handling
' Parse the Authentication and post results JSON to values

' Variable Setting variables defined when used see comments below
Dim result As String
Dim resultloadtype As String
Dim locbeg As Integer
Dim locend As Integer
Dim location As Integer
Dim i As Integer
Dim URL As String
Dim NewURL As String
Dim JSONTxt As String
Dim SearchArray As Variant
Dim winHttpReq As Object

MsgBox ("Starting Search for Manifests ID")

'Creating the object so we can use services in thsi macro
Set winHttpReq = CreateObject("msxml2.xmlhttp.6.0")

'Setting the URL for Authentication, Please note APIID and APIKey are named ranges in the excel file
URL = "https://rcrainfopreprod.epa.gov/rcrainfo/rest/api/v1/auth/" & Range("APIID") & "/" & Range("APIKey")

'Calling methds from the winHttpReq object to get the authentiucation token
winHttpReq.Open "GET", URL, False
winHttpReq.Send
result = winHttpReq.responseText

'For debugging
'result2 = result
'Parsing the Authentication token.  There is a better way to parse data, but this is a proof on concept.
locbeg = InStr(result, ": ") + 3
locend = InStr(result, "expiration") - 22

result = "Bearer " & Mid(result, locbeg, locend)
'For debugging
'locend2 = locend + 10
'MsgBox (Mid(result2, locend, locend2))
'Cells(10, 5).Value = result
   
' The URL for searching for the Manifest tracking numbers
NewURL = "https://rcrainfopreprod.epa.gov/rcrainfo/rest/api/v1/emanifest/search"

' The call for getting a list of Manifest tracking numbers by site, Please note this is a POST
winHttpReq.Open "POST", NewURL, False
winHttpReq.setRequestHeader "Accept", "application/json"
winHttpReq.setRequestHeader "Authorization", result
'Set the The body of the text
' --- old code but here if you want to search on a whole state and 1 site JSONTxt = "{""stateCode"":""" & Range("State") & """,""siteId"":""" & Range("Site_ID") & """}"

' Calling the parseSearch function to create the body of the HTTP Request
JSONTxt = parseSearch()

If Len(JSONTxt) = 0 Then
    MsgBox ("You must enter a value to search on.")
    Exit Sub
ElseIf JSONTxt = "X" Then
    Exit Sub
End If

'Send the callnot the difference when sending the body, vs Macro3()
winHttpReq.Send JSONTxt
resultloadtype = winHttpReq.responseText

'Setting information about this call to show original response
Cells(15, 2).Value = resultloadtype
'Cleaning up the JSON array to make it an excel array
resultloadtype = Replace(resultloadtype, "[", "")
resultloadtype = Replace(resultloadtype, "]", "")
resultloadtype = Replace(resultloadtype, """", "")
'Setting information about this call to show changes from original response
Cells(16, 2).Value = resultloadtype
'Putting the cleaned JSON data into the Search Array
SearchArray = Split(resultloadtype, ",")
'Setting the array length so that Macro3() knows how many manifests to retrieve.  Since arrays start at 0 I added 1 to the end.
location = UBound(SearchArray)
Cells(18, 2).Value = location + 1

'Setting the Manifest Tracking numbers that will be searched in Macro3()
For i = 0 To location
Cells(21 + i, 1).Value = SearchArray(i)
Next i
Call GetManifests
MsgBox ("Complete")
End Sub
