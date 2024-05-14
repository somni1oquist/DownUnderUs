from scenario_data_post import create_post, create_replies

def scenario1():
    post_id = create_post(content = "Recently, I've been doing project every day at uni and it's making me feel dull. I heard that this season is the best time to stargaze. Is anyone interested in forming a carpool to go stargazing together? I'm thinking of going to Mandurah. Let me know if you're interested!😁",
                post_date="2024-05-13 18:15:24",
                title="Stargazing Carpool Adventure!",
                location="East Perth",
                topic="Social",
                selected_tags=["#Stargazing #Carpool #Mandurah #event"],
                img_path="/static/images/scenario1/stars.jpg",
                user_id=1)

    reply_1=create_replies(content="Count me in! 😍 I have a telescope that I can bring. We should find a place with less light pollution to watch the stars. I recommend going to Preston Beach; there are public restrooms and formal parking available.",
                reply_date="2024-05-13 21:15:24",
                post_id=post_id,
                img_path="/static/images/scenario1/route.png",
                user_id=2,
                votes=666,
                accepted=True
                )
    # reply to one
    create_replies(content="I agree! Preston Beach is a great place to stargaze. I'm excited to see the stars!😍",
                reply_date="2024-05-13 23:15:24",
                parent_id=reply_1,
                user_id=3
                )
    create_replies(content="I am in, too! I have a car and can drive. I can pick up people from the city. I'm excited to see the stars!😍",
                reply_date="2024-05-13 23:19:24",
                parent_id=reply_1,
                user_id=4
                )
    create_replies(content="Very nice recommendation! Let's go to Preston Beach!😍",
                reply_date="2024-05-14 00:01:24",
                parent_id=reply_1,
                user_id=1
                )

    reply_2=create_replies(content="I've been looking for a chance to really enjoy the night sky, and I'm so glad you organized this! When do we plan to leave?",
                reply_date="2024-05-14 22:01:24",
                post_id=post_id,
                user_id=5
                )

    reply_2_1= create_replies(content="How about this Saturday 6PM? We could have dinner at a restaurant in Mandurah before we start stargazing.😀",
                reply_date="2024-05-13 00:18:20",
                parent_id=reply_2,
                user_id=1
                )

    reply_2_1_1=create_replies(content="Sounds good! Saturday is a sunny day, but i have a shift at work until 5PM. Can we leave at 6:30PM?",
                reply_date="2024-05-13 00:20:20",
                parent_id=reply_2_1,
                user_id=2
                )

    create_replies(content="Sure! We can leave at 6:30PM. I'll update the post.😂",
                reply_date="2024-05-13 00:22:20",
                parent_id=reply_2_1_1,
                user_id=1      
    )


    reply_3=create_replies(content="This is a great idea! I live downtown and can pick up people nearby. What should we bring?",
                reply_date="2024-05-14 08:13:20",
                post_id=post_id,
                user_id=6
                )

    create_replies(content="I recommend bringing a blanket, a chair, and some snacks. I'll bring a chair and some snacks for everyone.😀",
                reply_date="2024-05-14 08:15:20",
                parent_id=reply_3,
                user_id=1
                )

    create_replies(content="I'll bring a picnic blanket and some drinks. I'm excited to meet everyone!",
                reply_date="2024-05-14 08:17:20",
                parent_id=reply_3,
                user_id=4
                )
                            

    reply_4=create_replies(content="This sounds fun! I don't have a car; can I carpool with someone? I live in Cannington.",
                reply_date="2024-05-14 09:00:01",
                post_id=post_id,
                user_id=7
                )
    reply_4_1=create_replies(content="I can pick you up! I live in East Perth, so I can swing by Cannington to pick you up.",
                reply_date="2024-05-14 09:02:01",
                parent_id=reply_4,
                user_id=1
                )
    create_replies(content="Thank you! I can share the fuel cost",
                reply_date="2024-05-14 09:03:01",
                parent_id=reply_4_1,
                user_id=7
                )

    reply_4_2=create_replies(content="I can also pick you up! I live in Victoria Park, so I can pick you up on the way.",
                reply_date="2024-05-14 09:05:01",
                parent_id=reply_4,
                user_id=2
                )

    create_replies(content="Thank you! Maybe we can carpool together. I can share the fuel cost.",
                reply_date="2024-05-14 09:06:01",
                parent_id=reply_4_2,
                user_id=7
                )
    # reply to 4_1
    create_replies(content="So i will take victoria park carpool, no need to pick me up",
                reply_date="2024-05-14 09:07:01",
                parent_id=reply_4_1,
                user_id=7
                )
    # reply 5
    create_replies(content="To All Brave Stargazers,Weather: Current forecasts suggest clear skies and mild winds on Saturday night, but it will still be chilly, so it is recommended to wear windbreakers. Since we'll be at a seaside beach, wearing hiking shoes is also advisable to protect your feet from the fine sand.Destination: Preston Beach, equipped with public restrooms and formal parking.Drive: It is about an hour's drive, all on asphalt roads with cell service. However, please watch out for kangaroos and rabbits that might dash across from the woods.Time: The Milky Way will be visible from 19:44 to 03:21, so lets plan to meet between 6:30 and 7:00 PM.Other Gear: Bring beach chairs, beach mats, snacks, and drinks.",
                reply_date="2024-05-14 10:00:01",
                post_id=post_id,
                user_id=1,
                img_path="/static/images/scenario1/night.jpg"
                )