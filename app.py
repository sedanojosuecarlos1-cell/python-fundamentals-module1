"""
=============================================================================
Titulo: Especialización en Python for Analytics
Autor   : Josue Sedano Ramirez
Año     : 2026
Módulo  : Módulo 1 - Python Fundamentals
=============================================================================
"""

import streamlit as st
import pandas as pd


# CONFIGURACIÓN GENERAL

st.set_page_config(
  page_title="Python Analytics - Módulo 1",
  layout="centered"
)

# Menú lateral de navegación
selected_page = st.sidebar.selectbox(
  "Navegación",
  options=["Home", "Ejercicio 1", "Ejercicio 2", "Ejercicio 3", "Ejercicio 4"]
)


# HOME – Presentación del proyecto

def render_home_page():
  """Página principal de proyecto."""

  st.title("Proyecto Módulo 1 – Python Fundamentals")
  st.markdown("---")

  st.write("**Estudiante:** Josue Sedano Ramirez")
  st.write("**Curso:** Especialización en Python for Analytics")
  st.write("**Módulo:** Módulo 1 – Python Fundamentals")
  st.write("**Año:** 2025")

  st.markdown("---")
  st.subheader("Descripción del proyecto")
  st.write(
    "Esta aplicación integra los conceptos fundamentales aprendidos en el Módulo 1: "
    "variables, estructuras de datos, control de flujo, funciones, "
    "y Programación Orientada a Objetos (POO). "
    "Cada ejercicio es un módulo independiente accesible desde el menú lateral."
  )

  st.markdown("---")
  st.subheader("Tecnologías utilizadas")
  st.write("- Python 3.13")
  st.write("- Streamlit")
  st.write("- Pandas")


# EJERCICIO 1 – Variables y Condicionales

def evaluate_budget(budget: float, expense: float) -> dict:
  """
  Evalúar si el gasto está dentro del presupuesto.

  Arguments:
    budget : Presupuesto disponible.
    expense: Gasto realizado.

  Returns:
    dict: Resultado con estado booleano y diferencia monetaria.
  """
  difference = budget - expense          # Diferencia
  is_within_budget = expense <= budget   # Gasto N0 supera el presupuesto

  return {
    "is_within_budget": is_within_budget,
    "difference": difference
  }


def render_exercise_1():
  """Muestra el Ejercicio 1: verificador de presupuesto vs gatso."""

  st.title("Ejercicio 1 – Variables y Condicionales")
  st.write("Ingresa un presupuesto y un gasto para saber si estás dentro del límite.")
  st.markdown("---")

  # Inputs
  budget  = st.number_input("Presupuesto disponible (S/)", min_value=0.0, step=100.0, value=1000.0) # Preesupueto
  expense = st.number_input("Gasto realizado (S/)",        min_value=0.0, step=100.0, value=800.0)  # GAsto

  # Botón para ejecutar la evaluación
  if st.button("Evaluar presupuesto"):
    result = evaluate_budget(budget, expense)

    # Mostrar resultado
    if result["is_within_budget"]:
      st.success(f"Dentro del presupuesto, te sobran S/{result['difference']:,.2f}")
    else:
      st.error(f"Presupuesto excedido, te pasaste por S/{abs(result['difference']):,.2f}")

    # Mostrar diferencia
    st.write(f"Diferencia: **S/{result['difference']:,.2f}**")


# EJERCICIO 2 – Listas y Diccionarios

# Lista en session_state para actividades entre interacciones
if "financial_activities" not in st.session_state:
  st.session_state.financial_activities = []   # Inicializa la lista

def add_activity(name: str, activity_type: str, budget: float, actual_expense: float):
  """
  Define un diccionario con los datos de una actividad

  Arguments:
    name          :   Nombre
    activity_type :   Tipo
    budget        : Presupuesto
    actual_expense: Gasto
  """
  activity = {
    "Nombre":      name,
    "Tipo":        activity_type,
    "Presupuesto": budget,
    "Gasto Real":  actual_expense,
    "Estado":      "OK" if actual_expense <= budget else "Excedido"
  }
  st.session_state.financial_activities.append(activity)  # Agrega a lista


