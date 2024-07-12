# Gesture_Recognition_Flask
A Flask Application that recognizes the number of fingers you are holding up.

This gesture recognition model was taken from this [github repository](https://github.com/Gogul09/gesture-recognition.)

The pros of this model are:
* Ease of use: The code was very well written and easy to understand, making it very easy to adopt and integrate into my flask application. After tweaking the libraries and updating some code within the files, I got it working on my computer with relatively fast.

The cons of this model are:
* Limited features: The code only detects the number of fingers you are holding up, which is very simple compared to what other models might be able to do, the reason why those models could not be used in this short of time frame will be explained below
* Accuracy: The accuracy of this model is defintely a lot less than others, but I found it to be passable enough to use for the first iteration of the gesture recognition.

A few other models I would have had used:

[CNN gesture recognition](https://github.com/asingh33/CNNGestureRecognizer): This was the model that I orginaly wanted to use and felt like it was the superior version to the model that I was using before. It has very high accuracy and the capabilites seem nice. However, the code is very broken as it does not work in current enviornments and needs a lot of tweaking. I spent half a day on this one before going back to the drawing board and looking for other models to use. If I had more time, fixing this model so that the output was what it should be and then using that would have been the best bet.

[HAGRID](https://github.com/hukenovs/hagrid/tree/master): This model seems the most accurate and would give the best predictions, but I need to look much more into it before using it. Running it on my local machine proved to be very difficult, and so I need more time getting familiar with the code and the functionalities before adapting it for myself.

Overall, I felt like the model I chose was good enough to showcase my abilites of refactoring a gesture recongition model and utilizing the Flask api to create a web application. Further steps would include exploring HAGRID more and then using that instead. 

To run the application for yourself, all you have to do is to clone the repository onto your local machine and then run the *app.py* file, then proceed to the link in your terminal. Instructions on how the webapp works will be on the webapp. 
