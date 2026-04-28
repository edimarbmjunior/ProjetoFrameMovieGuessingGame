package com.project.movie.frame.projetoframemovieguessinggame.data.model

import androidx.annotation.StringRes
import com.project.movie.frame.projetoframemovieguessinggame.R

enum class Difficulty(@StringRes val labelRes: Int) {
    EASY(R.string.difficulty_easy),
    MEDIUM(R.string.difficulty_medium),
    HARD(R.string.difficulty_hard);
}
