from fastapi import FastAPI, HTTPException
from app.schemas import PostCreate, PostResponse
from app.db import Post, create_db_and_tables, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield
app = FastAPI(lifespan=lifespan)

text_posts = {
    1: {
        "title": "Morning Run Thoughts",
        "content": "Went for a 5km run this morning and realized how consistent small habits can really change your mindset. Feeling energized for the day!",
    },
    2: {
        "title": "New Python Trick I Learned",
        "content": "Just discovered list comprehensions with conditional logic — makes my code so much cleaner. Why didn’t I use this earlier?",
    },
    3: {
        "title": "Coffee Shop Review",
        "content": "Tried a new coffee shop downtown today. Great ambience, decent espresso, but a bit overpriced. Still worth checking out once.",
    },
    4: {
        "title": "Weekend Getaway",
        "content": "Spent the weekend at the beach. No emails, no Slack, just waves and fresh air. Highly recommend unplugging once in a while.",
    },
    5: {
        "title": "Debugging Frustration",
        "content": "Spent 2 hours fixing a bug... turns out it was a missing comma. Classic developer moment.",
    },
    6: {
        "title": "Book Recommendation",
        "content": "Currently reading 'Atomic Habits' — super insightful on how tiny changes compound into real progress over time.",
    },
    7: {
        "title": "Gym Progress",
        "content": "Finally hit a new personal record on deadlifts today 💪 Hard work paying off!",
    },
    8: {
        "title": "Learning New Tech",
        "content": "Started exploring Docker today. Containerization seemed intimidating at first, but it's actually pretty neat.",
    },
    9: {
        "title": "Late Night Coding",
        "content": "There’s something oddly satisfying about coding at 2AM with music in the background. Productivity hits different.",
    },
    10: {
        "title": "Small Win Today",
        "content": "Managed to finish all my tasks before 5PM. Rare but satisfying feeling 😄",
    }
}

@app.get("/posts")
def get_all_posts(limit: int = None):
    if limit:
        return list(text_posts.values())[:limit]
    return text_posts

@app.get("/posts/{post_id}")
def get_post(post_id: int) -> PostResponse:
    if post_id not in text_posts:
        raise HTTPException(status_code=404, detail="Post not found")
    return text_posts.get(post_id)

@app.post("/posts")
def create_post(post: PostCreate) -> PostResponse:
    new_post = {"title": post.title, "content": post.content}
    text_posts[max(text_posts.keys()) + 1] = new_post
    return new_post