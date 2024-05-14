from test_data.scenario_data_post import create_post, create_replies

def scenario2():
    post_id = create_post(
        content="I'd like to move to new place near UWA also near my housemates' workplace (Stirling and Perth CBD). We got 6 people, can anyone recommend a good place?",
        title="Looking for a new place",
        topic="Rentals",
        location="Perth",
        selected_tags=["#Rentals", "#UWA", "#Stirling", "#Perth"],
        img_path="/static/images/scenario2/area.png",
        user_id=5,
        post_date="2024-05-14 18:15:24"
    )
    first_reply_id = create_replies(
        content="I recommend looking for a place in Subiaco. It's a nice place and close to UWA. I'm sure you can find a good place there.",
        reply_date="2024-05-14 21:15:24",
        post_id=post_id,
        user_id=10,
        votes=5
    )
    # Reply to the first reply
    create_replies(
        content="But Subiaco is quite expensive. I recommend looking for a place in Shenton Park. It's close to UWA and not as expensive as Subiaco.",
        reply_date="2024-05-14 23:15:24",
        parent_id=first_reply_id,
        user_id=11
    )
    create_replies(
        content="Subiaco is expensive but considering the convenience and life quality, it's worth it. I recommend Subiaco.",
        reply_date="2024-05-14 23:19:24",
        parent_id=first_reply_id,
        user_id=12,
        votes=8
    )

    second_reply_id = create_replies(
        content="Have you considered Belmont? It's close to Stirling and Perth CBD taking bus. It's a good place for families like you as well.",
        img_path="/static/images/scenario2/map.png",
        reply_date="2024-05-14 22:01:24",
        post_id=post_id,
        user_id=13,
        votes=77,
        accepted=True
    )
    # Reply to the second reply
    create_replies(
        content="Belmont is a good place but it's a bit far from UWA. What's the transportation plan?",
        reply_date="2024-05-14 23:15:24",
        parent_id=second_reply_id,
        user_id=14
    )
    create_replies(
        content="Actually I live in Belmont right now. It's a balanced choice as we're near bus stop the target places. But our lease is due so need to relocate. Some of us by vehicals, some by bus. It's not a big deal.",
        reply_date="2024-05-14 23:19:24",
        parent_id=second_reply_id,
        user_id=5
    )
    second_first_first_reply_id = create_replies(
        content="I see, then Osborne Park is also a good choice. It's close to Stirling and Perth CBD, and not far from UWA.",
        reply_date="2024-05-15 00:06:29",
        parent_id=second_reply_id,
        user_id=14,
        votes=1
    )
    create_replies(
        content="Thanks for the recommendation! I'll check out the places you mentioned.",
        reply_date="2024-05-15 00:10:29",
        parent_id=second_first_first_reply_id,
        user_id=5
    )
    
    third_reply_id = create_replies(
        content="Morley is another great option as well. It's close to Stirling and Perth CBD, and has a lot of bus routes to UWA.",
        reply_date="2024-05-14 23:15:04",
        post_id=post_id,
        user_id=1,
        votes=10
    )
    # Reply to third reply
    create_replies(
        content="I agree! Morley is a great place. It's convenient and has everything you need nearby.",
        reply_date="2024-05-14 23:19:04",
        parent_id=third_reply_id,
        user_id=2,
        votes=3
    )
    create_replies(
        content="I also recommend Morley. It's a great place for families and close to everything.",
        reply_date="2024-05-14 23:30:04",
        parent_id=third_reply_id,
        user_id=3,
        votes=2
    )
    create_replies(
        content="I've checked out Morley and it is a good place. However, It's hard to find a place that fits 6 people. I'll keep looking!😁",
        reply_date="2024-05-15 00:01:04",
        parent_id=third_reply_id,
        user_id=5
    )
    
    fourth_reply_id = create_replies(
        content="What about Innaloo? It's close to Stirling and Perth CBD, and has a lot of rental options 😀",
        reply_date="2024-05-14 23:30:32",
        post_id=post_id,
        user_id=4,
        votes=7
    )
    create_replies(
        content="Innaloo is a good choice so I've submit lots of applications for there. But all I got is rejection. Seems like this place doesn't like us...",
        reply_date="2024-05-14 23:35:32",
        parent_id=fourth_reply_id,
        user_id=5
    )

    create_replies(
        content="Thanks everyone for the recommendations! I'll check out the places you mentioned and see which one suits us best.😀😀",
        reply_date="2024-05-15 00:01:32",
        post_id=post_id,
        user_id=5
    )