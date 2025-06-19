# ipa-adsb
Implementacion de un metodo de verificacion de confiabilidad de mensajes ADS-B

Formato del mensaje
+--------+--------+---------------+------------------------------+-------------+
| DF (5) | CA (3) |   ICAO (24)   | TC (5)         ME (51)       |   PI (24)   |
+--------+--------+---------------+------------------------------+-------------+

+-----------+--------+-------+-----------------------------+
|    Bit    | # bits |  Abr  |         Informacion         |
+-----------+--------+-------+-----------------------------+
| 1-5       | 5      | DF    | Downlink Format             |
| 6-8       | 3      | CA    | Transponder Capability      |
| 9-32      | 24     | ICAO  | ICAO Aircraft Address       |
| 33-88     | 26     | ME    | Message, extended squitter  |
|  (33-37)  | (5)    | (TC)  | (Type Code)                 |
| 89-112    | 24     | PI    | Parity/Interrogator ID      |
+-----------+--------+-------+-----------------------------+

Descripcion del diseño
	El metodo es simplemente una aplicacion que determina si los datos recibidos
	son confiables.
	Los datos originales igual se pueden usar. Si el TX o RX no implementan el
	nuevo metodo, no se ve afectado y se puede seguir usando el protocolo
	original.
	La fuente de los datos (el transponder) genera un hash a partir de mensajes
	enviados.
	El hash se encripta usando una llave privada.
		La llave la genera una entidad confiable.
		Solo los Transmisores y Receptores registrados tendrian acceso a las
		llaves
	El hash encriptado debe ser de 51 bits. Se envia como un mensaje ADS-B, en
	el campo ME (bits 38 a 88).
	Cada X cantidad de mensajes "normales" se envia un mensaje de identificacion
	El receptor guarda los mensajes recibidos en un buffer temporal.
	Cuando recibe un mensaje de identificacion, calcula el hash con los mensajes
	presentes en el bufer.
	Ademas, desencripta el hash recibido en el mensaje de identificacion.
	Si los valores de hash son iguales, guarda el ID del transmisor en una lista
	de fuentes confiables. Caso contrario, guarda el ID en una lista de fuentes
	no confiables.
	Estas banderas pueden ser usadas por la aeronave receptora para tomar
	decisiones respecto al uso de los datos a partir de fuentes no confiables.
