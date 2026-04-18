# Overview #
For Day 38 of the 100 Days of Code, I used natural language processing and Google Sheets to track exercise progress.
By inputting a short workout description, the program will track its duration and calories the exercise burned.

# Tech Stack #
- Python
- Requests
- Sheety

# Features #
- Takes an input from the user about a workout and requests an NLP library for the exercise included in the message
and an estimate of the calories burned and the duration of the exercise.
- The program then sends a post–request to Sheety, enabling it to provide all the relevant information into a Google sheet.

# Learning Outcomes #
In addition to learning how to use the Sheety API, I told myself after the last few projects that I would use proper class design
in my next task. I learned to appreciate how to run code using if __name__ == __main__, as in my eyes that line really captures
the essence of OOP.

As a final note on this day of coding, I have been inspired to start a project that would involve using my exercises on
a gym app and Google Sheets to track similar data automatically. I think it would be a practical and fun task that I am excited
to implement in real life.

# License #
MIT