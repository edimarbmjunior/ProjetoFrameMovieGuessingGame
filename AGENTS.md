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
- AGP `9.1.1`, Kotlin `2.2.10`, Compose BOM `2026.02.01`
- `compileSdk = release(36) { minorApiLevel = 1 }`, `minSdk = 24`, `targetSdk = 36`
- `versionName = "0.0.5"`, `versionCode = 1`
- `REPOSITORIES_MODE.FAIL_ON_PROJECT_REPOS` in `settings.gradle.kts`
- Uses Kotlin DSL (`.gradle.kts`) — not Groovy
- Compose is enabled in `app/build.gradle.kts`
- `enableEdgeToEdge()` called in `MainActivity.onCreate()`

## Dependencies
- Edit versions in `gradle/libs.versions.toml` (version catalog)
- Do NOT add versions directly in `build.gradle.kts`

## Testing
- Unit tests: `app/src/test/java/`
- Instrumented tests: `app/src/androidTest/java/`

## Architecture & State Management
- **No DI framework** (no Hilt/Koin). Repositories and ViewModels are instantiated manually:
  - `MovieRepository` created as a property in `MainActivity`
  - `AppSettingsRepository` instantiated in `MainActivity.onCreate()`
  - `AppSettingsViewModel` uses a manual inner `Factory` class
- **Navigation**: Jetpack Navigation Compose with `NavHost`
  - Routes: `home` -> `game1` -> `game1Askeds/{difficulty}/{category}` -> `finish/{difficulty}/{category}/{correct}/{wrong}`
  - Uses `popUpTo` for back stack cleanup
  - `launchSingleTop = true` used extensively
  - `navigateHome` uses `popUpTo(0) { inclusive = true }` to clear entire back stack
- **Theme**: Light/Dark mode persisted via DataStore (`AppSettingsRepository`)
  - Toggle button only on `HomeScreen`
  - All screens observe theme from `AppSettingsViewModel`
  - Default fallback: `isSystemInDarkTheme()` if no saved preference
  - On Android 12+: uses `dynamicDarkColorScheme` / `dynamicLightColorScheme` when `dynamicColor = true`
- **Language**: EN/PT-BR persisted via DataStore
  - Changing language recreates the Activity via `LocaleContextWrapper`
  - `runBlocking` used inside `attachBaseContext` to read locale synchronously before context attachment
  - `settingsRepository.appLocale.drop(1).collect { recreate() }` skips initial emission
  - `Locale.setDefault(locale)` called globally
  - API < 24 uses deprecated `config.locale`; API 24+ uses `config.setLocale(locale)`
- **DataStore**: Exposed via Kotlin extension property `Context.dataStore` in `DataStoreModule.kt`
- **`MovieJsonLoader`** is a Kotlin `object` (singleton), called directly with `Context`, asset path, and repository

## Data Models
- **`Movie`**:
  - `id`: Runtime-generated `UUID.randomUUID().toString()` (not present in JSON)
  - `name`: Movie title in Portuguese
  - `nameEn`: Movie title in English
  - `year`, `director`, `category`
  - `images: List<ImageFrame>`
  - `getLocalizedName(locale: String)`: returns `name` if locale starts with `"pt"` (case-insensitive), otherwise `nameEn`
- **`ImageFrame`**:
  - `id`: Runtime-generated UUID
  - `movieId`: UUID of the parent movie
  - `path`: External URL
  - `difficulty`: `Difficulty` enum
  - `order`: Integer preserving image sequence (derived from `mapIndexed` in loader, not from JSON)
- **`MovieJsonDto`** (serialization target):
  - Uses `@SerialName("name_en")` to map JSON `name_en` to Kotlin `nameEn`
  - Does **NOT** contain `order` or `id` fields
- **`ImageJsonDto`**:
  - Contains `path` and `difficulty` only
  - Does **NOT** contain `order` (order is derived at load time)

