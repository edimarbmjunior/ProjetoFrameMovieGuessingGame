---
name: android-design
description: Design Android UIs with Jetpack Compose following Material Design 3 guidelines and best practices
trigger: /android-design
---

# Android Design Guide

Design consistent, accessible Android UIs using Jetpack Compose and Material Design 3.

## Material Design 3 Principles

1. **Dynamic Color** - Use `dynamicColor` in themes when possible for system-adaptive palettes
2. **Expressive Typography** - Material 3 type scale (Display, Headline, Title, Body, Label)
3. **Tonal Elevation** - Use surface tint instead of shadows for elevation
4. **Accessible Contrast** - Minimum 4.5:1 for text, 3:1 for UI components

## Compose Layout Selection

| Use Case | Recommended Layout |
|----------|-------------------|
| Single child with positioning | `Box` |
| Horizontal arrangement | `Row` |
| Vertical arrangement | `Column` |
| Scrollable vertical list | `LazyColumn` |
| Scrollable horizontal list | `LazyRow` |
| Grid layout | `LazyVerticalGrid` |
| Overlapping elements | `Box` with `Modifier.offset` or `zIndex` |

## Theming Pattern

```kotlin
@Composable
fun MyAppTheme(
    darkTheme: Boolean = isSystemDarkColorScheme(),
    content: @Composable () -> Unit
) {
    val colorScheme = when {
        dynamicColor && Build.VERSION.SDK_INT >= 31 -> {
            val context = LocalContext.current
            if (darkTheme) dynamicDarkColorScheme(context) else dynamicLightColorScheme(context)
        }
        darkTheme -> DarkColorScheme
        else -> LightColorScheme
    }

    MaterialTheme(
        colorScheme = colorScheme,
        typography = Typography,
        content = content
    )
}
```

## Spacing System

- Use `Modifier.padding(16.dp)` for standard content padding
- Use `8.dp` for compact spacing between related elements
- Use `24.dp` for section separation
- Leverage `LazyColumn` item spacing via `verticalArrangement`

## Component Selection

| Component | Use When |
|-----------|----------|
| `Button` | Primary actions |
| `TextButton` | Secondary actions |
| `OutlinedButton` | Tertiary actions |
| `FilledTonalButton` | Subdued primary actions |
| `IconButton` | Toolbar actions |
| `FloatingActionButton` | Prominent single action |
| `Card` | Elevated content containers |
| `Surface` | Custom elevated containers |
| `Scaffold` | Page structure with top bar/bottom nav |

## Accessibility

- Use `contentDescription` on all images and icons
- Use `Semantics` for custom components
- Support 200% text scaling
- Ensure touch targets are minimum 48.dp
- Use `SelectionContainer` for selectable text

## Animation Guidelines

- Use `animateContentSize()` for size changes
- Use `AnimatedVisibility` for show/hide transitions
- Use `transition` animateFloatAsState for custom animations
- Keep durations under 300ms for micro-interactions
- Use `Easing.FastOutSlowInEasing` as default

## Anti-Patterns to Avoid

1. `Modifier.padding` after `Modifier.background` (order matters)
2. Hardcoded colors instead of theme colors
3. Fixed dimensions instead of wrap/fill
4. `Box` when `Column`/`Row` suffices
5. Missing `Modifier` when modifying components

## Project-Specific Notes

This is a movie guessing game project. Key UI considerations:
- Full-screen image display for movie frames
- Touch-friendly answer input
- Score display and timer visibility
- Game state feedback (correct/wrong animations)
- Dark mode support for extended play sessions