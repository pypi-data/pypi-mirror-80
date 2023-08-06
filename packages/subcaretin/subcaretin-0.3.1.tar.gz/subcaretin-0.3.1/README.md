# subcaretin

`subcaretin` ofrece la forma más efectiva y rápida de descargar automáticamente subtítulos en español.

## Características

`subcaretin` soporta búsquedas en Argenteam y Subdivx de películas y epsiodios. Tiene un modo automático y otro manual; cada modo opera así:

### Automático (por defecto)

* Incorpora el excelente reconocimiento de metadatos de vídeo por parte de [guessit](https://github.com/guessit-io/guessit)
* Utiliza un algoritmo simple para ordenar de mejor a peor los resultados de acuerdo a los datos obtenidos por guessit
* Descarga el mejor subtítulo disponible
* Renombra el subtítulo descargado de acuerdo al nombre del archivo de vídeo introducido

El cálculo de puntajes está inspirado en subliminal. En orden de importancia, cuenta los puntos de esta forma:

* Source (Bluray, DVD, WEB, etc): 7 puntos
* Codec de vídeo (x264, x265, etc): 3 puntos
* Codec de audio (aac, flac, etc): 3 puntos
* Resolución (480p, 720p, etc): 2 puntos
* Año: 2 puntos

### Manual

* El modo manual espera la interacción del usuario/usuaria en la búsqueda, la elección del subtítulo a descargar y la elección del archivo a extraer
 
## Instalar
```
pip3 install --upgrade subcaretin --user
```
O, para instalarlo manualmente:
```
git clone https://github.com/vitiko98/subcaretin.git
cd subcaretin
pip3 install -r requirements.txt
python3 setup.py install --user
```
Ahora, `subcaretin` está listo
> Nota: python-unrar requiere la librería de unrar instalada en tu sistema, por lo que puede que te salten errores a la hora de importarlo. Es recomendable que instales el paquete adecuado para tu distribución. Por ejemplo, `python3-unrar` en Debian y `python-unrar` en Arch Linux. Más información: [python-unrar](https://github.com/matiasb/python-unrar)
## Uso
```
Uso: subcaretin [-h] [-m] [-l int] [-p int] [-f] VIDEO

Argumento posicional obligatorio:
  VIDEO       el archivo de video de referencia

Argumentos opcionales:
  -h, --help  mostrar este mensaje cerrar
  -m          activar el modo manual (desactivado por defecto)
  -l int      el límite de resultados (ilimitado por defecto)
  -p int      puntaje mínimo para descargar subtítulos automáticamente (3 por defecto)
  -f          de existir, sobrescribir subtítulo descargado
```
## Ejemplo del modo automático
```console
[victor@arch]$ subcaretin True.Detective.S01E02.WEB-DL.x265.AAC.mkv
Buscando subtítulos para True.Detective.S01E02.WEB-DL.x265.AAC.mkv...

Score: 10

Bajando: True Detective S01E02 [subdivx.com]
sincronizados para la version true detective s01e02 seeing things 1080p amzn web-dl dd 5 1 h 265-sigma

Extracción exitosa: True.Detective.S01E02.WEB-DL.x265.AAC.es.srt
```
## Ejemplo del modo manual
```console
[victor@arch]$ subcaretin -m -l 7 Taxi.Driver.1976.Bluray.x264.mkv

Introduce el nombre que buscas:
- Taxi Driver 1976

Buscando subtítulos...
0: Taxi Driver (1976) - Taxi.Driver.%281976%29.DVDRip.DivX-NoGRP
1: Taxi Driver (1976) - Taxi.Driver.%281976%29.DVDRip.XviD.AC3-Taitongtan
2: Taxi Driver (1976) - Taxi.Driver.%281976%29.BDRip.x264.720p.DTS-AMIABLE
3: Taxi Driver (1976) - Taxi.Driver.%281976%29.BDRip.x264.1080p.DTS-AMIABLE
4: Taxi Driver (1976) - son para la nueva versión taxi driver 1976 1080p  x264-amiable  tome los que subió jfca283 (leanlestat) "taxi driver 1976 720p  dts x264 ebp" y los resincronicé  espero les sirva
5: Taxi Driver (1976) - sirve para taxi driver [bdrip-1080p-multilang-multisub-chapters][rip by max]
6: Taxi Driver (1976) - para la version de "zeus diaz" que ocupa 700 mb
(...)
Elige el número a descargar:
 - 2

Bajando: Taxi Driver (1976) [argenteam.net]
Taxi.Driver.%281976%29.BDRip.x264.720p.DTS-AMIABLE

Subtítulo descargado
0. Taxi.Driver.1976.720p.BluRay.X264-AMIABLE.srt
Elige el numero a descomprimir:
 - 0
Extracción exitosa: True.Detective.S01E02.WEB-DL.x265.AAC.es.srt
```
## API
Si por alguna razón necesitas subtítulos en español para tu programa, puedes utilizar `subcaretin` como módulo.

Por ejemplo, para conseguir el mejor subtítulo de acuerdo al primer argumento:
```python
>>> from subcaretin import mejor_sub
>>> mejor_sub.get('Taxi Driver (1976) Bluray x264.mkv', argenteam=True, subdivx=True, lista=False, array=0)
{'title': 'Taxi Driver (1976)', 'description': 'taxi.driver.%281976%29.bdrip.x264.720p.dts-amiable', 'url': 'http://www.argenteam.net/subtitles/31157/Taxi.Driver.%281976%29.BDRip.x264.720p.DTS-AMIABLE', 'provider': 'argenteam.net', 'score': 12}
```

De la misma forma, si estás buscando sin la necesidad de filtros:
```python
>>> from subcaretin import providers
>>> subs = providers.Subtitles('Corpus Christi')
>>> subs.get_subtitles(argenteam=False, subdivx=True, limit=2)
>>> subs.Subs
{'items': [{'title': 'Boze Cialo (2019) aka Corpus Christi', 'description': 'excelente pèlicula polaca  para \r\ncorpus christi 2019 1080p  x264-rovers[ethd], de 10,3 g', 'url': 'http://www.subdivx.com/X6XNTg2NDQ2X-boze-cialo-2019-aka-corpus-christi.html', 'provider': 'subdivx.com'}, {'title': 'Boze Cialo (2019) aka Corpus Christi', 'description': 'subtítulo sincronizado a la versión boze cialo [corpus christi] 2019 720p brrip x264-titler, de 1,22 gb', 'url': 'http://www.subdivx.com/X6XNTg2NTU3X-boze-cialo-2019-aka-corpus-christi.html', 'provider': 'subdivx.com'}]}
```
## Eficacia
`subcaretin` tiene una serie de filtros específicamente optimizados para las búsquedas en Argenteam y Subdivx, por lo que apunta a ser más eficaz que aplicaciones similares de subtítulos. De cualquier forma, mientras mejor estén nombrados tus archivos de vídeo, mejores resultados podrá ofrecer esta herramienta.
## TODO
* Mejorar los filtros
* Descargar por carpetas
* Mejorar el manejo de errores
* Agregar más proveedores (?)
## Miscelánea
* Para mejorar la compatibilidad, este script fue reescrito en Python a partir del 25 de Julio de 2020. Anteriormente fue un bash script. Puedes encontrar la versión obsoleta en las branches
* Mi subdivx: https://www.subdivx.com/X9X2117299
