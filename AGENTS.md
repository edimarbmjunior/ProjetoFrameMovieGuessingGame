# AGENTS.md

## Build Commands
- `./gradlew assembleDebug` - Build debug APK
- `./gradlew test` - Run unit tests
- `./gradlew connectedAndroidTest` - Run instrumented tests (requires emulator/device)

## Project Structure
- Single-module Android app (`:app`)
- Entry point: `app/src/main/java/.../MainActivity.kt`
- Package: `com.project.movie.frame.projetoframemovieguessinggame`

## Dependencies
- Edit versions in `gradle/libs.versions.toml` (version catalog)
- Do NOT add versions directly in `build.gradle.kts`

## Testing
- Unit tests: `app/src/test/java/`
- Instrumented tests: `app/src/androidTest/java/`

## Notes
- Uses Kotlin DSL (`.gradle.kts`) - not Groovy
- Compose is enabled in `app/build.gradle.kts`