package com.project.movie.frame.projetoframemovieguessinggame.data.json

import com.project.movie.frame.projetoframemovieguessinggame.data.model.Difficulty
import kotlinx.serialization.Serializable

@Serializable
data class MovieJsonDto(
    val name: String,
    val year: Int,
    val director: String,
    val category: String,
    val images: List<ImageJsonDto>
)

@Serializable
data class ImageJsonDto(
    val path: String,
    val difficulty: Difficulty
)
