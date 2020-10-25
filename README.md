# C�digo Fuente de "Descubriendo la Inteligencia Artificial"

Este es el c�digo fuente de los algoritmos explicados en el canal de Youtube
["Descubriendo la Inteligencia Artficial"][dia].

La mayor�a del c�digo se ha realizadon con el lenguaje de programaci�n Python,
m�s concretamente con la versi�n 3 de dicho lenguaje.

Los archivos que terminan con "_simple" son los que se han mostrado en los
v�deos del canal. Estos se diferencia de los que no llevan esa terminaci�n
en que no incluyen comentarios, no muestran log y su c�digo es menos seguro.

## Novedades

Poco a poco se ir�n subiendo nuevos algoritmos y c�digos de ejemplo.

De momento, s�lo hay algunos algoritmos:
* **Enfoque B�squedas**: s�lo b�squedas no informadas e informadas en grafos.
* **Enfoque Probabilidad**: reglas b�sicas de probabilidad.
* **Enfoque L�gica**: s�lo la l�gica de proposiciones con tablas de verdad.

Pero, en breve, se ir�n subiendo m�s en cada uno de los enfoques.

## Descripci�n de las Subcarpetas

* **agentes.py** Ejemplos de agentes tabla y reactivos (los m�s sencillos).
* **busqueda/** Incluye los algoritmos del enfoque de b�squeda en grafos.
  * **grafos.py** Definici�n de un problema para b�squeda en grafos.
  * **informada.py** Algoritmos de b�squeda informada en grafos.
  * **noinformada.py** Algoritmos de b�squeda no informada en grafos.
* **logica/** Incluye los algoritmos del enfoque l�gico-simb�lico.
  * **proposiciones/** L�gica de Proposiciones:
    * **motor.py** Clases para trabajar con la l�gica desde python.
    * **inferencia.py** Funciones para realizar inferencias con la l�gica.
* **redesbayesianas/** Incluye los algoritmos del enfoque probabil�stico.
  * **probabilidad.py** Reglas b�sicas de la probabilidad.
  * **inferencia.py** Funciones para realizar inferencias con la probabilidad.

[dia]: https://www.youtube.com/c/descubriendolainteligenciaartificial
       "Canal de Youtube Descubriendo la Inteligencia Artficial"
