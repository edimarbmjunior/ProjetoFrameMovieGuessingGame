package com.project.movie.frame.projetoframemovieguessinggame.ui.screens

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.wrapContentSize
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.ListItem
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import androidx.navigation.compose.rememberNavController
import com.project.movie.frame.projetoframemovieguessinggame.R
import com.project.movie.frame.projetoframemovieguessinggame.ui.theme.ProjetoFrameMovieGuessingGameTheme

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HomeScreen(
    navController: NavController,
    isDarkTheme: Boolean,
    appLocale: String,
    onThemeToggle: () -> Unit,
    onLocaleChange: (String) -> Unit
) {
    var showGameSelection by remember { mutableStateOf(false) }
    var showHowToPlay by remember { mutableStateOf(false) }
    var expanded by remember { mutableStateOf(false) }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { },
                actions = {
                    Box(
                        modifier = Modifier.wrapContentSize(Alignment.TopEnd)
                    ) {
                        TextButton(onClick = { expanded = true }) {
                            Text(
                                text = appLocale.uppercase(),
                                style = MaterialTheme.typography.titleMedium
                            )
                        }
                        DropdownMenu(
                            expanded = expanded,
                            onDismissRequest = { expanded = false }
                        ) {
                            DropdownMenuItem(
                                text = { Text("English") },
                                onClick = {
                                    onLocaleChange("en")
                                    expanded = false
                                }
                            )
                            DropdownMenuItem(
                                text = { Text("Português (Brasil)") },
                                onClick = {
                                    onLocaleChange("pt-BR")
                                    expanded = false
                                }
                            )
                        }
                    }
                    TextButton(onClick = onThemeToggle) {
                        Text(
                            text = if (isDarkTheme) "☀️" else "🌙",
                            style = MaterialTheme.typography.titleLarge
                        )
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.background
                )
            )
        }
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .padding(horizontal = 32.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {
            Text(
                text = stringResource(R.string.app_title),
                style = MaterialTheme.typography.displayMedium.copy(
                    fontWeight = FontWeight.Bold
                ),
                textAlign = TextAlign.Center,
                color = MaterialTheme.colorScheme.onBackground
            )

            Spacer(modifier = Modifier.height(12.dp))

            Text(
                text = stringResource(R.string.tagline),
                style = MaterialTheme.typography.bodyLarge,
                textAlign = TextAlign.Center,
                color = MaterialTheme.colorScheme.secondary
            )

            Spacer(modifier = Modifier.height(48.dp))

            Button(
                onClick = { showGameSelection = true },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(56.dp),
                shape = RoundedCornerShape(16.dp),
                colors = ButtonDefaults.buttonColors(
                    containerColor = MaterialTheme.colorScheme.primary,
                    contentColor = MaterialTheme.colorScheme.onPrimary
                )
            ) {
                Text(
                    text = stringResource(R.string.start_game),
                    style = MaterialTheme.typography.titleMedium
                )
            }

            Spacer(modifier = Modifier.height(16.dp))

            OutlinedButton(
                onClick = { showHowToPlay = true },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(56.dp),
                shape = RoundedCornerShape(16.dp)
            ) {
                Text(
                    text = stringResource(R.string.how_to_play),
                    style = MaterialTheme.typography.titleMedium
                )
            }
        }
    }

    if (showGameSelection) {
        AlertDialog(
            onDismissRequest = { showGameSelection = false },
            title = {
                Text(
                    text = stringResource(R.string.choose_game_mode),
                    style = MaterialTheme.typography.titleLarge
                )
            },
            text = {
                Column {
                    ListItem(
                        headlineContent = {
                            Text(text = stringResource(R.string.classic_mode))
                        },
                        supportingContent = {
                            Text(text = stringResource(R.string.classic_mode_desc))
                        },
                        modifier = Modifier.clickable {
                            showGameSelection = false
                            navController.navigate("game1")
                        }
                    )
                }
            },
            confirmButton = { },
            dismissButton = {
                TextButton(onClick = { showGameSelection = false }) {
                    Text(stringResource(R.string.cancel))
                }
            }
        )
    }

    if (showHowToPlay) {
        AlertDialog(
            onDismissRequest = { showHowToPlay = false },
            title = {
                Text(
                    text = stringResource(R.string.how_to_play_title),
                    style = MaterialTheme.typography.titleLarge
                )
            },
            text = {
                Text(
                    text = stringResource(R.string.how_to_play_desc),
                    style = MaterialTheme.typography.bodyMedium
                )
            },
            confirmButton = {
                TextButton(onClick = { showHowToPlay = false }) {
                    Text(stringResource(R.string.got_it))
                }
            }
        )
    }
}

@Preview(showBackground = true)
@Composable
fun HomeScreenLightPreview() {
    ProjetoFrameMovieGuessingGameTheme(darkTheme = false) {
        HomeScreen(
            navController = rememberNavController(),
            isDarkTheme = false,
            appLocale = "en",
            onThemeToggle = {},
            onLocaleChange = {}
        )
    }
}

@Preview(showBackground = true)
@Composable
fun HomeScreenDarkPreview() {
    ProjetoFrameMovieGuessingGameTheme(darkTheme = true) {
        HomeScreen(
            navController = rememberNavController(),
            isDarkTheme = true,
            appLocale = "en",
            onThemeToggle = {},
            onLocaleChange = {}
        )
    }
}
