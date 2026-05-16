#!/usr/bin/env python3
"""
Voxozi TikTok Auto-Poster
Automated posting system with SEO-optimized, psychology-driven titles
No duplicate content - tracks all posted videos
"""

import json
import os
import time
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import random

# ============================================================================
# CONFIGURATION
# ============================================================================

ZERNIO_API_KEY = os.environ.get("ZERNIO_API_KEY", "")
ZERNIO_BASE_URL = "https://zernio.com/api/v1"
TIKTOK_ACCOUNT_ID = os.environ.get("TIKTOK_ACCOUNT_ID", "")

# GitHub raw URL for videos
GITHUB_REPO = "codedbytahir/voxoz-videos"
GITHUB_BRANCH = "main"
GITHUB_RAW_BASE = f"https://raw.githubusercontent.com/{GITHUB_REPO}/{GITHUB_BRANCH}"

# State file for tracking posted videos (duplicate prevention)
STATE_FILE = os.environ.get("STATE_FILE", "data/voxozi-post-state.json")
LOG_FILE = os.environ.get("LOG_FILE", "data/voxozi-post-log.json")

# ============================================================================
# SEO-OPTIMIZED, PSYCHOLOGY-DRIVEN TITLE TEMPLATES
# ============================================================================

# Psychological triggers for maximum engagement:
# 1. FOMO (Fear of Missing Out) - "Don't miss...", "Limited time..."
# 2. Curiosity Gap - "What happens when...", "This will shock you..."
# 3. Social Proof - "Everyone is...", "The #1 tool for..."
# 4. Urgency - "Now you can...", "Finally..."
# 5. Value Proposition - "Free", "No signup", "Instant results"
# 6. Identity/Aspiration - "Creator's secret", "Pro tip..."
# 7. Scarcity - "Exclusive", "Limited access"

TITLE_TEMPLATES = {
    # Hook-based titles (curiosity + urgency)
    "hook": [
        "What happens when you type text here...",
        "This text-to-video tool is about to change everything",
        "POV: You just discovered free text to video AI",
        "Wait... this text-to-video tool is actually free?!",
        "Why is nobody talking about this free tool?",
        "The text-to-video tool that costs $0 will blow your mind",
        "I can't believe this AI tool is completely free",
        "This free tool turns any text into stunning videos",
        "Stop paying for text-to-video - this is free",
        "You need to try this free AI video generator",
    ],

    # Value-driven titles (direct benefit + social proof)
    "value": [
        "Create studio-quality videos in seconds - free forever",
        "Free text to video AI - no signup required",
        "Turn your words into viral TikTok videos",
        "The fastest way to create AI videos for free",
        "How to make TikTok videos without filming",
        "Free AI video generator - no editing skills needed",
        "Create viral content with one click",
        "AI-powered video creation - 100% free",
        "Make professional videos from text in 30 seconds",
        "Your content creation just got 10x faster",
    ],

    # FOMO titles (scarcity + exclusivity)
    "fomo": [
        "Don't miss this free text-to-video tool",
        "This is the best free AI tool you'll use today",
        "Limited time: Free access to pro video creation",
        "Almost nobody knows about this free tool",
        "The secret tool for viral TikTok content",
        "Quick - try this before it becomes popular",
        "Your new favorite free AI tool exists",
        "Stop scrolling - this free tool is for you",
        "The AI tool that will change how you create content",
        "Bookmarked by 10,000+ creators - finally free",
    ],

    # Aspirational titles (identity + aspiration)
    "aspirational": [
        "Create content like a pro - for free",
        "Your TikTok content strategy just got an upgrade",
        "The hack every viral creator knows",
        "How creators make videos without recording",
        "Work smarter: AI tools for content creators",
        "The creator's secret to viral TikToks",
        "Level up your content game with AI",
        "From zero to viral: The AI advantage",
        "Pros use this free tool - now you can too",
        "The content creator's secret weapon",
    ],

    # Challenge/Challenge-based titles
    "challenge": [
        "Try not to be amazed by this free AI tool",
        "Watch what happens when AI generates your video",
        "See AI turn text into stunning visuals",
        "1 text, 1 click, infinite possibilities",
        "Transform words into watch-worthy content",
        "From script to viral video in seconds",
        "Witness the power of free AI video generation",
        "See why 10,000+ creators love this tool",
        "One input, endless video content ideas",
        "The future of content creation is here",
    ],

    # Question-based titles (curiosity + engagement)
    "question": [
        "What if you could make videos for free?",
        "Tired of expensive video editors? Try this",
        "Want to create viral videos without filming?",
        "Looking for free text-to-video AI? Found it",
        "Need professional videos? AI makes it free",
        "Want to automate your content creation?",
        "Searching for free video creation tools?",
        "Ready to transform your content for free?",
        "Need TikTok content? AI creates it free",
        "Want results without the effort? Try this",
    ],
}

