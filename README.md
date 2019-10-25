# Tinanic Espacial
Esta práctica consiste en simular el trayecto de un cohete hacia el espacio y orbitar la tierra.

Para correr el programa se necesitan tener dos cosas en cuenta: 

1. Los parámetros
2. Los "skips" (los datos que se toman en cuenta para la trayectoria del plot)



1.1 Una sola mision
Se puede correr con un barrido editando el códibo fuente llamando a la función test_rocket. Como parámetros se tiene que especificar a qué grados con respecto a la superficie se desea lanzar el cohete y con qué velocidad en metros por segundo. El programa debería hacer los cálculos de la trayectoria y mostrar el plot en poco tiempo.

1.2 Barrido de misiones: se edita al final del código.
Para hacer el barrido tenemos varias opciones. Es mucho más fácil de explicar si se mira el código, entonces la explicación de como controlarlo está en el código.


2.1 Los skips están en la función de test_rocket y se editan si se quiere lidiar con menos datos. Si el plot resulta innavegable, recomendamos reducir la cantidad de puntos.
ADVERTENCIA: reducir la cantidad de puntos demasiado puede causar errores en el reporte de éxito o choque de misiones.

Para encontrar la variable de skip recomendamos usar CTRL+F "if skip ==" y editar al número de datos que se salta el modelo antes de guardar uno.

Si se quiere correr la simulación por más tiempo se debe cambiar lenTime. Recomendamos cambiar el último valor de la multiplicación únicamente.

MUCHA SUERTE, ASTRONAUTA!


