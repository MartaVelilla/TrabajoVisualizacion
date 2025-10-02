# TrabajoVisualizacion
Analisis de datos del sueño

## Introducción
En la sociedad actual, la calidad del sueño se ha convertido en un elemento central para entender y mejorar tanto la salud como el rendimiento físico y cognitivo de las personas. Distintos estudios científicos han demostrado la estrecha relación existente entre los patrones de sueño y variables fisiológicas como la frecuencia cardiaca, la variabilidad de la frecuencia cardiaca (HRV), la frecuencia respiratoria y el gasto energético. Asimismo, mantener un descanso adecuado influye de manera significativa en el estado de ánimo, la concentración, la productividad y la recuperación física tras la actividad deportiva.
El presente proyecto se enmarca en la asignatura de Desarrollo de Aplicaciones para la Visualización de Datos y tiene como finalidad la implementación de una aplicación capaz de analizar y representar información proveniente de un conjunto de datos personales de sueño. Estos datos han sido recopilados durante un período de más de un año mediante el uso de un reloj inteligente de la marca Apple. La idea principal es construir un modelo de análisis que permita comprender en qué medida la calidad del sueño afecta otras variables fisiológicas y hábitos diarios, con el objetivo último de crear una herramienta visual y analítica que proporcione conclusiones significativas y fácilmente interpretables.

## Base de datos
La base de datos cuenta con 528 observaciones continuas, cada una correspondiente a una noche registrada durante más de un año. Los registros permiten un estudio longitudinal de los patrones de sueño y de su impacto diario.
Cada registro incluye múltiples variables que forman un conjunto multidimensional rico en información:
•	Fecha de registro  
•	Duración total del sueño  
•	Duración de cada fase del sueño (sueño Core, sueño profundo, sueño REM, tiempo despierto)  
•	Frecuencia cardiaca mínima, máxima y media durante la noche  
•	Frecuencia respiratoria
•	Horas en posición de pie durante el día siguiente
•	Frecuencia cardiaca promedio mientras se camina
•	Tiempo total dedicado a la actividad física durante el día
•	Tiempo total de exposición a la luz
•	Variabilidad de la frecuencia cardiaca

## Objetivos del proyecto
El proyecto plantea tanto objetivos generales como específicos:
Objetivo general:
Diseñar y desarrollar una aplicación de análisis y visualización de datos de sueño que permita identificar patrones significativos y establecer relaciones entre la calidad del descanso y otros indicadores fisiológicos y de actividad diaria.
Objetivos específicos:
•	Analizar estadísticamente las diferentes fases del sueño y su influencia en métricas como frecuencia cardiaca.
•	Estudiar tendencias a lo largo del tiempo, detectando mejoras o deterioros en los hábitos de descanso.
•	Investigar la relación existente entre la calidad del sueño y el tiempo dedicado a la actividad física al día siguiente.
•	Desarrollar un sistema de visualizaciones interactivas que permitan explorar comparaciones personalizadas (por ejemplo, sueño profundo vs. frecuencia cardiaca media).
•	Explorar la posibilidad de elaborar un modelo predictivo sencillo que estime la calidad del sueño a partir de variables relacionadas con la frecuencia cardiaca y la actividad diaria.

## Metodología y herramientas
Para lograr los objetivos planteados, el desarrollo del proyecto se estructurará en varias fases:
1.	Preparación de los datos: limpieza, transformación y organización de las 528 observaciones en un formato adecuado para el análisis.
2.	Análisis de datos: identificación de valores atípicos, análisis de distribuciones y primeras correlaciones entre variables.
3.	Modelado estadístico y predictivo: aplicación de técnicas de regresión lineal o modelos más avanzados (ej. Random Forest de regresión) para explorar relaciones causales.
4.	Visualización de datos: diseño de gráficos descriptivos y dashboards interactivos. Se emplearán herramientas como Python (pandas, matplotlib, seaborn, plotly) o entornos especializados como Tableau o Power BI.
5.	Interpretación de resultados y conclusiones: generar un informe integrador que resuma patrones encontrados y recomendaciones personalizadas sobre el hábito de sueño.
## Resultados esperados
Se espera que la aplicación permita:
•	Visualizar de forma clara y atractiva la evolución de la calidad del sueño durante más de un año.
•	Identificar relaciones llamativas, por ejemplo, entre el sueño REM y la productividad física del día siguiente, o entre el sueño profundo y la frecuencia cardiaca mínima.
•	Proponer posibles hábitos o conductas asociados a una mejora en la calidad del descanso.
•	Demostrar la utilidad de los dispositivos de monitorización personal para generar conocimiento individual y facilitar decisiones en torno a la salud y el bienestar.