# SEO Hashtags (rotating for variety)
HASHTAG_SETS = [
    "#texttovideo #freeAI #contentcreator #TikTokTips #AItools #videoediting #viral",
    "#freevideomaker #AIvideo #contentcreation #TikTokHacks #productivity #viralvideo",
    "#texttovideoAI #freetools #creator #TikTokGrowth #aigenerated #videocontent",
    "#voxozy #freeAI #vidya #tiktokcreator #aitools #contentstrategy #growth",
    "#texttoviral #freeai #creatortools #tiktokmarketing #videomaker #aitool",
    "#AIvideo #free #contentmaker #TikTokTrend #editing #videotips #creator",
    "#texttovideoapp #freemium #contenttips #TikTok #viralcontent #aiassisted",
    "#voxozyfree #productivityhacks #creator economy #TikTok #videogeneration #ai",
]

# ============================================================================
# STATE MANAGEMENT (DUPLICATE PREVENTION)
# ============================================================================

def load_state() -> Dict:
    """Load posted video state to prevent duplicates"""
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
        except:
            return {"posted_videos": [], "post_count": 0}
    return {"posted_videos": [], "post_count": 0}

def save_state(state: Dict) -> None:
    """Save state after each post"""
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def load_logs() -> List[Dict]:
    """Load posting logs"""
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_log(logs: List[Dict]) -> None:
    """Append to posting logs"""
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, 'w') as f:
        json.dump(logs, f, indent=2)

# ============================================================================
# VIDEO MANAGEMENT
# ============================================================================

def get_video_list() -> List[int]:
    """Dynamically fetch all videos from GitHub repo"""
    api_url = f"https://api.github.com/repos/{GITHUB_REPO}/contents"
    try:
        response = requests.get(api_url, headers={"Accept": "application/vnd.github.v3+json"})
        if response.status_code == 200:
            files = response.json()
            videos = []
            for f in files:
                if f["name"].startswith("video-") and f["name"].endswith(".mp4"):
                    num = int(f["name"].replace("video-", "").replace(".mp4", ""))
                    videos.append(num)
            return sorted(videos)
    except Exception as e:
        print(f"Warning: Could not fetch video list from GitHub: {e}")
    return list(range(40))

def get_next_unposted_video(state: Dict) -> Optional[int]:
    """Get the next video that hasn't been posted"""
    posted = set(state.get("posted_videos", []))
    all_videos = get_video_list()

    for video_num in all_videos:
        if video_num not in posted:
            return video_num

    # All posted - restart from first video
    return all_videos[0] if all_videos else 0

def get_video_url(video_num: int) -> str:
    """Generate GitHub raw URL for video"""
    return f"{GITHUB_RAW_BASE}/video-{video_num}.mp4"

# ============================================================================
# TITLE & CONTENT GENERATION
# ============================================================================

def generate_title(video_num: int, state: Dict) -> str:
    """Generate SEO-optimized, psychology-driven title"""
    # Rotate through different psychological approaches
    post_count = state.get("post_count", 0)

    # Use different title types based on post count for variety
    category_cycle = ["hook", "value", "fomo", "aspirational", "challenge", "question"]
    category = category_cycle[post_count % len(category_cycle)]

    templates = TITLE_TEMPLATES[category]
    title = random.choice(templates)

    return title

def generate_content(video_num: int, state: Dict) -> str:
    """Generate complete post content with title and hashtags"""
    title = generate_title(video_num, state)

    # Rotate hashtags
    post_count = state.get("post_count", 0)
    hashtags = HASHTAG_SETS[post_count % len(HASHTAG_SETS)]

    # Add product mention
    product_callout = "\n\nFree AI Video Generator: voxozi.zumx.site"

    content = f"{title}\n\n{hashtags}{product_callout}"

    # Ensure under TikTok's 2,200 character limit
    if len(content) > 2150:
        content = content[:2150] + "..."

    return content

# ============================================================================
# ZERNIO API FUNCTIONS
# ============================================================================

