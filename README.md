# WEB-_Tech
EventEase - Quick Shortcut Guide 🚀
📊 Simple ERD Diagram
text
┌─────────┐          ┌─────────┐
│  USERS  │          │ EVENTS  │
├─────────┤          ├─────────┤
│PK id    │◄────────►│PK id    │
│  name   │     ▲    │  title  │
│  email  │     │    │  date   │
│  password│     │    │  price  │
│  role   │     │    │  image  │
└─────────┘     │    └─────────┘
                │          ▲
                │          │
           ┌────┴──────────┴────┐
           │   REGISTRATIONS     │
           ├─────────────────────┤
           │PK id                │
           │FK user_email        │
           │FK event_id          │
           │  paid (true/false)  │
           │  reg_date           │
           └─────────────────────┘
                │          ▲
                │          │
           ┌────┴──────────┴────┐
           │     PAYMENTS        │
           ├─────────────────────┤
           │PK id                │
           │FK user_email        │
           │FK event_id          │
           │  amount             │
           │  status             │
           └─────────────────────┘

Legend: PK = Primary Key, FK = Foreign Key
🎯 Quick System Flow
text
VISITOR ──► [Home/Events] ──► Register/Login ──► DASHBOARD
                              │
                   ┌──────────┴──────────┐
                   ▼                     ▼
              FREE EVENT             PAID EVENT
                   ▼                     ▼
            Register Now        Stripe Payment
                   ▼                     ▼
              CONFIRMATION ◄───────── SUCCESS
🔄 User Types & Actions
text
👤 GUEST          👥 USER          👑 ADMIN
─────────        ─────────        ─────────
• View           • Same as        • Same as User
• Browse         Guest +          • Create Events
• Contact        • Dashboard      • Edit Events
                 • Register       • Delete Events
                 • Pay Events     • View All Data
                 • My Events
📁 Core Files
text
EventEase/
│
├── app.py              # Main application (ALL code in one file!)
├── README.md           # Documentation
└── requirements.txt    # Dependencies
🔧 Quick Setup (3 Steps)
bash
# 1. Install
pip install flask pymongo bcrypt flask-cors stripe

# 2. Start MongoDB
mongod  # or sudo service mongod start

# 3. Run
python app.py
# Open: http://localhost:5000
🌐 Main Routes
text
GET  /              Home page
GET  /events        All events
GET  /login         Login form
POST /login         Login submit
GET  /register      Register form
POST /register      Register submit
GET  /dashboard     User dashboard
GET  /event/<id>    Event details
GET  /register_event/<id>  Free register
GET  /admin         Admin panel
GET  /contact       Contact page
💾 Database Collections
javascript
// Just 4 collections:
1. Users      // user accounts
2. Events     // event details
3. EventRegistrations  // who registered
4. Payments   // payment records
🔑 Default Test Accounts
text
Regular: user@test.com / password123
Admin:   admin@test.com / admin123
Stripe:  4242 4242 4242 4242 (test card)
🎨 Quick Color Reference
text
Primary:   #4361ee  (Blue)
Success:   #4cc9f0  (Light Blue)
Danger:    #f72585  (Pink)
Gradient:  Blue → Purple
📝 Common Commands
bash
# MongoDB queries
db.Users.find()
db.Events.find({price: {$gt: 0}})
db.EventRegistrations.find({user_email: "user@test.com"})

# Check if running
ps aux | grep mongo  # Linux/Mac
tasklist | findstr mongo  # Windows
🚨 Error Fixes
text
❌ MongoDB not connecting:
   → Run: mongod
   → Check: mongodb://localhost:27017/

❌ Flask not running:
   → Check port 5000 is free
   → Kill process: fuser -k 5000/tcp

❌ Stripe errors:
   → Use test keys only
   → Card: 4242 4242 4242 4242
⚡ Quick Tips
First login? Register as admin to create events

Testing payments? Use Stripe test card

Lost session? Clear cookies and login again

Events not showing? Check MongoDB is running

That's it! Just 4 collections, 1 main file, and 3 steps to run! 🎉
