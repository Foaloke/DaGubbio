'''
Created on 18 Aug 2017

@author: mtonnicchi
'''

import dagubbio.writer.distortions as d
import urllib
import os
import random
import utils.sourceutils as su
from PIL import ImageOps
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

class Writer(object):

    def __init__(self, fonts, white_space_spacing, padding_top, spacing_correction, warp_amplitude, warp_period, font_output_folder, text_output_folder):
        self.fonts = fonts
        self.white_space_spacing = white_space_spacing
        self.padding_top = padding_top
        self.spacing_correction = spacing_correction
        self.warp_amplitude = warp_amplitude
        self.warp_period = warp_period
        su.prepare_directory(font_output_folder)
        self.font_output_folder = font_output_folder
        self.text_output_folder = text_output_folder
    
    def write_from_file(self, source_dir, source_path):
        su.prepare_directory(self.text_output_folder)
        self.create_text_strip(source_path, su.load_source(source_dir, source_path))
    
    def create_text_strip(self, title, text):
        
        char_and_font_sequence = self.create_font_sequence(text)
        total_length = reduce((lambda x, y : x + y), [ c_f[1].size for c_f in char_and_font_sequence])
        if total_length >= 65535:
            first_half_end = int(len(text)/2)+(len(text)%2)
            second_half_start = len(text)-first_half_end+(len(text)%2)
            self.create_text_strip(title+"0", text[:first_half_end])
            self.create_text_strip(title+"1", text[second_half_start:])
        else:         
            max_height = max([ c_f[1].size*2 for c_f in char_and_font_sequence])
            canvas = Image.new("RGB", (total_length,max_height),(255,255,255))
            draw = ImageDraw.Draw(canvas)
            # Convenience line for setting alignment configuration
            #draw.line((0,60, total_length,60), fill=128, width=3)
    
            output_path = os.path.join(self.text_output_folder,title)
            x_offset = 0
            for c_f in self.create_font_sequence(text):
                if c_f[0] == ' ':
                    x_offset += int((self.white_space_spacing*0.5)+self.white_space_spacing*(random.randrange(25, 75, 1)*0.01))
                else:
                    font = ImageFont.truetype(c_f[1].path,c_f[1].size)
                    draw.text((x_offset,self.padding_top+c_f[1].offset),c_f[0],(0,0,0),font=font)
                    next_offset = ImageOps.invert(canvas).getbbox()[2]
                    x_offset = next_offset - 3
            
            print("INFO: Writing {} to {}".format((text[:25] + '..') if len(text) > 75 else text, output_path))
            distorted = d.SineWarp(self.warp_amplitude, self.warp_period).render(canvas)
            bbox = ImageOps.invert(distorted).getbbox()
            file_name = output_path+'.png'
            img = distorted.crop(bbox)
            img.save(file_name)
            return file_name
    
    def create_font_sequence(self, text):
        font_sequence = []
        for char in text:
            font_sequence.append((char,self.fonts[random.choice(self.fonts.keys())]))
        return font_sequence
        
    def generate_char_name(self, char, font_name, font_size):
        return urllib.quote_plus(char)+"_"+font_name+"_"+str(font_size)+".jpeg"
        
        