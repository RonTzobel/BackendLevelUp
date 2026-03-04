# PR reply comments – paste each block in the matching GitHub thread

---

## 1. `app/routers/auth/auth.py` – POST `/google/token`  
**Thread:** "בשביל מה זה ?"

**Reply (English):**
```
This endpoint lets Google-sign-in users call our API with our own JWT. After Google login, the frontend only has the Google ID token. Our PUT /users/preferences and GET /users/me expect a JWT we issue (from our SECRET_KEY). So we added POST /auth/google/token: the client sends the Google token, we validate it and return our JWT. The frontend then uses that JWT for profile/preferences. Without this, Google users got "Could not validate credentials" on the profile page.
```

**Reply (עברית):**
```
האנדפוינט הזה נועד כדי שמשתמשים שנכנסו עם גוגל יוכלו לקרוא ל-API עם JWT שלנו. אחרי התחברות גוגל, בפרונט יש רק את ה-token של גוגל. PUT /users/preferences ו-GET /users/me מצפים ל-JWT שאנחנו מנפיקים (עם ה-SECRET_KEY שלנו). אז הוספנו POST /auth/google/token: הלקוח שולח את הטוקן של גוגל, אנחנו מאמתים ומחזירים JWT שלנו. הפרונט משתמש ב-JWT הזה לפרופיל והעדפות. בלי זה משתמשי גוגל קיבלו "Could not validate credentials" בדף הפרופיל.
```

---

## 2. `app/routers/users/users.py` – PUT `/by-email/{email}`  
**Thread:** "למה שנית את זה ?"

**Reply (English):**
```
We renamed it so PUT /users/preferences would work. Before: we had both PUT /users/preferences and PUT /users/{email}. FastAPI matched PUT /users/something to the second route first, so "preferences" was treated as an email and PUT /users/preferences never ran. So we moved the update-by-email route to PUT /users/by-email/{email} and left PUT /users/preferences as-is. Now both routes work.
```

**Reply (עברית):**
```
שינינו כדי ש-PUT /users/preferences יעבוד. לפני: היו גם PUT /users/preferences וגם PUT /users/{email}. FastAPI התאים PUT /users/משהו לרוט השני קודם, אז "preferences" נחשב כאימייל ו-PUT /users/preferences לא הופעל. אז העברנו את העדכון לפי אימייל ל-PUT /users/by-email/{email} והשארנו את PUT /users/preferences כמו שהוא. עכשיו שני הרוטים עובדים.
```

---

## 3. `app/routers/users/users.py` – `joined = current_user.joined or ...`  
**Thread:** "למה צריך את זה ?"

**Reply (English):**
```
For Google users, `joined` was sometimes missing in the DB, so the profile page showed nothing for "Member since" / "Last login". This line guarantees we always return a date: use the stored `joined` if it exists, otherwise fall back to now so the UI has something to show.
```

**Reply (עברית):**
```
אצל משתמשי גוגל השדה joined לפעמים לא היה במסד, אז בדף הפרופיל "Member since" / "Last login" היו ריקים. השורה הזו מבטיחה שאנחנו תמיד מחזירים תאריך: אם יש joined שמור – משתמשים בו, אחרת נופלים ל-now כדי שבממשק יהיה מה להציג.
```

---

## 4. `app/dependencies.py` – token type `str` → `EmailStr`  
**Thread:** "תחזיר למה שהיה"

**Reply:**
```
Reverted as requested.
```
או: **החזרתי כמו שביקשת.**

---

## 5. `app/dependencies.py` – `JWTError` → `InvalidTokenError`  
**Thread:** "תחזיר למה שהיה"

**Reply:**
```
Reverted as requested.
```
או: **החזרתי כמו שביקשת.**

---

## 6. `app/server.py` – connect_args for SQLite  
**Thread:** "תחזיר למה שהיה"

**Reply:**
```
Reverted as requested.
```
או: **החזרתי כמו שביקשת.**

---

## 7. `app/db.py` – SQLite default + migration  
**Thread:** "תחזיר למה שהיה ?"

**Reply:**
```
Reverted as requested.
```
או: **החזרתי כמו שביקשת.**

---

*Note: After the reverts, the app expects PostgreSQL via DATABASE_URL (no SQLite default). Set DATABASE_URL in .env for local run.*
