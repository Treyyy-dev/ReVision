# ReVision

<img src="icon.png" width="128" alt="ReVision app icon">

A 3v3 anime tag-team fighting game with original characters, a walkable town hub,
story mode, summons, events, raids and missions. Runs in the browser and on Android.

## Play

- **Browser:** open `index.html`.
- **Android:** grab the newest `ReVision-*.apk` from the
  [Releases page](../../releases/latest) on your phone and open it to install.
  Android may ask you to allow installing apps from your browser the first time.

## Online setup (Firebase)

Online play runs on a free Firebase project: casual and ranked matches in the Arena, and the
shared town (choose **Online** after Start to see other players walking around the plaza and
inside buildings). Until it's connected, the Arena shows "not open yet".

If you change `firebase/database.rules.json` (for example, the `town` section added for the
shared town), paste it into **Realtime Database → Rules** again and press **Publish**.

1. Go to [console.firebase.google.com](https://console.firebase.google.com) and add a project
   (Google Analytics is optional).
2. **Build → Authentication → Get started → Sign-in method → Anonymous → Enable.**
3. **Build → Realtime Database → Create database.** Pick a location and start in **locked mode**.
   Open the **Rules** tab, replace everything with the contents of
   [`firebase/database.rules.json`](firebase/database.rules.json), and press **Publish**.
4. **Project settings (gear icon) → General → Your apps → Web (`</>`).** Register an app
   (no hosting needed) and copy the `firebaseConfig` object it shows. Make sure it includes
   `databaseURL`.
5. In `index.html`, replace `const FIREBASE_CONFIG=null;` with your config, for example
   `const FIREBASE_CONFIG={apiKey:"…",authDomain:"…",databaseURL:"…",projectId:"…",appId:"…"};`
   and push. The next APK build has online switched on.

The web config isn't a secret; access is controlled by the database rules.

How it works: players sign in anonymously; matchmaking runs through `queue/<mode>`; one player
hosts each fight and streams it to the other through `matches/<id>`; ranked ratings (Elo) live in
`players/<uid>`. The free tier includes 10 GB of database downloads a month, which is roughly
2,000 to 3,000 full matches.

## How the APK is built

Every push to `main` runs `.github/workflows/android.yml`, which:

1. copies `index.html` into the Android app with three.js and the Firebase SDK bundled,
2. builds the app in `android/` (a full-screen landscape WebView), and
3. attaches the APK to a new GitHub Release and to the workflow run.

To update the game, replace `index.html` and push.

The app icon source is `icon.svg`; the Android launcher layers (background, foreground and a
monochrome layer for themed icons) live in `android/app/src/main/res/mipmap-*`.

The APK is signed with the Android debug key, which is fine for sideloading.
Publishing to the Play Store needs your own release signing key.
