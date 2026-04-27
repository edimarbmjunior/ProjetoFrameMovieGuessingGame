package com.project.movie.frame.projetoframemovieguessinggame.ui.theme

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import com.project.movie.frame.projetoframemovieguessinggame.data.AppSettingsRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.launch

class AppSettingsViewModel(private val repository: AppSettingsRepository) : ViewModel() {

    private val _isDarkTheme = MutableStateFlow(false)
    val isDarkTheme: StateFlow<Boolean> = _isDarkTheme.asStateFlow()

    private val _appLocale = MutableStateFlow("en")
    val appLocale: StateFlow<String> = _appLocale.asStateFlow()

    init {
        viewModelScope.launch {
            val savedTheme = repository.isDarkTheme.first()
            _isDarkTheme.value = savedTheme ?: false

            val savedLocale = repository.appLocale.first()
            _appLocale.value = savedLocale ?: "en"
        }
    }

    fun toggleTheme() {
        viewModelScope.launch {
            val newValue = !_isDarkTheme.value
            _isDarkTheme.value = newValue
            repository.setDarkTheme(newValue)
        }
    }

    fun setLocale(locale: String) {
        viewModelScope.launch {
            _appLocale.value = locale
            repository.setLocale(locale)
        }
    }

    class Factory(private val repository: AppSettingsRepository) : ViewModelProvider.Factory {
        @Suppress("UNCHECKED_CAST")
        override fun <T : ViewModel> create(modelClass: Class<T>): T {
            if (modelClass.isAssignableFrom(AppSettingsViewModel::class.java)) {
                return AppSettingsViewModel(repository) as T
            }
            throw IllegalArgumentException("Unknown ViewModel class")
        }
    }
}