def render_exercise_2():
  """Muestra el Ejercicio 2: registro de actividades financieras."""

  st.title("Ejercicio 2 – Listas y Diccionarios")
  st.write("Registra actividades financieras y consulta su estado.")
  st.markdown("---")

  # --- Formulario ---
  st.subheader("Agregar nueva actividad")

  activity_name     = st.text_input("Nombre de la actividad", placeholder="Ej: Alguna vaina")
  activity_type     = st.selectbox("Tipo de actividad", options=["Gasto", "Ingreso", "Inversión"])
  activity_budget   = st.number_input("Presupuesto asignado (S/)", min_value=0.0, step=100.0)
  activity_expense  = st.number_input("Gasto real (S/)",           min_value=0.0, step=100.0)

  # Agregar actividad
  if st.button("Agregar"):
    if activity_name.strip() == "":
      st.error("El nombre de la actividad no puede estar vacío.")
    else:
      add_activity(activity_name, activity_type, activity_budget, activity_expense)
      st.success(f"Actividad '{activity_name}' registrada correctamente.")

  st.markdown("---")

  # --- Tabla ---
  if len(st.session_state.financial_activities) == 0:
    st.info("Sin actividades registradas")
  else:
    # Convertir a DataFrame
    st.subheader("Actividades registradas")
    activities_df = pd.DataFrame(st.session_state.financial_activities)
    st.dataframe(activities_df, use_container_width=True)

    # Mostrar estado de cada actviida
    st.subheader("Estado detallado por actividad")
    for activity in st.session_state.financial_activities:
      difference = activity["Presupuesto"] - activity["Gasto Real"]
      if activity["Gasto Real"] <= activity["Presupuesto"]:
        st.success(f"**{activity['Nombre']}** — Dentro del presupuesto (diferencia: S/{difference:,.2f})")
      else:
        st.warning(f"**{activity['Nombre']}** — Excedida por S/{abs(difference):,.2f}")

    # Borrar toda la wea
    if st.button("Limpiar todo"):
      st.session_state.financial_activities = []
      st.rerun()


# EJERCICIO 3 – Funciones y Programación Funcional

def calculate_expected_return(activity: dict, rate: float, months: int) -> float:
  """
  Calcula el retorno esperado de una actividad financiera.

  Fórmula: Retorno = presupuesto × tasa × meses

  Arguments:
    activity:  Diccionario con datos de la actividad.
    rate    : Tasa de retorno.
    months  :   Número de meses de la inversión.

  Returns:
    float: Retorno esperado.
  """
  return activity["Presupuesto"] * rate * months


def render_exercise_3():
  """Muestra el Ejercicio 3: cálculo de retorno con map y lambda."""

  st.title("Ejercicio 3 – Funciones y Programación Funcional")
  st.write("Calcula el retorno esperado de cada actividad registrada usando `map` y `lambda`.")
  st.markdown("---")

  # Verificar actividades del Ejercicio 2
  if len(st.session_state.financial_activities) == 0:
    st.warning("No hay actividades registradas")
    return

  # Tasa y meses
  return_rate  = st.slider("Tasa de retorno (%)", min_value=0.0, max_value=50.0, value=5.0, step=0.5)
  months_count = st.number_input("Número de meses", min_value=1, max_value=120, value=12, step=1)

  # Convertir porcentaje a decimal
  rate_decimal = return_rate / 100

  # Botón para ejecutar el cálculo
  if st.button("Calcular retornos"):
    # map() aplica la lambda a cada elemento de la lista
    expected_returns = list(
      map(
        lambda activity: {
          "Actividad":        activity["Nombre"],
          "Presupuesto (S/)":  activity["Presupuesto"],
          "Tasa (%)":         return_rate,
          "Meses":            months_count,
          "Retorno Esperado (S/)": calculate_expected_return(activity, rate_decimal, months_count)
        },
        st.session_state.financial_activities   # Lista sobre la que se aplica el maaaapppp()
      )
    )

    st.subheader("Resultados de retorno esperado")

    #Rresultados en tabla
    returns_df = pd.DataFrame(expected_returns)
    st.dataframe(returns_df, use_container_width=True)

    # Total de retorno esperado
    total_return = sum(item["Retorno Esperado (S/)"] for item in expected_returns)
    st.success(f"Retorno total esperado de todas las actividades: **S/{total_return:,.2f}**")


