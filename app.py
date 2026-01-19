import streamlit as st
import pandas as pd
import io
import matplotlib.pyplot as plt
import seaborn as sns

#Clasificación  de Variables:
def clasificar_variables(df):
    numericas = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
    categoricas = df.select_dtypes(include=["object"]).columns.tolist()
    return numericas, categoricas

#Aplicación:
st.set_page_config(
    page_title= "Proyecto",
    layout="wide"
)

#Menú Principal:
st.sidebar.title("Menú")
opcion = st.sidebar.radio(
    "Escoge una opción:",
    ["Home", "Carga del Dataset", "EDA", "Conclusiones"]
)

#PÁGINA 1:
if opcion == "Home":
    st.title("Mi Primer Proyecto de Portafolio Profesional")

    st.markdown(
        "<h3 style='color:#ff7f0e;'> Sobre el Proyecto:</h3>",
        unsafe_allow_html=True
    )

    st.write("Este proyecto mostrará un análisis de datos, transformación y visualización de datos sobre la deserción de los clientes en una empresa de telecomunciones.")
    st.write("En el dataset utilizado se puede obtener el detalle de los servicios del cliente, método de pago, el tipo de contrato, costo y si presenta Churn")
    st.markdown("""
    Las tecnologías utilizadas para realizar este proyecto son:
    - Python 
    - Pandas 
    - Streamlit
    - Io""")

    st.markdown(
        "<h3 style='color:#ff7f0e;'> Datos del Desarrollador:</h3>",
        unsafe_allow_html=True
    )
    st.markdown("""
    - **Alumno:** Sayda Bravo
    - **Curso / Especialización:** Especialización en Python for Analytics
    - **Año:** 2026""")

#Carga de Dataset:
elif opcion == "Carga del Dataset":

    st.title("Carga del Dataset:")

    archivo = st.file_uploader(
        "Selecciona un archivo:", type=["csv"]
    )

    if archivo is not None:
        df = pd.read_csv(archivo)
        st.session_state["df"] = df
        st.success("Archivo cargado correctamente")

        st.markdown(
        "<h3 style='color:#ff7f0e;'> Vista previa del dataset:</h3>",
        unsafe_allow_html=True
        )
        st.dataframe(df.head())


        st.markdown(
        "<h3 style='color:#ff7f0e;'> Dimensiones del Dataset:</h3>",
        unsafe_allow_html=True
        )
        st.write(f"Filas: {df.shape[0]}")
        st.write(f"Columnas: {df.shape[1]}")

    else:
        st.warning("El archivo no esta cargado. Porfavor, añadirlo")

#Análisis de todos los ítems solicitados:
elif opcion == "EDA":
    
    if "df" not in st.session_state:
        st.warning("Cargar el Dataset para continuar")
    else:
        df = st.session_state["df"]
        st.title("Análisis del Dataset:")

#ítem número 1:
    st.markdown(
    "<h3 style='color:#ff7f0e;'> Ítem 1: Información general del dataset</h3>",
    unsafe_allow_html=True)

    buffer = io.StringIO()
    df.info(buf=buffer)
    info_texto = buffer.getvalue()

    st.text(info_texto)

    st.subheader("Conteo de valores nulos")
    st.write(df.isnull().sum())

#Ítem número 2:
    st.markdown(
    "<h3 style='color:#ff7f0e;'> Ítem 2: Clasificación de variables</h3>",
    unsafe_allow_html=True)
    numericas, categoricas = clasificar_variables(df)
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Variables Numéricas")
        st.write(numericas)
        st.write(f"Total: {len(numericas)}")

    with col2:
        st.subheader("Variables Categóricas")
        st.write(categoricas)
        st.write(f"Total: {len(categoricas)}")

#Ítem número 3:
    st.markdown(
    "<h3 style='color:#ff7f0e;'> Ítem 3: Estadísticas descriptivas</h3>",
    unsafe_allow_html=True
    )

    st.subheader("Resumen estadístico de variables numéricas")
    st.dataframe(df.describe())

