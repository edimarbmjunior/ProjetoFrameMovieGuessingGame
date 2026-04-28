# AGENTS.md

## Build Commands
- `./gradlew assembleDebug` - Build debug APK
- `./gradlew test` - Run unit tests
- `./gradlew connectedAndroidTest` - Run instrumented tests (requires emulator/device)

## Project Structure
- Single-module Android app (`:app`)
- Entry point: `app/src/main/java/.../MainActivity.kt`
- Package: `com.project.movie.frame.projetoframemovieguessinggame`
- Movie data: `app/src/main/assets/movies.json`

## Dependencies
- Edit versions in `gradle/libs.versions.toml` (version catalog)
- Do NOT add versions directly in `build.gradle.kts`

## Testing
- Unit tests: `app/src/test/java/`
- Instrumented tests: `app/src/androidTest/java/`

## Architecture & State Management
- **Navigation**: Jetpack Navigation Compose with `NavHost`
  - Routes: `home` -> `game1` -> `game1Askeds` -> `finish`
  - Uses `popUpTo` for back stack cleanup
- **Theme**: Light/Dark mode persisted via DataStore (`AppSettingsRepository`)
  - Toggle button only on `HomeScreen`
  - All screens observe theme from `AppSettingsViewModel`
- **Language**: EN/PT-BR persisted via DataStore
  - Changing language recreates the Activity via `LocaleContextWrapper`
- **Movie Data**: Loaded from `assets/movies.json` into memory at app startup
  - `MovieRepository` manages in-memory list with filtering and sorting

## Game Logic
- **Categories**: Acao, Comedia, Romance, Drama, Ficcao Cientifica, Animacao, Distopia
- **Difficulty Levels**: EASY, MEDIUM, HARD
- **Image Distribution**: 15 images per movie
  - EASY: first 5 images (order 0-4)
  - MEDIUM: middle 5 images (order 5-9)
  - HARD: last 5 images (order 10-14)
- **Category "All"**: Sends `"ALL"` string in navigation to include all categories

## JSON Schema (movies.json)
- `name`: Movie title in Portuguese
- `year`: Release year
- `director`: Director name
- `category`: One of the 7 categories
- `images`: Array of image objects
  - `path`: External URL to the image
  - `difficulty`: "EASY", "MEDIUM", or "HARD"
  - `order`: Integer 0-14 preserving image sequence

## External Image Sources
- **Primary**: `https://movie-screencaps.com/`
- **Fallback**: `https://www.themoviedb.org/`

## UI Screens
- **HomeScreen**: TopAppBar with theme toggle and language dropdown, game mode dialog, "How to Play" dialog
- **GameScreen1**: Difficulty selection cards, dynamic category list, "Start Game" button (enabled only when both selected)
- **GameScreen1Askeds**: Text input, submit/surrender, feedback overlay, progress counters ("Movie X of Y", "Image X of Y")
- **FinishScreen**: Results display, "Play Again" (same difficulty/category), "Home" (clears back stack)

## Image Loading
- Uses **Coil** (`AsyncImage`) for loading images from external URLs
- Permission `INTERNET` declared in `AndroidManifest.xml`
- Replaced legacy `AssetImage` with `UrlImage` composable

## Important Notes
- Uses Kotlin DSL (`.gradle.kts`) - not Groovy
- Compose is enabled in `app/build.gradle.kts`
- `kotlinx-serialization-json` used for JSON parsing
- `MovieJsonLoader` uses `mapIndexed` to preserve image order
- `MovieRepository` sorts images by `order` field