## JSON Loading (`MovieJsonLoader`)
- Uses `kotlinx-serialization-json` for JSON parsing
- `Json { ignoreUnknownKeys = true }` — forward-compatible with schema changes
- `preloadFromAssets` workflow:
  1. Calls `repository.clearAll()` to remove stale data
  2. Parses `movies.json` into `List<MovieJsonDto>`
  3. Generates `UUID` for each `Movie.id`
  4. Maps images with `mapIndexed { index, ... -> order = index }` to preserve sequence
  5. Generates UUIDs for each `ImageFrame.id`
  6. Calls `repository.addMovie(movie)` for each movie
  7. Logs `"Preloaded X movies"` at `Log.i` level
- Wraps entire operation in try/catch: on failure, logs with `Log.e` but does **not** crash the app

## MovieRepository (`data/repository/MovieRepository.kt`)
- **In-memory mutable list** (`_movies`) exposed defensively via `movies: List<Movie> get() = _movies.toList()`
- `clearAll()` — empties the internal list (called before JSON preload)
- `addMovie(movie)`:
  - Detects duplicates by `name` **or** `nameEn` (case-insensitive)
  - **Overwrites** existing entry (not skip/merge) and logs warning
- `getMovieById(id: String)` — UUID lookup
- `getMovieByName(name: String)` — case-insensitive lookup by `name` **or** `nameEn`
- `getRandomMovie()` — returns random movie or `null` if empty
- `getUniqueCategories()` — returns distinct categories sorted alphabetically
- `getFramesByMovieId(movieId)` — returns images sorted by `order`
- `getFramesByMovieIdAndDifficulty(movieId, difficulty)` — filters by difficulty after sorting
- `getMoviesByDifficultyAndCategory(difficulty, category)`:
  1. Filters movies matching category (or all if `"ALL"`)
  2. Filters to movies that have at least one image of the requested difficulty
  3. Returns **deep copies** where `Movie.images` contains only images of that difficulty, sorted by `order`
  4. **Shuffles the result list** (`.shuffled()`) — order changes on every new game

## Game Logic
- **Categories**: Acao, Comedia, Romance, Drama, Ficcao Cientifica, Animacao, Distopia
- **Difficulty Levels**: EASY, MEDIUM, HARD
- **Image Distribution**: 15 images per movie
  - EASY: first 5 images (order 0-4)
  - MEDIUM: middle 5 images (order 5-9)
  - HARD: last 5 images (order 10-14)
- **Category "All"**: Sends `"ALL"` string in navigation to include all categories
- **Movie order**: Shuffled randomly on every new game via `getMoviesByDifficultyAndCategory().shuffled()`
- **Answer validation**: Accepts both Portuguese (`movie.name`) and English (`movie.nameEn`) titles, regardless of app language
- **Progressive frame advancement on wrong answer**:
  - Wrong guess with remaining frames → advances to next frame of **same movie**, clears input, does **NOT** increment `wrongCount`
  - Only when all frames are exhausted without correct guess → `wrongCount++`
- **Surrender**: Immediately increments `wrongCount` and reveals localized movie name
- **Correct answer**: Increments `correctCount`, shows "Correct!" feedback, disables input
- **Feedback overlay**: Stays on screen until user presses **"Continue"** button (no auto-advance delays)
- **Empty movie list handling**: Shows `Toast`, delays 1500ms, auto-navigates back to `"game1"`
- **Invalid difficulty fallback**: Catches `IllegalArgumentException` and defaults to `Difficulty.EASY`
- **Input disabling**: `enableInput = false` during feedback prevents further submissions
- **Keyboard management**: `keyboardController?.hide()` and `focusManager.clearFocus()` on submit/surrender
- **`key(currentFrame.id)`**: Forces Compose recomposition around `UrlImage` when frame changes
- **Debug logging**: `Log.d` prints movie index, frame index, `order`, `id`, and URL on every recomposition

## JSON Schema (movies.json)
- `name`: Movie title in Portuguese
- `name_en`: Movie title in English (mapped via `@SerialName("name_en")`)
- `year`: Release year
- `director`: Director name
- `category`: One of the 7 categories
- `images`: Array of image objects
  - `path`: External URL to the image
  - `difficulty`: "EASY", "MEDIUM", or "HARD"
  - Note: `order` is NOT in the JSON; derived at runtime via `mapIndexed`

## External Image Sources
- **Primary**: `https://movie-screencaps.com/`
- **Fallback**: `https://www.themoviedb.org/`

## UI Screens

