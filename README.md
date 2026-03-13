🚀 EventEase – Web Technology Project

EventEase is a Flask + MongoDB based Event Management System that allows users to browse events, register for free or paid events, and administrators to manage events efficiently.

🎯 Project Overview

EventEase provides a simple platform where:

Visitors can browse available events

Users can register and join events

Admins can create, update, and delete events

Paid events are processed using Stripe payments

👥 User Roles
Role	Features
👤 Guest	View events, browse website, contact page
👥 User	Register, login, access dashboard, join events, pay for paid events
👑 Admin	Create events, edit events, delete events, view users and registrations
📁 Project Structure
EventEase/
│
├── app.py              # Main Flask Application
├── requirements.txt    # Python Dependencies
└── README.md           # Project Documentation
⚙️ Installation Guide
1️⃣ Install Required Libraries
pip install flask pymongo bcrypt flask-cors stripe
2️⃣ Start MongoDB Server
mongod

Linux users can run:

sudo service mongod start
3️⃣ Run the Application
python app.py

Open your browser and visit:

http://localhost:5000
🌐 Main Routes
Method	Route	Description
GET	/	Home Page
GET	/events	View all events
GET	/login	Login form
POST	/login	Login submission
GET	/register	Registration form
POST	/register	Registration submission
GET	/dashboard	User dashboard
GET	/event/<id>	Event details
GET	/register_event/<id>	Register for free event
GET	/admin	Admin panel
GET	/contact	Contact page
💾 Database Collections

The system uses MongoDB with 4 collections:

Users
Events
EventRegistrations
Payments
Example MongoDB Structure
Users
{
  name: "Maira",
  email: "maira@test.com",
  password: "hashed_password",
  role: "user"
}
🔑 Default Test Accounts
User Account
Email: user@test.com
Password: password123
Admin Account
Email: admin@test.com
Password: admin123

Stripe Test Card

4242 4242 4242 4242
🎨 UI Color Theme
Type	Color
Primary	#4361ee
Success	#4cc9f0
Danger	#f72585
Gradient	Blue → Purple
📝 Useful MongoDB Commands

Check all users:

db.Users.find()

Find paid events:

db.Events.find({price: {$gt: 0}})

Find registrations of a user:

db.EventRegistrations.find({user_email: "user@test.com"})
🚨 Common Error Fixes
MongoDB Connection Error

Run MongoDB server:

mongod

Check connection:

mongodb://localhost:27017/
Flask Not Running

Make sure port 5000 is free.

Linux:

fuser -k 5000/tcp

Windows:

taskkill /F /IM python.exe
Stripe Payment Errors

Use Stripe test keys only

Test Card:

4242 4242 4242 4242
⚡ Quick Tips

✔ Register as Admin first to create events
✔ Use Stripe test card for payments
✔ If login fails → clear cookies and login again
✔ If events are not showing → check MongoDB server

🎉 Project Summary

Backend: Flask (Python)

Database: MongoDB

Payment: Stripe

Collections: 4

Main File: app.py

Simple architecture with 1 backend file and MongoDB database makes the project easy to run and maintain.

If you want, I can also make:

⭐ Professional GitHub README with badges

📊 ER Diagram for your report

🧾 15-page Web Technology project report

🎨 System Architecture Diagram

for your EventEase project submission.
