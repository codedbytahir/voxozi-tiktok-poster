# Voxozi TikTok Auto-Poster

Automated TikTok posting system using GitHub Actions. Posts 40 videos on a 2-hour schedule with SEO-optimized, psychology-driven titles.

## Features

- **Auto-cycling**: Posts 40 videos, then automatically restarts from video-0
- **Duplicate prevention**: Tracks all posted videos in state file
- **SEO-optimized titles**: 60+ title templates using psychological triggers
- **Variety**: Rotates through 8 different hashtag sets
- **Scheduled execution**: Runs every 2 hours via GitHub Actions
- **Manual trigger**: Can be triggered manually via workflow_dispatch

## Setup

### 1. Create a new repository

```bash
# Clone the repository
git clone https://github.com/codedbytahir/voxozi-tiktok-poster.git
cd voxozi-tiktok-poster
```

### 2. Add GitHub Secrets

In your repository, go to **Settings → Secrets and variables → Actions** and add:

| Secret Name | Value |
|------------|-------|
| `ZERNIO_API_KEY` | Your Zernio API key |
| `TIKTOK_ACCOUNT_ID` | Your TikTok account ID |

### 3. Initial State (Optional)

If you want to continue from where you left off, update `data/voxozi-post-state.json` with your current progress:

```json
{
  "posted_videos": [0, 1, 2, 3, 4],
  "post_count": 5
}
```

## Usage

### Automatic Posting

The workflow runs automatically every 2 hours. No manual intervention needed.

### Manual Trigger

Go to **Actions → Voxozi TikTok Auto-Poster → Run workflow** to trigger manually.

### Check Status

```bash
python3 scripts/voxozi_poster.py status
```

## File Structure

```
voxozi-tiktok-poster/
├── .github/
│   └── workflows/
│       └── post.yml          # GitHub Actions workflow
├── data/
│   ├── voxozi-post-state.json   # Tracks posted videos
│   └── voxozi-post-log.json     # Posting history
├── scripts/
│   └── voxozi_poster.py         # Main posting script
├── requirements.txt
└── README.md
```

## Workflow Schedule

- **Schedule**: Every 2 hours (`0 */2 * * *`)
- **Timeout**: 10 minutes per run
- **State persistence**: Commits state changes back to repo

## Title Templates

The system uses 6 categories of psychology-driven titles:
- Hook (curiosity + urgency)
- Value (direct benefit + social proof)
- FOMO (scarcity + exclusivity)
- Aspirational (identity + aspiration)
- Challenge (engagement through challenge)
- Question (curiosity + engagement)

## Support

For issues or questions, create an issue in the repository.