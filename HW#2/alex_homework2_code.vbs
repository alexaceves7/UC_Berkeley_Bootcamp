sub moderate_code()

'----------------------------------------------------------

' Moderate

'----------------------------------------------------------

Dim last_row as double
' last_row will count the last row and will be used for the for loop

Dim ticker as string
' ticker is the variable that will save the ticker for the new table

Dim opening_price as double
Dim closing_price as double
'will save the opening price and closing price to find the change

Dim year_change as double
Dim percent_change as double
'will store the change and percent for printing on new table

Dim total_stock as double
' total_stock will be accumulating the total volume per ticker for the new table

Dim i as long 
' i is for the for loop

Dim ticker_row as integer  
' ticker_row is the row in the new table the information will be added to


total_stock = 0
' the total stock volume is starting at 0


For each ws in worksheets
    ticker_row = 2
    last_row = ws.cells(rows.count, 1).end(xlup).row
    ' calculating the last row
    opening_price = ws.cells(2, 3).value 
    for i = 2 to last_row
    ' loop will go through each row at a time 

'-----use the if for zero in the other if and if zero don't do the division vs do the division

 
        if ws.cells(i+1, 1).value <> ws.cells(i, 1).value then 'not equal
            ticker = ws.cells(i, 1).value
            'sets the ticker to the value on that cell
            total_stock = total_stock + ws.cells(i, 7).value
            'adds the final volume to total stock
            closing_price = ws.cells(i, 6).value
            'saves the closing price for that year
            year_change = closing_price - opening_price
            'gets the year change
           
            if opening_price <> 0 then 
                percent_change = year_change/opening_price
                'gets the percent change
            else percent_change = 0
            end if

            ws.range("I" & ticker_row).value = ticker
            'adds the ticker to the new table
            ws.range("L" & ticker_row).value = total_stock
            'adds the final total to the new table
            ws.range("J" & ticker_row).value = year_change
            'adds the year change to the new table
            if year_change < 0 then
                ws.range("J" & ticker_row).interior.colorindex = 3
            else ws.range("J" & ticker_row).interior.colorindex = 4
            end if 
            'if statement to change colors
            ws.range("K" & ticker_row).value = percent_change
            'adds the percenr to the new table
            ticker_row = ticker_row + 1
            'adds to the ticker row count for next ticker type
            total_stock = 0
            'resets the total to 0 
            opening_price = ws.cells(i+1, 3).value 
        else 
            total_stock = total_stock + ws.cells(i, 7).value
            'if tickers are equal, just keeps adding to total 
        end if
        
    next i 
    ws.cells(1, 9).value = "Ticker" 
    ws.cells(1, 10).value = "Yearly Change"
    ws.cells(1, 11).value = "Percent Change"
    ws.cells(1, 12).value = "Total Stock Volume"
    'Headers
    ws.Range("K2:K100000").NumberFormat = "0.00%"
    'makes the new table percents a percent
next ws

End sub

'-------------------------------------------------------------------

'Hard
'I set up a new sub for the new table, used two buttons 
'one button for the moderate code and one for the hard code

'-------------------------------------------------------------------

Sub hard_code()

Dim change_lastrow as double
Dim max_percent as double
Dim max_volume as double 
Dim min_percent as double 
Dim max_ticker as string
Dim min_ticker as string
Dim ticker_volume as string
'set up all my variables



For each ws in worksheets
    change_lastrow = ws.cells(rows.count, 9).end(xlup).row
    'gets last row of new table created in moderate
    max_percent = 0
    min_percent = 0
    max_volume = 0 
    'starts all variables fresh at zero
    for j = 2 to change_lastrow
        if ws.cells(j, 11).value > max_percent then
            max_percent = ws.cells(j, 11).value
            max_ticker = ws.cells(j, 9).value 
            'gets the max percent 
        elseif ws.cells(j, 11).value < min_percent then
            min_percent = ws.cells(j, 11).value
            min_ticker = ws.cells(j, 9).value 
            'gets the min percent
        end if 
        if ws.cells(j, 12).value > max_volume then
            max_volume = ws.cells(j, 12).value 
            ticker_volume = ws.cells(j, 9).value 
            'new if for the max volume
        end if
    next j

    ws.range("O1").value = "Ticker"
    ws.range("P1").value = "Value"
    ws.range("N2").value = "Greatest % Increase"
    ws.range("O2").value = max_ticker
    ws.range("P2").value = max_percent
    ws.range("N3").value = "Greatest % Decrease"
    ws.range("O3").value = min_ticker
    ws.range("P3").value = min_percent
    ws.range("N4").value = "Greatest Total Volume"
    ws.range("O4").value = ticker_volume
    ws.range("P4").value = max_volume  
    'Sets up and prints to new table
next ws 

End Sub