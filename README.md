# Validacion de mensajes ADS-B (**Prueba de concepto**)
Implementacion de un metodo de validacion de mensajes ADS-B que permite determinar si una fuente especifica (transponder) es confiable.<br>
El metodo propuesto utiliza el metodo _**CHACHA20**_ para cifrar los datos y _**CRC32**_ para generar una huella unica.<br>
Los datos originales igual se pueden usar. Si el TX o RX no implementan el nuevo metodo, no se ve afectado y se puede seguir usando el protocolo original.

## Formato de mensajes ADS-B

### Componentes del mensaje
El mensaje tiene una longitud total de 112 bits


|    Bit           | # bits    |  Abrev     |         Informacion                       |
|:----------------:|:---------:|:----------:|:-----------------------------------------:|
| 1-5              | 5         | DF         | Downlink Format                           |
| 6-8              | 3         | CA         | Transponder Capability                    |
| 9-32             | 24        | ICAO       | ICAO Aircraft Address                     |
| 33-88<br>(33-37) | 56<br>(5) | ME<br>(TC) | Message, extended squitter<br>(Type Code) |
| 89-112           | 24        | PI         | Parity/Interrogator ID                    |

## Descripcion del diseño
En esta seccion se detalla el principio de funcionamiento del sistema de validacion

### Transmisor
* La fuente de los datos crea bloques de 512 bits con 4 mensajes antes de enviarlos.
	* Como el mensaje de ADS-B es de 112 bits, a cada mensaje se le agregan 16 bits para completar 128.
* El bloque de 512 bits se cifra mediante _**CHACHA20**_
	* Para el cifrado utiliza una llave privada proporcionada por un ente confiable.
	* Las llaves podrian ser generadas por los responsables de cada espacio aereo.
	* Las aeronaves que entran a un espacio aereo determinado deben solicitar la llave privada por un canal seguro para ese espacio, si quieren utilizar el sistema de validacion.
* Se genera una huella unica usando _**CRC32**_ a partir de los datos cifrados
* La huella unica se envia como el quinto mensaje en cola, justo despues de los cuatro mensajes usados para generarla

### Receptor
* El receptor guarda los mensajes recibidos en un buffer temporal.
* Cuando recibe un mensaje de identificacion, cifra los mensajes presentes en el bufer usando la misma llave privada que el transmisor.
* A partir del mensaje cifrado, calcula la huella unica usando _**CRC32**_
* Compara la huella calculada con la huella recibida en el mensaje de identificacion
	* Si las huellas son iguales, agrega el ID del transmisor a una lista de confianza
	* Si las huellas son diferentes, elimina el ID del transmisor de la lista de confianza
	
## Mensaje de identificacion
TBD

## Notas
1. Un receptor tipico puede ver hasta 100 aviones simultaneamente en zonas de<br>
alto trafico.
2. El metodo CHACHA20 se aplica a bloques de 512 bits.
3. La validacion se realiza para cada fuente de datos.
	1. Esto implica que se debe contar con al menos 100*512 ~ 50kB para los<br>
	bufer de almacenamiento temporal para CHACHA20
4. La solucion propuesta implica ajustes al estandar del ADS-B para el transmisor
5. En el receptor la aplicacion funciona de manera paralela e independiente, por<br>
lo que la validacion es transparante para el sistema original.

## Limitaciones
TBD

## Posibles mejoras
TBD
