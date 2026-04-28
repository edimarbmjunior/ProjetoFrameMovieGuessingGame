package com.project.movie.frame.projetoframemovieguessinggame.data.repository

import android.util.Log
import com.project.movie.frame.projetoframemovieguessinggame.data.model.Difficulty
import com.project.movie.frame.projetoframemovieguessinggame.data.model.ImageFrame
import com.project.movie.frame.projetoframemovieguessinggame.data.model.Movie

class MovieRepository {

    private val _movies = mutableListOf<Movie>()
    val movies: List<Movie> get() = _movies.toList()

    fun clearAll() {
        _movies.clear()
    }

    fun addMovie(movie: Movie) {
        val existingIndex = _movies.indexOfFirst {
            it.name.equals(movie.name, ignoreCase = true)
        }
        if (existingIndex != -1) {
            Log.w("MovieRepository", "Duplicate movie found: '${movie.name}'. Overwriting existing entry.")
            _movies[existingIndex] = movie
        } else {
            _movies.add(movie)
        }
    }

    fun addAll(movies: List<Movie>) {
        movies.forEach { addMovie(it) }
    }

    fun getAllMovies(): List<Movie> = movies

    fun getMovieById(id: String): Movie? = _movies.find { it.id == id }

    fun getMovieByName(name: String): Movie? = _movies.find {
        it.name.equals(name, ignoreCase = true)
    }

    fun getFramesByMovieId(movieId: String): List<ImageFrame> {
        return _movies.find { it.id == movieId }?.images?.sortedBy { it.order } ?: emptyList()
    }

    fun getFramesByMovieIdAndDifficulty(movieId: String, difficulty: Difficulty): List<ImageFrame> {
        return getFramesByMovieId(movieId).filter { it.difficulty == difficulty }
    }

    fun getRandomMovie(): Movie? {
        if (_movies.isEmpty()) return null
        return _movies.random()
    }

    fun getUniqueCategories(): List<String> {
        return _movies.map { it.category }.distinct().sorted()
    }

    fun getMoviesByDifficultyAndCategory(
        difficulty: Difficulty,
        category: String
    ): List<Movie> {
        return _movies.filter { movie ->
            val categoryMatch = category.equals("All", ignoreCase = true) ||
                    movie.category.equals(category, ignoreCase = true)
            val hasFramesOfDifficulty = movie.images.any { it.difficulty == difficulty }
            categoryMatch && hasFramesOfDifficulty
        }.map { movie ->
            movie.copy(
                images = movie.images
                    .filter { it.difficulty == difficulty }
                    .sortedBy { it.order }
            )
        }
    }
}
