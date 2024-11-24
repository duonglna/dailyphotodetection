Daily Photo Bot
A personal project to automate uploading daily photos to a Telegram chat bot, analyze their content using TensorFlow for object detection, and review these memories after 365 days. The project integrates Make.com (formerly Integromat) for automation and TensorFlow for object classification.

Purpose
This project was designed to:

Build a habit of capturing daily moments.
Use AI to detect objects in photos and tag them for easy review.
Create a personalized, automated way to reflect on memories after a year.
Key Features
Daily Photo Upload: Automatically upload a photo to a Telegram chat bot every day.
Object Detection: Use TensorFlow to identify objects in the photo and tag them.
Automation with Make.com: Integrate Telegram with automation workflows for seamless photo uploads and reminders.
Memory Reflection: After 365 days, review photos and their detected tags.
How It Works
1. Uploading Daily Photos
Telegram Bot:

A Telegram bot receives daily photo uploads.
Users interact with the bot via simple commands like /upload or /review.
Make.com Automation:

Trigger: User uploads a photo to the Telegram bot.
Action: Save the photo to a database and forward it for object detection.
2. Object Detection
TensorFlow Integration:

Uses a pre-trained model (ssd_mobilenet_v2) to detect objects in uploaded photos.
Detected objects (e.g., "person", "dog", "building") are stored as tags in the database.
Non-Maximum Suppression (NMS) ensures clean and accurate tagging.
Example Detected Tags:

Photo: A person walking a dog in front of a building.
Tags: ['person', 'dog', 'building'].
3. Memory Reflection
After 365 days, the Telegram bot sends the user their photo along with its tags for reflection.
Users can browse through all previous photos and tags in a web app.
Tech Stack
Backend
Flask: Web framework for managing the bot and object detection pipeline.
PostgreSQL: Database for storing photo metadata, detected tags, and upload dates.
TensorFlow: For object detection with ssd_mobilenet_v2.
Automation
Make.com:
Automates photo uploads from Telegram to the backend.
Sends reminders for daily uploads and fetches photos for review after 365 days.
Frontend
Telegram Bot:
Simplifies user interaction.
Provides commands like /upload, /review, and /help.
Web App:
Displays photos, tags, and timelines.
Allows users to review photos from specific dates.