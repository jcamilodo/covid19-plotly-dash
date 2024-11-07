import pandas as pd

def agrupar_departamentos(df):

    # Filtrar por COVID-19 = CONFIRMADOS
    df_covid_confirmados = df[df['COVID-19'] == 'CONFIRMADO']

    # Agrupar por DEPARTAMENTO y asignar campo cantidad
    grouped_dpto = df_covid_confirmados.groupby('DEPARTAMENTO').size().reset_index(name='CANTIDAD')

    grouped_dpto['DEPARTAMENTO'] = grouped_dpto['DEPARTAMENTO'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

    grouped_dpto['DEPARTAMENTO'] = grouped_dpto['DEPARTAMENTO'].apply(lambda x: 'NARIÑO' if x == 'NARINO' else x)
    grouped_dpto['DEPARTAMENTO'] = grouped_dpto['DEPARTAMENTO'].apply(lambda x: 'SANTAFE DE BOGOTA D.C' if x == 'BOGOTA, D.C.' else x)
    grouped_dpto['DEPARTAMENTO'] = grouped_dpto['DEPARTAMENTO'].apply(lambda x: 'ARCHIPIELAGO DE SAN ANDRES PROVIDENCIA Y SANTA CATALINA' if "ARCHIPIELAGO DE SAN ANDRES, PROVIDENCIA" in x else x)

    return grouped_dpto


def ciudad_indice(df, max):
    # 
    df_covid_confirmados = df[df['COVID-19'] == 'CONFIRMADO']

    # Calcular el numero total de registros
    total_records = len(df_covid_confirmados)

    # Group by MUNICIPIO and calculate counts
    municipio_counts = df_covid_confirmados.groupby('MUNICIPIO').size().reset_index(name='CANTIDAD')

    # Calculate INDICE_MUERTE
    municipio_counts['INDICE_MUERTE'] = municipio_counts['CANTIDAD'] / total_records

    # Calculate INDICE_PER
    municipio_counts['INDICE_PER'] = round(((municipio_counts['CANTIDAD'] / total_records) * 1000), 2)

    # Order by INDICE_PER in descending order
    municipio_counts = municipio_counts.sort_values('INDICE_PER', ascending=False)

    # Display the resulting DataFrame
    municipio_counts = municipio_counts.head(max)    

    return municipio_counts

def muertes_mes_anio(df):
    df_covid_confirmados = df[df['COVID-19'] == 'CONFIRMADO']
    # Convert 'FECHA DEFUNCIÓN' to datetime objects, handling errors
    df_covid_confirmados['FECHA DEFUNCIÓN'] = pd.to_datetime(df_covid_confirmados['FECHA DEFUNCIÓN'], errors='coerce')

    # Create 'Year-Month' column
    df_covid_confirmados['Year-Month'] = df_covid_confirmados['FECHA DEFUNCIÓN'].dt.to_period('M')
    df_covid_confirmados['Year-Month'] = df_covid_confirmados['Year-Month'].astype('str')

    # Group by 'Year-Month' and count
    grouped_by_month = df_covid_confirmados.groupby('Year-Month').size().reset_index(name='CANTIDAD')    

    return grouped_by_month

def min_edad(rango):
  if '+'  in rango:
    return int(90)
  min = rango.split('-')[0].strip()
  return int(min)

def frecuencia_muertes(df):
    df_covid_confirmados = df[df['COVID-19'] == 'CONFIRMADO']
    # Group by 'RANGO EDAD' and count
    rango_edad_counts = df_covid_confirmados.groupby('RANGO EDAD').size().reset_index(name='CANTIDAD')
    rango_edad_counts['MIN_EDAD'] = rango_edad_counts['RANGO EDAD'].apply(min_edad)
    rango_edad_counts = rango_edad_counts.sort_values('MIN_EDAD')

    return rango_edad_counts