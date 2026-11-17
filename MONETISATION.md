# ArtOnBar — הגדרות הכנסה (מה נשאר לך לעשות)

כל המזהים והמחירים יושבים בקובץ אחד: `_config.yml`, בבלוק "MONEY SETTINGS".
אחרי כל שינוי שם: commit + push ל-main, ו-GitHub Pages בונה מחדש תוך דקה.

## 1. Booking.com (קישורי מלונות, 36 באתר)
1. הרשמה: https://www.booking.com/affiliate-program/v2/index.html (או דרך Travelpayouts, שמאגד גם GetYourGuide).
2. אחרי אישור, ב-Partner Centre מופיע מספר **AID**.
3. ב-`_config.yml`: `booking_aid: "1234567"`.
   כל קישור ל-booking.com באתר מקבל אוטומטית `?aid=...`.

## 2. GetYourGuide (118 קישורים וווידג'טים)
1. כניסה ל-https://partner.getyourguide.com → Profile → Partner ID.
2. באתר היו שני מזהים: `EAQF7O2` (אות O) ו-`EAQF702` (אפס). עכשיו יש ערך אחד:
   `gyg_partner_id: "EAQF7O2"` ב-`_config.yml`. תוודאי שזה הנכון ותתקני אם לא.

## 3. ניוזלטר (היום ההרשמות הולכות למייל שלך ונעלמות)
1. פתיחת חשבון חינמי ב-MailerLite (עד 1,000 נמענים) או Buttondown.
2. יצירת טופס Embedded form והעתקת כתובת ה-`action` של הטופס.
3. ב-`_config.yml`:
   - `newsletter_form_action: "https://...."`
   - `newsletter_email_field`: MailerLite → `"fields[email]"`, Mailchimp → `"EMAIL"`, Buttondown/Beehiiv → `"email"`.

## 4. Featured listings ו-Sponsored posts (עמוד /submit-a-bar/)
1. המחירים המוצעים (€49 לחודש, €249 לעונה, €99 לפוסט) ב-`pricing:` — תשני כרצונך.
2. בלי Stripe הכפתורים פותחים את טופס הפנייה עם החבילה מסומנת, ואת שולחת חשבונית ידנית.
3. עם Stripe: Dashboard → Payment Links → ליצור קישור לכל חבילה ולהדביק ב-`stripe_links:`.
   הכפתורים הופכים אוטומטית ל"Book it" שמוביל לתשלום.
4. כשבר משלם: בעמוד העיר שלו, על ה-`<a class="bar-list-item">`, להוסיף את הקלאס
   `bar-list-item--featured` ואת התג `<span class="tag tag--primary">Featured</span>`
   בשורת ה-`__sub`, ולהעביר אותו לדירוג 1.

## 5. הסתרת כתובת המייל בטפסים (FormSubmit)
1. https://formsubmit.co → המחרוזת האקראית מופיעה במייל האימות (או "Replace email with a hash").
2. ב-`js/main.js`: להחליף את הערך של `FORMSUBMIT_ID` במחרוזת.

## 6. נתונים (Search Console + GA4)
מהיר: Search Console → Performance → Export → Google Sheets; GA4 → Reports → Pages → Share → Export to Sheets.
הגיליונות ב-Drive נגישים ל-Claude דרך הקונקטור של Google Sheets.
קבוע: Service Account בגוגל עם גישה ל-GSC ול-GA4, וקובץ ה-JSON שלו כסוד בסביבת Claude Code.

## 7. פרסומות
לא לפני שיש נתוני תנועה. AdSense אפשרי מיד אבל משלם מעט; Ezoic דורש תנועה מינימלית; Mediavine דורש ~50 אלף סשנים בחודש.
