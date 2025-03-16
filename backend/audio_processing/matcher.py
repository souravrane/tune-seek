from collections import defaultdict, Counter
from models.database import db
from utils.logger import log_function

def create_hashes(fingerprint, tag_range=5):
    """Creates hashes from fingerprint peaks by pairing anchor points with nearby peaks."""
    hashes = list()

    for i in range(len(fingerprint) - 1):
        anchor_time, anchor_freq = fingerprint[i]

        # Pair with the next peak in the tag range
        for j in range(i + 1, min(i + tag_range, len(fingerprint))):
            target_time, target_freq = fingerprint[j]
            
            # Compute time difference
            delta_t = target_time - anchor_time

            # Create hash
            hash_value = (int(anchor_freq), int(target_freq), int(delta_t))
            hashes.append((hash_value, int(anchor_time)))  # Store with song offset time

    return hashes

def match_fingerprint(audio_hashes):
    """Finds best matching song using hashes and offset times."""
    match_scores = defaultdict(list)

    for query_hash, query_offset in audio_hashes:
        results = db.songs.find({"hash": query_hash}, {"title": 1, "offset_time": 1})
        
        for result in results:
            song = result["title"]
            song_offset = result["offset_time"]

            # Compute offset difference
            offset_diff = song_offset - query_offset
            match_scores[song].append(offset_diff)

    print("Matches ", match_scores)
    # Find and return the top 5 matching tunes based on the offset score
    matching_tunes = list()

    for song, offsets in match_scores.items():
        histogram = Counter(offsets)
        # Get the most common offset and its count
        if histogram:
            # Since peak_offset isn't used, directly get the count
            most_common = histogram.most_common(1)[0]
            peak_count = most_common[1]
            matching_tunes.append([peak_count, song])

    matching_tunes.sort(reverse=True)
    return matching_tunes[:3]

