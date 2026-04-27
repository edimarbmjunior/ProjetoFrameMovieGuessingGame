package com.project.movie.frame.projetoframemovieguessinggame

import android.content.Context
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.datastore.preferences.core.stringPreferencesKey
import androidx.lifecycle.lifecycleScope
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.project.movie.frame.projetoframemovieguessinggame.data.AppSettingsRepository
import com.project.movie.frame.projetoframemovieguessinggame.data.LocaleContextWrapper
import com.project.movie.frame.projetoframemovieguessinggame.data.dataStore
import com.project.movie.frame.projetoframemovieguessinggame.ui.screens.FinishScreen
import com.project.movie.frame.projetoframemovieguessinggame.ui.screens.GameScreen1
import com.project.movie.frame.projetoframemovieguessinggame.ui.screens.HomeScreen
import com.project.movie.frame.projetoframemovieguessinggame.ui.theme.AppSettingsViewModel
import com.project.movie.frame.projetoframemovieguessinggame.ui.theme.ProjetoFrameMovieGuessingGameTheme
import kotlinx.coroutines.flow.drop
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.launch
import kotlinx.coroutines.runBlocking

class MainActivity : ComponentActivity() {

    override fun attachBaseContext(newBase: Context) {
        val localeTag = runBlocking {
            newBase.dataStore.data
                .map { it[stringPreferencesKey("app_locale")] }
                .first()
        }
        val wrapped = LocaleContextWrapper.applyLocale(newBase, localeTag ?: "en")
        super.attachBaseContext(wrapped)
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()

        val repository = AppSettingsRepository(this)

        setContent {
            val viewModel: AppSettingsViewModel = viewModel(
                factory = AppSettingsViewModel.Factory(repository)
            )
            val isDarkTheme by viewModel.isDarkTheme.collectAsState()
            val appLocale by viewModel.appLocale.collectAsState()
            val navController = rememberNavController()

            ProjetoFrameMovieGuessingGameTheme(darkTheme = isDarkTheme) {
                NavHost(navController = navController, startDestination = "home") {
                    composable("home") {
                        HomeScreen(
                            navController = navController,
                            isDarkTheme = isDarkTheme,
                            appLocale = appLocale,
                            onThemeToggle = { viewModel.toggleTheme() },
                            onLocaleChange = { viewModel.setLocale(it) }
                        )
                    }
                    composable("game1") {
                        GameScreen1(navController = navController)
                    }
                    composable("finish") {
                        FinishScreen(navController = navController)
                    }
                }
            }
        }

        lifecycleScope.launch {
            repository.appLocale.drop(1).collect {
                recreate()
            }
        }
    }
}
