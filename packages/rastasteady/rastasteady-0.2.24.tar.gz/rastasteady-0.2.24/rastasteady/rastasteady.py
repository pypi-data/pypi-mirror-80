#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import math
import subprocess
import os
import pathlib
import shlex
from subprocess import check_output

class RastaSteady:
   # ffmpeg commands
   ffmpegcommands = {
      'ffprobe': 'ffprobe -v error -select_streams v:0 -show_entries stream=width,height,codec_name,bit_rate -of csv=p=0 %s',
      'dual': 'ffmpeg -y -i %s -i %s -filter_complex hstack %s',
      'vidstabdetect': 'ffmpeg -y -i %s -vf vidstabdetect=shakiness=10:accuracy=15:result=\'%s\' -f null -',
      'vidstabtransform': 'ffmpeg -y -i %s -vf vidstabtransform=input=\'%s\':%s -c:v %s -b:v %s -c:a aac %s',
      'rastaview': 'ffmpeg -y -i %s -i %s -i %s -filter_complex remap,format=yuv420p -c:v %s -b:v %s -c:a aac -tune film %s'
   }

   # stabilization profiles
   stabprofiles = {
      'low': 'zoom=0:optzoom=1:interpol=linear:smoothing=5',
      'medium': 'zoom=0:optzoom=1:interpol=bilinear:smoothing=10,unsharp=5:5:0.8:3:3:0.4',
      'high': 'zoom=5:optzoom=1:interpol=bicubic:smoothing=30,unsharp=5:5:0.8:3:3:0.4',
      'ultra': 'zoom=10:optzoom=1:interpol=bicubic:smoothing=50,unsharp=5:5:0.8:3:3:0.4'
   }

   # constructor
   def __init__(self, inputpathlib = '', tmppathlib = '', verbose = 1):
      # read input file, temporary location
      self.inputpathlib = inputpathlib
      self.inputfile = str(self.inputpathlib)
      self.tmppathlib = tmppathlib

      # verbose controls the output in the console
      #   - 0 means no output at all
      #   - 1 means only frames process in console
      #   - 2 means full output in console
      self.verbose = verbose

      # check for input file and exit if it doesn't exists
      if not self.inputpathlib.is_file():
         raise FileNotFoundError('Error: Input file not found. Exiting.')

      # get video information
      self.codec, self.width, self.height, self.bitrate = self.getvideoinfo()
      self.width = int(self.width)
      self.height = int(self.height)

      # create temporary directory and fail otherwise
      try:
         self.tmppathlib.parent.mkdir()
      except FileExistsError:
         pass
      except:
         raise SystemExit('Error: Error creating temporary directory. Exiting.')

   # calculate a file path based on the temporary directory
   def tmpfile(self, filename):
      return str(self.tmppathlib.with_name(filename))

   # check if a file exists in the temporary directory
   def tmpfileexists(self, filename):
      return self.tmppathlib.with_name(filename).is_file()

   # runs a command saving the output in a file and showing some text in the console
   def runcommand(self, command, logfile):
      # print the command prior to executing it if verbose
      if self.verbose > 1:
         print("** %s" % command)

      # create a logfile for the execution with the full output
      log = open(self.tmpfile(logfile), 'w')
      log.write(command)

      # run the process
      # TODO: review if this can be done in a better way
      if self.verbose == 0:
         # self.verbose == 0 is faster as we need to show nothing in console
         process = subprocess.call(shlex.split(command, posix=False), stdout=log, stderr=subprocess.STDOUT)
      else:
         # for verbose mode we need to check every single line to show it in the console
         process = subprocess.Popen(shlex.split(command, posix=False), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines = True)
         while True:
            output = process.stdout.readline()
            # are we done?
            if output == '' and process.poll() is not None:
                break
            if output:
                # write the full line in the log file
                log.write(output)
                # if the line starts with 'frame' and it's not silent mode, print it
                if self.verbose == 2:
                    print('  ' + output.strip(), flush = True)
                elif self.verbose == 1 and output.startswith('frame'):
                    print('  ' + output.strip(), end = '\r', flush = True)

      if self.verbose > 0: print()
      log.close()

      return

   # gets video info (resolution, codec and bitrate)
   def getvideoinfo(self):
      command = self.ffmpegcommands['ffprobe'] % self.inputfile
      out = subprocess.Popen(command.split(), stdout = subprocess.PIPE)
      stdout, stderr = out.communicate()
      return stdout.decode('utf-8').split(',')

   # creates a dual video side by side
   def dual(self):
      # do nothing if the file already exists
      if not self.tmpfileexists('dual.mp4'):
         # try to find a suitable video in the temporary directory
         if self.tmpfileexists('rastaview.mp4'):
            video = 'rastaview.mp4'
         elif self.tmpfileexists('stabilized.mp4'):
            video = 'stabilized.mp4'
         else:
            # fail otherwise
            raise FileNotFoundError('Error: Missing required files to create dual video. Exiting.')

         self.runcommand(self.ffmpegcommands['dual'] % (
                     self.inputfile,
                     self.tmpfile(video),
                     self.tmpfile('dual.mp4')), 'dual.log')

   # creates the stabilized video based on a selected profile
   def stabilize(self, profile = 'high'):
      # https://trac.ffmpeg.org/ticket/2166
      transforms = self.tmpfile('transforms.trf')
      if os.name == 'nt':
         transforms = transforms.replace("\\", "/").replace(":", "\:")

      # do nothing if the file already exists
      if not self.tmpfileexists('transforms.trf'):
         self.runcommand(self.ffmpegcommands['vidstabdetect'] % (
                     self.inputfile,
                     transforms), 'transforms.log')

      # do nothing if the file already exists
      if not self.tmpfileexists('stabilized.mp4'):
         self.runcommand(self.ffmpegcommands['vidstabtransform'] % (
                     self.inputfile,
                     transforms,
                     self.stabprofiles[profile],
                     self.codec,
                     self.bitrate,
                     self.tmpfile('stabilized.mp4')), 'stabilized.log')

   # TODO: ask PaketeFPV about this one and embedd it into rastaview()
   def derp_it(self, tx, target_width, src_width):
      x = (float(tx) / target_width - 0.5) * 2
      sx = tx - (target_width - src_width) / 2
      offset = math.pow(x, 2) * (-1 if x < 0 else 1) * ((target_width - src_width) / 2)
      return sx - offset

   # applies rastaview effect to a previously stabilized file
   def rastaview(self, percentage = 20):
      # do nothing if the percentage value is zero
      if percentage == 0:
         return

      # calculate target width based on the percentaje
      target_width = int(self.width + (self.width/100*int(percentage)))

      # create xmap/ymap file for transformation
      # do nothing if the files already exists
      if not self.tmpfileexists('xmap.pgm') or not self.tmpfileexists('ymap.pgm'):
         xmap = open(self.tmpfile('xmap.pgm'), 'w')
         ymap = open(self.tmpfile('ymap.pgm'), 'w')

         xmap.write('P2 {0} {1} 65535\n'.format(target_width, self.height))
         ymap.write('P2 {0} {1} 65535\n'.format(target_width, self.height))

         for y in range(self.height):
            for x in range(target_width):
               fudgeit = self.derp_it(x, target_width, self.width)
               xmap.write('{0} '.format(int(fudgeit)))
               ymap.write('{0} '.format(y))
            xmap.write('\n')
            ymap.write('\n')

         xmap.close()
         ymap.close()

      # do nothing if the file already exists
      if not self.tmpfileexists('rastaview.mp4'):
         # check for stabilized file and exit if it doesn't exist
         if not self.tmpfileexists('stabilized.mp4'):
            raise FileNotFoundError('Error: Missing stabilized file required to create rastaview video. Exiting.')

         # check for transformation files and exit if they don't exist
         if not self.tmpfileexists('xmap.pgm') or not self.tmpfileexists('ymap.pgm'):
            raise FileNotFoundError('Error: Missing transformation map file(s) required to create rastaview video. Exiting.')

         self.runcommand(self.ffmpegcommands['rastaview'] % (
                     self.tmpfile('stabilized.mp4'),
                     self.tmpfile('xmap.pgm'),
                     self.tmpfile('ymap.pgm'),
                     self.codec,
                     self.bitrate,
                     self.tmpfile('rastaview.mp4')), 'rastaview.log')