### HomeScreen
- TopAppBar with theme toggle (emoji ☀️/🌙) and language dropdown (`appLocale.uppercase()`)
- TopAppBar title is empty; action buttons for language and theme only
- Game mode dialog (`AlertDialog`) controlled by `showGameSelection`
- "How to Play" dialog (`AlertDialog`) controlled by `showHowToPlay`
- Two `@Preview` composables: `HomeScreenLightPreview` and `HomeScreenDarkPreview`

### GameScreen1 (Selection)
- Difficulty cards in `Row` with `weight(1f)` and `Arrangement.SpaceEvenly`, height `80.dp`
- Categories in `FlowRow` with `maxItemsInEachRow = 3`, cards `100.dp × 48.dp`
- Toast validation if difficulty and category not both selected
- Back arrow calls `navController.popBackStack()`
- BottomBar "Back to Home" clears entire back stack (`popUpTo(0) { inclusive = true }`)

### GameScreen1Askeds (Gameplay)
- Receives `appLocale: String` as direct parameter from `MainActivity`
- Progress counters: "Movie X of Y", "Image X of Y"
- `OutlinedTextField`: `singleLine = true`, `shape = RoundedCornerShape(12.dp)`, enabled bound to `enableInput`
- Submit button (`weight(2f)`) / Surrender button (`weight(1f)`) ratio 2:1
- Feedback overlay: full-screen `Box` with `alpha = 0.88f` background
- Feedback card colors:
  - Correct: hardcoded green `Color(0xFF2E7D32)` with text `Color(0xFFE8F5E9)`
  - Wrong/Surrender: `errorContainer` with `onErrorContainer` text
- BottomBar contains "Back to Game Selection" button
- `UrlImage` composable wraps `AsyncImage`

### FinishScreen
- Route: `finish/{difficulty}/{category}/{correct}/{wrong}`
- Results Card with `containerColor = surfaceVariant`
- Correct count in green `Color(0xFF2E7D32)`, wrong count in theme error color
- "Play Again" navigates with `popUpTo("finish") { inclusive = true }`
- "Home" clears back stack (`popUpTo(0) { inclusive = true }`)
- TopAppBar back button uses unicode `\u2190` (left arrow) and navigates to `"game1"`
- BottomBar also has "Back to Home" button

## Image Loading
- Uses **Coil** (`AsyncImage`) for loading images from external URLs
- Permission `INTERNET` declared in `AndroidManifest.xml`
- `UrlImage` composable: `contentScale = ContentScale.Fit`, `placeholder = null`, `error = null`
- Replaced legacy `AssetImage` with `UrlImage` composable
- `key(currentFrame.id)` forces Coil to treat each frame as a distinct composable

## Theme & Colors
- Custom "Cinematic Minimalist" palette in `Color.kt`:
  - Light: `CinematicBlack`, `CinematicDarkGrey`, `CinematicWhite`, `CinematicOffWhite`, `CinematicLightGrey`
  - Dark: `CinematicBackgroundDark`, `CinematicSurfaceDark`, `CinematicPrimaryDark`, `CinematicSecondaryDark`
- Typography: mostly Material3 defaults; only `bodyLarge` is customized in `Type.kt`

## Localization
- Full string resource catalogs for EN (`values/strings.xml`) and PT-BR (`values-pt-rBR/strings.xml`)
- ~30 localized strings including all UI labels, toasts, dialog text, and game feedback
- `LocaleContextWrapper` handles API-level locale application differences

## Validation, Error Handling & Edge Cases
- Duplicate movies are **overwritten**, not ignored
- `ignoreUnknownKeys = true` provides forward JSON compatibility
- JSON load failure is caught and logged; app continues with empty repository
- `runBlocking` in `attachBaseContext` is deliberate to ensure locale is ready before super-context attachment
- Movies returned by `getMoviesByDifficultyAndCategory()` are defensive deep copies with only relevant-difficulty images

## Important Notes
- `kotlinx-serialization-json` used for JSON parsing
- `MovieJsonLoader` uses `mapIndexed` to preserve image order
- `MovieRepository` sorts images by `order` field
- `MovieRepository.getMoviesByDifficultyAndCategory()` shuffles results for random game order
