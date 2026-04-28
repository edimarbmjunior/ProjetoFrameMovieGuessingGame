package com.project.movie.frame.projetoframemovieguessinggame.data.json

import android.content.Context
import android.util.Log
import com.project.movie.frame.projetoframemovieguessinggame.data.model.ImageFrame
import com.project.movie.frame.projetoframemovieguessinggame.data.model.Movie
import com.project.movie.frame.projetoframemovieguessinggame.data.repository.MovieRepository
import kotlinx.serialization.json.Json
import java.util.UUID

object MovieJsonLoader {

    private const val TAG = "MovieJsonLoader"
    private val jsonParser = Json { ignoreUnknownKeys = true }

    fun preloadFromAssets(
        context: Context,
        assetPath: String,
        repository: MovieRepository
    ) {
        try {
            val jsonString = context.assets.open(assetPath).bufferedReader().use { it.readText() }
            val moviesDto = jsonParser.decodeFromString<List<MovieJsonDto>>(jsonString)

            repository.clearAll()

            for (dto in moviesDto) {
                val movieId = UUID.randomUUID().toString()
                val images = dto.images.mapIndexed { index, imageDto ->
                    ImageFrame(
                        id = UUID.randomUUID().toString(),
                        movieId = movieId,
                        path = imageDto.path,
                        difficulty = imageDto.difficulty,
                        order = index
                    )
                }

                val movie = Movie(
                    id = movieId,
                    name = dto.name,
                    year = dto.year,
                    director = dto.director,
                    category = dto.category,
                    images = images
                )

                repository.addMovie(movie)
            }

            Log.i(TAG, "Preloaded ${moviesDto.size} movies from $assetPath")
        } catch (e: Exception) {
            Log.e(TAG, "Error loading movies from $assetPath", e)
        }
    }
}
