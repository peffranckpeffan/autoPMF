import configparser

config = configparser.ConfigParser(inline_comment_prefixes=';')
config.read('lib/base-files/input.in')

#stand_files=config['standard.files']
#init_config=config['initial.configuration']


#min_size_water_box = init_config['minimum size water box'].split(',')

#print(" ".join(min_size_water_box))

print(config.sections())