#Ítem número 4:
    st.markdown(
    "<h3 style='color:#ff7f0e;'> Ítem 4: Análisis de valores faltantes</h3>",
    unsafe_allow_html=True
    )

    missing = df.isnull().sum()
    st.subheader("Conteo de valores faltantes por variable")
    st.dataframe(missing[missing > 0])
    st.markdown("""
    **Nota:**
    - No se observan valores nulos explícitos en el dataset, pero este contiene datos para reemplazar los nulos como los 0 en datos numéricos.
    """)
    st.write("Valores vacíos en TotalCharges (CARGOS TOTALES):")
    st.write(df["TotalCharges"].str.strip().eq("").sum())

#Ítem número 5:
    st.markdown(
    "<h3 style='color:#ff7f0e;'> Ítem 5: Distribución de variables numéricas</h3>",
    unsafe_allow_html=True
    )

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    sns.histplot(
    data=df,
    x="tenure", #Permanencia
    hue="Churn", #Indicador
    bins=30,
    kde=True,
    ax=axes[0]
    )
    axes[0].set_title("Distribución de tenure/Permanencia según Churn")

    sns.histplot(
        data=df,
        x="MonthlyCharges",  #Cargos Mensuales
        hue="Churn", #Indicador
        bins=30,
        kde=True,
        ax=axes[1]
    )
    axes[1].set_title("Distribución de MonthlyCharges /Cargos Mensuales según Churn")

    st.pyplot(fig)

    st.markdown("""
    **Análisis de Ítem 5:**\n
    _Gráfico 1:_
    - Los clientes que tienen menor tiempo de permanencia presentan un churn superior.
    - Por lo que se deberá enfocar en este segmento de clientes para próximos análisis.\n
    _Gráfico 2:_
    - Se observa que clientes con cargos mensuales tienen mayor Churn, por lo que se se debe evaluar el tipo de servicios que tiene el cliente.
    """)

#Ítem 6,7 y 8 análisis:
    st.markdown(
    "<h3 style='color:#ff7f0e;'> Ítem 6,7 y 8: Variables categóricas según Churn</h3>",
    unsafe_allow_html=True
    )

    fig, ax = plt.subplots(figsize=(6,4))
    sns.countplot(
        data=df,
        x="Contract",
        hue="Churn",
        ax=ax
    )
    ax.set_title("Tipo de contrato vs Churn")
    ax.set_xlabel("Tipo de contrato")
    ax.set_ylabel("Cantidad de clientes")
    st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(6,4))

    sns.countplot(
        data=df,
        x="InternetService",
        hue="Churn",
        ax=ax
    )

    ax.set_title("Servicio de Internet vs Churn")
    ax.set_xlabel("Tipo de servicio")
    ax.set_ylabel("Cantidad de clientes")
    st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(7,4))
    sns.countplot(
        data=df,
        x="PaymentMethod",
        hue="Churn",
        ax=ax
    )

    ax.set_title("Método de pago vs Churn")
    ax.set_xlabel("Método de pago")
    ax.set_ylabel("Cantidad de clientes")
    ax.tick_params(axis='x', rotation=30)
    st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(6,4))

    sns.boxplot(
        data=df,
        x="Churn",
        y="tenure",
        ax=ax
    )

    ax.set_title("Permanencia según Churn")
    ax.set_xlabel("Churn")
    ax.set_ylabel("Meses de permanencia")

    st.pyplot(fig)

    st.markdown("""
    **Análisis:**
    - Los clientes con contrato mensual presentan una mayor Churn.
    - El servicio de internet por fibra óptica muestra mayor Churn, lo cuál es raro porque la Fibra Óptica es mejor respecto a la tecnología.
    - Métodos de pago automáticos presentan un menor Churn.
    - Mayor Churn hasta maso menos unos 30 meses desde la contratación.
    """)