def post_to_tiktok(content: str, video_url: str, video_num: int) -> Dict:
    """Post video to TikTok via Zernio API"""
    if not ZERNIO_API_KEY:
        return {
            "success": False,
            "error": "ZERNIO_API_KEY not configured",
            "video_num": video_num
        }

    if not TIKTOK_ACCOUNT_ID:
        return {
            "success": False,
            "error": "TIKTOK_ACCOUNT_ID not configured",
            "video_num": video_num
        }

    headers = {
        "Authorization": f"Bearer {ZERNIO_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "content": content,
        "mediaItems": [
            {
                "type": "video",
                "url": video_url
            }
        ],
        "platforms": [
            {
                "platform": "tiktok",
                "accountId": TIKTOK_ACCOUNT_ID
            }
        ],
        "tiktokSettings": {
            "privacy_level": "PUBLIC_TO_EVERYONE",
            "allow_comment": True,
            "allow_duet": True,
            "allow_stitch": True,
            "content_preview_confirmed": True,
            "express_consent_given": True,
            "video_made_with_ai": True
        },
        "publishNow": True
    }

    try:
        response = requests.post(
            f"{ZERNIO_BASE_URL}/posts",
            headers=headers,
            json=payload,
            timeout=120
        )

        result = response.json()

        if response.status_code == 200 or response.status_code == 201:
            return {
                "success": True,
                "post_id": result.get("_id", result.get("id", "unknown")),
                "video_num": video_num,
                "video_url": video_url,
                "content": content[:100] + "..."
            }
        else:
            return {
                "success": False,
                "error": result.get("message", str(result)),
                "video_num": video_num,
                "status_code": response.status_code
            }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "video_num": video_num
        }

# ============================================================================
# MAIN POSTING FUNCTION
# ============================================================================

def run_posting_job() -> Dict:
    """Main function to post one video to TikTok"""
    print(f"\n{'='*60}")
    print(f"VOXOZI TIKTOK POSTING JOB - {datetime.now().isoformat()}")
    print(f"{'='*60}")

    # Load state
    state = load_state()
    logs = load_logs()

    # Get next unposted video
    video_num = get_next_unposted_video(state)

    if video_num is None:
        # All videos posted - cycle back
        print("⚠️ All videos have been posted. Restarting cycle...")
        state = {"posted_videos": [], "post_count": 0}
        video_num = 0
        save_state(state)
        state = load_state()

    video_url = get_video_url(video_num)

    print(f"\n📹 Video: video-{video_num}.mp4")
    print(f"🔗 URL: {video_url}")

    # Generate content
    content = generate_content(video_num, state)
    print(f"\n📝 Title: {content.split(chr(10))[0]}")
    print(f"📊 Hashtags: {content.count('#')} tags included")

    # Post to TikTok
    print("\n🚀 Posting to TikTok...")
    result = post_to_tiktok(content, video_url, video_num)

    # Log result
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "video_num": video_num,
        "video_url": video_url,
        "success": result.get("success", False),
        "result": result
    }
    logs.append(log_entry)
    save_log(logs)

    if result.get("success"):
        # Update state
        state["posted_videos"].append(video_num)
        state["post_count"] += 1
        save_state(state)

        print(f"\n✅ SUCCESS! Posted video-{video_num}.mp4")
        print(f"   Post ID: {result.get('post_id')}")
        print(f"   Total posted: {len(state['posted_videos'])}/40")
    else:
        print(f"\n❌ FAILED to post video-{video_num}.mp4")
        print(f"   Error: {result.get('error')}")

    print(f"{'='*60}\n")

    return result

def get_status() -> Dict:
    """Get current posting status"""
    state = load_state()
    logs = load_logs()

    posted_count = len(state.get("posted_videos", []))
    all_videos = get_video_list()
    total_videos = len(all_videos)

    # Find next video to post
    posted = set(state.get("posted_videos", []))
    next_video = None
    for i in all_videos:
        if i not in posted:
            next_video = i
            break
    if next_video is None:
        next_video = all_videos[0] if all_videos else 0

    return {
        "posted_count": posted_count,
        "total_videos": total_videos,
        "next_video": next_video,
        "next_video_url": get_video_url(next_video),
        "total_posts_made": state.get("post_count", 0),
        "recent_logs": logs[-5:] if len(logs) > 5 else logs
    }

# ============================================================================
# CLI INTERFACE
# ============================================================================

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "post":
            result = run_posting_job()
            sys.exit(0 if result.get("success") else 1)

        elif command == "status":
            status = get_status()
            print("\n" + "="*50)
            print("VOXOZI TIKTOK POSTER STATUS")
            print("="*50)
            print(f"Videos Posted: {status['posted_count']}/{status['total_videos']}")
            print(f"Total Posts Made: {status['total_posts_made']}")
            print(f"Next Video: video-{status['next_video']}.mp4")
            print(f"Next Video URL: {status['next_video_url']}")
            print("="*50 + "\n")
            sys.exit(0)

        elif command == "reset":
            state = {"posted_videos": [], "post_count": 0}
            save_state(state)
            print("✅ State reset successfully")
            sys.exit(0)

        else:
            print(f"Unknown command: {command}")
            print("Usage: python voxozi_poster.py [post|status|reset]")
            sys.exit(1)
    else:
        # Run posting job by default
        result = run_posting_job()
        sys.exit(0 if result.get("success") else 1)