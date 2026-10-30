# ReVision

<img src="icon.png" width="128" alt="ReVision app icon">

A 3v3 anime tag-team fighting game with original characters, a walkable town hub,
story mode, summons, events, raids and missions. Runs in the browser and on Android.

## Play

- **Browser:** open `index.html`.
- **Android:** grab the newest `ReVision-*.apk` from the
  [Releases page](../../releases/latest) on your phone and open it to install.
  Android may ask you to allow installing apps from your browser the first time.

## How the APK is built

Every push to `main` runs `.github/workflows/android.yml`, which:

1. copies `index.html` into the Android app with three.js bundled, so the game runs offline,
2. builds the app in `android/` (a full-screen landscape WebView), and
3. attaches the APK to a new GitHub Release and to the workflow run.

To update the game, replace `index.html` and push.

The app icon source is `icon.svg`; the Android launcher layers (background, foreground and a
monochrome layer for themed icons) live in `android/app/src/main/res/mipmap-*`.

The APK is signed with the Android debug key, which is fine for sideloading.
Publishing to the Play Store needs your own release signing key.
