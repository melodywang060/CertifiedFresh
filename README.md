# Certified Fresh

You've heard of Rotten Tomatoes, now get ready for Certified Fresh!

Our web app is designed to integrate Open CV, Python, & Express with gardening knowledge to lower the barriers of gardening and reduce organic waste.

Gardening is largely associated with people who have a green thumb. However, more often than not, people who fail at gardening probably didn't water their plants regularly and people who fail at using their produce don't even realize it's gone bad!

Certified Fresh takes in images and generates a healthiness index depending on the state of the plant or produce. The app is also able to remind users to water their plants or check their produce when the time comes. 

The main technologies include a bounding box-based image extraction to isolate the subject from any noise and then utilizing a custom made rgb detection script to determine healthiness based on parameters such as overall color values as well as "regions of rottenness". 

Based on this data, we provide users with a way to track their plants and produce using our growth tracker, which showcases the latest images of the subject as well as the healthiness index over time. Using this data, the users will be notified about what the best course of action is, such as watering their plants or quickly using their produce!

We also provide a beginner friendly index for gardening which features different plants based on what a user can provide.
