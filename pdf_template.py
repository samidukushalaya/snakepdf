PDF_TEMPLATE = """%PDF-1.6

1 0 obj
<<
/AcroForm << /Fields [ ###FIELD_LIST### ] >>
/Pages 2 0 R
/OpenAction 17 0 R
/Type /Catalog
>>
endobj

2 0 obj
<<
/Count 1
/Kids [ 16 0 R ]
/Type /Pages
>>
endobj

21 0 obj
[
###FIELD_LIST###
]
endobj

###FIELD_OBJECTS###

16 0 obj
<<
/Annots 21 0 R
/Contents 3 0 R
/CropBox [ 0 0 612 792 ]
/MediaBox [ 0 0 612 792 ]
/Parent 2 0 R
/Resources << >>
/Rotate 0
/Type /Page
>>
endobj

3 0 obj
<< >>
stream
endstream
endobj

17 0 obj
<<
/JS 42 0 R
/S /JavaScript
>>
endobj

42 0 obj
<< >>
stream

###GAME_JS###

endstream
endobj

trailer
<<
/Root 1 0 R
>>

%%EOF
"""