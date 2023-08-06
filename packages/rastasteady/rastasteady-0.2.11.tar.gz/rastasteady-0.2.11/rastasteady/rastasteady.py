import sys
import math
import subprocess
import os
import pathlib
import time
from subprocess import check_output

class RastaSteady:
   def __init__(self, filename = '', debug = False):
      self.debug = debug
      self.pathlib = pathlib.Path(filename)
      self.tmppathlib = pathlib.Path(str(self.pathlib.cwd()) + '/.rastasteady-' + self.pathlib.name + '/.placeholder')

      self.inputfile = str(self.pathlib)

      try:
          self.tmppathlib.parent.mkdir()
      except FileExistsError:
          pass
      except:
          print('Error: error creating temporary directory')
          exit()

      self.getresolution()

   def tmpfile(self, filename):
      return str(self.tmppathlib.with_name(filename))

   def tmpfileexists(self, filename):
      return self.tmppathlib.with_name(filename).is_file()

   def debugopts(self):
      if self.debug == False: return '-hide_banner -loglevel warning -stats'
      return ''

   def derp_it(self, tx, target_width, src_width):
      x = (float(tx) / target_width - 0.5) * 2
      sx = tx - (target_width - src_width) / 2
      offset = math.pow(x, 2) * (-1 if x < 0 else 1) * ((target_width - src_width) / 2)
      return sx - offset

   def getresolution(self):
      out = subprocess.Popen(['ffprobe', '-v', 'error','-show_entries','stream=width,height','-of','csv=p=0:s=x', self.inputfile],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT) ## if STDERROR !!!
      stdout, stderr = out.communicate()
      cleanmsg = stdout.decode('utf-8')
      print(cleanmsg)
      listamedida = cleanmsg.split('x')
      self.src_width = int(listamedida[0].strip('\n'))
      height = listamedida[1].strip('\n')
      self.height = int(height)

   def dual(self):
      if not self.tmpfileexists('dual.mp4'):
          if self.tmpfileexists('rastaview.mp4'):
              video = 'rastaview.mp4'
          elif self.tmpfileexists('stabilized.mp4'):
              video = 'stabilized.mp4'
          command = 'ffmpeg ' + self.debugopts() + ' -y -i ' + self.inputfile + ' -i ' + self.tmpfile(video) + ' -filter_complex hstack ' + self.tmpfile('dual.mp4')
          os.system(command)

   def stabilize(self, profile='default'):
      options = {
          'fast': ':zoom=0:optzoom=1:interpol=linear:smoothing=5',
          'default': ':zoom=0:optzoom=1:interpol=bilinear:smoothing=10,unsharp=5:5:0.8:3:3:0.4',
          'slow': ':zoom=1:optzoom=1:interpol=bicubic:smoothing=30,unsharp=5:5:0.8:3:3:0.4'
      }

      # https://trac.ffmpeg.org/ticket/2166
      transforms = self.tmpfile('transforms.trf')
      if os.name == 'nt':
         transforms = "'" + transforms.replace("\\", "/").replace(":", "\\:") + "'"

      if not self.tmpfileexists('transforms.trf'):
          command1 = 'ffmpeg ' + self.debugopts() + ' -y -i ' + self.inputfile + ' -vf vidstabdetect=shakiness=10:accuracy=15:result=' + transforms + ' -f null -'
          os.system(command1)
      if not self.tmpfileexists('stabilized.mp4'):
          command2 = 'ffmpeg ' + self.debugopts() + ' -y -i ' + self.inputfile + ' -vf vidstabtransform=input="' + transforms + options[profile] + '" -acodec copy -vcodec libx264 -level 50 ' + self.tmpfile('stabilized.mp4')
          os.system(command2)

   def crop(self):
      command = 'ffmpeg ' + self.debugopts() + ' -y -i ' + self.tmpfile('rastaview.mp4') + ' -vf "crop=in_w-80:in_h-60" '+ self.tmpfile('cropped.mp4')
      os.system(command)

   def rastaview(self, percentage = 20):
      if percentage == 0:
         return
      target_width = self.src_width + (self.src_width/100*int(percentage))
      target_width = int(target_width)

      xmap = open(self.tmpfile('xmap.pgm'), 'w')
      xmap.write('P2 {0} {1} 65535\n'.format(target_width, self.height))
      for y in range(self.height):
         for x in range(target_width):
            fudgeit = self.derp_it(x, target_width, self.src_width)
            xmap.write('{0} '.format(int(fudgeit)))
         xmap.write('\n')
      xmap.close()

      ymap = open(self.tmpfile('ymap.pgm'), 'w')
      ymap.write('P2 {0} {1} 65535\n'.format(target_width, self.height))
      for y in range(self.height):
         for x in range(target_width):
            ymap.write('{0} '.format(y))
         ymap.write('\n')
      ymap.close()

      if not self.tmpfileexists('rastaview.mp4'):
          command = 'ffmpeg ' + self.debugopts() + ' -y -i ' + self.tmpfile('stabilized.mp4') + ' -i ' + self.tmpfile('xmap.pgm') + ' -i ' + self.tmpfile('ymap.pgm') + ' -filter_complex remap,format=yuv420p -vcodec libx264 -level 50 ' + self.tmpfile('rastaview.mp4')
          os.system(command)
