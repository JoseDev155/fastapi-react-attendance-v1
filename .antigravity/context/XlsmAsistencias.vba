' Macros de la hoja Asistencias 2025-10 (Hoja1), Plantilla.xlsm

Private Sub Worksheet_Change(ByVal Target As Range)
    Dim cell As Range
    Dim affectedCells As Range
    Dim attendanceRange As Range
    
    ' 1. Definimos el rango de trabajo
    Set attendanceRange = Me.Range("C5:AG105")
    
    ' 2. Intentamos la intersección de forma segura
    On Error Resume Next
    Set affectedCells = Application.Intersect(Target, attendanceRange)
    On Error GoTo 0
    
    ' Si el cambio es fuera del rango o no hay celdas, salimos
    If affectedCells Is Nothing Then Exit Sub
    
    ' 3. Usamos .Count (más compatible que CountLarge)
    If affectedCells.Count > 500 Then Exit Sub

    ' 4. Ejecución del cambio
    On Error GoTo CleanUp
    Application.EnableEvents = False
    
    For Each cell In affectedCells
        ' Verificamos que la celda no esté vacía y sea un 1
        If Not IsEmpty(cell) Then
            If cell.Value = 1 Then
                cell.Value = TimeSerial(Hour(Time), Minute(Time), 0)
                cell.NumberFormat = "hh:mm:ss"
            End If
        End If
    Next cell

CleanUp:
    Application.EnableEvents = True
End Sub