#Última parte del análisis:
    st.markdown(
    "<h3 style='color:#ff7f0e;'> Ítem 9: Análisis dinámico con selectbox</h3>",
    unsafe_allow_html=True
    )

    variable = st.selectbox(
        "Selecciona una variable categórica:",
        [
            "Contract",
            "InternetService",
            "PaymentMethod",
            "gender",
            "SeniorCitizen"
        ]
    )

    fig, ax = plt.subplots(figsize=(6,4))

    sns.countplot(
        data=df,
        x=variable,
        hue="Churn",
        ax=ax
    )

    ax.set_title(f"{variable} vs Churn")
    ax.tick_params(axis='x', rotation=30)

    st.pyplot(fig)

    st.markdown(
    "<h3 style='color:#ff7f0e;'> Análisis con múltiples variables</h3>",
    unsafe_allow_html=True
    )

    variables = st.multiselect(
        "Selecciona una o más variables categóricas:",
        [
            "Contract",
            "InternetService",
            "PaymentMethod",
            "gender",
            "SeniorCitizen"
        ]
    )

    for var in variables:
        fig, ax = plt.subplots(figsize=(6,4))

        sns.countplot(
            data=df,
            x=var,
            hue="Churn",
            ax=ax
        )

        ax.set_title(f"{var} vs Churn")
        ax.tick_params(axis='x', rotation=30)

        st.pyplot(fig)

#Final:        
elif opcion == "Conclusiones":

    if "df" not in st.session_state:
        st.warning("Primero debes cargar el dataset.")
    else:
        df = st.session_state["df"]

        df_churn = df[df["Churn"] == "Yes"]
        clientes_churn = df_churn.shape[0]
        perdida_total = df_churn["MonthlyCharges"].sum()

        st.title("Conclusiones:")
        st.markdown(
            "<h3 style='color:#ff7f0e;'> Impacto económico del Churn</h3>",
            unsafe_allow_html=True
        )

        st.metric(
            label="Total de clientes que desertaro:",
            value=clientes_churn
        )

        st.metric(
            label="Pérdida mensual estimada (COSTOS):",
            value=f"{perdida_total:,.2f}"
        )

        impacto = pd.DataFrame({
            "Estado del cliente": ["Clientes retenidos", "Clientes que desertaron"],
            "Ingresos mensuales": [
                df[df["Churn"] == "No"]["MonthlyCharges"].sum(),
                df[df["Churn"] == "Yes"]["MonthlyCharges"].sum()
            ]
        })

        fig, ax = plt.subplots(figsize=(6,4))

        sns.barplot(
            data=impacto,
            x="Estado del cliente",
            y="Ingresos mensuales",
            ax=ax
        )

        ax.set_title("Impacto económico mensual del Churn")
        ax.set_ylabel("Ingresos mensuales (moneda del dataset)")
        ax.tick_params(axis='x', rotation=10)

        st.pyplot(fig)

        st.markdown(
            "<h3 style='color:#ff7f0e;'> Conclusiones Finales:</h3>",
            unsafe_allow_html=True
        )
        
        st.markdown("""
        - Cómo pudemos observar en los gráficos los puntos más importantes a evaluar es el tipo de cliente que esta desertando en la empresa, siendo estos los clientes 
         que tienen fibra óptica, presentar un contrato mensual, pagan por electronic check y tienen el servicio contratado, es decir son clientes nuevos.
        - Por un lado, se debe investigar la tecnología que brinda la empresa, ya que se sabe que la Fibra Óptica es la mejor tecnología para el servicio de internet. Averiguar si es un tema de  una incorrecta instalación, daños externos en la fibra o si la tecnología no es la viable para sus clientes.
        - Por otro lado, podemos ver que los clientes retenidos tienen mayor ingreso, por lo que insentivar una retención  y crear nuevas herramientas de retención es en lo que se debe enfocar la empresa.
        \n
        
        - Con todo ello, se puede crear una campaña de prevención en los clientes nuevos que tengan fibra óptica contratada, para revisar inconvenientes, retenerlos antes de que los clientes lo hagan por si mismos, ver la viabiliad de migrarlos de tecnología o realizar una reinstalación para solucionar el problema del cliente. 
        Asimsimo, se deben incrementar las herramientas de retención que presenta la empresa, como tener descuentos estratégicos, mantenimiento priorizado para clientes nuevos e incentivar el pago automático de tarjeta, ya que presenta menor Churn.
        Durante la venta del servicio, se debe priorizar un contrato de dos o un año y pago automático con tarjeta, todo esto acompañado de un seguimiento en los primeros meses del servicio para evitar inconvenientes futuros.
        """)


