#!/usr/bin/env python
# -*- coding: utf-8 -*-
import click
import os
import pathlib
from rastasteady.rastasteady import RastaSteady

@click.command(no_args_is_help=True, context_settings=dict(max_content_width=120))

@click.argument('video', type=str, required=True)

@click.option('--debug', type=bool, is_flag=True, default=False, help='Muestra informacion durante los procesos del video.', show_default=True)
@click.option('--dual', type=bool, is_flag=True, default=False, help='Crea fichero dual con video original y procesado. Requiere efecto RastaView.', show_default=True)
@click.option('--no-rastaview', type=bool, is_flag=True, default=False, help='No crea efecto RastaView del video. Require estabilizar video.', show_default=True)
@click.option('--no-reusar', type=bool, is_flag=True, default=False, help='Borra ficheros temporales si existen.', show_default=True)
@click.option('--perfil', type=click.Choice(['fast', 'default', 'slow'], case_sensitive=False), default='default', help='Perfil de estabilizado: rapido (peor estabilización), normal, lento (mejor estabilización).', show_default=True)
@click.option('--recortar', type=bool, is_flag=True, default=False, help='Recorta el fichero final para eliminar distorsion. Requiere efecto RastaView.', show_default=True)

@click.version_option('0.2.13')

def cli(video, debug, dual, no_rastaview, no_reusar, perfil, recortar):
    """RastaSteady es un software de estabilizacion de video para el sistema DJI FPV digital."""
    click.echo('Procesando %s!' % video)

    inputpathlib = pathlib.Path(video)
    currpathlib = pathlib.Path(str(inputpathlib.cwd()) + '/.placeholder')
    tmppathlib = pathlib.Path(str(inputpathlib.cwd()) + '/.rastasteady-' + inputpathlib.name + '/.placeholder')

    if no_reusar:
        for file in ['transforms.trf', 'xmap.pgm', 'ymap.pgm', 'cropped.mp4', 'dual.mp4', 'rastaview.mp4', 'stabilized.mp4']:
            if tmppathlib.with_name(file).is_file():
                tmppathlib.with_name(file).unlink()

    myVideo = RastaSteady(video, debug=debug)
    myVideo.stabilize(perfil)
    if not no_rastaview:
        myVideo.rastaview()
    if dual:
        myVideo.dual()
    if recortar:
        myVideo.crop()

    for file in ['cropped.mp4', 'dual.mp4', 'rastaview.mp4', 'stabilized.mp4']:
        if tmppathlib.with_name(file).is_file():
            if currpathlib.with_name(inputpathlib.stem + '-' + file).is_file():
                currpathlib.with_name(inputpathlib.stem + '-' + file).unlink()
            os.rename(tmppathlib.with_name(file), currpathlib.with_name(inputpathlib.stem + '-' + file))
