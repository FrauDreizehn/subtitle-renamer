import os
from difflib import SequenceMatcher
import re
from pathlib import Path
import argparse

def clean_filename(filename):
    """Remove common patterns and clean filename for better matching."""
    # Remove extension
    name = os.path.splitext(filename)[0]
    # Remove common patterns like resolution, quality markers
    name = re.sub(r'\b\d{3,4}p?\b', '', name, flags=re.IGNORECASE)  # Remove resolution like 720p
    name = re.sub(r'\b(HD|SD|HQ)\b', '', name, flags=re.IGNORECASE)  # Remove quality markers
    # Remove special characters and convert to lowercase
    name = re.sub(r'[._-]', ' ', name)
    return name.lower().strip()

def similarity_ratio(str1, str2):
    """Calculate similarity ratio between two strings."""
    return SequenceMatcher(None, str1, str2).ratio()

def find_matching_pairs(video_dir):
    """Find matching video and subtitle files."""
    # Convert string path to Path object
    video_path = Path(video_dir)
    
    # Get all video and subtitle files
    video_files = [f.name for f in video_path.glob('*') if f.suffix.lower() in ('.mp4', '.mkv', '.avi')]
    srt_files = [f.name for f in video_path.glob('*.srt')]
    
    pairs = []
    for srt in srt_files:
        best_match = None
        best_ratio = 0
        clean_srt = clean_filename(srt)
        
        for video in video_files:
            clean_video = clean_filename(video)
            ratio = similarity_ratio(clean_srt, clean_video)
            
            if ratio > best_ratio:
                best_ratio = ratio
                best_match = video
        
        if best_match and best_ratio > 0.3:  # Adjust threshold as needed
            pairs.append((srt, best_match))
    
    return pairs

def rename_subtitles(video_dir, dry_run=True):
    """Rename subtitle files to match their corresponding videos."""
    video_path = Path(video_dir)
    pairs = find_matching_pairs(video_dir)
    
    for srt, video in pairs:
        # Keep the .srt extension but use video filename
        new_name = os.path.splitext(video)[0] + '.srt'
        old_path = video_path / srt
        new_path = video_path / new_name
        
        if dry_run:
            print(f"Would rename: {srt} -> {new_name}")
        else:
            try:
                old_path.rename(new_path)
                print(f"Renamed: {srt} -> {new_name}")
            except OSError as e:
                print(f"Error renaming {srt}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Rename subtitle files to match video filenames.')
    parser.add_argument('directory', nargs='?', default='.', 
                       help='Directory containing the video and subtitle files (default: current directory)')
    parser.add_argument('--execute', action='store_true',
                       help='Execute the renaming (without this flag, will only show preview)')
    
    args = parser.parse_args()
    
    # First run in preview mode
    if not args.execute:
        print("Preview of changes (dry run):")
        rename_subtitles(args.directory, dry_run=True)
        print("\nTo perform the actual renaming, run the script with --execute")
    else:
        print("Performing actual renaming:")
        rename_subtitles(args.directory, dry_run=False)
