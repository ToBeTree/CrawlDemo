from scrapy.cmdline import execute

name = 'douban_movie'
cmd = 'scrapy crawl {0}'.format(name)
execute(cmd.split())
