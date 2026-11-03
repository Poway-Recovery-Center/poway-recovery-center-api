""" Recovery group pages: the programs that meet at the center (data only, no database table)

Content is copied word for word from each group's page on powayrecoverycenter.org (source_url),
split into blocks the frontend lays out: an intro, then sections of
  {"type": "heading", "text"}              a section title
  {"type": "text", "html"}                 paragraphs/lists (only <p> <strong> <em> <ul> <li> <h3> <sup> <br>)
  {"type": "items", "items": [{label, html}]}  "key aspects" style label + description pairs
image is the group's photo in the frontend repo (images/programs/photos/).
"""

PROGRAMS = [{'slug': 'aa',
  'name': 'Alcoholics Anonymous',
  'short': 'AA',
  'image': 'images/programs/photos/aa.jpg',
  'intro': '<p>Alcoholics Anonymous is a fellowship of men and women who share their experience, strength and hope '
           'with each other that they may solve their common problem and help others to recover from alcoholism. The '
           'only requirement for membership is a desire to stop drinking. There are no dues or fees for AA membership; '
           'we are self-supporting through our own contributions. AA is not allied with any sect, denomination, '
           'politics, organization or institution; does not wish to engage in any controversy; neither endorses nor '
           'opposes any causes. Our primary purpose is to stay sober and help other alcoholics to achieve '
           'sobriety.</p>',
  'sections': [{'type': 'text',
                'html': '<p><strong>Alcoholics Anonymous</strong> history begins June 10, 1935 in Akron, Ohio when '
                        'Bill W. and Dr. Bob through the Oxford Group helped each other until forming what became AA. '
                        'They started working with alcoholics at Akron’s City Hospital. One patient, who soon achieved '
                        'sobriety, joined them and together they formed the foundation of what would later become '
                        'Alcoholics Anonymous. Same year a new group of alcoholics began forming in New York, followed '
                        'by another in Cleveland in 1939. Over the course of 4 years, these 3 initial groups helped '
                        'around 100 people achieve sobriety. In 1939 the Fellowship published its foundational text, '
                        '<em>Alcoholics Anonymous, </em>which outlined AA’s philosophy and introduced the <em>Twelve '
                        'Steps</em>. Media coverage generated a surge of interest and requests for help, Fellowship '
                        'grew significantly and in April 1946 Bill W. began promoting Twelve Traditions.</p><p>Today, '
                        'AA is present in approximately 180 nations. By 2018, AA had more then 2 million members and '
                        'more then 120 thousand groups.</p>'},
               {'type': 'heading', 'text': 'Here are some key aspects of AA'},
               {'type': 'items',
                'items': [{'label': '12-Step Program',
                           'html': 'The AA program is based on 12 steps, which encourage individuals to acknowledge '
                                   'their powerlessness over alcohol, seek help from a higher power (however they '
                                   'define it), and make amends for harm done in the past. The steps also include '
                                   'regular self-examination and maintenance of sobriety through daily practices.'},
                          {'label': 'Meetings',
                           'html': 'AA hosts regular meetings where members can share their experiences, challenges, '
                                   'and successes in a supportive environment. Meetings can be in-person or virtual, '
                                   'and they are typically open to anyone who wishes to stop drinking.'},
                          {'label': 'Anonymity',
                           'html': 'One of the key principles of AA is anonymity. Members are encouraged to protect '
                                   'the identity of other members to create a safe and supportive environment where '
                                   'people feel comfortable sharing their experiences without fear of stigma.'},
                          {'label': 'Support Network',
                           'html': 'AA promotes building a support network of people who understand what one is going '
                                   'through. Members are encouraged to form sponsorship relationships, where a more '
                                   'experienced member (the sponsor) offers guidance and support to someone newer to '
                                   'the program.'},
                          {'label': 'Literature',
                           'html': 'AA has published a variety of literature, including “The Big Book,” which outlines '
                                   'the principles of the program and includes personal stories from members.'},
                          {'label': 'Global Fellowship',
                           'html': 'AA has groups in many countries, making it accessible to people worldwide. The '
                                   'organization emphasizes that recovery can be achieved through community '
                                   'support.'}]},
               {'type': 'text',
                'html': '<h3>Types of Meetings:</h3><ul><li><strong>Open Meetings:</strong> These meetings are open to '
                        'anyone interested in learning about AA, including family and friends.</li><li><strong>Closed '
                        'Meetings:</strong> These are for individuals who identify as having a drinking problem. They '
                        'provide a more intimate space for sharing experiences.</li><li><strong>Specialty '
                        'Meetings:</strong> Some groups focus on specific populations or particular topics related to '
                        'recovery.</li></ul>'},
               {'type': 'text',
                'html': '<h3>Currently we have:</h3><ul><li>Men only</li><li>Women only</li><li>Mixed</li><li>Speaker '
                        'meetings</li><li>Seniors in Recovery</li><li>Discussion</li><li>Book Study</li></ul>'}],
  'source_url': 'https://powayrecoverycenter.org/aa/'},
 {'slug': 'aca',
  'name': 'Adult Children of Alcoholics',
  'short': 'ACA',
  'image': 'images/programs/photos/aca.jpg',
  'intro': '<p>Adult Children of Alcoholics is a Twelve Step, Twelve Tradition program of men and women who grew up in '
           'alcoholic or otherwise dysfunctional homes.</p><p>The ACA program was founded on the belief that family '
           'dysfunction is a disease that infected us as children and affects us as adults. Our membership also '
           'includes adults from homes were alcohol or drugs were not present; however, abuse, neglect or unhealthy '
           'behavior was.</p><p>We meet to share our experience and recovery in an atmosphere of mutual respect. We '
           'discover how alcoholism and other family dysfunction affected us in the past and how it influences us in '
           'the present. We begin to see the unhealthy elements of our childhood. By practicing the Twelve Steps, '
           'focusing on the ACA Solution, and accepting a loving Higher Power of our own understanding, we find '
           'freedom.</p>',
  'sections': [{'type': 'text',
                'html': '<p><strong>Adult Children of Alcoholics</strong> founded circa 1978 is a fellowship of people '
                        'who desire to recover from the effects of growing up in an alcoholic or otherwise '
                        'dysfunctional family. ACA membership has few formal requirements. ACA does not accept any '
                        'outside contributions and is supported entirely by donations from its members. The '
                        'organization is not related to any particular religion and has no political affiliation. Tony '
                        'A.<sup></sup> was among its co-founders and is the author of <em>The Laundry List</em>, '
                        '<em>12 steps for adult children of alcoholics</em> (known as “Tony A’s 12 '
                        'Steps”)<sup></sup><em>, The Problem</em>,<sup></sup> which are all published in his book, '
                        '<em>The Laundry List: The ACOA Experience</em> (co-authored with Dan F.)<sup></sup></p>'},
               {'type': 'heading', 'text': 'Here are some key aspects of ACA'},
               {'type': 'items',
                'items': [{'label': 'Understanding Dysfunction',
                           'html': 'Recognizing how alcoholism and family dysfunction affect emotional and '
                                   'psychological development.'},
                          {'label': 'Identifying Patterns',
                           'html': 'Acknowledging recurring behaviors and patterns that stem from childhood '
                                   'experiences, such as low self-esteem, difficulty with relationships, and fear of '
                                   'abandonment.'},
                          {'label': 'Healing Process',
                           'html': 'Emphasizing the importance of recovery through self-awareness, self-acceptance, '
                                   'and emotional healing.'},
                          {'label': 'Supportive Community',
                           'html': 'Creating a safe space for individuals to share their experiences, fostering '
                                   'understanding and connection with others who have similar backgrounds.'},
                          {'label': 'Twelve-Step Program',
                           'html': 'Utilizing a framework similar to Alcoholics Anonymous that encourages personal '
                                   'growth, accountability, and spiritual development.'},
                          {'label': 'Focus on Change',
                           'html': 'Encouraging members to work towards breaking the cycle of dysfunction and '
                                   'developing healthier coping mechanisms.'},
                          {'label': 'Commitment to Growth',
                           'html': 'Advocating for ongoing personal development and self-care practices.'},
                          {'label': 'Personal Responsibility',
                           'html': 'Encouraging individuals to take responsibility for their own actions and feelings. '
                                   'This includes recognizing that while they may have been affected by their '
                                   'upbringing, they have the power to make choices that lead to healing and '
                                   'growth.'}]},
               {'type': 'text',
                'html': '<h3>Member Experiences</h3><ul><li><strong>Common Challenges</strong>: Members often discuss '
                        'challenges like perfectionism, difficulty in setting boundaries, and struggles with intimacy '
                        'and trust in relationships.</li><li><strong>Personal Transformations</strong>: Many members '
                        'report significant changes in their self-perception and relationships as they work through '
                        'the recovery process.</li></ul>'},
               {'type': 'text',
                'html': '<h3>Therapeutic Techniques</h3><ul><li><strong>Inner Child Work</strong>: A significant '
                        'aspect of ACA is the concept of healing the “inner child.” This involves acknowledging and '
                        'nurturing the parts of oneself that were neglected or wounded during '
                        'childhood.</li><li><strong>Communication Skills</strong>: Members often learn effective '
                        'communication skills, helping them articulate their needs and feelings in healthier '
                        'ways.</li></ul>'}],
  'source_url': 'https://powayrecoverycenter.org/aca/'},
 {'slug': 'al-anon',
  'name': 'Al-Anon',
  'short': 'Al-Anon',
  'image': 'images/programs/photos/alanon.jpg',
  'intro': '<p>The Al-Anon Family Groups are a fellowship of relatives and friends of alcoholics who share their '
           'experience, strength and hope in order to solve their common problems. We believe alcoholism is a family '
           'illness and that changed attitudes can aid recovery.</p><p>Al-Anon is not allied with any sect, '
           'denomination, political entity, organization or institution; neither endorses nor opposes any cause. There '
           'are no dues for membership. Al-Anon is self-supporting through its own voluntary '
           'contributions.</p><p>Al-Anon has but one purpose: to help families of alcoholics. We do this by practicing '
           'the Twelve Steps, by welcoming and giving comfort to families of alcoholics and by giving understanding '
           'and encouragement to the alcoholics.</p>',
  'sections': [{'type': 'text',
                'html': '<p>Al-Anon was co-founded in 1951 by Anne B. and Lois W. (wife of AA co-founder Bill W.). '
                        'Before the formation of Al-Anon, independent groups of families of alcoholics met. “Bill '
                        'thought the[se] groups could be consolidated and that Lois should be the one to take it '
                        'on.”</p><p>Al-Anon adopted the Twelve Steps of Alcoholics Anonymous for their own use, '
                        'changing the word “alcoholics” in the 12th step to “others” (“we tried to carry this message '
                        'to others”).</p><p>Although people commonly turn to Al-Anon for help in stopping another’s '
                        'drinking, the organization recognizes that the friends and families of alcoholics are often '
                        'traumatized themselves and in need of emotional support and understanding.</p>'},
               {'type': 'heading', 'text': 'Here are some key aspects of Al-Anon'},
               {'type': 'items',
                'items': [{'label': 'Understanding and Support',
                           'html': 'Al-Anon offers a safe space for individuals to share their experiences and '
                                   'feelings with others who understand the challenges of living with someone who has '
                                   'an alcohol problem.'},
                          {'label': 'The 12 Steps',
                           'html': 'The program is based on the 12-step recovery model, which emphasizes personal '
                                   'growth, self-reflection, and community support.'},
                          {'label': 'Focus on Self-Care',
                           'html': 'Al-Anon encourages members to focus on their own well-being rather than trying to '
                                   'control or change the behavior of the alcoholic.'},
                          {'label': 'Anonymity',
                           'html': 'Confidentiality and anonymity are core principles, fostering an environment where '
                                   'members can share openly without fear of judgment.'},
                          {'label': 'Literature and Resources',
                           'html': 'Al-Anon provides various literature, including books and pamphlets, to help '
                                   'members understand the effects of alcoholism and how to cope.'},
                          {'label': 'Meetings',
                           'html': 'Regular meetings, both in-person and virtual, offer ongoing support and connection '
                                   'with others who are experiencing similar challenges.'},
                          {'label': 'Spiritual Growth',
                           'html': 'The program promotes spiritual development, encouraging members to find their own '
                                   'understanding of a higher power.'},
                          {'label': 'Empowerment',
                           'html': 'Members learn to reclaim their own lives and make positive changes by recognizing '
                                   'that they cannot control the alcoholic’s behavior.'}]},
               {'type': 'heading', 'text': 'Core principles'},
               {'type': 'items',
                'items': [{'label': 'Focus on Self-Care',
                           'html': 'Al-Anon emphasizes the importance of self-care for family members and friends of '
                                   'alcoholics. Members learn that they cannot change the drinker’s behavior but can '
                                   'work on their own reactions and well-being.'},
                          {'label': 'Detachment with Love',
                           'html': 'One of the key concepts is “detachment with love,” which encourages members to '
                                   'care for their loved ones without enabling harmful behaviors.'}]}],
  'source_url': 'https://powayrecoverycenter.org/al-anon/'},
 {'slug': 'alateen',
  'name': 'Alateen',
  'short': 'Alateen',
  'image': 'images/programs/photos/alateen-1.jpg',
  'intro': '<p>Alateen, part of Al-Anon Family Groups, is for young people who have been affected by alcoholism in a '
           'family member or friend. We help each other by sharing our experience, strength, and hope.</p><p>We '
           'believe alcoholism is a family disease affecting everyone emotionally and sometimes physically. Although '
           'we cannot change or control the alcoholics in our lives, we can detach from their problems while '
           'continuing to love them.</p><p>In Alateen we focus on our own program rather than outside issues such as '
           'religion, politics, social media, or other Twelve Step programs. There are no dues for membership. Alateen '
           'is self-supporting through its own voluntary contributions. Alateen has one purpose: to help young people '
           'affected by someone else’s drinking. We are careful to protect each other’s anonymity as well that of all '
           'Al-Anon and A.A. members.</p>',
  'sections': [{'type': 'text',
                'html': '<p><strong>Alateen</strong> is a support group for young people (typically ages 13–18) who '
                        'have been affected by someone else’s alcoholism or addiction. It is a part of the larger '
                        'Al-Anon Family Groups, which provide support to families and friends of individuals '
                        'struggling with alcohol abuse. Alateen offers a safe, confidential space for teenagers to '
                        'share their experiences, find understanding, and learn coping strategies.</p>'},
               {'type': 'heading', 'text': 'Here are some key aspects of Alateen'},
               {'type': 'items',
                'items': [{'label': 'Support for Teens',
                           'html': 'Alateen helps teenagers who are living in environments where a family member, '
                                   'friend, or loved one has an alcohol addiction. It helps them understand that they '
                                   'are not alone and that their feelings of confusion, fear, anger, or sadness are '
                                   'common among those affected by addiction.'},
                          {'label': 'The 12-Step Program',
                           'html': 'Like Al-Anon, Alateen uses the 12-step program derived from Alcoholics Anonymous '
                                   '(AA). This program provides a structure for personal growth, healing, and '
                                   'emotional resilience. The steps guide participants toward recovery through '
                                   'self-reflection, sharing, and learning how to detach from the behavior of the '
                                   'alcoholic or addict without condoning or enabling it.'},
                          {'label': 'Confidential and Nonjudgmental Environment',
                           'html': 'Meetings are led by trained adult sponsors who have experience in Al-Anon, '
                                   'ensuring a safe, supportive, and nonjudgmental environment. The primary focus is '
                                   'to listen, share experiences, and support each other.'},
                          {'label': 'Meetings',
                           'html': 'Alateen meetings are held in person, online, or by phone, and are usually free of '
                                   'charge. They are structured to allow participants to share their experiences, '
                                   'thoughts, and feelings, often with the help of a topic or reading. While each '
                                   'group may have its own specific format, the main goal is always to help members '
                                   'heal and grow emotionally.'},
                          {'label': 'Alateen’s Impact',
                           'html': 'Many teens who attend Alateen report feeling a sense of relief and belonging. By '
                                   'sharing their struggles with others who truly understand, they often feel less '
                                   'isolated. They also gain a better sense of control over their own lives and '
                                   'emotions, even if they cannot control the alcoholic’s behavior.'}]}],
  'source_url': 'https://powayrecoverycenter.org/alateen/'},
 {'slug': 'na',
  'name': 'Narcotics Anonymous',
  'short': 'NA',
  'image': 'images/programs/photos/na.jpg',
  'intro': '<p>Narcotics Anonymous is a fellowship of men and women who share their experience, strength, and hope '
           'with each other that they may solve their common problem and help others recover from addiction. We are '
           'not interested in what or how much you used, but in what you want to do about your problem and how we can '
           'help.</p>',
  'sections': [{'type': 'text',
                'html': '<p>Narcotics Anonymous was founded in 1953 by Jimmy K. It uses a 12-step model developed for '
                        'people with varied substance use disorders and is the second-largest 12-step '
                        'organization.</p><p>There are more than 77,000 NA meetings each week in 145 countries.</p>'},
               {'type': 'heading', 'text': 'Here are some key aspects of NA'},
               {'type': 'items',
                'items': [{'label': 'Meetings',
                           'html': 'NA holds regular meetings where members can share their experiences and support '
                                   'one another. These meetings are typically free and open to anyone struggling with '
                                   'substance use.'},
                          {'label': '12-Step Program',
                           'html': 'The program emphasizes personal recovery through the 12 steps, which include '
                                   'admitting powerlessness over addiction, seeking help from a higher power, and '
                                   'making amends for past mistakes.'},
                          {'label': 'Anonymity',
                           'html': 'The principle of anonymity is crucial to NA, allowing members to share openly '
                                   'without fear of judgment or repercussions.'},
                          {'label': 'Diversity',
                           'html': 'NA is inclusive and welcomes individuals from all backgrounds and walks of life. '
                                   'The organization acknowledges that addiction can affect anyone, regardless of age, '
                                   'gender, or socioeconomic status.'},
                          {'label': 'Literature and Resources',
                           'html': 'NA offers various resources, including literature on recovery, personal stories, '
                                   'and informational pamphlets that outline the program and its principles.'},
                          {'label': 'Global Presence',
                           'html': 'NA has a presence in many countries around the world, providing a supportive '
                                   'community for those in need.'}]},
               {'type': 'heading', 'text': 'Philosophy and Principles'},
               {'type': 'items',
                'items': [{'label': 'Recovery Focus',
                           'html': 'NA emphasizes that recovery is a personal journey. Members are encouraged to take '
                                   'responsibility for their own recovery while supporting others in their struggles.'},
                          {'label': 'Higher Power',
                           'html': 'The concept of a “higher power” is central to the 12-step program. Members can '
                                   'interpret this higher power in a way that resonates with them personally, whether '
                                   'it’s a traditional religious belief or a more abstract concept.'},
                          {'label': 'Sponsorship',
                           'html': 'Many members choose to work with a sponsor—someone who has experience in recovery '
                                   'and can provide guidance and support throughout the process.'}]}],
  'source_url': 'https://powayrecoverycenter.org/na/'},
 {'slug': 'ca',
  'name': 'Cocaine Anonymous',
  'short': 'CA',
  'image': 'images/programs/photos/ca.jpg',
  'intro': '<p>Cocaine Anonymous is a fellowship of men and women who share their experience, strength and hope with '
           'each other that they may solve their common problem and help others to recover from their addiction. The '
           'only requirement for membership is a desire to stop using cocaine and all other mind‐ altering substances. '
           'There are no dues or fees for membership; we are fully self‐ supporting through our own contributions. We '
           'are not allied with any sect, denomination, politics, organization or institution. We do not wish to '
           'engage in any controversy, and we neither endorse nor oppose any causes. Our primary purpose is to stay '
           'free from cocaine and all other mind‐ altering substances and to help others achieve the same freedom.</p>',
  'sections': [{'type': 'text',
                'html': '<p>October 12, 1979 is the earliest known date for the name “Cocaine Anonymous” – A New York '
                        'drug counsellor, John Burrell launched a special treatment group for coke users calling it '
                        '“Cocaine Anonymous.” Later, on November 20, 1979, on WBAB Radio with Joel Martin, the topic '
                        'of discussion is Cocaine Anonymous and John Burell is featured as the founder of Cocaine '
                        'Anonymous. It is a 12-step program that accepts everybody who desire freedom from “cocaine '
                        'and all other mind-altering substances” as members.</p>'},
               {'type': 'heading', 'text': 'Here are some key aspects of CA'},
               {'type': 'items',
                'items': [{'label': 'Fellowship',
                           'html': 'CA is a supportive community where members share their experiences, strength, and '
                                   'hope to help each other recover.'},
                          {'label': '12-Step Program',
                           'html': 'Similar to Alcoholics Anonymous, CA follows a 12-step approach, which includes '
                                   'admitting powerlessness over cocaine and seeking help from a higher power.'},
                          {'label': 'Meetings',
                           'html': 'Regular meetings provide a space for members to share their struggles and '
                                   'successes, offering mutual support.'},
                          {'label': 'Anonymity',
                           'html': 'Anonymity is a cornerstone, allowing members to share openly without fear of '
                                   'judgment.'},
                          {'label': 'Literature',
                           'html': 'CA provides literature, including the “Cocaine Anonymous Text” and other recovery '
                                   'resources to aid in the journey.'},
                          {'label': 'Service',
                           'html': 'Members are encouraged to engage in service to help others, reinforcing their own '
                                   'recovery and fostering community.'},
                          {'label': 'Diversity',
                           'html': 'CA welcomes individuals from all backgrounds and walks of life, promoting '
                                   'inclusivity and understanding.'},
                          {'label': 'Sponsorship',
                           'html': 'Members are encouraged to find a sponsor—someone who has experience in '
                                   'recovery—who can provide guidance, support, and accountability throughout the '
                                   'recovery process. This relationship is vital for personal growth and navigating '
                                   'challenges.'}]},
               {'type': 'heading', 'text': 'Philosophy and principles'},
               {'type': 'items',
                'items': [{'label': 'Powerlessness',
                           'html': 'Acknowledging powerlessness over cocaine and recognizing that addiction is a '
                                   'disease is fundamental. This admission is often seen as the first step toward '
                                   'recovery.'},
                          {'label': 'Spirituality',
                           'html': 'CA emphasizes a spiritual approach, encouraging members to seek a higher power, '
                                   'however they define it, to help in their recovery journey. This spirituality is '
                                   'not tied to any specific religion.'},
                          {'label': 'Personal Responsibility',
                           'html': 'Members are encouraged to take responsibility for their actions and decisions, '
                                   'promoting self-awareness and personal growth.'},
                          {'label': 'Honesty and Openness',
                           'html': 'CA fosters an environment where members can share their truths without judgment, '
                                   'emphasizing the importance of honesty in recovery.'},
                          {'label': 'Service to Others',
                           'html': 'Helping fellow members is crucial. Engaging in service not only supports others '
                                   'but also reinforces the individual’s own recovery.'},
                          {'label': 'Unity and Community',
                           'html': 'Building connections and fostering a sense of belonging are essential. The '
                                   'collective strength of the community supports individual recovery.'},
                          {'label': 'Continuous Growth',
                           'html': 'Recovery is viewed as an ongoing process. Members are encouraged to continue '
                                   'working on their personal development and remain vigilant against relapse.'}]}],
  'source_url': 'https://powayrecoverycenter.org/ca/'},
 {'slug': 'ga',
  'name': 'Gamblers Anonymous',
  'short': 'GA',
  'image': 'images/programs/photos/ga.jpg',
  'intro': '<p>GA is a fellowship of men and women who share their experiences, strength and hope with each other that '
           'they may solve their common problem and help others to recover from a gambling problem.</p><p>The only '
           'requirement for membership is a desire to stop gambling. There are no dues or fees for GA membership; we '
           'are self-supporting through our own contributions. GA is not allied with any sect, denomination, politics, '
           'organization or institution; does not wish to engage in any controversy; neither endorses nor opposes any '
           'cause. Our primary purpose is to stop gambling and to help other compulsive gamblers to do the '
           'same.</p><p>Most of us have been unwilling to admit we were real problem gamblers. No one likes to think '
           'they are different from their fellows. Therefore, it is not surprising that our gambling careers have been '
           'characterized by countless vain attempts to prove we could gamble like other people. The idea that '
           'somehow, someday, we will control our gambling is the great obsession of every compulsive gambler. The '
           'persistence of this illusion is astonishing. Many pursue it into the gates of prison, insanity or '
           'death.</p><p>We learned we had to concede fully to our innermost selves that we are compulsive gamblers. '
           'This is the first step in our recovery. With reference to gambling, the delusion that we are like other '
           'people, or presently may be, has to be smashed.</p><p>We have lost the ability to control our gambling. We '
           'know that no real compulsive gambler ever regains control. All of us felt at times we were regaining '
           'control, such intervals – usually brief – were inevitably followed by still less control, which led in '
           'time to pitiful and incomprehensible demoralization. We are convinced that gamblers of our type are in the '
           'grip of a progressive illness. Over any considerable period of time we get worse, never '
           'better.</p><p>Therefore, in order to lead normal happy lives, we try to practice to the best of our '
           'ability, certain principles in our daily affairs.</p>',
  'sections': [{'type': 'text',
                'html': '<p>Gamblers Anonymous was founded in 1957 by Jim W., who used his experience in Alcoholics '
                        'Anonymous as the foundation in forming GA into a 12 step program. First Group Meeting was '
                        'held on September 13, 1957 in Los Angeles, California and was attended by 13 people. Now GA '
                        'has groups in all 50 states and all over the world.</p><p>Gamblers Anonymous members use the '
                        '20 Questions. as a guide to determine whether they are compulsive gamblers.</p>'},
               {'type': 'heading', 'text': 'Here are some key aspects of GA'},
               {'type': 'items',
                'items': [{'label': 'Peer Support',
                           'html': 'Members share their experiences, struggles, and successes, providing a supportive '
                                   'community for those affected by gambling addiction.'},
                          {'label': 'Anonymity',
                           'html': 'Anonymity is a core principle, creating a safe space where individuals can discuss '
                                   'their feelings and experiences without fear of stigma.'},
                          {'label': 'Meetings',
                           'html': 'GA holds regular meetings, both in-person and online, where participants can '
                                   'discuss their gambling issues and support each other.'},
                          {'label': 'Literature',
                           'html': 'GA provides literature, including pamphlets and books, that outlines the steps of '
                                   'recovery and offers guidance.'},
                          {'label': '12-Step Program',
                           'html': 'The program encourages personal reflection, accountability, and the development of '
                                   'coping strategies.'},
                          {'label': 'No Fees',
                           'html': 'Membership is free, and there are no dues or fees associated with attending '
                                   'meetings.'}]},
               {'type': 'heading', 'text': 'Core Values and Philosophy'},
               {'type': 'text',
                'html': '<h3>Anonymity and Confidentiality:</h3><ul><li><strong>Anonymity</strong> is one of the '
                        'cornerstones of Gamblers Anonymous. It ensures that members feel safe sharing their '
                        'experiences without fear of judgment or repercussions. In GA, you are known only by your '
                        'first name or a pseudonym if you choose. The focus is on mutual support and not on individual '
                        'identity.</li><li><strong>Confidentiality</strong> is paramount. What is shared in a meeting '
                        'stays in the meeting, and this creates an environment of trust, which is critical for the '
                        'recovery process.</li></ul>'},
               {'type': 'text',
                'html': '<h3>The Importance of Fellowship:</h3><ul><li>GA emphasizes <strong>fellowship</strong> and '
                        'mutual support. Many members find that the shared experiences of others help them feel '
                        'understood and less alone. In many cases, recovery is not just about abstaining from gambling '
                        'but also about rebuilding relationships and finding a healthier social network.</li><li>The '
                        'fellowship is also a source of accountability. Many members describe how having a supportive '
                        'group to lean on helps them stay on track with their recovery goals.</li></ul>'},
               {'type': 'text',
                'html': '<h3>Personal Responsibility:</h3><ul><li>While the 12-step program emphasizes reliance on a '
                        'higher power (as each individual understands it), GA also encourages personal responsibility '
                        'in recovery. Members are encouraged to take full responsibility for their actions and work '
                        'actively towards their recovery.</li><li>This includes making amends where possible, '
                        'recognizing and working through triggers and emotions that lead to gambling, and learning '
                        'healthier coping strategies.</li></ul>'},
               {'type': 'text',
                'html': '<h3>Spiritual Growth:</h3><ul><li>The <strong>spiritual aspect</strong> of GA is about '
                        'finding a sense of meaning and purpose beyond gambling. The “higher power” concept is not '
                        'restricted to any specific religion but can be understood in a more general sense—whether '
                        'that’s a belief in God, the universe, or the collective strength of the group. For '
                        'non-religious individuals, this step is often interpreted as focusing on self-improvement or '
                        'a deeper connection to the world around them.</li><li>Many members report a sense of inner '
                        'peace and renewed purpose as they progress through the steps and align their values with '
                        'those of the program.</li></ul>'},
               {'type': 'text',
                'html': '<h3>Surrender and Acceptance:</h3><ul><li>One of the key principles of GA is surrendering to '
                        'the fact that gambling is uncontrollable for those who have an addiction. This acceptance is '
                        'vital in the recovery process. It’s not about denying the urge to gamble but about '
                        'recognizing that gambling cannot be controlled by willpower alone.</li><li>Step 1—“We '
                        'admitted we were powerless over gambling—that our lives had become unmanageable”—represents '
                        'this step of acceptance. Only by admitting their powerlessness can individuals begin to move '
                        'forward in their recovery journey.</li></ul>'}],
  'source_url': 'https://powayrecoverycenter.org/ga/'},
 {'slug': 'sa',
  'name': 'Sexaholics Anonymous',
  'short': 'SA',
  'image': 'images/programs/photos/sa.jpg',
  'intro': '<p>Sexaholics Anonymous is a fellowship of men and women who share their experience, strength, and hope '
           'with each other that they may solve their common problem and help others to recover. The only requirement '
           'for membership is a desire to stop lusting and become sexually sober. There are no dues or fees for SA '
           'membership; we are self-supporting through our own contributions. SA is not allied with any sect, '
           'denomination, politics, organization, or institution; does not wish to engage in any controversy; neither '
           'endorses nor opposes any causes. Our primary purpose is to stay sexually sober and help others to achieve '
           'sexual sobriety.</p>',
  'sections': [{'type': 'heading', 'text': 'Here are some key aspects of SA'},
               {'type': 'items',
                'items': [{'label': '12-Step Program',
                           'html': 'Similar to Alcoholics Anonymous, SA follows a 12-step framework that emphasizes '
                                   'personal growth, accountability, and support from peers.'},
                          {'label': 'Anonymity',
                           'html': 'Maintaining confidentiality is crucial, allowing members to share their '
                                   'experiences without fear of judgment.'},
                          {'label': 'Higher Power',
                           'html': 'The program encourages individuals to connect with a higher power, which can be '
                                   'understood in a personal way, to aid in recovery.'},
                          {'label': 'Meetings',
                           'html': 'Regular meetings provide a supportive environment for members to share their '
                                   'struggles and successes.'},
                          {'label': 'Literature',
                           'html': 'SA has specific literature that outlines its principles, including “The White '
                                   'Book,” which describes the program and its approach to recovery.'},
                          {'label': 'Sponsorship',
                           'html': 'Members often find sponsors—more experienced individuals in recovery—who guide '
                                   'them through the program.'},
                          {'label': 'Service',
                           'html': 'Participation in service work is encouraged, reinforcing the idea of helping '
                                   'others as a way to maintain one’s own recovery.'},
                          {'label': 'Personal Inventory',
                           'html': 'Members are encouraged to take a moral inventory to understand their behaviors and '
                                   'patterns, facilitating personal growth.'}]},
               {'type': 'heading', 'text': 'Philosophy'},
               {'type': 'items',
                'items': [{'label': 'Recovery through Fellowship',
                           'html': 'SA believes that sharing experiences and supporting one another is essential for '
                                   'healing. The collective strength of the group helps individuals confront their '
                                   'issues and find hope.'},
                          {'label': 'Personal Responsibility',
                           'html': 'Members are encouraged to take responsibility for their actions and their recovery '
                                   'journey. This includes recognizing the impact of their behaviors on themselves and '
                                   'others.'},
                          {'label': 'Spiritual Growth',
                           'html': 'The program emphasizes the importance of a spiritual connection, which can be '
                                   'understood individually. This spirituality is not tied to any specific religion '
                                   'but encourages personal exploration of faith and values.'},
                          {'label': 'Continuous Improvement',
                           'html': 'Recovery is viewed as a lifelong journey. Members are encouraged to continually '
                                   'reflect on their behaviors, seek personal growth, and strive for sexual '
                                   'sobriety.'}]},
               {'type': 'heading', 'text': 'Principles'},
               {'type': 'items',
                'items': [{'label': 'Anonymity',
                           'html': 'The principle of anonymity creates a safe space for members to share openly '
                                   'without fear of judgment or exposure.'},
                          {'label': 'Acceptance',
                           'html': 'Members are encouraged to accept their struggles with sexual addiction and '
                                   'recognize their powerlessness over it, which is the first step toward recovery.'},
                          {'label': 'Service to Others',
                           'html': 'Helping others is a fundamental principle. By serving others, members reinforce '
                                   'their own recovery and contribute to the community.'},
                          {'label': 'Integrity and Honesty',
                           'html': 'Honesty with oneself and others is crucial. Members are encouraged to conduct a '
                                   'personal inventory and address dishonesty in their lives.'},
                          {'label': 'Humility',
                           'html': 'Acknowledging the need for help and being open to guidance from a higher power and '
                                   'others in the fellowship is essential for growth.'},
                          {'label': 'Spiritual Principles',
                           'html': 'The program encourages the practice of spiritual principles such as love, '
                                   'forgiveness, and compassion, both for oneself and others.'}]}],
  'source_url': 'https://powayrecoverycenter.org/sa/'}]

_BY_SLUG = {p["slug"]: p for p in PROGRAMS}


def program_list():
    """ Every group, for links and menus """
    return [{"slug": p["slug"], "name": p["name"], "short": p["short"], "image": p["image"]} for p in PROGRAMS]


def program(slug):
    """ One group's full page, or None """
    return _BY_SLUG.get(slug)
