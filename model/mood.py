""" Mood Room rooms and keyword matching (data only, no database table)

Each room lists the keywords that lead to it. A keyword matches at the start of a word, so "anxious"
also matches "anxiously" but "happy" does not match "unhappy" (which has its own keyword).
The room with the most keyword hits wins; ties go to the room listed first, so safety rooms come first.
"""
import re


def music_url(term):
    return "https://music.apple.com/us/search?term=" + term.replace(" ", "%20")


ROOMS = [
    {
        "id": "crisis",
        "keys": ["suicide", "suicidal", "kill myself", "end my life", "end it all", "want to die", "self harm",
                 "self-harm", "hurt myself", "cutting", "no reason to live", "overdose"],
        "label": "A room for right now",
        "title": "You deserve support from a real person right now.",
        "desc": "What you are carrying sounds very heavy. Please call or text 988 to reach the Suicide & Crisis "
                "Lifeline any time, day or night. If you are in immediate danger, call 911.",
        "music": "Soft ambient",
        "music_desc": "Quiet, low-stimulation sound to keep nearby while you reach out.",
        "music_term": "soft ambient",
        "prompt": "Pick up your phone and dial or text 988. You can say, “I’m not okay and I need someone to talk to.”",
    },
    {
        "id": "craving",
        "keys": ["withdraw", "craving", "crave", "urge", "relapse", "using again", "drinking", "drunk", "get high", "getting high",
                 "detox", "shaky", "sweating", "sick"],
        "label": "A room for steadiness",
        "title": "Your body deserves care and attention.",
        "desc": "Physical discomfort and urges can be exhausting. Urges rise and fall like waves. If you are "
                "experiencing withdrawal or concerning symptoms, seek medical guidance rather than trying to push through alone.",
        "music": "Nature sounds",
        "music_desc": "Simple environmental sound with minimal stimulation.",
        "music_term": "nature sounds",
        "prompt": "Check the basics: water, a safe place to sit, a supportive person, and whether you need urgent medical help.",
    },
    {
        "id": "panic",
        "keys": ["panic", "anxious", "anxiety", "racing", "overwhelm", "spiraling", "spiralling", "can't breathe",
                 "heart pounding", "freaking out"],
        "label": "A room for settling",
        "title": "Let’s make the next minute smaller.",
        "desc": "Your system may be carrying a lot of activation. You do not have to solve everything right now. "
                "Try reducing stimulation and orienting to the room around you.",
        "music": "Ambient piano",
        "music_desc": "Soft instrumental music for a slower pace.",
        "music_term": "ambient piano",
        "prompt": "Look around and name three neutral objects. Let your eyes move slowly rather than forcing a deep breath.",
    },
    {
        "id": "nervous",
        "keys": ["nervous", "worried", "worry", "uneasy", "jittery", "on edge", "tense", "butterflies", "apprehensive"],
        "label": "A room for calming",
        "title": "Nerves are your body getting ready, not a sign you will fail.",
        "desc": "Nervousness often shows up before something that matters to you. You can let the feeling be "
                "there and still take the next small step.",
        "music": "Calming music",
        "music_desc": "Slow, gentle tracks to bring your heart rate down.",
        "music_term": "calming music",
        "prompt": "Breathe out a little longer than you breathe in, five times. Then name the very next small step you will take.",
    },
    {
        "id": "scared",
        "keys": ["scared", "afraid", "fear", "frightened", "terrified", "unsafe", "danger"],
        "label": "A room for safety",
        "title": "Let’s start by checking that you are safe.",
        "desc": "Fear is trying to protect you. If you are in danger, call 911. If the danger is a feeling more "
                "than a situation, it can help to remind your body where you are right now.",
        "music": "Soothing strings",
        "music_desc": "Warm, steady instrumental music that feels protective.",
        "music_term": "soothing strings",
        "prompt": "Say quietly: “Right now I am in ___, it is ___ o’clock, and in this moment I am ___.”",
    },
    {
        "id": "angry",
        "keys": ["angry", "anger", "mad", "furious", "irritated", "rage", "pissed", "resent", "trigger"],
        "label": "A room for creating space",
        "title": "You can pause without dismissing what happened.",
        "desc": "Anger often carries information about boundaries, hurt, or overload. You can honor the feeling "
                "while choosing a response that protects you.",
        "music": "Low-tempo focus",
        "music_desc": "Steady instrumental sound for a reset.",
        "music_term": "low tempo instrumental",
        "prompt": "Put one sentence between the feeling and the action: “I am angry, and I can wait ten minutes before deciding.”",
    },
    {
        "id": "frustrated",
        "keys": ["frustrated", "frustrating", "annoyed", "fed up", "stuck", "nothing works", "can't figure"],
        "label": "A room for loosening up",
        "title": "Being stuck is a moment, not a verdict.",
        "desc": "Frustration builds when effort is not paying off yet. A short break or a smaller version of the "
                "problem often helps more than pushing harder.",
        "music": "Lo-fi beats",
        "music_desc": "Relaxed, steady beats to take the pressure off.",
        "music_term": "lofi beats",
        "prompt": "Shrink the task: what is a version of this that would take five minutes?",
    },
    {
        "id": "stressed",
        "keys": ["stress", "pressure", "deadline", "too much", "busy", "swamped", "burnt out", "burned out", "burnout"],
        "label": "A room for unloading",
        "title": "You are allowed to set some of this down.",
        "desc": "When everything feels urgent, nothing gets your full attention. Choosing one thing to focus on "
                "is not giving up on the rest.",
        "music": "Relaxing jazz",
        "music_desc": "Easygoing jazz to soften a long day.",
        "music_term": "relaxing jazz",
        "prompt": "Write down everything on your mind, then circle only one thing to do in the next hour.",
    },
    {
        "id": "grief",
        "keys": ["grief", "grieving", "loss", "lost someone", "passed away", "died", "funeral", "miss them", "mourning"],
        "label": "A room for remembering",
        "title": "Grief is love that has nowhere to go right now.",
        "desc": "There is no correct way or timeline to grieve. Some moments will be heavier than others, and "
                "that is not a sign you are doing it wrong.",
        "music": "Gentle classical",
        "music_desc": "Tender, unhurried pieces to sit with what you feel.",
        "music_term": "gentle classical",
        "prompt": "Think of one small memory of who or what you lost. Let yourself hold it for a few breaths.",
    },
    {
        "id": "lonely",
        "keys": ["lonely", "alone", "isolated", "no one", "nobody", "left out", "disconnected", "abandoned"],
        "label": "A room for connection",
        "title": "You do not have to carry this in isolation.",
        "desc": "Loneliness can make reaching out feel like work. A small connection counts: a text, a shared "
                "space, or simply sitting near someone safe.",
        "music": "Acoustic comfort",
        "music_desc": "Gentle acoustic songs for companionship.",
        "music_term": "acoustic comfort",
        "prompt": "Write one person’s name. You do not have to contact them yet; just consider what you might say if you did.",
    },
    {
        "id": "sad",
        "keys": ["sad", "unhappy", "feeling down", "feel down", "depressed", "blue", "cry", "hopeless", "empty", "heartbroken",
                 "miserable", "numb", "feeling low"],
        "label": "A room for comfort",
        "title": "It is okay to not be okay right now.",
        "desc": "Sadness asks us to slow down. You do not need to fix it immediately. Small comforts, like a warm "
                "drink or fresh air, still count.",
        "music": "Comforting acoustic",
        "music_desc": "Soft songs that keep you company without forcing a mood change.",
        "music_term": "comforting acoustic songs",
        "prompt": "Name one small comfort within reach right now, and give yourself permission to have it.",
    },
    {
        "id": "ashamed",
        "keys": ["ashamed", "shame", "guilt", "guilty", "embarrassed", "regret", "failure", "worthless", "hate myself"],
        "label": "A room for self-compassion",
        "title": "A hard moment does not define who you are.",
        "desc": "Shame tells us we are the problem. Guilt says we did something we want to repair. Both can be "
                "met with the kindness you would offer a friend.",
        "music": "Warm soul",
        "music_desc": "Gentle, reassuring vocals.",
        "music_term": "warm soul music",
        "prompt": "Write what you would say to a close friend who told you this. Then read it back to yourself.",
    },
    {
        "id": "tired",
        "keys": ["tired", "exhausted", "drained", "fatigue", "sleepy", "worn out", "no energy", "wiped"],
        "label": "A room for resting",
        "title": "Rest is part of recovery, not a reward for it.",
        "desc": "Exhaustion makes everything feel harder. If you can, let this be a moment of rest rather than "
                "one more thing to push through.",
        "music": "Restful ambient",
        "music_desc": "Slow, spacious sound to help your body rest.",
        "music_term": "restful ambient",
        "prompt": "Let your shoulders drop and your jaw unclench. Rest your eyes for one minute.",
    },
    {
        "id": "sleepless",
        "keys": ["can't sleep", "cant sleep", "insomnia", "awake", "sleepless", "nightmare", "up all night"],
        "label": "A room for winding down",
        "title": "You do not have to force sleep to get some rest.",
        "desc": "Lying awake is frustrating. Resting quietly with low light still helps your body, even when sleep "
                "does not come right away.",
        "music": "Sleep music",
        "music_desc": "Soft, slow tracks for the middle of the night.",
        "music_term": "sleep music",
        "prompt": "Starting at your toes, relax each part of your body one at a time, moving slowly upward.",
    },
    {
        "id": "confused",
        "keys": ["confused", "lost", "unsure", "don't know", "dont know", "uncertain", "foggy", "mixed up", "torn"],
        "label": "A room for clearing",
        "title": "You do not need the whole answer today.",
        "desc": "Uncertainty is uncomfortable, but you only need enough clarity for the next step, not the whole path.",
        "music": "Focus instrumental",
        "music_desc": "Clear, uncluttered music for sorting your thoughts.",
        "music_term": "focus instrumental",
        "prompt": "Finish this sentence: “The one thing I do know right now is…”",
    },
    {
        "id": "bored",
        "keys": ["bored", "boring", "restless", "nothing to do", "idle", "unmotivated", "meh"],
        "label": "A room for spark",
        "title": "Boredom can be a door to something new.",
        "desc": "In recovery, boredom can be a risky moment. Filling it with something small and engaging can shift "
                "your whole afternoon.",
        "music": "Feel-good indie",
        "music_desc": "Bright, catchy songs to get you moving.",
        "music_term": "feel good indie",
        "prompt": "Pick one: take a ten-minute walk, text a friend, or try a meeting on the schedule this week.",
    },
    {
        "id": "happy",
        "keys": ["happy", "joy", "joyful", "great", "excited", "amazing", "wonderful", "glad", "cheerful", "elated",
                 "good day", "awesome", "fantastic"],
        "label": "A room for celebrating",
        "title": "Let yourself soak this in.",
        "desc": "Good moments matter in recovery. Noticing them, even briefly, helps your mind remember that they "
                "are possible.",
        "music": "Upbeat music",
        "music_desc": "Feel-good, upbeat songs to match your energy.",
        "music_term": "upbeat happy music",
        "prompt": "Name what made today good, and who you might share it with.",
    },
    {
        "id": "proud",
        "keys": ["proud", "accomplished", "milestone", "sober", "clean", "days sober", "chip", "anniversary", "achieved",
                 "made it"],
        "label": "A room for recognizing progress",
        "title": "This is worth celebrating.",
        "desc": "Progress in recovery is built one day at a time. Take a moment to recognize the effort that got you here.",
        "music": "Celebration anthems",
        "music_desc": "Big, uplifting songs for a win.",
        "music_term": "celebration anthems",
        "prompt": "Write down one thing you did differently that helped you get here.",
    },
    {
        "id": "hopeful",
        "keys": ["hope", "hopeful", "motivated", "inspired", "determined", "ready", "optimistic", "fresh start",
                 "new beginning"],
        "label": "A room for momentum",
        "title": "Hold onto this feeling and give it a direction.",
        "desc": "Hope is a powerful starting point. Turning it into one concrete plan helps it last past today.",
        "music": "Uplifting pop",
        "music_desc": "Energizing songs with forward motion.",
        "music_term": "uplifting pop",
        "prompt": "What is one step you can take this week to build on this feeling?",
    },
    {
        "id": "grateful",
        "keys": ["grateful", "thankful", "blessed", "appreciate", "lucky", "gratitude"],
        "label": "A room for gratitude",
        "title": "Gratitude grows when we stay with it.",
        "desc": "Noticing what is going right does not erase what is hard, but it gives you something steady to stand on.",
        "music": "Feel-good soul",
        "music_desc": "Warm, joyful songs to carry the feeling.",
        "music_term": "feel good soul",
        "prompt": "List three things you are grateful for today, as small or as big as they are.",
    },
    {
        "id": "calm",
        "keys": ["calm", "peaceful", "relaxed", "content", "okay", "fine", "chill", "serene", "at ease"],
        "label": "A room for staying grounded",
        "title": "Steady moments are worth noticing too.",
        "desc": "Calm can feel unremarkable, but it is a good time to build habits and resources for harder days.",
        "music": "Chill acoustic",
        "music_desc": "Easy, mellow songs to keep the calm going.",
        "music_term": "chill acoustic",
        "prompt": "What helped you feel this way today? Write it down so you can return to it later.",
    },
]

