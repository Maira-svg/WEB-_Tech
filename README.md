# WEB-_Tech
🚀 EventEase – Quick Project Guide

EventEase is a Flask + MongoDB Event Management System where users can browse events, register for free or paid events, and admins can manage events.

📊 ERD Diagram (Visual):<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/6734a19a-95dc-49c1-bbeb-6ace4c82b98b" />


👥 User Roles
Role	Features
👤 Guest	View events, browse site, contact
👥 User	Register/login, dashboard, join events, pay for paid events
👑 Admin	Create events, edit events, delete events, view all users
📁 Project Structure
EventEase/
│
├── app.py
├── requirements.txt
└── README.md
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
