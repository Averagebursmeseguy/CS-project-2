# CS project 2 - habit/wellness tracker

## About
We'll be making a simple app that will track the user's wellness and habits along with a short diary entry. Our tech stack will involve:
  - Tkinter(or even ttk) for UI
  - matplotlib for data visualisation
  - And despite **REALLY** wanting to use an ORM, Sqlite3 for Database-related things
(Please read up on how to use these)

We will build the UI with Tkinter and generate things like graphs and histograms with matplotlib. To run calculations, validations and storages we'll use python's Sqlite3.

## Things to include
  - Database tables to track:
      - Habits
      - daily habit log (water intake, sleep, homework time, etc)
      - daily mood/diary log (seperate from the habit log)
      - mood
        
  - UI Elements to add:
      - Dynamic goal completion calculation based on daily, monthly or weekly timespans
      - Query functions and sorting goals
      - (hopefully) easy to use UI and menu system
        
  - Database features to add:
      - Create new habits
          - Add entries to habits
          - see habit completion
      - Update habits
          - Change habit goals
      - query the habits
          - aggregate reports
          - progress calculations
          - minimum, maximum

