
🚀 EventEase – Web Technology Project
EventEase is a modern Event Management System developed using Flask (Python) and MongoDB.
The system allows users to explore events, register for events, and administrators to manage the entire event system efficiently.

The platform supports free and paid events, secure user authentication, and online payment processing.

🎯 Project Overview
EventEase provides a centralized platform where different users interact with events based on their role.

The system enables:

• Visitors to browse events
• Users to register and participate in events
• Administrators to manage events and users
• Paid events to be handled through secure online payment

This system simplifies event organization and participation.

👥 User Roles
👤 Guest
Guests can only browse the website.

Features:

• View events
• Browse event details
• Access contact page

Guests must register to participate in events.

👥 User
Registered users have access to their personal dashboard.

Features:

• User Registration
• User Login
• Access Dashboard
• View available events
• Register for free events
• Pay for paid events
• View registered events

👑 Admin
Admin has full system control.

Features:

• Create events
• Update events
• Delete events
• View registered users
• View event registrations
• Monitor payments

🧩 System Features
1️⃣ User Authentication
The system supports secure authentication.

Users can:

• Register
• Login
• Access personal dashboard

Passwords are hashed for security.

2️⃣ Event Management
Admin can manage all events.

Event fields include:

• Event Name
• Description
• Date
• Location
• Price (Free or Paid)

3️⃣ Event Registration
Users can register for events.

Two types of events:

• Free Events → instant registration
• Paid Events → payment required

4️⃣ Online Payment
Paid events are handled using Stripe payment gateway.

Users can pay using Stripe test cards during testing.

🗂 Project Structure
EventEase/
│
├── app.py
├── requirements.txt
└── README.md
Files Description
app.py

Main Flask application file containing:

• Routes
• Database operations
• Authentication logic
• Event management

requirements.txt

Contains Python dependencies used in the project.

Example:

flask
pymongo
bcrypt
flask-cors
stripe
README.md

Contains project documentation and instructions.

⚙️ Installation Guide
Follow these steps to run the project.

1️⃣ Install Required Libraries
Run the following command:

pip install flask pymongo bcrypt flask-cors stripe
2️⃣ Start MongoDB Server
Run:

mongod
Linux users:

sudo service mongod start
3️⃣ Run the Application
Run the Flask server:

python app.py
4️⃣ Open the Website
Open in browser:

http://localhost:5000
🌐 Main Routes
Method	Route	Description
GET	/	Home Page
GET	/events	View all events
GET	/login	Login page
POST	/login	Login request
GET	/register	Register page
POST	/register	Register request
GET	/dashboard	User dashboard
GET	/event/<id>	Event details
GET	/register_event/<id>	Register for free event
GET	/admin	Admin dashboard
GET	/contact	Contact page
💾 MongoDB Database
The system uses MongoDB database with four collections.

1️⃣ Users
Stores login information.

Example:

{
  name: "Maira",
  email: "maira@test.com",
  password: "hashed_password",
  role: "user"
}
2️⃣ Events
Stores event information.

Example:

{
  title: "Tech Conference",
  description: "Annual technology event",
  date: "2026-04-15",
  location: "Karachi",
  price: 0
}
3️⃣ EventRegistrations
Stores which user registered for which event.

Example:

{
  user_email: "maira@test.com",
  event_id: "123456"
}
4️⃣ Payments
Stores payment details for paid events.

Example:

{
  user_email: "maira@test.com",
  event_id: "123456",
  amount: 50,
  status: "paid"
}
🔑 Default Test Accounts
User Account
Email

user@test.com
Password

password123
Admin Account
Email

admin@test.com
Password

admin123
💳 Stripe Test Card
Use this card for testing payments.

4242 4242 4242 4242
Expiry date: any future date
CVV: any 3 digits

🎨 UI Color Theme
Type	Color
Primary	#4361ee
Success	#4cc9f0
Danger	#f72585
Gradient	Blue → Purple
📝 Useful MongoDB Commands
Show all users
db.Users.find()
Show paid events
db.Events.find({price: {$gt: 0}})
Show user registrations
db.EventRegistrations.find({user_email: "user@test.com"})
🚨 Common Errors & Fixes
MongoDB Connection Error
Make sure MongoDB server is running.

Run:

mongod
Connection string:

mongodb://localhost:27017/
Flask Not Running
Make sure port 5000 is free.

Windows:

taskkill /F /IM python.exe
Linux:

fuser -k 5000/tcp
Stripe Payment Error
Use Stripe test keys and test card only.

4242



ChatGPT is still generating a response...
