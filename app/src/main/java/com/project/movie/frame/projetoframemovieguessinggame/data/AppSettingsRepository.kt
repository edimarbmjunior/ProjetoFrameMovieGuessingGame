package com.project.movie.frame.projetoframemovieguessinggame.data

import android.content.Context
import androidx.datastore.preferences.core.booleanPreferencesKey
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.stringPreferencesKey
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map

class AppSettingsRepository(context: Context) {
    private val dataStore = context.dataStore

    private val darkThemeKey = booleanPreferencesKey("dark_theme")
    private val localeKey = stringPreferencesKey("app_locale")

    val isDarkTheme: Flow<Boolean?> = dataStore.data.map { preferences ->
        preferences[darkThemeKey]
    }

    val appLocale: Flow<String?> = dataStore.data.map { preferences ->
        preferences[localeKey]
    }

    suspend fun setDarkTheme(isDark: Boolean) {
        dataStore.edit { preferences ->
            preferences[darkThemeKey] = isDark
        }
    }

    suspend fun setLocale(locale: String) {
        dataStore.edit { preferences ->
            preferences[localeKey] = locale
        }
    }
}
