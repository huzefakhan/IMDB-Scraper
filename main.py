import scrapy

class ScratchQuotes(scrapy.Spider):
    name = 'imdb'
    start_urls = ['https://www.imdb.com/chart/top/']


    def parse(self, response):
        for i in response.css('.lister-list tr'):
            movieName = i.css('.titleColumn a ::text').get()
            year = i.css('.titleColumn span ::text').get()
            url = i.css('::attr(href)').get()
            rating = i.css('.imdbRating strong ::text').get()
            dic = {
                'Movie':movieName,
                'URL':url,
                'year':year,
                'rating':rating
            }
            yield response.follow(url, callback=self.parseMovie, meta=dic)

    def parseMovie(self, response):
        movieName = response.meta['Movie']
        popularity = response.css('.sc-edc76a2-1::text').get()
        duration = response.css('.subtext time::text').get()
        directorName = response.css('.ipc-metadata-list__item a::text').extract()
        genres = response.css('a.sc-16ede01-3 span::text').extract()
        #genres = ' , '.join(response.css('.subtext a:not(:last-child)::text').getall())
        #directorName = response.css('h4:contains("Director") + a::text').get()
        directorUrl = response.css('h4:contains("Director") + a::attr(href)').get()
        dic = {
            'Movie Name': movieName,
            'popularity': popularity,
            # 'Duration': duration,
            'Genres' : genres,
            #'Director Name': directorName,
        }
        print(dic)
        #yield response.follow(directorUrl, callback=self.parseDir, meta=dic, dont_filter = True)

    def parseDir(self, response):
        topFourMovies = response.css('.knownfor-title-role a::text').getall()
        topFourMovies = ' , '.join(topFourMovies)
        yield {
            'Movie Name' : response.meta['Movie Name'],
            'Duration' : response.meta['Duration'],
            'Genres': response.meta['Genres'],
            'Director Name': response.meta['Director Name'],
            'Top Four Movies' : topFourMovies
        }

        pass




