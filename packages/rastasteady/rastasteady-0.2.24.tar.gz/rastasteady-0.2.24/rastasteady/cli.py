#!/usr/bin/env python
# -*- coding: utf-8 -*-
import click
import os
import pathlib
from rastasteady.rastasteady import RastaSteady

@click.command(no_args_is_help = True, context_settings = dict(max_content_width = 120))

# main argument: the video file
@click.argument('video', type = str, required = True)

# optional parameters
@click.option('--verbose', type = click.Choice(['0', '1', '2']), default = '1', help = 'Muestra informacion durante los procesos del video: 0 (no muestra nada), 1 (muestra informacion de progreso unicamente, 2 (muestra toda la informacion)', show_default = True)
@click.option('--dual', type = bool, is_flag = True, default = False, help = 'Crea fichero dual con video original y procesado. Requiere efecto RastaView.', show_default = True)
@click.option('--no-rastaview', type = bool, is_flag = True, default = False, help = 'No crea efecto RastaView del video. Require estabilizar video.', show_default = True)
@click.option('--no-reusar', type = bool, is_flag = True, default = False, help = 'Borra ficheros temporales si existen.', show_default = True)
@click.option('--perfil', type = click.Choice(['low', 'medium', 'high', 'ultra'], case_sensitive = False), default = 'high', help='Perfil de estabilizado: bajo (peor estabilización), medio, alto (mejor estabilización), ultra.', show_default = True)

# version
# TODO: this version string should be centralized in other place
@click.version_option('0.2.24')

# main code
def cli(video, verbose, dual, no_rastaview, no_reusar, perfil):
    """RastaSteady es un software de estabilizacion de video para el sistema DJI FPV digital."""
    # calculate input directory and temporary location
    inputpathlib = pathlib.Path(video)
    tmppathlib = pathlib.Path(str(os.getcwd()) + '/rastasteady-' + inputpathlib.stem + '/.placeholder')

    print('RastaSteady 0.2.24. Estabiliza y amplia el FOV del video de tu sistema DJI FPV.')
    print('\nProcesando video %s:' % inputpathlib.name)

    # if asked, delete any existing file in the temporary location
    if no_reusar:
        print('* Eliminando ficheros existentes...')
        for file in ['transforms.trf', 'xmap.pgm', 'ymap.pgm', 'cropped.mp4', 'dual.mp4', 'rastaview.mp4', 'stabilized.mp4']:
            if tmppathlib.with_name(file).is_file():
                tmppathlib.with_name(file).unlink()
                if int(verbose) > 0: print('** Fichero %s eliminado.' % file)

    # create the rastasteady object
    myVideo = RastaSteady(inputpathlib, tmppathlib, verbose=int(verbose))

    # stabilize the file and apply rastaview and/or dual if they apply
    print('* Generando video stabilized.mp4 usando el perfil de estabilizado \'%s\'...' % perfil)
    myVideo.stabilize(perfil)
    if not no_rastaview:
        print('* Generando video rastaview.mp4...')
        myVideo.rastaview()
    if dual:
        print('* Generando video dual.mp4...')
        myVideo.dual()

    # say goodbye
    print('\nProceso finalizado!\nLos ficheros generados se encuentran en el directorio %s.\n' % str(tmppathlib.parent.absolute()))

