# Analisis-de-titulares-fentanilo-2016-2024
Tendencias y patrones en la cobertura mediática del fentanilo en América del Norte y Colombia, 2016 - 2024

##        Contexto del análisis

Existe un boom de información relacionada al fentanilo desde el 2016 que va de la mano con muchas cosas tales como; la declaración del gobierno provincial de Columbia Británica – Canadá de una crisis de fentanilo en abril de ese año, visibilización de los consumidores mientras se encuentran bajo su efecto, sobredosis, aumento de la oferta y demanda en el mercado negro, combinaciones peligrosas con otras sustancias, noticias criminales entorno a la sustancia, supuestas aperturas de nuevos mercados, entre otras tantas que en ocasiones son verdad, pero que en otras ocasiones son solo noticias que busca avivar las pasiones de las personas para traer clicks y visitas.

El uso de fentanilo es un problema que ha afectado de forma real y en gran cantidad a muchas personas en México, EE.UU y Canadá. Fuera de estos territorios, específicamente desde Colombia, se ha venido gestando un ambiente mediático opaco, en donde se refuerza la narrativa prohibicionista y donde se pronostica que el fentanilo va a destruir a los colombianos sin pruebas claras o análisis a profundidad. Es una herramienta discursiva que emplea toda la agenda mediática como gran aliada para seguir fortaleciendo los enfoques punitivos sobre las sustancias ilegales y para aumentar la represión en los eslabones más débiles de esta cadena de distribución, esto disfrazado de “preocupación por la comunidad” y la necesidad de “más seguridad”.

Teniendo todo esto en cuenta se plantea la razón de la necesidad de realizar este análisis descriptivo y exploratorio desde Colombia. Pese a que no somos un país que se haya visto mayormente afectado por la problemática relacionada al consumo de fentanilo, se usa al aparato mediático como forma de avivar este mensaje de preocupación por la sustancia y las tragedias que nos puede traer, ignorando problemas estructurales mayores que ya tenemos como la polarización, estigmatización, exclusión e incluso odio en contra de los eslabones más débiles de la cadena distribución de las sustancias como consumidores y pequeñas y pequeños expendedores, estos últimos, en su mayoría comunidad pobre buscando otras alternativas económicas para sus vidas.

El contexto anterior ayudará a entender la razón por la cuál para este análisis se accedieron a medios de comunicación en México, Canadá, EE.UU y Colombia tanto en inglés, francés y español.

##       Objetivos del proyecto

Objetivo principal: Analizar el cubrimiento mediático relacionado al fentanilo entre los años 2016-2024.

Objetivos generales: Identificar tendencias y patrones significativos.

Analizar qué tipo de impacto pueden tener estas noticias en la percepción pública y el comportamiento de las personas que las consumen.

##        Mapear datos

Luego de una revisión general y teniendo en cuenta el espacio de tiempo de los datos necesarios para el análisis se decidió extraer la información de 2 herramientas. Primero, una especializada en análisis de medios, Media Cloud y su API oficial, y segundo, uno de los agregadores de noticias más usados, Google News usando la librería BeautifulSoup para rascar la información.

Se decide hacer uso de ambas herramientas ya que Media Cloud es una herramienta muy completa pero no cuenta con bases de datos de información de antes del año 2020. En este punto entró Google News como complemento para extraer la información del año 2016 al 2019.

Teniendo en cuenta los países más cercanos a la problemática del fentanilo (Canadá, EE.UU, México) y el país desde donde se hace este análisis (Colombia), se decide extraer la información para el análisis en francés, inglés y español.
 
       
##        Obtener y cargar los datos

### Extracción de la información:

Como ya se mencionó anteriormente, para obtener la información necesaria para el análisis se usó  Media Cloud, una herramienta especializada para análisis de medios e investigación relacionada y también uno de los agregadores de noticias más populares, Google News.

![MediaCloud Api](mediacloudapi1.png)

*MediaCloud Api*

![MediaCloud Api 2](mediacloudapi2.png)

*MediaCloud Api*

![Google News y BeautifulSoup Api](googlenewsbsp1.png)

*Google News y BeautifulSoup*

![Beautiful Soup](Beautifulsoup.png)

*BeautifulSoup*


### Limpieza de la información:

Pensando a otros análisis que se hagan a futuro en este punto se hace una primera limpieza de los datos revisando que todas las urls de donde se extrajeron las noticias sigan disponibles. Con esto se asegura de que más adelante, si se quiere obtener por ejemplo una captura de pantalla o información aparte de las columnas que están en el csv creado con los resultados, se podrá acceder a cualquier enlace porque todos deberían estar funcionando. Además de las url que no dieran respuesta, se limpiaron algunos registros que se salían de la estructura de las bases de datos por ejemplo, titulares que se cortaban en 2 o más partes y que se colaban en otras columnas, no fue un número significativo por lo que se eliminaron.

De aquí salieron 6 bases de datos; 3 con información extraída de Google News del año 2016 al año 2019 en inglés, francés y español; 3 con información extraída de Media Cloud del año 2020 al año 2024 en inglés, francés y español. Los resultados obtenidos desde ambas fuentes diferían en cuanto a los formatos de las fechas de publicación de las noticias, antes proceder a unir la información de Media Cloud y Google News, desde 2016 – 2019, agrupadas por idiomas, se solucionó este paso estableciendo un formato de fecha igual para toda la información (AAAA-MM-DD).


