'''
Created on 16 Aug 2017

@author: mtonnicchi
'''

import os
import utils.sourceutils as su
import utils.config as cfg
import dagubbio.acquirer.downloader_thelatinlibrary as latin_library
import dagubbio.acquirer.textcleaner as text_cleaner
import dagubbio.writer.writer as writer
import dagubbio.writer.font as font

if __name__ == '__main__':
    pass


cfg_latinlibrary = cfg.Config('config.ini').section('LATIN_LIBRARY')
# Download the latin library
# latin_library.Downloader_LatinLibrary(cfg_latinlibrary['url'], cfg_latinlibrary['storage_folder']).download()

cfg_textcleaning = cfg.Config('config.ini').section('TEXT_CLEANING')
# Clean text and Store
#cleaner = text_cleaner.TextCleaner(cfg_textcleaning['allowed_non_literal'])
#cleaner.clean_and_save_all_html_files(cfg_textcleaning['html_sources'], cfg_textcleaning['storage_folder'])

# Print text
cfg_writer = cfg.Config('config.ini').section('WRITER')
cfg_fonts = cfg.Config('config.ini').section('FONTS')

font_directory = cfg_writer['font_folder']
fonts = {}
for font_name,font_data in cfg_fonts.items():
    font_data_split = font_data.split(',')
    font_path = os.path.join(font_directory, font_name+'.'+font_data_split[0])
    fonts[font_name] = font.FontInfo(font_name, font_path, int(font_data_split[1]), int(font_data_split[2]))

wrt = writer.Writer(fonts, int(cfg_writer['white_space_spacing']),  int(cfg_writer['padding_top']),  int(cfg_writer['spacing_correction']),  cfg.tuple(cfg_writer['warp_amplitude']),  cfg.tuple(cfg_writer['warp_period']), cfg_writer['font_output_folder'], cfg_writer['text_output_folder'])
wrt.write_from_file('texts', 'http%3A%2F%2Fwww.thelatinlibrary.com%2F12tables.html.html')