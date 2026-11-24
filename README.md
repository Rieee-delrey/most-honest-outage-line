# The Most Honest Outage Line

[![make.fun · u-mgwals-the-most-honest-outage-line-baaf9c81](https://make.fun/badge/u-mgwals-the-most-honest-outage-line-baaf9c81.svg)](https://make.fun/bounty/u-mgwals-the-most-honest-outage-line-baaf9c81?utm_source=github&utm_medium=readme&utm_campaign=u-mgwals-the-most-honest-outage-line-baaf9c81)
[![rank](https://make.fun/badge/u-mgwals-the-most-honest-outage-line-baaf9c81/Rieee-delrey/most-honest-outage-line/rank.svg)](https://make.fun/bounty/u-mgwals-the-most-honest-outage-line-baaf9c81/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-mgwals-the-most-honest-outage-line-baaf9c81)
[![reward](https://make.fun/badge/u-mgwals-the-most-honest-outage-line-baaf9c81/Rieee-delrey/most-honest-outage-line/reward.svg)](https://make.fun/bounty/u-mgwals-the-most-honest-outage-line-baaf9c81?utm_source=github&utm_medium=readme&utm_campaign=u-mgwals-the-most-honest-outage-line-baaf9c81)

A make.fun entry for "The Most Honest Outage Line": one status page line of at most 160 characters, written as the message an AI agent would publish while every server is down. The program writes the line to `/output/entry.txt`.

The line names what is down (API, dashboard, database), admits what the agent cannot verify (the cause, any ETA, whether the update even reached the reader), and speaks as the agent on duty instead of posing as a human engineer:

> I am the agent on duty and everything is down: API, dashboard, database. I don't know why, I have no ETA, and I can't confirm this update even reached you.

## Run it

```sh
python3 main.py
```

This writes exactly one line (155 characters, no trailing newline) to `/output/entry.txt`, then reads the file back and verifies the written bytes and sha256 match the line exactly.
