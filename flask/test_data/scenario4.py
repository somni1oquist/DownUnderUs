from test_data.scenario_data_post import create_post, create_replies

def scenario4():
    post_id = create_post(
        content="I've heard that Liu Cixin, author of the science fiction novel Three Bodies, is coming to Perth on June 25th for a book signing; I'm a huge fan of his books and really enjoy his novels. Anyone in Perth interested? We can all go to the book signing and join the event, and we can also have a fan club.",
        title="Attention Perth book fans! Cixin Liu book signing coming soon!",
        topic="Social",
        location="Perth",
        selected_tags=["#Cixin Liu", "#UWA", "#Perth", "#science fictiom", "#3 bodies", "#book signing"],
        img_path="/static/images/scenario4/3-body-1.jpg",
        user_id=25,
        post_date="2024-05-14 18:15:24"
    )
    first_reply_id = create_replies(
        content="I watched the Trilogy TV show and it was super good! It's attracted my interest in buying the book. I'd also love to go to Perth for a book signing, but I'm not sure the timing is right.",
        reply_date="2024-05-15 10:45:18",
        post_id=post_id,
        user_id=18,
        votes=5
    )
    # Reply to the first reply
    create_replies(
        content="I'd love to go, but I have other appointments that day and I'm not sure if I can fit it in. I'll try to adjust my schedule to be sure to attend, though!",
        reply_date="2024-05-15 17:45:27",
        parent_id=first_reply_id,
        user_id=24
    )
    create_replies(
        content="Where is the location does anyone know? My family lives in the Fremental area and I'm not sure if it's too far for me. If it's not too far, I'd consider attending.",
        reply_date="2024-05-14 23:19:24",
        parent_id=first_reply_id,
        user_id=26,
        votes=8
    )

    second_reply_id = create_replies(
        content="I am also a Perth resident and was very excited when I heard the news! As far as I know, the event should be held in the Reid Library of UWA, starting at 11 a.m. on June 25. Although I am not a fan of science fiction novels, I think this book signing will be very interesting, and I am ready to go and see the excitement!",
        img_path="/static/images/scenario4/3-body-2.jpg",
        reply_date="2024-05-14 22:01:24",
        post_id=post_id,
        user_id=19,
        votes=12,
        accepted=True
    )
    # Reply to the second reply
    create_replies(
        content="I live in a dormitory on the UWA campus, which is great! ! I can go to the event directly from my dormitory. I am also a fan of science fiction novels, and I am very excited to meet Liu Cixin in person!",
        reply_date="2024-05-15 21:30:15",
        parent_id=second_reply_id,
        user_id=33
    )
    create_replies(
        content="I'm also a huge fan of Cixin Liu's books! I heard he's coming to Perth for a book signing and I've been ready to go for a long time. I hope to be able to connect with other fans and share my love for his work then!",
        reply_date="2024-05-14 23:19:24",
        parent_id=second_reply_id,
        user_id=16
    )
    second_first_first_reply_id = create_replies(
        content="I've heard the news as well! My house is not far from Perth and I'm really looking forward to attending the signing! However, I think it's important to plan ahead because it's sure to be crowded and I'll be in a mood to lose my mind if I don't grab an autograph by then.",
        reply_date="2024-05-15 16:20:09",
        parent_id=second_reply_id,
        user_id=30,
        votes=5
    )
    create_replies(
        content="It's great to see so many people going",
        reply_date="2024-05-15 17:10:29",
        parent_id=second_first_first_reply_id,
        user_id=25
    )
    
    third_reply_id = create_replies(
        content="I've always had some interest in Liu Cixin's novels, but I've never had the chance to delve into them. This book signing sounds interesting, maybe I can take the opportunity to buy a few books to go back and savor.",
        reply_date="2024-05-15 22:15:50",
        post_id=post_id,
        user_id=1,
        votes=10
    )
    # Reply to third reply
    create_replies(
        content="Ditto! I've heard of him before, but never actually gotten around to reading his books. This book signing could be a great opportunity to get into his work.",
        reply_date="2024-05-15 22:23:50",
        parent_id=third_reply_id,
        user_id=36,
        votes=5
    )
    create_replies(
        content="Yes, book signings are not only a chance to meet the author in person, but also to share your love of his work and exchange ideas with other fans. I hope you have an enjoyable experience!",
        reply_date="2024-05-16 10:45:20",
        parent_id=third_reply_id,
        user_id=31,
        votes=10
    )
    create_replies(
        content="I've always been interested in science fiction, but I've never been exposed to Liu Cixin's work. This book signing seemed like a great opportunity to get to know his work, and incidentally, to share my thoughts with other fans.😁",
        reply_date="2024-05-16 11:30:59",
        parent_id=third_reply_id,
        user_id=26
    )
    
    fourth_reply_id = create_replies(
        content="I watched the trilogy TV series and I felt it was pretty good, especially the special effects were done quite cool. But compared to the original, there are still some parts that weren't shown very well.",
        reply_date="2024-05-16 14:00:35",
        post_id=post_id,
        user_id=38,
        votes=7
    )
    create_replies(
        content="I felt the same way! The special effects were really stunning, but the plot was cut in some places compared to the original, causing the overall feel to be a bit distorted.",
        reply_date="2024-05-16 14:30:50",
        parent_id=fourth_reply_id,
        user_id=34
    )

    create_replies(
        content="Agree with you that the TV series does give a visually stunning feel, but the psychological portrayal of the original characters and the unfolding of the complex plot is a bit rushed. Perhaps this is a common dilemma when remaking novels to TV series.",
        reply_date="2024-05-16 16:00:25",
        post_id=post_id,
        user_id=12
    )