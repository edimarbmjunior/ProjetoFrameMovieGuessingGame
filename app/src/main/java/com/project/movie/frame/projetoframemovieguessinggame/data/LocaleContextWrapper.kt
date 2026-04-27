package com.project.movie.frame.projetoframemovieguessinggame.data

import android.content.Context
import android.content.ContextWrapper
import android.os.Build
import java.util.Locale

object LocaleContextWrapper {

    fun applyLocale(context: Context, localeTag: String?): ContextWrapper {
        val locale = if (localeTag.isNullOrBlank()) Locale.ENGLISH else Locale.forLanguageTag(localeTag)
        Locale.setDefault(locale)

        val config = context.resources.configuration
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.N) {
            config.setLocale(locale)
            return ContextWrapper(context.createConfigurationContext(config))
        } else {
            @Suppress("DEPRECATION")
            config.locale = locale
            @Suppress("DEPRECATION")
            context.resources.updateConfiguration(config, context.resources.displayMetrics)
            return ContextWrapper(context)
        }
    }
}
