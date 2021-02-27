# Final Curtain

Final Curtain is a website for checking the vital status (Dead or Alive) of the actors in a given film.

This is a second iteration on https://github.com/ewencluley/imdbdeadoralive which relied on screen scraping IMDB (as they have no api). 
Of course it eventually broke.

## Data
![](https://www.themoviedb.org/assets/2/v4/logos/v2/blue_long_2-9665a76b1ae401a510ec1e0ca40ddcb3b0cfe45f1d51b77a308fea0845885648.svg)

This site uses The Movie DB API (https://developers.themoviedb.org) to get film/tv show and actor data.

## How-to
### Run
```shell script
gunicorn finalcurtain.wsgi --log-file -
```
### Run Unit Tests
```shell script
python manage.py test
```