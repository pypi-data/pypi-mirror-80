import sys
import math
import subprocess
import os
import pathlib
from subprocess import check_output

class RastaSteady:
   # ffmpeg commands
   ffmpegcommands = {
      'ffprobe': 'ffprobe -v error -show_entries stream=width,height -of csv=p=0:s=x %s',
      'dual': 'ffmpeg %s -y -i %s -i %s -filter_complex hstack %s',
      'vidstabdetect': 'ffmpeg %s -y -i %s -vf vidstabdetect=shakiness=10:accuracy=15:result=%s -f null -',
      'vidstabtransform': 'ffmpeg %s -y -i %s -vf vidstabtransform=input=%s:%s -acodec copy -vcodec libx264 -preset slow -tune film -level 50 %s',
      'rastaview': 'ffmpeg %s -y -i %s -i %s -i %s -filter_complex remap,format=yuv420p -vcodec libx264 -preset slow -tune film -level 50 %s'
   }

   # stabilization profiles
   stabprofiles = {
      'low': 'zoom=0:optzoom=1:interpol=linear:smoothing=5',
      'medium': 'zoom=0:optzoom=1:interpol=bilinear:smoothing=10,unsharp=5:5:0.8:3:3:0.4',
      'high': 'zoom=5:optzoom=1:interpol=bicubic:smoothing=30,unsharp=5:5:0.8:3:3:0.4',
      'ultra': 'zoom=10:optzoom=1:interpol=bicubic:smoothing=50,unsharp=5:5:0.8:3:3:0.4'
   }


   def __init__(self, inputpathlib = '', tmppathlib = '', debug = False):
      # read input file, temporary location and debug mode
      self.inputpathlib = inputpathlib
      self.inputfile = str(self.inputpathlib)
      self.tmppathlib = tmppathlib      
      self.debug = debug

      # check for input file and exit if it doesn't exists
      if not self.inputpathlib.is_file():
         raise FileNotFoundError('Error: Input file not found. Exiting.')

      # create temporary directory and fail otherwise
      try:
         self.tmppathlib.parent.mkdir()
      except FileExistsError:
         pass
      except:
         raise SystemExit('Error: Error creating temporary directory. Exiting.')

      # calculate input resolution
      self.getresolution()

   # calculate a file path based on the temporary directory
   def tmpfile(self, filename):
      return str(self.tmppathlib.with_name(filename))

   # check if a file exists in the temporary directory
   def tmpfileexists(self, filename):
      return self.tmppathlib.with_name(filename).is_file()

   # return a string to include debug options for ffmpeg
   def debugopts(self):
      if self.debug == False: return '-hide_banner -loglevel warning -stats'
      return ''

   # runs a command
   def runcommand(self, command):
      if self.debug:
         print(command)
      os.system(command)

   # TODO: ask PaketeFPV about this one
   def derp_it(self, tx, target_width, src_width):
      x = (float(tx) / target_width - 0.5) * 2
      sx = tx - (target_width - src_width) / 2
      offset = math.pow(x, 2) * (-1 if x < 0 else 1) * ((target_width - src_width) / 2)
      return sx - offset

   # gets the resolution of the video based on ffprobe output
   # TODO: reduce it if possible
   def getresolution(self):
      command = self.ffmpegcommands['ffprobe'] % self.inputfile
      out = subprocess.Popen(command.split(),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT) ## if STDERROR !!!
      stdout, stderr = out.communicate()
      cleanmsg = stdout.decode('utf-8')
      listamedida = cleanmsg.split('x')
      self.src_width = int(listamedida[0].strip('\n'))
      height = listamedida[1].strip('\n')
      self.height = int(height)

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
                     self.debugopts(),
                     self.inputfile,
                     self.tmpfile(video),
                     self.tmpfile('dual.mp4')))

   # creates the stabilized video based on a selected profile
   def stabilize(self, profile='high'):
      # https://trac.ffmpeg.org/ticket/2166
      transforms = self.tmpfile('transforms.trf')
      if os.name == 'nt':
         transforms = "'" + transforms.replace("\\", "/").replace(":", "\\:") + "'"

      # do nothing if the file already exists
      if not self.tmpfileexists('transforms.trf'):
         self.runcommand(self.ffmpegcommands['vidstabdetect'] % (
                     self.debugopts(),
                     self.inputfile,
                     transforms))

      # do nothing if the file already exists
      if not self.tmpfileexists('stabilized.mp4'):
         self.runcommand(self.ffmpegcommands['vidstabtransform'] % (
                     self.debugopts(),
                     self.inputfile,
                     transforms,
                     self.stabprofiles[profile],
                     self.tmpfile('stabilized.mp4')))

   # applies rastaview effect to a previously stabilized file
   def rastaview(self, percentage = 20):
      # do nothing if the percentage value is zero
      if percentage == 0:
         return

      # calculate target width based on the percentaje
      target_width = self.src_width + (self.src_width/100*int(percentage))
      target_width = int(target_width)

      # create xmap file for transformation
      xmap = open(self.tmpfile('xmap.pgm'), 'w')
      xmap.write('P2 {0} {1} 65535\n'.format(target_width, self.height))
      for y in range(self.height):
         for x in range(target_width):
            fudgeit = self.derp_it(x, target_width, self.src_width)
            xmap.write('{0} '.format(int(fudgeit)))
         xmap.write('\n')
      xmap.close()

      # create ymap file for transformation
      ymap = open(self.tmpfile('ymap.pgm'), 'w')
      ymap.write('P2 {0} {1} 65535\n'.format(target_width, self.height))
      for y in range(self.height):
         for x in range(target_width):
            ymap.write('{0} '.format(y))
         ymap.write('\n')
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
                     self.debugopts(),
                     self.tmpfile('stabilized.mp4'),
                     self.tmpfile('xmap.pgm'),
                     self.tmpfile('ymap.pgm'),
                     self.tmpfile('rastaview.mp4')))
