#!/usr/bin/env python
# -*- coding: utf-8 -*-
import click
import os
import pathlib
from rastasteady.rastasteady import RastaSteady

@click.command(no_args_is_help=True, context_settings=dict(max_content_width=120))

# main argument: the video file
@click.argument('video', type=str, required=True)

# optional parameters
@click.option('--debug', type=bool, is_flag=True, default=False, help='Muestra informacion durante los procesos del video.', show_default=True)
@click.option('--dual', type=bool, is_flag=True, default=False, help='Crea fichero dual con video original y procesado. Requiere efecto RastaView.', show_default=True)
@click.option('--no-rastaview', type=bool, is_flag=True, default=False, help='No crea efecto RastaView del video. Require estabilizar video.', show_default=True)
@click.option('--no-reusar', type=bool, is_flag=True, default=False, help='Borra ficheros temporales si existen.', show_default=True)
@click.option('--perfil', type=click.Choice(['low', 'medium', 'high', 'ultra'], case_sensitive=False), default='high', help='Perfil de estabilizado: bajo (peor estabilización), medio, alto (mejor estabilización), ultra.', show_default=True)

# version
# TODO: this version string should be centralized in other place
@click.version_option('0.2.17')

# main code
def cli(video, debug, dual, no_rastaview, no_reusar, perfil):
    """RastaSteady es un software de estabilizacion de video para el sistema DJI FPV digital."""
    # calculate input directory and temporary location
    inputpathlib = pathlib.Path(video)
    tmppathlib = pathlib.Path(str(os.getcwd()) + '/rastasteady-' + inputpathlib.stem + '/.placeholder')

    # if asked, delete any existing file in the temporary location
    if no_reusar:
        for file in ['transforms.trf', 'xmap.pgm', 'ymap.pgm', 'cropped.mp4', 'dual.mp4', 'rastaview.mp4', 'stabilized.mp4']:
            if tmppathlib.with_name(file).is_file():
                tmppathlib.with_name(file).unlink()

    # create the rastasteady object
    myVideo = RastaSteady(inputpathlib, tmppathlib, debug=debug)

    # stabilize the file and apply rastaview and/or dual if they apply
    myVideo.stabilize(perfil)
    if not no_rastaview:
        myVideo.rastaview()
    if dual:
        myVideo.dual()
