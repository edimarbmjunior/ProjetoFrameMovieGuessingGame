package com.project.movie.frame.projetoframemovieguessinggame.data.model

data class Movie(
    val id: String,
    val name: String,
    val year: Int,
    val director: String,
    val category: String,
    val images: List<ImageFrame>
)

data class ImageFrame(
    val id: String,
    val movieId: String,
    val path: String,
    val difficulty: Difficulty
)
