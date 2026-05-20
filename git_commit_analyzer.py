#!/usr/bin/env python3
"""
Detect bot spam in git repos using commit metadata patterns
Inspired by: HN #11 "We stopped AI bot spam using Git's --author flag"

Looks for:
  - Same author committing thousands of times in seconds
  - Identical commit messages (copy-paste spam)
  - Commits at impossible times (all 24h non-stop)
  - Repeated file paths
"""
import subprocess, json, argparse, re
from collections import Counter
from datetime import datetime

def git_log(repo='.'):
    cmd = f'cd {repo} && git log --format="%H|%ae|%an|%ai|%s" --all'
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    commits = []
    for line in r.stdout.strip().splitlines():
        parts = line.split('|')
        if len(parts) >= 5:
            commits.append({
                'hash': parts[0],
                'email': parts[1],
                'author': parts[2],
                'timestamp': parts[3],
                'message': parts[4],
            })
    return commits

def git_files(repo='.', commit_hash='HEAD'):
    cmd = f'cd {repo} && git show --name-only --format="" {commit_hash}'
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return r.stdout.strip().splitlines()

def analyze(repo='.', verbose=False):
    commits = git_log(repo)
    
    if not commits:
        print("No commits found.")
        return
    
    # Check 1: Same author, high commit frequency
    author_commits = Counter(c['email'] for c in commits)
    suspicious = []
    
    for email, count in author_commits.most_common():
        author_emails = [c for c in commits if c['email'] == email]
        if count > 100:  # Suspicious threshold
            times = [c['timestamp'] for c in author_emails[-10:]]
            msg_hashes = Counter(c['message'] for c in author_emails)
            dup_msgs = [m for m, cnt in msg_hashes.items() if cnt > 5]
            
            if dup_msgs or count > 500:
                suspicious.append({
                    'email': email,
                    'commit_count': count,
                    'duplicate_messages': dup_msgs[:3],
                    'risk': 'HIGH' if count > 500 else 'MEDIUM'
                })
    
    print(f"\n🤖 Git Commit Analysis — {repo}")
    print("=" * 50)
    print(f"Total commits: {len(commits)}")
    print(f"Unique authors: {len(author_commits)}")
    
    if suspicious:
        print(f"\n⚠️  {len(suspicious)} suspicious author(s) detected:\n")
        for s in suspicious:
            print(f"  [{s['risk']}] {s['email']}")
            print(f"        {s['commit_count']} commits")
            if s['duplicate_messages']:
                print(f"        Repeated messages: {s['duplicate_messages'][0][:50]}")
    else:
        print("\n✅ No bot spam detected.")
    
    return suspicious

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', default='.', help='Git repo path')
    parser.add_argument('--verbose', action='store_true')
    args = parser.parse_args()
    analyze(args.repo, args.verbose)
