class MinfoView(View):
    def get(self, request, movie_pk):
        # movies = Movie.objects.order_by('-popularity')
        movie = get_object_or_404(Movie, pk=movie_pk)
        genres = Movie_genres.objects.all()
        mgenres = Genre.objects.all()

        if (movie.vote_average * 10 // 10) >= 8:
            vote_average = '★★★★★'
        elif (movie.vote_average * 10 // 10) >= 6:
            vote_average = '★★★★'
        elif (movie.vote_average * 10 // 10) >= 4:
            vote_average = '★★★'
        elif (movie.vote_average * 10 // 10) >= 2:
            vote_average = '★★'
        elif (movie.vote_average * 10 // 10) >= 0:
            vote_average = '★'

            return vote_average

        # genre = Movie_genres.objects.select_related(movie)
        # genre = Movie.objects.select_related(id)
        # genres = Movie_genres.objects.all()

        # select title, movie_id, genre_id, name
        # from movies_movie as mm, movies_movie_genres as mmg, movies_genre as mg
        # where mm.id = mmg.movie_id and mmg.genre_id = mg.id;
        
        gr = Movie_genres.objects.filter(movie__id=movie_pk).values('genre__name')

        context = {
            'movie': movie,
            'genres': genres,
            'mgenres': mgenres,
            'star': vote_average,
            'gr': gr
        }
        return render(request, 'movies/minfo.html', context)
