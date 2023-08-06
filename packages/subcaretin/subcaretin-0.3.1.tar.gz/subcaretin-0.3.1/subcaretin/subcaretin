#!/usr/bin/env python3

import magic
import os
import sys
import shutil
import requests
import tempfile
import argparse

from zipfile import ZipFile
from bs4 import BeautifulSoup as bso
from pathlib import Path

from subcaretin import providers
from subcaretin import filtros
from subcaretin import guess
from subcaretin import mejor_sub

def args():
    parser = argparse.ArgumentParser(prog='subcaretin', description='descarga \
                                     subtítulos de forma automática o manual desde \
                                     Subdivx y Argenteam')
    parser.add_argument("VIDEO",
                        help="el archivo de video de referencia")
    parser.add_argument("-m", action="store_true",
                        help="activar el modo manual (desactivado por defecto)")
    parser.add_argument("-l", metavar="int", type=int, default=30,
                        help="el límite de resultados (30 por defecto)")
    parser.add_argument("-p", metavar="int", type=int, default=3,
                        help="puntaje mínimo para descargar subtítulos \
                        automáticamente (3 por defecto)")
    parser.add_argument("-f", action="store_true",
                        help="de existir, sobrescribir subtítulo descargado\
                        (desactivado por defecto)")
    return parser.parse_args()


def manual(limite):
    query = input('Introduce el nombre que buscas\n - ')
    print('Buscando {}...\n'.format(query))
    busqueda = providers.Subtitles(query)
    busqueda.get_subtitles(argenteam=True, subdivx=True, limit=limite)

    if not busqueda.Subs['items']:
        sys.exit('Sin resultados')
    else:
        print('Resultados:\n')
        for i, n in zip(busqueda.Subs['items'], range(len(busqueda.Subs['items']))):
            print('{}. {}: {}'.format(n, i['title'], i['description']))
    try:
        elegido = int(input('\n\nElige el número a descargar:\n - '))
        return busqueda.Subs['items'][elegido]
    except ValueError:
        sys.exit('Inválido')

def descargar(conseguido, temp):
    def printSub():
        print('\nBajando: {} [{}]\n{}\n'.format(conseguido['title'],
                                                conseguido['provider'],
                                                conseguido['description']))
    try:
        if conseguido['provider'] == 'argenteam.net':
            printSub()
            comprimido = requests.get(conseguido['url'], allow_redirects=True)
            open(temp + '/subs', 'wb').write(comprimido.content)
        else:
            printSub()
            link = requests.get(conseguido['url'])
            sopa = bso(link.content, 'html.parser')
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
                "referer": 'https://subdivx.com'
            }
            descargar = 'http://www.subdivx.com/' + sopa.find('a', class_='link1')['href']
            comprimido = requests.get(descargar, headers=headers, allow_redirects=True)
            open(temp + '/subs', 'wb').write(comprimido.content)
        return True
    except requests.exceptions.Timeout:
        return
    except requests.exceptions.TooManyRedirects:
        return


def descomprimirTipo(extractor, auto, temp, dest):
    zipped = extractor(temp + '/subs')
    nombre = zipped.namelist()
    for i in nombre:
        if '.srt' not in i or '.en.srt' in i or '.eng.srt' in i:
            nombre.remove(i)
    if auto:
        eleccion = 0
    else:
        for n in range(len(nombre)):
            print('{}. {}'.format(n, nombre[n]))
        eleccion = int(input('Elige el numero a descomprimir:\n - '))

    try:
        source = temp + '/' + nombre[eleccion]
    except IndexError:
        sys.exit('Número inválido')
    zipped.extract(nombre[eleccion], temp + '/')
    shutil.move(source, dest)


def existe(dest):
    if os.stat(dest).st_size == 0:
        try:
            os.remove(dest)
        except OSError:
            pass
        return False
    else:
        return True


def descomprimir(dest, temp, auto=True):
    tipo = magic.from_file(temp + '/subs')

    if 'Zip' in tipo:
        descomprimirTipo(ZipFile, auto, temp, dest)
    else:
        try:
            from unrar import rarfile
        except ImportError:
            sys.exit('Instala python-unrar. También recuerda que necesitas'
                     'la librería de unrar instalada Es recomendable que '
                     'instales el paquete adecuado para tu distribución. Por'
                     'ejemplo, python3-unrar en Debian y python-unrar en Arch'
                     'Linux. Más información: https://github.com/matiasb/python-unrar')
        descomprimirTipo(rarfile.RarFile, auto, temp, dest)

    return existe(dest)


def main():
    arguments = args()
    # información del archivo
    movie_name = arguments.VIDEO
    to_srt = Path(movie_name).with_suffix('')
    destino = '{}.es.srt'.format(to_srt)

    if os.path.isfile('{}.es.srt'.format(to_srt)):
        if not arguments.f:
            sys.exit('Ya existe un subtítulo descargado')
    # directorio temporal de acuerdo al OS
    temp = tempfile.gettempdir()
    # modo manual
    if arguments.m:
        manual_mode = manual(arguments.l)

        if descargar(manual_mode, temp):
            print('Subtítulo descargado')
        else:
            sys.exit('Error al descargar. Prueba de nuevo')

        if descomprimir(destino, temp, False):
            print('Extracción exitosa: {}'.format(destino))
        else:
            print('Error. Prueba otro subtítulo')
    # modo automático
    else:
        print('Buscando subtítulos para {}...'.format(movie_name))
        count = 0
        while True:
            # pelicula, argenteam, subdivx, lista, array
            mejor = mejor_sub.get(movie_name, True, True, False, count)
            if not mejor:
                sys.exit('Sin resultados')
            print('Score: {}'.format(mejor['score']))
            if descargar(mejor, temp):
                if descomprimir(destino, temp, True):
                    print('Extracción exitosa: {}'.format(destino))
                    break
                else:
                    print('Extracción fallida. Probando el siguiente...')
                    count += 1
            else:
                count += 1

            if count > 5:
                print('Demasiados intentos. Terminando...')
                break


if __name__ == "__main__":
    sys.exit(main())
