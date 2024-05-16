from test_data.scenario_data_post import create_post, create_replies

def scenario3():
    initial_post_content = """
Hey Neighbours! 😍

I hope everyone's doing great! I'm excited to announce that I'm planning a 'Share the Plate' event for our community, \
and I could really use your input and ideas.

The main question on my mind is: Where should we host this fantastic event? Do we have any suggestions for a perfect \
location that can accommodate all of us? Feel free to chime in with your thoughts and recommendations!

Now, let me share what I have in mind. I'm itching to cook up a batch of my delicious Butter Chicken recipe - a crowd-pleaser,\
if I do say so myself! But of course, the more, the merrier! So, if cooking's your thing, why not bring along a dish that you \
love and share it with the rest of us? It'll be a feast to remember!

And let's not forget the fun part - games! I'm thinking some friendly competition to add a bit of excitement to the day. \
Whether it's board games, outdoor activities, or anything else you have in mind, let's make this event a blast! 😀

So, what do you say, neighbours? Are you in? Let's plan this 'Share the Plate' event together and make it an unforgettable \
experience for everyone!

Looking forward to hearing your ideas and seeing you all there!

PS: Mark your calendars! The event is scheduled for Saturday of the upcoming long weekend and will be held in Fremantle.

Also, to tantalise your taste buds and give you a sneak peek of what's to come, here's a glimpse of my mouthwatering Butter \
Chicken recipe:
"""

    final_post__content = """
Thanks everyone for your fantastic contributions and ideas. I'm overwhelmed by the fantastic response and the wealth of \
creative ideas pouring in for our 'Share the Plate' event! Your enthusiasm is truly contagious.😍

From the mouthwatering barbecue suggestions to the tantalising cultural twists, it's clear that we're in for a culinary \
adventure. And with the addition of live music and games, this event promises to be an absolute blast!

Also with the weather looking promising and our plans falling into place, I'm confident that this event is going to be a \
smashing success!

Just a quick update: we've settled on hosting the event this Saturday, taking full advantage of the upcoming long weekend. \
Our chosen venue is Fremantle's picturesque community park, easily accessible by public transport. So mark your calendars \
and prepare your favourite dishes! The festivities kick off at 11:00 AM, and I couldn't be more excited to share this special \
day with all of you.

Remember to pack your picnic baskets, bring along your favourite dishes, and don't forget the sunscreen, hats, and sunnies! \
Oh, and if you've got any board games or musical instruments lying around, be sure to toss those in too. Let's make this \
'Share the Plate' event a day to remember! 😀
"""
    post_id = create_post(content = initial_post_content,
                post_date="2024-05-13 18:15:24",
                title="Share the Plate Event: Let's Plan Together!",
                location="Fremantle",
                topic="Food and Cooking",
                selected_tags=["#FoodAndFun","#FamilyFriendly","#LocalEvent","#SunnyDay", "#BoardGames"],
                img_path= "/static/images/scenario3/ButterChicken.png",
                # Image Reference - https://www.marionskitchen.com/wp-content/uploads/2024/02/20240212_MK_Easiest-Butter-Chicken-From-Scratch-8.webp
                user_id=1)

    reply_1=create_replies(content="I love the idea of a 'Share the Plate' event! 😍 As for the location, what about the \
                           community park? It's spacious, has picnic tables, and a playground for the kids. Count me in \
                           for some homemade lasagna! Also, here's a picture of the community park, conveniently located \
                            next to the station, making it easily accessible via public transport.",
                reply_date="2024-05-13 21:15:24",
                post_id=post_id,
                img_path="/static/images/scenario3/community.png",
                # Image Reference - https://images.squarespace-cdn.com/content/v1/50afefd0e4b01c11f0ec0c82/1551238130609-C0HAH9S6XZCXEL0JSGUL/ElkRidgePark-101-DesignConcepts.jpg?format=1500w
                user_id=2,
                votes=666,
                accepted=True
                )

    create_replies(content="I second your suggestion for the park! It sounds like the perfect spot. I'll whip up my famous \
                   chocolate chip cookies for dessert! Can't wait for the fun and games!",
                reply_date="2024-05-13 23:15:24",
                parent_id=reply_1,
                user_id=3
                )

    reply_2=create_replies(content="I'm excited for the event! How about setting up a barbecue station at the park? I'll \
                           bring my grill and some burgers and hot dogs. Let's make it a feast to remember! Here's a \
                           snapshot of my barbecue setup to get everyone excited!",
                reply_date="2024-05-14 22:01:24",
                post_id=post_id,
                img_path="/static/images/scenario3/Bbq.png",
                # Image Reference - https://cdn.revjet.com/s3/csp/3493/1711656183543/Sonoma_Timberline-XL-Lifestyle_012_small.jpg
                user_id=4
                )

    create_replies(content="The barbecue idea sounds fantastic! I'll bring some side salads and condiments to \
                              complement the burgers and hot dogs. Can't wait to dig in! 😀",
                reply_date="2024-05-15 00:18:20",
                parent_id=reply_2,
                user_id=5
                )
    create_replies(content="I couldn't agree more! A barbecue in sunny weather sounds like a dream come true! \
                              I'll definitely be there to enjoy some delicious burgers and hot dogs hot off the grill. \
                              And to beat the heat, I'll whip up my signature lemonade - it's the perfect thirst-quencher \
                              for a sunny day! Can't wait to catch up with everyone and enjoy the fantastic food and weather! 😍",
                reply_date="2024-05-15 00:18:25",
                parent_id=reply_2,
                user_id=6
                )
    
    reply_2_3= create_replies(content="Love the idea! I've got all the barbecue tools covered - from the grill to the tongs \
                              and everything in between. Let's fire it up and make this event sizzle! Your barbecue setup \
                              looks impressive, by the way - it's got me even more pumped for the feast!",
                reply_date="2024-05-15 00:18:29",
                parent_id=reply_2,
                user_id=7
                )

    create_replies(content="I'm ready to contribute to the barbecue station as well! I've got a portable grill \
                               and some savoury marinades that'll take those burgers and hot dogs to the next level. \
                               Let's turn up the heat and make this gathering one to remember!",
                reply_date="2024-05-15 00:20:20",
                parent_id=reply_2_3,
                user_id=8
                )

    reply_3=create_replies(content="Brilliant idea, everyone! How about adding a little cultural twist? I'll bring my homemade \
                           falafel wraps with tahini sauce. Plus, I'll bring my guitar for some live music! Here's a sneak \
                           peek of my falafel wraps to get everyone drooling!",
                reply_date="2024-05-14 08:13:20",
                post_id=post_id,
                img_path="/static/images/scenario3/falafel.png",
                # Image Reference - https://thecozyapron.com/wp-content/uploads/2017/02/falafel_wrap_thecozyapron_02-13-17_1.jpg
                user_id=9
                )

    create_replies(content="Your falafel wraps look delicious! Can't wait to try them! And the idea of live music is just \
                   the cherry on top! Can't wait to savour those delicious wraps and enjoy the musical vibes at the event!😀",
                reply_date="2024-05-14 08:15:20",
                parent_id=reply_3,
                user_id=10
                )

    create_replies(content="Love the cultural twist you're bringing to the table!! And live music too? Count me in\
                    for sure! Can't wait to taste those mouthwatering falafel wraps and enjoy some great tunes together.",
                reply_date="2024-05-14 08:17:20",
                parent_id=reply_3,
                user_id=11
                )
    
    create_replies(content="Absolutely! Your enthusiasm is contagious! I'm thrilled to join in on the fun. \
                   As a fellow musician, I'll bring along my ukulele and jam along with your guitar. \
                   Can't wait to create some unforgettable melodies together while savouring those delicious falafel wraps! 😍",
                reply_date="2024-05-14 08:17:20",
                parent_id=reply_3,
                user_id=12
                )
                            

    reply_4=create_replies(content="Hey everyone! Great idea! 😄 The park sounds fantastic. I'll bring some grilled veggies \
                           skewers for the vegetarians. Looking forward to a day of good food and laughter!",
                reply_date="2024-05-14 09:00:01",
                post_id=post_id,
                user_id=13
                )
    
    reply_4_1=create_replies(content="Your grilled veggie skewers sound amazing! I'll definitely try some. I'll bring my \
                             board games collection for some indoor fun. Looking forward to it!",
                reply_date="2024-05-14 09:02:01",
                parent_id=reply_4,
                user_id=14
                )
    
    create_replies(content="I love the idea of bringing board games for some indoor fun too. It'll be a great way to \
                   keep everyone entertained while we wait for the food to cook on barbecue. Looking forward to the \
                   delicious food and playing some games together!",
                reply_date="2024-05-14 09:03:01",
                parent_id=reply_4_1,
                user_id=15
                )

    # reply 5
    create_replies(content=final_post__content,
                reply_date="2024-05-16 10:00:01",
                post_id=post_id,
                user_id=1,
                img_path="/static/images/scenario3/essentials.png"
                # Image Reference - ChatGPT
                )