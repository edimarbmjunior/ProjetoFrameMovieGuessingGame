package com.project.movie.frame.projetoframemovieguessinggame.ui.screens

import android.widget.Toast
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalFocusManager
import androidx.compose.ui.platform.LocalSoftwareKeyboardController
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import coil.compose.AsyncImage
import com.project.movie.frame.projetoframemovieguessinggame.R
import com.project.movie.frame.projetoframemovieguessinggame.data.model.Difficulty
import com.project.movie.frame.projetoframemovieguessinggame.data.repository.MovieRepository
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun GameScreen1Askeds(
    navController: NavController,
    difficulty: String,
    category: String,
    movieRepository: MovieRepository
) {
    val context = LocalContext.current
    val keyboardController = LocalSoftwareKeyboardController.current
    val focusManager = LocalFocusManager.current
    val scope = rememberCoroutineScope()

    val parsedDifficulty = remember(difficulty) {
        try {
            Difficulty.valueOf(difficulty)
        } catch (e: IllegalArgumentException) {
            Difficulty.EASY
        }
    }

    val movies = remember(parsedDifficulty, category, movieRepository) {
        movieRepository.getMoviesByDifficultyAndCategory(parsedDifficulty, category)
    }

    // Handle empty list
    if (movies.isEmpty()) {
        val noMoviesText = stringResource(R.string.no_movies_found)
        LaunchedEffect(Unit) {
            Toast.makeText(context, noMoviesText, Toast.LENGTH_SHORT).show()
            delay(1500)
            navController.navigate("game1") {
                popUpTo("game1") { inclusive = true }
                launchSingleTop = true
            }
        }
        Box(
            modifier = Modifier.fillMaxSize(),
            contentAlignment = Alignment.Center
        ) {
            Text(
                text = stringResource(R.string.no_movies_found),
                style = MaterialTheme.typography.bodyLarge
            )
        }
        return
    }

    // Pre-compute string resources
    val correctText = stringResource(R.string.correct)
    val wrongAnswerFormat = stringResource(R.string.wrong_answer)
    val surrenderFormat = stringResource(R.string.surrender_result)
    val enterMovieNameText = stringResource(R.string.enter_movie_name)
    val submitText = stringResource(R.string.submit)
    val surrenderText = stringResource(R.string.surrender)
    val movieCounterFormat = stringResource(R.string.movie_counter)
    val frameCounterFormat = stringResource(R.string.frame_counter)

    // Game state
    var currentMovieIndex by remember { mutableStateOf(0) }
    var currentFrameIndex by remember { mutableStateOf(0) }
    var correctCount by remember { mutableStateOf(0) }
    var wrongCount by remember { mutableStateOf(0) }
    var userGuess by remember { mutableStateOf("") }
    var isShowingFeedback by remember { mutableStateOf(false) }
    var feedbackMessage by remember { mutableStateOf("") }
    var enableInput by remember { mutableStateOf(true) }

    val currentMovie = movies[currentMovieIndex]
    val currentFrames = currentMovie.images
    val currentFrame = currentFrames[currentFrameIndex]

    fun navigateToFinish() {
        navController.navigate("finish/$difficulty/$category/$correctCount/$wrongCount") {
            popUpTo("game1") { inclusive = false }
        }
    }

    fun advanceToNextMovieOrFinish() {
        if (currentMovieIndex + 1 < movies.size) {
            currentMovieIndex++
            currentFrameIndex = 0
            userGuess = ""
            isShowingFeedback = false
            enableInput = true
        } else {
            navigateToFinish()
        }
    }

    val navigateBackToSelection: () -> Unit = {
        navController.navigate("game1") {
            popUpTo("game1") { inclusive = true }
            launchSingleTop = true
        }
    }

    Scaffold(
        modifier = Modifier.fillMaxSize(),
        containerColor = MaterialTheme.colorScheme.background,
        topBar = {
            TopAppBar(
                title = { Text(stringResource(R.string.guess_the_movie)) },
                navigationIcon = {
                    IconButton(onClick = navigateBackToSelection) {
                        Icon(
                            imageVector = Icons.AutoMirrored.Filled.ArrowBack,
                            contentDescription = stringResource(R.string.back_to_game_selection)
                        )
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.background
                )
            )
        },
        bottomBar = {
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 32.dp, vertical = 24.dp)
            ) {
                Button(
                    onClick = navigateBackToSelection,
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(56.dp),
                    shape = RoundedCornerShape(16.dp)
                ) {
                    Text(
                        text = stringResource(R.string.back_to_game_selection),
                        style = MaterialTheme.typography.titleMedium
                    )
                }
            }
        }
    ) { paddingValues ->
        Box(modifier = Modifier.fillMaxSize().padding(paddingValues)) {
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(horizontal = 24.dp),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                Spacer(modifier = Modifier.height(16.dp))

                Text(
                    text = String.format(movieCounterFormat, currentMovieIndex + 1, movies.size),
                    style = MaterialTheme.typography.titleMedium.copy(fontWeight = FontWeight.Bold),
                    color = MaterialTheme.colorScheme.onBackground
                )

                Spacer(modifier = Modifier.height(16.dp))

                UrlImage(
                    imageUrl = currentFrame.path,
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(240.dp)
                )

                Spacer(modifier = Modifier.height(8.dp))

                Text(
                    text = String.format(frameCounterFormat, currentFrameIndex + 1, currentFrames.size),
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.secondary
                )

                Spacer(modifier = Modifier.height(16.dp))

                OutlinedTextField(
                    value = userGuess,
                    onValueChange = { if (enableInput) userGuess = it },
                    label = { Text(enterMovieNameText) },
                    enabled = enableInput,
                    modifier = Modifier.fillMaxWidth(),
                    singleLine = true,
                    shape = RoundedCornerShape(12.dp)
                )

                Spacer(modifier = Modifier.height(16.dp))

                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(16.dp)
                ) {
                    Button(
                        onClick = {
                            if (!enableInput || isShowingFeedback) return@Button
                            keyboardController?.hide()
                            focusManager.clearFocus()

                            if (userGuess.trim().equals(currentMovie.name, ignoreCase = true)) {
                                correctCount++
                                feedbackMessage = correctText
                                isShowingFeedback = true
                                enableInput = false

                                scope.launch {
                                    delay(4500)
                                    advanceToNextMovieOrFinish()
                                }
                            } else {
                                if (currentFrameIndex + 1 < currentFrames.size) {
                                    currentFrameIndex++
                                    userGuess = ""
                                } else {
                                    wrongCount++
                                    feedbackMessage = String.format(wrongAnswerFormat, currentMovie.name)
                                    isShowingFeedback = true
                                    enableInput = false

                                    scope.launch {
                                        delay(7500)
                                        advanceToNextMovieOrFinish()
                                    }
                                }
                            }
                        },
                        modifier = Modifier.weight(2f),
                        enabled = enableInput,
                        shape = RoundedCornerShape(12.dp)
                    ) {
                        Text(submitText, style = MaterialTheme.typography.titleMedium)
                    }

                    OutlinedButton(
                        onClick = {
                            if (!enableInput || isShowingFeedback) return@OutlinedButton
                            keyboardController?.hide()
                            focusManager.clearFocus()

                            wrongCount++
                            feedbackMessage = String.format(surrenderFormat, currentMovie.name)
                            isShowingFeedback = true
                            enableInput = false

                            scope.launch {
                                delay(1500)
                                advanceToNextMovieOrFinish()
                            }
                        },
                        modifier = Modifier.weight(1f),
                        enabled = enableInput,
                        shape = RoundedCornerShape(12.dp)
                    ) {
                        Text(surrenderText, style = MaterialTheme.typography.titleMedium)
                    }
                }

                Spacer(modifier = Modifier.weight(1f))
            }

            // Feedback overlay
            if (isShowingFeedback) {
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(paddingValues)
                        .background(MaterialTheme.colorScheme.background.copy(alpha = 0.88f)),
                    contentAlignment = Alignment.Center
                ) {
                    Card(
                        modifier = Modifier
                            .fillMaxWidth(0.85f)
                            .padding(16.dp),
                        shape = RoundedCornerShape(20.dp),
                        colors = CardDefaults.cardColors(
                            containerColor = if (feedbackMessage == correctText) {
                                Color(0xFF2E7D32)
                            } else {
                                MaterialTheme.colorScheme.errorContainer
                            }
                        )
                    ) {
                        Box(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(vertical = 48.dp),
                            contentAlignment = Alignment.Center
                        ) {
                            Text(
                                text = feedbackMessage,
                                style = MaterialTheme.typography.headlineMedium.copy(fontWeight = FontWeight.Bold),
                                color = if (feedbackMessage == correctText) {
                                    Color(0xFFE8F5E9)
                                } else {
                                    MaterialTheme.colorScheme.onErrorContainer
                                },
                                textAlign = TextAlign.Center,
                                modifier = Modifier.padding(horizontal = 16.dp)
                            )
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun UrlImage(
    imageUrl: String,
    modifier: Modifier = Modifier
) {
    AsyncImage(
        model = imageUrl,
        contentDescription = null,
        modifier = modifier,
        contentScale = ContentScale.Fit
    )
}
