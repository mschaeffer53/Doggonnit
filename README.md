

# Doggonnit

**Project Overview**

Doggonnit is an app that lets a network of users help track and locate lost dogs.

Problem:

Everyday dogs run away, and families are left to search by themselves for their beloved pet.
Pedestrians, bikers, and drivers see these lost dogs running around their neiborhood, but for several reasons
(e.g. safety, time, physical ability) they may not be able to help catch the animal.

Solution:

This app will facilitate an exchange of information between these people so that dogs are reunited with their families sooner.

Features:
- An easy to read map that tracks sightings of lost dogs.
- User profiles that can contain information about the human and their pet.
- Alerts when you are in the area of a missing dog.
- Alerts when someone has spotted your missing dog.
- An interface that allows users to quickly report their dog missing or a lost dog sighting.

Libraries and frameworks:
- Django; GET and POST profile information to the database
- Geodjango or Mapbox to create maps and exract location information

**Functionality**

*New users will be prompted to set up an account* 

A basic account will let you:
  -  ~~See maps of lost dogs/sighted dogs~~
  -  ~~Post your own sightings of dogs to the network~~
  
~~An advanced account will let you:~~ *Only one type of account now*
  - Same features of basic account
  - Have profiles for your own dogs
  - Easily notify the network of your missing dog
  
 *Once signed in*
 
 The user will see a map of missing dogs in their area.
 The map will have points that represent where a dog was seen,
 and a line connecting the dots of a specific dog chronologically. The line connecting the 
 points will be stylized so that you can tell where the dog was most recently seen.
        
        #TODO 
        ~~Line connecting the points~~
        Get custom markers for dogmap homes
 ~~Users can click on dog profiles to get more details about the dog (e.g. name, breed, age, pictures, rewards).~~
 
 *Recovering a lost dog*
 
 Non-owners of the dog:
 - Can report a "soft-recovery" (i.e. the dog is found but not returned to the owner).
 - Owners will be alerted of the "soft-recovery" and the two parties will be able to contact each other.
 
 Owners of the dog:
 - Can report a "hard-recover" (i.e. the dog is home).
 - The instances of the dog on the map will be removed.
 - Post a success story.
 - Send a reward to "soft-recovery" user.
 
 *Other possible features*
  - A fun point reward system to game-ify the app. You get points for spotting dogs and recovering them. Unlock flair and different levels of awesomeness.
  - Text message alerts instead of e-mail alerts.
  - App stats about number of dogs found
  
  **Models**
  
  *User Profile*
  - Name
  - Phone number
  - E-mail
  - Address
  - Points (for reward system)
  - Foreign key (link to their dog's profile, many-to-many relationship)
  
  *Dog Profile*
  - Name
  - Age
  - Sex
  - Breed
  - Color
  - Pattern
  - Picture
  - Weight
  - Personality (e.g. timid, rabid, feral, friendly) 
  - Description
  - Lost Status (boolean)
  - Foreign key (link dog's map information)
  
  ~~*Map information*~~ *Missing Dog Report*
  - Location
  - Timestamp
  - Dog Profile info
  
  **Schedule**
  
  *Milestone 1*
  - ~~User profiles~~
  - ~~Dog profiles~~
  - ~~Maps~~
  - Alert System
  
  *Milestone 2*
  - Fun reward system
  - App stats
  
  *Milestone 3*
  - Blog page for success stories 
  - Bitcoin rewards
  
  *Milestone 4*
  - Phone app version
  - Push notifications
  - Paypal rewards


##todos and thoughts
- ~~make line color gradient~~
- add points for reward system
- delete sightings when dog is found
- ~~add more details to unknown dog map popup/side profile~~
- ~~connect user account details link to each page~~
- ~~make quick links on top of website~~
- ~~links to unknown dog map~~
- ~~alert dog owner when user sees their dog~~
- ~~add "missing since date/time" to missing profile~~
- bootstrap that shit! Getting there!
- Fix second row of profiles on dog map
- user who sees missing dog should get credit on the map or something
- ~~graphic art~~
- ~~in My Account add hyperlink to dogs profile page~~
- Anchor nav bar to top of page on scrolling
- ~~On dog profile page have map next to profile instead of under~~
- Have unknown dog points auto find possible profile matches
- Allow user who added point ability to delete it.
- ~~add logout button~~
- Notifications
- When user adds a marker they should be told that the dog owner was emailed.
- ~~Link to map in emails (views>def irecognizethatdog)~~
- ~~Not NULL error when creating new dog profile~~
- ~~Popups with timestamp and description/details on the dog profile map~~
- get newlines to work in emails