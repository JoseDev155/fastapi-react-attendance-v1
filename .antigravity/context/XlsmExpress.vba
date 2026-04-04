' Macros de la hoja Asistencia Express (Hoja2), Plantilla.xlsm
' Configuración: A6=Día, B6=Hora, C6=Trigger(1), E6=Días de clase (ej: Lunes, Jueves)
' Compatible con encabezados: "Lun 06", "Mart 07", "Mie 08", etc.

Private Sub Worksheet_Change(ByVal Target As Range)
    Dim wsAsistencia As Worksheet
    Dim celdaTrigger As Range, celdaConfig As Range
    
    Set celdaTrigger = Me.Range("C6")
    Set celdaConfig = Me.Range("B18")
    Set wsAsistencia = ThisWorkbook.Worksheets("Asistencias 2025-10")

    ' --- CASO A: Asistencia Masiva (Activado por C6) ---
    If Not Intersect(Target, celdaTrigger) Is Nothing Then
        If Target.Value = 1 Then
            Call EjecutarAsistenciaMasiva(wsAsistencia, Me.Range("A6").Value, Me.Range("B6").Value)
            
            Application.EnableEvents = False
            Me.Range("C6").Value = 0
            Me.Range("A6").ClearContents
            Me.Range("B6").ClearContents
            Application.EnableEvents = True
        End If
    End If

    ' --- CASO B: Configurar Hoja / Ocultar Columnas (Activado por E6) ---
    If Not Intersect(Target, celdaConfig) Is Nothing Then
        Call ConfigurarColumnasVisibles(wsAsistencia, celdaConfig.Value)
    End If
End Sub

' --- RUTINA: Asistencia Masiva ---
Private Sub EjecutarAsistenciaMasiva(ws As Worksheet, dia As String, hora As Variant)
    Dim colBusqueda As Range, colIndex As Long, i As Long
    
    Set colBusqueda = ws.Rows(4).Find(What:=dia, LookIn:=xlValues, LookAt:=xlPart)
    
    If colBusqueda Is Nothing Then
        MsgBox "No se encontró la columna para el día: " & dia, vbCritical
        Exit Sub
    End If
    
    colIndex = colBusqueda.Column
    Application.ScreenUpdating = False
    
    For i = 5 To 104
        If Trim(ws.Cells(i, 1).Value) <> "" And Trim(ws.Cells(i, 2).Value) <> "" Then
            ws.Cells(i, colIndex).Value = hora
            ws.Cells(i, colIndex).NumberFormat = "hh:mm:ss"
        End If
    Next i
    
    Application.ScreenUpdating = True
    MsgBox "Asistencia cargada con éxito.", vbInformation
End Sub

' --- RUTINA: Ocultar/Mostrar Columnas con match inteligente ---
Private Sub ConfigurarColumnasVisibles(ws As Worksheet, diasInput As String)
    Dim diasArray As Variant, col As Long, diaActual As Variant
    Dim encabezadoOriginal As String, prefijoHeader As String, diaLimpio As String
    Dim mostrar As Boolean

    Application.ScreenUpdating = False
    ws.Columns.Hidden = False 
    
    If Trim(diasInput) = "" Then Exit Sub
    
    diasArray = Split(diasInput, ",")
    
    ' Columnas de la C (3) a la AG (33)
    For col = 3 To 33
        encabezadoOriginal = Trim(ws.Cells(4, col).Value)
        If encabezadoOriginal = "" Then GoTo SiguienteColumna
        
        ' Extraer solo la parte del texto (ej: de "Mart 07" extrae "mart")
        If InStr(encabezadoOriginal, " ") > 0 Then
            prefijoHeader = LCase(Left(encabezadoOriginal, InStr(encabezadoOriginal, " ") - 1))
        Else
            prefijoHeader = LCase(encabezadoOriginal)
        End If
        
        mostrar = False
        For Each diaActual In diasArray
            diaLimpio = LCase(Trim(diaActual))
            ' Normalización básica para "Mie" vs "Mié"
            diaLimpio = Replace(diaLimpio, "á", "a"): diaLimpio = Replace(diaLimpio, "é", "e")
            diaLimpio = Replace(diaLimpio, "í", "i"): diaLimpio = Replace(diaLimpio, "ó", "o")
            diaLimpio = Replace(diaLimpio, "ú", "u")

            ' Si el prefijo (lun, mart, mie) está contenido en el día ingresado (lunes, martes, miercoles)
            If InStr(1, diaLimpio, prefijoHeader, vbTextCompare) > 0 Then
                mostrar = True
                Exit For
            End If
        Next diaActual
        
        If Not mostrar Then ws.Columns(col).Hidden = True

SiguienteColumna:
    Next col
    
    Application.ScreenUpdating = True
End Sub