DEFAULT_ROOM = {
    "id": "default",
    "label": "A room for whatever is here",
    "title": "You can begin without having the right words.",
    "desc": "There is no requirement to name your experience perfectly. Start with one thing you can notice: "
            "a sensation, a thought, or something you need.",
    "music": "Gentle instrumental",
    "music_desc": "A flexible starting point for a quieter environment.",
    "music_term": "gentle instrumental",
    "prompt": "Complete this sentence privately: “Right now, the smallest helpful thing might be…”",
}

# One regex per room: each keyword at a word start; curly apostrophes are normalized before matching
_PATTERNS = [(room, re.compile(r"\b(?:" + "|".join(re.escape(k) for k in room["keys"]) + ")")) for room in ROOMS]


def match_room(text):
    """ Returns the room (as sent to the frontend) whose keywords appear most often in text """
    text = (text or "").lower().replace("’", "'")
    best, best_hits = DEFAULT_ROOM, 0
    for room, pattern in _PATTERNS:
        hits = len(pattern.findall(text))
        if hits > best_hits:
            best, best_hits = room, hits
    return {
        "id": best["id"],
        "label": best["label"],
        "title": best["title"],
        "description": best["desc"],
        "music": best["music"],
        "music_description": best["music_desc"],
        "music_url": music_url(best["music_term"]),
        "prompt": best["prompt"],
    }


def keyword_count():
    return sum(len(room["keys"]) for room in ROOMS)