# EJERCICIO 4 – Programación Orientada a Objetos (POO)

class FinancialActivity:
  """
  Clase que modela una actividad financiera con atributos y métodos.

  Atributos:
    name          :   Nombre.
    activity_type :   Tipo.
    budget        : Presupuesto.
    actual_expense: Gasto.
  """

  def __init__(self, name: str, activity_type: str, budget: float, actual_expense: float):
    """Inicializa los atributos del objeto."""
    self.name           = name
    self.activity_type  = activity_type
    self.budget         = budget
    self.actual_expense = actual_expense

  def is_within_budget(self) -> bool:
    """
    Evalúa si el gasto real no supera el presupuesto

    Returns:
      bool: Dentro del presupuesto
    """
    return self.actual_expense <= self.budget

  def get_difference(self) -> float:
    """
    Calcula la diferencia entre presupuesto y gasto real

    Returns:
      float: Diferencia
    """
    return self.budget - self.actual_expense

  def get_summary(self) -> str:
    """
    Genera un resumen de texto de la actividad

    Returns:
      str: Resumen con los datos principales de la actividad
    """
    status = "Dentro del presupuesto" if self.is_within_budget() else "Excedida"
    return (
      f"Actividad: {self.name} | "
      f"Tipo: {self.activity_type} | "
      f"Presupuesto: S/{self.budget:,.2f} | "
      f"Gasto Real: S/{self.actual_expense:,.2f} | "
      f"Estado: {status}"
    )


def convert_activities_to_objects(activities: list) -> list:
  """
  Convierte una lista de diccionarios en una lista de objetos FinancialActivity.

  Arguments:
    activities: Lista de diccionarios del Ejercicio 2.

  Returns:
    list: Lista de objetos FinancialActivity.
  """
  return [
    FinancialActivity(
      name           = act["Nombre"],
      activity_type  = act["Tipo"],
      budget         = act["Presupuesto"],
      actual_expense = act["Gasto Real"]
    )
    for act in activities   # List comprehension para crear objetos desde diccionarios
  ]


def render_exercise_4():
  """Muestra el Ejercicio 4: uso de clases y POO."""

  st.title("Ejercicio 4 – Programación Orientada a Objetos (POO)")
  st.write("Se utiliza la clase `FinancialActivity` para modelar cada actividad como un objeto.")
  st.markdown("---")

  # Verificar actividades registradas en el Ejercicio 2
  if len(st.session_state.financial_activities) == 0:
      st.warning("No hay actividades registradas")
      return

  # Convertir diccionarios en FinancialActivity
  activity_objects = convert_activities_to_objects(st.session_state.financial_activities)

  st.subheader(f"Se crearon {len(activity_objects)} objeto(s) de tipo `FinancialActivity`")
  st.markdown("---")

  # Info de cada objeto
  for obj in activity_objects:
    summary = obj.get_summary()          # mostrar_info
    difference = obj.get_difference()    # diferencia

    # Mostrar color según estado
    if obj.is_within_budget():
      st.success(summary)
      st.write(f"Sobrante: **S/{difference:,.2f}**")
    else:
      st.warning(summary)
      st.write(f"Excedido en: **S/{abs(difference):,.2f}**")

    st.markdown("---")


# ENRUTADOR

if   "Home"       in selected_page: render_home_page()
elif "Ejercicio 1" in selected_page: render_exercise_1()
elif "Ejercicio 2" in selected_page: render_exercise_2()
elif "Ejercicio 3" in selected_page: render_exercise_3()
elif "Ejercicio 4" in selected_page: render_exercise_4()