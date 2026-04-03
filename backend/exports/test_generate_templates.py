# Librerias
import os
import sys

# Agregar el root del backend al path para que las importaciones relativas funcionen
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import SessionLocal
from uploads import process_attendance_excel
from exports import generate_attendance_template

def run_tests():
    db = SessionLocal()
    
    # 1. Probar generar plantilla
    print("Probando generación de plantilla...")
    students_mock = [
        {"enrollment_id": 1, "nickname": "Juanito", "full_name": "Juan Perez"},
        {"enrollment_id": 2, "nickname": "Maria", "full_name": "Maria Lopez"},
    ]
    try:
        excel_stream = generate_attendance_template(2026, 4, students_mock)
        with open("test_abril_2026.xlsx", "wb") as f:
            f.write(excel_stream.read())
        print("Plantilla generada exitosamente en test_abril_2026.xlsx")
    except Exception as e:
        print(f"Error al generar plantilla: {e}")
        
    # 2. Probar parsear archivo existente
    print("\nProbando parseo del archivo...")
    data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data", "Lista de Asistencias UBBJ.xlsx")
    if os.path.exists(data_path):
        try:
            with open(data_path, "rb") as f:
                content = f.read()
            result = process_attendance_excel(content, db)
            print("Parseo exitoso:")
            print(result)
        except Exception as e:
            print(f"Error al parsear: {e}")
    else:
        print(f"Archivo no encontrado en {data_path}. (Asegúrate de que existe)")
        
    db.close()

if __name__ == "__main__":
    run_tests()
